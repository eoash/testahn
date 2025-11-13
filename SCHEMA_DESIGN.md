# EO Studio 재무 대시보드 - 데이터 스키마

## 📋 구글 시트 탭 구조

### 1️⃣ **RAW_Revenue** (매출 원천 데이터)

모든 매출 거래를 기록하는 탭입니다.

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| `transaction_id` | TEXT | 거래 고유 ID | REV-2024-001 |
| `date` | DATE | 거래 발생일 | 2024-01-15 |
| `country` | TEXT | 국가 | Korea, USA, Vietnam |
| `team` | TEXT | 담당 팀 | Video Production, Branded Content, EO School |
| `client_name` | TEXT | 고객명 | Samsung Electronics |
| `project_name` | TEXT | 프로젝트명 | Galaxy S24 Campaign |
| `amount_original` | NUMBER | 원화 금액 | 50000000 |
| `currency` | TEXT | 통화 | KRW, USD, VND |
| `amount_krw` | NUMBER | KRW 환산 금액 | 50000000 |
| `exchange_rate` | NUMBER | 적용 환율 | 1.0 (KRW), 1300 (USD) |
| `payment_status` | TEXT | 입금 상태 | Paid, Pending, Overdue |
| `invoice_date` | DATE | 청구일 | 2024-01-10 |
| `payment_date` | DATE | 실제 입금일 | 2024-01-15 |
| `payment_terms` | TEXT | 결제 조건 | NET 30, NET 60 |
| `category` | TEXT | 매출 카테고리 | Retainer, Project-based, License |
| `notes` | TEXT | 비고 | 분할 입금 1/3 |

**샘플 데이터 예시:**
```
REV-2024-001 | 2024-01-15 | Korea | Video Production | Samsung | Galaxy S24 | 50000000 | KRW | 50000000 | 1.0 | Paid | 2024-01-10 | 2024-01-15 | NET 30 | Project-based | -
REV-2024-002 | 2024-01-20 | USA | Branded Content | Nike | Spring Campaign | 30000 | USD | 39000000 | 1300 | Pending | 2024-01-15 | - | NET 60 | Retainer | -
```

---

### 2️⃣ **RAW_Expense** (비용 원천 데이터)

모든 비용 지출을 기록하는 탭입니다.

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| `expense_id` | TEXT | 비용 고유 ID | EXP-2024-001 |
| `date` | DATE | 지출 발생일 | 2024-01-15 |
| `country` | TEXT | 국가 | Korea, USA, Vietnam |
| `team` | TEXT | 담당 팀 (해당시) | Video Production, Branded Content, EO School, Admin |
| `category_l1` | TEXT | 대분류 | Personnel, Marketing, Operations, COGS |
| `category_l2` | TEXT | 중분류 | Salary, Freelancer, Ads, Office Rent, Equipment |
| `vendor` | TEXT | 거래처명 | Google Ads, Freelancer John |
| `description` | TEXT | 설명 | 2024년 1월 급여 |
| `amount_original` | NUMBER | 원화 금액 | 10000000 |
| `currency` | TEXT | 통화 | KRW, USD, VND |
| `amount_krw` | NUMBER | KRW 환산 금액 | 10000000 |
| `exchange_rate` | NUMBER | 적용 환율 | 1.0 |
| `payment_method` | TEXT | 지불 방법 | Bank Transfer, Credit Card |
| `is_recurring` | BOOLEAN | 정기 지출 여부 | TRUE, FALSE |
| `project_related` | TEXT | 프로젝트 연결 (COGS) | Galaxy S24 Campaign |
| `notes` | TEXT | 비고 | - |

**샘플 데이터 예시:**
```
EXP-2024-001 | 2024-01-15 | Korea | Admin | Personnel | Salary | - | 2024년 1월 급여 | 80000000 | KRW | 80000000 | 1.0 | Bank Transfer | TRUE | - | -
EXP-2024-002 | 2024-01-20 | Korea | Video Production | COGS | Freelancer | John Doe | 편집 작업 | 5000000 | KRW | 5000000 | 1.0 | Bank Transfer | FALSE | Galaxy S24 | -
```

---

### 3️⃣ **RAW_Cash** (현금 잔고)

각 계좌별 현금 잔고를 추적하는 탭입니다.

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| `date` | DATE | 기준일 | 2024-01-31 |
| `country` | TEXT | 국가 | Korea, USA, Vietnam |
| `account_name` | TEXT | 계좌명 | 신한은행 법인계좌, Chase Business |
| `currency` | TEXT | 통화 | KRW, USD, VND |
| `balance_original` | NUMBER | 원화 잔고 | 500000000 |
| `balance_krw` | NUMBER | KRW 환산 잔고 | 500000000 |
| `exchange_rate` | NUMBER | 적용 환율 | 1.0 |

---

### 4️⃣ **Sales_Pipeline** (영업 파이프라인)

