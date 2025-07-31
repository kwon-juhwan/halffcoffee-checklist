# app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="퇴근 전 점검 체크리스트", layout="centered")

st.title("퇴근 전 점검 체크리스트")

# 체크리스트 불러오기
try:
    checklist = requests.get(f"{API_URL}/checklist").json()
except:
    st.error("백엔드 서버에 연결할 수 없습니다. 먼저 backend.py를 실행하세요.")
    st.stop()

st.write("아래 항목을 모두 확인 후 체크하고, 세부 내용을 입력하세요.")

submissions = []

# 모든 항목 반복 출력
for item in checklist:
    st.markdown(f"### {item['number']}. {item['title']}")
    checked = st.checkbox("확인 완료", key=f"chk_{item['id']}")
    detail = st.text_area("세부내용", value=item['description'], key=f"detail_{item['id']}")
    submissions.append({
        "item_id": item["id"],
        "checked": checked,
        "detail": detail
    })
    st.markdown("---")

# 이름 입력
user_name = st.text_input("작성자 이름")

# 제출 버튼
if st.button("제출하기"):
    if not user_name:
        st.warning("이름을 입력하세요.")
    elif not all(sub["checked"] for sub in submissions):
        st.warning("모든 항목을 체크해야 제출할 수 있습니다.")
    else:
        payload = {
            "user_name": user_name,
            "submissions": submissions
        }
        res = requests.post(f"{API_URL}/submit", json=payload)
        if res.status_code == 200:
            st.success("퇴근 전 점검 체크리스트가 저장되었습니다.")
        else:
            st.error("저장 중 오류가 발생했습니다.")
