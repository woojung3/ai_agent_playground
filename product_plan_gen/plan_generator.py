import os
import re
import json # Added this import
from ailoy import Runtime, APIModel, Agent
from .mermaid_parser import MermaidParser # Import the MermaidParser

# This utility function can be shared across agents
_thinking_model_id = "gemini-2.5-pro"
_fast_model_id = "gemini-2.5-flash"
_current_llm_model_id = _thinking_model_id

def _call_llm_with_fallback(rt: Runtime, api_key: str, prompt: str, system_message_for_agent: str = None) -> str:
    global _current_llm_model_id  # Declare intent to modify global variable

    for model_fallback_attempt in range(2):  # Loop for model fallback
        for retry_503_attempt in range(5):  # Loop for 503 retries (up to 5 times)
            try:
                print(f"ℹ️  Attempting to use model: {_current_llm_model_id}")
                agent = Agent(rt, APIModel(id=_current_llm_model_id, api_key=api_key), system_message=system_message_for_agent)
                full_response_content = ""
                response_iterator = agent.query(prompt)

                for resp in response_iterator:
                    if resp.type == "output_text":
                        full_response_content += resp.content
                return full_response_content  # Success
            except Exception as e:
                error_message = str(e)
                if "overloaded" in error_message or "503" in error_message or "Failed to read connection" in error_message:
                    if retry_503_attempt < 4:
                        print(f"⚠️ Model is overloaded or connection failed. Retrying attempt {retry_503_attempt + 2}/5 for model {_current_llm_model_id}...")
                        continue
                    else:
                        print(f"❌ Model is still overloaded after 5 attempts for {_current_llm_model_id}.")
                        break
                elif "Quota exceeded" in error_message or "429" in error_message:
                    print(f"⚠️ Quota exceeded for {_current_llm_model_id}.")
                    break
                else:
                    raise
        
        # Fallback logic (though it will just fall back to the same model)
        if _current_llm_model_id == "gemini-2.5-pro":
            print(f"⚠️ Switching to gemini-2.5-flash and retrying...")
            _current_llm_model_id = "gemini-2.5-flash"
        else:
            # Already on flash, so just indicate failure for this attempt
            print(f"❌ Model call failed for {_current_llm_model_id}. No further fallback available.")
            raise
            
    raise Exception("Failed to get LLM response after all attempts and fallbacks.")


