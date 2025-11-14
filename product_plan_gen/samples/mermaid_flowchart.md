## 관리자 - 서버 초기 설정
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

    A_suadm(슈퍼 어드민):::actor
	
	Ea1(슈퍼 어드민 자동 생성됨)
	Ea2(슈퍼 어드민 로그인됨)
	Ea3(슈퍼 어드민 페이지에서 센터 생성됨)
	Ea4(슈퍼 어드민 페이지에서 센터 설정됨)
	Ea4_a1(센터별 주행 요금제가 설정됨)
	Ea4_b1(센터 약관이 등록됨)
	Ea4_b2(센터 약관이 수정됨)

	Ea1 --> Ea2 --> Ea3 --> Ea4 --> Ea4_a1
	Ea4 --> Ea4_b1 --> Ea4_b2
	A_suadm --> Ea2
```

## 관리자 - 일반 관리자 초기 설정
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

    A_suadm(슈퍼 어드민):::actor
    %% A_ctradm(센터 관리자):::actor
    %% A_adm(일반 관리자):::actor
    %% A_user(회원):::actor
    %% A_driver(기사):::actor
	
	Eb1(슈퍼 어드민 페이지에서 일반 관리자 등록됨)
	Eb2(관리자가 로그인됨)
	Eb2_a1(회원이 등록됨)
	Eb2_b1(기사가 등록됨)
	Eb2_c1(차량 모델이 등록됨)
	Eb2_d1(회원이 일괄 등록됨)
	Eb2_e1(기사가 일괄 등록됨)
	Eb2_f1(차량이 일괄 등록됨)
	Eb2_g1(회원이 일괄 수정됨)
	Eb2_h1(기사가 일괄 수정됨)
	Eb2_i1(관리자가 로그아웃됨)
	
	Eb2_a1_a1(회원 목록이 조회됨)
	Eb2_a1_b1(회원 상세 정보가 조회됨)
	Eb2_a1_c1(회원 정보가 수정됨)
	Eb2_a1_d1(회원이 삭제됨)

	Ob2_a1_c1(회원 수정 이력 저장 기능 필요):::opportunity
    S_excel(엑셀 템플릿):::system

	A_suadm --> Eb1 --> Eb2 --> Eb2_a1 --> Eb2_a1_a1
	Eb2_a1 --> Eb2_a1_b1
	Eb2_a1 --> Eb2_a1_c1
	Ob2_a1_c1 --> Eb2_a1_c1
	Eb2_a1 --> Eb2_a1_d1
	A_adm --> Eb2
	
	Eb2 --> Eb2_d1 
	S_excel --> Eb2_d1
	Eb2 --> Eb2_e1 
	S_excel --> Eb2_e1
	Eb2 --> Eb2_f1 
	S_excel --> Eb2_f1
	Eb2 --> Eb2_g1 
	S_excel --> Eb2_g1
	Eb2 --> Eb2_h1 
	S_excel --> Eb2_h1
	Eb2 --> Eb2_i1 
	
	Eb2_b1_a1(기사 행정 일정 스케줄이 삭제됨)
	Eb2_b1_b1(기사가 조회됨)
	Eb2_b1_b2(기사 행정 일정 스케줄이 등록됨)
	Eb2_b1_c1(차량에 담당기사가 등록됨)
	
	Ob2_b1_c1_1(차량에 15명의 기사 등록가능 - VoC 반영):::opportunity
	Ob2_b1_c1_2(차량 1대당 최대 기사 3명까지 등록가능):::opportunity
	
	Eb2 --> Eb2_b1 --> Eb2_b1_a1
	Eb2_b1 --> Eb2_b1_b1 --> Eb2_b1_b2
	Eb2_b1 --> Eb2_b1_c1
	
	Ob2_b1_c1_1 --> Eb2_b1_c1
	Ob2_b1_c1_2 --> Eb2_b1_c1
	
	Eb2_c1_a1(차량이 등록됨)
	Eb2_c1_a2(차량이 조회됨)
	Eb2_c1_b1(차량 모델이 조회됨)
	Eb2_c1_c1(차량 모델이 삭제됨)
	
	Eb2_c1 --> Eb2_c1_a1 --> Eb2_c1_a2 --> Eb2_b1_c1
	Eb2_c1 --> Eb2_c1_b1
	Eb2_c1 --> Eb2_c1_c1
	
	Eb2_b1_c1_a1(기사 근무 스케줄이 등록됨)
	Eb2_b1_c1_b1(기사 근무 스케줄 목록이 조회됨)
	Eb2_b1_c1_c1(일별 기사 예약 스케줄이 조회됨)
	Eb2_b1_c1_d1(기사 스케줄이 이동됨)
	
	Eb2_b1_c1 --> Eb2_b1_c1_a1
	Eb2_b1_c1 --> Eb2_b1_c1_b1
	Eb2_b1_c1 --> Eb2_b1_c1_c1
	Eb2_b1_c1 --> Eb2_b1_c1_d1
	
	Eb2_b1_c1_a1_a1(기사 휴식 스케줄이 등록됨)
	Eb2_b1_c1_a1_b1(기사 근무 스케줄이 수정됨)
	Eb2_b1_c1_a1_c1(기사 일정이 다른 기사에게 이동됨)

	Hb2_b1_c1_a1_a1(자동 휴식 배정 정책 필요):::hotspot
	Hb2_b1_c1_a1_a1 --> Eb2_b1_c1_a1_a1
	
	Eb2_b1_c1_a1 --> Eb2_b1_c1_a1_a1 --> Eb2_b1_c1_a1_a2(기사 휴식 스케줄이 수정됨)
	Eb2_b1_c1_a1 --> Eb2_b1_c1_a1_b1
	Eb2_b1_c1_a1 --> Eb2_b1_c1_a1_c1
```

