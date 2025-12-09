FROM python:3.11-slim

# Install Chrome (working 2025 method)
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q https://dl.google.com/linux/linux_signing_key.pub -O /usr/share/keyrings/google-linux-signing-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

WORKDIR /app
COPY . .

# Install deps
RUN uv sync --frozen

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
