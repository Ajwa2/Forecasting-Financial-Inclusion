"""Streamlit dashboard app for Task 5.

Run locally:

    pip install -r requirements.txt streamlit plotly
    streamlit run dashboard/app.py

"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


@st.cache_data
def load_forecasts():
    p = Path('reports/forecasts_task4.csv')
    if not p.exists():
        st.error('Forecasts file not found. Run notebooks/task4_forecast.ipynb or task4_forecast.py first.')
        return pd.DataFrame()
    return pd.read_csv(p)


def overview_page(fore):
    st.title('Financial Inclusion — Overview')
    st.markdown('Key metrics and trend highlights')
    cols = st.columns(3)
    # show latest baseline for each series
    for i, s in enumerate(fore['series'].unique()):
        df_s = fore[fore['series'] == s]
        latest = df_s.sort_values('year').iloc[-1]
        cols[i].metric(label=s, value=f"{latest['baseline']:.1f}%")


def trends_page(fore):
    st.header('Trends')
    series = st.multiselect('Select series', options=fore['series'].unique().tolist(), default=fore['series'].unique().tolist())
    dfp = fore[fore['series'].isin(series)]
    fig = go.Figure()
    for s in dfp['series'].unique():
        d = dfp[dfp['series'] == s]
        fig.add_trace(go.Scatter(x=d['year'], y=d['baseline'], mode='lines+markers', name=s))
    st.plotly_chart(fig, use_container_width=True)


def forecasts_page(fore):
    st.header('Forecasts')
    model = st.selectbox('Model selection (prototype)', options=['logit-linear (baseline)'])
    series = st.selectbox('Series', options=fore['series'].unique())
    d = fore[fore['series'] == series]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d['year'], y=d['baseline'], mode='lines+markers', name='Baseline'))
    fig.add_trace(go.Scatter(x=d['year'].tolist()+d['year'][::-1].tolist(), y=(d['ci95_high'].tolist()+d['ci95_low'][::-1].tolist()), fill='toself', name='95% CI', opacity=0.2, showlegend=True))
    st.plotly_chart(fig, use_container_width=True)
    st.download_button('Download forecasts CSV', data=d.to_csv(index=False), file_name=f'forecasts_{series.replace(" ","_")}.csv')


def inclusion_page(fore):
    st.header('Inclusion Projections')
    series = 'Account Ownership Rate'
    d = fore[fore['series'] == series]
    target = st.slider('Target (%)', min_value=10, max_value=100, value=60)
    st.metric('Target', f'{target}%')
    latest = d[d['year'] == d['year'].min()].iloc[0]
    st.markdown(f"Latest baseline forecast: {d['baseline'].iloc[0]:.1f}%")
    fig = px.line(d, x='year', y='baseline', title=f'Progress toward {target}% target')
    fig.add_hline(y=target, line_dash='dash', annotation_text=f'{target}% target')
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.set_page_config(layout='wide')
    fore = load_forecasts()
    if fore.empty:
        return
    page = st.sidebar.selectbox('Page', ['Overview', 'Trends', 'Forecasts', 'Inclusion Projections'])
    if page == 'Overview':
        overview_page(fore)
    elif page == 'Trends':
        trends_page(fore)
    elif page == 'Forecasts':
        forecasts_page(fore)
    else:
        inclusion_page(fore)


if __name__ == '__main__':
    main()
"""
Dashboard application for Financial Inclusion Forecasting
"""

def main():
    """Main entry point for the dashboard"""
    print("Dashboard application - to be implemented")
    pass

if __name__ == "__main__":
    main()