## 관리자 - 일상 운영
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

    A_suadm(슈퍼 어드민):::actor
    %% A_ctradm(센터 관리자):::actor
    A_adm(일반 관리자):::actor
    A_user(회원):::actor
    %% A_driver(기사):::actor
	
	S_map(지도 서비스):::system
	S_firebase(Firebase):::system
	S_ncp(문자발송 서버):::system
	S_safenum(안심번호 발급 서버):::system
	
	Ec1_a1(유선으로 예약이 요청됨)
	Ec1_a2(예약이 접수됨)
	Oc1_a2(상습 무단 취소 승객으로 블랙리스트 표시 기능 필요):::opportunity
	Ec1_a3(출발지에게 경유지, 목적지까지의 주행거리가 계산됨)
	Ec1_a4(승객의 예약의 중복여부가 확인됨)
	Ec1_a5(예약이 등록됨)
	Ec1_b1(배송이 요청됨)
	Ec1_b2(배송이 접수됨)
	Hc1_b2(예약과 동시간대에 중복하여 접수 가능):::hotspot
	Ec1_c1(취소된 예약 내역이 조회됨)
	Ec1_c2(취소된 예약이 복구요청 됨)
	Ec1_d1(예약 내역이 조회됨)

	A_user --> Ec1_a1
	A_user --> Ec1_b1
	A_adm --> Ec1_c1
	A_adm --> Ec1_d1
	A_adm --> Ec1_a2
	Oc1_a2 --> Ec1_a2
	A_adm --> Ec1_b2
	Hc1_b2 --> Ec1_b2
	Ec1_a1 --> Ec1_a2 --> Ec1_a3 --> S_map
	Ec1_b1 --> Ec1_b2 --> Ec1_a3 --> Ec1_a4 --> Ec1_a5
	Ec1_c1 --> Ec1_c2 --> Ec1_a3
	
	Ec1_a5_a1(접수 기록에 예약 내역이 생성됨)
	Ec1_a5_b1(배차대기 상태로 전환됨)
	Ec1_a5_c1(다량의 예약이 등록됨)
	Ec1_a5_c2(전체 기사, 즉 차량의 배차 일정이 확인됨)
	Ec1_a5_c3(다량의 예약이 일괄 배차됨)
	Oc1_a5_c3(일괄배차의 예약취소와 예약변경 문자 송신 기능 필요):::opportunity
	Hc1_a5_c1(16시쯤 전화가 몰림, 배차대기로 일괄 예약접수 후 자동 혹은 수동배차로 진행):::hotspot
	
	Ec1_a5 --> Ec1_a5_a1
	Ec1_a5 --> Ec1_a5_b1
	Ec1_a5 --> Ec1_a5_c1
	A_adm --> Ec1_a5_c1
	Hc1_a5_c1 --> Ec1_a5_c1 --> Ec1_a5_c2 --> Ec1_a5_c3
	A_adm --> Ec1_a5_c2
	A_adm --> Ec1_a5_c3
	Oc1_a5_c3 --> Ec1_a5_c3 --> Ec1_a5_b1_a2
	
	Ec1_a5_b1_a1(자동배차됨)
	Hc1_a5_b1_a1(자동배차됨):::hotspot
	Hc1_a5_b1_a1 --> Ec1_a5_b1_a1
	Ec1_a5_b1_a2(예약 완료 상태 전환됨)
	Ec1_a5_b1_b1(예약이 수동배차됨)
	A_adm --> Ec1_a5_b1_b1
	Ec1_a5_b1_c1(예약이 자동배차 실패됨)
	Ec1_a5_b1_c2(자동배차가 실패 후 수동배차 가능 시간이 출력됨)
	
	Ec1_a5_b1 --> Ec1_a5_b1_a1 --> Ec1_a5_b1_a2
	Ec1_a5_b1 --> Ec1_a5_b1_b1 --> Ec1_a5_b1_a2
	Ec1_a5_b1 --> Ec1_a5_b1_c1 --> Ec1_a5_b1_c2 --> Ec1_a5_b1_b1
	A_adm --> Ec1_a5_b1_b1
	
	Ec1_a5_b1_a2_a1(당일예약의 경우, 배차 내역이 기사앱에 푸시로 발송됨)
	Ec1_a5_b1_a2_a1 --> S_firebase
	Ec1_a5_b1_a2_b1(예약 내역이 문자로 승객에게 발송됨)
	Ec1_a5_b1_a2_b1 --> S_ncp
	Ec1_a5_b1_a2_c1(모든 탑승자에게 안심번호 할당됨)
	Ec1_a5_b1_a2_c1 --> S_safenum
	Hc1_a5_b1_a2_c1(안심번호 할당 정책 필요):::hotspot
	Hc1_a5_b1_a2_c1 --> S_safenum
	Ec1_a5_b1_a2_d1(예약정보만 변경됨)
	Ec1_a5_b1_a2_e1(예약 변경 요청됨)
	A_user --> Ec1_a5_b1_a2_e1
	Ec1_a5_b1_a2_f1(예약이 취소 요청됨)
	A_user --> Ec1_a5_b1_a2_f1
	
	Ec1_a5_b1_a2 --> Ec1_a5_b1_a2_a1
	Ec1_a5_b1_a2 --> Ec1_a5_b1_a2_b1
	Ec1_a5_b1_a2 --> Ec1_a5_b1_a2_c1
	Ec1_a5_b1_a2 --> Ec1_a5_b1_a2_d1
	Ec1_a5_b1_a2 --> Ec1_a5_b1_a2_e1
	Ec1_a5_b1_a2 --> Ec1_a5_b1_a2_f1
	
	Ec1_a5_b1_a2_e2(배차가 취소됨)
	Ec1_a5_b1_a2_e1 --> Ec1_a5_b1_a2_e2
	A_adm --> Ec1_a5_b1_a2_e2
	Oc1_a5_b1_a2_e2(예약 수정 이력 저장 기능 필요):::opportunity
	Oc1_a5_b1_a2_e2 --> Ec1_a5_b1_a2_e2
	
	Ec1_a5_b1_a2_e2_a1(예약이 변경됨)
	Ec1_a5_b1_a2_e2_b1(업무일지에 예약내역이 갱신됨)
	Ec1_a5_b1_a2_e2_c1(접수기록에 예약내역이 갱신됨)
	
	Ec1_a5_b1_a2_e2 --> Ec1_a5_b1_a2_e2_a1
	Ec1_a5_b1_a2_e2 --> Ec1_a5_b1_a2_e2_b1
	Ec1_a5_b1_a2_e2 --> Ec1_a5_b1_a2_e2_c1
	
	Ec1_a5_b1_a2_f2(배차가 취소됨)
	Ec1_a5_b1_a2_f1 --> Ec1_a5_b1_a2_f2
	A_adm --> Ec1_a5_b1_a2_f2
	Ec1_a5_b1_a2_f2 --> Ec1_a5_b1_a2_e2_b1
	Ec1_a5_b1_a2_f2 --> Ec1_a5_b1_a2_e2_c1
	
	Ec1_a5_b1_a2_e2_a1_a1(배차대기 상태로 전환됨)
	Ec1_a5_b1_a2_e2_a1_b1(기사앱으로 예약변경 푸시 발송됨)
	Ec1_a5_b1_a2_e2_a1_b2(예약변경 푸시 발송이 확인됨)
	Ec1_a5_b1_a2_e2_a1_c1(승객에게 예약변경 문자 발송됨)
	Ec1_a5_b1_a2_e2_a1_c2(예약변경 문자 발송 확인됨)
	
	Ec1_a5_b1_a2_e2_a1 --> Ec1_a5_b1_a2_e2_a1_a1
	Ec1_a5_b1_a2_e2_a1 --> Ec1_a5_b1_a2_e2_a1_b1 --> Ec1_a5_b1_a2_e2_a1_b2
	Ec1_a5_b1_a2_e2_a1_b1 --> S_firebase
	Ec1_a5_b1_a2_e2_a1 --> Ec1_a5_b1_a2_e2_a1_c1 --> Ec1_a5_b1_a2_e2_a1_c2
	Ec1_a5_b1_a2_e2_a1_c1 --> S_ncp
	
	Ec1_a5_b1_a2_f3(예약이 무단 혹은 정상 취소됨)
	Ec1_a5_b1_a2_f2 --> Ec1_a5_b1_a2_f3
	
	Ec1_a5_b1_a2_f3_a1(승객에게 예약취소 문자 발송됨)
	Ec1_a5_b1_a2_f3_a2(예약취소 문자 발송 확인됨)
	Oc1_a5_b1_a2_f3_a2(문자 발송에 대한 성공/실패에 대한 내역을 관리자에서 확인 가능하면 좋겠음):::opportunity
	Hc1_a5_b1_a2_f3_a2(문자 발송에 대한 클레임이 많음):::hotspot
	Ec1_a5_b1_a2_f3_b1(기사앱으로 예약취소 푸시 발송됨)
	Ec1_a5_b1_a2_f3_b2(예약취소 푸시 발송이 확인됨)
	Ec1_a5_b1_a2_f3_c1(예약자의 무단 취소 횟수가 증가됨)
	Oc1_a5_b1_a2_f3_c1(무단취소에 대한 블랙리스트 관리가 있으면 좋겠음):::opportunity
	Hc1_a5_b1_a2_f3_c1(무단은 승객에 의한 취소, 정상은 그 외):::hotspot
	
	Ec1_a5_b1_a2_f3 --> Ec1_a5_b1_a2_f3_a1 --> S_ncp
	Ec1_a5_b1_a2_f3_a1 --> Ec1_a5_b1_a2_f3_a2
	Oc1_a5_b1_a2_f3_a2 --> Ec1_a5_b1_a2_f3_a2
	Hc1_a5_b1_a2_f3_a2 --> Ec1_a5_b1_a2_f3_a2
	Ec1_a5_b1_a2_f3 --> Ec1_a5_b1_a2_f3_b1 --> Ec1_a5_b1_a2_f3_b2
	Ec1_a5_b1_a2_f3_b1 --> S_firebase
	Ec1_a5_b1_a2_f3 --> Ec1_a5_b1_a2_f3_c1
	
	Oc1_a5_b1_a2_f3_c1 --> Ec1_a5_b1_a2_f3_c1
	Hc1_a5_b1_a2_f3_c1 --> Ec1_a5_b1_a2_f3_c1
