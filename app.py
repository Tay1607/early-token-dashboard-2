import streamlit as st
import pandas as pd
from utils import get_pairs

st.set_page_config(page_title="Early Token Dashboard", page_icon="🚀")
st.title("🚀 Early Token Dashboard")

@st.cache_data(ttl=300)
def fetch_pairs():
    return get_pairs()

# Første load
if "pairs" not in st.session_state:
    st.session_state.pairs = fetch_pairs()

# Opdater-knap
if st.button("🔄 Opdater data"):
    st.session_state.pairs = fetch_pairs()
    st.success("Data opdateret")

pairs = st.session_state.pairs

# Visning
if not pairs:
    st.warning("Ingen data hentet endnu.")
else:
    df = pd.DataFrame(pairs)
    # Pænere kolonnenavne
    df = df.rename(columns={
        "pairAddress": "Pair",
        "baseSymbol": "Base",
        "quoteSymbol": "Quote",
        "priceUsd": "Price (USD)",
        "liquidityUsd": "Liquidity (USD)",
        "dexId": "DEX",
        "chainId": "Chain",
    })
    # Sortér efter likviditet hvis tal findes
    with st.expander("Filtre", expanded=False):
        min_liq = st.number_input("Minimum liquidity (USD)", min_value=0, value=0, step=1000)
    def to_float(x):
        try:
            return float(x)
        except Exception:
            return None
    if "Liquidity (USD)" in df.columns:
        df["Liquidity_num"] = df["Liquidity (USD)"].map(to_float)
        df = df[df["Liquidity_num"].fillna(0) >= min_liq].drop(columns=["Liquidity_num"])

    st.dataframe(df, use_container_width=True)
    st.metric("Antal par", len(df))
