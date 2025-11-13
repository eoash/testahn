# 구글 시트 연결 가이드

## 🎯 개요

현재 `dashboard.py`는 더미 데이터를 사용하고 있습니다.
실제 구글 시트의 데이터를 연결하려면 아래 방법 중 하나를 선택하세요.

---

## 방법 1: CSV Export 방식 (가장 간단) ⭐ 추천

### 장점
- 구글 계정 인증 불필요
- 설정이 매우 간단
- 실시간 업데이트 가능 (시트 수정 시 자동 반영)

### 단점
- 시트를 "웹에 게시"해야 하므로 민감한 데이터는 부적합
- 읽기 전용 (대시보드에서 데이터 수정 불가)

### 📋 단계별 가이드

#### 1단계: 구글 시트 준비

1. 구글 시트를 열고 `SCHEMA_DESIGN.md`에 정의된 대로 탭을 생성합니다:
   - `RAW_Revenue`
   - `RAW_Expense`
   - `RAW_Cash`
   - `Sales_Pipeline`
   - `Headcount`
   - (선택) `Budget`, `Exchange_Rates`, `PL_Monthly`

2. 각 탭에 컬럼 헤더를 추가합니다 (예: `RAW_Revenue` 탭):
   ```
   transaction_id | date | country | team | client_name | project_name | amount_original | currency | amount_krw | payment_status | ...
   ```

3. 샘플 데이터를 몇 개 입력합니다.

#### 2단계: 웹에 게시

각 탭마다 다음 작업을 수행합니다:

1. 해당 탭을 선택합니다 (예: `RAW_Revenue`)
2. **파일 > 공유 > 웹에 게시** 클릭
3. **게시할 항목**: 해당 탭 선택 (예: `RAW_Revenue`)
4. **형식**: `쉼표로 구분된 값(.csv)` 선택
5. **게시** 버튼 클릭
6. **생성된 URL을 복사**합니다 (예: `https://docs.google.com/spreadsheets/d/e/.../pub?gid=...&single=true&output=csv`)

#### 3단계: 코드 수정

`dashboard.py`의 `load_fake_data()` 함수를 아래와 같이 교체합니다:

```python
import pandas as pd
import streamlit as st

# 구글 시트 CSV URL (각 탭별로 웹에 게시한 URL)
SHEET_URLS = {
    'revenue': 'https://docs.google.com/spreadsheets/d/e/.../pub?gid=...&single=true&output=csv',
    'expense': 'https://docs.google.com/spreadsheets/d/e/.../pub?gid=...&single=true&output=csv',
    'cash': 'https://docs.google.com/spreadsheets/d/e/.../pub?gid=...&single=true&output=csv',
    'pipeline': 'https://docs.google.com/spreadsheets/d/e/.../pub?gid=...&single=true&output=csv',
    'headcount': 'https://docs.google.com/spreadsheets/d/e/.../pub?gid=...&single=true&output=csv'
}

@st.cache_data(ttl=300)  # 5분마다 캐시 갱신
def load_data_from_google_sheets():
    """
    구글 시트에서 데이터 로드 (CSV Export 방식)
    """
    try:
        # Revenue 데이터
        df_revenue = pd.read_csv(SHEET_URLS['revenue'])
        df_revenue['date'] = pd.to_datetime(df_revenue['date'])

        # Expense 데이터
        df_expense = pd.read_csv(SHEET_URLS['expense'])
        df_expense['date'] = pd.to_datetime(df_expense['date'])

        # Cash 데이터
        df_cash = pd.read_csv(SHEET_URLS['cash'])
        df_cash['date'] = pd.to_datetime(df_cash['date'])

        # Pipeline 데이터
        df_pipeline = pd.read_csv(SHEET_URLS['pipeline'])
        df_pipeline['expected_close_date'] = pd.to_datetime(df_pipeline['expected_close_date'])

        # Headcount 데이터
        df_headcount = pd.read_csv(SHEET_URLS['headcount'])

        return {
            'revenue': df_revenue,
            'expense': df_expense,
            'cash': df_cash,
            'pipeline': df_pipeline,
            'headcount': df_headcount
        }
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None
```

#### 4단계: 함수 호출 변경

`dashboard.py`에서 데이터 로드 부분을 다음과 같이 변경:

```python
# 기존 코드:
# data = load_fake_data()

# 새로운 코드:
data = load_data_from_google_sheets()

if data is None:
    st.stop()  # 데이터 로드 실패 시 중단
```

#### 5단계: 테스트

터미널에서 실행:
```bash
streamlit run dashboard.py
```

