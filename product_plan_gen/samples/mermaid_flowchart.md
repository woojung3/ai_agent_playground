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

## 기타 - 운영중

flowchart LR
    %% --- 유형 정의 ---
    classDef actor       fill:#ffff00,stroke:#333,stroke-width:2px
    classDef command     fill:#add8e6,stroke:#333,stroke-width:2px
    classDef system      fill:#ffb6c1,stroke:#333,stroke-width:2px
    classDef hotspot     fill:#ff69b4,stroke:#333,stroke-width:6px
    classDef opportunity fill:#90ee90,stroke:#333,stroke-width:6px
    classDef policy      fill:#e6e6fa,stroke:#333,stroke-width:2px
    classDef readmodel   fill:#8fbc8f,stroke:#333,stroke-width:2px
    %% --- 요소 정의 ---
	A_admin(시스템 관리자):::actor
	A_user(유저):::actor
	S_db(DB):::system
	S_hsm(HSM):::system
	S_factory(공장서버실):::system
    %% --- 프로세스 흐름 ---
    S_db --> E1(서버 부하율이 출력됨) --> H1(서버 부하율 어떻게 추출?):::hotspot
	S_db --> E2(특정 노드가 죽었을 경우 DB 유효성이 맞는지 확인함)
	A_admin --> E3(특정 노드가 죽었을 경우 HSM 유효성이 맞는지 확인함) --> S_hsm
	A_admin --> E4(인증서 갱신 스케쥴링이 진행됨) --> H4(인증서 발급 프로파일에 갱신 여부 추가 필요):::hotspot
	E5(인증서 만료가 임박함) --> H5(알림 기능 구현해야 함?):::hotspot --> O5(필요할걸요 화면기획에 있는 것 같던데요):::opportunity
	A_user --> E6(개인키 복구 요청이 들어옴) --> H6(HSM 사용시 개인키 복구가 가능한가요?):::hotspot
	E6 --> H61(개인키 복구 기능이 필요한 기능인지 확인 필요):::hotspot
	E7(CA 갱신 스케쥴링이 진행됨) --> H7(CA 갱신만 해요? 종단 인증서는 갱신 스케쥴링은 안 하나요?):::hotspot --> O7(인증서 발급 프로파일에 갱신 여부 추가하면 처리 가능):::opportunity
	A_admin --> E8(서버 복구가 진행됨) --> S_factory
	A_admin --> E9(DB 복구가 진행됨) --> S_factory
	A_user --> E10(서버 부하가 임계치를 넘음) --> O10(모니터링 툴 추가하여 관리페이지 표출하면 좋지 않을까?):::opportunity --> O11(관리자 로그인시 알림 및 외부연동 알림 추가 기획이 있어요):::opportunity
	A_user --> E11(DB 부하가 임계치를 넘음) --> O10

## 외부시스템 연계 - 운영중

flowchart LR
    %% --- 유형 정의 ---
    classDef actor       fill:#ffff00,stroke:#333,stroke-width:2px
    classDef command     fill:#add8e6,stroke:#333,stroke-width:2px
    classDef system      fill:#ffb6c1,stroke:#333,stroke-width:2px
    classDef hotspot     fill:#ff69b4,stroke:#333,stroke-width:6px
    classDef opportunity fill:#90ee90,stroke:#333,stroke-width:6px
    classDef policy      fill:#e6e6fa,stroke:#333,stroke-width:2px
    classDef readmodel   fill:#8fbc8f,stroke:#333,stroke-width:2px
    %% --- 요소 정의 ---
	S_key(KeyLink):::system
	H1(OCSP 응답 속도가 요구사항 대비 충분한지?):::hotspot
	H2(모든 CA CRL 다운로드시 성능 문제?):::hotspot
	H3(어떤 CA에 요청한 것인지 URL을 통해서 구분하도록 하면 API 수정하는게 좋을 것 같음):::hotspot
	H4(종단 인증서 발급 성능이 충분한지?):::hotspot
	O1(SKI Hex로 구분되는 것 같던데):::opportunity
	O2(운영할 때 편리할 듯):::opportunity
    %% --- 프로세스 흐름 ---
	S_key --> E10(인증서 프로파일 생성 요청이 들어옴) --> E11(인증서 프로파일이 생성됨)
	S_key --> E21(CA 인증서 발급 프로파일 선택함) --> E22(CA 인증서 발급 요청됨) --> E23(상위 인증서 체인 검증됨) --> E24(CA 인증서 발급됨)
	E20(CA 인증서 발급 권한이 있는 RA 인증서 발급됨) --> E21
	S_key --> E30(OCSP 요청됨) --> H1
	E24 --> E240(CA 인증서 다운로드 요청됨)
	E24 --> E241(CA 인증서 폐기 요청됨)
	E24 --> E242(CA 인증서 갱신 요청됨)
	E24 --> E243(CA 인증서 내보내기 요청)
	E24 --> E244(CA 인증서의 CRL이 생성됨)
	E244 --> E2441(CRL이 자동 갱신됨) --> E24410(외부 채널에 알림이 전송됨) --> O2
	E2442a(인증서 만료 임박 메시지가 전송됨) --> E24410
	E2442b(시스템 오류 메시지가 전송됨) --> E24410
	E244 --> E2442(모든 CA의 CRL 다운로드를 요청함) --> H2
	E244 --> E2443(특정 CA의 CRL 다운로드를 요청함)
	S_key --> E31(종단 인증서 발급 프로파일 선택함)
	E30(종단 인증서 발급 권한이 있는 RA 인증서 발급됨) --> E31 --> E32(종단 인증서 생성 요청됨) --> E33(상위 인증서 체인 검증됨) --> E34(종단 인증서 발급됨) --> E341(종단 인증서 갱신 요청됨)
	E34 --> E342(종단 인증서 폐기 요청됨)
	E34 --> E343(종단 인증서 다운로드 요청됨)
	E34 --> H4
	E32 --> H3 --> O1

