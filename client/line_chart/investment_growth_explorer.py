import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv('portfolio_optimization_results.csv')
st.title("💼 Investment Growth Explorer")

# Sidebar inputs
st.sidebar.header("Your Investment Inputs")

# Mappings
regime_map = {0: "Bear", 1: "Neutral", 2: "Bull"}
risk_map = {'risk_averse': 'Conservative', 'risk_neutral': 'Moderate', 'risk_loving': 'Aggressive'}
duration_map = {63: "3 Months", 126: "6 Months", 252: "1 Year"}
# Reverse mappings for filtering
reverse_regime_map = {v: k for k, v in regime_map.items()}
reverse_risk_map = {v: k for k, v in risk_map.items()}
reverse_duration_map = {v: k for k, v in duration_map.items()}

# Display options in readable form
regimes = sorted([regime_map[r] for r in df['regime'].unique()])
risks = sorted([risk_map[r] for r in df['risk_appetite'].unique()])
durations = sorted([duration_map[d] for d in df['holding_duration'].unique()])

regime_label = st.sidebar.selectbox("Market Regime/Conditions", regimes)
risk_label = st.sidebar.selectbox("Risk Appetite", risks)
duration_label = st.sidebar.selectbox("Holding Period", durations)
initial_cash = st.sidebar.number_input("Initial Investment ($)", min_value=1000, value=10000, step=500)

# Convert back to original values for filtering
regime = reverse_regime_map[regime_label]
risk = reverse_risk_map[risk_label]
holding_days = reverse_duration_map[duration_label]

# Filter for matching portfolio
match = df[
    (df['regime'] == regime) &
    (df['risk_appetite'] == risk) &
    (df['holding_duration'] == holding_days)
]

##need to add line chart
if match.empty:
    st.warning("No matching portfolio found.")
else:
    row = match.iloc[0]
    expected_return = row['expected_return']
    projected_value = initial_cash * (1 + expected_return)

    st.markdown("### 📊 Results")
    st.write(f"**Expected Return:** {expected_return:.2%}")
    st.write(f"**Projected Portfolio Value:** ${projected_value:,.2f}")

    st.caption(f"""
    - Expected return is based on a {duration_label} holding period.
    - This is a simple projection, not compounded over time.
    """)