브라우저에서 대시보드가 구글 시트 데이터로 표시되는지 확인합니다.

---

## 방법 2: Google Sheets API (권장 - 보안 필요 시) 🔒

### 장점
- 시트를 공개하지 않아도 됨 (비공개 유지 가능)
- 읽기/쓰기 모두 가능
- 더 많은 기능 활용 가능

### 단점
- 초기 설정이 복잡함
- 서비스 계정 생성 및 권한 설정 필요

### 📋 단계별 가이드

#### 1단계: Google Cloud 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 (예: `eo-studio-finance`)
3. **API 및 서비스 > 라이브러리** 메뉴로 이동
4. 다음 API를 검색하여 **사용 설정**:
   - Google Sheets API
   - Google Drive API

#### 2단계: 서비스 계정 생성

1. **API 및 서비스 > 사용자 인증 정보** 메뉴로 이동
2. **사용자 인증 정보 만들기 > 서비스 계정** 클릭
3. 서비스 계정 이름 입력 (예: `finance-dashboard`)
4. **역할**: `편집자` 선택
5. **완료** 클릭

#### 3단계: JSON 키 다운로드

1. 생성된 서비스 계정을 클릭
2. **키** 탭으로 이동
3. **키 추가 > 새 키 만들기** 클릭
4. **JSON** 형식 선택 후 **만들기**
5. JSON 파일이 자동 다운로드됩니다 (예: `eo-studio-finance-xxxxx.json`)
6. 이 파일을 프로젝트 디렉토리에 저장 (예: `credentials.json`)

⚠️ **보안 주의**: 이 파일은 절대 git에 커밋하지 마세요! `.gitignore`에 추가하세요.

#### 4단계: 구글 시트 권한 부여

1. JSON 파일을 열어 `client_email` 값을 복사합니다:
   ```json
   {
     "client_email": "finance-dashboard@eo-studio-finance.iam.gserviceaccount.com",
     ...
   }
   ```

2. 구글 시트를 열고 **공유** 버튼 클릭
3. 복사한 이메일 주소를 입력하고 **편집자** 권한 부여

#### 5단계: 라이브러리 설치

터미널에서 실행:
```bash
pip install gspread oauth2client
```

#### 6단계: 코드 수정

`dashboard.py`에 다음 코드를 추가:

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets 설정
SPREADSHEET_ID = '여기에_시트_ID_입력'  # URL에서 복사: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
CREDENTIALS_FILE = 'credentials.json'  # 다운로드한 JSON 파일 경로

@st.cache_data(ttl=300)
def load_data_from_google_sheets_api():
    """
    Google Sheets API를 사용하여 데이터 로드
    """
    try:
        # 인증
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)

        # 스프레드시트 열기
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        # 각 탭에서 데이터 읽기
        df_revenue = pd.DataFrame(spreadsheet.worksheet('RAW_Revenue').get_all_records())
        df_revenue['date'] = pd.to_datetime(df_revenue['date'])

        df_expense = pd.DataFrame(spreadsheet.worksheet('RAW_Expense').get_all_records())
        df_expense['date'] = pd.to_datetime(df_expense['date'])

        df_cash = pd.DataFrame(spreadsheet.worksheet('RAW_Cash').get_all_records())
        df_cash['date'] = pd.to_datetime(df_cash['date'])

        df_pipeline = pd.DataFrame(spreadsheet.worksheet('Sales_Pipeline').get_all_records())
        df_pipeline['expected_close_date'] = pd.to_datetime(df_pipeline['expected_close_date'])

        df_headcount = pd.DataFrame(spreadsheet.worksheet('Headcount').get_all_records())

        return {
            'revenue': df_revenue,
            'expense': df_expense,
            'cash': df_cash,
            'pipeline': df_pipeline,
            'headcount': df_headcount
        }
    except Exception as e:
        st.error(f"Google Sheets API 오류: {e}")
        return None
```

#### 7단계: 함수 호출 변경

```python
# 기존 코드:
# data = load_fake_data()

# 새로운 코드:
data = load_data_from_google_sheets_api()

if data is None:
    st.stop()
