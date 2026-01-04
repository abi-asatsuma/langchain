from transformers import AutoTokenizer, AutoModelForCausalLM

# Llama 3.2 3Bモデルをダウンロード
model_name = "meta-llama/Llama-3.2-3B-Instruct"
print("ダウンロード中...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# ローカルに保存
tokenizer.save_pretrained("./llama-japanese")
model.save_pretrained("./llama-japanese")
print("ダウンロード完了！")
