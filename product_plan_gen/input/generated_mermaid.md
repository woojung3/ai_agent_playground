## Event Storming Whiteboard - Mermaid Flowchart

```mermaid
flowchart LR
    %% --- 유형 정의 ---
    classDef actor      fill:#ffff00,stroke:#333,stroke-width:2px
    classDef command     fill:#add8e6,stroke:#333,stroke-width:2px
    classDef system      fill:#ffb6c1,stroke:#333,stroke-width:2px
    classDef hotspot     fill:#ff69b4,stroke:#333,stroke-width:6px
    classDef opportunity fill:#90ee90,stroke:#333,stroke-width:6px
    classDef policy      fill:#e6e6fa,stroke:#333,stroke-width:2px
    classDef readmodel   fill:#8fbc8f,stroke:#333,stroke-width:2px

    %% --- 요소 정의 ---

    %% Actors (A)
    A1(정책 관리자):::actor
    A2(QA):::actor
    A3(엔지니어):::actor
    A4(시스템 관리자):::actor
    A5(ADMIN User):::actor
    A6(인증서 발급 요청자):::actor
    A7(인증서 관리자):::actor
    A8(계정 관리자):::actor
    A9(DIRECTOR Admin):::actor
    A10(외부 연계 시스템):::actor
    A11(시스템 원격지):::actor
    A12(개발/운영):::actor
    A13(비연계 장비):::actor

    %% Systems (S)
    S1(HSM):::system
    S2(External PKI):::system
    S3(KeyLink):::system
    S4(DB):::system

    %% Hotspots (H)
    H1(이건 어떻게 해야 하는 건지 아직 잘 모르겠음):::hotspot
    H2(고객이 어떤 인증서 발급 정책을 원하는지 좀 더 명확하게 알고 싶음):::hotspot
    H3(Observability 구축 필요!!):::hotspot
    H4(DR 리허설 테스트 필요!!):::hotspot
    H5(MariaDB 이중화 시 데이터 동기화 테스트 필요):::hotspot
    H6(HSM 이중화 시 데이터 동기화 테스트 필요):::hotspot
    H7(자동으로 발급하다가 실패했을 경우에는?):::hotspot
    H8(그냥 TLS Server/Client 직접 발급할 수 있게 하면 안되나요...?):::hotspot
    H9(이거 시스템 내부적으로 TLS용 인증서를 별도의 테이블로 관리하고 있어서, 수동 발급한 애는 여기서 말하는 TLS Server Issuing CA로 등록이 안 되어요. 기능 추가가 필요합니다.):::hotspot
    H10(인증서 발급 프로파일에 없는 확장 필드를 추가할 수 있나요?):::hotspot
    H11(인증서 폐기 시 처리 로직상 TimeZone/Date/Time 고려가 되나요?):::hotspot
    H12(OCSP 응답 속도/가용성에 대한 요구사항은?):::hotspot
    H13(모든 CA CRL 다운로드 시 성능 문제는?):::hotspot
    H14(특정 노드가 죽었을 경우 유효성 확인은?):::hotspot
    H15(서버 부팅에 무슨 순서가 중요한가요?):::hotspot
    H16(인증서 발급 정책은 어디에 저장되어야 하나요?):::hotspot
    H17(서버 장애 시 DB부터 복구하는 게 맞는 건가요?):::hotspot
    H18(복구 후 기능 테스트는 누가 해야 하나요?):::hotspot
    H19(폐기 방식은 뭐로 할까요?):::hotspot
    H20(비밀키를 복구할 수 있는 기능이 있어야 하는 건가요?):::hotspot
    H21(HSM 사용자/관리자 비밀키가 누가 관리해야 하나요?):::hotspot
    H22(어떤 스트림을 타는 걸까요?):::hotspot
    H23(어떤 프로토콜로 외부시스템(API)에 이 정보를 전달할지 결정 필요):::hotspot


    %% Opportunities (O)
    O1(기능 통합 테스트 모듈이 있으면 좋을 것 같음):::opportunity
    O2(TLS용 인증서 수동 발급 자체가 안되진 않는 것 같던데):::opportunity
    O3(인증서 발급 프로파일에 없는 필드를 추가할 수 있어야 함):::opportunity
    O4(발급 요청 이후에도 수정 가능하도록 기능 추가 필요함):::opportunity
    O5(CRL 배포는 정해진 규칙/시간/정책에 따라 자동화되어야 함):::opportunity
    O6(수정보다는 삭제 후 추가가 좋을 듯 - Oid Field):::opportunity
    O7(수정보다는 삭제 후 추가가 좋을 듯 - Oid Value):::opportunity
    O8(URL로 등록해 API 구현하도록 구성하는 게 좋을 것 같음):::opportunity
    O9(모든 CA CRL 다운로드를 지원해야 함):::opportunity
    O10(별도의 테이블로 관리하지 않고 DB에 넣어 관리하면 안 되나요?):::opportunity
    O11(DB 백업/복구 요청됨):::opportunity

    %% Policies (P)
    P1(라이선스 구현 방식 확인 필요):::policy
    P2(운영 로그 정책 필요):::policy
    P3(EKU 발급 필드 정의 등 정책):::policy

    %% Read Models / State / Actions (R) - Using readmodel class for yellow boxes
    R1[CP/CPS가 작성됨]:::readmodel
    R2[주요 인증서 발급 정책 정의]:::readmodel
    R3[MVP 기능 테스트에 통과함]:::readmodel
    R4[성능 요구사항을 만족하고 부하 테스트에 통과함]:::readmodel
    R5[라이선스가 등록됨]:::readmodel
    R6[제품이 센터에 최초 설치됨]:::readmodel
    R7[DB 이중화 설정이 완료됨]:::readmodel
    R8[HSM 이중화 설정이 완료됨]:::readmodel
    R9[Sub CA 인증서를 발급할 상위 인증서 체인이 구성됨]:::readmodel
    R10[ROOT 인증서 발급됨]:::readmodel
    R11[CA 인증서용 키를 저장함]:::readmodel
    R12[서버 인증서 발급됨]:::readmodel
    R13[기존 CA Chain Import됨]:::readmodel
    R14[ROOT 인증서 발급 요청됨]:::readmodel
    R15[Sub CA 인증서 발급됨]:::readmodel
    R16[CA/RA 프로파일이 생성됨]:::readmodel
    R17[인증서 발급 요청됨]:::readmodel
    R18[인증서 발급 처리 요청이 들어옴]:::readmodel
    R19[인증서 발급 완료됨]:::readmodel
    R20[CRL 파일이 생성됨]:::readmodel
    R21[CRL 배포됨]:::readmodel
    R22[폐기할 인증서 정보가 조회됨]:::readmodel
    R23[폐기된 인증서 정보가 저장됨]:::readmodel
    R24[Custom Oid Field가 생성됨]:::readmodel
    R25[Custom Oid Value가 생성됨]:::readmodel
    R26[Custom Oid Field 수정 요청이 들어옴]:::readmodel
    R27[인증서 프로파일 등록/수정됨]:::readmodel
    R28[CA 인증서 발급 요청됨]:::readmodel
    R29[CA 인증서 폐기 요청됨]:::readmodel
    R30[사용자 인증서 발급 요청이 들어옴]:::readmodel
    R31[OCSP 응답됨]:::readmodel
    R32[서버 부팅 완료됨]:::readmodel
    R33[인증서 정책이 로딩됨]:::readmodel
    R34[VA에 정책이 로딩됨]:::readmodel
    R35[VA 발급 요청됨]:::readmodel
    R36[인증서 발급 정책이 확인됨]:::readmodel
    R37[인증서 정보가 조회됨]:::readmodel
    R38[서비스 재시작 요청됨]:::readmodel
    R39[시스템 정보가 조회됨]:::readmodel
    R40[CA 인증서가 발급됨]:::readmodel
    R41[CRL 업데이트 식별 변경 요청이 들어옴]:::readmodel
    R42[OCSP 인증서 생성 요청됨]:::readmodel


    %% --- 프로세스 흐름 ---

    subgraph 1. 설치 및 QA/정책 수립
        A1 --> R1
        A1 --> H1
        A1 --> R2
        R2 --> H2
        R1 & R2 --> A2
        A2 --> R3
        R3 --> O1
        A2 --> R4
        R4 --> H3
        R3 & R4 --> A3
        A3 --> P1
        A3 --> R5
        R5 --> R6
        A3 --> R7
        A3 --> R8
        R7 & R8 --> H4
        R7 --> H5
        R8 --> H6
        H3 & H4 & H5 & H6 --> P2
    end

    subgraph 2. 최초 CA/인증서 구성
        direction TB
        S2 --> R13
        R13 --> R11
        R13 --> R14
        R14 --> S1
        R11 & R14 --> R10
        R10 --> R12

        A5 --> R14
        A5 --> R9
        R9 --> R15
        R15 --> H7
        R12 --> H8
        H8 --> O2
        H8 --> H9
        H9 --> O10(DB 관리 방안)
    end

    subgraph 3. CA/인증서 라이프사이클 관리
        A5 --> R16
        A5 --> R17
        R17 --> R18
        R18 --> R19
        R19 --> H10
        H10 --> O3
        R17 --> O4
        R19 --> R20
        R20 --> R21
        R21 --> O5
        R19 --> R22
        R22 --> R23

        A4(시스템 관리자) --> R24
        R24 --> R26
        R26 --> O6

        A5 --> R25
        R25 --> O7
        P3 --> R24 & R25
        
        R19 --> A6
        A6 --> R40
        R40 --> A7
        A7 --> H19
        A7 --> H20
        A7 --> R22
        R22 --> R42

        A8(계정 관리자) --> R41
        R41 --> H22

        R40 --> H23

        R21 --> A9
    end

    subgraph 4. 외부 시스템 연계 및 OCSP
        A10 --> R27
        A10 --> R28
        R28 --> S3
        S3 --> R29
        A10 --> R30
        A10 --> R31
        R31 --> H12
        R28 --> O8
        R29 --> H13
        H13 --> O9

        A11(시스템 원격지) --> R32
        R32 --> R33
        R33 --> R34
        R34 --> R35
        R33 --> H16
        
        A12(개발/운영) --> R38
        A12 --> R39

        R33 & R34 --> R36
        R36 --> R37
        R37 --> H25(인증 확인)
        R37 --> A13
        
        S4(DB) --> H14
        S1(HSM) --> H21
        H15 --> R32

        A12 --> O11
        O11 --> H17
        H17 --> H18

    end

    %% --- 주요 시스템 연동 ---
    R10 & R15 & R19 --> S1
    S1 --> R8
    S4 --> R7
```