```

## 관리자 - 기사 연계
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

    %% A_suadm(슈퍼 어드민):::actor
    %% A_ctradm(센터 관리자):::actor
    %% A_adm(일반 관리자):::actor
    %% A_user(회원):::actor
    A_driver(기사):::actor
	
	S_map(지도 서비스):::system
	S_firebase(Firebase):::system
	S_ncp(문자발송 서버):::system
	
	Ed1_a1(출발시간 N분전 문자 발송됨)
	Ed1_b1(주행이 시작됨)
	
	Ed1_a1 --> S_ncp
	A_driver --> Ed1_b1
	
	Ed1_b1_a1(지도에서 차량의 위치가 조회됨)
	Ed1_b1_a1 --> S_map
	Ed1_b1_a1 --> S_firebase
	Ed1_b1_b1(예약내역에서 운행중으로 상태 변경됨)
	Ed1_b1_c1(주행내역에 새로운 행이 생성됨)
	Ed1_b1_d1(주행이 강제 종료됨)
	Ed1_b1_d1_a1(주행 완료됨)
	Ed1_b1_d1_a2(종료 푸시 발송됨)
	Ed1_b1_d1_a2 --> S_firebase
	Ed1_b1_d1_a3(주행 종료 푸시 확인됨)
	Ed1_b1_d1_b1(강제종료 시점까지의 주행기록이 저장됨)
	
	Ed1_b1 --> Ed1_b1_a1
	Ed1_b1 --> Ed1_b1_b1
	Ed1_b1 --> Ed1_b1_c1
	Ed1_b1 --> Ed1_b1_d1
	Hd1_b1_d1(강제 주행 종료시 요금 산정 방식. 주행내역에서 요금 입력함. 1. 강제종료 시 이용요금은 예약정보 기반으로 계산되고, 필요시 이후 관리자시스템에서 별도로 요금정보를 수정. 2. 강제종료시 기사앱에서 결제처리가 안된 승객의 결제요금은 0원으로 처리. 이후 관리자시스템에서 별도로 결제정보를 수정.):::hotspot
	Hd1_b1_d1 --> Ed1_b1_d1
	Ed1_b1_d1 --> Ed1_b1_d1_a1 --> Ed1_b1_d1_a2 --> Ed1_b1_d1_a3
	Ed1_b1_d1 --> Ed1_b1_d1_b1
	Hd1_b1_d1_b1(종료 전까지 저장된 데이터 기반, 혹은 없다면 예약 내역 기반으로 데이터 처리):::hotspot
	Hd1_b1_d1_b1 --> Ed1_b1_d1_b1
```

