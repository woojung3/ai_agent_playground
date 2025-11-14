import typer
from typing_extensions import Annotated
import os
import json
import re
from glob import glob

from ailoy import Runtime, VectorStore, Agent, APIModel
from tc_gen.document_parser import extract_text_from_html
from tc_gen.tc_generator import create_tc_excel, read_tc_excel

app = typer.Typer()

# --- Constants ---
OUTPUT_DIR = "tc_gen/output" # Relative to the project root
KNOWLEDGE_BASE_FILENAME = os.path.join(OUTPUT_DIR, "knowledge_base.jsonl")

PARSE_SRS_SYSTEM_MESSAGE = "당신은 SRS 문서를 JSONL 형식으로 정확하게 파싱하는 전문가입니다. 각 요구사항은 ID, 요구사항 상세 설명, 유형(FR/NFR)을 포함해야 합니다."

UPDATE_SYSTEM_MESSAGE = """당신은 테스트 케이스 전문가입니다. 주어진 테스트 케이스를 분석하고, 사용자 요청에 따라 수정된 테스트 케이스를 JSON 형식으로 반환해야 합니다.
테스트 케이스의 구조는 다음과 같습니다:
{
  "id": "TC-{{요구사항ID}}-001",
  "title": "{{테스트 케이스 제목}}",
  "preconditions": [
    "{{사전 조건 1}}",
    "{{사전 조건 2}}"
  ],
  "test_steps": [
    {
      "step": 1,
      "action": "{{동작 1}}",
      "test_data": "{{테스트 데이터 1}}",
      "expected_result": "{{예상 결과 1}}"
    }
  ],
  "notes": "{{참고 사항}}"
}
"""

_current_llm_model_id = "gemini-2.5-pro" # Module-level variable to track preferred model

def _call_llm_with_fallback(rt: Runtime, api_key: str, prompt: str, system_message_for_agent: str = None) -> str:
    global _current_llm_model_id  # Declare intent to modify global variable

    for model_fallback_attempt in range(2):  # Loop for model fallback (pro -> flash)
        for retry_503_attempt in range(5):  # Loop for 503 retries (up to 5 times)
            try:
                agent = Agent(rt, APIModel(id=_current_llm_model_id, api_key=api_key), system_message=system_message_for_agent)
                full_response_content = ""
                response_iterator = agent.query(prompt)

                for resp in response_iterator:
                    if resp.type == "output_text":
                        full_response_content += resp.content
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


DEFAULT_TC_EXCEL_FILENAME = "test_cases.xlsx"
DEFAULT_SRS_JSONL_FILENAME = "srs.jsonl"
DEFAULT_SYSTEM_MESSAGE_FILE = os.path.join(OUTPUT_DIR, "system_message.md")


