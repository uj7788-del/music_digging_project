"""
나만의 흑인음악 취향 디깅(Digging) 대시보드 v2.1
My Black Music Taste Digging Dashboard — Light Theme Edition

실행 방법: streamlit run music_digging.py
의존성: pip install streamlit plotly pandas
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# 1. 페이지 기본 설정
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="흑인음악 디깅 대시보드",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# 2. 전역 CSS — 밝은 테마 (Light Theme)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700;900&display=swap');

  /* ── 전체 배경 ── */
  .stApp { background-color: #f5f4f0; font-family: 'Noto Sans KR', sans-serif; }
  .block-container { padding-top: 1.6rem; padding-bottom: 2rem; }

  /* ── 사이드바 ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f0eeff 100%);
    border-right: 1px solid #e4dff7;
  }
  [data-testid="stSidebar"] * { color: #3b2f6e !important; }
  [data-testid="stSidebar"] .stSelectbox label { color: #6d4fc2 !important; font-weight: 600; }

  /* ── 타이틀 배너 ── */
  .title-banner {
    background: linear-gradient(135deg, #ede9fe 0%, #dbeafe 60%, #d1fae5 100%);
    border-radius: 20px;
    padding: 28px 36px;
    border: 1px solid #c4b5fd;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
  }
  .title-banner::before {
    content: '';
    position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(139,92,246,0.06) 0%, transparent 60%),
                radial-gradient(circle at 70% 50%, rgba(59,130,246,0.05) 0%, transparent 60%);
  }
  .title-main {
    font-size: 2rem; font-weight: 900;
    background: linear-gradient(90deg, #7c3aed, #2563eb, #059669);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.2; margin-bottom: 8px;
  }
  .title-sub { font-size: 0.9rem; color: #6b7280; line-height: 1.6; }

  /* ── 단계 뱃지 ── */
  .step-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, #ede9fe, #dbeafe);
    border: 1px solid #a5b4fc;
    border-radius: 50px; padding: 6px 16px;
    font-size: 0.8rem; font-weight: 700; color: #4338ca;
    margin-bottom: 16px;
  }
  .step-dot { width: 8px; height: 8px; border-radius: 50%; background: #7c3aed; }

  /* ── 곡 카드 ── */
  .track-card {
    background: #ffffff;
    border: 1.5px solid #e0d9f7;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    position: relative;
    box-shadow: 0 2px 12px rgba(109,79,194,0.07);
  }
  .track-number {
    position: absolute; top: 16px; right: 20px;
    font-size: 2.5rem; font-weight: 900; color: rgba(124,58,237,0.08);
    line-height: 1;
  }
  .track-title { font-size: 1.15rem; font-weight: 700; color: #1e1b4b; margin-bottom: 4px; }
  .track-artist { font-size: 0.85rem; color: #6d4fc2; margin-bottom: 12px; font-weight: 600; }
  .track-desc {
    font-size: 0.8rem; color: #6b7280; line-height: 1.6;
    border-left: 3px solid #c4b5fd; padding-left: 10px; margin-bottom: 14px;
  }
  .yt-link {
    display: inline-flex; align-items: center; gap: 6px;
    background: #fff1f2; border: 1px solid #fecdd3;
    border-radius: 8px; padding: 7px 16px;
    font-size: 0.82rem; color: #e11d48; text-decoration: none; font-weight: 700;
    transition: background 0.15s;
  }
  .yt-link:hover { background: #ffe4e6; }

  /* ── 트랙 진행 표시기 ── */
  .track-progress-wrap {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 20px;
  }
  .track-pip {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 800;
    border: 2px solid;
    transition: all 0.2s ease;
  }
  .pip-done   { background: #d1fae5; border-color: #059669; color: #065f46; }
  .pip-active { background: #ede9fe; border-color: #7c3aed; color: #5b21b6; }
  .pip-locked { background: #f3f4f6; border-color: #d1d5db; color: #9ca3af; }
  .track-pip-line { flex: 1; height: 2px; background: #e5e7eb; border-radius: 2px; }
  .track-pip-line-done { background: #a7f3d0; }

  /* ── 평가 섹션 ── */
  .eval-label {
    font-size: 0.78rem; font-weight: 700; color: #7c3aed;
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 6px; margin-top: 14px;
  }

  /* ── 진행 표시 바 (사이드바) ── */
  .progress-wrap { margin: 12px 0 20px 0; }
  .progress-track { background: #ede9fe; border-radius: 999px; height: 8px; overflow: hidden; }
  .progress-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #7c3aed, #3b82f6);
    transition: width 0.4s ease;
  }
  .progress-label { font-size: 0.75rem; color: #9ca3af; margin-top: 4px; }

  /* ── 추천 카드 ── */
  .rec-card {
    background: #ffffff;
    border: 1.5px solid #e0e7ff;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 1px 6px rgba(67,56,202,0.06);
  }
  .rec-card-matched {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    border: 1.5px solid #6ee7b7;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    position: relative;
    box-shadow: 0 2px 10px rgba(5,150,105,0.1);
  }
  .rec-match-badge {
    position: absolute; top: 14px; right: 14px;
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    border: 1px solid #34d399;
    border-radius: 999px; padding: 2px 10px;
    font-size: 0.7rem; color: #065f46; font-weight: 800;
  }
  .rec-rank { font-size: 1.4rem; font-weight: 900; color: rgba(99,102,241,0.2); float: right; line-height: 1; }
  .rec-title { font-size: 1rem; font-weight: 700; color: #1e1b4b; margin-bottom: 3px; }
  .rec-artist { font-size: 0.82rem; color: #6b7280; margin-bottom: 8px; }
  .rec-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
  .rec-tag {
    background: #f1f5f9; border: 1px solid #e2e8f0;
    border-radius: 999px; padding: 3px 10px;
    font-size: 0.72rem; color: #64748b;
  }
  .rec-tag-highlight {
    background: #ede9fe; border: 1px solid #c4b5fd;
    border-radius: 999px; padding: 3px 10px;
    font-size: 0.72rem; color: #5b21b6; font-weight: 600;
  }

  /* ── 믹스테이프 리포트 ── */
  .mixtape-box {
    background: #fafaf9;
    border: 1.5px solid #e5e7eb;
    border-radius: 16px;
    padding: 24px 28px;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: #4b5563;
    line-height: 1.9;
    white-space: pre-wrap;
  }

  /* ── 분석 결과 헤더 ── */
  .result-header {
    background: linear-gradient(135deg, #ede9fe 0%, #dbeafe 100%);
    border: 1.5px solid #c4b5fd;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
  }
  .result-title { font-size: 1.2rem; font-weight: 800; color: #4338ca; margin-bottom: 6px; }
  .result-persona { font-size: 0.9rem; color: #6d28d9; line-height: 1.6; }

  /* ── 섹션 구분선 ── */
  .section-divider { border: none; border-top: 1.5px solid #e9e4f7; margin: 28px 0; }

  /* ── 버튼 커스텀 ── */
  .stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(124,58,237,0.25) !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca) !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.35) !important;
    transform: translateY(-1px) !important;
  }

  /* ── 별점 안내 ── */
  .star-guide { font-size: 0.82rem; color: #d97706; margin-top: 3px; font-weight: 600; }

  /* ── 완료 배너 ── */
  .complete-banner {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    border: 1.5px solid #6ee7b7;
    border-radius: 14px; padding: 14px 20px;
    font-size: 0.88rem; color: #065f46;
    font-weight: 700; margin-bottom: 16px;
  }

  /* ── 전체 평가완료 배너 ── */
  .all-done-banner {
    background: linear-gradient(135deg, #ede9fe, #dbeafe);
    border: 1.5px solid #a5b4fc;
    border-radius: 14px; padding: 16px 22px;
    font-size: 0.9rem; color: #3730a3;
    font-weight: 700; margin-bottom: 16px;
    display: flex; align-items: center; gap: 10px;
  }

  /* ── 탭 스타일 ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #f3f0ff; border-radius: 10px; padding: 4px; gap: 4px;
    border: 1px solid #e0d9f7;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent; color: #9ca3af;
    border-radius: 8px; font-weight: 600; font-size: 0.88rem;
  }
  .stTabs [aria-selected="true"] {
    background: #ffffff !important; color: #6d28d9 !important;
    box-shadow: 0 1px 4px rgba(109,79,194,0.15) !important;
  }

  /* ── 속성 바 ── */
  .attr-bar-bg { background: #f1f5f9; border-radius: 999px; height: 8px; overflow: hidden; }

  /* ── 사이드바 정보 박스 ── */
  .sidebar-info {
    background: #f5f3ff; border-radius: 10px; padding: 14px;
    margin-top: 10px; border: 1px solid #ddd6fe;
    font-size: 0.75rem; color: #6d4fc2; line-height: 1.7;
  }

  /* ── 타임라인 ── */
  .timeline-wrap {
    position: relative;
    padding: 10px 0 10px 0;
    margin: 0 0 8px 0;
  }
  .timeline-wrap::before {
    content: '';
    position: absolute; left: 26px; top: 0; bottom: 0;
    width: 2px;
    background: linear-gradient(180deg, #7c3aed 0%, #3b82f6 60%, transparent 100%);
  }
  .timeline-item {
    display: flex; align-items: flex-start; gap: 18px;
    margin-bottom: 28px; position: relative;
  }
  .timeline-node {
    flex-shrink: 0; width: 52px; height: 52px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem; font-weight: 900; line-height: 1.1;
    text-align: center; position: relative; z-index: 1; border: 2px solid;
    letter-spacing: -0.03em;
  }
  .timeline-content {
    flex: 1; background: #ffffff; border-radius: 14px;
    padding: 14px 18px; border: 1.5px solid #e5e7eb;
    margin-top: 4px; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  }
  .timeline-year {
    font-size: 0.72rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px;
  }
  .timeline-title { font-size: 0.95rem; font-weight: 700; color: #1e1b4b; margin-bottom: 5px; }
  .timeline-desc { font-size: 0.78rem; color: #6b7280; line-height: 1.6; }
  .timeline-artists { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px; }
  .timeline-artist-tag {
    background: #ede9fe; border: 1px solid #c4b5fd;
    border-radius: 999px; padding: 2px 10px;
    font-size: 0.7rem; color: #5b21b6; font-weight: 600;
  }
  .timeline-header {
    background: linear-gradient(135deg, #faf5ff 0%, #eff6ff 100%);
    border: 1.5px solid #ddd6fe;
    border-radius: 16px; padding: 18px 22px; margin-bottom: 22px;
    box-shadow: 0 1px 6px rgba(109,79,194,0.06);
  }
  .timeline-header-title { font-size: 1.05rem; font-weight: 800; color: #4338ca; margin-bottom: 5px; }
  .timeline-header-sub { font-size: 0.8rem; color: #9ca3af; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 3. 하드코딩 데이터셋
#    yt_query: "아티스트명 - 곡제목" 정확히 일치 (유튜브 검색 직결)
# ══════════════════════════════════════════════════════════════

GENRE_DATA = {

    # ────────────────────────
    # 1. Neo-Soul
    # ────────────────────────
    "🌙 Neo-Soul": {
        "desc": "70~80년대 소울의 감성을 현대적 R&B 프로덕션으로 재해석. 따뜻한 멜로디, 깊은 보컬, 아날로그 질감.",
        "color": "#7c3aed",
        "tracks": [
            {
                "title": "On & On",
                "artist": "Erykah Badu",
                "year": 1997,
                "desc": "네오소울의 시작점. 아날로그 드럼, Badu의 독특한 보컬 톤, 재즈적 코드 진행이 장르를 정의한 곡.",
                "yt_query": "Erykah Badu - On & On",
                "vibe": ["멜로디", "보컬", "그루브"],
            },
            {
                "title": "Untitled (How Does It Feel)",
                "artist": "D'Angelo",
                "year": 2000,
                "desc": "빈티지 펑크와 소울의 완벽한 결합. 레이어드된 보컬 하모니와 끈적한 그루브가 압도적.",
                "yt_query": "D'Angelo - Untitled (How Does It Feel)",
                "vibe": ["그루브", "보컬", "리듬"],
            },
            {
                "title": "Ex-Factor",
                "artist": "Lauryn Hill",
                "year": 1998,
                "desc": "The Miseducation 시대의 정수. 어쿠스틱 기타와 깊은 가사, 감정적 보컬 전달력이 핵심.",
                "yt_query": "Lauryn Hill - Ex-Factor",
                "vibe": ["가사", "멜로디", "보컬"],
            },
        ],
        "recommendations": [
            {"title": "Bag Lady", "artist": "Erykah Badu", "year": 2000,
             "tags": ["위로", "소울", "재즈"], "match_attributes": ["멜로디", "보컬"]},
            {"title": "Brown Sugar", "artist": "D'Angelo", "year": 1995,
             "tags": ["감성", "빈티지", "로맨틱"], "match_attributes": ["그루브", "보컬"]},
            {"title": "Be Here", "artist": "Raphael Saadiq", "year": 2004,
             "tags": ["따뜻함", "멜로디", "어덜트소울"], "match_attributes": ["멜로디", "리듬"]},
            {"title": "New Amerykah Pt.1", "artist": "Erykah Badu", "year": 2008,
             "tags": ["실험적", "의식적", "사이키델릭"], "match_attributes": ["가사", "보컬"]},
            {"title": "Voodoo (Album)", "artist": "D'Angelo", "year": 2000,
             "tags": ["그루브", "레이어드", "완성도"], "match_attributes": ["그루브", "리듬"]},
        ],
        "timeline": [
            {"year": "1972", "era": "Proto",
             "title": "Al Green의 황금기",
             "desc": "소울의 감성과 펑크 사운드가 처음 교차. Al Green의 'Let's Stay Together'가 이후 네오소울 보컬 감성의 원형을 확립.",
             "artists": ["Al Green", "Stevie Wonder", "Marvin Gaye"]},
            {"year": "1988", "era": "Transition",
             "title": "Tony! Toni! Toné!의 등장",
             "desc": "클래식 소울을 현대적으로 재해석하는 흐름이 시작. 라이브 악기와 현대 프로덕션의 혼합이 네오소울의 전조가 됨.",
             "artists": ["Tony! Toni! Toné!", "Anita Baker"]},
            {"year": "1994", "era": "Birth",
             "title": "장르의 탄생 — Kedar Massenburg의 명명",
             "desc": "Motown 프로듀서 Kedar Massenburg가 'Neo-Soul'이라는 장르명을 처음 사용. D'Angelo의 데뷔앨범 'Brown Sugar'로 장르가 공식화.",
             "artists": ["D'Angelo", "Me'Shell NdegéOcello"]},
            {"year": "1997~1999", "era": "Golden Age",
             "title": "황금기 — Soulquarians의 시대",
             "desc": "Erykah Badu, Lauryn Hill, Common, Mos Def, Q-Tip 등이 모인 집단 Soulquarians가 네오소울의 철학적·음악적 기준을 완성.",
             "artists": ["Erykah Badu", "Lauryn Hill", "Common", "Mos Def"]},
            {"year": "2000", "era": "Peak",
             "title": "D'Angelo 'Voodoo' — 장르의 정점",
             "desc": "Voodoo 앨범은 네오소울의 역사상 최고작으로 평가받음. J Dilla, Questlove와의 협업으로 리듬 언어 자체를 혁신.",
             "artists": ["D'Angelo", "J Dilla", "Questlove"]},
            {"year": "2014~현재", "era": "Revival",
             "title": "네오소울의 르네상스",
             "desc": "D'Angelo 'Black Messiah' 귀환, Anderson .Paak, Noname, Syd 등이 장르를 재점화. Frank Ocean의 'Channel Orange'는 현대 네오소울의 기준점.",
             "artists": ["Anderson .Paak", "Frank Ocean", "Noname", "Syd"]},
        ],
    },

    # ────────────────────────
    # 2. Funk
    # ────────────────────────
    "🔥 Funk": {
        "desc": "James Brown에서 시작된 그루브 중심 사운드. 강렬한 베이스라인, 촘촘한 리듬 섹션, 반복적 훅이 특징.",
        "color": "#ea580c",
        "tracks": [
            {
                "title": "Super Freak",
                "artist": "Rick James",
                "year": 1981,
                "desc": "강렬한 신스 리프와 Rick James의 에너지가 폭발하는 클래식 펑크. MC Hammer 샘플로도 유명.",
                "yt_query": "Rick James - Super Freak",
                "vibe": ["그루브", "리듬", "보컬"],
            },
            {
                "title": "Flash Light",
                "artist": "Parliament",
                "year": 1977,
                "desc": "George Clinton의 P-Funk 우주관. 무겁고 끈적한 신스 베이스와 집단 보컬이 만드는 황홀경.",
                "yt_query": "Parliament - Flash Light",
                "vibe": ["그루브", "리듬", "멜로디"],
            },
            {
                "title": "Give Up the Funk (Tear the Roof off the Sucker)",
                "artist": "Parliament",
                "year": 1975,
                "desc": "펑크의 교과서. 반복적 리프, 콜앤리스폰스 보컬, 인펙셔스한 그루브가 완벽하게 맞물린 곡.",
                "yt_query": "Parliament - Give Up the Funk (Tear the Roof off the Sucker)",
                "vibe": ["리듬", "그루브", "가사"],
            },
        ],
        "recommendations": [
            {"title": "I Got You (I Feel Good)", "artist": "James Brown", "year": 1965,
             "tags": ["에너지", "파워", "클래식"], "match_attributes": ["리듬", "그루브"]},
            {"title": "Jungle Boogie", "artist": "Kool & The Gang", "year": 1973,
             "tags": ["펑키", "브라스", "댄서블"], "match_attributes": ["그루브", "리듬"]},
            {"title": "That Lady", "artist": "The Isley Brothers", "year": 1973,
             "tags": ["기타", "그루브", "소울펑크"], "match_attributes": ["그루브", "멜로디"]},
            {"title": "Shining Star", "artist": "Earth, Wind & Fire", "year": 1975,
             "tags": ["업리프팅", "브라스", "완성도"], "match_attributes": ["멜로디", "리듬"]},
            {"title": "Le Freak", "artist": "Chic", "year": 1978,
             "tags": ["디스코펑크", "리프", "댄스플로어"], "match_attributes": ["리듬", "그루브"]},
        ],
        "timeline": [
            {"year": "1960s", "era": "Origin",
             "title": "James Brown — 펑크의 아버지",
             "desc": "'Papa's Got a Brand New Bag'(1965)으로 비트의 1박 강조, 싱코페이션 리듬이 탄생. 모든 펑크 음악의 DNA가 여기서 시작.",
             "artists": ["James Brown", "The Famous Flames"]},
            {"year": "1967~1969", "era": "Development",
             "title": "Sly & The Family Stone의 혁신",
             "desc": "흑인과 백인, 남성과 여성이 함께한 밴드. 사이키델릭 록과 펑크의 결합으로 장르 경계를 무너뜨림.",
             "artists": ["Sly Stone", "Larry Graham"]},
            {"year": "1972~1975", "era": "P-Funk Era",
             "title": "George Clinton의 P-Funk 우주",
             "desc": "Parliament-Funkadelic 듀얼 밴드 운영. '마더십(Mothership Connection)' 컨셉으로 펑크를 문화·철학적 운동으로 확장.",
             "artists": ["George Clinton", "Bootsy Collins", "Bernie Worrell"]},
            {"year": "1976~1979", "era": "Disco Fusion",
             "title": "디스코와의 만남 — Earth, Wind & Fire",
             "desc": "펑크가 디스코의 화려함과 결합. EWF, Chic, Kool & The Gang이 댄스플로어를 지배하며 대중화에 성공.",
             "artists": ["Earth, Wind & Fire", "Chic", "Nile Rodgers"]},
            {"year": "1980s", "era": "Electro-Funk",
             "title": "신시사이저와의 결합 — Electro-Funk",
             "desc": "Prince, Rick James가 신스와 드럼머신을 흡수. 미니멀하고 섹슈얼한 펑크 사운드로 진화.",
             "artists": ["Prince", "Rick James", "Zapp"]},
            {"year": "1990s~현재", "era": "Legacy",
             "title": "힙합 샘플의 바이블",
             "desc": "NWA, De La Soul, Public Enemy 등 힙합이 펑크 비트를 샘플링하며 명맥 유지. Kendrick Lamar의 'To Pimp a Butterfly'로 현대에 부활.",
             "artists": ["Kendrick Lamar", "Bruno Mars", "Anderson .Paak"]},
        ],
    },

    # ────────────────────────
    # 3. Contemporary R&B
    # ────────────────────────
    "💜 Contemporary R&B": {
        "desc": "2000년대 이후 팝·힙합이 융합된 현대 R&B. 세련된 프로덕션, 오토튠 활용, 감성적 가사가 트레이드마크.",
        "color": "#db2777",
        "tracks": [
            {
                "title": "Climax",
                "artist": "Usher",
                "year": 2012,
                "desc": "컨템포러리 R&B와 일렉트로닉의 경계를 허문 Diplo 프로덕션. Usher의 팔세토가 절정.",
                "yt_query": "Usher - Climax",
                "vibe": ["멜로디", "보컬", "그루브"],
            },
            {
                "title": "Die For You",
                "artist": "The Weeknd",
                "year": 2016,
                "desc": "80s 신스팝 미학 위에 얹힌 The Weeknd의 감성적 가사. 현대 R&B의 교과서적 트랙.",
                "yt_query": "The Weeknd - Die For You",
                "vibe": ["멜로디", "가사", "보컬"],
            },
            {
                "title": "Location",
                "artist": "Khalid",
                "year": 2016,
                "desc": "청춘의 감성을 담은 lo-fi R&B. 편안한 프로덕션과 Khalid의 허스키 보컬이 완벽한 조화.",
                "yt_query": "Khalid - Location",
                "vibe": ["가사", "멜로디", "보컬"],
            },
        ],
        "recommendations": [
            {"title": "Best Part", "artist": "Daniel Caesar ft. H.E.R.", "year": 2017,
             "tags": ["로맨틱", "어쿠스틱R&B", "듀엣"], "match_attributes": ["멜로디", "보컬"]},
            {"title": "Superstar", "artist": "Usher", "year": 2004,
             "tags": ["클래식R&B", "스무드", "감성"], "match_attributes": ["보컬", "그루브"]},
            {"title": "Come Through", "artist": "H.E.R.", "year": 2017,
             "tags": ["기타R&B", "쿨", "세련됨"], "match_attributes": ["멜로디", "가사"]},
            {"title": "Earned It", "artist": "The Weeknd", "year": 2015,
             "tags": ["오케스트라", "극적", "감성"], "match_attributes": ["멜로디", "보컬"]},
            {"title": "Nobody", "artist": "Khalid & Alina Barraza", "year": 2018,
             "tags": ["팝R&B", "발라드", "청춘"], "match_attributes": ["가사", "멜로디"]},
        ],
        "timeline": [
            {"year": "1994~1997", "era": "New School",
             "title": "TLC·Aaliyah — 미래형 R&B의 선구자",
             "desc": "Timbaland·Missy Elliott 프로덕션팀이 드럼패턴과 R&B 보컬을 혁신적으로 결합. Aaliyah 'One in a Million'이 컨템포러리 R&B의 문을 열었다.",
             "artists": ["Aaliyah", "TLC", "Timbaland"]},
            {"year": "2001~2004", "era": "Golden Era",
             "title": "Usher·Beyoncé — 팝R&B 전성기",
             "desc": "Usher 'Confessions', Beyoncé 'Dangerously in Love'로 R&B가 팝 메인스트림을 완전 장악.",
             "artists": ["Usher", "Beyoncé", "Alicia Keys"]},
            {"year": "2008~2011", "era": "Experimental",
             "title": "The Weeknd·Frank Ocean — 얼터너티브 R&B",
             "desc": "인디·얼터너티브 정서가 R&B에 유입. 어둡고 내성적인 가사, lo-fi 텍스처가 새로운 미학을 창조.",
             "artists": ["The Weeknd", "Frank Ocean", "Miguel"]},
            {"year": "2016~2019", "era": "Streaming Age",
             "title": "스트리밍 시대의 R&B — 장르 해방",
             "desc": "SZA 'Ctrl', Daniel Caesar 'Freudian', Khalid 'American Teen'이 장르 경계를 완전히 해체.",
             "artists": ["SZA", "Daniel Caesar", "Khalid", "H.E.R."]},
            {"year": "2020~현재", "era": "Post-Genre",
             "title": "포스트 장르 시대",
             "desc": "Brent Faiyaz, Giveon, Bryson Tiller 등 '장르 이름 없는' 아티스트들이 주류로.",
             "artists": ["Brent Faiyaz", "Giveon", "Summer Walker"]},
        ],
    },

    # ────────────────────────
    # 4. New Jack Swing
    # ────────────────────────
    "🎤 New Jack Swing": {
        "desc": "80년대 후반~90년대 초 Teddy Riley가 창시한 장르. 힙합 비트 + 소울 보컬의 완벽한 합성.",
        "color": "#0891b2",
        "tracks": [
            {
                "title": "My Prerogative",
                "artist": "Bobby Brown",
                "year": 1988,
                "desc": "뉴잭스윙의 탄생을 알린 선언적 트랙. Teddy Riley 프로덕션, 힙합 비트 위의 소울 보컬 공식 완성.",
                "yt_query": "Bobby Brown - My Prerogative",
                "vibe": ["리듬", "보컬", "그루브"],
            },
            {
                "title": "Rump Shaker",
                "artist": "Wreckx-N-Effect",
                "year": 1992,
                "desc": "극도로 댄서블한 뉴잭스윙. 반복되는 비트 패턴과 중독성 있는 훅이 장르 정수를 보여줌.",
                "yt_query": "Wreckx-N-Effect - Rump Shaker",
                "vibe": ["리듬", "그루브", "멜로디"],
            },
            {
                "title": "Creep",
                "artist": "TLC",
                "year": 1994,
                "desc": "여성 그룹의 관점에서 완성한 뉴잭스윙. 쿨하고 절제된 보컬과 촘촘한 비트의 균형.",
                "yt_query": "TLC - Creep",
                "vibe": ["리듬", "보컬", "가사"],
            },
        ],
        "recommendations": [
            {"title": "Poison", "artist": "Bell Biv DeVoe", "year": 1990,
             "tags": ["에너지", "엣지", "뉴잭"], "match_attributes": ["리듬", "그루브"]},
            {"title": "I Want Her", "artist": "Keith Sweat", "year": 1987,
             "tags": ["스무드", "로맨틱", "뉴잭"], "match_attributes": ["보컬", "그루브"]},
            {"title": "Remember the Time", "artist": "Michael Jackson", "year": 1992,
             "tags": ["팝뉴잭", "클래식", "완성도"], "match_attributes": ["그루브", "멜로디"]},
            {"title": "No Scrubs", "artist": "TLC", "year": 1999,
             "tags": ["걸파워", "팝R&B", "아이코닉"], "match_attributes": ["가사", "보컬"]},
            {"title": "Motownphilly", "artist": "Boyz II Men", "year": 1991,
             "tags": ["아카펠라", "하모니", "소울"], "match_attributes": ["보컬", "멜로디"]},
        ],
        "timeline": [
            {"year": "1987", "era": "Origin",
             "title": "Teddy Riley — 장르의 창시자",
             "desc": "Guy 밴드의 데뷔와 함께 드럼 머신 비트 + R&B 멜로디 공식을 처음 확립.",
             "artists": ["Teddy Riley", "Guy"]},
            {"year": "1988~1989", "era": "Breakout",
             "title": "Bobby Brown·Keith Sweat — 상업적 폭발",
             "desc": "Bobby Brown 'My Prerogative', Keith Sweat 'Make It Last Forever'가 차트를 점령.",
             "artists": ["Bobby Brown", "Keith Sweat"]},
            {"year": "1991~1992", "era": "Peak",
             "title": "Michael Jackson의 합류 — 메인스트림 정복",
             "desc": "MJ 'Dangerous' 앨범이 뉴잭스윙을 팝 최정상으로 끌어올림.",
             "artists": ["Michael Jackson", "Boyz II Men", "Jodeci"]},
            {"year": "1992~1995", "era": "Evolution",
             "title": "TLC·SWV — 여성 아티스트의 재해석",
             "desc": "TLC가 여성적 관점과 힙합 감성으로 뉴잭스윙을 재정의.",
             "artists": ["TLC", "SWV", "En Vogue"]},
            {"year": "1996~2000", "era": "Decline & Legacy",
             "title": "Timbaland 시대로의 이행",
             "desc": "Timbaland·Missy Elliott가 더 복잡한 비트 구조로 진화시키며 컨템포러리 R&B의 기반이 됨.",
             "artists": ["Timbaland", "Missy Elliott", "Ginuwine"]},
        ],
    },

    # ────────────────────────
    # 5. Quiet Storm R&B
    # ────────────────────────
    "🌊 Quiet Storm R&B": {
        "desc": "70~80년대 라디오 포맷에서 탄생한 어덜트 R&B. 느린 템포, 풍부한 오케스트레이션, 성숙한 가사.",
        "color": "#059669",
        "tracks": [
            {
                "title": "Always and Forever",
                "artist": "Heatwave",
                "year": 1977,
                "desc": "Quiet Storm의 정의. 천천히 흐르는 멜로디, 부드러운 현악, 성숙한 러브송의 교과서.",
                "yt_query": "Heatwave - Always and Forever",
                "vibe": ["멜로디", "보컬", "가사"],
            },
            {
                "title": "Between the Sheets",
                "artist": "The Isley Brothers",
                "year": 1983,
                "desc": "Ron Isley의 실크 같은 보컬. 느린 그루브와 깊은 감성이 Quiet Storm의 진수를 보여줌.",
                "yt_query": "The Isley Brothers - Between the Sheets",
                "vibe": ["보컬", "그루브", "멜로디"],
            },
            {
                "title": "At Your Best (You Are Love)",
                "artist": "Aaliyah",
                "year": 1994,
                "desc": "Isley Brothers 원곡을 Aaliyah가 재해석. 10대의 목소리로 Quiet Storm 감성을 현대화한 명곡.",
                "yt_query": "Aaliyah - At Your Best (You Are Love)",
                "vibe": ["멜로디", "보컬", "가사"],
            },
        ],
        "recommendations": [
            {"title": "A Ribbon in the Sky", "artist": "Stevie Wonder", "year": 1982,
             "tags": ["낭만", "피아노", "클래식소울"], "match_attributes": ["멜로디", "가사"]},
            {"title": "Never Too Much", "artist": "Luther Vandross", "year": 1981,
             "tags": ["성숙", "스무드", "로맨틱"], "match_attributes": ["보컬", "멜로디"]},
            {"title": "Rock with You", "artist": "Michael Jackson", "year": 1979,
             "tags": ["부드러움", "댄서블", "팝소울"], "match_attributes": ["그루브", "멜로디"]},
            {"title": "I'll Make Love to You", "artist": "Boyz II Men", "year": 1994,
             "tags": ["로맨틱", "발라드", "아카펠라"], "match_attributes": ["보컬", "가사"]},
            {"title": "Sweet Love", "artist": "Anita Baker", "year": 1986,
             "tags": ["재즈소울", "성숙", "깊이"], "match_attributes": ["보컬", "멜로디"]},
        ],
        "timeline": [
            {"year": "1976", "era": "Origin",
             "title": "WHUR-FM — Quiet Storm 탄생",
             "desc": "워싱턴 DC 라디오 DJ Melvin Lindsey가 야간 프로그램 'Quiet Storm'을 시작.",
             "artists": ["Smokey Robinson", "Marvin Gaye"]},
            {"year": "1977~1981", "era": "Definition",
             "title": "장르의 정의 — 소프트 소울의 황금기",
             "desc": "Luther Vandross, Stephanie Mills, Peabo Bryson 등이 Quiet Storm 포맷을 완성.",
             "artists": ["Luther Vandross", "Peabo Bryson", "Teddy Pendergrass"]},
            {"year": "1983~1986", "era": "Sophistication",
             "title": "재즈와의 결합 — Anita Baker·Sade",
             "desc": "Anita Baker 'Rapture', Sade 'Diamond Life'로 재즈·소울의 성숙한 융합이 완성.",
             "artists": ["Anita Baker", "Sade", "Freddie Jackson"]},
            {"year": "1990s", "era": "Mainstream",
             "title": "Barry White·Boyz II Men — 대중화",
             "desc": "Boyz II Men, Brian McKnight, R. Kelly가 Quiet Storm 감성을 팝 차트로 이동.",
             "artists": ["Boyz II Men", "Brian McKnight", "Barry White"]},
            {"year": "2000s~현재", "era": "Legacy",
             "title": "슬로우 잼의 현재",
             "desc": "John Legend, Musiq Soulchild 등이 Quiet Storm의 성숙한 감성을 현대 R&B에 이식.",
             "artists": ["John Legend", "Musiq Soulchild", "Tweet"]},
        ],
    },

    # ────────────────────────
    # 6. 60~70s Classic Soul / Motown
    # ────────────────────────
    "🎸 60~70s Classic Soul / Motown": {
        "desc": "흑인음악의 뿌리. 모타운 팩토리 사운드, 시민권 운동의 목소리, 소울·리듬앤블루스의 황금 원형.",
        "color": "#b45309",
        "tracks": [
            {
                "title": "What's Going On",
                "artist": "Marvin Gaye",
                "year": 1971,
                "desc": "흑인음악 역사상 가장 위대한 앨범 중 하나. 베트남전·인종차별에 저항하는 시대의 목소리. 재즈·소울·팝의 완벽한 결합.",
                "yt_query": "Marvin Gaye - What's Going On",
                "vibe": ["가사", "멜로디", "보컬"],
            },
            {
                "title": "Respect",
                "artist": "Aretha Franklin",
                "year": 1967,
                "desc": "소울의 여왕 Aretha Franklin의 아이콘적 곡. 여성 해방과 흑인 자존감의 앤섬. 강렬한 보컬 전달력의 교과서.",
                "yt_query": "Aretha Franklin - Respect",
                "vibe": ["보컬", "가사", "리듬"],
            },
            {
                "title": "I Was Made to Love Her",
                "artist": "Stevie Wonder",
                "year": 1967,
                "desc": "10대 Stevie Wonder의 에너지가 폭발하는 Motown 클래식. 브라스와 리듬 섹션이 완벽하게 맞물리는 그루브.",
                "yt_query": "Stevie Wonder - I Was Made to Love Her",
                "vibe": ["그루브", "멜로디", "리듬"],
            },
        ],
        "recommendations": [
            {"title": "Papa Was a Rollin' Stone", "artist": "The Temptations", "year": 1972,
             "tags": ["사이키델릭소울", "드라마틱", "긴장감"], "match_attributes": ["가사", "그루브"]},
            {"title": "I Heard It Through the Grapevine", "artist": "Marvin Gaye", "year": 1968,
             "tags": ["드라마틱", "모타운", "클래식"], "match_attributes": ["멜로디", "보컬"]},
            {"title": "Chain of Fools", "artist": "Aretha Franklin", "year": 1967,
             "tags": ["파워풀", "그루브", "소울"], "match_attributes": ["보컬", "리듬"]},
            {"title": "Superstition", "artist": "Stevie Wonder", "year": 1972,
             "tags": ["펑키", "클라비넷", "그루브"], "match_attributes": ["그루브", "리듬"]},
            {"title": "Ain't No Mountain High Enough", "artist": "Marvin Gaye & Tammi Terrell", "year": 1967,
             "tags": ["듀엣", "감동", "클래식모타운"], "match_attributes": ["멜로디", "보컬"]},
        ],
        "timeline": [
            {"year": "1959~1961", "era": "Birth",
             "title": "Berry Gordy — 모타운 레코드 설립",
             "desc": "Detroit의 자동차 공장 노동자 Berry Gordy가 $800로 Motown을 창업. 흑인 음악을 백인 주류 시장에 팔겠다는 혁명적 비전.",
             "artists": ["Berry Gordy", "The Miracles", "Smokey Robinson"]},
            {"year": "1963~1966", "era": "Factory Sound",
             "title": "모타운 팩토리 사운드의 완성",
             "desc": "Funk Brothers 세션 밴드, Holland-Dozier-Holland 작곡팀. Supremes, Temptations, Four Tops로 전 세계 차트 정복.",
             "artists": ["The Supremes", "The Temptations", "Four Tops"]},
            {"year": "1967~1969", "era": "Soul Revolution",
             "title": "Atlantic Soul — Aretha·Otis의 시대",
             "desc": "Stax·Atlantic 레이블의 거친 소울이 Motown과 경쟁. 시민권 운동과 음악의 결합.",
             "artists": ["Aretha Franklin", "Otis Redding", "Sam Cooke"]},
            {"year": "1971~1974", "era": "Conscious Soul",
             "title": "Marvin Gaye·Stevie Wonder — 예술적 독립",
             "desc": "'What's Going On', 'Innervisions' 등 사회의식 담은 명작 탄생.",
             "artists": ["Marvin Gaye", "Stevie Wonder", "Curtis Mayfield"]},
            {"year": "1975~1979", "era": "Disco Era",
             "title": "소울에서 디스코로의 이행",
             "desc": "모타운과 소울이 디스코의 물결에 적응. 소울의 감성은 디스코 속에서 살아남음.",
             "artists": ["Commodores", "Diana Ross", "Lionel Richie"]},
            {"year": "현재", "era": "Legacy",
             "title": "모든 흑인음악의 DNA",
             "desc": "네오소울, 힙합, 컨템포러리 R&B의 모든 샘플과 감성의 원점.",
             "artists": ["Beyoncé", "Kendrick Lamar", "Leon Bridges"]},
        ],
    },

    # ────────────────────────
    # 7. 90s Hip-Hop Soul
    # ────────────────────────
    "🎧 90s Hip-Hop Soul": {
        "desc": "90년대 힙합의 날카로움과 R&B의 감성이 결합한 폭발적 장르. Mary J. Blige, Brandy, Puff Daddy가 정의한 시대.",
        "color": "#dc2626",
        "tracks": [
            {
                "title": "Real Love",
                "artist": "Mary J. Blige",
                "year": 1992,
                "desc": "힙합소울의 창시자 Mary J. Blige의 대표곡. 힙합 비트 위의 날 것 그대로의 감성. '거리의 소울'이라는 새 언어를 만들었다.",
                "yt_query": "Mary J. Blige - Real Love",
                "vibe": ["보컬", "그루브", "리듬"],
            },
            {
                "title": "Waterfalls",
                "artist": "TLC",
                "year": 1995,
                "desc": "힙합소울의 사회의식. T-Boz·Left Eye·Chilli 3인방이 에이즈·마약·폭력을 정면으로 노래. 장르가 메시지를 품은 순간.",
                "yt_query": "TLC - Waterfalls",
                "vibe": ["가사", "멜로디", "보컬"],
            },
            {
                "title": "I'll Be Missing You",
                "artist": "Puff Daddy & Faith Evans",
                "year": 1997,
                "desc": "Notorious B.I.G. 추모곡. 힙합과 소울이 애도라는 감정 위에서 완벽하게 결합된 역사적 트랙.",
                "yt_query": "Puff Daddy & Faith Evans - I'll Be Missing You",
                "vibe": ["가사", "보컬", "멜로디"],
            },
        ],
        "recommendations": [
            {"title": "Not Gon' Cry", "artist": "Mary J. Blige", "year": 1995,
             "tags": ["감성", "파워보컬", "힙합소울"], "match_attributes": ["보컬", "가사"]},
            {"title": "The Boy Is Mine", "artist": "Brandy & Monica", "year": 1998,
             "tags": ["듀엣", "대결", "팝R&B"], "match_attributes": ["보컬", "멜로디"]},
            {"title": "One in a Million", "artist": "Aaliyah", "year": 1996,
             "tags": ["미래적", "그루브", "쿨"], "match_attributes": ["그루브", "리듬"]},
            {"title": "If I Ruled the World", "artist": "Nas ft. Lauryn Hill", "year": 1996,
             "tags": ["의식적", "힙합", "소울"], "match_attributes": ["가사", "멜로디"]},
            {"title": "No Diggity", "artist": "Blackstreet ft. Dr. Dre", "year": 1996,
             "tags": ["그루브", "스무드", "힙합R&B"], "match_attributes": ["그루브", "리듬"]},
        ],
        "timeline": [
            {"year": "1991~1992", "era": "Birth",
             "title": "Mary J. Blige — 힙합소울의 탄생",
             "desc": "Sean 'Puffy' Combs 프로덕션으로 'What's the 411?' 발매. '힙합 소울'이라는 카테고리 창조.",
             "artists": ["Mary J. Blige", "Sean 'Puffy' Combs"]},
            {"year": "1993~1995", "era": "Explosion",
             "title": "TLC·SWV·Xscape — 여성 그룹의 전성기",
             "desc": "힙합소울이 여성 그룹을 통해 폭발적으로 확산.",
             "artists": ["TLC", "SWV", "Xscape", "En Vogue"]},
            {"year": "1994~1997", "era": "Timbaland Revolution",
             "title": "Timbaland의 비트 혁명",
             "desc": "Aaliyah 'One in a Million'으로 Timbaland가 힙합소울의 리듬 언어를 완전히 재설계.",
             "artists": ["Timbaland", "Aaliyah", "Missy Elliott"]},
            {"year": "1997~1999", "era": "Bad Boy Era",
             "title": "Bad Boy 레이블 — 힙합소울의 글래머화",
             "desc": "Puff Daddy·Bad Boy 사운드가 힙합소울에 럭셔리와 화려함을 더함.",
             "artists": ["Faith Evans", "112", "Puff Daddy"]},
            {"year": "2000~현재", "era": "Legacy",
             "title": "힙합소울의 유산 — R&B의 표준이 되다",
             "desc": "힙합소울의 문법이 이후 모든 R&B의 기본 문법으로 편입.",
             "artists": ["Beyoncé", "Rihanna", "Destiny's Child"]},
        ],
    },

    # ────────────────────────
    # 8. Afrobeats / Dancehall
    # ────────────────────────
    "🌍 Afrobeats / Dancehall": {
        "desc": "서아프리카·카리브해의 리듬이 세계 팝 무대로. Burna Boy, WizKid, Dancehall 사운드가 만드는 글로벌 그루브.",
        "color": "#16a34a",
        "tracks": [
            {
                "title": "Come Closer",
                "artist": "WizKid ft. Drake",
                "year": 2017,
                "desc": "아프로비츠가 글로벌 팝을 정복한 순간. WizKid의 기타 기반 아프로팝과 Drake의 감성이 결합된 시대 정의적 트랙.",
                "yt_query": "WizKid ft. Drake - Come Closer",
                "vibe": ["그루브", "리듬", "멜로디"],
            },
            {
                "title": "Essence",
                "artist": "WizKid ft. Tems",
                "year": 2020,
                "desc": "아프로비츠 역사상 가장 아름다운 트랙 중 하나. Tems의 독특한 보컬과 유기적 그루브가 완벽하게 맞물림.",
                "yt_query": "WizKid ft. Tems - Essence",
                "vibe": ["보컬", "멜로디", "그루브"],
            },
            {
                "title": "Ye",
                "artist": "Burna Boy",
                "year": 2018,
                "desc": "아프로퓨전의 교과서. 댄스홀·레게·아프로비츠가 하나로 융합되어 'Afro-Fusion'이라는 독자 언어를 완성.",
                "yt_query": "Burna Boy - Ye",
                "vibe": ["리듬", "그루브", "보컬"],
            },
        ],
        "recommendations": [
            {"title": "Last Last", "artist": "Burna Boy", "year": 2022,
             "tags": ["감성", "아프로퓨전", "서사"], "match_attributes": ["가사", "보컬"]},
            {"title": "Temperature", "artist": "Sean Paul", "year": 2005,
             "tags": ["댄스홀", "댄서블", "파티"], "match_attributes": ["리듬", "그루브"]},
            {"title": "Soco", "artist": "WizKid", "year": 2018,
             "tags": ["아프로팝", "축제", "밝음"], "match_attributes": ["멜로디", "그루브"]},
            {"title": "Ojuelegba", "artist": "WizKid", "year": 2014,
             "tags": ["향수", "스트리트", "멜로디"], "match_attributes": ["가사", "멜로디"]},
            {"title": "Calm Down", "artist": "Rema", "year": 2022,
             "tags": ["아프로팝", "댄서블", "로맨틱"], "match_attributes": ["멜로디", "리듬"]},
        ],
        "timeline": [
            {"year": "1970s", "era": "Roots",
             "title": "Fela Kuti — 아프로비트(Afrobeat)의 원조",
             "desc": "나이지리아의 음악가·활동가 Fela Kuti가 재즈·펑크·요루바 전통 음악을 결합해 'Afrobeat' 창조.",
             "artists": ["Fela Kuti", "Tony Allen"]},
            {"year": "1980s", "era": "Dancehall Birth",
             "title": "자메이카 댄스홀의 탄생",
             "desc": "레게에서 파생된 댄스홀이 Kingston 클럽 문화에서 독립 장르로 성장.",
             "artists": ["Yellowman", "Shabba Ranks"]},
            {"year": "2000s", "era": "Mainstream Dancehall",
             "title": "Sean Paul·Beenie Man — 댄스홀의 글로벌화",
             "desc": "Sean Paul 'Dutty Rock'이 전 세계 차트를 석권.",
             "artists": ["Sean Paul", "Beenie Man", "Shaggy"]},
            {"year": "2010~2016", "era": "Afrobeats Rise",
             "title": "현대 Afrobeats의 탄생 — Lagos 클럽씬",
             "desc": "나이지리아 Lagos를 중심으로 WizKid, Davido, P-Square가 현대적 아프로비츠 공식 완성.",
             "artists": ["WizKid", "Davido", "P-Square"]},
            {"year": "2017~2020", "era": "Global Takeover",
             "title": "Drake·Beyoncé와의 협업 — 세계 정복",
             "desc": "WizKid-Drake 'One Dance', Beyoncé 'The Lion King: The Gift'로 아프로비츠가 서구 팝 주류에 완전 편입.",
             "artists": ["Burna Boy", "WizKid", "Tems"]},
            {"year": "2021~현재", "era": "Afrobeats Dominance",
             "title": "Burna Boy — Grammy & 세계 무대",
             "desc": "Burna Boy 그래미 수상, Tems·Ayra Starr·Rema의 부상. 아프로비츠가 글로벌 팝의 새 문법으로 자리잡음.",
             "artists": ["Burna Boy", "Tems", "Rema", "Ayra Starr"]},
        ],
    },
}

# ── 매력 요소 목록 ──
ATTRIBUTES = ["멜로디", "가사", "그루브", "리듬", "보컬"]

# ── 페르소나 프리셋 ──
PERSONA_MAP = [
    ({"그루브", "리듬"},          "🕺 극단적 댄서블 성향 — 몸이 먼저 반응하는 리드미컬 리스너"),
    ({"멜로디", "보컬"},          "🎶 감성 멜로디스트 — 아름다운 선율과 목소리에 최우선 가치를 두는 청취자"),
    ({"가사", "보컬"},            "📖 리릭 다이버 — 가사의 깊이와 스토리텔링을 파고드는 지적 리스너"),
    ({"그루브", "보컬"},          "🎤 보컬 그루버 — 가수의 표현력과 리듬감이 결합된 순간에 전율하는 타입"),
    ({"멜로디", "리듬"},          "🌊 하모닉 리듬리스트 — 선율과 비트가 맞물리는 순간의 완성도를 추구"),
    ({"멜로디", "가사", "보컬"},   "💜 올라운드 소울 — 음악의 모든 요소를 균등하게 즐기는 풍부한 감수성"),
    ({"그루브", "리듬", "멜로디"}, "🔥 바이브 헌터 — 에너지·그루브·선율이 모두 갖춰진 완성형 트랙을 추구"),
]

# ── 타임라인 노드 스타일 (밝은 테마) ──
TIMELINE_NODE_STYLES = [
    {"bg": "#ede9fe", "border": "#7c3aed", "text": "#5b21b6"},
    {"bg": "#dbeafe", "border": "#2563eb", "text": "#1e40af"},
    {"bg": "#d1fae5", "border": "#059669", "text": "#065f46"},
    {"bg": "#fef3c7", "border": "#d97706", "text": "#92400e"},
    {"bg": "#fee2e2", "border": "#dc2626", "text": "#991b1b"},
    {"bg": "#f0fdf4", "border": "#16a34a", "text": "#14532d"},
]


# ══════════════════════════════════════════════════════════════
# 4. session_state 초기화
# ══════════════════════════════════════════════════════════════

def init_session(genre_key: str):
    if st.session_state.get("current_genre") != genre_key:
        st.session_state.current_genre = genre_key
        st.session_state.current_track = 0   # 현재 보여줄 트랙 인덱스 (0,1,2)
        st.session_state.evaluations   = {}  # {idx: {score, attributes, note}}
        st.session_state.phase         = "eval"

def get_eval(idx: int) -> dict:
    return st.session_state.evaluations.get(idx, {"score": 3, "attributes": [], "note": ""})

def save_eval(idx: int, score: int, attributes: list, note: str):
    st.session_state.evaluations[idx] = {"score": score, "attributes": attributes, "note": note}


# ══════════════════════════════════════════════════════════════
# 5. 분석 로직
# ══════════════════════════════════════════════════════════════

def calc_attribute_scores(evaluations: dict) -> dict:
    attr_scores = {a: 0.0 for a in ATTRIBUTES}
    for ev in evaluations.values():
        for attr in ev["attributes"]:
            if attr in attr_scores:
                attr_scores[attr] += ev["score"]
    return attr_scores

def get_persona(attr_scores: dict) -> str:
    sorted_attrs = sorted(attr_scores.items(), key=lambda x: x[1], reverse=True)
    top_two   = {a for a, s in sorted_attrs[:2] if s > 0}
    top_three = {a for a, s in sorted_attrs[:3] if s > 0}
    for key_set, text in PERSONA_MAP:
        if len(key_set) == 3 and key_set <= top_three:
            return text
    for key_set, text in PERSONA_MAP:
        if key_set <= top_two or key_set == top_two:
            return text
    return f"🎵 자유로운 리스너 — {', '.join(top_two)} 중심의 개성 있는 음악 취향" if top_two \
           else "🎵 탐색 중인 리스너 — 다양한 장르를 자유롭게 유영 중"

def rank_recommendations_dynamic(recommendations: list, attr_scores: dict) -> list:
    """사용자 상위 2 속성과 match_attributes 교집합 개수로 내림차순 정렬"""
    top_attrs = {a for a, s in sorted(attr_scores.items(), key=lambda x: x[1], reverse=True)[:2] if s > 0}
    scored = [{**r, "match_score": len(top_attrs & set(r.get("match_attributes", [])))}
              for r in recommendations]
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored

def build_radar_chart(attr_scores: dict, genre_color: str) -> go.Figure:
    labels = list(ATTRIBUTES)
    values = [attr_scores.get(a, 0) for a in labels]
    max_val = max(values) if max(values) > 0 else 1
    norm    = [round(v / max_val * 10, 1) for v in values]
    norm_c  = norm + [norm[0]]
    lbl_c   = labels + [labels[0]]
    r, g, b = int(genre_color[1:3], 16), int(genre_color[3:5], 16), int(genre_color[5:7], 16)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=norm_c, theta=lbl_c, fill="toself",
        fillcolor=f"rgba({r},{g},{b},0.12)",
        line=dict(color=genre_color, width=2.5),
        hovertemplate="%{theta}: %{r:.1f}/10<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.6)",
            radialaxis=dict(visible=True, range=[0, 10],
                            tickfont=dict(color="#9ca3af", size=9),
                            gridcolor="#f3f4f6", linecolor="#e5e7eb"),
            angularaxis=dict(tickfont=dict(color="#374151", size=13, family="Noto Sans KR"),
                             linecolor="#e5e7eb", gridcolor="#f3f4f6"),
        ),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=40, l=40, r=40), showlegend=False, height=400,
    )
    return fig

def generate_mixtape_report(genre_key, evaluations, attr_scores, persona, ranked_recs) -> str:
    tracks = GENRE_DATA[genre_key]["tracks"]
    now    = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
    lines  = [
        "╔══════════════════════════════════════════════╗",
        "║     🎵 나만의 흑인음악 디깅 믹스테이프 리포트     ║",
        "╚══════════════════════════════════════════════╝",
        "", f"📅 디깅 날짜    : {now}",
        f"🎧 선택 장르    : {genre_key}",
        f"🎭 나의 페르소나 : {persona}", "",
        "━" * 50, "  📊 나의 음악 속성 분석", "━" * 50,
    ]
    max_s = max(attr_scores.values()) if max(attr_scores.values()) > 0 else 1
    for attr in ATTRIBUTES:
        s = attr_scores.get(attr, 0)
        bl = int(s / max_s * 20) if max_s > 0 else 0
        lines.append(f"  {attr:5s}  [{'█'*bl}{'░'*(20-bl)}]  {s:.0f}pts")
    lines += ["", "━"*50, "  🎵 오늘의 디깅 트랙 & 나의 노트", "━"*50]
    for idx, track in enumerate(tracks):
        ev    = evaluations.get(idx, {})
        score = ev.get("score", "-")
        attrs = ev.get("attributes", [])
        note  = ev.get("note", "").strip() or "(노트 없음)"
        stars = "★"*int(score) + "☆"*(5-int(score)) if isinstance(score, int) else "—"
        lines += ["",
                  f"  [{idx+1}] {track['title']} — {track['artist']} ({track['year']})",
                  f"      총점    : {stars} ({score}/5)",
                  f"      매력    : {', '.join(attrs) if attrs else '선택 없음'}",
                  f"      📝 노트  : {note}"]
    lines += ["", "━"*50, "  🏆 맞춤 추천 플레이리스트 TOP 5", "━"*50]
    for i, rec in enumerate(ranked_recs[:5], 1):
        mark = " ★ MATCHED" if rec.get("match_score", 0) > 0 else ""
        lines.append(f"  {i}. {rec['title']} — {rec['artist']} ({rec['year']}){mark}")
        lines.append(f"     태그: {' | '.join(rec['tags'])}")
    lines += ["", "━"*50, "  Generated by 흑인음악 디깅 대시보드 v2.1 🎵",
              "  Keep Digging, Keep Growing.", "━"*50]
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
# 6. 타임라인 렌더링
# ══════════════════════════════════════════════════════════════

def render_timeline(genre_key: str, genre_color: str):
    tl = GENRE_DATA[genre_key].get("timeline", [])
    if not tl:
        st.info("타임라인 데이터 준비 중입니다.")
        return
    st.markdown(f"""