## 관리자 - 주행 종료 처리
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

    %% A_suadm(슈퍼 어드민):::actor
    %% A_ctradm(센터 관리자):::actor
    %% A_adm(일반 관리자):::actor
    %% A_user(회원):::actor
    %% A_driver(기사):::actor
	
	%% S_map(지도 서비스):::system
	%% S_firebase(Firebase):::system
	%% S_ncp(문자발송 서버):::system
	
	Ee1_a1(주행이 종료됨)
	Ee1_b1(주행 요금이 수정됨)
	Ee1_c1(주행 내역에 탑승자가 추가됨)
	Ee1_d1(주행정보가 업무일지에 계산됨)
	Ee1_e1(결제 내역이 관리자시스템 주행 상세 정보에 입력 혹은 갱신됨)
	Ee1_f1(주행 상세내역에 분당 위치데이터 표출됨)
	Ee1_f2(데이터 클릭시, 지도에 포인팅됨)
	Ee1_f1 --> Ee1_f2
	
	Ee1_a1_a1(주행상세정보에서 탑승자 정보 변경됨)
	Ee1_a1_a1_a1(추가 미예약자를 등록함. 기존 회원)
	Ee1_a1_a1_b1(기사앱에서 등록된 미예약자를 회원으로 치환함)
	Ee1_a1_a1_c1(탑승자별 탑승지 혹은 하차지를 변경함)
	Ee1_a1_a1_c2(요금정보가 자동 변경됨)
	He1_a1_a1_c2(요금 변경 정책 필요):::hotspot
	Ee1_a1_a1_d1(신규 회원 등록함)
	Ee1_a1_b1(주행상세정보에서 결제내역 정보 수정함)
	He1_a1_b1(결제 요금을 수정하는 케이스가 있음. 예를 들어 실제 5km 주행했는데 10km로 거리가 계산되어 요금을 초과하여 납부해야 하는 경우에 실제 5km의 금액을 지불하고 관리자에서 후처리를 해줌):::hotspot
	Ee1_a1_b1_a1(결제정보 내용이 갱신됨)
	Ee1_a1_b1_b1(결제이력에 내용 생성됨)
	Ee1_a1_c1(주행상세정보에서 요금 정보 수정함)
	Ee1_a1_c1_a1(요금정보 내용이 갱신됨)
	Ee1_a1_c1_b1(결제이력에 내용 생성됨)
	Ee1_a1_d1(주행상세정보에서 탑승자별 탑승/미탑승 상태 변경함)
	Ee1_a1_d1_a1(업무일지 내역 갱신됨)
	He1_a1_d1_a1(용도별 이용현황의 전체와 각 세부 항목의 합이 맞지 않은 스펙 개선 필요):::hotspot
	Ee1_a1_d1_a2(통계 현황 수집에 내용 갱신됨)
	Ee1_a1_d1_b1(결제정보 내역에서 삭제됨)
	Ee1_a1_d1_c1(주행내역에 표시되는 수치가 갱신됨)
	
	Ee1_a1 --> Ee1_a1_a1
	Ee1_a1 --> Ee1_a1_b1
	He1_a1_b1 --> Ee1_a1_b1
	Ee1_a1 --> Ee1_a1_c1
	Ee1_a1 --> Ee1_a1_d1
	
	Ee1_a1_a1 --> Ee1_a1_a1_a1
	Ee1_a1_a1 --> Ee1_a1_a1_b1
	Ee1_a1_a1 --> Ee1_a1_a1_c1 --> Ee1_a1_a1_c2
	He1_a1_a1_c2 --> Ee1_a1_a1_c2
	Ee1_a1_a1 --> Ee1_a1_a1_d1
	
	Ee1_a1_b1 --> Ee1_a1_b1_a1
	Ee1_a1_b1 --> Ee1_a1_b1_b1
	
	Ee1_a1_c1 --> Ee1_a1_c1_a1
	Ee1_a1_c1 --> Ee1_a1_c1_b1
	
	Ee1_a1_d1 --> Ee1_a1_d1_a1 --> Ee1_a1_d1_a2
	He1_a1_d1_a1 --> Ee1_a1_d1_a1
	Ee1_a1_d1 --> Ee1_a1_d1_b1
	Ee1_a1_d1 --> Ee1_a1_d1_c1
