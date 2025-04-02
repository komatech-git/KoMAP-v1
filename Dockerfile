# ベースイメージの設定
FROM python:3.12

# Pythonの標準出力のバッファリングを解除して、出力を即座に表示できるよう設定
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリをappに設定
WORKDIR /app

# Node.js のインストール
# 以下の手順で Node.js をインストールします
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    node -v && npm -v


# pipの最新バージョンにアップグレード
RUN pip install --upgrade pip

# 依存関係のインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# npm install の実行
COPY theme/static_src/package*.json /app/theme/static_src/
WORKDIR /app/theme/static_src
RUN npm install

# 作業ディレクトリを元に戻して、コードを最終にコピー
WORKDIR /app 
COPY . /app/