# 📊 CSV Analyst AI

A modern, interactive Retrieval-Augmented Generation (RAG) system designed to analyze and chat with your CSV data. Built with **FastAPI**, **Streamlit**, and powered by **Google Gemini 2.5 Flash**.

![CSV Analyst AI](https://raw.githubusercontent.com/ahmedjaved-hub/CSV-analyst-Rag-System/main/screenshot_placeholder.png) *(Note: Add a real screenshot here)*
`  
## ✨ Features

- **Instant Data Context**: Automatically extracts summary statistics, column types, and sample data to provide context to the LLM.
- **Interactive Visualizations**: Dynamic pie charts for categorical data exploration.
- **AI-Powered Chat**: Ask complex questions about your data and get cited, structured answers.
- **Streaming Responses**: Real-time AI response streaming for a snappy user experience.
- **Premium UI**: Clean, modern interface built with Streamlit and custom CSS.

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python web framework.
- **Frontend**: [Streamlit](https://streamlit.io/) - Fast data app development.
- **LLM**: [Google Gemini 2.5 Flash](https://ai.google.dev/gemini-api) - State-of-the-art AI for data analysis.
- **Data Handling**: [Pandas](https://pandas.pydata.org/) & [Numpy](https://numpy.org/).
- **Visualization**: [Matplotlib](https://matplotlib.org/).

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- A Google Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ahmedjaved-hub/CSV-analyst-Rag-System.git
   cd csv-analyst
   ```

2. **Set up environment variables:**
   Create a `.env` file in the `backend/` directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Install dependencies:**
   Using `uv` (recommended) or `pip`:
   ```bash
   pip install -r requirements.txt
   # OR if you have uv
   uv sync
   ```

### Running the Application

1. **Start the Backend:**
   ```bash
   cd backend
   fastapi dev main.py
   ```
   The backend will run on `http://localhost:8000`.

2. **Start the Frontend:**
   Open a new terminal window:
   ```bash
   cd frontend
   streamlit run app_ui.py
   ```
   The frontend will be accessible at `http://localhost:8501`.

## 📂 Project Structure

```text
csv_analyst/
├── backend/
│   ├── main.py        # FastAPI endpoints (Upload & Chat)
│   ├── rag.py         # CSV context building logic
│   └── .env           # API Keys (gitignored)
├── frontend/
│   └── app_ui.py      # Streamlit interface & visualizations
├── samples/
│   └── dummy.csv      # Sample data for testing
├── pyproject.toml     # Project configuration & dependencies
└── README.md          # You are here!
```

## 📝 How it Works

1. **Upload**: When you upload a CSV, the backend processes it using Pandas.
2. **Contextualize**: The `rag.py` module creates a text representation of the data, including shape, summary stats, and the first 20 rows.
3. **Analyze**: The frontend generates a pie chart for any selected column to give you a quick visual overview.
4. **Chat**: When you ask a question, the backend sends the context + your question to Gemini 2.5 Flash, which generates a response based *only* on your data.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ for data enthusiasts.
