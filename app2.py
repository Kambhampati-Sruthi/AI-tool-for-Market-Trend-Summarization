import streamlit as st
import pandas as pd
import json
import re
import matplotlib.pyplot as plt
from openai import OpenAI
import os

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="AI tool for Market Trend Summarization", layout="wide")

# ----------------- CSS -----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #e0f7fa, #fef3c7); }
h1, h2, h3 { color: #1e3a8a; font-weight: 700; }
.card { background: rgba(255,255,255,0.95); padding: 24px; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); margin-bottom: 20px; }
.trend-positive { color: #16a34a; font-size: 20px; font-weight: 700; }
.trend-negative { color: #dc2626; font-size: 20px; font-weight: 700; }
.trend-neutral { color: #ca8a04; font-size: 20px; font-weight: 700; }
.stButton button { background: linear-gradient(to right, #2563eb, #7c3aed); color: white; font-weight: 600; border-radius: 12px; padding: 10px 22px; border: none; }
.stButton button:hover { background: linear-gradient(to right, #1e40af, #6d28d9); }
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------- TITLE -----------------
st.title("📊 Market Trend Summarization")
st.write("Upload data or paste market info to generate insights and visualizations.")

# ----------------- INPUT -----------------
input_method = st.radio("Input Type", ["Upload CSV/TXT", "Paste Text"], horizontal=True)
raw_text = ""

if input_method == "Upload CSV/TXT":
    uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "txt"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.success("Dataset loaded")
            st.dataframe(df.head())
            raw_text = df.to_string(index=False)
        else:
            raw_text = uploaded_file.read().decode("utf-8")
            st.success("Text file loaded")
else:
    raw_text = st.text_area("Paste your market data", height=150, placeholder="Q1 $120,000 | Q2 $135,000 | Q3 $160,000 | Q4 $180,000")

analyze_btn = st.button("✨ Generate Insights")

# ----------------- HELPER -----------------
def extract_sales(text):
    return [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", text)]

def analyze_market(text):
    # Using OpenAI API instead of Ollama
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    prompt = f"""
    You are a market analyst. Summarize the following data and provide:
    1. Summary
    2. Trend (positive, negative, neutral)
    3. Key drivers (list)
    4. Potential risks (list)
    Data: {text}
    Respond in JSON format like:
    {{ "summary": "...", "trend": "...", "drivers": [...], "risks": [...] }}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ----------------- OUTPUT -----------------
if analyze_btn and raw_text.strip():
    with st.spinner("Analyzing..."):
        try:
            result = analyze_market(raw_text)
            data = json.loads(result)
        except Exception as e:
            st.error("Failed to process AI response.")
            st.text(result)
            data = {}

    if data:
        sales = extract_sales(raw_text)
        quarters = [f"Q{i+1}" for i in range(len(sales))]

        # ---------- SUMMARY & TREND ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🧠 Market Summary")
        st.write(data.get("summary", "No summary available."))

        trend = data.get("trend","neutral").lower()
        if trend in ["positive", "increasing", "bullish"]:
            st.markdown('<div class="trend-positive">⬆ Market is trending upward</div>', unsafe_allow_html=True)
        elif trend in ["negative", "decreasing", "bearish"]:
            st.markdown('<div class="trend-negative">⬇ Market is trending downward</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="trend-neutral">➖ Market is stable</div>', unsafe_allow_html=True)

        # Optional: Drivers
        drivers = data.get("drivers", [])
        if drivers:
            st.write("**Key Drivers:**")
            for d in drivers:
                st.info(d)
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- VISUALIZATIONS ----------
        if len(sales) >= 2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Sales Visualizations")
            df_chart = pd.DataFrame({"Quarter": quarters, "Sales": sales})

            col1, col2 = st.columns(2)
            with col1:
                st.line_chart(df_chart.set_index("Quarter"))
            with col2:
                fig, ax = plt.subplots()
                ax.pie(sales, labels=quarters, autopct="%1.1f%%", startangle=90, colors=['#2563eb','#38bdf8','#22c55e','#facc15'])
                ax.axis("equal")
                st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- RISKS ----------
        risks = data.get("risks", [])
        if risks:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("⚠ Potential Risks")
            for r in risks:
                st.warning(r)
            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- DOWNLOAD REPORT ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📥 Export Analysis")
        report = {
            "trend": data.get("trend"),
            "summary": data.get("summary"),
            "drivers": drivers,
            "risks": risks,
            "sales": sales
        }
        st.download_button("Download JSON Report", json.dumps(report, indent=2), file_name="market_analysis.json", mime="application/json")
        st.markdown('</div>', unsafe_allow_html=True)

elif analyze_btn:
    st.warning("Please provide data before analyzing.")