## 내부시스템(UI포함) - 계정관리

flowchart LR
    %% --- 유형 정의 ---
    classDef actor       fill:#ffff00,stroke:#333,stroke-width:2px
    classDef command     fill:#add8e6,stroke:#333,stroke-width:2px
    classDef system      fill:#ffb6c1,stroke:#333,stroke-width:2px
    classDef hotspot     fill:#ff69b4,stroke:#333,stroke-width:6px
    classDef opportunity fill:#90ee90,stroke:#333,stroke-width:6px
    classDef policy      fill:#e6e6fa,stroke:#333,stroke-width:2px
    classDef readmodel   fill:#8fbc8f,stroke:#333,stroke-width:2px
    %% --- 요소 정의 ---
	A_admin(시스템 관리자):::actor
	H(계정 추가 어떻게? 누가 필요로 하나요? 꼭 필요할까요?):::hotspot
    %% --- 프로세스 흐름 ---
	A_admin --> E1(계정이 조회 요청이 들어옴) --> E11(계정목록이 조회됨)
	A_admin --> E2(계정 수정 요청이 들어옴) --> E21(계정이 수정됨)
	A_admin --> E3(계정 삭제 요청이 들어옴) --> E31(계정이 삭제됨)
	A_admin --> E4(계정 추가 요청이 들어옴) --> E41(계정이 추가됨) --> H

## 내부시스템(UI포함) - 통계관리

flowchart LR
    %% --- 유형 정의 ---
    classDef actor       fill:#ffff00,stroke:#333,stroke-width:2px
    classDef command     fill:#add8e6,stroke:#333,stroke-width:2px
    classDef system      fill:#ffb6c1,stroke:#333,stroke-width:2px
    classDef hotspot     fill:#ff69b4,stroke:#333,stroke-width:6px
    classDef opportunity fill:#90ee90,stroke:#333,stroke-width:6px
    classDef policy      fill:#e6e6fa,stroke:#333,stroke-width:2px
    classDef readmodel   fill:#8fbc8f,stroke:#333,stroke-width:2px
    %% --- 요소 정의 ---
	A_admin(시스템 관리자):::actor
	H1(발급 현황 정합성은 어떻게 맞출 것인가?):::hotspot
	H2(통계 조회시 운영 서버에 영향 적도록 해야):::hotspot
	O1(그래프로 보여주면 좋을듯):::opportunity
	O2(대시보드에서 통계 그래프로 보여줄 예정입니다):::opportunity
    %% --- 프로세스 흐름 ---
	A_admin --> E1(관리자 계정으로 로그인에 성공) --> E2(대시보드에 접속됨)
	Ea(인증서 발급 현황 데이터 수집됨) --> E2
	Ea --> H1 --> O1 --> O2
	Eb(인증서 요청 현황 데이터 수집됨) --> E2
	E2 --> E21(인증서 발급 현황 조회됨)
	E2 --> E22(인증서 발급 요청 현황 조회됨)
	E2 --> E2a(인증서 발급 통계 조회 요청이 들어옴) --> H2

## 내부시스템(UI포함) - 기타관리

