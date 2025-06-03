FROM python:3.12.10-bullseye

WORKDIR /app

# システム依存関係
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションをコピー
COPY . .

# 非rootユーザーで実行
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app


# Railway用の起動コマンド
CMD ["sh", "-c", "python app.py"]