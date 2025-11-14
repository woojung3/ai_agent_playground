import typer
from typing_extensions import Annotated
import os
import re
import glob

from ailoy import Runtime, APIModel, Agent

app = typer.Typer()

# --- Constants ---
OUTPUT_DIR = "presentation_gen/output"
SAMPLES_DIR = "presentation_gen/samples"
DEFAULT_STYLE_GUIDE_FILE = "style_guide.md"

# This utility function is borrowed from tc_gen/main.py
_current_llm_model_id = "gemini-2.5-pro"

def _call_llm_with_fallback(rt: Runtime, api_key: str, prompt: str, system_message_for_agent: str = None) -> str:
    global _current_llm_model_id  # Declare intent to modify global variable

    for model_fallback_attempt in range(2):  # Loop for model fallback (pro -> flash)
        for retry_503_attempt in range(5):  # Loop for 503 retries (up to 5 times)
            try:
                agent = Agent(rt, APIModel(id=_current_llm_model_id, api_key=api_key), system_message=system_message_for_agent)
                full_response_content = ""
                response_iterator = agent.query(prompt)

                # print("--- LLM Response Stream Debug --- DUMPING ALL RESPONSE OBJECTS ---")
                for resp in response_iterator:
                #     print(f"DEBUG: {resp}") # Print the full response object
                    if resp.type == "output_text":
                        full_response_content += resp.content
                # print("--- End of LLM Response Stream Debug ---")
                return full_response_content  # Success
            except Exception as e:
                error_message = str(e)
                if "overloaded" in error_message or "503" in error_message:
                    if retry_503_attempt < 4:  # Check if more retries are left (0, 1, 2, 3)
                        print(f"⚠️ Model is overloaded. Retrying attempt {retry_503_attempt + 2}/5 for model {_current_llm_model_id}...")
                        continue  # This will retry the inner loop
                    else:
                        # 503 retries exhausted for this model, break to trigger model fallback
                        print(f"❌ Model is still overloaded after 5 attempts for {_current_llm_model_id}.")
                        break  # break from inner loop
                elif "Quota exceeded" in error_message or "429" in error_message:
                    # Quota error, break inner loop immediately to trigger model fallback
                    print(f"⚠️ Quota exceeded for {_current_llm_model_id}.")
                    break  # break from inner loop
                else:
                    raise  # Other errors, fail immediately
        
        # This block is reached if the inner loop was broken (not returned from).
        # This means we either had a quota error or 503 retries were exhausted.
        # Time to fall back to the next model.
        if _current_llm_model_id == "gemini-2.5-pro":
            print(f"⚠️ Switching to gemini-2.5-flash and retrying...")
            _current_llm_model_id = "gemini-2.5-flash"
            # The outer loop will continue with the new model
        else:
            # We were already on the fallback model, and it failed.
            print(f"❌ Fallback model also failed. No further fallback available.")
            raise  # Re-raise the last exception
            
    raise Exception("Failed to get LLM response after all attempts and fallbacks.")