flowchart LR
    %% --- 유형 정의 ---
    classDef actor       fill:#ffff00,stroke:#333,stroke-width:2px
    classDef command     fill:#add8e6,stroke:#333,stroke-width:2px
    classDef system      fill:#ffb6c1,stroke:#333,stroke-width:2px
    classDef hotspot     fill:#ff69b4,stroke:#333,stroke-width:6px
    classDef opportunity fill:#90ee90,stroke:#333,stroke-width:6px
    classDef policy      fill:#e6e6fa,stroke:#333,stroke-width:2px
    classDef readmodel   fill:#8fbc8f,stroke:#333,stroke-width:2px
    %% --- 요소 정의 ---
	A_admin(시스템 관리자):::actor
	A_requester(인증서 발급 요청자):::actor
	H1(복구 불가능한 시나리오는 어떻게 핸들링?):::hotspot
	H2(EKU 말고도 잠재적으로 추가될만한 것들은 어떤 것이 있나요?):::hotspot
	H3(Oid Field 수정 기능의 필요성?):::hotspot
	H4(Oid Value 수정 기능의 필요성?):::hotspot
	H5(어떤 방식으로 구현해야 할지? 이력 테이블을 만들어서 인증서 발급시 데이터 추가?):::hotspot
	H6(개인키 분실의 의미?):::hotspot
	H7(이거 돼요?):::hotspot
	H8(어떤 스케쥴러를 말하는 건가요?):::hotspot
	O1(수정보다는 삭제 후 추가가 좋을듯):::opportunity
	O2(아니요):::opportunity
	O3(높은 확률로 CRL 갱신 스케쥴러인듯):::opportunity
	O4(CA 인증서 자동갱신이랑 CA 인증서 만료시 자동알림 같은거더라구요: 만료 n일전 자동갱신 실행 혹은 만료 n일전 자동 알림 발송 등):::opportunity
    %% --- 프로세스 흐름 ---
	A_admin --> E1(시스템이 복구됨) --> H1
	A_admin --> E2(관리자 계정으로 로그인에 성공)
	E2 --> E21(Custom Oid Field 생성 요청이 들어옴)
	E2 --> E22(어떤 프로파일과 Oid로 발급한 인증서인지 이력확인을 요청함) --> H5
	E2 --> E23(발급받은 인증서가 요청한 프로파일에 부합한지 검증)
	E2 --> E24(CA 인증서가 발급됨)
	E2 --> E25(서버 설정 페이지에 접속함)
	E2 --> E26(OCSP 인증서 목록 조회함) --> E261(OCSP 인증서 생성 요청됨)
	E21 --> H2
	E21 --> E211(Custom Oid Field가 생성됨) --> E2111(Custom Oid Field 삭제 요청이 들어옴)
	E211 --> E2112(Custom Oid Field 수정 요청이 들어옴) --> H3 --> O1
	E211 --> E2113(Custom Oid Value 생성 요청이 들어옴) --> E21131(Custom Oid Value가 생성됨) --> E211311(Custom Oid Value 수정 요청이 들어옴) --> H4 --> O1
	E21131 --> E22312(Custom Oid 삭제 요청이 들어옴)
	E24 --> A_requester --> E241(개인키가 분실됨) --> A_admin --> E242(개인키 복구됨) --> H7 --> O2
	E241 --> H6
	E25 --> E251(세션 타임아웃 설정 변경 요청이 들어옴)
	E25 --> E252(스케쥴러 설정 변경 요청이 들어옴) --> H8 --> O3 --> O4
	E25 --> E253(CRL 업데이트 시간 변경 요청이 들어옴)

## 내부시스템(UI포함) - 운영관리

