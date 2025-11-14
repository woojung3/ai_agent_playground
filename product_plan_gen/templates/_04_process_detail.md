## 💡 **프로세스 표현 가이드**

- 프로세스를 가장 잘 설명할 수 있는 방식을 사용하여 작성합니다. (Flowchart, BPMN, Sequence Diagram, Use Case, User Journey 등)
- BPMN의 경우 UML만 허용되며, 나머지는 Mermaid로 작성해야 합니다.
- 다이어그램만으로 설명이 부족할 경우, 각 단계의 세부 내용이나 비즈니스 규칙을 보충 설명합니다.

---

### **프로세스 개요**

| 항목 | 설명 |
| :--- | :--- |
| **목적** | {{PROCESS_PURPOSE}} |
| **시작 조건** | {{PROCESS_PRECONDITION}} |
| **종료 조건** | {{PROCESS_POSTCONDITION}} |

---

### **프로세스 표현 ({{DIAGRAM_TYPE}})**

```mermaid
{{PROCESS_DIAGRAM}}
```

---

### **상세 절차**

| 단계 | 수행자 | 행동 (Action) | 상세 설명 |
| :--- | :--- | :--- | :--- |
| {{STEP_NUMBER}} | {{STEP_ACTOR}} | {{STEP_ACTION}} | {{STEP_DESCRIPTION}} |