<div class="timeline-header">
  <div class="timeline-header-title">📜 {genre_key} — 장르 역사 타임라인</div>
  <div class="timeline-header-sub">
    이 장르가 어떻게 태동하고, 발전하고, 세상을 바꿨는지 핵심 역사를 따라가보세요.
  </div>
</div>
""", unsafe_allow_html=True)
    st.markdown('<div class="timeline-wrap">', unsafe_allow_html=True)
    for i, item in enumerate(tl):
        s = TIMELINE_NODE_STYLES[i % len(TIMELINE_NODE_STYLES)]
        artist_tags = "".join(f'<span class="timeline-artist-tag">{a}</span>'
                               for a in item.get("artists", []))
        st.markdown(f"""
<div class="timeline-item">
  <div class="timeline-node"
       style="background:{s['bg']};border-color:{s['border']};color:{s['text']};">
    {item['year']}
  </div>
  <div class="timeline-content">
    <div class="timeline-year" style="color:{s['border']};">{item.get('era','').upper()} ERA</div>
    <div class="timeline-title">{item['title']}</div>
    <div class="timeline-desc">{item['desc']}</div>
    <div class="timeline-artists">{artist_tags}</div>
  </div>
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 7. 사이드바
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🎧 장르 선택")
    st.markdown('<div style="font-size:0.8rem;color:#9ca3af;margin-bottom:10px;">디깅할 서브 장르를 골라보세요 (총 8개)</div>',
                unsafe_allow_html=True)

    selected_genre = st.selectbox("서브 장르", list(GENRE_DATA.keys()), label_visibility="collapsed")
    gdata = GENRE_DATA[selected_genre]

    st.markdown(f'<div class="sidebar-info">{gdata["desc"]}</div>', unsafe_allow_html=True)
    st.markdown("---")

    # 세션 초기화 (장르 변경 시)
    init_session(selected_genre)

    completed = len(st.session_state.evaluations)
    prog_pct  = int(completed / 3 * 100)
    st.markdown("### 📈 진행 상황")
    st.markdown(f"""
<div class="progress-wrap">
  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
    <span style="font-size:0.78rem;color:#6b7280;">평가 완료</span>
    <span style="font-size:0.78rem;color:#7c3aed;font-weight:700;">{completed}/3곡</span>
  </div>
  <div class="progress-track">
    <div class="progress-fill" style="width:{prog_pct}%;"></div>
  </div>
  <div class="progress-label">
    {"✅ 분석 준비 완료!" if completed == 3 else f"{3-completed}곡 더 평가하면 결과를 볼 수 있어요"}
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 처음부터 다시 시작", use_container_width=True):
        for k in ["current_genre", "current_track", "evaluations", "phase"]:
            if k == "evaluations": st.session_state[k] = {}
            elif k == "current_track": st.session_state[k] = 0
            elif k == "phase": st.session_state[k] = "eval"
            else: st.session_state[k] = None
        st.rerun()

    st.markdown("""
<div style="font-size:0.72rem;color:#d1d5db;margin-top:20px;line-height:1.8;">
ℹ️ 3곡 평가 완료 시<br>레이더 차트·맞춤 추천·<br>믹스테이프 리포트 생성<br><br>
🆕 v2.1 — 유튜브 직결 링크<br>
🆕 밝은 테마 적용<br>
🆕 순차 트랙 평가 플로우
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 8. 타이틀 배너
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="title-banner">
  <div class="title-main">나만의 흑인음악 취향 디깅 대시보드 🎵</div>
  <div class="title-sub">
    단 3곡의 청취 평가로 당신의 음악 DNA를 분석합니다.
    멜로디에 끌리는지, 그루브에 반응하는지 — 지금 바로 확인해보세요.<br>
    <span style="color:#7c3aed;font-weight:600;">✦ 8개 장르 · 취향 기반 동적 추천 · 장르 역사 타임라인</span>
  </div>
</div>
""", unsafe_allow_html=True)

# 세션 재확인
init_session(selected_genre)
tracks      = gdata["tracks"]
genre_color = gdata["color"]

if len(st.session_state.evaluations) == 3 and st.session_state.phase == "eval":
    st.session_state.phase = "result"


# ══════════════════════════════════════════════════════════════
# 9. EVAL 단계 — 메인 탭 (음악 평가 | 장르 타임라인)
# ══════════════════════════════════════════════════════════════

if st.session_state.phase == "eval":

    main_tab_eval, main_tab_history = st.tabs(["🎵 음악 평가", "📜 장르 역사 타임라인"])

    # ──────────────────────────────────────
    # 음악 평가 탭
    # ──────────────────────────────────────
    with main_tab_eval:

        st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  STEP 01 — 음악 청취 &amp; 다차원 평가
</div>
""", unsafe_allow_html=True)

        # ── 상단 트랙 진행 표시기 ──
        cur = st.session_state.current_track
        pip_html = '<div class="track-progress-wrap">'
        for i in range(3):
            if i in st.session_state.evaluations:
                cls = "pip-done"; label = "✓"
            elif i == cur:
                cls = "pip-active"; label = str(i + 1)
            else:
                cls = "pip-locked"; label = str(i + 1)
            pip_html += f'<div class="track-pip {cls}">{label}</div>'
            if i < 2:
                line_cls = "track-pip-line-done" if i in st.session_state.evaluations else "track-pip-line"
                pip_html += f'<div class="track-pip-line {line_cls}"></div>'
        pip_html += '</div>'
        st.markdown(pip_html, unsafe_allow_html=True)

        # ── 현재 트랙 정보 ──
        track = tracks[cur]
        yt_q  = track["yt_query"].replace(" ", "+").replace("'", "%27").replace("&", "%26")

        st.markdown(f"""
<div class="track-card">
  <div class="track-number">0{cur+1}</div>
  <div class="track-title">🎵 {track['title']}</div>
  <div class="track-artist">👤 {track['artist']} · {track['year']}</div>
  <div class="track-desc">{track['desc']}</div>
  <a class="yt-link"
     href="https://www.youtube.com/results?search_query={yt_q}"
     target="_blank">▶ YouTube에서 "{track['artist']} - {track['title']}" 검색 ↗</a>
</div>
""", unsafe_allow_html=True)

        # 이미 저장된 값 불러오기
        prev = get_eval(cur)

        # ── 총점 슬라이더 ──
        st.markdown('<div class="eval-label">⭐ 총점 (1~5점)</div>', unsafe_allow_html=True)
        score = st.slider("총점", 1, 5, value=prev["score"],
                          key=f"score_{selected_genre}_{cur}",
                          label_visibility="collapsed")
        st.markdown(f'<div class="star-guide">{"★"*score}{"☆"*(5-score)} &nbsp; {score}점</div>',
                    unsafe_allow_html=True)

        # ── 매력 요소 체크박스 ──
        st.markdown('<div class="eval-label">✨ 좋았던 매력 요소 (복수 선택 가능)</div>',
                    unsafe_allow_html=True)
        attr_cols = st.columns(5)
        selected_attrs = []
        for ai, attr in enumerate(ATTRIBUTES):
            with attr_cols[ai]:
                if st.checkbox(attr, value=(attr in prev["attributes"]),
                               key=f"attr_{selected_genre}_{cur}_{attr}"):
                    selected_attrs.append(attr)

        # ── 한 줄 디깅 노트 ──
        st.markdown('<div class="eval-label">📝 한 줄 디깅 노트</div>', unsafe_allow_html=True)
        note = st.text_input("디깅 노트", value=prev["note"],
                             placeholder="이 곡을 들으며 느낀 감상평이나 매력 포인트를 자유롭게 적어보세요...",
                             key=f"note_{selected_genre}_{cur}",
                             label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 버튼 영역 ──
        already_saved = cur in st.session_state.evaluations

        if cur < 2:
            # ── Track 1, 2: "평가 저장 후 다음 트랙으로" ──
            bcol1, bcol2, _ = st.columns([1.4, 1.4, 2])
            with bcol1:
                btn_label = "💾 수정 저장" if already_saved else "✅ 평가 완료"
                if st.button(btn_label, key=f"save_{selected_genre}_{cur}", use_container_width=True):
                    save_eval(cur, score, selected_attrs, note)
                    st.rerun()

            # "다음 트랙" 버튼 — 현재 트랙이 저장된 경우에만 활성화
            with bcol2:
                next_disabled = cur not in st.session_state.evaluations
                if st.button(
                    f"➡️ Track {cur+2}로 이동",
                    key=f"next_{selected_genre}_{cur}",
                    disabled=next_disabled,
                    use_container_width=True,
                ):
                    st.session_state.current_track = cur + 1
                    st.rerun()

            if next_disabled:
                st.caption("💡 먼저 **평가 완료** 버튼을 눌러 저장해주세요.")

        else:
            # ── Track 3: "평가 완료 & 결과 보기" ──
            bcol1, _ = st.columns([1.6, 2])
            with bcol1:
                btn_label = "💾 수정 저장" if already_saved else "🎉 평가 완료 & 결과 보기"
                if st.button(btn_label, key=f"save_{selected_genre}_{cur}", use_container_width=True):
                    save_eval(cur, score, selected_attrs, note)
                    if len(st.session_state.evaluations) == 3:
                        st.session_state.phase = "result"
                    st.rerun()

        # 이전 트랙으로 돌아가기 (첫 트랙이 아닐 때)
        if cur > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"← Track {cur}으로 돌아가기",
                         key=f"prev_{selected_genre}_{cur}"):
                st.session_state.current_track = cur - 1
                st.rerun()

        # 이미 저장된 트랙 요약 표시
        if already_saved:
            saved = st.session_state.evaluations[cur]
            st.markdown(f"""
<div class="complete-banner">
  ✅ 저장됨 — {saved['score']}점 · {', '.join(saved['attributes']) if saved['attributes'] else '속성 미선택'}
  {f' · 📝 {saved["note"][:30]}{"..." if len(saved["note"])>30 else ""}' if saved.get('note') else ''}
</div>
""", unsafe_allow_html=True)

    # ──────────────────────────────────────
    # 장르 역사 타임라인 탭
    # ──────────────────────────────────────
    with main_tab_history:
        st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  HISTORY — 장르 역사 타임라인
