## 💡 **프로세스 작성 가이드**

- **어떤 단계인가?** 사용자가 특정 목표를 달성하기 위해 거치는 핵심적인 여정과 시스템의 동작을 시각적으로 표현합니다. '핵심 이벤트 흐름'을 이곳에 담습니다.
- **어떻게 작성해야 하는가?** 프로세스의 복잡성과 목적에 따라 플로우차트, 시퀀스 다이어그램, BPMN, 유저 저니, 유즈케이스 등 다양한 다이어그램을 사용할 수 있습니다.

---

### **주요 프로세스**

> ⓘ 이 페이지는 우리 서비스의 모든 핵심 비즈니스 프로세스를 한눈에 볼 수 있는 목차 페이지입니다. 각 프로세스의 상세 내용은 개별 하위 페이지에서 확인하세요.

| 프로세스명 | 핵심 설명 | 상태 | 링크 |
| :--- | :--- | :--- | :--- |
| 인증서 발급 라이프사이클 관리 | Root CA, Sub CA, 사용자 인증서 발급 및 요청 수정 등 인증서의 생성 및 초기 관리 과정을 포함합니다. | 계획 중 | [상세 보기](./process_issuance.md) |
| 인증서 폐기 및 CRL 관리 | 발급된 인증서의 폐기 처리 로직, 폐기 목록(CRL) 생성 및 자동 배포 프로세스를 정의합니다. | 계획 중 | [상세 보기](./process_revocation_crl.md) |
| PKI 정책 및 프로파일 관리 | 인증서 발급 정책, CA/RA 프로파일, Custom OID 필드/값 정의 및 관리 기능을 다룹니다. | 계획 중 | [상세 보기](./process_policy_profile.md) |
| 보안 키 관리 및 HSM 연동 | HSM(Hardware Security Module)을 통한 키 생성, 안전한 저장, HSM 이중화 및 비밀키 관리 정책을 수립합니다. | 계획 중 | [상세 보기](./process_key_hsm.md) |
| 시스템 고가용성 및 DR 관리 | MariaDB 및 HSM 이중화 설정, DR(재해 복구) 리허설 테스트, 시스템 복구 절차 등을 포함합니다. | 계획 중 | [상세 보기](./process_ha_dr.md) |
| 외부 시스템 연동 (OCSP/CRL/KeyLink) | External PKI (OCSP, CRL), KeyLink와의 연동 및 API 구현 방식을 상세화합니다. | 계획 중 | [상세 보기](./process_external_integration.md) |
| 시스템 모니터링 및 감사 로그 | 시스템 건강 상태 모니터링, Observability 구축, 운영 로그 및 감사 로그 관리, 노드 장애 시 유효성 확인을 다룹니다. | 계획 중 | [상세 보기](./process_monitoring_audit.md) |
| QA 및 통합 테스트 | MVP 기능 테스트, 성능 부하 테스트, 기능 통합 테스트 모듈 구현 및 검증 프로세스를 포함합니다. | 계획 중 | [상세 보기](./process_qa_testing.md) |

---
## Summary for Automation

```json
{
  "processes": [
    {
      "process_name": "인증서 발급 라이프사이클 관리"
    },
    {
      "process_name": "인증서 폐기 및 CRL 관리"
    },
    {
      "process_name": "PKI 정책 및 프로파일 관리"
    },
    {
      "process_name": "보안 키 관리 및 HSM 연동"
    },
    {
      "process_name": "시스템 고가용성 및 DR 관리"
    },
    {
      "process_name": "외부 시스템 연동 (OCSP/CRL/KeyLink)"
    },
    {
      "process_name": "시스템 모니터링 및 감사 로그"
    },
    {
      "process_name": "QA 및 통합 테스트"
    }
  ]
}
```
