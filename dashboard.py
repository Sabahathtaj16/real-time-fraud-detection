import streamlit as st
import pandas as pd
import json
import time
import altair as alt

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")
st.title(" Real-Time Fraud Detection Dashboard")

placeholder = st.empty()

while True:
    try:
        with open('dashboard_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    if data:
        df = pd.DataFrame(data)

        total = len(df)
        frauds = df[df['is_fraud'] == 1]
        legitimate = df[df['is_fraud'] == 0]

        with placeholder.container():
            st.metric("Total Transactions", total)
            st.metric("Fraudulent", len(frauds))
            st.metric("Legitimate", len(legitimate))

            st.dataframe(df[::-1])  # Show latest transactions first

            # Create histograms for fraud vs legitimate
            df['label'] = df['is_fraud'].map({0: 'Legitimate', 1: 'Fraudulent'})

            chart = alt.Chart(df).mark_bar(opacity=0.7).encode(
                x=alt.X('label:N', title='Transaction Type'),
                y=alt.Y('count()', title='Count'),
                color=alt.Color('label:N',
                    scale=alt.Scale(
                        domain=['Fraudulent', 'Legitimate'],
                        range=['lightcoral', 'lightgreen']
                    ),
                    legend=None
                )
            ).properties(
                title="Transaction Distribution"
            )

            st.altair_chart(chart, use_container_width=True)

    else:
        st.info("No transactions yet...")

    time.sleep(5)  # Refresh every 5 seconds
