"""
EO Studio CFO Dashboard
재무 데이터 시각화 대시보드

실행 방법:
streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ================================
# 페이지 설정
# ================================
st.set_page_config(
    page_title="EO Studio CFO Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# 더미 데이터 생성 함수
# 나중에 구글 시트 연결 시 이 함수만 교체하면 됩니다
# ================================

@st.cache_data
def load_fake_data():
    """
    더미 데이터 생성
    실제 환경에서는 이 함수를 구글 시트 또는 CSV에서 읽어오는 함수로 교체
    """
    np.random.seed(42)

    # 날짜 범위 생성 (2023년 1월 ~ 2024년 10월)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 10, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    countries = ['Korea', 'USA', 'Vietnam']
    teams = ['Video Production', 'Branded Content', 'EO School']

    # ============ RAW_Revenue 데이터 생성 ============
    revenue_data = []
    for i in range(500):  # 500개의 매출 거래
        date = np.random.choice(date_range)
        country = np.random.choice(countries, p=[0.5, 0.3, 0.2])
        team = np.random.choice(teams)

        # 국가별 금액 범위 조정
        if country == 'Korea':
            amount = np.random.randint(10_000_000, 100_000_000)
            currency = 'KRW'
            amount_krw = amount
        elif country == 'USA':
            amount = np.random.randint(10_000, 80_000)
            currency = 'USD'
            amount_krw = amount * 1300
        else:  # Vietnam
            amount = np.random.randint(200_000_000, 1_500_000_000)
            currency = 'VND'
            amount_krw = amount * 0.055

        payment_status = np.random.choice(['Paid', 'Pending', 'Overdue'], p=[0.7, 0.2, 0.1])

        revenue_data.append({
            'transaction_id': f'REV-{i+1:04d}',
            'date': date,
            'country': country,
            'team': team,
            'client_name': f'Client {np.random.randint(1, 50)}',
            'project_name': f'Project {np.random.randint(1, 100)}',
            'amount_original': amount,
            'currency': currency,
            'amount_krw': amount_krw,
            'payment_status': payment_status,
            'category': np.random.choice(['Retainer', 'Project-based', 'License'])
        })

    df_revenue = pd.DataFrame(revenue_data)
    df_revenue['date'] = pd.to_datetime(df_revenue['date'])

    # ============ RAW_Expense 데이터 생성 ============
    expense_data = []
    categories_l1 = ['Personnel', 'Marketing', 'Operations', 'COGS']

    for i in range(800):  # 800개의 비용 거래
        date = np.random.choice(date_range)
        country = np.random.choice(countries, p=[0.5, 0.3, 0.2])
        team = np.random.choice(teams + ['Admin'])
        category_l1 = np.random.choice(categories_l1, p=[0.5, 0.15, 0.2, 0.15])

        # 비용 카테고리별 금액 범위
        if category_l1 == 'Personnel':
            amount = np.random.randint(3_000_000, 15_000_000)
        elif category_l1 == 'Marketing':
            amount = np.random.randint(500_000, 10_000_000)
        elif category_l1 == 'COGS':
            amount = np.random.randint(1_000_000, 20_000_000)
        else:
            amount = np.random.randint(500_000, 5_000_000)

        expense_data.append({
            'expense_id': f'EXP-{i+1:04d}',
            'date': date,
            'country': country,
            'team': team,
            'category_l1': category_l1,
            'category_l2': f'{category_l1}_sub',
            'vendor': f'Vendor {np.random.randint(1, 30)}',
            'description': f'Expense description {i+1}',
            'amount_krw': amount,
            'currency': 'KRW'
        })

    df_expense = pd.DataFrame(expense_data)
    df_expense['date'] = pd.to_datetime(df_expense['date'])

    # ============ Cash 데이터 생성 ============
    cash_data = []
    cash_dates = pd.date_range(start='2023-01-31', end='2024-10-31', freq='M')

    for date in cash_dates:
        for country in countries:
            balance = np.random.randint(100_000_000, 800_000_000)
            cash_data.append({
                'date': date,
                'country': country,
                'balance_krw': balance
            })

    df_cash = pd.DataFrame(cash_data)
    df_cash['date'] = pd.to_datetime(df_cash['date'])

    # ============ Sales Pipeline 데이터 생성 ============
    pipeline_data = []
    stages = ['Proposal', 'Contract', 'Payment Pending', 'Closed Won']

    for i in range(50):
        country = np.random.choice(countries)
        team = np.random.choice(teams)
        stage = np.random.choice(stages)

        amount = np.random.randint(20_000_000, 150_000_000)
        probability = {
            'Proposal': np.random.randint(20, 50),
            'Contract': np.random.randint(60, 80),
            'Payment Pending': np.random.randint(80, 95),
            'Closed Won': 100
        }[stage]

        pipeline_data.append({
            'opportunity_id': f'OPP-{i+1:04d}',
            'client_name': f'Prospect {i+1}',
            'project_name': f'Opportunity {i+1}',
            'country': country,
            'team': team,
            'stage': stage,
            'probability': probability,
            'amount_krw': amount,
            'expected_close_date': datetime.now() + timedelta(days=np.random.randint(30, 180))
        })

    df_pipeline = pd.DataFrame(pipeline_data)

    # ============ Headcount 데이터 생성 ============
    headcount_data = []
    for i in range(50):
        country = np.random.choice(countries, p=[0.5, 0.3, 0.2])
        team = np.random.choice(teams + ['Admin'])

        headcount_data.append({
            'employee_id': f'EMP-{i+1:03d}',
            'name': f'Employee {i+1}',
            'country': country,
            'team': team,
            'role': np.random.choice(['Junior', 'Senior', 'Lead', 'Manager']),
            'monthly_salary_krw': np.random.randint(3_000_000, 12_000_000),
            'status': 'Active'
        })

    df_headcount = pd.DataFrame(headcount_data)

    return {
        'revenue': df_revenue,
        'expense': df_expense,
        'cash': df_cash,
        'pipeline': df_pipeline,
        'headcount': df_headcount
    }

# ================================
# 데이터 로드
# ================================
data = load_fake_data()
df_revenue = data['revenue']
df_expense = data['expense']
df_cash = data['cash']
df_pipeline = data['pipeline']
df_headcount = data['headcount']

# ================================
# 사이드바 - 필터
# ================================
st.sidebar.title("🎛️ 필터 설정")

# 날짜 범위 필터
min_date = min(df_revenue['date'].min(), df_expense['date'].min())
max_date = max(df_revenue['date'].max(), df_expense['date'].max())

date_range = st.sidebar.date_input(
    "기간 선택",
    value=(min_date, max_date),
    min_value=min_date.date(),
    max_value=max_date.date()
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df_revenue_filtered = df_revenue[(df_revenue['date'] >= pd.Timestamp(start_date)) &
                                      (df_revenue['date'] <= pd.Timestamp(end_date))]
    df_expense_filtered = df_expense[(df_expense['date'] >= pd.Timestamp(start_date)) &
                                      (df_expense['date'] <= pd.Timestamp(end_date))]
else:
    df_revenue_filtered = df_revenue
    df_expense_filtered = df_expense

# 국가 필터
countries = st.sidebar.multiselect(
    "국가 선택",
    options=df_revenue['country'].unique(),
    default=df_revenue['country'].unique()
)

if countries:
    df_revenue_filtered = df_revenue_filtered[df_revenue_filtered['country'].isin(countries)]
    df_expense_filtered = df_expense_filtered[df_expense_filtered['country'].isin(countries)]

# 팀 필터
teams = st.sidebar.multiselect(
    "팀 선택",
    options=df_revenue['team'].unique(),
    default=df_revenue['team'].unique()
)

if teams:
    df_revenue_filtered = df_revenue_filtered[df_revenue_filtered['team'].isin(teams)]

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: 필터를 조정하여 원하는 데이터를 확인하세요.")

# ================================
# 메인 대시보드
# ================================

st.title("📊 EO Studio CFO Dashboard")
st.markdown("### 실시간 재무 및 경영 지표")

# ================================
# 1. 상단 KPI 카드
# ================================
st.markdown("---")
st.subheader("🎯 핵심 KPI")

# 계산
total_revenue = df_revenue_filtered['amount_krw'].sum()
total_expense = df_expense_filtered['amount_krw'].sum()
net_profit = total_revenue - total_expense
profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0

# 현금 잔고 (최신)
latest_cash_date = df_cash['date'].max()
latest_cash = df_cash[df_cash['date'] == latest_cash_date]['balance_krw'].sum()

# 인원 수
total_headcount = len(df_headcount[df_headcount['status'] == 'Active'])
per_capita_revenue = total_revenue / total_headcount if total_headcount > 0 else 0

# KPI 카드 표시
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 총 매출",
        value=f"₩{total_revenue/1e8:.1f}억",
        delta=f"{(total_revenue/1e8):.1f}억 (선택 기간)"
    )

with col2:
    st.metric(
        label="💸 총 비용",
        value=f"₩{total_expense/1e8:.1f}억",
        delta=f"-{(total_expense/1e8):.1f}억"
    )

with col3:
    st.metric(
        label="📈 순이익",
        value=f"₩{net_profit/1e8:.1f}억",
        delta=f"{profit_margin:.1f}% 마진"
    )

with col4:
    st.metric(
        label="🏦 현금 잔고",
        value=f"₩{latest_cash/1e8:.1f}억",
        delta=f"{latest_cash_date.strftime('%Y-%m-%d')} 기준"
    )

with col5:
    st.metric(
        label="👥 인당 매출",
        value=f"₩{per_capita_revenue/1e7:.1f}천만",
        delta=f"{total_headcount}명"
    )

# ================================
# 2. Cash & Runway
# ================================
st.markdown("---")
st.subheader("💵 Cash Flow & Runway")

col1, col2 = st.columns(2)

with col1:
    # 월별 Cash Flow
    df_revenue_monthly = df_revenue_filtered.copy()
    df_revenue_monthly['year_month'] = df_revenue_monthly['date'].dt.to_period('M')
    revenue_monthly = df_revenue_monthly.groupby('year_month')['amount_krw'].sum().reset_index()
    revenue_monthly['year_month'] = revenue_monthly['year_month'].astype(str)

    df_expense_monthly = df_expense_filtered.copy()
    df_expense_monthly['year_month'] = df_expense_monthly['date'].dt.to_period('M')
    expense_monthly = df_expense_monthly.groupby('year_month')['amount_krw'].sum().reset_index()
    expense_monthly['year_month'] = expense_monthly['year_month'].astype(str)

    # 합치기
    cashflow_monthly = pd.merge(revenue_monthly, expense_monthly, on='year_month', how='outer', suffixes=('_rev', '_exp'))
    cashflow_monthly = cashflow_monthly.fillna(0)
    cashflow_monthly['net_cashflow'] = cashflow_monthly['amount_krw_rev'] - cashflow_monthly['amount_krw_exp']

    fig_cashflow = go.Figure()
    fig_cashflow.add_trace(go.Bar(
        x=cashflow_monthly['year_month'],
        y=cashflow_monthly['amount_krw_rev'] / 1e8,
        name='매출',
        marker_color='#28a745'
    ))
    fig_cashflow.add_trace(go.Bar(
        x=cashflow_monthly['year_month'],
        y=-cashflow_monthly['amount_krw_exp'] / 1e8,
        name='비용',
        marker_color='#dc3545'
    ))
    fig_cashflow.add_trace(go.Scatter(
        x=cashflow_monthly['year_month'],
        y=cashflow_monthly['net_cashflow'] / 1e8,
        name='순 Cash Flow',
        mode='lines+markers',
        line=dict(color='#007bff', width=3),
        yaxis='y2'
    ))

    fig_cashflow.update_layout(
        title="월별 Cash Flow",
        xaxis_title="월",
        yaxis_title="금액 (억 원)",
        yaxis2=dict(
            title="순 Cash Flow (억 원)",
            overlaying='y',
            side='right'
        ),
        barmode='relative',
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig_cashflow, use_container_width=True)

with col2:
    # Runway 계산
    avg_monthly_expense = df_expense_monthly.groupby('year_month')['amount_krw'].sum().mean()
    runway_months = latest_cash / avg_monthly_expense if avg_monthly_expense > 0 else 0

    # Runway 게이지 차트
    fig_runway = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=runway_months,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Runway (개월)", 'font': {'size': 24}},
        delta={'reference': 12, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 24], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 6], 'color': '#ffcccc'},
                {'range': [6, 12], 'color': '#ffffcc'},
                {'range': [12, 24], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 6
            }
        }
    ))

    fig_runway.update_layout(height=400)
    st.plotly_chart(fig_runway, use_container_width=True)

    st.info(f"""
    **💡 Runway 분석:**
    - 현재 현금: ₩{latest_cash/1e8:.1f}억
    - 월평균 Burn Rate: ₩{avg_monthly_expense/1e8:.1f}억
    - 예상 Runway: **{runway_months:.1f}개월**
    """)

# ================================
# 3. Revenue 분석
# ================================
st.markdown("---")
st.subheader("💵 Revenue 분석")

tab1, tab2, tab3 = st.tabs(["📈 추이 분석", "🌍 국가별", "👥 팀별"])

with tab1:
    # 월별 매출 추이 (국가별)
    df_rev_country = df_revenue_filtered.copy()
    df_rev_country['year_month'] = df_rev_country['date'].dt.to_period('M').astype(str)
    rev_country_monthly = df_rev_country.groupby(['year_month', 'country'])['amount_krw'].sum().reset_index()

    fig_rev_trend = px.line(
        rev_country_monthly,
        x='year_month',
        y='amount_krw',
        color='country',
        markers=True,
        title="국가별 월간 매출 추이",
        labels={'amount_krw': '매출 (원)', 'year_month': '월', 'country': '국가'}
    )
    fig_rev_trend.update_yaxis(tickformat=".2s")
    fig_rev_trend.update_layout(height=450)
    st.plotly_chart(fig_rev_trend, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        # 국가별 매출 합계 (파이 차트)
        rev_by_country = df_revenue_filtered.groupby('country')['amount_krw'].sum().reset_index()
        fig_country_pie = px.pie(
            rev_by_country,
            values='amount_krw',
            names='country',
            title="국가별 매출 비중",
            hole=0.4
        )
        fig_country_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_country_pie, use_container_width=True)

    with col2:
        # 국가별 매출 합계 (바 차트)
        fig_country_bar = px.bar(
            rev_by_country,
            x='country',
            y='amount_krw',
            title="국가별 매출 합계",
            labels={'amount_krw': '매출 (원)', 'country': '국가'},
            text='amount_krw'
        )
        fig_country_bar.update_traces(texttemplate='₩%{text:.2s}', textposition='outside')
        fig_country_bar.update_yaxis(tickformat=".2s")
        st.plotly_chart(fig_country_bar, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)

    with col1:
        # 팀별 매출 합계
        rev_by_team = df_revenue_filtered.groupby('team')['amount_krw'].sum().reset_index()
        fig_team_bar = px.bar(
            rev_by_team,
            x='team',
            y='amount_krw',
            title="팀별 매출 합계",
            labels={'amount_krw': '매출 (원)', 'team': '팀'},
            text='amount_krw',
            color='team'
        )
        fig_team_bar.update_traces(texttemplate='₩%{text:.2s}', textposition='outside')
        fig_team_bar.update_yaxis(tickformat=".2s")
        st.plotly_chart(fig_team_bar, use_container_width=True)

    with col2:
        # 팀별 월간 매출 추이
        df_rev_team = df_revenue_filtered.copy()
        df_rev_team['year_month'] = df_rev_team['date'].dt.to_period('M').astype(str)
        rev_team_monthly = df_rev_team.groupby(['year_month', 'team'])['amount_krw'].sum().reset_index()

        fig_team_trend = px.line(
            rev_team_monthly,
            x='year_month',
            y='amount_krw',
            color='team',
            markers=True,
            title="팀별 월간 매출 추이",
            labels={'amount_krw': '매출 (원)', 'year_month': '월', 'team': '팀'}
        )
        fig_team_trend.update_yaxis(tickformat=".2s")
        st.plotly_chart(fig_team_trend, use_container_width=True)

# ================================
# 4. Expense 분석
# ================================
st.markdown("---")
st.subheader("💸 Expense 분석")

col1, col2 = st.columns(2)

with col1:
    # 비용 카테고리별 합계
    exp_by_category = df_expense_filtered.groupby('category_l1')['amount_krw'].sum().reset_index()
    exp_by_category = exp_by_category.sort_values('amount_krw', ascending=False)

    fig_exp_category = px.bar(
        exp_by_category,
        x='category_l1',
        y='amount_krw',
        title="비용 카테고리별 합계",
        labels={'amount_krw': '비용 (원)', 'category_l1': '카테고리'},
        text='amount_krw',
        color='category_l1'
    )
    fig_exp_category.update_traces(texttemplate='₩%{text:.2s}', textposition='outside')
    fig_exp_category.update_yaxis(tickformat=".2s")
    st.plotly_chart(fig_exp_category, use_container_width=True)

with col2:
    # 비용 카테고리별 비중 (파이 차트)
    fig_exp_pie = px.pie(
        exp_by_category,
        values='amount_krw',
        names='category_l1',
        title="비용 카테고리별 비중",
        hole=0.4
    )
    fig_exp_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_exp_pie, use_container_width=True)

# 월별 비용 추이
df_exp_monthly = df_expense_filtered.copy()
df_exp_monthly['year_month'] = df_exp_monthly['date'].dt.to_period('M').astype(str)
exp_monthly = df_exp_monthly.groupby(['year_month', 'category_l1'])['amount_krw'].sum().reset_index()

fig_exp_trend = px.area(
    exp_monthly,
    x='year_month',
    y='amount_krw',
    color='category_l1',
    title="월별 비용 카테고리별 추이 (Stacked Area)",
    labels={'amount_krw': '비용 (원)', 'year_month': '월', 'category_l1': '카테고리'}
)
fig_exp_trend.update_yaxis(tickformat=".2s")
fig_exp_trend.update_layout(height=450)
st.plotly_chart(fig_exp_trend, use_container_width=True)

# ================================
# 5. P&L 요약
# ================================
st.markdown("---")
st.subheader("📊 손익계산서 (P&L) 요약")

# 월별 P&L 계산
df_rev_pl = df_revenue_filtered.copy()
df_rev_pl['year_month'] = df_rev_pl['date'].dt.to_period('M').astype(str)
pl_revenue = df_rev_pl.groupby('year_month')['amount_krw'].sum().reset_index()
pl_revenue.columns = ['year_month', 'revenue']

df_exp_pl = df_expense_filtered.copy()
df_exp_pl['year_month'] = df_exp_pl['date'].dt.to_period('M').astype(str)

# COGS와 Operating Expense 분리
pl_cogs = df_exp_pl[df_exp_pl['category_l1'] == 'COGS'].groupby('year_month')['amount_krw'].sum().reset_index()
pl_cogs.columns = ['year_month', 'cogs']

pl_opex = df_exp_pl[df_exp_pl['category_l1'] != 'COGS'].groupby('year_month')['amount_krw'].sum().reset_index()
pl_opex.columns = ['year_month', 'opex']

# 합치기
pl_summary = pl_revenue.merge(pl_cogs, on='year_month', how='left').merge(pl_opex, on='year_month', how='left')
pl_summary = pl_summary.fillna(0)

pl_summary['gross_profit'] = pl_summary['revenue'] - pl_summary['cogs']
pl_summary['gross_margin_pct'] = (pl_summary['gross_profit'] / pl_summary['revenue'] * 100).round(1)
pl_summary['net_profit'] = pl_summary['revenue'] - pl_summary['cogs'] - pl_summary['opex']
pl_summary['net_margin_pct'] = (pl_summary['net_profit'] / pl_summary['revenue'] * 100).round(1)

# 금액을 억 원 단위로 변환
pl_display = pl_summary.copy()
pl_display['revenue'] = (pl_display['revenue'] / 1e8).round(1)
pl_display['cogs'] = (pl_display['cogs'] / 1e8).round(1)
pl_display['gross_profit'] = (pl_display['gross_profit'] / 1e8).round(1)
pl_display['opex'] = (pl_display['opex'] / 1e8).round(1)
pl_display['net_profit'] = (pl_display['net_profit'] / 1e8).round(1)

pl_display.columns = ['월', '매출 (억)', 'COGS (억)', '매출총이익 (억)', '매출총이익률 (%)', 'OpEx (억)', '순이익 (억)', '순이익률 (%)']

st.dataframe(pl_display, use_container_width=True, height=400)

# 월별 마진율 추이
fig_margin = go.Figure()
fig_margin.add_trace(go.Scatter(
    x=pl_summary['year_month'],
    y=pl_summary['gross_margin_pct'],
    name='매출총이익률 (%)',
    mode='lines+markers',
    line=dict(color='#28a745', width=3)
))
fig_margin.add_trace(go.Scatter(
    x=pl_summary['year_month'],
    y=pl_summary['net_margin_pct'],
    name='순이익률 (%)',
    mode='lines+markers',
    line=dict(color='#007bff', width=3)
))
fig_margin.update_layout(
    title="월별 마진율 추이",
    xaxis_title="월",
    yaxis_title="마진율 (%)",
    hovermode='x unified',
    height=400
)
st.plotly_chart(fig_margin, use_container_width=True)

# ================================
# 6. Sales Pipeline
# ================================
st.markdown("---")
st.subheader("🎯 Sales Pipeline")

col1, col2, col3 = st.columns(3)

with col1:
    total_pipeline_value = df_pipeline['amount_krw'].sum()
    st.metric("총 파이프라인 가치", f"₩{total_pipeline_value/1e8:.1f}억")

with col2:
    weighted_pipeline = (df_pipeline['amount_krw'] * df_pipeline['probability'] / 100).sum()
    st.metric("가중 파이프라인 가치", f"₩{weighted_pipeline/1e8:.1f}억", delta="확률 반영")

with col3:
    closed_won = df_pipeline[df_pipeline['stage'] == 'Closed Won']['amount_krw'].sum()
    st.metric("계약 완료", f"₩{closed_won/1e8:.1f}억")

# Stage별 파이프라인
pipeline_by_stage = df_pipeline.groupby('stage')['amount_krw'].sum().reset_index()
pipeline_by_stage = pipeline_by_stage.sort_values('amount_krw', ascending=True)

fig_pipeline = px.funnel(
    pipeline_by_stage,
    x='amount_krw',
    y='stage',
    title="Sales Pipeline by Stage",
    labels={'amount_krw': '금액 (원)', 'stage': 'Stage'}
)
fig_pipeline.update_traces(texttemplate='₩%{x:.2s}')
st.plotly_chart(fig_pipeline, use_container_width=True)

# 팀별 파이프라인
pipeline_by_team = df_pipeline.groupby('team')['amount_krw'].sum().reset_index()
fig_pipeline_team = px.bar(
    pipeline_by_team,
    x='team',
    y='amount_krw',
    title="팀별 파이프라인 가치",
    labels={'amount_krw': '금액 (원)', 'team': '팀'},
    text='amount_krw',
    color='team'
)
fig_pipeline_team.update_traces(texttemplate='₩%{text:.2s}', textposition='outside')
fig_pipeline_team.update_yaxis(tickformat=".2s")
st.plotly_chart(fig_pipeline_team, use_container_width=True)

# ================================
# 7. Headcount & Productivity
# ================================
st.markdown("---")
st.subheader("👥 인력 & 생산성")

col1, col2 = st.columns(2)

with col1:
    # 국가별 인원
    hc_by_country = df_headcount[df_headcount['status'] == 'Active'].groupby('country').size().reset_index()
    hc_by_country.columns = ['country', 'headcount']

    fig_hc_country = px.bar(
        hc_by_country,
        x='country',
        y='headcount',
        title="국가별 인원",
        labels={'headcount': '인원 수', 'country': '국가'},
        text='headcount',
        color='country'
    )
    fig_hc_country.update_traces(textposition='outside')
    st.plotly_chart(fig_hc_country, use_container_width=True)

with col2:
    # 팀별 인원
    hc_by_team = df_headcount[df_headcount['status'] == 'Active'].groupby('team').size().reset_index()
    hc_by_team.columns = ['team', 'headcount']

    fig_hc_team = px.bar(
        hc_by_team,
        x='team',
        y='headcount',
        title="팀별 인원",
        labels={'headcount': '인원 수', 'team': '팀'},
        text='headcount',
        color='team'
    )
    fig_hc_team.update_traces(textposition='outside')
    st.plotly_chart(fig_hc_team, use_container_width=True)

# 팀별 생산성
team_revenue = df_revenue_filtered.groupby('team')['amount_krw'].sum().reset_index()
team_revenue.columns = ['team', 'revenue']

team_productivity = team_revenue.merge(hc_by_team, on='team', how='left')
team_productivity['per_capita_revenue'] = team_productivity['revenue'] / team_productivity['headcount']
team_productivity = team_productivity.sort_values('per_capita_revenue', ascending=False)

fig_productivity = px.bar(
    team_productivity,
    x='team',
    y='per_capita_revenue',
    title="팀별 인당 매출 (생산성)",
    labels={'per_capita_revenue': '인당 매출 (원)', 'team': '팀'},
    text='per_capita_revenue',
    color='team'
)
fig_productivity.update_traces(texttemplate='₩%{text:.2s}', textposition='outside')
fig_productivity.update_yaxis(tickformat=".2s")
st.plotly_chart(fig_productivity, use_container_width=True)

# ================================
# 8. Risk Management
# ================================
st.markdown("---")
st.subheader("⚠️ Risk Management")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💰 미수금 현황")

    # 미수금 (Pending + Overdue)
    ar_data = df_revenue[df_revenue['payment_status'].isin(['Pending', 'Overdue'])].copy()

    if len(ar_data) > 0:
        ar_total = ar_data['amount_krw'].sum()
        ar_overdue = ar_data[ar_data['payment_status'] == 'Overdue']['amount_krw'].sum()
        ar_pending = ar_data[ar_data['payment_status'] == 'Pending']['amount_krw'].sum()

        st.metric("총 미수금", f"₩{ar_total/1e8:.1f}억")
        st.metric("연체 미수금", f"₩{ar_overdue/1e8:.1f}억", delta="⚠️ 주의 필요")
        st.metric("정상 미수금", f"₩{ar_pending/1e8:.1f}억")

        # 미수금 상태별 차트
        ar_by_status = ar_data.groupby('payment_status')['amount_krw'].sum().reset_index()
        fig_ar = px.pie(
            ar_by_status,
            values='amount_krw',
            names='payment_status',
            title="미수금 상태별 비중",
            hole=0.4,
            color_discrete_map={'Pending': '#ffc107', 'Overdue': '#dc3545'}
        )
        st.plotly_chart(fig_ar, use_container_width=True)
    else:
        st.success("✅ 미수금이 없습니다!")

with col2:
    st.markdown("#### 🏦 현금 분산 (국가별)")

    cash_by_country = df_cash[df_cash['date'] == latest_cash_date].groupby('country')['balance_krw'].sum().reset_index()

    fig_cash_dist = px.pie(
        cash_by_country,
        values='balance_krw',
        names='country',
        title="국가별 현금 보유 비중",
        hole=0.4
    )
    fig_cash_dist.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_cash_dist, use_container_width=True)

    st.dataframe(
        cash_by_country.style.format({'balance_krw': '₩{:,.0f}'}),
        use_container_width=True
    )

# Critical Alerts
st.markdown("#### 🚨 Critical Alerts")

alerts = []

# Runway 체크
if runway_months < 6:
    alerts.append({
        'severity': '🔴 Critical',
        'category': 'Cash',
        'message': f'Runway가 {runway_months:.1f}개월로 6개월 미만입니다. 긴급 자금 확보 필요!'
    })
elif runway_months < 12:
    alerts.append({
        'severity': '🟡 Warning',
        'category': 'Cash',
        'message': f'Runway가 {runway_months:.1f}개월입니다. 자금 계획 검토 권장.'
    })

# 미수금 체크
if len(ar_data) > 0:
    ar_overdue_pct = ar_overdue / total_revenue * 100 if total_revenue > 0 else 0
    if ar_overdue_pct > 10:
        alerts.append({
            'severity': '🔴 Critical',
            'category': 'AR',
            'message': f'연체 미수금이 매출의 {ar_overdue_pct:.1f}%입니다. 회수 조치 필요!'
        })

# 손익 체크
if net_profit < 0:
    alerts.append({
        'severity': '🔴 Critical',
        'category': 'P&L',
        'message': f'선택 기간 동안 순이익이 -₩{abs(net_profit)/1e8:.1f}억으로 적자입니다.'
    })

if len(alerts) > 0:
    df_alerts = pd.DataFrame(alerts)
    st.dataframe(df_alerts, use_container_width=True, hide_index=True)
else:
    st.success("✅ 현재 Critical Alert가 없습니다!")

# ================================
# Footer
# ================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>EO Studio CFO Dashboard v1.0 | 데이터 기준: 더미 데이터 (샘플)</p>
    <p>실제 구글 시트 연결 시 load_fake_data() 함수를 교체하세요.</p>
</div>
""", unsafe_allow_html=True)