@app.command()
def parse(
    input_dir: Annotated[str, typer.Argument(help="The path to the directory containing HTML documents (e.g., Confluence export).")]
):
    global _current_llm_model_id # Declare intent to modify global variable
    """Parses all HTML documents, creates knowledge_base.jsonl, and generates a system_message.md summary."""
    print(f"🔍 Starting parsing of directory: {input_dir}")

    all_knowledge_chunks = []

    html_files = glob(os.path.join(input_dir, "**/*.html"), recursive=True)
    if not html_files:
        print(f"❌ Error: No HTML files found in {input_dir}")
        raise typer.Exit(code=1)

    for html_file_path in html_files:
        base_filename = os.path.basename(html_file_path)
        print(f"  Processing {base_filename}...")
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            general_chunks = extract_text_from_html(content, source_file=base_filename)
            all_knowledge_chunks.extend(general_chunks)
            print(f"    Extracted {len(general_chunks)} general chunks.")

        except Exception as e:
            print(f"❌ Error processing {base_filename}: {e}")

    try:
        with open(KNOWLEDGE_BASE_FILENAME, 'w', encoding='utf-8') as f:
            for chunk in all_knowledge_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
        print(f"\n📄 Successfully created knowledge base: {KNOWLEDGE_BASE_FILENAME} ({len(all_knowledge_chunks)} chunks).")
    except Exception as e:
        print(f"❌ Error writing knowledge_base.jsonl: {e}")
        raise typer.Exit(code=1)

    # Automatically generate system_message.md from the knowledge base
    print("\n🤖 Generating system_message.md from knowledge base...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not set. Skipping system_message.md generation.")
    else:
        rt = Runtime()
        try:
            knowledge_base_content = "\n".join([chunk['content'] for chunk in all_knowledge_chunks])
            
            max_kb_length = 128
            if len(knowledge_base_content) > max_kb_length*1024:
                print(f"⚠️ Knowledge base content is very large ({len(knowledge_base_content)} chars). Truncating to {max_kb_length} for prompt.")
                knowledge_base_content = knowledge_base_content[:max_kb_length*1024]

            system_message_prompt = f"""
            당신은 제공된 기술 문서를 분석하여, 테스트 케이스 생성 AI를 위한 컨텍스트 시스템 메시지를 생성하는 기술 문서 전문가입니다.
            주어진 Knowledge Base 내용을 바탕으로 `system_message.md` 파일의 전체 내용을 한국어로 생성해주세요.
            출력은 다른 설명 없이 완전한 마크다운 형식이어야 합니다.

            다음 구조와 지침을 정확히 따라주세요:

            # 테스트 케이스 생성을 위한 시스템 메시지

            ## 1. 제품 개요
            (Knowledge Base를 바탕으로 프로젝트에 대한 간결한 개요를 작성합니다. 주요 목적과 대상 사용자를 서술하고, 핵심 기능은 글머리 기호 목록으로 나열해주세요.)

            ## 2. 주요 용어 정의
            (Knowledge Base에서 중요한 기술 용어와 약어를 식별하고, 아래의 마크다운 정의 목록 형식을 사용하여 정의해주세요.)
            **예시 형식:**
            - **V2X**: Vehicle-to-Everything의 약자로, 차량이 주변의 모든 것과 통신하는 기술을 의미합니다.
            - **PKI**: Public Key Infrastructure의 약자로, 공개 키 암호 방식을 기반으로 하는 보안 인프라입니다.

            ## 3. 테스트 케이스 생성 가이드라인
            (아래 가이드라인을 그대로 사용하고, 절대 변경하지 마세요.)
            - 당신은 **ISTQB Advanced Level 자격증을 소지한 QA 전문가**입니다.
            - 각 요구사항에 대해 Positive 시나리오와 Negative 시나리오를 각각 1개씩 생성합니다.
            - 테스트 케이스 제목은 시나리오의 목적을 명확하게 설명하는 간결하고 서술적인 문구여야 합니다. 제목에 'Positive', 'Negative'와 같은 분류어를 포함하지 마세요.
            - 제공된 Knowledge Base 정보를 최대한 활용하여 현실적이고 효과적인 테스트 케이스를 작성하세요.
            - 테스트 단계는 사용자의 행동, 테스트 데이터, 그리고 예상되는 시스템의 반응을 명확하게 기술해야 합니다.

            ---
            ## 4. 소프트웨어 요구사항 명세서 (SRS)
            (이 섹션에는 다음 문구를 그대로 포함해주세요: "(이 섹션은 프로그램에 의해 SRS 파일의 내용가 자동으로 추가되는 영역입니다.)")

            ---
            사용할 Knowledge Base 내용은 다음과 같습니다:
            --- Knowledge Base ---
            {knowledge_base_content}
            --- END Knowledge Base ---

            이제 `system_message.md` 파일의 완전하고 최종적인 마크다운 콘텐츠를 생성해주세요.
            """

            generator_agent_system_message = "당신은 제공된 기술 문서 내용을 분석하여, 다른 AI를 위한 컨텍스트 시스템 메시지를 생성하는 전문가입니다."
            
            _current_llm_model_id = "gemini-2.5-flash"
            print(f"🤖 Requesting LLM ({_current_llm_model_id}) to generate system_message.md...")
            generated_system_message = _call_llm_with_fallback(
                rt=rt,
                api_key=api_key,
                prompt=system_message_prompt,
                system_message_for_agent=generator_agent_system_message
            )
            _current_llm_model_id = "gemini-2.5-pro"
            
            # Clean up potential markdown code blocks from the response
            match = re.search(r"```(markdown)?\s*([\s\S]*?)\s*```", generated_system_message, re.IGNORECASE)
            if match:
                generated_system_message = match.group(2)

            with open(DEFAULT_SYSTEM_MESSAGE_FILE, 'w', encoding='utf-8') as f:
                f.write(generated_system_message)
            
            print(f"📄 Successfully generated system message file: {DEFAULT_SYSTEM_MESSAGE_FILE}")

        except Exception as e:
            print(f"❌ An error occurred during system_message.md generation: {e}")
        finally:
            rt.stop()

    print("✨ Parsing completed successfully!")


