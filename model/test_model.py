from llama_cpp import Llama

model = "model/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf"

llm = Llama(model_path=model, n_threads=4)

# Run a quick prompt
prompt = (
    "You are a concise assistant. Never reveal your chain-of-thought—"
    "only output the single-sentence answer for someone with no coding knowledge.\n\n"
    "Why is selecting input variables necessary for a machine learning model?\n"
    
)

token_ids = llm.tokenize(prompt.encode("utf-8"))

prompt_token_count = len(token_ids)

max_tokens = 131072 - prompt_token_count


resp = llm(prompt, max_tokens=max_tokens, temperature=0.0, stop=["\n"])

full = resp['choices'][0]['text']
#answer = next(line for line in full.splitlines() if line.strip())

# Print out the model’s suggestion
print("AI Decide suggestion:\n", full)