</div>
""", unsafe_allow_html=True)
        render_timeline(selected_genre, genre_color)


# ══════════════════════════════════════════════════════════════
# 10. RESULT 단계 — 분석 결과 화면
# ══════════════════════════════════════════════════════════════

elif st.session_state.phase == "result":

    evaluations = st.session_state.evaluations
    attr_scores = calc_attribute_scores(evaluations)
    persona     = get_persona(attr_scores)
    ranked_recs = rank_recommendations_dynamic(gdata["recommendations"], attr_scores)

    # 완료 배너
    st.markdown("""
<div class="all-done-banner">
  🎉 3곡 평가 완료! 당신의 음악 DNA 분석 결과를 확인해보세요.
</div>
""", unsafe_allow_html=True)

    bc1, bc2, _ = st.columns([1, 1, 3])
    with bc1:
        if st.button("← 평가 수정하기"):
            st.session_state.phase = "eval"
            st.rerun()
    with bc2:
        if st.button("📜 장르 역사 보기"):
            st.session_state.phase = "history_only"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 결과 헤더
    avg = sum(e["score"] for e in evaluations.values()) / 3
    st.markdown(f"""
<div class="result-header">
  <div class="result-title">🎭 {persona}</div>
  <div class="result-persona">
    선택 장르: <strong>{selected_genre}</strong> &nbsp;|&nbsp;
    평균 점수: <strong>{'★'*round(avg)}{'☆'*(5-round(avg))} ({avg:.1f}/5)</strong>
    &nbsp;|&nbsp; 총 평가 트랙: <strong>3곡</strong>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── 2단계: 레이더 차트 ──
    st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  STEP 02 — 취향 오각형 레이더 차트
