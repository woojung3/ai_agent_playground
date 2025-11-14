import typer
from typing_extensions import Annotated
import os
import sys

from product_plan_gen.plan_generator import ProductPlanGenerator

app = typer.Typer()

OUTPUT_DIR = "product_plan_gen/output"
TEMPLATE_DIR = "product_plan_gen/templates"

@app.command()
def generate(
    input_files: Annotated[list[str], typer.Argument(help="Path to the input files. The first should be the mermaid flowchart, followed by context files like intro.md.")],
):
    """
    Generates a Product Plan markdown files from a Mermaid event storming file and other context documents.
    """
    # Workaround for a typer bug where the command name is included in the arguments when run with `python -m`
    if input_files and input_files[0] == 'generate':
        input_files = input_files[1:]

    print("✨ Starting Product Plan generation...")
    
    if not input_files:
        print("❌ Error: No input files provided.")
        raise typer.Exit(code=1)

    main_input_file = input_files[0]
    context_files = input_files[1:]

    print(f"  - Main Input (Mermaid): {main_input_file}")
    if context_files:
        print("  - Context Files:")
        for f in context_files:
            print(f"    - {f}")
    else:
        print("  - No context files provided.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"  - Output files will be saved to: {OUTPUT_DIR}")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set.")
        raise typer.Exit(code=1)

    try:
        generator = ProductPlanGenerator(api_key=api_key, template_dir=TEMPLATE_DIR)
        
        major_files_for_review = [
            "00_main.md",
            "01_crs.md",
            "02_ia.md",
            "03_process_list.md",
            "05_policy_list.md",
            "07_screen_list.md",
            "08_screen_design.md",
        ]

        # Iterate over the generator and save each file as it's created
        for filename, content in generator.generate_full_plan(main_input_file, context_files, OUTPUT_DIR):
            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Successfully generated and saved: {output_path}")

            # human-in-the-loop checkpoint
            if filename in major_files_for_review:
                response = input(f"✋ Paused for review. Check '{output_path}'. Press Enter to continue, or type 'exit' to stop: ")
                if response.lower() == 'exit':
                    print("🛑 User requested to stop. Exiting.")
                    raise typer.Exit()
            
        print(f"\n✅ Product Plan generation complete. All sections saved to {OUTPUT_DIR}")

    except Exception as e:
        print(f"❌ An error occurred during plan generation: {e}")
        # In a real scenario, you might want to print the traceback
        # import traceback
        # traceback.print_exc()
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