@app.command(name="create-style-guide")
def create_style_guide(
    samples_dir: Annotated[str, typer.Option(help="The directory containing example markdown files.")] = SAMPLES_DIR,
):
    """Analyzes sample presentation files and creates a detailed style guide."""
    print(f"✨ Analyzing samples from '{samples_dir}' to create a style guide.")

    # Hardcoded output path
    output_path = os.path.join(OUTPUT_DIR, "style_guide.md")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"  - Output will be saved to: {output_path}")

    sample_files = glob.glob(os.path.join(samples_dir, "*.md"))
    if not sample_files:
        print(f"❌ Error: No sample markdown files found in '{samples_dir}'.")
        raise typer.Exit(code=1)

    examples_content = ""
    for sample_file in sample_files:
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                content = f.read()
            filename = os.path.basename(sample_file)
            # Fixed typo in the end marker
            examples_content += f"--- EXAMPLE: {filename} ---\n{content}\n--- END EXAMPLE: {filename} ---\n\n"
        except Exception as e:
            print(f"⚠️ Warning: Could not read sample file {sample_file}. Skipping. Error: {e}")

    if not examples_content:
        print("❌ Error: Failed to read any sample files.")
        raise typer.Exit(code=1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set.")
        raise typer.Exit(code=1)

    rt = Runtime()
    try:
        system_message = "You are an expert technical writer specializing in creating documentation. Your task is to analyze several example presentation files and synthesize a comprehensive style guide in Markdown format."
        prompt = f'''
        You are an expert technical writer specializing in creating documentation. Your task is to analyze several example presentation files and synthesize a comprehensive style guide in Markdown format.

        The goal is to create a guide that a developer or another AI can use to create new presentations with a consistent look and feel.

        Here are the example presentation files:
        {examples_content}

        Please generate a detailed style guide with the following structure. For each section, analyze the provided examples and summarize the common patterns. If there are variations, describe them.

        # Presentation Style Guide (Obsidian Advanced Slides)

        ## 1. YAML Frontmatter
        - Describe the common key-value pairs found in the YAML frontmatter.
        - Example:
          - `theme`: (e.g., white, black)
          - `defaultTemplate`: (e.g., "[[tpl-base-no-title]]")
          - `transition`: (e.g., fade)
          - `slideNumber`: (e.g., c/t)

        ## 2. Global Styles (`<style>` block)
        - Summarize the CSS rules defined in the `<style>` block.
        - Mention imported fonts (e.g., Noto Sans KR, Source Code Pro).
        - Describe common styles for elements like `.reveal`, `h1`-`h6`, `p`, `li`, and any custom classes like `.code-block-fixed`.

        ## 3. Slide Structure
        ### 3.1. Slide Separation
        - Explain how individual slides are separated (e.g., using `---`).
        ### 3.2. Slide Templates
        - List the common slide templates used (e.g., `<!-- slide template="[[tpl-title]]" -->`).
        - Describe the structure of a title slide, including the `::: title`, `::: author`, and `::: date` blocks.
        - Describe the structure of standard content slides.
        ### 3.3. Slide Backgrounds and Modifiers
        - Explain how to set slide backgrounds or apply other modifiers (e.g., `<!-- .slide: bg="white" data-background-opacity="0.5" -->`).

        ## 4. Content Formatting
        ### 4.1. Text and Lists
        - Describe how standard text, lists, and blockquotes (`> [!quote]`) are used.
        ### 4.2. Code Blocks
        - Explain how code blocks are formatted, including language specification (e.g., ```java).
        ### 4.3. Footnotes
        - Describe the syntax for footnotes (e.g., `::: footnote`).
        ### 4.4. Images and Media
        - Explain how images are embedded and styled (e.g., `![[image.png|400]]`).

        ## 5. Mermaid Diagrams
        - If present, explain how Mermaid diagrams are included.

        Based on the provided examples, generate the complete and detailed style guide now. The output should be only the style guide content in Markdown format.
        '''

        # Add logging for prompt size
        print(f"ℹ️  Total prompt size: {len(prompt)} characters.")
        if len(prompt) > 500000: # Arbitrary large number for a warning
             print(f"⚠️ Warning: The prompt is very large. This may take a long time and could be truncated by the model.")

        print(f"🤖 Requesting LLM ({_current_llm_model_id}) to generate the style guide...")
        generated_style_guide = _call_llm_with_fallback(
            rt=rt,
            api_key=api_key,
            prompt=prompt,
            system_message_for_agent=system_message
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(generated_style_guide)

        print(f"📄 Successfully generated style guide: {output_path}")

    except Exception as e:
        print(f"❌ An error occurred during style guide generation: {e}")
        raise typer.Exit(code=1)
    finally:
        rt.stop()


@app.command()
def generate(
    draft_files: Annotated[list[str], typer.Argument(help="Path(s) to draft file(s). First file is main draft, others are context.")],
    output: Annotated[str, typer.Option(help="The filename for the output Markdown file.")] = "presentation.md",
):
    """Generates a presentation markdown file using LLM based on a style guide and a draft."""
    style_guide_file = os.path.join(OUTPUT_DIR, "style_guide.md")

    print(f"✨ Starting presentation generation...")
    print(f"  - Using default style guide: {style_guide_file}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output)
    print(f"  - Output File: {output_path}")

    # --- 1. Read input files ---
    try:
        with open(style_guide_file, 'r', encoding='utf-8') as f:
            style_guide_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Style guide file not found at {style_guide_file}")
        print("Please run the 'create-style-guide' command first.")
        raise typer.Exit(code=1)

    if not draft_files:
        print("❌ Error: No draft files provided.")
        raise typer.Exit(code=1)

    main_draft_file = draft_files[0]
    context_files = draft_files[1:]

    print(f"  - Main Draft File: {main_draft_file}")
    try:
        with open(main_draft_file, 'r', encoding='utf-8') as f:
            main_draft_content = f.read()
    except Exception as e:
        print(f"❌ Error reading main draft file {main_draft_file}: {e}")
        raise typer.Exit(code=1)

    context_content = ""
    if context_files:
        print("  - Contextual Files:")
        for context_file in context_files:
            print(f"    - {context_file}")
            try:
                with open(context_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    filename = os.path.basename(context_file)
                    context_content += f"--- CONTEXT FROM: {filename} ---\n{content}\n--- END CONTEXT FROM: {filename} ---\n\n"
            except Exception as e:
                print(f"⚠️ Warning: Could not read context file {context_file}. Error: {e}. Skipping.")

    # --- 2. Split draft into chunks by H1 headers ---
    chunks = re.split(r'(^\s*\$\$\$\$.*)', main_draft_content, flags=re.MULTILINE)
    if chunks and not chunks[0].strip():
        chunks = chunks[1:]
    
    chunk_instructions = []
    for i in range(0, len(chunks), 2):
        if i + 1 < len(chunks):
            chunk_instructions.append(chunks[i] + chunks[i+1])
        else:
            chunk_instructions.append(chunks[i])

    if not chunk_instructions:
        print("❌ Error: Could not find any chunks to process in the draft file. Make sure to use '#' headers as delimiters.")
        raise typer.Exit(code=1)

    # --- 3. Iteratively generate presentation --- 
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set.")
        raise typer.Exit(code=1)

    rt = Runtime()
    final_presentation_parts = []
    previously_generated_content = ""

    try:
        # --- Step 3.1: Generate Preamble (YAML + Style) ---
        print("🔄 Generating presentation preamble (YAML & Style)...")
        preamble_system_message = "You are a technical writer specializing in Obsidian Advanced Slides formatting."
        preamble_prompt = f"""Based on the `STYLE GUIDE`, generate the YAML frontmatter and the global `<style>` block for an Obsidian Advanced Slides presentation.
        The output should ONLY be the complete YAML block (starting with `---` and ending with `---`) followed by the `<style>` block. Do not add any other markdown or explanation.

        --- STYLE GUIDE ---
        {style_guide_content}
        --- END STYLE GUIDE ---
        """
        
        preamble = _call_llm_with_fallback(
            rt=rt,
            api_key=api_key,
            prompt=preamble_prompt,
            system_message_for_agent=preamble_system_message
        )
        # Replace the fenced yaml block with its content, keeping the rest.
        preamble = re.sub(r"```(yaml|markdown)\s*([\s\S]*?)\s*```", r"\2", preamble, count=1).strip()

        final_presentation_parts.append(preamble)
        previously_generated_content = preamble

        # --- Step 3.2: Generate Content Chunks ---
        for i, instruction in enumerate(chunk_instructions):
            print(f"🔄 Processing content chunk {i + 1}/{len(chunk_instructions)}...")
            
            system_message = "You are an expert technical writer continuing to build a presentation. Your task is to generate the next section of content, ensuring it logically follows the previously generated parts."
            prompt = f"""
            You are an expert technical writer continuing a presentation. Your primary goal is to generate the content for the sections described in `NEXT SECTION'S INSTRUCTIONS`.

            --- NEXT SECTION'S INSTRUCTIONS ---
            {instruction}
            --- END NEXT SECTION'S INSTRUCTIONS ---

            To complete this task, you must use the provided context. The instructions may require you to analyze source code or other documents found in the `ADDITIONAL CONTEXTUAL MATERIALS`. You must follow these instructions precisely.

            --- PRESENTATION SO FAR ---
            {previously_generated_content}
            --- END PRESENTATION SO FAR ---

            --- STYLE GUIDE ---
            {style_guide_content}
            --- END STYLE GUIDE ---

            --- ADDITIONAL CONTEXTUAL MATERIALS ---
            {context_content if context_content else "No additional context provided."}
            --- END ADDITIONAL CONTEXTUAL MATERIALS ---

            Now, generate ONLY the new markdown content for the sections described in the instructions. Ensure your output logically follows the `PRESENTATION SO FAR` and adheres to the `STYLE GUIDE`.

            **IMPORTANT INSTRUCTIONS FOR OUTPUT FORMAT:**
            1. The special combination header (string with $$$$, four dollars) in the `NEXT SECTION'S INSTRUCTIONS` is a comment for a delimiter. **DO NOT include this comment header in your output**. Your output should begin directly with content slides.
            2. Your output for this section **MUST start with a `---` slide separator** to connect it to the previous slide.
            3. All other markdown elements from the instructions, such as H2 headers (`##`) or lists, should be transformed into slides as appropriate, **maintaining their original heading levels**.
            """

            print(f"🤖 Requesting LLM ({_current_llm_model_id}) for chunk {i + 1}...")
            generated_chunk = _call_llm_with_fallback(
                rt=rt,
                api_key=api_key,
                prompt=prompt,
                system_message_for_agent=system_message
            )
            
            generated_chunk = generated_chunk.strip()
            # Per user request, the logic to unwrap markdown code blocks has been disabled
            # to prevent potential content truncation. The raw output from the LLM will be used directly.

            final_presentation_parts.append(generated_chunk)
            previously_generated_content += "\n\n" + generated_chunk

        # --- 4. Assemble and save the final presentation ---
        final_output = "\n".join(final_presentation_parts)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_output)

        print(f"📄 Successfully generated presentation: {output_path}")

    except Exception as e:
        print(f"❌ An error occurred during presentation generation: {e}")
        raise typer.Exit(code=1)
    finally:
        rt.stop()

    print("✅ Presentation generation finished successfully!")


if __name__ == "__main__":
    app()
