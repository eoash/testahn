# 📊 EO Studio CFO Dashboard

> **실시간 재무 및 경영 지표를 한눈에 확인할 수 있는 인터랙티브 대시보드**

EO Studio의 한국, 미국, 베트남 3개국 사업 전반의 재무 데이터를 시각화하고 분석하는 웹 기반 대시보드입니다.

---

## 🎯 주요 기능

### 1. 💰 핵심 KPI 카드
- 총 매출, 비용, 순이익
- 현금 잔고 및 인당 매출

### 2. 💵 Cash Flow & Runway
- 월별 Cash Flow 추이 (매출 vs 비용)
- Runway 게이지 (현금 소진까지 남은 개월 수)
- Burn Rate 분석

### 3. 📈 Revenue 분석
- 국가별/팀별 매출 분해
- 월간 매출 추이
- 매출 비중 분석 (파이 차트, 바 차트)

### 4. 💸 Expense 분석
- 비용 카테고리별 합계 및 비중
- 월별 비용 추이 (Stacked Area Chart)

### 5. 📊 손익계산서 (P&L)
- 월별 Revenue, COGS, Gross Profit, OpEx, Net Profit
- 매출총이익률 및 순이익률 추이
- 월별 P&L 테이블

### 6. 🎯 Sales Pipeline
- 단계별 파이프라인 (Proposal → Contract → Payment Pending → Closed Won)
- 가중 파이프라인 가치 (확률 반영)
- 팀별 파이프라인

### 7. 👥 Headcount & Productivity
- 국가별/팀별 인원 현황
- 팀별 인당 매출 (생산성 지표)

### 8. ⚠️ Risk Management
- 미수금 현황 (Pending, Overdue)
- 국가별 현금 분산
- Critical Alerts (Runway 부족, 연체 미수금 등)

---

## 🚀 빠른 시작

### 1. 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)

### 2. 설치

```bash
# 저장소 클론 (또는 파일 다운로드)
git clone <repository-url>
cd testahn

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 실행

```bash
streamlit run dashboard.py
```

브라우저가 자동으로 열리고 `http://localhost:8501`에서 대시보드를 확인할 수 있습니다.

---

## 📁 프로젝트 구조

```
testahn/
├── dashboard.py              # 메인 대시보드 코드
├── requirements.txt          # Python 의존성
├── SCHEMA_DESIGN.md          # 데이터 스키마 설계 문서
├── GOOGLE_SHEETS_GUIDE.md    # 구글 시트 연결 가이드
├── README.md                 # 이 파일
└── data/                     # (선택) 로컬 CSV 데이터 저장 폴더
```

---

## 📊 데이터 구조

현재 대시보드는 **더미 데이터**를 사용합니다. 실제 데이터로 전환하려면 다음 단계를 따르세요:

### 데이터 소스 옵션

1. **구글 시트 (CSV Export)** ⭐ 추천
   - 가장 간단하고 빠른 방법
   - `GOOGLE_SHEETS_GUIDE.md` 참조

2. **Google Sheets API**
   - 보안이 중요한 경우
   - `GOOGLE_SHEETS_GUIDE.md` 참조

3. **로컬 CSV 파일**
   - 오프라인 환경
   - `data/` 폴더에 CSV 파일 저장

### 필수 데이터 탭

`SCHEMA_DESIGN.md`를 참조하여 다음 탭을 구글 시트에 생성하세요:

1. `RAW_Revenue` - 매출 거래 데이터
2. `RAW_Expense` - 비용 지출 데이터
3. `RAW_Cash` - 현금 잔고 데이터
4. `Sales_Pipeline` - 영업 파이프라인
5. `Headcount` - 인력 현황

각 탭의 컬럼 구조는 `SCHEMA_DESIGN.md`에 상세히 정의되어 있습니다.

---

## 🔧 커스터마이징

### 1. KPI 추가

`dashboard.py`의 상단 KPI 카드 섹션을 수정:

```python
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="새로운 KPI",
        value="값",
        delta="변화량"
    )
```

### 2. 차트 추가

Plotly를 사용하여 새로운 차트 추가:

```python
fig = px.bar(df, x='column1', y='column2', title='새로운 차트')
st.plotly_chart(fig, use_container_width=True)
```

### 3. 필터 추가

사이드바에 새로운 필터 추가:

```python
new_filter = st.sidebar.selectbox(
    "새로운 필터",
    options=['옵션1', '옵션2']
)
```

---

## 📖 상세 문서

- **[SCHEMA_DESIGN.md](SCHEMA_DESIGN.md)**: 데이터 스키마 및 구글 시트 탭 구조
- **[GOOGLE_SHEETS_GUIDE.md](GOOGLE_SHEETS_GUIDE.md)**: 구글 시트 연결 방법 (3가지 방식)

---

## 🛠️ 기술 스택

- **Frontend**: Streamlit (Python 웹 프레임워크)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (인터랙티브 차트)
- **Data Source**: Google Sheets (또는 CSV)

---

## 📝 사용 팁

### 1. 필터 활용
- 사이드바에서 기간, 국가, 팀을 선택하여 데이터를 필터링하세요.
- 여러 필터를 조합하여 세부 분석이 가능합니다.

### 2. 차트 인터랙션
- 모든 차트는 인터랙티브합니다:
  - 호버하여 상세 정보 확인
  - 줌 인/아웃
  - 범례 클릭하여 항목 토글
  - 우측 상단 아이콘으로 PNG 다운로드

### 3. 데이터 새로고침
- 브라우저에서 `R` 키를 눌러 페이지 새로고침
- 또는 `C` 키를 눌러 캐시 클리어

### 4. 대시보드 공유
- Streamlit Community Cloud에 무료로 배포 가능
- 또는 로컬 네트워크에서 `streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0`

---

## 🚨 트러블슈팅

### 문제: 대시보드가 실행되지 않아요

**해결**:
```bash
# 의존성 재설치
pip install --upgrade -r requirements.txt

# Streamlit 버전 확인
streamlit version

# 캐시 클리어
streamlit cache clear
```

### 문제: 데이터가 표시되지 않아요

**해결**:
- 현재는 더미 데이터를 사용합니다. `load_fake_data()` 함수가 정상 작동하는지 확인하세요.
- 실제 데이터 연결 시: `GOOGLE_SHEETS_GUIDE.md` 참조

### 문제: 차트가 깨져요

**해결**:
- Plotly 버전 확인: `pip install --upgrade plotly`
- 브라우저 캐시 클리어

---

## 🔐 보안 주의사항

### Google Sheets API 사용 시

1. **절대 git에 커밋하지 마세요**:
   - `credentials.json` (서비스 계정 키)
   - `.env` (환경 변수)

2. **`.gitignore`에 추가**:
   ```
   credentials.json
   *.json
   .env
   __pycache__/
   ```

3. **시트 권한 관리**:
   - 최소 권한 원칙 적용
   - 정기적으로 권한 검토

---

## 🤝 기여

이 프로젝트는 EO Studio 내부용으로 개발되었습니다.

개선 사항이나 버그 발견 시:
1. 이슈를 생성하거나
2. Pull Request를 제출해주세요

---

## 📄 라이선스

Copyright (c) 2024 EO Studio. All rights reserved.

---

## 👨‍💼 담당자

- **Finance Lead / CFO**
- **Data Engineer**: Claude (AI Assistant)

---

## 📅 버전 히스토리

### v1.0.0 (2024-11)
- 초기 버전 출시
- 더미 데이터 기반 대시보드
- 8개 주요 섹션 구현
- 구글 시트 연결 가이드 포함

---

## 🎓 다음 단계

### Phase 1: 데이터 연결 (현재 단계)
- [ ] 구글 시트 탭 생성
- [ ] 샘플 데이터 입력
- [ ] 구글 시트 연결 (CSV Export 방식)
- [ ] 대시보드 테스트

### Phase 2: 실제 데이터 마이그레이션
- [ ] 기존 엑셀 데이터를 구글 시트로 이전
- [ ] 데이터 검증
- [ ] 팀원 교육

### Phase 3: 고급 기능
- [ ] 예산 대비 실적 비교
- [ ] 환율 자동 업데이트
- [ ] 이메일 알림 (Critical Alerts)
- [ ] 월간 리포트 자동 생성

### Phase 4: 배포
- [ ] Streamlit Community Cloud 배포
- [ ] 또는 자체 서버 배포
- [ ] 접근 권한 관리

---

**🚀 행운을 빕니다! EO Studio의 성공적인 재무 관리를 응원합니다!**
