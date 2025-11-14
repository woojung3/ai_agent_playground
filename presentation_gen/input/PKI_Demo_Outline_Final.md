아래 내용을 그대로 발표자료화하지 말고, 비개발자가 보기에도 친절할 정도로 부연설명을 잘 달아줘.

$$$$ 타이틀
# X.509 PKI 솔루션 데모 발표 자료

**발표 목표:** 우리 PKI 솔루션이 **`keylink`가 필요로 하는 핵심 기능들을 mTLS와 인증서 기반 권한 모델 위에서 어떻게 안전하게 지원**하는지 명확하게 보여주는 것

$$$$ 인트로
## 1. 인트로: TDM과 keylink를 위한 신뢰의 기반 (5분)
*   TDM 프로젝트의 당면 과제와 `keylink`의 역할
*   **PKI의 목표:** `keylink`가 키 관리, 서명/검증 등을 수행하는 데 필요한 **신뢰의 원점(Root of Trust)과 핵심 서비스를 '안전하고 통제된 방식'으로 제공**하는 것
*   **솔루션 한 줄 요약:** "`keylink`를 위한 제로 트러스트 기반의 인증서 발급 및 관리 전문 서비스"

$$$$ 아키텍처
## 2. 솔루션 아키텍처: PKI와 keylink의 협력 모델 (5분)
*   **전체 연동 아키텍처:** [ `keylink` (RA) ] <- **mTLS** -> [ **PKI 솔루션 (CA/VA)** ] <-> [ HSM ]
    *   모든 API 통신이 mTLS로 암호화되고 상호 인증됨을 강조
*   **인증서 기반 인가(Authorization) 모델:**
    *   `keylink`의 모든 API 접근 권한이 **`keylink`에게 발급된 클라이언트 인증서 자체에 의해 결정**됨을 설명
    *   "Payload가 아닌 신원(Identity)에 기반한 권한 제어"

$$$$ 유저 시나리오 - 이 부분은 시나리오만 써줘. 스크린샷 등 내용은 사람이 직접 채워넣을거야.
## 3. 핵심 연동 시나리오 중심의 라이브 데모 (15분)

*   **시나리오 0: `keylink` 시스템의 안전한 등록 (Provisioning)**
    *   **상황:** 새로운 `keylink` 시스템을 PKI에 등록하고 통신을 시작해야 할 때
    *   **프로세스:**
        1.  CA 관리자가 PKI UI에서 `keylink`를 위한 클라이언트 인증서 생성
        2.  이때, **`keylink`의 역할에 맞는 최소한의 권한만 인증서에 할당** (예: `ISSUE_CERT`, `RENEW_SELF`)
        3.  암호화된 PFX(.p12) 파일로 내보내 **안전한 채널(Out-of-Band)로 `keylink` 관리자에게 전달**
    *   **데모:** PKI 관리자 화면에서 RA용 인증서를 생성하고, '권한'을 선택하여 부여하는 모습 시연

*   **시나리오 1: `keylink`의 mTLS 기반 인증서 발급 요청**
    *   **상황:** `keylink`가 디바이스의 CSR을 받아 CA에 인증서 발급을 요청할 때
    *   **프로세스:**
        1.  `keylink`는 **자신의 클라이언트 인증서(PFX)를 사용**하여 PKI API 서버와 mTLS 세션 수립
        2.  PKI는 `keylink`가 제시한 인증서를 검증하고, **`ISSUE_CERT` 권한이 있는지 확인**
        3.  권한이 충분하면 CSR을 처리하여 인증서 발급 후 반환. 부족하면 `403 Forbidden` 반환
    *   **데모:** `curl`의 mTLS 옵션을 사용하여 API를 성공적으로 호출하는 모습과, 권한이 없는 API 호출 시 `403` 오류가 발생하는 모습 비교 시연

*   **시나리오 2: `keylink`의 펌웨어 서명 검증 지원**
    *   **상황:** `keylink`가 펌웨어 서명 검증을 위해 서명 인증서의 폐지 상태를 확인할 때
    *   **프로세스:** PKI는 `keylink`가 조회할 수 있도록 CRL 배포 엔드포인트(CDP)와 실시간 OCSP 엔드포인트를 제공
    *   **데모:** `openssl` 명령어로 OCSP 엔드포인트에 상태 조회를 요청하고, `good` 응답을 확인하는 과정 시연

$$$$ X.509 PKI 제품과, 이 제품을 이용하는 타 솔루션의 통합 가이드
## 4. TDM & keylink 통합 가이드 (5분)

*   **`keylink` 개발 항목과 PKI 서비스 매핑 표:** (이전과 동일)
*   **PKI 솔루션 간이 연동 가이드 (mTLS 기반 최종안):**

    ---
    ### **PKI 솔루션 간이 연동 가이드 (mTLS Quick Start)**
    [info]
    모든 API 요청은 Bearer Token이 아닌, **mTLS 클라이언트 인증서**를 통해 인증 및 인가됩니다.

    **사전 준비:**
    *   PKI 서버 Base URL: `https://pki.example.com`
    *   PKI 관리자로부터 전달받은 클라이언트 인증서 파일: `keylink_identity.p12`
    *   인증서 파일 암호: `p12_password`

    **Step 1. 연동 테스트 (mTLS Health Check)**
    *   전달받은 인증서로 mTLS 통신이 정상적으로 수립되는지 확인합니다.
    ```bash
    curl --cert-type P12 --cert keylink_identity.p12:p12_password \
         https://pki.example.com/health
    ```
    *   **예상 응답:** `{"status": "UP"}`

    **Step 2. 인증서 발급 요청 (mTLS 기반)**
    *   `--cert` 옵션을 포함하여 API를 호출하면, PKI가 인증서를 분석해 권한을 확인합니다.
    ```bash
    curl -X POST \
         --cert-type P12 --cert keylink_identity.p12:p12_password \
         -H "Content-Type: application/json" \
         -d '{
               "csr": "-----BEGIN CERTIFICATE REQUEST-----\n...",
               "profile": "TDM_DEVICE_LEVEL_1"
             }' \
         https://pki.example.com/api/v1/certificates
    ```
    *   **예상 응답:** `keylink_identity.p12`에 `ISSUE_CERT` 권한이 있는 경우, 발급된 인증서(PEM) 반환. 그렇지 않으면 `403 Forbidden`.

    **Step 3. 내 인증서 갱신 (RENEW_SELF)**
    *   만료가 임박한 `keylink` 자신의 인증서를 스스로 갱신합니다.
    ```bash
    curl -X POST \
         --cert-type P12 --cert keylink_identity.p12:p12_password \
         https://pki.example.com/api/v1/certificates/renew-self
    ```
    *   **예상 응답:** `keylink_identity.p12`에 `RENEW_SELF` 권한이 있는 경우, 갱신 발급된 인증서(PEM) 반환.

    ---

$$$$ 결론 및 Q&A
## 5. 결론 및 협력 방안 (3분)
*   **핵심 가치:** 단순 기능 제공을 넘어, **제로 트러스트 원칙에 입각한 안전한 연동 모델**을 통해 `keylink`와 TDM 생태계 전체의 보안 수준을 격상
*   **향후 협력:** `keylink` 연동을 위한 mTLS 인증서 발급 및 기술 지원 계획 공유

## 6. Q&A (7분)