class ProductPlanGenerator:
    global _current_llm_model_id  # Declare intent to modify global variable

    def __init__(self, api_key: str, template_dir: str):
        self.api_key = api_key
        self.template_dir = template_dir
        self.rt = Runtime()
        self.mermaid_parser = MermaidParser() # Initialize the parser

    def __del__(self):
        self.rt.stop()

    def _read_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"⚠️ Warning: File not found, skipping: {file_path}")
            return ""
        except Exception as e:
            print(f"⚠️ Warning: Could not read file {file_path}. Error: {e}")
            return ""

    def generate_full_plan(self, main_input_file: str, context_files: list[str], output_dir: str):
        # 1. Read main input and context files
        main_content = self._read_file_content(main_input_file)
        
        context_content = ""
        for file in context_files:
            context_content += f"--- CONTEXT FROM: {os.path.basename(file)} ---\n"
            context_content += self._read_file_content(file)
            context_content += f"\n--- END CONTEXT ---\n\n"

        # 2. Parse mermaid data
        parsed_mermaid_data = self.mermaid_parser.parse(main_content)
        mermaid_context_for_llm = json.dumps(parsed_mermaid_data, indent=2, ensure_ascii=False)

        # 3. Sequentially generate sections
        template_files = sorted([f for f in os.listdir(self.template_dir) if f.startswith('_') and f.endswith('.md')])
        
        previous_sections_context = ""
        
        # Helper to generate a single file
        def _generate_and_yield(template_filename, prompt_context, item_name=None, item_index=None):
            output_filename_base = template_filename.replace('_', '', 1).replace('.md', '')
            
            if item_index is not None:
                # For detail files, create numbered filenames
                output_filename = f"{output_filename_base}-{str(item_index + 1).zfill(3)}.md"
            else:
                output_filename = f"{output_filename_base}.md"

            output_path = os.path.join(output_dir, output_filename)

            if os.path.exists(output_path):
                print(f"⏩ Skipping already generated section: {output_path}")
                return self._read_file_content(output_path)

            template_path = os.path.join(self.template_dir, template_filename)
            template_content = self._read_file_content(template_path)
            
            # Add the specific item to the prompt if provided
            item_context = f"\n--- Current Item to Detail ---\n{item_name}\n" if item_name else ""

            prompt = f"""
You are an AI assistant specialized in generating product plan documentation.
Your task is to expand on the provided Markdown template using the given context.
{item_context}
--- Mermaid Flowchart Data ---
{mermaid_context_for_llm}

--- Additional Context Files ---
{context_content}

--- Previously Generated Sections ---
{prompt_context}

--- Current Section Template ({template_filename}) ---

{template_content}



Based on the above information, generate the content for the current section.

Ensure consistency with previously generated sections and leverage the Mermaid data.

Output only the Markdown content for this section.

"""

            # Add special instruction for list files to ensure JSON summary is generated

            if template_filename in ["_03_process_list.md", "_05_policy_list.md"]:

                prompt += """

IMPORTANT: After generating the markdown table, you MUST also fill in the `Summary for Automation` section with a valid JSON array of the generated items. This is critical for the next automation step.

"""



            print(f"🔄 Generating section: {output_filename}...")

            generated_text = _call_llm_with_fallback(self.rt, self.api_key, prompt)

            

            yield (output_filename, generated_text)

            return generated_text

        # Main generation loop
        i = 0
        while i < len(template_files):
            template_filename = template_files[i]
            
            # Skip detail templates, they are handled by their list counterparts
            if template_filename in ["_04_process_detail.md", "_06_policy_detail.md"]:
                i += 1
                continue

            # Generate the list file first
            list_content = ""
            # Use a temporary generator to avoid advancing the main one
            temp_gen = _generate_and_yield(template_filename, previous_sections_context)
            try:
                filename, content = next(temp_gen)
                yield (filename, content)
                list_content = content
            except StopIteration: # Happens if the file was skipped
                output_filename = template_filename.replace('_', '', 1).replace('.md', '.md')
                output_path = os.path.join(output_dir, output_filename)
                list_content = self._read_file_content(output_path)

            previous_sections_context += f"\n--- {template_filename.replace('_', '', 1)} ---\n{list_content}\n"

            # Special handling for list-detail generation
            detail_template_map = {
                "_03_process_list.md": "_04_process_detail.md",
                "_05_policy_list.md": "_06_policy_detail.md"
            }

            if template_filename in detail_template_map:
                _current_llm_model_id = _fast_model_id

                detail_template = detail_template_map[template_filename]
                # Find and parse the JSON summary block
                json_match = re.search(r'```json\s*([\s\S]*?)\s*```', list_content)
                items = []
                if json_match:
                    try:
                        summary_json = json.loads(json_match.group(1))
                        if template_filename == "_03_process_list.md":
                            items = [p.get("process_name") for p in summary_json.get("processes", []) if p.get("process_name")]
                        elif template_filename == "_05_policy_list.md":
                             items = [p.get("policy_name") for p in summary_json.get("policies", []) if p.get("policy_name")]
                    except json.JSONDecodeError:
                        print(f"⚠️ Warning: Could not decode JSON from {template_filename}. Skipping detail generation.")

                print(f"ℹ️  Found {len(items)} items in {template_filename} to generate details for.")

                # IMPORTANT: Use a fixed context that does NOT include previously generated details
                base_context_for_details = previous_sections_context

                for item_index, item in enumerate(items):
                    # Use a temporary generator for each detail file
                    detail_gen = _generate_and_yield(detail_template, base_context_for_details, item_name=item, item_index=item_index)
                    try:
                        # Yield the detail file content
                        yield next(detail_gen)
                    except StopIteration:
                        # This happens if the detail file was skipped, which is fine.
                        pass

                _current_llm_model_id = _thinking_model_id

            i += 1
