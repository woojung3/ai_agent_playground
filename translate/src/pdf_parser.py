import fitz  # PyMuPDF
import re

def get_common_font_size(blocks):
    """Heuristically finds the most common font size on the page to identify body text."""
    font_sizes = {}
    for block in blocks:
        if 'type' in block and block['type'] == 0:  # Only consider text blocks
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span['size'])
                    font_sizes[size] = font_sizes.get(size, 0) + 1
    
    if not font_sizes:
        return 10.0 # Default if no text blocks found
    
    # Return the font size that appears most frequently
    return max(font_sizes, key=font_sizes.get)

def parse_pdf(pdf_path: str):
    """
    Parses a PDF file, analyzing its text blocks to identify structural elements
    like headings, paragraphs, code blocks, and lists based on font properties
    and layout. Image elements are included as placeholders but not translated.

    Args:
        pdf_path (str): The path to the PDF file.

    Yields:
        dict: A dictionary representing a structured content element, e.g.,
              {'type': 'heading', 'level': 2, 'content': '...'}
              {'type': 'paragraph', 'content': '...'}
              {'type': 'code', 'content': '...'}
              {'type': 'list_item', 'content': '...'}
              {'type': 'image', 'content': '![[image_p1_1.png]]'}
              {'type': 'caption', 'content': '_Figure 1: ..._'}
    """
    print(f"Analyzing PDF structure: {pdf_path}")
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract text blocks and image bounding boxes
        text_blocks_raw = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]
        image_list = page.get_images(full=True)

        # Prepare all elements for unified sorting
        all_elements_on_page = []
        for block in text_blocks_raw:
            # Add x0, y0 for sorting consistency if not already present
            block['x0'] = block['bbox'][0]
            block['y0'] = block['bbox'][1]
            all_elements_on_page.append(block)

        for img_index, img in enumerate(image_list):
            bbox = page.get_image_bbox(img)
            if bbox:
                image_elements = {
                    "type": "image_raw", # Temporary type to distinguish from text blocks
                    "bbox": bbox,
                    "y0": bbox.y0,
                    "x0": bbox.x0,
                    "image_filename": f"image_p{page_num + 1}_{img_index + 1}.png" # Unique filename
                }
                all_elements_on_page.append(image_elements)
        
        # Sort all elements by vertical, then horizontal position
        all_elements_on_page.sort(key=lambda b: (b['y0'], b['x0']))

        body_font_size = get_common_font_size([b for b in text_blocks_raw if 'type' in b and b['type'] == 0]) # Only use text blocks for body font size
        
        last_image_bbox = None
        for element_raw in all_elements_on_page:
            # Handle image elements
            if element_raw.get("type") == "image_raw":
                # Yield the structured image element, for now markdown_converter will filter it out
                yield {'type': 'image', 'content': f"![[{element_raw['image_filename']}]]"}
                last_image_bbox = element_raw["bbox"]
                continue

            # Process text blocks (type == 0 implicitly after filtering image_raw)
            if element_raw['type'] == 0:
                full_block_text = ""
                lines = element_raw.get("lines", [])
                if not lines:
                    continue

                first_span_in_block = None
                try:
                    # Find the first non-empty span for style analysis
                    for line in lines:
                        if line.get("spans"):
                            first_span_in_block = line["spans"][0]
                            break
                except (IndexError, KeyError):
                    pass # first_span_in_block remains None

                if first_span_in_block:
                    span_size = round(first_span_in_block['size'])
                    font_name = first_span_in_block['font'].lower()
                    # Check for italic flag for quotes
                    is_italic = bool(first_span_in_block['flags'] & 1) # fitz.TEXT_ITALIC is 1
                else: # Fallback for blocks with no discernible spans
                    span_size = body_font_size
                    font_name = "unknown"
                    is_italic = False

                for line in lines:
                    line_text = "".join([span["text"] for span in line.get("spans", [])])
                    full_block_text += line_text + "\n"
                full_block_text = full_block_text.strip()
                
                if not full_block_text:
                    continue

                # --- Heuristics for structure detection ---
                
                # Caption detection
                if last_image_bbox and \
                   element_raw['bbox'][1] > last_image_bbox[3] and \
                   (element_raw['bbox'][1] - last_image_bbox[3]) < 50: # proximity threshold
                    if re.match(r'^(Figure|Fig\.|Table)\s*\d+', full_block_text, re.IGNORECASE):
                        yield {'type': 'caption', 'content': f"_{full_block_text}_"}
                        last_image_bbox = None # Consume caption
                        continue
                last_image_bbox = None # Reset if no caption found or not close enough

                # Code block detection (monospace font or significant indentation)
                if 'mono' in font_name or 'courier' in font_name or \
                   (full_block_text.count('\n') > 1 and len(element_raw['lines'][0]['spans'][0]['text']) > 0 and element_raw['lines'][0]['spans'][0]['origin'][0] - element_raw['bbox'][0] > 20): # Indentation check
                    yield {'type': 'code', 'content': full_block_text}
                    continue

                # Heading detection (font size substantially larger than body text, and not a list)
                # Check for "Chapter X" or "Section X" patterns
                if re.match(r'^(Chapter|Section)\s\d+', full_block_text) or \
                   (span_size > body_font_size * 1.2 and not re.match(r'^[\*\-]?\s*(\d+\.)', full_block_text)):
                    if span_size > body_font_size * 1.5:
                        yield {'type': 'heading', 'level': 1, 'content': full_block_text}
                    elif span_size > body_font_size * 1.2:
                        yield {'type': 'heading', 'level': 2, 'content': full_block_text}
                    else:
                        yield {'type': 'heading', 'level': 3, 'content': full_block_text} # Fallback for slightly larger text
                    continue
                
                # List Item detection (bulleted or numbered)
                if re.match(r'^[\*\-]\s', full_block_text) or re.match(r'^\d+\.\s', full_block_text):
                    yield {'type': 'list_item', 'content': full_block_text}
                    continue

                # Quote detection (italic style or specific block formatting)
                if is_italic and len(full_block_text.splitlines()) > 1: # Basic heuristic for italic blocks as quotes
                    yield {'type': 'quote', 'content': full_block_text}
                    continue
                
                # Default to paragraph
                yield {'type': 'paragraph', 'content': full_block_text}
    
    print("PDF structure analysis complete.")