```

#### 8단계: .gitignore 업데이트

프로젝트 루트에 `.gitignore` 파일 생성 또는 업데이트:
```
credentials.json
*.json
__pycache__/
.streamlit/
```

---

## 방법 3: 로컬 CSV 파일 (오프라인)

### 장점
- 인터넷 연결 불필요
- 가장 빠른 성능

### 단점
- 수동 업데이트 필요
- 자동화 어려움

### 📋 단계별 가이드

#### 1단계: CSV 파일 다운로드

1. 구글 시트에서 각 탭을 CSV로 다운로드:
   - **파일 > 다운로드 > 쉼표로 구분된 값(.csv, 현재 시트)**

2. 다운로드한 파일들을 프로젝트의 `data/` 폴더에 저장:
   ```
   data/
   ├── RAW_Revenue.csv
   ├── RAW_Expense.csv
   ├── RAW_Cash.csv
   ├── Sales_Pipeline.csv
   └── Headcount.csv
   ```

#### 2단계: 코드 수정

```python
import os

DATA_DIR = 'data'

@st.cache_data
def load_data_from_local_csv():
    """
    로컬 CSV 파일에서 데이터 로드
    """
    try:
        df_revenue = pd.read_csv(os.path.join(DATA_DIR, 'RAW_Revenue.csv'))
        df_revenue['date'] = pd.to_datetime(df_revenue['date'])

        df_expense = pd.read_csv(os.path.join(DATA_DIR, 'RAW_Expense.csv'))
        df_expense['date'] = pd.to_datetime(df_expense['date'])

        df_cash = pd.read_csv(os.path.join(DATA_DIR, 'RAW_Cash.csv'))
        df_cash['date'] = pd.to_datetime(df_cash['date'])

        df_pipeline = pd.read_csv(os.path.join(DATA_DIR, 'Sales_Pipeline.csv'))
        df_pipeline['expected_close_date'] = pd.to_datetime(df_pipeline['expected_close_date'])

        df_headcount = pd.read_csv(os.path.join(DATA_DIR, 'Headcount.csv'))

        return {
            'revenue': df_revenue,
            'expense': df_expense,
            'cash': df_cash,
            'pipeline': df_pipeline,
            'headcount': df_headcount
        }
    except Exception as e:
        st.error(f"CSV 파일 로드 실패: {e}")
        return None

# 사용
data = load_data_from_local_csv()
```

---

## 🔄 어떤 방법을 선택해야 할까요?

| 상황 | 추천 방법 |
|------|-----------|
| **빠르게 테스트하고 싶어요** | ⭐ 방법 1: CSV Export |
| **민감한 데이터를 다룹니다** | 🔒 방법 2: Google Sheets API |
| **인터넷이 없는 환경입니다** | 📁 방법 3: 로컬 CSV |
| **실시간 협업이 중요합니다** | ⭐ 방법 1 또는 🔒 방법 2 |
| **데이터를 대시보드에서 수정하고 싶어요** | 🔒 방법 2: Google Sheets API |

---

## 🚀 다음 단계

1. 선택한 방법으로 구글 시트 연결 완료
2. 실제 데이터를 시트에 입력
3. 대시보드에서 데이터 확인
4. 필요시 차트나 KPI 커스터마이징
5. 팀원들과 공유

---

## 🛠️ 트러블슈팅

### 문제 1: "데이터 로드 실패" 오류

**원인**: CSV URL이 잘못되었거나, 시트가 게시되지 않음

**해결**:
- URL을 다시 확인
- 시트를 "웹에 게시" 했는지 확인
- 브라우저에서 URL을 직접 열어서 CSV가 다운로드되는지 테스트

### 문제 2: "Google Sheets API 오류"

**원인**: 인증 실패 또는 권한 부족

**해결**:
- `credentials.json` 파일 경로 확인
- 서비스 계정 이메일이 시트에 공유되었는지 확인
- Google Sheets API가 활성화되었는지 확인

### 문제 3: 날짜 형식 오류

**원인**: 구글 시트의 날짜 형식이 Python과 호환되지 않음

**해결**:
- 구글 시트에서 날짜를 `YYYY-MM-DD` 형식으로 통일
- 코드에서 날짜 파싱 시 `format` 매개변수 추가:
  ```python
  df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
  ```

### 문제 4: 데이터가 업데이트되지 않음

**원인**: Streamlit 캐시 때문에 이전 데이터가 표시됨

**해결**:
- 브라우저에서 `C` 키를 눌러 캐시 클리어
- 또는 `@st.cache_data(ttl=60)` 에서 TTL 값을 줄임

---

## 📞 도움이 필요하세요?

- Streamlit 공식 문서: https://docs.streamlit.io
- Google Sheets API 문서: https://developers.google.com/sheets/api
- gspread 라이브러리 문서: https://docs.gspread.org

---

**작성자**: Claude (EO Studio CFO Dashboard 프로젝트)
**최종 업데이트**: 2024년 11월
