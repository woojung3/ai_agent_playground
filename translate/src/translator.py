import os
from google import genai

class Translator:
    """
    A class to handle text translation using the Gemini API.
    """
    def __init__(self, model_name="gemini-2.5-flash", base_system_prompt=""): # Added base_system_prompt
        print(f"TRACE: Entering Translator.__init__(model_name='{model_name}', base_system_prompt='{base_system_prompt[:50]}...').") # Added base_system_prompt to trace
        """
        Initializes the Translator.

        Args:
            model_name (str): The name of the Gemini model to use.
            base_system_prompt (str): The base system prompt for translation.
        """
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_system_prompt = base_system_prompt # Store base system prompt
        
        if self.api_key:
            self.client = genai.Client()
            print(f"Translator initialized with model '{self.model_name}'.")
        else:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please set it to use the Gemini API for translation.")

    def translate(self, text: str, target_lang: str = "ko", system_context: str = "", translation_summary: str = "") -> str:
        print(f"TRACE: Entering Translator.translate(len_text={len(text)}, target_lang='{target_lang}', has_system_context={bool(system_context)}, has_translation_summary={bool(translation_summary)}).")
        """
        Translates text to the target language.

        Args:
            text (str): The text to translate.
            target_lang (str): The target language code (e.g., 'ko' for Korean).
            system_context (str): Additional system-wide context for the translation.
            translation_summary (str): Summary of previously translated content for context.

        Returns:
            str: The translated text.
        """
        if not text.strip():
            return ""
        
        # Real translation logic with a system prompt for consistency
        try:
            # Use the instance variable base_system_prompt
            prompt_parts = [
                self.base_system_prompt
            ]
            if system_context:
                prompt_parts.append(system_context)
            if translation_summary:
                prompt_parts.append(translation_summary)
            
            prompt_parts.append(f"""Original Text:
---
{text}
---

Translated Text:
""")
            prompt = "\n\n".join(prompt_parts)
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            if not response.text:
                return "" # Return empty string for truly empty LLM response
            return response.text
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            raise # Re-raise the exception to trigger the retry mechanism in the agent
