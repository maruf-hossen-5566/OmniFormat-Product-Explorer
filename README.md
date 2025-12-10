# 🛒 OmniFormat Product Explorer

A streamlined product-exploration tool built with **Streamlit + Selenium**, allowing you to search Amazon products and view results in multiple formats — **cards, tables, JSON, or structured text**.

This project is optimized for **Railway deployment**, includes **Docker support**, and uses **uv** for ultra-fast Python dependency management.

---

## 📌 Features

- 🔍 Amazon product search using headless or headful Selenium  
- 🧩 Modular scraper architecture (scraper + parser separation)  
- 🖥️ Clean Streamlit UI  
- 📄 View results as Cards, Tables, JSON, or Structured Text  
- 🧹 Built-in logging with rotating file handlers  
- ⚡ Ultra-fast dependency management with **uv**
- 🐳 Docker support  

---

## 📂 Project Structure

```
OmniFormat-Product-Explorer/
│
├── main.py # Streamlit entry point
├── logger.py # Logging setup
│
├── ui/
│ ├── app.py # Main UI
│ ├── components.py # Reusable UI components
│ └── init.py
│
├── scraper/
│ ├── scraper.py # Selenium scraping logic
│ ├── driver.py # Driver setup
│ ├── proxy.py # Proxy setup
│ ├── parser.py # HTML/JSON parsing
│ └── utils.py 
│
├── Dockerfile
├── pyproject.toml # Managed by uv
└── uv.lock
```

---

## 🚀 Getting Started (Local)

### 1️⃣ Clone the Repo
```
git clone https://github.com/maruf-hossen-5566/OmniFormat-Product-Explorer.git
cd OmniFormat-Product-Explorer
```

### 2️⃣ Install Dependencies (using uv)

```
uv sync
```

### Or create a fresh environment:

```
uv venv
source .venv/bin/activate
uv sync
```

---

### ▶️ Run the App
```
streamlit run main.py
```

---

### 🐳 Running with Docker


#### Build:
```
docker build -t omniformat .
```

#### Run:
```
docker run -p 8501:8501 omniformat
```

---

## 🧠 How It Works

1. User enters a query

2. Selenium fetcher loads Amazon page

3. Parser extracts product details

4. UI renders data in whichever format the user selects


---

## 🌐 Deploying on Railway

Just push to GitHub → Create new Railway project → Point to main.py.

No Chrome install required — the app uses headless mode.

---

## ⭐ Support

If you find this useful, please ⭐ star the repo!