</div>
""", unsafe_allow_html=True)

    r_col, d_col = st.columns([1.1, 0.9])
    with r_col:
        st.plotly_chart(build_radar_chart(attr_scores, genre_color),
                        use_container_width=True, config={"displayModeBar": False})

    with d_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.9rem;font-weight:700;color:#374151;margin-bottom:14px;">📊 속성별 점수 분포</div>',
                    unsafe_allow_html=True)
        max_sv = max(attr_scores.values()) if max(attr_scores.values()) > 0 else 1
        color_map = {"멜로디": "#db2777", "가사": "#4f46e5",
                     "그루브": "#ea580c", "리듬": "#0891b2", "보컬": "#7c3aed"}
        for rank, (attr, s) in enumerate(sorted(attr_scores.items(), key=lambda x: x[1], reverse=True), 1):
            pct = int(s / max_sv * 100) if max_sv > 0 else 0
            bc  = color_map.get(attr, "#6366f1")
            med = ["🥇","🥈","🥉","4️⃣","5️⃣"][rank-1]
            st.markdown(f"""
<div style="margin-bottom:14px;">
  <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
    <span style="font-size:0.83rem;color:#374151;font-weight:600;">{med} {attr}</span>
    <span style="font-size:0.83rem;color:{bc};font-weight:700;">{s:.0f}pts</span>
  </div>
  <div class="attr-bar-bg">
    <div style="width:{pct}%;height:8px;background:linear-gradient(90deg,{bc}88,{bc});border-radius:999px;"></div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#374151;margin-bottom:10px;">🎵 트랙별 평가 요약</div>',
                    unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame([{"곡": t["title"][:18],
                           "점수": "★"*evaluations.get(i,{}).get("score",0),
                           "매력": ", ".join(evaluations.get(i,{}).get("attributes",[])) or "-"}
                          for i, t in enumerate(tracks)]),
            hide_index=True, use_container_width=True,
        )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ── 3단계: 추천 플레이리스트 + 믹스테이프 ──
    st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  STEP 03 — 나만의 믹스테이프 &amp; 취향 맞춤 추천
