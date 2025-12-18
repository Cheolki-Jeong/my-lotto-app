import streamlit as st
import random
import time

# 1. 페이지 기본 설정 (웹 브라우저 탭에 표시될 내용)
st.set_page_config(page_title="대박 기원 로또", page_icon="💰", layout="centered")

# 2. 메인 타이틀과 인사하는 라이언
st.title("🍀 정철기의 대박 로또 생성기")
st.write("당신의 행운을 위해 정철기가 응원합니다!")

# [이미지 1] 메인 화면 라이언 (현재 작동하는 주소로 교체)
# 나중에 이미지를 GitHub에 올리신다면 "lion.gif"로 이름을 바꾸시면 됩니다.
st.image("kakaofriends_01.gif", width=200)

# 3. 사이드바 - 설정창
st.sidebar.header("⚙️ 행운 설정")
count = st.sidebar.slider("몇 게임을 생성할까요?", 1, 10, 5)

lucky_input = st.sidebar.text_input("꼭 넣고 싶은 숫자 (쉼표로 구분)", "")
exclude_input = st.sidebar.text_input("제외하고 싶은 숫자 (쉼표로 구분)", "")

# 4. 번호 생성 로직 및 애니메이션
if st.button("🚀 행운의 번호 뽑기!", type="primary"):
    try:
        # 입력된 숫자 정리
        lucky_nums = [int(x.strip()) for x in lucky_input.split(',')] if lucky_input else []
        exclude_nums = [int(x.strip()) for x in exclude_input.split(',')] if exclude_input else []
        
        # 유효성 검사
        if len(lucky_nums) > 6:
            st.error("행운의 숫자는 6개 이하로 입력해주세요!")
        elif any(n < 1 or n > 45 for n in lucky_nums + exclude_nums):
            st.error("숫자는 1부터 45 사이여야 합니다.")
        else:
            # 로딩 애니메이션 (카카오프렌즈)
            with st.spinner('라이언이 번호를 신중하게 고르고 있어요...'):
                loading_bar = st.empty()
                # [이미지 2] 계산 중인 라이언
                loading_bar.image("lion_01.gif", width=150)
                time.sleep(2) # 2초 동안 긴장감 조성
                loading_bar.empty()

            st.balloons() # 축하 풍선 효과!
            st.subheader("🎉 오늘의 행운 번호입니다!")
            
            # [이미지 3] 축하하는 캐릭터
            st.image("peach_01.gif", width=180)

            all_results = []
            pool = [n for n in range(1, 46) if n not in exclude_nums and n not in lucky_nums]

            for i in range(1, count + 1):
                # 부족한 숫자만큼 랜덤 추출
                pick = random.sample(pool, 6 - len(lucky_nums))
                lotto_set = sorted(lucky_nums + pick)
                
                # 결과 출력
                res_str = f"**{i}세트:** " + "  |  ".join([f"{num}" for num in lotto_set])
                st.success(res_str)
                all_results.append(res_str)

            # 파일 저장 기능
            result_text = "\n".join(all_results).replace("**", "")
            st.download_button("📄 번호 저장하기 (TXT)", result_text, file_name="lucky_numbers.txt")

    except ValueError:
        st.error("숫자 입력 시 숫자와 쉼표(,)만 사용해 주세요!")

# 5. 하단 응원 문구
st.divider()
st.info("정철기가 당신의 1등 당첨을 진심으로 응원합니다! 대박 나세요!     잠깐!!!!   그라고, 솔직허게 이 프로그램을 이용해서 로또 1등이 당첨되얐다면, 인간적으로다가 개발자한테 1억씩만 주씨요~~~ ^^")
