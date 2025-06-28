import threading
from llama_cpp import Llama
import config

class ChatBot:
    
    #converting the gguf model to a class so that it can be used in multiple screens without loading it again and again
    
    def __init__(self):
        path    = "model/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf"
        threads = 4

        #loading the model
        self.llm  = Llama(model_path=path, n_threads=threads)
        self.lock = threading.Lock()

    def ask(self, prompt: str, callback):
        
        #worker function to run in a separate thread
        def _worker():

            #getting the token count of the prompt by geting the token ids and counting them
            token_ids = self.llm.tokenize(prompt.encode("utf-8"))
            prompt_token_count = len(token_ids)

            #setting the maximum tokens for the response maximum token minus the prompt token count
            max_tokens = 131072 - prompt_token_count
            with self.lock:
                resp   = self.llm(prompt, max_tokens=max_tokens, temperature=0.0, stop=["\n"])
                answer = resp['choices'][0]['text'].strip()

            #going back to the main thread to update the UI
            config.main_window.after(0, lambda: callback(answer))

        threading.Thread(target=_worker, daemon=True).start()
