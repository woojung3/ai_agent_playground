import re

def format_element_to_markdown(element: dict) -> str:

    """
    Formats a single structured content element into a Markdown string.
    Handles headings, code blocks, paragraphs, list items, quotes, and captions.
    Returns an empty string for image elements as per user's request to suppress them.
    """
    elem_type = element["type"]

    if elem_type == "chunk_start_marker":
        return "\n# --- 번역된 청크 시작 ---\n"
    
    if elem_type == "chunk_end_marker":
        return "# --- 번역된 청크 끝 (일관성 유지됨) ---\n"
    
    content = element["content"] # Moved this line here, after marker checks

    if elem_type == "translated_markdown_chunk":
        return f"{content}\n" # Return the pre-formatted translated markdown directly

    if elem_type == "heading":
        return f"\n{'#' * element['level']} {content}\n"
    
    if elem_type == "code":
        # clean up potential leading/trailing newlines and wrap in backticks
        return f"\n```\n{content.strip()}\n```\n"

    if elem_type == "paragraph":
        # Add extra newline for paragraph separation in markdown
        return f"{content}\n"
    
    if elem_type == "list_item":
        # List items already formatted by parser with leading bullet/number
        return f"{content}\n"
        
    if elem_type == "quote":
        # Prefix each line with '> ' for markdown quote format
        quoted_content = "\n> ".join(content.strip().split('\n'))
        return f"\n> {quoted_content}\n"

    if elem_type == "caption":
        return f"{content}\n"
    
    if elem_type == "image":
        # User requested to suppress image output
        return "" # Return empty string for image placeholders
    
    return content # Fallback for unexpected types

def stitch_markdown(elements):
    """
    Stitches a list of markdown-formatted elements into a single document,
    cleaning up excessive whitespace.
    """
    full_markdown = "\n".join(elements)
    
    # Clean up excessive newlines
    full_markdown = re.sub(r'\n{3,}', '\n\n', full_markdown)
    
    return full_markdown
