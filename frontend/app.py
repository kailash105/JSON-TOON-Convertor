import streamlit as st
import requests
import json
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="LLM Prompt Optimizer", layout="wide")

st.title("🧠 LLM Prompt Optimizer")
st.caption("Convert JSON prompts into TOON format and save real money 💸")

# --- Backend URL ---
BACKEND_URL = "http://127.0.0.1:8000/optimize"

# --- Accurate OpenAI Pricing (per 1K tokens) ---
PRICING = {
    "gpt-4o": 0.0025,
    "gpt-4o-mini": 0.00015,
    "gpt-3.5-turbo": 0.0005
}

# --- Model Selector ---
model = st.selectbox(
    "Select model for cost estimation:",
    ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
    index=1
)

# --- Input Section ---
st.subheader("Input JSON")
json_input = st.text_area(
    "Paste your JSON data here 👇",
    value=json.dumps(
        {
            "data": {
                "products": [
                    {"id": 1, "name": "Laptop", "price": 1200},
                    {"id": 2, "name": "Mouse", "price": 25}
                ]
            }
        },
        indent=2
    ),
    height=250
)

# --- Optimize Button ---
if st.button("🚀 Optimize"):
    try:
        json_data = json.loads(json_input)

        with st.spinner("Optimizing your prompt... 🧩"):
            response = requests.post(BACKEND_URL, json={"data": json_data})


        if response.status_code == 200:
            result = response.json()
            st.success("✅ Optimization Successful!")

            # --- Accurate Pricing ---
            rate_per_1k = PRICING[model]
            json_cost = round(result["json_tokens"] / 1000 * rate_per_1k, 6)
            toon_cost = round(result["toon_tokens"] / 1000 * rate_per_1k, 6)
            savings_percent = round((1 - toon_cost / json_cost) * 100, 2) if json_cost > 0 else 0

            # --- Metrics ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("JSON Tokens", result["json_tokens"])
            with col2:
                st.metric("TOON Tokens", result["toon_tokens"])
            with col3:
                st.metric("Savings (%)", savings_percent)

            st.write("---")

            # --- Chart ---
            if result["json_tokens"] > 0 and result["toon_tokens"] > 0:
                chart_data = pd.DataFrame({
                    "Type": ["JSON", "TOON"],
                    "Tokens": [result["json_tokens"], result["toon_tokens"]]
                })
                st.subheader("📊 Token Comparison")
                st.bar_chart(chart_data.set_index("Type"))
            else:
                st.warning("⚠️ Chart skipped: token values not valid.")

            st.write("---")

            # --- Cost Comparison ---
            st.subheader("💰 Cost Comparison")
            st.write(f"**Model:** `{model}`")
            st.write(f"**JSON Cost:** ${json_cost}")
            st.write(f"**TOON Cost:** ${toon_cost}")
            st.write(f"**Estimated Savings:** ${round(json_cost - toon_cost, 6)} per prompt")

            st.write("---")

            # --- TOON Output ---
            st.subheader("🧾 TOON Output")
            st.code(result["toon_output"], language="yaml")

            # --- Download Button ---
            st.download_button(
                label="⬇️ Download TOON File",
                data=result["toon_output"],
                file_name="optimized_prompt.toon",
                mime="text/plain"
            )

        else:
            st.error(f"Error: {response.text}")

    except Exception as e:
        st.error(f"⚠️ Invalid JSON or connection error: {e}")
