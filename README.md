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

## ライセンス
MIT
