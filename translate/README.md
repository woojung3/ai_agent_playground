# PDF to Markdown Translator Agent

This project provides a Python agent to translate PDF documents into Markdown format, specifically tailored for technical documentation. It supports incremental translation, allowing for robust handling of interruptions and retries for API calls.

## Features

*   **PDF Parsing**: Extracts structured content from PDF files.
*   **Markdown Conversion**: Formats extracted content into Markdown.
*   **Gemini API Integration**: Utilizes Google Gemini for high-quality English to Korean translation.
*   **Robust Resume Functionality**: Automatically saves progress and resumes translation from the last completed chunk upon restart, even after interruptions.
*   **Retry Mechanism**: Implements retries for failed translation API calls to handle transient errors.
*   **Configurable**: System prompts, base translator prompt, and input PDF path are configurable via `config.ini`.
*   **Korean Document Formatting**: Translates adhering to specific Korean technical document formatting guidelines.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd translate
    ```
2.  **Install dependencies**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Set up Gemini API Key**:
    Obtain your `GEMINI_API_KEY` from [Google AI Studio](https://ai.google.dev/). Set it as an environment variable:
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```
    (On Windows, use `set GEMINI_API_KEY="YOUR_API_KEY"`)

## Configuration

Edit the `config.ini` file in the project root to configure the agent's behavior:

```ini
[Translation]
pdf_path = sw_architecture_with_cpp.pdf
global_system_context = This document is about Software Architecture with C++. Translate in a formal and professional tone.

[TranslatorPrompt]
base_system_prompt = """
    You are a professional translator specializing in technical IT documents.
    Translate the following text from English to Korean (ko).
    - Maintain a consistent, formal, and professional tone.
    - Ensure that technical terms like 'C++', 'SOLID', 'DRY', 'microservices', 'architecture' are translated consistently.
    - Preserve all original Markdown formatting in the translated output, including:
        - Headings (#, ##, ###, etc.)
        - Bold (**text**) and italics (*text*)
        - Blockquotes (> text)
        - Code blocks (```code```) and inline code (`code`)
        - Lists (bulleted/numbered)
        - Specific syntax for notes/warnings (e.g., >[!note])
        - Image references (e.g., ![[filename.png]])
    - Follow these specific Korean document formatting guidelines:
        - When using bulleted lists (itemize), do not use periods (.) at the end of sentences.
        - Use bulleted lists (itemize) rather than numbered lists (enumerate).
        - Sentences should end in noun form (e.g., ~함, ~것, ~관리).
    - Format the output as plain text without any additional commentary.
    """
```

*   **`pdf_path`**: The relative path to the input PDF file to be translated.
*   **`global_system_context`**: A high-level context for the entire document, passed to the Gemini model for consistent translation.
*   **`base_system_prompt`**: The core instructions for the Gemini model, defining its role, task, tone, terminology handling, and detailed Markdown formatting rules.

## Usage

To run the translation agent:

```bash
source .venv/bin/activate
python3 agent.py
```

The translated Markdown will be saved to `output/<original_pdf_filename>_translated.md`.
Translation progress is saved in `output/translation_progress.txt`, allowing for seamless resumption.

## Notes and Limitations

*   **Gemini API Quota**: Be mindful of your Gemini API usage quotas. Exceeding them will result in `429 Quota Exceeded` errors and temporary termination of the translation process. You may need to wait for the quota to reset or upgrade your plan.
*   **`google.generativeai` FutureWarning**: You might see a `FutureWarning` regarding the `google.generativeai` package. This is a library-specific message indicating a deprecation and does not affect the agent's functionality. It's recommended to migrate to the `google.genai` package as suggested in the warning.
*   **Image Handling**: Currently, images embedded in the PDF are processed as references (`![[filename.png]]`) in the markdown. The agent does not extract and save image files separately.
*   **PDF Layout Complexity**: While the PDF parser attempts to extract structured elements, extremely complex PDF layouts or non-standard formatting might lead to less accurate Markdown conversion.

## Contributing

(Section for contributing guidelines - add if applicable)