</div>
""", unsafe_allow_html=True)

    rec_col, rep_col = st.columns([1, 1])

    with rec_col:
        top_attrs_display = [a for a, s in sorted(attr_scores.items(), key=lambda x: x[1], reverse=True)[:2] if s > 0]
        st.markdown(
            f'<div style="font-size:0.95rem;font-weight:700;color:#111827;margin-bottom:6px;">🏆 맞춤 추천 플레이리스트</div>'
            f'<div style="font-size:0.75rem;color:#9ca3af;margin-bottom:14px;">'
            f'선호 속성 <strong style="color:#7c3aed;">{" · ".join(top_attrs_display)}</strong> 기반 정렬</div>',
            unsafe_allow_html=True,
        )
        rank_labels = ["🥇","🥈","🥉","4","5"]
        for rank, rec in enumerate(ranked_recs[:5], 1):
            ms       = rec.get("match_score", 0)
            card_cls = "rec-card-matched" if ms > 0 else "rec-card"
            badge    = f'<div class="rec-match-badge">{"🎯 BEST MATCH" if ms==2 else "✓ MATCH"}</div>' if ms > 0 else ""
            ma_set   = set(rec.get("match_attributes", []))
            tag_html = "".join(f'<span class="{"rec-tag-highlight" if t in ma_set else "rec-tag"}">{t}</span>'
                                for t in rec["tags"])
            st.markdown(f"""
