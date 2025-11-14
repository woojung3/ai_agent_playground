# SRS 기반 테스트 케이스 자동 생성기 (tc-gen)

`tc-gen`은 소프트웨어 요구사항 명세서(SRS) 문서를 분석하여, 테스트 케이스(TC)를 엑셀 형식으로 자동 생성해주는 명령줄 인터페이스(CLI) 도구입니다.

이 도구는 LLM(대규모 언어 모델)을 활용하여 SRS의 내용을 이해하고, 지정된 템플릿에 맞춰 TC를 생성함으로써 QA 엔지니어의 반복적인 작업을 줄이고 생산성을 높이는 것을 목표로 합니다.

## 1. 설치

이 도구를 사용하기 위해 필요한 환경 설정 및 라이브러리 설치 절차입니다.

### 1.1. Python 가상 환경 설정

프로젝트 의존성을 격리하기 위해 Python 가상 환경을 생성하고 활성화하는 것을 권장합니다.

```bash
# 1. 이 프로젝트 폴더로 이동합니다.
cd path/to/tc-gen

# 2. 가상 환경을 생성합니다. (.venv 라는 폴더가 생성됩니다)
python3 -m venv .venv

# 3. 가상 환경을 활성화합니다.
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

가상 환경이 활성화되면, 터미널 프롬프트 앞에 `(.venv)`가 표시됩니다.

### 1.2. Gemini API 키 설정 (중요)

이 도구는 Google의 Gemini AI 모델을 사용하여 테스트 케이스를 생성합니다. 따라서, API를 사용하기 위한 **API 키**가 반드시 필요하며, 보안을 위해 환경 변수로 설정해야 합니다.

**API 키 발급 방법:**

1.  **[Google AI Studio](https://aistudio.google.com/)** 로 이동하여 Google 계정으로 로그인합니다.
2.  왼쪽 메뉴의 **'Get API key'** 탭을 클릭합니다.
3.  **'Create API key in new project'** 버튼을 클릭하여 새 API 키를 생성합니다.
4.  생성된 키 문자열을 복사합니다.

**환경 변수 설정:**

아래 명령어의 `"YOUR_API_KEY"` 부분을 방금 복사한 키로 교체하여 터미널에서 실행하세요. 이 명령어는 현재 터미널 세션에만 유효하므로, 도구를 사용할 때마다 실행하거나 셸 설정 파일(`.bashrc`, `.zshrc` 등)에 추가해두는 것이 편리합니다.

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

### 1.3. 필요 라이브러리 설치

가상 환경이 활성화되고 API 키가 설정되었다면, 다음 명령어로 도구 실행에 필요한 모든 라이브러리를 한 번에 설치합니다.

```bash
pip install -r requirements.txt
```


## 2. 사용법

`tc-gen`은 여러 단계의 명령어를 통해 테스트 케이스를 생성하고 관리합니다. 모든 명령어는 `python -m tc_gen.main <command>` 형식으로 실행됩니다.

### 2.1. 지식 베이스 파싱 (`parse`)

Confluence 등에서 익스포트된 HTML 문서들을 파싱하여 LLM이 참조할 수 있는 지식 베이스(`knowledge_base.jsonl`)를 생성합니다.

```bash
python -m tc_gen.main parse <HTML_문서_디렉토리_경로>
```

*   `<HTML_문서_디렉토리_경로>`: HTML 문서들이 포함된 디렉토리의 경로입니다.
*   생성된 `knowledge_base.jsonl` 파일은 `tc_gen/output/` 디렉토리에 저장됩니다.

### 2.2. SRS 마크다운 파싱 (`parse-srs`)

수기로 작성된 SRS 마크다운 파일을 LLM을 활용하여 구조화된 JSONL 형식(`srs.jsonl`)으로 변환합니다. 이 파일은 각 요구사항을 개별 항목으로 포함합니다.

```bash
python -m tc_gen.main parse-srs <SRS_마크다운_파일_경로>
```

*   `<SRS_마크다운_파일_경로>`: SRS 내용이 담긴 마크다운 파일의 경로입니다.
*   생성된 `srs.jsonl` 파일은 `tc_gen/output/` 디렉토리에 저장됩니다.

### 2.3. 테스트 케이스 생성 (`generate`)

파싱된 SRS (`srs.jsonl`)와 지식 베이스 (`knowledge_base.jsonl`)를 활용하여 각 SRS 요구사항에 대한 테스트 케이스를 생성하고 Excel 파일로 저장합니다.

```bash
python -m tc_gen.main generate tc_gen/output/srs.jsonl tc_gen/output/knowledge_base.jsonl --output <출력_엑셀_파일명.xlsx>
```

*   `tc_gen/output/srs.jsonl`: `parse-srs` 명령어로 생성된 SRS JSONL 파일입니다.
*   `tc_gen/output/knowledge_base.jsonl`: `parse` 명령어로 생성된 지식 베이스 JSONL 파일입니다.
*   `--output <출력_엑셀_파일명.xlsx>`: 생성될 테스트 케이스 Excel 파일의 이름입니다. (기본값: `test_cases.xlsx`)

### 2.4. 테스트 케이스 업데이트 (`update`)

생성된 Excel 파일 내의 특정 테스트 케이스를 LLM을 통해 수정합니다. TC ID를 지정하고, LLM에게 수정 지시를 내려 대화형으로 테스트 케이스를 개선할 수 있습니다.

```bash
python -m tc_gen.main update <엑셀_파일_경로.xlsx> <TC_ID>
```

*   `<엑셀_파일_경로.xlsx>`: 수정할 테스트 케이스가 포함된 Excel 파일의 경로입니다.
*   `<TC_ID>`: 수정할 테스트 케이스의 고유 ID입니다.
*   명령어 실행 후, LLM에게 수정 지시를 내리고 제안된 변경 사항을 확인하여 적용 여부를 결정할 수 있습니다. 'no'를 입력하면 LLM에게 새로운 지시를 내려 추가 수정을 요청할 수 있습니다.