@app.command(name="parse-srs")
def parse_srs(
    srs_md_file: Annotated[str, typer.Argument(help="The path to the manually created SRS Markdown file.")],
    output_file: Annotated[str, typer.Option(help="The filename for the output .jsonl file.")] = os.path.join(OUTPUT_DIR, DEFAULT_SRS_JSONL_FILENAME),
):
    """Parses a Markdown SRS file into a structured .jsonl format using LLM."""
    print(f"🔍 Parsing SRS Markdown file: {srs_md_file} using LLM...")
    
    try:
        with open(srs_md_file, 'r', encoding='utf-8') as f:
            srs_md_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: SRS Markdown file {srs_md_file} not found.")
        raise typer.Exit(code=1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set.")
        raise typer.Exit(code=1)

    rt = Runtime()
    try:
        system_message = PARSE_SRS_SYSTEM_MESSAGE
        user_prompt = f"""
        다음은 Markdown 형식의 SRS 문서입니다. 이 문서에서 각 기능 요구사항(FR)과 비기능 요구사항(NFR)을 추출하여 JSONL 형식으로 변환해주세요. 각 줄은 하나의 JSON 객체여야 하며, 다음 필드를 포함해야 합니다:
        - ID: 요구사항의 고유 식별자 (예: PV25-FR-01)
        - 요구사항 상세 설명: 요구사항의 전체 내용
        - type: 'FR' 또는 'NFR'

        --- SRS Markdown 문서 ---
        {srs_md_content}

        --- 출력 형식 ---
        각 요구사항은 한 줄의 JSON 객체로 출력해주세요. 예시:
        {{"ID": "PV25-FR-01", "요구사항 상세 설명": "인증서를 발급할 수 있어야 한다", "type": "FR"}}
        {{"ID": "PV25-NFR-01", "요구사항 상세 설명": "인증서 발급 성능: p95 latency ≤ 40 ms", "type": "NFR"}}
        """
        
        print(f"🤖 Requesting LLM ({_current_llm_model_id}) to parse SRS Markdown...")
        full_response_content = _call_llm_with_fallback(
            rt=rt,
            api_key=api_key,
            prompt=user_prompt,
            system_message_for_agent=system_message
        )
        
        # LLM 응답을 .jsonl 파일로 저장 (각 줄이 유효한 JSON인지 검증)
        lines = full_response_content.strip().split('\n')
        valid_json_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    json.loads(line) # Validate if it's a valid JSON
                    valid_json_lines.append(line)
                except json.JSONDecodeError:
                    print(f"⚠️ Warning: Skipping invalid JSON line in LLM response: {line}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(valid_json_lines))
        
        print(f"📄 Successfully parsed SRS Markdown to {output_file} ({len(valid_json_lines)} items).")

    except Exception as e:
        print(f"❌ An error occurred during LLM-powered SRS parsing: {e}")
        raise typer.Exit(code=1)
    finally:
        rt.stop()

    print("✨ SRS Markdown parsing completed successfully!")


@app.command()
def generate(
    srs_jsonl_file: Annotated[str, typer.Argument(help="The path to the parsed SRS .jsonl file.")],
    knowledge_base_file: Annotated[str, typer.Argument(help="The path to the knowledge base .jsonl file.")],
    output: Annotated[str, typer.Option(help="The filename for the output Excel file.")] = DEFAULT_TC_EXCEL_FILENAME,
    use_rag: Annotated[bool, typer.Option(help="Whether to use RAG (VectorStore) for context retrieval. Defaults to False.")] = False,
    system_message_file: Annotated[str, typer.Option(help="The path to the Markdown file containing the base system message.")] = DEFAULT_SYSTEM_MESSAGE_FILE,
):
    """Generate test cases for all SRS items in the parsed file."""
    print(f"Generating test cases from SRS: {srs_jsonl_file}")
    print(f"Using knowledge base: {knowledge_base_file}")
    print(f"Output will be saved to: {output}")

    srs_items_for_tc_gen = []
    try:
        with open(srs_jsonl_file, 'r', encoding='utf-8') as f:
            srs_items_for_tc_gen = [json.loads(line) for line in f]
        print(f"📄 Loaded {len(srs_items_for_tc_gen)} SRS items from {srs_jsonl_file}")
    except FileNotFoundError:
        print(f"❌ Error: SRS .jsonl file {srs_jsonl_file} not found.")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f"❌ Error reading SRS .jsonl file: {e}")
        raise typer.Exit(code=1)

    system_message_base = ""
    if os.path.exists(system_message_file):
        try:
            with open(system_message_file, 'r', encoding='utf-8') as f:
                system_message_base = f.read()
            print(f"📄 Loaded base system message from: {system_message_file}")
        except Exception as e:
            print(f"⚠️ Warning: Could not read system message file {system_message_file}. Proceeding without it. Error: {e}")
    else:
        print(f"⚠️ Warning: System message file {system_message_file} not found. Proceeding without a base message.")

    srs_content_for_system_message = "\n"
    for item in srs_items_for_tc_gen:
        srs_content_for_system_message += f"ID: {item.get('ID')}\n유형: {item.get('type')}\n상세 설명: {item.get('요구사항 상세 설명')}\n---\n"

    final_system_message = f"{system_message_base}\n{srs_content_for_system_message}"

    knowledge_chunks = []
    try:
        with open(knowledge_base_file, 'r', encoding='utf-8') as f:
            knowledge_chunks = [json.loads(line) for line in f]
        print(f"📄 Loaded {len(knowledge_chunks)} chunks from knowledge base.")
    except FileNotFoundError:
        print(f"❌ Error: Knowledge base file {knowledge_base_file} not found.")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f"❌ Error reading knowledge base file: {e}")
        raise typer.Exit(code=1)

    rt = Runtime()
    vs = None
    try:
        if use_rag:
            with VectorStore(rt, "BAAI/bge-m3", "faiss") as initialized_vs:
                vs = initialized_vs
                print("🤖 Building in-memory VectorStore from knowledge base... (This may take a while)")
                all_insert_items = []
                for chunk in knowledge_chunks:
                    document = chunk.get('content', '')
                    metadata = {'source_file': chunk.get('source_file'), 'type': chunk.get('type')}
                    embedding = vs.embedding(document)
                    all_insert_items.append({
                        "embedding": embedding,
                        "document": document,
                        "metadata": metadata,
                    })

                if all_insert_items:
                    vs._runtime.call_method(
                        vs._component_state.vector_store_name,
                        "insert_many",
                        {"items": all_insert_items},
                    )
                print("✅ VectorStore built.")
        else:
            print("⚠️ RAG is disabled. Using simple string matching for context retrieval.")

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("❌ Error: GEMINI_API_KEY environment variable not set.")
            raise typer.Exit(code=1)
        
        print("🧑‍💻 Agent initialized with enhanced system message.")
        final_tcs_to_write = {}

        if os.path.exists(output):
            print(f"📄 Loading existing test cases from {output}...")
            existing_tcs = read_tc_excel(output)
            for tc in existing_tcs:
                final_tcs_to_write[tc.get("id")] = tc
            print(f"📄 Loaded {len(existing_tcs)} existing test cases.")
            max_tc_id = 0
            for tc_id_str in final_tcs_to_write.keys():
                match = re.match(r"TC-(\d+)", tc_id_str)
                if match:
                    max_tc_id = max(max_tc_id, int(match.group(1)))
            tc_id_counter = max_tc_id + 1
            print(f"Starting TC ID counter from: {tc_id_counter}")
        else:
            tc_id_counter = 1
            print("No existing test cases found. Starting TC ID counter from 1.")

        for srs_item in srs_items_for_tc_gen:
            related_existing_tcs = [
                tc for tc in final_tcs_to_write.values() 
                if tc.get("srs_id") == srs_item.get("ID")
            ]
            
            if related_existing_tcs:
                related_existing_tc_ids = {tc.get("id") for tc in related_existing_tcs}
                print(f"⏩ Skipping TC generation for {srs_item.get('ID')}. Already found TCs: {', '.join(related_existing_tc_ids)}")
                continue
            print(f"\n✨ Generating TC for {srs_item.get('ID')}...")
            
            query_text = srs_item.get('요구사항 상세 설명')
            if query_text is None:
                query_text = srs_item.get('요구사항')
            context_str = ""

            if use_rag and vs is not None:
                retrieved_context = vs.retrieve(query_text, top_k=5)
                context_str = "\n".join([item.document for item in retrieved_context])
            else:
                matched_chunks = []
                for chunk in knowledge_chunks:
                    if query_text.lower() in chunk.get('content', '').lower():
                        matched_chunks.append(chunk.get('content', ''))
                
                if matched_chunks:
                    context_str = "\n".join(matched_chunks)
                    print(f"  - Found {len(matched_chunks)} matching chunks using simple string matching.")
                else:
                    print("  - No matching chunks found using simple string matching.")

            user_prompt = f"""
            다음 SRS 요구사항에 대해 테스트 케이스를 생성해주세요. 이 요구사항은 이미 시스템 메시지로 제공된 전체 SRS의 일부입니다.
            
            --- 현재 SRS 요구사항 ---
            ID: {srs_item.get('ID')}
            유형: {srs_item.get('type')}
            상세 설명: {query_text}
            
            --- 추가 참고 자료 (Knowledge Base) ---
            {context_str if context_str else "제공된 참고 자료 없음."}
            
            --- 테스트 케이스 생성 지시 ---
            위 요구사항과 참고 자료를 바탕으로, Positive 시나리오 1개와 Negative 시나리오 1개를 포함하여 총 2개의 테스트 케이스를 생성해주세요. 테스트 케이스 제목은 필수이며, 해당 테스트 케이스의 목적을 명확하게 설명하는 간결하고 서술적인 문구여야 합니다. 제목에 'Positive', 'Negative'와 같은 분류어를 포함하지 말고, 제목만으로 시나리오를 충분히 이해할 수 있도록 작성해주세요. 예를 들어, '성공적인 인증서 발급 요청' 또는 '정책 위반으로 인한 인증서 발급 요청 거절'과 같이 작성합니다. 각 테스트 케이스는 다음 JSON 형식에 맞춰 출력해야 합니다:
            
            ```json
            [
              {{
                "srs_id": "{srs_item.get('ID')}",
                "title": "{{테스트 케이스 제목}}",
                "preconditions": [
                  "{{사전 조건 1}}",
                  "{{사전 조건 2}}"
                ],
                "test_steps": [
                  {{
                    "step": 1,
                    "action": "{{동작 1}}",
                    "test_data": "{{테스트 데이터 1}}",
                    "expected_result": "{{예상 결과 1}}"
                  }},
                  {{
                    "step": 2,
                    "action": "{{동작 2}}",
                    "test_data": "{{테스트 데이터 2}}",
                    "expected_result": "{{예상 결과 2}}"
                  }}
                ],
                "notes": "{{참고 사항}}"
              }}
            ]
            ```
            
            JSON 형식으로만 응답해주세요.
            """

            print(f"🤖 Requesting LLM ({_current_llm_model_id}) to generate TC for {srs_item.get('ID')}...")
            full_response_content = _call_llm_with_fallback(
                rt=rt,
                api_key=api_key,
                prompt=user_prompt,
                system_message_for_agent=final_system_message
            )
            
            try:
                match = re.search(r"```(json)?\s*([\s\S]*?)\s*```", full_response_content)
                if match:
                    json_str = match.group(2)
                else:
                    json_str = full_response_content.strip()

                generated_tcs = json.loads(json_str)
                for tc in generated_tcs:
                    tc_id = f"TC-{tc_id_counter:03d}"
                    tc['id'] = tc_id
                    final_tcs_to_write[tc_id] = tc
                    tc_id_counter += 1
                    title_display = tc.get('title', 'No Title')
                    if not title_display.strip():
                        title_display = "(Empty Title)"
                    print(f"    - {tc['id']}: {title_display}")
                print(f"✅ Generated {len(generated_tcs)} TCs for {srs_item.get('ID')}.")
                create_tc_excel(list(final_tcs_to_write.values()), output)
                print(f"📄 Progress saved to {output}")
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response for {srs_item.get('ID')}: {e}")
                print(f"Raw response: {full_response_content[:500]}...")

    except Exception as e:
        print(f"❌ An error occurred during generation: {e}")
        raise typer.Exit(code=1)
    finally:
        rt.stop()


