import threading
from llama_cpp import Llama
import config
import customtkinter as ctk

class ChatBot:
    
    #converting the gguf model to a class so that it can be used in multiple screens without loading it again and again
    
    def __init__(self):
        path    = "model/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf"
        threads = 4

        #loading the model
        self.llm  = Llama(model_path=path, n_threads=threads, verbose=False)
        self.lock = threading.Lock()

    #function to animate the text in a label
    #this will reveal one character at a time to create a typing effect
    def animate_text(self, label: ctk.CTkLabel, full_text: str, delay: int = 30, index: int = 0):
            
            
            if index <= len(full_text):
                label.configure(text=full_text[:index])
                #scheduling the next character
                #this will call the animate_text function again after the delay
                label.after(delay, self.animate_text, label, full_text, delay, index + 1)

    #funtion to ask a question to the LLM
    def ask(self, prompt: str, callback, stop: list[str] | None = None):
        
        if stop is None:
            stop = ["\n\n"]

        #worker function to run in a separate thread
        def worker():

            #getting the token count of the prompt by geting the token ids and counting them
            token_ids = self.llm.tokenize(prompt.encode("utf-8"))
            prompt_token_count = len(token_ids)

            #setting the maximum tokens for the response maximum token minus the prompt token count
            max_tokens = 131072 - prompt_token_count
            with self.lock:
                resp   = self.llm(prompt, max_tokens=max_tokens, temperature=0.0, stop=stop)
                answer = resp['choices'][0]['text'].strip()

            #going back to the main thread to update the UI
            config.main_window.after(0, lambda: callback(answer))

        threading.Thread(target=worker, daemon=True).start()
    
    def close(self):
        #close the LLM connection
        try:
            self.llm.close()
            print("ChatBot connection closed.")
        except Exception:
            pass

        #setting the llm to None to free up memory
        self.llm = None