진행 중인 영업 기회를 추적하는 탭입니다.

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| `opportunity_id` | TEXT | 기회 고유 ID | OPP-2024-001 |
| `client_name` | TEXT | 고객명 | LG Electronics |
| `project_name` | TEXT | 프로젝트명 | Q2 Brand Video |
| `country` | TEXT | 국가 | Korea |
| `team` | TEXT | 담당 팀 | Video Production |
| `stage` | TEXT | 단계 | Proposal, Contract, Payment Pending, Closed Won, Closed Lost |
| `probability` | NUMBER | 성공 확률 (%) | 70 |
| `amount_original` | NUMBER | 예상 금액 | 80000000 |
| `currency` | TEXT | 통화 | KRW |
| `amount_krw` | NUMBER | KRW 환산 금액 | 80000000 |
| `expected_close_date` | DATE | 예상 계약일 | 2024-03-15 |
| `expected_payment_date` | DATE | 예상 입금일 | 2024-04-15 |
| `created_date` | DATE | 생성일 | 2024-01-10 |
| `last_updated` | DATE | 최종 업데이트 | 2024-02-01 |
| `notes` | TEXT | 비고 | Decision maker meeting scheduled |

---

### 5️⃣ **Headcount** (인력 현황)

직원 정보를 추적하는 탭입니다.

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| `employee_id` | TEXT | 직원 ID | EMP-001 |
| `name` | TEXT | 이름 | 홍길동 |
| `country` | TEXT | 근무 국가 | Korea |
| `team` | TEXT | 소속 팀 | Video Production |
| `role` | TEXT | 직책 | Senior Editor |
| `employment_type` | TEXT | 고용 형태 | Full-time, Part-time, Contractor |
| `join_date` | DATE | 입사일 | 2023-01-15 |
| `leave_date` | DATE | 퇴사일 (해당시) | - |
| `monthly_salary_krw` | NUMBER | 월급 (KRW) | 5000000 |
| `status` | TEXT | 상태 | Active, Inactive |

---

### 6️⃣ **Budget** (예산 계획)

월별 예산 목표를 설정하는 탭입니다.

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| `year` | NUMBER | 연도 | 2024 |
| `month` | NUMBER | 월 | 1 |
| `country` | TEXT | 국가 | Korea |
| `team` | TEXT | 팀 | Video Production |
| `revenue_target_krw` | NUMBER | 매출 목표 | 200000000 |
| `expense_budget_krw` | NUMBER | 비용 예산 | 150000000 |
| `profit_target_krw` | NUMBER | 이익 목표 | 50000000 |

---

### 7️⃣ **Exchange_Rates** (환율 데이터)

월별 환율을 기록하는 탭입니다.

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| `date` | DATE | 기준일 | 2024-01-31 |
| `usd_to_krw` | NUMBER | USD → KRW | 1300 |
| `vnd_to_krw` | NUMBER | VND → KRW | 0.055 |

---

### 8️⃣ **PL_Monthly** (월별 손익계산서 집계)

이 탭은 RAW 데이터로부터 자동으로 계산되거나, 수동으로 집계할 수 있습니다.

| 컬럼명 | 설명 |
|--------|------|
| `year_month` | 연월 (2024-01) |
| `country` | 국가 |
| `team` | 팀 |
| `revenue_krw` | 매출 |
| `cogs_krw` | 매출원가 |
| `gross_profit_krw` | 매출총이익 |
| `gross_margin_pct` | 매출총이익률 (%) |
| `operating_expense_krw` | 영업비용 |
| `ebitda_krw` | EBITDA |
| `ebitda_margin_pct` | EBITDA 마진 (%) |
| `net_profit_krw` | 순이익 |
| `net_margin_pct` | 순이익률 (%) |

---

## 🎯 데이터 입력 가이드

1. **RAW_Revenue, RAW_Expense**: 거래가 발생할 때마다 **행 단위로 추가**
2. **RAW_Cash**: 매월 말일 또는 주간 단위로 **잔고 스냅샷 기록**
3. **Sales_Pipeline**: 영업 기회 발생 시 추가, 진행 상황에 따라 `stage` 업데이트
4. **Headcount**: 입사/퇴사 시 업데이트
5. **Budget**: 연초 또는 분기 초에 목표 설정
6. **Exchange_Rates**: 매월 말일 환율 기록 (또는 주간)
7. **PL_Monthly**: 대시보드에서 자동 계산하거나, 구글 시트에서 PIVOT/QUERY 함수로 집계

---

## 🔗 데이터 연결 방식

초기 단계에서는 **더미 데이터**를 Python 코드 내에서 생성하고,
이후 아래 방법 중 하나로 실제 구글 시트와 연결합니다:

1. **CSV Export 방식** (가장 간단)
   - 구글 시트를 "웹에 게시" → CSV 링크 생성
   - `pd.read_csv(url)` 으로 읽기

2. **Google Sheets API** (권장)
   - 서비스 계정 생성 → JSON 키 다운로드
   - `gspread` 라이브러리 사용

3. **수동 다운로드**
   - 로컬에서 CSV 파일을 주기적으로 다운로드하여 사용
