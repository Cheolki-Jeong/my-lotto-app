import streamlit as st
import random

# 웹 페이지 설정
st.set_page_config(page_title="행운의 로또 생성기", page_icon="🍀")

st.title("🍀 나만의 행운 로또 생성기")
st.write("바이브 코딩으로 만든 나만의 맞춤형 로또 앱입니다.")

# 사이드바 설정 (입력칸)
st.sidebar.header("설정")
count = st.sidebar.number_input("몇 게임을 만들까요?", min_value=1, max_value=10, value=5)

lucky_str = st.sidebar.text_input("꼭 넣고 싶은 숫자 (쉼표로 구분)", "")
exclude_str = st.sidebar.text_input("빼고 싶은 숫자 (쉼표로 구분)", "")

if st.button("번호 생성하기! ✨"):
    # 입력값 정리
    lucky_nums = [int(x.strip()) for x in lucky_str.split(',')] if lucky_str else []
    exclude_nums = [int(x.strip()) for x in exclude_str.split(',')] if exclude_str else []
    
    pool = [n for n in range(1, 46) if n not in exclude_nums]
    
    st.subheader("🎉 생성 결과")
    
    results = []
    for i in range(1, count + 1):
        temp_pool = [n for n in pool if n not in lucky_nums]
        pick = random.sample(temp_pool, 6 - len(lucky_nums))
        lotto_set = sorted(lucky_nums + pick)
        
        # 화면 출력
        st.success(f"**{i}세트:** {', '.join(map(str, lotto_set))}")
        results.append(f"{i}세트: {lotto_set}")

    # 파일 다운로드 버튼 (스마트폰에 저장)
    result_text = "\n".join(results)
    st.download_button("결과를 텍스트 파일로 저장", result_text, file_name="lotto.txt")

st.info("행운이 함께하시길 바랍니다! ^^")