@app.command()
def update(
    excel_file: Annotated[str, typer.Argument(help="The path to the Excel file containing test cases.")],
    tc_id: Annotated[str, typer.Argument(help="The ID of the test case to update.")],
):
    """Updates a specific test case in the Excel file using LLM."""
    print(f"🔍 Attempting to update TC '{tc_id}' in '{excel_file}'...")

    # 1. Load Excel and find the TC
    all_tcs = read_tc_excel(excel_file)
    if not all_tcs:
        print(f"❌ Error: No test cases found in {excel_file} or file not found.")
        raise typer.Exit(code=1)

    original_tc = None
    original_tc_index = -1
    for i, tc in enumerate(all_tcs):
        if tc.get("id") == tc_id:
            original_tc = tc
            original_tc_index = i
            break

    if not original_tc:
        print(f"❌ Error: Test case with ID '{tc_id}' not found in {excel_file}.")
        raise typer.Exit(code=1)

    print("\n--- Original Test Case ---")
    print(json.dumps(original_tc, indent=2, ensure_ascii=False))

    # 2. Prompt LLM for Update
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set.")
        raise typer.Exit(code=1)

    rt = Runtime()
    try:
        system_message = UPDATE_SYSTEM_MESSAGE
        
        current_tc_for_llm = original_tc # This will be the TC that the LLM sees and modifies                
        while True: # Loop until user confirms or cancels
            update_instruction = typer.prompt("어떻게 테스트 케이스를 수정하고 싶으신가요? (예: '음성 시나리오 추가', '사전 조건 명확화', 'no' 입력 시 종료)")
            
            if update_instruction.lower() == "no":
                print("❌ Update cancelled by user. No changes applied.")
                break

            llm_query_prompt = f"""
            다음 테스트 케이스를 사용자 지시에 따라 수정해주세요.
            --- 현재 테스트 케이스 ---
            {json.dumps(current_tc_for_llm, indent=2, ensure_ascii=False)}

            --- 사용자 지시 ---
            {update_instruction}

            수정된 테스트 케이스를 위에서 제시된 JSON 형식으로만 응답해주세요.
            """

            print(f"🤖 Requesting LLM ({_current_llm_model_id}) to update test case...")
            full_response_content = _call_llm_with_fallback(
                rt=rt,
                api_key=api_key,
                prompt=llm_query_prompt,
                system_message=system_message
            )
            
            # LLM 응답에서 JSON 부분만 추출 (마크다운 블록 처리)
            match = re.search(r"```(json)?\s*([\s\S]*?)\s*```", full_response_content)
            if match:
                json_str = match.group(2)
            else:
                json_str = full_response_content.strip()
            
            try:
                updated_tc = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response from LLM: {e}")
                print(f"Raw LLM response: {full_response_content[:500]}...")
                print("⚠️ Please try again with a different instruction or type 'no' to exit.")
                continue # Continue the loop to ask for new instruction
            
            # 3. Display Proposed Changes (simple diff for now)
            print("\n--- Proposed Updated Test Case ---")
            print(json.dumps(updated_tc, indent=2, ensure_ascii=False))
            
            # 4. User Confirmation
            confirmation = typer.prompt("이 변경 사항을 적용하시겠습니까? ('yes' 입력 시 적용, 다른 지시 입력 시 LLM 재요청, 'no' 입력 시 종료)")
            
            if confirmation.lower() == "yes":
                all_tcs[original_tc_index] = updated_tc
                create_tc_excel(all_tcs, excel_file)
                print(f"✅ Test case '{tc_id}' successfully updated in {excel_file}.")
                break # Exit loop after successful update
            elif confirmation.lower() == "no":
                print("❌ Update cancelled by user. No changes applied.")
                break # Exit loop if user cancels
            else:
                # If not 'yes' and not 'no', treat it as a new instruction for the LLM
                # The next iteration of the loop will use this as the new update_instruction
                # And the LLM will modify the 'updated_tc' from this iteration.
                # So, we need to make 'updated_tc' the 'current_tc_for_llm' for the next iteration.
                current_tc_for_llm = updated_tc
                # update_instruction = confirmation # This line is not needed as the loop will re-prompt for instruction
                print("\n🔄 Re-prompting LLM with your new instruction...")
    except Exception as e:
        print(f"❌ An error occurred during update: {e}")
        raise typer.Exit(code=1)
    finally:
        rt.stop()

    print("✨ Test case update process completed.")

if __name__ == "__main__":
    app()