```

## 관리자 - 기타
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

    %% A_suadm(슈퍼 어드민):::actor
    A_ctradm(센터 관리자):::actor
    A_adm(일반 관리자):::actor
    %% A_user(회원):::actor
    A_driver(기사):::actor
	
	%% S_map(지도 서비스):::system
	%% S_firebase(Firebase):::system
	%% S_ncp(문자발송 서버):::system
	
	A_adm --> Ef1_a1(분실물 목록이 조회됨) --> Ef1_a2(분실물이 등록됨) --> Ef1_a3(분실물이 삭제됨)
	A_adm --> Ef1_b1(공지사항 목록이 조회됨)
	Ef1_b1_a1(공지사항 상세 정보가 조회됨)
	Ef1_b1_b1(공지사항이 등록됨)
	Ef1_b1_b1_a1(공지사항이 수정됨)
	Ef1_b1_b1_b1(공지사항이 삭제됨)
	Ef1_b1 --> Ef1_b1_a1
	Ef1_b1 --> Ef1_b1_b1
	Ef1_b1_b1 --> Ef1_b1_b1_a1
	Ef1_b1_b1 --> Ef1_b1_b1_b1
	A_driver --> Ef1_c1(기사앱의 계기판 거리가 입력됨) --> Ef1_c2(차량 운행 정보가 조회됨)
	A_ctradm --> Ef1_c2(차량 운행 정보가 조회됨)
	Ef1_c2_a1(차량 운행 정보가 수정됨)
	Ef1_c2_b1(차량 운행 정보가 일괄 수정됨)
	Ef1_c2 --> Ef1_c2_a1
	Ef1_c2 --> Ef1_c2_b1
	A_ctradm --> Ef1_d1(차량 주유 정보가 조회됨) --> Ef1_d2(차량 주유 정보가 등록됨)
	Of1_d1(주유나 정비 등 기사앱에서도 직접 등록할 수 있게 개선해달라는 요구사항도 존재):::opportunity --> Ef1_d1
	Hf1_d2(관리자가 기사로부터 전달받아 등록):::hotspot --> Ef1_d2
	Ef1_e1(데이터 다운로드됨)
	Ef1_f1(차량의 위치 정보가 지도위에 표시됨)
	Ef1_g1(매일 새벽 1시에 관리자시스템에서 통계현황에 카운팅됨)
	A_ctradm --> Ef1_h1(원격지원 요청됨)
	A_ctradm --> Ef1_i1(센터관리의 센터정보 및 용도 수정함)
	A_ctradm --> Ef1_j1(차량 정비 정보가 등록됨)
	Of1_j1(OBD를 통해 주유, 정비 정보를 조회할 수 있으면 좋겠음):::opportunity --> Ef1_j1
	A_ctradm --> Ef1_k1(통합관제에서 차량 위치와 운행상태를 확인됨)
```