<div class="{card_cls}">
  {badge}
  <div class="rec-rank">{rank_labels[rank-1]}</div>
  <div class="rec-title">{rec['title']}</div>
  <div class="rec-artist">👤 {rec['artist']} · {rec['year']}</div>
  <div class="rec-tags">{tag_html}</div>
</div>
""", unsafe_allow_html=True)

    with rep_col:
        st.markdown('<div style="font-size:0.95rem;font-weight:700;color:#111827;margin-bottom:14px;">📼 오늘의 디깅 믹스테이프 리포트</div>',
                    unsafe_allow_html=True)
        report_text = generate_mixtape_report(selected_genre, evaluations, attr_scores, persona, ranked_recs)
        st.markdown(f'<div class="mixtape-box">{report_text}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button("⬇️ TXT 다운로드", data=report_text.encode("utf-8"),
                               file_name=f"digging_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                               mime="text/plain", use_container_width=True)
        with dl2:
            st.text_area("복사용", value=report_text, height=80,
                         label_visibility="collapsed", key="copy_area")

    # 하단 타임라인
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  BONUS — 장르 역사 타임라인
</div>
""", unsafe_allow_html=True)
    render_timeline(selected_genre, genre_color)

    st.markdown("""
<div style="background:#f9fafb;border:1.5px solid #e5e7eb;border-radius:12px;
            padding:16px 20px;text-align:center;margin-top:16px;">
  <div style="font-size:0.82rem;color:#9ca3af;line-height:1.8;">
    💡 <strong style="color:#7c3aed;">다른 장르도 디깅해보세요!</strong>
    사이드바에서 장르를 변경하면 새로운 탐험을 시작합니다.<br>
    총 8개 장르 · 각 장르마다 다른 레이더 차트·추천 리스트·역사 타임라인이 생성됩니다.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 11. HISTORY_ONLY 단계
# ══════════════════════════════════════════════════════════════

elif st.session_state.phase == "history_only":
    if st.button("← 분석 결과로 돌아가기"):
        st.session_state.phase = "result"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    render_timeline(selected_genre, genre_color)
