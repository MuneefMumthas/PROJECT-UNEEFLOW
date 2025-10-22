from llama_cpp import Llama
import os

model = "model/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf"

llm = Llama(model_path=model, n_threads=min(max(os.cpu_count() or 4, 4), 16), verbose=True, n_ctx=4096,
    n_batch=512,)

#promt to generate a answer
prompt1 = (
    "You are a concise assistant. Never reveal your chain-of-thought—"
    "only output the single-sentence answer for someone with no coding knowledge.\n\n"
    "Why is selecting input variables necessary for a machine learning model?\n"
    
)

prompt2 = (
    "You are a concise assistant. Never reveal your chain-of-thought—"
    "only output the single-sentence answer for someone with no coding knowledge.\n\n"
    "Why is selecting target variables necessary for a machine learning model?\n"
    
)

#getting the token count of the prompt by geting the token ids and counting them
# token_ids = llm.tokenize(prompt.encode("utf-8"))
# prompt_token_count = len(token_ids)

#setting the maximum tokens for the response maximum token minus the prompt token count
#max_tokens = 131072 - prompt_token_count

def question(prompt):
    response = llm(prompt, max_tokens=128, temperature=0.0, stop=["\n"], stream=True)

    # full = response['choices'][0]['text']
    # #answer = next(line for line in full.splitlines() if line.strip())

    # # Print out the model’s suggestion
    # print("AI Decide suggestion:\n", full)

    full = ""
    print("AI Decide suggestion:\n", end="", flush=True)

    # iterate through streaming chunks
    for chunk in response:
        text = chunk["choices"][0].get("text", "")
        full += text
        print(text, end="", flush=True)


question(prompt1)
question(prompt2)
question(prompt1)
question(prompt2)


