import os
import pandas as pd
import requests

# CSVファイルを読み込む
csv_input_path = os.path.join(os.path.dirname(__file__), 'input.csv') # カレントディレクトリ取得 + input.csv
df = pd.read_csv(csv_input_path)

def call_chat_api(prompt):
    url = "http://localhost:8000/chat"
    payload = {"message": prompt}
    print(f"送信内容: {payload}")  # 追加
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"API呼び出しエラー: {e}")
        return None

# 各行の'text'カラムをAPIに送り、生成結果を'output'カラムに追加
df["output"] = df["text"].apply(lambda x: call_chat_api(x))

# 結果を新しいCSVに保存
csv_output_path = os.path.join(os.path.dirname(__file__), 'output.csv') # カレントディレクトリ取得 + output.csv
df.to_csv(csv_output_path, index=False)

# データの最初の5行を表示
print(df.head())
