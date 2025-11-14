## 💡 **세부 정책 정의**

> ⓘ 아래 형식 중, 작성하려는 정책의 성격과 가장 잘 맞는 형식을 선택하여 사용하세요.

---

### **형식 1: 일반 정책**
> `기능 명세, 기술 결정, 일반 규칙, 이벤트 기반 규칙 등 넓은 범위의 정책을 주제별로 자유롭게 기술할 때 사용합니다.`

> 💡 **이벤트 기반 규칙 작성 Tip**
> `트리거(Trigger)가 되는 이벤트와 실행 내용(Action)을 명확히 구분하여 작성하면 이해하기 쉽습니다.`
> - **Trigger**: `{{EVENT_TRIGGER}}`
> - **Action**: `{{EVENT_ACTION}}`

| 대구분 | 중구분 | 상세 | 비고 |
| :--- | :--- | :--- | :--- |
| {{POLICY_SECTION}} | {{POLICY_SUB_SECTION}} | {{POLICY_DETAIL}} | {{POLICY_REMARK}} |

---

### **형식 2: 권한**
> `사용자 역할(Role)별로 시스템의 특정 기능이나 데이터에 대한 접근 권한(CRUD)을 정의할 때 사용합니다.`

| 대구분 | 중구분 | 사용자 | 보기 | 수정 | 삭제 | 쓰기 | 비고 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| {{PERMISSION_SECTION}} | {{PERMISSION_SUB_SECTION}} | {{USER_ROLE}} | {{CRUD_C}} | {{CRUD_R}} | {{CRUD_U}} | {{CRUD_D}} | {{PERMISSION_REMARK}} |

---

### **형식 3: 검증**
> `입력 폼(Form) 등에서 사용자의 입력값이 유효한지, 또는 필수값이 모두 채워졌는지 등을 검증하는 규칙을 상세히 정의할 때 사용합니다.`

#### **필수 입력항목**

| 상황 | 문구 | 처리 시나리오 |
| :--- | :--- | :--- |
| {{VALIDATION_REQUIRED_SITUATION}} | {{VALIDATION_REQUIRED_MESSAGE}} | {{VALIDATION_REQUIRED_ACTION}} |

#### **유효성 체크**

| 상황 | 문구 | 처리 시나리오 |
| :--- | :--- | :--- |
| {{VALIDATION_CHECK_SITUATION}} | {{VALIDATION_CHECK_MESSAGE}} | {{VALIDATION_CHECK_ACTION}} |
