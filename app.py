import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytz  # ✅ 한국 시간 변환 라이브러리

# 페이지 설정
st.set_page_config(page_title="퇴근 전 점검 체크리스트", layout="centered")

# ✅ Google Sheets 설정
SHEET_KEY = "1N_n9kU7mqpVXm1Zm4f-jRilQdlnlwxuNiUt-0llzOHY"
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

if "SERVICE_ACCOUNT" in st.secrets:
    service_account_info = dict(st.secrets["SERVICE_ACCOUNT"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
else:
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)

client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_KEY).sheet1

# ✅ 체크리스트 항목
checklist = [
    (1, "세척", "블렌더 볼(뚜껑/받침/브랜더), 파우더 뚜껑, 소스 뚜껑, 컵 등 세척, 원료 및 배수구 정리"),
    (2, "에스프레소 머신정리", "포터 필터에 소독 가루 넣고 2회 소독 후, 내부 망/ 고무 분해 / 포터 필터 분해/ 받침대 2개 모두 세척 완료 및 배수 통로에 온수 5회 부어주기 / 세척 한 도구 원위치로 설치"),
    (3, "그라인더", "호퍼 마개 닫고 안에 들어있는 가루 빼주기 -> 원두를 시그니처/디카페인 구분하여 분리 보관(밀폐 필수) 및 호퍼 세척 완료 / 전원 OFF"),
    (4, "매장 청소", "고객 테이블 / 원두가루 통 / 창고 쓰레기통 분리배출 / 테이블 및 주방 청소"),
    (5, "냉장고 냉동고 확인", "냉장도/냉동고 온도 확인 및 문단속"),
    (6, "발주", "발주 물건 거래명세서 확인 후 원위치 채워두기"),
    (7, "판넬 정리 및 출입문", "판넬/벤치 주차장 안으로 넣어두고 정문&후문 셔터 닫기/ 메인 출입문, 키오스크 유리문, 뒷문 잠금"),
    (8, "POS 마감", "키오스크 -> 포스기 순서로 마감 및 종료 / 현금 시제 확인 / 배달 매출 따로 보고"),
    (9, "전체 기기 전원OFF", "에어컨(매장/창고), 서큘레이터, 스피커, 멀티탭, 저울 3개, 오븐, 캔시머, TV, 매장 불, 간판 불 OFF")
]

# ✅ UI 표시
submissions = []
for num, title, desc in checklist:
    st.markdown(f"### {num}. {title}")
    checked = st.checkbox("확인 완료", key=f"chk_{num}")
    detail = st.text_area("세부내용", value=desc, key=f"detail_{num}")
    submissions.append((checked, detail))

# 작성자 이름
st.markdown("---")
user_name = st.text_input("작성자 이름")

# 제출 버튼 동작
if st.button("제출하기"):
    if not user_name:
        st.warning("이름을 입력하세요.")
    elif not all(sub[0] for sub in submissions):
        st.warning("모든 항목을 체크해야 제출할 수 있습니다.")
    else:
        # ✅ 한국 시간으로 저장
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
        
        sheet.append_row([user_name, now])
        st.success(f"퇴근 전 점검 체크리스트가 저장되었습니다. (저장 시간: {now})")
