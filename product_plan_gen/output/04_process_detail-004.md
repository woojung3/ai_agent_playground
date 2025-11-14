## 💡 **프로세스 표현 가이드**

- 프로세스를 가장 잘 설명할 수 있는 방식을 사용하여 작성합니다. (Flowchart, BPMN, Sequence Diagram, Use Case 등)
- 다이어그램만으로 설명이 부족할 경우, 각 단계의 세부 내용이나 비즈니스 규칙을 보충 설명합니다.

---

### **프로세스 개요**

| 항목 | 설명 |
| :--- | :--- |
| **목적** | HSM (Hardware Security Module) 연동을 통해 Root CA, Sub CA, 사용자 인증서 등 모든 암호화 키를 안전하게 생성하고 저장하며, HSM의 고가용성을 확보하고 키 관리 정책을 수립하여 최고 수준의 보안을 유지합니다. |
| **시작 조건** | - PKI 시스템이 KeyLink 및 HSM과 연동 가능한 상태여야 합니다.<br/>- HSM 장비가 설치 및 네트워크에 연결되어 있어야 합니다.<br/>- PKCS#11 인터페이스를 위한 드라이버 및 라이브러리가 시스템에 설치되어 있어야 합니다.<br/>- 인증서 발급을 위한 상위 인증서 체인(예: 기존 CA Chain)이 존재하거나 Root CA 발급 요청이 준비되어 있어야 합니다. |
| **종료 조건** | - 모든 중요한 암호화 키가 HSM 내에 안전하게 저장됩니다.<br/>- HSM 이중화 설정이 완료되고 데이터 동기화가 검증됩니다.<br/>- HSM 사용자/관리자 비밀키 관리 및 비밀키 복구에 대한 정책이 수립됩니다.<br/>- 시스템은 HSM을 통해 안전하게 암호화 작업을 수행할 수 있습니다. |

---

### **프로세스 표현 (Flowchart)**

```mermaid
graph TD
    subgraph "키 생성 및 저장"
        A4[시스템 관리자] -- Root CA 발급 요청 --> R14_REQ(ROOT 인증서 발급 요청됨)
        R14_REQ --> S1(HSM)
        S1 -- PKCS#11 인터페이스 활용 --> R11_STORE(CA 인증서용 키를 저장함)
        R11_STORE --> R10(ROOT 인증서 발급됨)
        A5_ADMIN[ADMIN User] -- Sub CA 발급 요청 --> R9_SUB_REQ(Sub CA 인증서 발급 상위 체인 구성됨)
        R9_SUB_REQ --> S1
        S1 --> R15(Sub CA 인증서 발급됨)
        A6_USER[인증서 발급 요청자] -- 사용자/서버 인증서 발급 요청 --> R17_REQ(인증서 발급 요청됨)
        R17_REQ --> S1
        S1 --> R19(인증서 발급 완료됨)
        R10 & R15 & R19 -- 모든 중요 키를 HSM에 안전하게 저장 --> CRS17_MET[보안 요구사항 충족 (CRS-017)]
    end

    subgraph "HSM 운영 및 관리"
        A3[엔지니어] -- HSM 이중화 설정 --> R8(HSM 이중화 설정이 완료됨)
        R8 -- 데이터 동기화 테스트 필요 --> H6(HSM 이중화 시 데이터 동기화 테스트 필요)
        H6 -- 테스트 완료 --> S1
        A4_SYSADM[시스템 관리자] -- HSM 비밀키 관리 정책 수립 --> P_HSM_KEY_POLICY[HSM 비밀키 관리 정책]
        P_HSM_KEY_POLICY --> H21(HSM 사용자/관리자 비밀키 관리 주체)
        A7[인증서 관리자] -- 비밀키 복구 기능 필요성 검토 --> P_KEY_RECOVERY_CONSIDER[비밀키 복구 정책 검토]
        P_KEY_RECOVERY_CONSIDER --> H20(비밀키 복구 기능 필요 여부)
        P_HSM_KEY_POLICY & P_KEY_RECOVERY_CONSIDER --> CRS11_MET[HSM 키 관리 정책 수립 (CRS-011)]
    end

    style S1 fill:#f9f,stroke:#333,stroke-width:2px
    style R10 fill:#fff,stroke:#333,stroke-width:2px
    style R15 fill:#fff,stroke:#333,stroke-width:2px
    style R19 fill:#fff,stroke:#333,stroke-width:2px
    style H6 fill:#FFB3B3,stroke:#CC0000,stroke-width:2px
    style H20 fill:#FFB3B3,stroke:#CC0000,stroke-width:2px
    style H21 fill:#FFB3B3,stroke:#CC0000,stroke-width:2px
```

---

### **상세 절차**

| 단계 | 수행자 | 행동 (Action) | 상세 설명 |
| :--- | :--- | :--- | :--- |
| 1 | 엔지니어 (A3) | HSM 연동 환경 설정 | HSM 장비 설치 및 네트워크 연결, PKCS#11 드라이버/라이브러리 설치를 포함하여 HSM과의 안전한 통신을 위한 물리적/논리적 연결을 설정합니다. `integration.txt`에 명시된 PKCS#11 인터페이스를 활용합니다. |
| 2 | 시스템 관리자 (A4), ADMIN User (A5) | Root CA/Sub CA 키 페어 생성 및 HSM 저장 | Root CA (R10) 및 Sub CA (R15) 인증서 발급 요청 (R14) 시, 해당 키 페어는 HSM (S1) 내에서 생성되고 안전하게 저장됩니다 (R11). 이는 PKI 시스템의 보안 핵심이며, 모든 중요한 키를 HSM에 저장해야 한다는 요구사항(CRS-017)을 충족합니다. |
| 3 | 인증서 발급 요청자 (A6), ADMIN User (A5) | 사용자/서버 인증서 키 페어 생성 및 HSM 저장 | 사용자 (R30) 및 서버 (R12) 인증서 발급 요청 (R17) 시, 관련된 키 페어도 HSM (S1) 내에서 생성 및 저장될 수 있도록 합니다 (R19). 이를 통해 엔드-엔티티 키의 보안을 강화하고 중앙 집중식 키 관리를 가능하게 합니다. |
| 4 | 엔지니어 (A3), 시스템 관리자 (A4) | HSM 이중화 설정 및 데이터 동기화 테스트 | 시스템 고가용성(HA)을 위해 HSM 이중화(R8)를 설정하고, 재해 복구(DR) 시나리오를 고려하여 데이터 동기화 (H6) 및 페일오버(Failover) 테스트(`integration.txt`)를 수행합니다. 이는 DR 리허설 테스트(CRS-003)의 중요한 부분입니다. |
| 5 | 시스템 관리자 (A4), 인증서 관리자 (A7) | 비밀키 관리 정책 수립 | HSM 사용자/관리자 비밀키를 누가 관리할지 (H21) 명확히 정의하고, 필요한 경우 비밀키 복구 기능 (H20) 제공 여부 및 절차에 대한 정책(CRS-011)을 수립합니다. 이는 `PRD.txt`에 언급된 강력한 키 관리 요구사항을 충족합니다. |
