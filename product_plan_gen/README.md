# Product Plan Generation AI Agent

이 문서는 `product_plan_gen` AI Agent의 사용 방법을 안내합니다. 이 Agent는 이벤트스토밍 결과(Mermaid 플로우차트)와 추가 컨텍스트 문서를 기반으로 다단계 제품 기획 문서를 자동으로 생성합니다.

## 1. PNG 이미지로부터 Mermaid 플로우차트 변환 가이드

Confluence 화이트보드와 같은 시각적 이벤트스토밍 다이어그램을 Mermaid 플로우차트 코드로 변환하는 과정입니다. 이 과정은 Gemini Vision 모델을 활용하여 이미지 내용을 분석하고, 지정된 스타일 가이드에 따라 Mermaid 코드를 생성합니다.

### 1.1. 준비물

*   **이벤트스토밍 이미지 파일**: Confluence 화이트보드에서 내보낸 PNG 또는 JPG 형식의 이벤트스토밍 다이어그램 이미지 파일. (예: `2025-10-21 이벤트스토밍.png`)
*   **Mermaid 스타일 가이드 프롬프트**: `product_plan_gen/prompts/image_to_mermaid_prompt.md` 파일에 정의된 프롬프트 내용.

### 1.2. 변환 단계

1.  **이미지 파일 배치**: 변환하고자 하는 PNG 또는 JPG 이미지 파일을 `product_plan_gen/input/` 디렉토리에 배치합니다.
    *   예시: `product_plan_gen/input/2025-10-21 이벤트스토밍.png`

2.  **Mermaid 변환 요청 (Gemini CLI Agent에게)**:
    *   다음 명령어를 사용하여 저(Gemini CLI Agent)에게 Mermaid 플로우차트 생성을 요청합니다. 이 명령어는 이미지 파일을 읽고, `image_to_mermaid_prompt.md`의 지시사항과 스타일 가이드를 참조하여 Mermaid 코드를 생성합니다.
    *   생성된 Mermaid 코드는 `product_plan_gen/input/generated_mermaid.md` 파일로 저장됩니다.

    ```
    read_file(absolute_path='product_plan_gen/prompts/image_to_mermaid_prompt.md')
    ```
    위 명령어를 실행하여 프롬프트 내용을 저에게 전달해 주십시오. 제가 프롬프트 내용을 확인한 후, 이미지와 함께 Vision Model에 전달하여 Mermaid 코드를 생성하겠습니다.

    **[Agent의 응답 후, 다음 명령어를 실행합니다]**

    ```
    # (Agent가 생성한 Mermaid 코드를 확인하고, 필요시 수정합니다.)
    # (Agent가 Human-in-the-loop 검수를 위해 일시 정지하면, Enter를 눌러 계속 진행합니다.)
    ```

3.  **생성된 Mermaid 코드 검수**:
    *   변환 과정이 완료되면, `product_plan_gen/input/generated_mermaid.md` 파일을 열어 생성된 Mermaid 코드를 검토합니다.
    *   필요한 경우, Mermaid 문법에 따라 수동으로 수정할 수 있습니다.

## 2. AI Agent 프로그램 실행 가이드 (제품 기획서 생성)

Mermaid 플로우차트와 추가 컨텍스트 파일을 기반으로 다단계 제품 기획 문서를 생성하는 과정입니다.

### 2.1. 준비물

*   **주요 Mermaid 플로우차트 파일**: `product_plan_gen/input/generated_mermaid.md` (위 변환 가이드를 통해 생성된 파일) 또는 직접 작성한 Mermaid 파일.
*   **추가 컨텍스트 파일 (선택 사항)**: `product_plan_gen/input/PRD.txt`, `product_plan_gen/input/integration.txt`와 같이 제품 기획에 필요한 추가 정보를 담은 마크다운 또는 텍스트 파일.

### 2.2. 프로그램 실행 단계

1.  **가상 환경 활성화**: 프로젝트 루트 디렉토리에서 가상 환경을 활성화합니다.
    ```bash
    source ./.venv/bin/activate
    ```

2.  **Agent 실행**: 다음 명령어를 사용하여 제품 기획서 생성을 시작합니다.
    *   `generated_mermaid.md`가 주 입력 파일이며, 그 뒤에 필요한 컨텍스트 파일들을 나열합니다.

    ```bash
    ./.venv/bin/python -m product_plan_gen.main generate product_plan_gen/input/generated_mermaid.md product_plan_gen/input/PRD.txt product_plan_gen/input/integration.txt
    ```

3.  **Human-in-the-loop 검수**:
    *   `00_main.md`, `01_crs.md`, `02_ia.md`, `03_process_list.md`, `05_policy_list.md`, `07_screen_list.md`, `08_screen_design.md`와 같은 주요 파일이 생성될 때마다 프로그램이 일시 정지됩니다.
    *   생성된 파일을 검토한 후, 터미널에 `Enter`를 눌러 다음 단계로 진행하거나, `exit`를 입력하여 프로그램을 중단할 수 있습니다.

4.  **결과 확인**:
    *   모든 과정이 완료되면, `product_plan_gen/output/` 디렉토리에서 생성된 다단계 마크다운 제품 기획서 파일들을 확인할 수 있습니다.
    *   `03_process_list.md`와 `05_policy_list.md`에 기반하여 `04_process_detail-NNN.md` 및 `06_policy_detail-NNN.md` 파일들이 자동으로 생성됩니다.

---
**참고:**

*   `GEMINI_API_KEY` 환경 변수가 설정되어 있어야 합니다.
*   모델 과부하 등으로 인해 생성 과정이 실패할 경우, 이미 생성된 파일은 건너뛰고 실패 지점부터 다시 시작할 수 있습니다.