---
## 기사앱 - 초기 설정
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

    %% A_adm(일반 관리자):::actor
    A_driver(기사):::actor
	
	S_bizone(비즈원 Pay 시스템):::system
	%% S_kg(KG 이니시스 페이팜):::system
	%% S_firebase(Firebase):::system
	%% S_safenum(안심번호 서비스):::system
	%% S_nav(내비게이션 앱):::system

	Eg1_a1(기사앱이 설치됨)
	A_driver --> Eg1_a1
	Eg1_a2(기사앱이 실행됨)
	Eg1_a2_a1(기사앱 버전이 비교됨)
	Eg1_a2_a1_a1(기사 로그인됨)
	Eg1_a2_a1_b1(앱 권한이 승인됨)
	Eg1_a2_a1_b2(기사 인증이 시도됨)
	Eg1_a2_a1_b3(기사 인증번호 확인됨)
	Eg1_a2_a1_b4(약관 동의됨)
	Hg1_a2_a1_b4_1(약관동의가 계속 발생함. 저장도 안 됨. 약관동의자, 동의시간에 대해서 내역 남길 수 있도록 처리 필요):::hotspot
	Hg1_a2_a1_b4_2(약관 관리 정책 필요):::hotspot
	Eg1_a2_a1_c1(선택 업데이트됨)
	Eg1_a2_a1_d1(강제 업데이트됨)
	Eg1_a2_b1(QR 코드로 하드웨어 등록됨)
	Eg1_a2_b2(차량에 OBD 장착됨)
	Eg1_d1(차량이 시동됨)
	Eg1_a2_b2_a1(OBD와 기사앱이 블루투스로 연결됨)
	Eg1_a2_b2_b1(OBD와 기사앱이 자동으로 연결됨)
	Eg1_a2_b2_c1(OBD와 기사앱이 블루투스로 연결이 실패됨)
	Eg1_b1(OBD 배송됨)
	Hg1_b1(OBD 등록, 장착, 연결 가이드 필요):::hotspot
	Eg1_c1(비즈원 결제 단말기 배송됨)
	Hg1_c1(비즈원 결제 단말기 및 앱설치 가이드와 연동 가이드 필요):::hotspot
	Eg1_c2(비즈원 결제 단말기가 실행됨)
	Eg1_c3(비즈원 결제단말기와 비즈원 pay앱 연동됨)
	Eg1_e1(비즈원 pay앱 설치됨)
	Eg1_a2_a1_a1_2(자동 로그인됨)
	Hg1_a2_a1_a1_2(인증이 없음... 위치기반서비스 실태조사 대비용으로 필요):::hotspot
	Eg1_a2_a1_a1_3(간편 로그인됨)
	Hg1_a2_a1_a1_3(위치기반 대응시 문제가 있는지 검토 필요. 사용 편의성과 법률대응 양방이 필요함):::hotspot
	
	Eg1_a1 --> Eg1_a2
	Eg1_a2 --> Eg1_a2_a1
	Eg1_a2_a1 --> Eg1_a2_a1_a1
	Eg1_a2_a1 --> Eg1_a2_a1_b1 --> Eg1_a2_a1_b2 --> Eg1_a2_a1_b3 --> Eg1_a2_a1_b4 --> Eg1_a2_a1_a1
	Hg1_a2_a1_b4_1 --> Eg1_a2_a1_b4
	Hg1_a2_a1_b4_2 --> Eg1_a2_a1_b4
	Eg1_a2_a1 --> Eg1_a2_a1_c1
	Eg1_a2_a1 --> Eg1_a2_a1_d1
	Hg1_b1 --> Eg1_b1 --> Eg1_a2 --> Eg1_a2_b1 --> Eg1_a2_b2
	A_driver --> Eg1_a2_b1
	Eg1_a2_b2 --> Eg1_a2_b2_a1
	Eg1_a2_b2 --> Eg1_a2_b2_b1
	Eg1_a2_b2 --> Eg1_a2_b2_c1
	Eg1_d1 --> Eg1_a2_b2_a1
	Eg1_d1 --> Eg1_a2_b2_b1
	Eg1_d1 --> Eg1_a2_b2_c1
	Hg1_c1 --> Eg1_c1 --> Eg1_c2 --> Eg1_c3 --> S_bizone
	Eg1_c2 --> S_bizone
	Eg1_e1 --> S_bizone
	
	Eg1_a2_a1_a1_2 --> Eg1_a2_a1_a1
	Hg1_a2_a1_a1_2 --> Eg1_a2_a1_a1_2
	Eg1_a2_a1_a1_3 --> Eg1_a2_a1_a1
	Hg1_a2_a1_a1_3 --> Eg1_a2_a1_a1_3
```


## 기사앱 - 일반 기능
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

    %% A_adm(일반 관리자):::actor
    A_driver(기사):::actor
	
	S_kg(KG 이니시스 페이팜):::system
	%% S_bizone(비즈원 Pay 시스템):::system
	%% S_firebase(Firebase):::system
	%% S_safenum(안심번호 서비스):::system
	%% S_nav(내비게이션 앱):::system

	A_driver --> Eh1
	Eh1(기사 로그인됨)
	Eh1_a1(주행내역이 조회됨)
	Eh1_a1_a1(결제 취소됨)
	Hh1_a1_a1(결제 취소 정책 필요):::hotspot
	Hh1_a1_a1 --> Eh1_a1_a1
	Eh1_a1_a1_a1(취소 영수증이 출력됨)
	Eh1_a1_a1_b1(미수금 사유가 선택됨)
	Oh1_a1_a1_b1(미수금 사유 선택 후 결제취소로 플로우 바꾸면 좋을 것 같습니다):::opportunity
	Oh1_a1_a1_b1 --> Eh1_a1_a1_b1
	Eh1_a1_a1_a1 --> Eh1_a1_a1_b1
	Eh1_a1_b1(미수금이 재결제 요청됨)
	Eh1_a1_b1_a1(거리 및 요금 정보가 수정됨)
	Eh1_a1_b1_b1(결제수단 선택됨)
	Eh1_a1_b1_a1 --> Eh1_a1_b1_b1
	Eh1_a1_b1_b2(미수금이 재결제됨) --> S_kg
	Eh1_a1_b1_b3(미수금 재결제 영수증이 출력됨)
	Eh1_b1(기사 정보 조회됨)
	Eh1_c1(분실물 등록됨)
	Eh1_d1(기본 내비게이션 설정됨)
	Eh1_e1(배정 차량이 조회됨)
	Eh1_f1(버전 정보가 확인됨)
	Eh1_g1(근무일정이 조회됨)
	Eh1_h1(공지사항이 확인됨)
	Oh1_h1(딥링크 처리 혹은 표시 기한 설정):::opportunity
	
	Eh1 --> Eh1_a1
	Eh1 --> Eh1_b1
	Eh1 --> Eh1_c1
	Eh1 --> Eh1_d1
	Eh1 --> Eh1_e1
	Eh1 --> Eh1_f1
	Eh1 --> Eh1_g1
	Eh1 --> Eh1_h1
	Oh1_h1 --> Eh1_h1
	
	Eh1_a1 --> Eh1_a1_a1 --> Eh1_a1_a1_a1
	Eh1_a1_a1 --> Eh1_a1_a1_b1
	Eh1_a1 --> Eh1_a1_b1
	Eh1_a1_b1 --> Eh1_a1_b1_a1
	Eh1_a1_b1 --> Eh1_a1_b1_b1 --> Eh1_a1_b1_b2 --> Eh1_a1_b1_b3
```

