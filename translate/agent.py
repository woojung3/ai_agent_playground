import os
import time
import re
import itertools
import sys
import configparser # Import configparser

from src.pdf_parser import parse_pdf
from src.translator import Translator
from src.markdown_converter import format_element_to_markdown, stitch_markdown

class PdfTranslationAgent:
    """
    An agent to translate a PDF file into a structured, translated Markdown file.
    """
    MIN_CHUNK_SIZE = 3000 # Minimum character count for a translated chunk to be marked with start/end tags
    MAX_TRANSLATION_CHUNK_SIZE = 10000 # Max character count for chunks sent to LLM
    MAX_RETRIES = 5
    RETRY_DELAY_SECONDS = 5
    PROGRESS_FILE_NAME = "translation_progress.txt"
    def __init__(self, pdf_path, output_dir="output", model_name="gemini-2.5-flash", global_system_context="", base_system_prompt=""): # Added new parameters
        print(f"TRACE: Entering PdfTranslationAgent.__init__(pdf_path='{pdf_path}', output_dir='{output_dir}', model_name='{model_name}', global_system_context='{global_system_context[:50]}...', base_system_prompt='{base_system_prompt[:50]}...').") # Added new parameters
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.global_system_context = global_system_context # Store global system context
        self.translator = Translator(model_name=model_name, base_system_prompt=base_system_prompt) # Pass base_system_prompt
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Initialize an empty list to buffer translatable elements
        self._translation_batch_buffer = []
        self._translated_chunks_history = [] # History of translated chunks for context
        self.HISTORY_SIZE = 3 # Number of past chunks to keep for summary

    def _read_and_chunk_markdown(self, markdown_file_path, max_chunk_chars):
        print(f"TRACE: Entering PdfTranslationAgent._read_and_chunk_markdown(markdown_file_path='{markdown_file_path}', max_chunk_chars={max_chunk_chars}).")
        """
        Reads a markdown file and yields chunks of content for translation,
        attempting to break at natural markdown boundaries.
        """
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by two or more newlines to get logical blocks (paragraphs, lists, code blocks, headings)
        blocks = [block for block in re.split(r'\n{2,}', content) if block.strip()]

        current_chunk = []
        current_chunk_char_count = 0

        for block in blocks:
            # Estimate block size, adding 2 for potential newlines between blocks
            block_size_estimate = len(block) + 2 

            if current_chunk_char_count + block_size_estimate > max_chunk_chars and current_chunk:
                yield "\n\n".join(current_chunk)
                current_chunk = [block]
                current_chunk_char_count = block_size_estimate
            else:
                current_chunk.append(block)
                current_chunk_char_count += block_size_estimate
        
        # Yield any remaining chunk
        if current_chunk:
            yield "\n\n".join(current_chunk)

    def _generate_translation_summary(self):
        print("TRACE: Entering PdfTranslationAgent._generate_translation_summary().")
        """
        Generates a summary from the recent translation history to maintain context.
        """
        if not self._translated_chunks_history:
            return ""

        summary_text = "Previously translated content (for context):\n"
        # Concatenate recent chunks, possibly truncating if they are too long
        for i, chunk in enumerate(self._translated_chunks_history):
            summary_text += f"Chunk {i+1}: {chunk[:200]}...\n" # Take first 200 chars for summary
        return summary_text

    def _load_previous_translation_state(self, output_file_path, resume_index):
        print(f"TRACE: Entering PdfTranslationAgent._load_previous_translation_state(output_file_path='{output_file_path}', resume_index={resume_index}).")
        """
        Loads previously translated content and history for resuming.
        Returns (string of previous full markdown content, list of raw translated chunks for history).
        """
        previous_full_markdown_content = ""
        initial_history_chunks = []

        if os.path.exists(output_file_path) and resume_index > 0:
            with open(output_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            start_marker_pattern = r'\n# --- 번역된 청크 시작 ---\n'
            end_marker_pattern = r'\n# --- 번역된 청크 끝 (일관성 유지됨) ---\n'

            start_markers = [(m.start(), m.end()) for m in re.finditer(start_marker_pattern, content)]
            end_markers = [(m.start(), m.end()) for m in re.finditer(end_marker_pattern, content)]

            if len(start_markers) != len(end_markers):
                print(f"Warning: Unbalanced markers in {output_file_path}. Cannot reliably resume. Starting from the beginning.")
                return "", []
            
            # Ensure markers are correctly ordered and we have enough markers for resume_index
            if resume_index > len(start_markers):
                print(f"Warning: resume_index ({resume_index}) is greater than the number of completed chunks ({len(start_markers)}). Starting from the beginning.")
                return "", []

            last_valid_end_index = 0
            for i in range(resume_index): # Iterate only up to resume_index - 1
                start_match_start, start_match_end = start_markers[i]
                end_match_start, end_match_end = end_markers[i]

                if start_match_start > end_match_start: # Should not happen if previous check passed, but for safety
                    print(f"Warning: Malformed markers (start after end) in chunk {i}. Cannot reliably resume. Starting from the beginning.")
                    return "", []

                # Correctly extract raw translated chunk content - between start and end marker
                raw_translated_chunk = content[start_match_end:end_match_end].strip() 
                initial_history_chunks.append(raw_translated_chunk)
                if len(initial_history_chunks) > self.HISTORY_SIZE:
                    initial_history_chunks.pop(0)

                last_valid_end_index = end_match_end

            previous_full_markdown_content = content[:last_valid_end_index]

        return previous_full_markdown_content, initial_history_chunks



    def run(self):
        print("TRACE: Entering PdfTranslationAgent.run().")
        """
        Runs the full PDF to Markdown translation pipeline.
        """
        print(f"Starting agent for PDF: {self.pdf_path}")
        start_time = time.time()

        # Load translation progress
        resume_from_chunk_index = 0
        progress_file_path = os.path.join(self.output_dir, self.PROGRESS_FILE_NAME)
        if os.path.exists(progress_file_path):
            with open(progress_file_path, 'r', encoding='utf-8') as f:
                try:
                    loaded_index = f.read().strip()
                    if loaded_index: # Ensure it's not empty
                        resume_from_chunk_index = int(loaded_index)
                        print(f"Resuming translation from chunk index {resume_from_chunk_index}...")
                    else:
                        print(f"Warning: Progress file {progress_file_path} is empty. Starting from the beginning.")
                except ValueError:
                    print(f"Warning: Corrupted progress file at {progress_file_path}. Starting from the beginning.")
                except Exception as e:
                    print(f"Error loading progress file: {e}. Starting from the beginning.")
                    resume_from_chunk_index = 0
        
        # Phase 1: Generate Untranslated Markdown
        # 1. Parse PDF into structured elements
        elements = list(parse_pdf(self.pdf_path))
        print(f"PDF Parsed into {len(elements)} structural elements.")
        
        # 2. Format ALL elements to untranslated Markdown
        # This will use format_element_to_markdown on original elements.
        # The marker types (chunk_start_marker, chunk_end_marker, translated_markdown_chunk)
        # will not be present in 'elements' from parse_pdf, so format_element_to_markdown
        # will act as a simple formatter for original elements.
        untranslated_md_elements = [format_element_to_markdown(elem) for elem in elements]

        # 3. Stitch ALL untranslated markdown parts into a single document
        untranslated_markdown_content = stitch_markdown(untranslated_md_elements)
        
        # 4. Save this untranslated Markdown to a temporary file
        temp_untranslated_md_path = os.path.join(self.output_dir, "temp_untranslated_document.md")
        with open(temp_untranslated_md_path, 'w', encoding='utf-8') as f:
            f.write(untranslated_markdown_content)
        print(f"Untranslated markdown saved to {temp_untranslated_md_path}")

        # Define a system-wide context that applies to all translations
        global_system_context = self.global_system_context # Use from instance variable
        
        # Determine the final output path
        output_filename = os.path.splitext(os.path.basename(self.pdf_path))[0] + "_translated.md"
        output_path = os.path.join(self.output_dir, output_filename)

        # Load previous translation state if resuming
        translated_full_content_str, self._translated_chunks_history = self._load_previous_translation_state(output_path, resume_from_chunk_index)
        
        # Initialize the output file based on resume_from_chunk_index
        # If resuming, the file already contains the previous content.
        # If starting fresh, clear the file.
        if resume_from_chunk_index == 0:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("") # Clear the file

        # Prepare the chunk iterator, skipping already processed chunks if resuming
        chunk_iterator = self._read_and_chunk_markdown(temp_untranslated_md_path, max_chunk_chars=self.MAX_TRANSLATION_CHUNK_SIZE)
        
        # Convert the original_chunk_iterator to a list ONCE to get its length and make it reusable
        all_chunks_list = list(chunk_iterator) 
        print(f"DEBUG: Total number of chunks to process: {len(all_chunks_list)}.")
        
        # Create the resumed_chunk_iterator from the reusable list
        resumed_chunk_iterator = itertools.islice(all_chunks_list, resume_from_chunk_index, None)
        
        # Now iterate through the chunks and translate
        for chunk_num_relative, untranslated_chunk in enumerate(resumed_chunk_iterator):
            chunk_num = resume_from_chunk_index + chunk_num_relative # Calculate actual 0-based chunk index
            print(f"Translating chunk {chunk_num + 1} (length: {len(untranslated_chunk)} chars)...")
            
            # Generate summary from previously translated chunks
            translation_summary = self._generate_translation_summary()
            
            # Call translator with context
            translated_chunk = ""
            for attempt in range(self.MAX_RETRIES):
                try:
                    translated_chunk = self.translator.translate(
                        text=untranslated_chunk,
                        system_context=self.global_system_context, # Use from instance variable
                        translation_summary=translation_summary
                    )
                    break # Success, break out of retry loop
                except Exception as e:
                    print(f"Translation attempt {attempt + 1}/{self.MAX_RETRIES} failed for chunk {chunk_num + 1}: {e}")
                    if attempt < self.MAX_RETRIES - 1:
                        print(f"Retrying in {self.RETRY_DELAY_SECONDS} seconds...")
                        time.sleep(self.RETRY_DELAY_SECONDS) # Corrected typo here
                    else:
                        print(f"All {self.MAX_RETRIES} attempts failed for chunk {chunk_num + 1}.")
                        print("Translation terminated due to unrecoverable LLM error.")
                        # Clean up progress file to avoid resuming from a failed state
                        if os.path.exists(progress_file_path):
                            os.remove(progress_file_path)
                        sys.exit(1) # Terminate the program with an error code
            
            # Construct the chunk with markers to write
            chunk_with_markers = "\n# --- 번역된 청크 시작 ---\n" + translated_chunk + "\n# --- 번역된 청크 끝 (일관성 유지됨) ---\n"
            
            # Append the translated content to the output file
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(chunk_with_markers)
            
            # Save progress (index)
            with open(progress_file_path, 'w', encoding='utf-8') as f:
                f.write(str(chunk_num + 1))
            
            # Update translation history
            self._translated_chunks_history.append(translated_chunk)
            if len(self._translated_chunks_history) > self.HISTORY_SIZE:
                self._translated_chunks_history.pop(0) # Keep history limited
        
        # Finalization (no extra write needed as content is incrementally saved)
        # The file is already correctly finalized as content is appended.
        
        print(f"Final translated markdown saved to {output_path}")
        
        end_time = time.time()
        print("\n--- Agent Finished ---")
        print(f"Total processing time: {end_time - start_time:.2f} seconds")
        print(f"Translated file: {output_path}")

def main():
    print("TRACE: Entering main().")
    """Main function to run the agent."""

    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    pdf_file_path_from_config = config['Translation']['pdf_path']
    global_system_context_from_config = config['Translation']['global_system_context']
    base_system_prompt_from_config = config['TranslatorPrompt']['base_system_prompt']

    # Use the configured pdf_file_path
    if not os.path.exists(pdf_file_path_from_config):
        print(f"Error: PDF file not found at '{pdf_file_path_from_config}' specified in config.ini")
        print("Please make sure the PDF is in the same directory as the agent or the path is correct.")
        return

    # Pass base_system_prompt to translator, and global_system_context and pdf_path to agent
    agent = PdfTranslationAgent(
        pdf_path=pdf_file_path_from_config,
        model_name="gemini-2.5-flash",
        global_system_context=global_system_context_from_config, # Pass to agent
        base_system_prompt=base_system_prompt_from_config # Pass to agent to then pass to translator
    )
    agent.run()

if __name__ == '__main__':
    main()
