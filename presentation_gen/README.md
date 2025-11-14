# Obsidian Advanced Slides 기반 발표자료 자동 생성기 (presentation-gen)

`presentation-gen`은 LLM을 활용하여 Obsidian Advanced Slides 형식의 마크다운 발표 자료를 자동으로 생성하는 CLI 도구입니다.

이 도구는 두 단계의 워크플로우를 통해 작동합니다:
1.  **스타일 가이드 생성**: 기존 발표 자료 샘플들을 분석하여 일관된 스타일 가이드를 생성합니다.
2.  **발표자료 생성**: 생성된 스타일 가이드와 사용자가 작성한 발표 내용 초안을 바탕으로 최종 마크다운 파일을 생성합니다.

## 1. 설치

`tc-gen`과 동일한 Python 가상 환경 및 Gemini API 키 설정을 공유합니다. 별도의 설치 과정은 필요하지 않습니다.

## 2. 사용법

### 2.1. 스타일 가이드 생성 (`create-style-guide`)

기존에 작성된 발표자료 마크다운 파일들로부터 공통 스타일을 추출하여, `presentation_gen/output/style_guide.md` 파일을 생성합니다.

```bash
python -m presentation_gen.main create-style-guide
```

*   `--samples-dir <샘플_디렉토리>`: (선택 사항) 분석할 샘플 마크다운 파일들이 위치한 디렉토리입니다. (기본값: `presentation_gen/samples`)
*   이 명령어로 생성된 `presentation_gen/output/style_guide.md` 파일을 필요에 맞게 수정하여 `generate` 단계에서 사용할 수 있습니다.

### 2.2. 발표자료 생성 (`generate`)

`presentation_gen/output/style_guide.md` 파일과 발표 내용 초안을 바탕으로 최종 발표자료 마크다운 파일을 생성합니다.

```bash
python -m presentation_gen.main generate <초안_파일.md> --output <결과물.md>
```

*   `<초안_파일.md>`: 발표할 내용의 초안이 담긴 마크다운 파일의 경로입니다.
*   `--output <결과물.md>`: (선택 사항) 생성될 최종 발표자료 파일의 이름입니다. (기본값: `presentation.md`)
*   생성된 파일은 `presentation_gen/output/` 디렉토리에 저장됩니다.