## 기사앱 - 배차 조회
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

    A_driver(기사):::actor
	
	S_firebase(Firebase):::system
	
	A_driver --> Ej1_a1(출근하기 버튼 클릭함) --> Ej1_a2(운행차량 선택됨) --> Ej1_a3(계기판 거리 입력됨) --> Ej1_a4(기사가 출근처리됨)
	Hj1_a3(한 대의 차량에 대해 복수 기사가 계기판 거리를 입력할 때 계기판 거리 이슈가 있었음):::hotspot
	Oj1_a3(계기판 정보를 기사가 수동으로 입력하는 것이 아니라 출근처리 했을 때 자동으로 반영되면 좋을 것 같습니다.):::opportunity
	HOj1_a3(OBD로 계기판 데이터 가져오는 것 문제 발생시 책임의 소재로 복잡해 질 수 있음. 담당자의 부재):::hotspot
	Hj1_a3 --> Ej1_a3
	Oj1_a3 --> Ej1_a3
	HOj1_a3 --> Oj1_a3
	
	Ej1_b1(신규 배차 내역 추가됨)
	Ej1_c1(기존 배차 내역 취소처리됨)
	Ej1_d1(기존 배차 내역 수정됨)
	
	Ej1_a4_a1(배차내역이 조회됨)
	Ej1_a4 --> Ej1_a4_a1
	Ej1_a4_b1(차량 운행 업무 일지가 조회됨)
	Ej1_a4_c1(차량이 변경이 요청됨) --> Ej1_a4_c2(현재 차량의 계기판거리가 입력됨) --> Ej1_a4_c3(차량이 변경됨) --> Ej1_a4_c4(변경된 차량에 배정된 예약건이 조회됨) --> Ej1_a4_a1
	Hj1_a4_c1(기사님이 다른 차량으로 변경될 수 있음):::hotspot --> Ej1_a4_c1
	Hj1_a4_c4(추후 논의):::hotspot --> Ej1_a4_c4
	
	Ej1_a4 --> Ej1_a4_b1
	Ej1_a4 --> Ej1_a4_c1
	
	Ej1_a4 --> S_firebase
	S_firebase --> E_firebase_a1(당일건에 대해, 신규 예약 배차 푸시 알림 수신됨)
	S_firebase --> E_firebase_b1(당일건에 대해, 예약 취소 푸시 알림 수신됨)
	S_firebase --> E_firebase_c1(당일건에 대해, 예약 변경 푸시 알림 수신됨)
	
	Ej1_a4_a1 --> Ek1_a1(배차내역이 선택됨)
	A_driver --> Ek1_a1
```

## 기사앱 - 배차 선택과 주행
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

    A_driver(기사):::actor
	
	S_safenum(안심번호 서비스):::system
	S_nav(내비게이션 앱):::system

	A_driver --> Ek1_a1(배차내역이 선택됨) --> Ek1_a2(내비게이션 실행됨) --> Ek1_a3(현재 위치부터 출발지까지의 위치가 조회됨) --> Ek1_a4(출발지로 이동됨) --> Ek1_a5(승객 대기가 시작됨) --> Ek1_a6(승객 도착이 확인됨) --> Ek1_a7(승객 승차 도움이 처리됨) --> Ek1_a8(모든 승객 탑승이 확인됨) --> Ek1_a9(주행이 시작됨) --> Ek1_a10(네비게이션 실행됨) --> Ek1_a11(목적지로 이동됨) --> Ek1_a12(도움이 시작됨) --> Ek1_a13(도움이 종료됨) --> Ek1_a14(하차 처리 완료됨) --> Ek1_a15(주행완료됨) --> Ek1_a16(주행내역 및 결제내역이 표출됨) --> Ek1_a17(기사 재량으로 선택적. 거리 및 요금정보 수정함) --> Ek1_a18(요금 결제 요청됨)
	Ek1_a2 --> S_nav
	Hk1_a2(내비게이션 실행 정책 필요):::hotspot --> Ek1_a2
	Ek1_a4_a1(승객별 결제인 경우에만 해당. 승객대기 대상 선택됨)
	Ek1_a4_b1(미예약자가 추가됨)
	Ek1_a4_c1(주행이 취소됨)
	
	Ek1_a4 --> Ek1_a4_a1 --> Ek1_a5 --> Ek1_a4_c1
	Ek1_a5 --> Ek1_a5_a1(승객에게 전화 연결이 시도됨) --> S_safenum
	Hk1_a5_a1(안심번호 할당 실패 시 정책 필요):::hotspot --> Ek1_a5_a1
	Ek1_a4 --> Ek1_a4_b1
	Ek1_a4 --> Ek1_a4_c1
	Ek1_a4 --> Ek1_a6
	
	Ek1_a6_a1(승객별 결제인 경우만 해당. 승객대기 종료 대상 선택됨)
	Ek1_a6 --> Ek1_a6_a1 --> Ek1_a7
	Hk1_a7(OBD 거리값이 오르지 않아야 함):::hotspot --> Ek1_a7
	
	Ek1_a10 --> S_nav
	H_nav(경유지가 있는 주행인 경우 별도 팝업으로 경유지 선택하여 검색할지 결정함):::hotspot --> S_nav
	Ek1_a10_1(출발지에서 도착지까지 자동입력되어 외부 어플로 화면 전환됨) --> S_nav
	
	Ek1_a10 --> Ek1_a10_a1(경유지에 도착함) --> Ek1_a10_a1_a1(도움이 시작됨) --> Ek1_a10_a1_a2(도움이 종료됨) --> Ek1_a10_a1_a3(하차인원이 선택됨) --> Ek1_a10_a1_a4(하차 처리 완료됨) --> Ek1_a10_a1_a5(승차인원이 선택됨)
	Ek1_a10_a1 --> Ek1_a10_a1_a5
	Hk1_a10_a1_a3(선택사항이며, 승객별 결제의 경우 대상을 직접 선택할 수 있다):::hotspot --> Ek1_a10_a1_a3
	Ek1_a10_a1_a4 --> Ek1_a9
	Ek1_a15 --> Ek1_a15_a1(관리자시스템의 주행내역에서 상태 변경됨)
	
	Ek1_a9 --> Ek1_a9_a1(주행이 취소됨)
	Ek1_a9_a1 --> Ek1_a9_a1_a1(주행 취소 사유로 실수로 인한 초기화가 선택됨) --> Ek1_a9_a1_a2(주행상태가 이전상태로 초기화 됨)
	Hk1_a9_a1_a2(승객별 결제의 경우 결제가 되었다면, 주행 전체를 초기화할 수 없음):::hotspot --> Ek1_a9_a1_a2
	Ek1_a9_a1 --> Ek1_a9_a1_b1(주행 취소 사유로 승객의 일방적인 취소가 선택됨) --> Ek1_a9_a1_b2(선터 전화로 유도됨. 기사가 센터로.)
```

