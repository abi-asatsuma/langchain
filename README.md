# LangChain + Ollama チェーン最小サンプル

## 概要
LangChainとOllamaを使った、最小限のLLMチェーンサンプルです。

## 使い方
1. Ollamaをインストールし、llama3モデルをpullしてください。
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3:8b
   ```
2. 依存パッケージをインストール
   ```bash
   pip install -r requirements.txt
   ```
3. スクリプトを実行
   ```bash
   python langchain_sample01.py
   ```
## main起動
Ollamaサーバーを起動
1. Python仮想環境の準備・依存パッケージのインストール
 - 仮想環境を有効化
 ```
 source .venv/bin/activate
 ```
2. FastAPIサーバーの起動
プロジェクトルートで
```
uvicorn langchainapp.main:api --reload
```

## ライセンス
MIT
