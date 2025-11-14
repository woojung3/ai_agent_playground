## Image to Mermaid Conversion Prompt

You are an expert in Event Storming and Mermaid diagramming. Your task is to analyze a sequence of image parts, each representing a section of an Event Storming whiteboard, and integrate them to convert the complete whiteboard into a Mermaid flowchart diagram. Identify actors, events, systems, hotspots, opportunities, and policies, and their connections.

Generate a Mermaid `flowchart LR` diagram that accurately represents the event storming.

--- Mermaid Style Guidance ---
Adhere to the following Mermaid style, especially the `classDef` and `:::` syntax for different element types, as shown in this example. This is crucial for consistency and readability.

## 기타 - 최초 설치 이전

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
    A_policy(정책 관리자):::actor
    A_qa(QA):::actor
    A_eng(엔지니어):::actor
	E1(CP/CPS 작성됨)
	E2(주요 인증서 발급 정책이 정의됨)
	E3(CA/B 등 기본 프로파일은 제품에 최초부터 포함됨)
	E4(기본기능 검수를 통과함)
	E5(기본성능 검수를 통과함)
	E6(부하테스트를 통과함)
	E7(라이센스가 등록됨)
    E8(제품이 센터에 최초 설치됨)
    E9(DB 이중화 설정이 완료됨)
    E10(HSM 이중화 설정이 완료됨)
    H_policy(운영정책 정의 필요):::hotspot
    H_license(라이센스 구현방식 확인 필요):::hotspot
    H_db(MariaDB 이중화 테스트 필요):::hotspot
    H_hsm(HSM 이중화 테스트 필요):::hotspot
    S_next(최초 설치 시나리오로 이동):::system
    %% --- 프로세스 흐름 ---
    A_policy --> E1 --> H_policy
    A_policy --> E2 --> H_policy
    A_policy --> E3
    A_qa --> E4
    A_qa --> E5
    A_qa --> E6
    A_eng --> E7 --> H_license
    A_eng --> E8 --> S_next
    A_eng --> E9 --> H_db
	A_eng --> E10 --> H_hsm


## 내부시스템(UI포함) - 최초 설치 직후

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
    A1(관리자):::actor
    H1(자동으로 발급하다가 실패했을 경우에는?):::hotspot
    H2(그냥 TLS Server/Client 직접 발급할 수 있게 하면 안되나요...?):::hotspot
    O1(TLS용 인증서 수동 발급 자체가 안되진 않는 것 같던데):::opportunity
    H3(이거 시스템 내부적으로 TLS용 인증서를 별도의 테이블로 관리하고 있어서, 수동 발급한 애는 여기서 말하는 TLS Server Issuing CA로 등록이 안 되어요. 기능 추가가 필요합니다.):::hotspot
	S1(HSM):::system
	S2(외부PKI):::system
    %% --- 프로세스 흐름 ---
	A1 --> E01[Sub CA 인증서를 발급할 상위 인증서 체인이 구성됨] --> E02[Sub CA 인증서 발급 요청됨] --> E03[Sub CA 인증서용 비밀키가 생성됨] --> E04[Sub CA 인증서 서명됨] --> E05[Sub CA 상위 인증서 체인이 검증됨] --> E06[Sub CA 인증서 발급됨]
	S1 --> E03
	S1 --> E04
	A1 --> E11[사용자 계정 비밀번호 초기 설정 요청이 들어옴] --> E21[기존 CA Chain Import 됨] <--> S1
	E11 --> E31[외부 체인 참여용 CSR 발급] --> E32[외부 체인에 참여할 CA 인증서 발급됨] --> E33[CA 인증서의 키를 저장됨] <--> S1
	E32 <--> S2
	E11 --> E41[ROOT 인증서 초기화 요청됨] --> E42[Root 인증서용 비밀키 생성됨] <--> S1
	E42 --> E43[ROOT 인증서 서명됨] <--> S1
	E43 --> E44[ROOT 인증서 발급됨] --> E45[서버인증서 발급됨: RRA Leaf, TLS Client/Server Issuing CA, TLS Server Leaf]
	E45 --> H1 --> O1 --> H3
	E45 --> H2

--- End Mermaid Style Guidance ---

Output ONLY the Mermaid `flowchart LR` code block, including the `classDef` definitions. Do not include any other text or explanation.