flowchart LR
    %% --- 유형 정의 ---
    classDef actor       fill:#ffff00,stroke:#333,stroke-width:2px
    classDef command     fill:#add8e6,stroke:#333,stroke-width:2px
    classDef system      fill:#ffb6c1,stroke:#333,stroke-width:2px
    classDef hotspot     fill:#ff69b4,stroke:#333,stroke-width:6px
    classDef opportunity fill:#90ee90,stroke:#333,stroke-width:6px
    classDef policy      fill:#e6e6fa,stroke:#333,stroke-width:2px
    classDef readmodel   fill:#8fbc8f,stroke:#333,stroke-width:2px
    %% --- 요소 정의 ---
	A_admin(시스템 관리자):::actor
    %% --- 프로세스 흐름 ---
	A_admin --> E1(관리자 계정으로 로그인에 성공)
	E1 --> E2(종단 인증서 발급 프로파일 선택함)
	E2 --> E21(종단 인증서 발급 요청됨) --> E22(종단 인증서 발급됨) --> H22(인증서 발급 후 발급된 인증서를 포함한 체인 검증 중):::hotspot
	E21 --> O21(P10CR 발급기능 추가 필요):::opportunity
	E21 --> H21(발급 실패 이벤트가 필요하지 않을까? 전체적으로 해피케이스만 있는듯):::hotspot
	E1 --> E3(ROOT 인증서 발급 프로파일 선택함)
	E3 --> E31(ROOT 인증서 발급 요청됨) --> E32(ROOT 인증서 발급됨)
	E32 --> E321(RRA 인증서 재발급 요청함) --> E322(RRA 인증서 발급됨)
	E32 --> E322 --> H322(RRA 인증서 자동 갱신이 필요해보임. 사실, CA, OCSP 다 필요):::hotspot
	E1 --> E4(CA 인증서 발급 프로파일 선택함) --> E41(CA 인증서 발급 요청됨) --> E42(CA 인증서 발급됨) --> E43(CA 인증서의 CRL이 생성됨) --> H43(CRL 스케쥴러와 수동갱신 등의 기능 제공이 필요):::hotspot
	E41 --> H41(CA 인증서 발급 시 HSM 키 생성이 필요함):::hotspot
	E41 --> O41(요청 전에 키를 미리 만들어두면 발급 성능이 크게 향상될 듯)
	E1 --> E5(RA 인증서 권한을 설정함)
	E5 --> E51(RA인증서 발급을 요청함) --> E52(RA 인증서 발급됨)
	E52 --> E521(발급한 RA 인증서를 pfx 파일로 다운로드함)
	E52 --> E522(다운로드 받은 RA 인증서를 통해 mTLS 인증 테스트)
	E52 --> E523(발급된 RA 인증서의 권한 변경을 요청함)
	E1 --> E6(인증서 프로파일 생성 요청이 들어옴)
	E6 --> E61(인증서 프로파일을 템플릿으로 저장하는 요청이 들어옴) --> E64(인증서 프로파일이 생성됨)
	E6 --> E62(인증서 프로파일 생성시 관리자 승인 필요 제약을 거는 요청이 들어옴) --> E64
	E6 --> E63(인증서 프로파일 필드 제약 규칙 추가 요청이 들어옴) --> E64
	E6 --> H6(OID 정책을 명확하게 정의해야 함. CP/CPS와 관련이 있을까?):::hotspot --> H61(인증서 프로파일에 어떤 데이터가 들어가야 하는지 명확했으면 좋겠음. 이 부분이 명확해지면 인증서 프로파일 상속 기능을 더 잘 구현할 수 있을 것 같음):::hotspot
	E61 --> H61(템플릿으로 저장한다는 것이, 저장한 프로파일을 불러와서 그 내용을 베이스로 새로 만드는 것인지?):::hotspot
	E63 --> H63(조금 더 구체적인 기준을 정해야 할 것 같습니다. 어떤 필드만 허용할 것인지 등. 지금 프로파일 만들 때 DN도 안 받고 있고요):::hotspot
	E1 --> E7(발급된 CA 인증서 목록 조회 요청함)
	E7 --> E71(인증서 상세 정보 조회 요청함) --> O71(인증서 유효기간 표시에 타임존 선택 기능 필요):::opportunity
	E7 --> E72(CA 인증서 폐기 요청됨) --> E73(폐기 사유를 선택함) --> E74(인증서 폐기됨) --> H74(폐기된 인증서는 복구가 가능한가요?):::hotspot
	E73 --> H73(HSM에 쌓인 키를 어떻게 정리하면 좋을지 논의가 필요해 보임):::hotspot
	H74 --> O741(폐기 사유에 따라 복구 가능/불가를 정해도 좋을 것 같긴 한데):::opportunity
	H74 --> O742(폐기는 복구 안 되어야 할걸요):::opportunity
	E7 --> E73(CA 인증서 갱신 요청됨) --> O73(사용자가 직접 원하는 갱신 기간을 설정할 수 있다면 더 편할 것 같아요):::opportunity
	E7 --> E74(CA 인증서 다운로드 요청됨)
	E7 --> E75(CA 인증서 및 키 내보내기 요청)
	E1 --> E8(발급된 종단 인증서 목록 조회 요청함) --> E81(종단 인증서 상세 정보 요청함)
	E81 --> E811(종단 인증서 갱신 요청됨)
	E81 --> E812(종단 인증서 폐기 요청됨)
	E81 --> E813(종단 인증서 다운로드 요청됨)
