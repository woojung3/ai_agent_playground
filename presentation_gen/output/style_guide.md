# Presentation Style Guide (Obsidian Advanced Slides)

이 스타일 가이드는 Obsidian Advanced Slides를 사용하여 일관된 스타일의 발표 자료를 만들기 위한 규칙과 권장 사항을 정의합니다.

## 1. YAML Frontmatter

모든 발표 자료의 시작 부분에는 다음 YAML 프론트매터를 사용하여 기본적인 설정을 정의합니다.

```yaml
---
theme: white
defaultTemplate: "[[tpl-base-no-title]]"
transition: fade
slideNumber: c/t
---
```

- **theme**: 슬라이드의 전체적인 테마를 지정합니다. `white`만을 기본값으로 사용합니다.
- **defaultTemplate**: 별도 템플릿이 지정되지 않은 슬라이드에 기본으로 적용될 템플릿입니다. `"[[tpl-base-no-title]]"`을 기본값으로 사용합니다.
- **transition**: 슬라이드 전환 효과를 지정합니다. `fade`를 사용합니다.
- **slideNumber**: 슬라이드 번호 표시 형식을 지정합니다. `c/t` (현재 슬라이드 / 전체 슬라이드)를 사용합니다.

## 2. Global Styles (`<style>` block)

YAML 프론트매터 바로 다음에 `<style>` 블록을 추가하여 전체 슬라이드에 적용될 CSS를 정의합니다.

```html
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro&display=swap');

.code-block-fixed {  
  display: block;  padding: 5px;  overflow: auto; min-height:100px; max-height: 100%;  word-wrap: normal;
}
.reveal .hljs:not(:first-child).fragment { box-sizing: content-box; }
.reveal, .reveal h1, .reveal h2, .reveal h3, .reveal h4, .reveal h5, .reveal h6 {
  font-family: 'Noto Sans KR', sans-serif;
  text-transform: none;
  margin-bottom: 1px;
}
.reveal p {
  margin: 10px;
}
li:last-of-type {
  margin-bottom: 10px;
}
</style>
```

- **글꼴**: 본문은 `Noto Sans KR`, 코드는 `Source Code Pro`를 사용합니다.
- **전역 스타일**: `.reveal` 선택자를 사용하여 제목(`h1`-`h6`), 문단(`p`), 리스트(`li`) 등의 기본 여백과 스타일을 일관되게 유지합니다.

## 3. Slide Structure

### 3.1. Slide Separation

각 슬라이드는 `---`를 사용하여 구분합니다.

### 3.2. Slide Templates

- **제목 슬라이드**: 발표의 첫 슬라이드는 제목 템플릿을 사용합니다.
  ```markdown
  <!-- .slide: template="[[tpl-title]]" -->
  ::: title
  제목
  :::
  
  ::: author
  발표자
  :::
  
  ::: date
  📆 YYYY-MM-DD
  :::
  ```
- **기본 슬라이드**: `defaultTemplate`에 의해 별도 지정이 없으면 기본 템플릿(`[[tpl-base-no-title]]`)이 적용됩니다.

### 3.3. Slide Modifiers

특정 슬라이드의 배경이나 속성을 변경할 수 있습니다.

- **배경 변경**: `<!-- .slide: bg="URL_or_Color" data-background-opacity="0.5" -->`
- **2단 레이아웃**: `<!-- slide template="[[tpl-2col-1_1]]" -->` 와 `::: left`, `::: right`를 사용합니다.

## 4. Content Formatting

### 4.1. Text and Lists

- **제목**: `#`, `##`, `###` 등을 사용하여 제목 계층을 표현합니다.
- **목록**: 하이픈(`-`)을 사용하여 순서 없는 목록을 작성합니다.
- **인용**: `> [!quote]` 형식을 사용하여 인용구를 강조합니다.
- **각주**: `::: footnote` 블록을 사용하여 슬라이드 하단에 각주를 추가합니다.

### 4.2. Code Blocks

- 코드 블록은 백틱 3개(```)로 감싸고, 코드의 언어를 명시하여 구문 강조를 적용합니다. (예: ` ```java`)

### 4.3. Images

- 이미지는 `![[image.png|width]]` 형식으로 삽입하며, `|` 뒤에 숫자를 넣어 너비를 조절할 수 있습니다.

### 4.4. Tables

- 표준 마크다운 테이블 문법을 사용하여 표를 작성합니다.

  ```markdown
  | Header 1 | Header 2 |
  | -------- | -------- |
  | Cell 1   | Cell 2   |
  ```

### 4.5. Mermaid Diagrams

- ` ```mermaid` 코드 블록을 사용하여 간트 차트, 순서도 등의 다이어그램을 그릴 수 있습니다.

  ```markdown
  ` ``mermaid
  gantt
  dateFormat   YYYY-MM-DD
  title        A Gantt Diagram
  ...
  ` ``
  ```

## 5. Style
- 글머리 기호 목록(itemize/enumerate)을 만들 때, 각 항목의 끝에 마침표(.)를 찍지 않습니다.
- 문서는 명사형으로 종결하는 것을 기본으로 합합니다. (예: ~함, ~있음, ~필요)
- 항목화된 목록에는 별표(*) 대신 하이픈(-)을 사용합니다.
