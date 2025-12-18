import streamlit as st
import random
import time # 시간을 잠시 멈추는 효과를 위해 추가

# --- 페이지 설정 ---
st.set_page_config(page_title="대박 기원 로또", page_icon="💰")

# --- 제목 및 메인 이미지 ---
st.title("🍀 라이언이 뽑아주는 대박 로또!")
st.write("오늘은 어떤 번호가 나올까요? 행운을 빕니다!")

# 1. 메인 화면에서 반겨주는 움직이는 이미지 (인사하는 라이언 GIF 예시)
# (주의: 인터넷 주소이므로 링크가 만료되면 이미지가 안 보일 수 있습니다.)
st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMThwNHB5ZmN5aWx2Z3A0aW14YmY0aW14YmY0aW14YmY0aW14eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/L0NjK3WNbz0I7w8I8X/giphy.gif", width=200)


# --- 사이드바 설정 ---
st.sidebar.header("⚙️ 설정")
st.sidebar.write("원하는 조건을 설정해주세요.")
count = st.sidebar.slider("몇 게임을 만들까요?", 1, 20, 5) # 슬라이더로 변경해서 더 편하게!

lucky_str = st.sidebar.text_input("꼭 넣을 숫자 (쉼표 구분)", "", placeholder="예: 7, 15")
exclude_str = st.sidebar.text_input("뺄 숫자 (쉼표 구분)", "", placeholder="예: 1, 2")

# --- 메인 로직 ---
if st.button("🚀 번호 생성 시작!", type="primary"): # 버튼 강조
    
    # 2. 계산하는 동안 보여줄 로딩 애니메이션 (계산하는 춘식이 GIF 예시)
    with st.spinner('춘식이가 열심히 번호를 고르는 중... 잠시만요!'):
        loading_placeholder = st.empty() # 이미지가 들어갈 빈 공간 마련
        loading_placeholder.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzN0cDV4aW14YmY0aW14YmY0aW14YmY0aW14YmY0aW14eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/MeMg0i391gC6N0sK2e/giphy.gif", width=150)
        time.sleep(2.5) # 2.5초 동안 뜸 들이기 (재미를 위해)
        loading_placeholder.empty() # 로딩 이미지 지우기

    # 입력값 정리
    try:
        lucky_nums = [int(x.strip()) for x in lucky_str.split(',')] if lucky_str else []
        exclude_nums = [int(x.strip()) for x in exclude_str.split(',')] if exclude_str else []
        
        pool = [n for n in range(1, 46) if n not in exclude_nums]
        
        st.divider() # 구분선
        st.subheader("🎉 짜잔! 오늘의 행운 번호입니다")
        
        # 3. 결과와 함께 보여줄 축하 이미지 (춤추는 캐릭터 GIF 예시)
        st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExazJ3aW14YmY0aW14YmY0aW14YmY0aW14YmY0aW14YmY0aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/TDDwL0gTjj4pZgYf1T/giphy.gif", width=200)
        
        results = []
        for i in range(1, count + 1):
            temp_pool = [n for n in pool if n not in lucky_nums]
            
            # 예외 처리: 행운의 숫자가 너무 많거나 제외 숫자가 너무 많을 때
            if len(lucky_nums) > 6 or len(temp_pool) < (6 - len(lucky_nums)):
                 st.error("설정한 숫자가 너무 많아서 6개를 뽑을 수가 없어요! 설정을 확인해주세요.")
                 results = []
                 break

            pick = random.sample(temp_pool, 6 - len(lucky_nums))
            lotto_set = sorted(lucky_nums + pick)
            
            # 번호를 예쁜 상자 안에 보여주기
            st.success(f"**{i}게임:** {'  |  '.join(map(str, lotto_set))}")
            results.append(f"{i}게임: {lotto_set}")

        if results:
            # 파일 다운로드 버튼
            result_text = "\n".join(results)
            st.download_button("📄 결과 텍스트 파일로 저장", result_text, file_name="lucky_lotto.txt")
            st.balloons() # 성공 시 풍선 날리기 효과!

    except ValueError:
        st.error("숫자 입력칸에는 숫자와 쉼표(,)만 입력해주세요!")

# --- 하단 안내 ---
st.divider()
st.caption("행운이 함께하시길 바랍니다이! 그라고, 솔직허게 이 프로그램을 이용해서 로또 1등이 당첨되얐다면, 인간적으로다가 개발자한테 1억씩만 주씨요~~~ ^^ ^^")
