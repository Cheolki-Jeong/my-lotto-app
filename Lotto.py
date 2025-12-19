import streamlit as st
import requests
import pandas as pd
import random
import time
import plotly.express as px
from bs4 import BeautifulSoup

# --- 페이지 설정 ---
st.set_page_config(page_title="정철기 통합 복권 분석 프로", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; border: none; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 정철기의 통합 복권 올인원 분석 대시보드")
st.write("로또 6/45와 연금복권 720+의 데이터를 실시간으로 분석하여 최적의 조합을 제안합니다.")

tab1, tab2 = st.tabs(["🍀 로또 6/45 분석", "🧧 연금복권 720+ 분석"])

# =================================================================
# [TAB 1] 로또 6/45 섹션
# =================================================================
with tab1:
    @st.cache_data(show_spinner=False)
    def get_lotto_deep_history(analyze_count=500):
        history_list, full_data = [], []
        check_round = 1200
        url_check = "https://www.dhlottery.co.kr/common.do?method=main"
        try:
            res_main = requests.get(url_check, timeout=5)
            soup_main = BeautifulSoup(res_main.text, 'html.parser')
            check_round = int(soup_main.select_one("#lottoDrwNo").text)
        except: pass

        p_bar = st.progress(0, text=f"로또 {analyze_count}회차 수집 중...")
        for i in range(analyze_count):
            target = check_round - i
            if target < 1: break
            url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={target}"
            try:
                res = requests.get(url, timeout=3).json()
                if res.get("returnValue") == "success":
                    nums = [res[f"drwtNo{j}"] for j in range(1, 7)]
                    history_list.extend(nums)
                    full_data.append({'round': target, 'numbers': set(nums), 'bonus': res['bnusNo']})
            except: pass
            p_bar.progress((i + 1) / analyze_count)
        p_bar.empty()
        return history_list, full_data, check_round

    lotto_nums, lotto_full, lotto_latest = get_lotto_deep_history(500)
    
    if lotto_nums:
        df_lotto = pd.DataFrame(lotto_nums, columns=['number'])
        lotto_counts = df_lotto['number'].value_counts().sort_index().reset_index()
        lotto_counts.columns = ['번호', '빈도']
        
        st.subheader(f"🔢 로또 최근 500회차 숫자 출현 빈도 (최신: {lotto_latest}회)")
        fig_lotto = px.bar(lotto_counts, x='번호', y='빈도', color='빈도', 
                           color_continuous_scale='Viridis', labels={'빈도':'출현 횟수'})
        st.plotly_chart(fig_lotto, use_container_width=True)
        
        st.divider()
        l_col1, l_col2 = st.columns([1, 1.2])
        with l_col1:
            st.write("🤖 **빈도 기반 예측 번호**")
            l_game_count = st.slider("생성할 게임 수", 1, 10, 5)
            if st.button("🚀 로또 예측 번호 생성!", key="lotto_btn"):
                all_nums = list(range(1, 46))
                weights = [lotto_counts[lotto_counts['번호'] == n]['빈도'].values[0] if n in lotto_counts['번호'].values else 1 for n in all_nums]
                l_preds = []
                for _ in range(l_game_count):
                    one_game = sorted(random.choices(all_nums, weights=weights, k=6))
                    while len(set(one_game)) < 6:
                        one_game = sorted(random.choices(all_nums, weights=weights, k=6))
                    l_preds.append(list(set(one_game)))
                st.session_state['l_preds'] = l_preds

        with l_col2:
            if 'l_preds' in st.session_state:
                st.write("🔍 **과거 당첨 이력 검증**")
                for idx, pred in enumerate(st.session_state['l_preds']):
                    matches = [len(set(pred) & past['numbers']) for past in lotto_full]
                    st.code(f"세트 {idx+1}: {pred}")
                    if 6 in matches: st.warning("🥇 과거 1등 당첨 이력이 있는 번호입니다!")
                    elif 5 in matches: st.info("🥈/🥉 과거 2~3등 당첨 이력이 있습니다.")
                    else: st.caption("✨ 과거 1~3등 이력이 없는 '신선한' 조합입니다.")

# =================================================================
# [TAB 2] 연금복권 720+ 섹션 (로직 보강)
# =================================================================
with tab2:
    st.subheader("🧧 연금복권 720+ 전자리수 심층 분석")

    @st.cache_data(ttl=3600)
    def get_pension_full_history(count=50):
        url_main = "https://www.dhlottery.co.kr/gameResult.do?method=win720"
        headers = {'User-Agent': 'Mozilla/5.0'}
        groups, positions = [], [[] for _ in range(6)]
        latest_round = 0
        
        try:
            res = requests.get(url_main, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            latest_text = soup.select_one(".win_result h4 strong").text
            latest_round = int(''.join(filter(str.isdigit, latest_text)))
            
            p_bar = st.progress(0, text=f"연금복권 {count}회차 수집 중...")
            for i in range(count):
                url = f"https://www.dhlottery.co.kr/gameResult.do?method=win720&drwNo={latest_round - i}"
                r = requests.get(url, headers=headers, timeout=3)
                s = BeautifulSoup(r.text, 'html.parser')
                
                # 조 추출
                g_tag = s.select_one(".win720_num .alrg")
                if g_tag:
                    g_val = ''.join(filter(str.isdigit, g_tag.text))
                    if g_val: groups.append(int(g_val))
                
                # 번호 추출
                n_tags = s.select(".win720_num .num span")
                extracted = [n.text.strip() for n in n_tags if n.text.strip().isdigit()]
                for idx, val in enumerate(extracted[:6]):
                    positions[idx].append(int(val))
                
                p_bar.progress((i + 1) / count)
                time.sleep(0.05)
            p_bar.empty()
            return groups, positions, latest_round
        except:
            return groups, positions, latest_round

    p_groups, p_positions, p_latest = get_pension_full_history(50)

    # 데이터가 충분하지 않을 때(10회분 미만)는 경고 메시지 출력
    if len(p_groups) < 10:
        st.warning("⚠️ 실시간 데이터 수집량이 부족하여 분석 기능이 제한됩니다. 생성 버튼을 누르면 랜덤 번호가 제공됩니다.")
    else:
        c_p1, c_p2 = st.columns([1, 2])
        with c_p1:
            g_df = pd.DataFrame(p_groups, columns=['조']).value_counts().reset_index(name='빈도')
            st.plotly_chart(px.pie(g_df, values='빈도', names='조', hole=.3), use_container_width=True)
        with c_p2:
            # 일 단위 빈도 차트 예시
            pos_df = pd.DataFrame(p_positions[5], columns=['숫자']).value_counts().sort_index().reset_index(name='빈도')
            st.plotly_chart(px.bar(pos_df, x='숫자', y='빈도', title="일 단위 출현 빈도"), use_container_width=True)

    st.divider()
    cp1, cp2 = st.columns([1, 1.2])
    with cp1:
        p_count = st.slider("생성할 게임 수", 1, 10, 5, key="p_slid")
        if st.button("🧧 연금복권 분석 번호 생성!", type="primary"):
            p_preds = []
            for _ in range(p_count):
                res_group = random.choice(p_groups) if p_groups else random.randint(1, 5)
                res_nums = ""
                for pos_list in p_positions:
                    # 데이터가 10개 이상 충분할 때만 빈도 기반, 아니면 완전 랜덤!
                    if len(pos_list) >= 10:
                        res_nums += str(random.choice(pos_list))
                    else:
                        res_nums += str(random.randint(0, 9))
                p_preds.append(f"{res_group}조 {res_nums}")
            st.session_state['p_preds'] = p_preds

    with cp2:
        if 'p_preds' in st.session_state:
            for p_res in st.session_state['p_preds']:
                st.success(f"추천: {p_res}")

# --- 엔딩 섹션 (문법 오류 수정됨) ---
st.divider()
st.markdown(f"""
    <div style="text-align: center; padding: 20px; background-color: #fff3f3; border-radius: 10px;">
        <h3 style="color: #d32f2f;">💡 정철기 님이 만든 프로그램으로 1등에 당첨되얐다면?</h3>
        <p style="font-size: 1.2em;">인간적으로다가 개발자한테 <b>1억씩만</b> 주씨요~~~ ^^ 😂</p>
    </div>
    """, unsafe_allow_html=True)
