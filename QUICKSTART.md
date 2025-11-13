# 🚀 EO Studio CFO Dashboard - 빠른 시작 가이드

## 📌 5분 안에 대시보드 실행하기

### Step 1: 패키지 설치 (1분)

```bash
pip install -r requirements.txt
```

### Step 2: 대시보드 실행 (10초)

```bash
streamlit run dashboard.py
```

브라우저가 자동으로 열리고 `http://localhost:8501`에 대시보드가 표시됩니다!

---

## 🎯 현재 상태

✅ **완료된 항목**
- 더미 데이터 기반 완전히 작동하는 대시보드
- 8개 주요 섹션 구현 (Cash Flow, Revenue, Expense, P&L, Pipeline, Headcount, Risk)
- 20+ 인터랙티브 차트
- 필터 기능 (기간, 국가, 팀)
- 반응형 레이아웃

📋 **다음 단계**
- 구글 시트 준비 및 연결
- 실제 데이터 입력
- 팀원 교육

---

## 📊 대시보드 둘러보기

### 1. 사이드바 (왼쪽)
- **기간 선택**: 분석할 날짜 범위 설정
- **국가 선택**: Korea, USA, Vietnam 중 선택
- **팀 선택**: Video Production, Branded Content, EO School 중 선택

### 2. 메인 화면 (스크롤하며 확인)

#### 🎯 핵심 KPI (최상단)
5개의 주요 지표 카드:
- 총 매출
- 총 비용
- 순이익
- 현금 잔고
- 인당 매출

#### 💵 Cash Flow & Runway
- 월별 매출/비용 추이 바 차트
- Runway 게이지 (현금 소진까지 남은 개월)

#### 💵 Revenue 분석
3개 탭으로 구성:
- **추이 분석**: 국가별 월간 매출 라인 차트
- **국가별**: 파이 차트 + 바 차트
- **팀별**: 팀별 매출 합계 및 추이

#### 💸 Expense 분석
- 카테고리별 비용 합계 (Personnel, Marketing, Operations, COGS)
- 월별 비용 추이 (Stacked Area Chart)

#### 📊 손익계산서 (P&L)
- 월별 P&L 상세 테이블
- 매출총이익률 및 순이익률 추이 차트

#### 🎯 Sales Pipeline
- Funnel Chart (Proposal → Contract → Payment Pending → Closed Won)
- 총 파이프라인 가치 및 가중 파이프라인
- 팀별 파이프라인

#### 👥 Headcount & Productivity
- 국가별/팀별 인원 현황
- 팀별 인당 매출 (생산성)

#### ⚠️ Risk Management
- 미수금 현황 (Pending, Overdue)
- 국가별 현금 분산
- Critical Alerts

---

## 🔄 실제 데이터로 전환하기

### 옵션 1: 구글 시트 (CSV Export) ⭐ 추천

**소요 시간**: 약 30분

1. **구글 시트 생성** (10분)
   - 새 구글 시트 생성
   - `SCHEMA_DESIGN.md` 참조하여 탭 생성:
     - RAW_Revenue
     - RAW_Expense
     - RAW_Cash
     - Sales_Pipeline
     - Headcount
   - 각 탭에 컬럼 헤더 추가

2. **샘플 데이터 입력** (10분)
   - 각 탭에 최소 5-10개 데이터 입력
   - 날짜 형식: YYYY-MM-DD (예: 2024-01-15)
   - 금액: 숫자만 입력 (쉼표 없이)

3. **웹에 게시** (5분)
   - 각 탭마다: 파일 > 공유 > 웹에 게시
   - 형식: CSV 선택
   - URL 복사

4. **코드 수정** (5분)
   - `dashboard.py` 열기
   - `GOOGLE_SHEETS_GUIDE.md`의 "방법 1" 코드 복사
   - `load_fake_data()` 함수를 `load_data_from_google_sheets()`로 교체
   - URL 입력

5. **테스트**
   ```bash
   streamlit run dashboard.py
   ```

**상세 가이드**: `GOOGLE_SHEETS_GUIDE.md` 참조

---

## 💡 유용한 팁

### 차트 다운로드
- 각 차트 우측 상단의 카메라 아이콘 클릭 → PNG로 저장

### 대시보드 새로고침
- 브라우저에서 `R` 키 → 페이지 새로고침
- `C` 키 → 캐시 클리어 (데이터 강제 새로고침)

### 필터 조합
- 예: "2024년 1월~6월, 한국, Video Production 팀" 매출만 보기
- 여러 팀 동시 선택 가능

### 대시보드 공유
- **로컬 네트워크**:
  ```bash
  streamlit run dashboard.py --server.address 0.0.0.0
  ```
  → 같은 와이파이의 다른 기기에서 접속 가능

- **인터넷 공유**: Streamlit Community Cloud (무료)
  - https://streamlit.io/cloud 에서 배포

---

## 🎓 학습 리소스

### 데이터 구조 이해하기
- **SCHEMA_DESIGN.md**: 각 탭의 컬럼 의미와 샘플 데이터

### 구글 시트 연결하기
- **GOOGLE_SHEETS_GUIDE.md**: 3가지 방법 상세 설명
  - 방법 1: CSV Export (간단)
  - 방법 2: Google Sheets API (보안)
  - 방법 3: 로컬 CSV (오프라인)

### 프로젝트 전체 설명
- **README.md**: 프로젝트 개요, 기능, 커스터마이징

---

## 🆘 문제 해결

### 문제: ModuleNotFoundError
```bash
# 해결
pip install -r requirements.txt
```

### 문제: 대시보드가 안 열려요
```bash
# 수동으로 브라우저에서 접속
http://localhost:8501
```

### 문제: 포트 8501이 이미 사용 중
```bash
# 다른 포트 사용
streamlit run dashboard.py --server.port 8502
```

### 문제: 데이터가 이상해요
- 현재는 **더미 데이터**를 사용합니다
- 실제 데이터 연결 전까지 정상입니다

---

## 📞 추가 도움

### 문서 읽기 순서
1. **QUICKSTART.md** (이 문서) - 빠른 시작
2. **README.md** - 프로젝트 전체 개요
3. **SCHEMA_DESIGN.md** - 데이터 구조 이해
4. **GOOGLE_SHEETS_GUIDE.md** - 실제 데이터 연결

### 코드 구조
- `dashboard.py`: 단일 파일로 모든 기능 포함
- `load_fake_data()` 함수: 더미 데이터 생성 (나중에 교체)

---

## ✅ 체크리스트

### 초기 설정
- [ ] Python 3.8+ 설치 확인
- [ ] `pip install -r requirements.txt` 실행
- [ ] `streamlit run dashboard.py` 실행
- [ ] 브라우저에서 대시보드 확인

### 실제 데이터 연결 준비
- [ ] `SCHEMA_DESIGN.md` 읽기
- [ ] 구글 시트 생성 및 탭 구조화
- [ ] 샘플 데이터 입력
- [ ] `GOOGLE_SHEETS_GUIDE.md` 따라 연결

### 배포 (선택)
- [ ] Streamlit Community Cloud 계정 생성
- [ ] GitHub 저장소 연결
- [ ] 배포 및 팀원과 공유

---

**🎉 이제 시작할 준비가 되었습니다! 대시보드를 실행해보세요:**

```bash
streamlit run dashboard.py
```

**행운을 빕니다! 🚀**
