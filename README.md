# 📈 AI Tool for Market Trend Summarization

An intelligent, Streamlit-powered web application designed to process market research data, extract key sales figures, perform trend analysis, and generate structured insights using local LLMs (via Ollama) or built-in analytics.

🌐 **Live Application:** [AI Market Trend Summarizer on Streamlit](https://ai-tool-for-market-trend-summarization.streamlit.app/)

---

## 🚀 Key Features

* **Cloud & Local Deployment:** Access the live web tool instantly via [Streamlit Cloud](https://ai-tool-for-market-trend-summarization.streamlit.app/) or run locally with Ollama integration (`aicrue:latest` model).
* **Interactive UI & Custom Styling:** Built with **Streamlit** featuring custom gradients, metric status cards, and responsive layouts (`app2.py`).
* **Multi-Format Data Input:** Accept raw market text snippets directly or upload structured datasets (`.csv` and `.txt` files).
* **Data Visualization:** Automatically parses sales metrics using regular expressions to plot interactive line charts and Matplotlib percentage distribution pie charts.
* **Structured JSON Reporting:** Standardized output parsing for market trends, key drivers, potential risks, and summary breakdowns with a one-click JSON export feature.
* **Modular Prompt Management:** Centralized prompt templates (`prompts.py`) tailored for chunk-based market sentiment and final strategy synthesis.

---

## 📂 Project Structure
'''text
AI-tool-for-Market-Trend-Summarization/
│
├── analyzer.py        # Core local LLM execution script (Ollama integration & JSON parsing)
├── app2.py            # Streamlit frontend, visualization logic, and UI components
├── prompts.py         # Prompt engineering templates (chunk and final analysis prompts)
└── requirements.txt   # Project python dependencies
'''
🛠️ Tech Stack
Language: Python

Web Framework: Streamlit

Data Processing: Pandas, NumPy

Visualization: Matplotlib, Streamlit native charts

AI Engine: Ollama (local model inference)

⚙️ Installation & Setup
1. Clone the Repository
git clone [https://github.com/Kambhampati-Sruthi/AI-tool-for-Market-Trend-Summarization.git](https://github.com/Kambhampati-Sruthi/AI-tool-for-Market-Trend-Summarization.git)
cd AI-tool-for-Market-Trend-Summarization
2. Create and Activate a Virtual Environment
Bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Setup Local AI Model (Optional for Ollama execution)
Ensure Ollama is installed and running locally, and pull the required model specified in analyzer.py:

Bash
ollama pull aicrue:latest
🚀 Running the Application
Launch the Streamlit app locally by executing:

Bash
https://ai-tool-for-market-trend-summarization.streamlit.app/
Open your browser and navigate to the local link provided in your terminal (typically http://localhost:8501).

💡 Usage Guide
Select Input Method: Choose between uploading a dataset (.csv / .txt) or pasting raw market text/sales data directly into the text area.

Generate Insights: Click the ✨ Generate Insights button to process the data.

Review Visuals & Summaries: Inspect the generated market summary, trend direction (Positive/Negative/Neutral), key drivers, potential risks, and visual charts.

Export Report: Download the final output instantly as a structured .json report file.