## 기사앱 - 요금 결제
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

    A_adm(일반 관리자):::actor
    A_driver(기사):::actor
	
	S_bizone(비즈원 Pay 시스템):::system
	
	A_driver --> El1_a1(요금 결제 요청됨) --> El1_a2(음성안내로 승객에게 요금정보가 안내됨) --> El1_a3(최종 요금이 확정됨)
	El1_c1(최종 요금이 수정됨) --> El1_a3
	Hl1_a3(정산은 백엔드로부터 받음):::hotspot --> El1_a3
	Ol1_a2(재건출할 때, 이유에 코로나 멘트 삭제한 고정멘트 수정본 전달받아 적용 필요합니다. 요구사항입니다.):::opportunity --> El1_a2
	A_adm --> El1_b1(주행 강제 종료됨)
	El1_b1 --> El1_b1_a1(강제 종료 팝업 표시됨)
	El1_b1 --> El1_b1_b1(강제 종료 푸시알림 표시됨)
	
	El1_a3_a1(카드 결제 및 삼성페이로 결제됨) --> S_bizone
	El1_a3_b1(카드 결제 및 삼성페이로 결제가 실패됨)
	El1_a3_c1(미결제 됨)
	El1_a3_d1(현금으로 결제됨)
	El1_a3 --> El1_a3_a1 --> El1_a3_a2(결제 영수증이 출력됨) --> El1_a3_a3(결제 완료됨)
	Hl1_a3_a2(결제완료 및 영수증 자동출력 설정 시 영수증 자동출력됨):::hotspot --> El1_a3_a2
	El1_a3 --> El1_a3_b1 --> El1_a3_b2(재결제 요청됨) --> El1_a3_a1
	El1_a3_b2 --> El1_a3_c1
	El1_a3 --> El1_a3_c1 --> El1_a3_c2(미결제 사유가 선택됨)
	El1_a3 --> El1_a3_d1
```

## 기사앱 - 기타
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
	
	Em1_a1(퇴근이 요청됨) --> Em1_a2(계기판 거리가 입력됨) --> Em1_a3(퇴근처리됨)
	Om1_a2(구현된 기능은 없으나 가끔 퇴사하시는 분이 퇴근하기를 하지 않아 후처리가 번거롭긴 합니다. 후처리란 해당 기사로 로그인하여 퇴근하기 시도 등입니다.):::opportunity --> Em1_a2
	Hm1_a2(퇴근처리 안했을 경우의 정책 필요):::hotspot --> Em1_a2
	Em1_b1(강제 업데이트 요청됨) --> Em1_b2(강제 업데이트 됨)
	Hm1_b2_1(앱 강제 업데이트 시간이 맞지 않음. 1시간):::hotspot --> Em1_b2
	Hm1_b2_2(주행중에는 X):::hotspot --> Em1_b2
	Em1_c1(선택 업데이트 요청됨) --> Em1_c2(선택 업데이트 됨)
	Hm1_b2_2 --> Em1_c2
```

## 기사앱 - 배송
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

	S_nav(내비게이션 앱):::system
	
	En1(예약된 배송 내역이 확인됨) --> En2(내비게이션 실행됨) --> En3(현재 위치부터 출발지까지 위치가 조회됨) --> En4(출발지로 이동됨) --> En5(물품이 인수됨) --> En6(배송이 시작됨) --> En7(내비게이션 실행됨) --> En8(목적지로 이동됨) --> En9(주행 완료됨) --> En10(주행내역 및 결제내역이 표출됨) --> El1_a1(요금 결제 요청됨)
	En2 --> S_nav
	En7 --> S_nav
	Hn10(배송 요금을 누가 언제 결제할지에 대한 선택권이 없음. 선불인지 착불인지 등):::hotspot
	Hn10 --> En10
```

