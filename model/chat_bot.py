import threading
from llama_cpp import Llama
import config
import customtkinter as ctk
import os

class ChatBot:
    
    
    
    #converting the gguf model to a class so that it can be used in multiple screens without loading it again and again
    
    def __init__(self):
        if hasattr(self, 'initialized') and self.initialized:
            return
        
        path    = "model/Phi-3.5-mini-instruct-Q4_K_M.gguf"
        threads = max(2, (os.cpu_count() or 6) - 4)

        #loading the model
        self.llm  = Llama(model_path=path, n_threads=threads, verbose=False, n_ctx=4096, n_batch=512)
        self.lock = threading.Lock()

        self.initialized = True

    # #function to animate the text in a label
    # #this will reveal one character at a time to create a typing effect
    def animate_text(self, label: ctk.CTkLabel, full_text: str, delay: int = 30, index: int = 0):
            
        if index <= len(full_text):
            label.configure(text=full_text[:index])
            #scheduling the next character
            #this will call the animate_text function again after the delay
            label.after(delay, self.animate_text, label, full_text, delay, index + 1)

    #funtion to ask a question to the LLM
    def ask(self, prompt: str, label: ctk.CTkLabel, progress_bar:ctk.CTkProgressBar, back_btn: ctk.CTkButton, next_btn: ctk.CTkButton ,stop: list[str] | None = None):
        
        if stop is None:
            stop = ["\n\n"]

        #worker function to run in a separate thread
        def worker():

            text_buffer = []
            started = False

            with self.lock:

                for chunk in self.llm(prompt, max_tokens=512, temperature=0.0, stop=stop, stream=True):
                    text = chunk['choices'][0].get('text', '')
                    if text:
                        if not started:
                            started = True
                            if progress_bar is not None:
                                #stopping and hiding the progress bar when the first text chunk is received
                                config.main_window.after(0, lambda: progress_bar.stop())
                                config.main_window.after(10, lambda: progress_bar.pack_forget())
            
                        text_buffer.append(text)
                        current_text = ''.join(text_buffer)
                        
                        #using the streaming text update to show the text as it is being generated
                        config.main_window.after(0, lambda t=current_text: label.configure(text=f"UneePhi: {t}"))

                #using animate_text to reveal the full text with typing effect
                # if progress_bar is not None:
                #     config.main_window.after(0, lambda: progress_bar.stop())
                #     config.main_window.after(10, lambda: progress_bar.pack_forget())

                # config.main_window.after(0, lambda t=current_text: self.animate_text(label, f"UneeSeek: {t}"))

                        

            #re enabling the buttons after the response is complete
            if back_btn is not None and next_btn is not None:

                config.main_window.after(0, lambda: (
                    back_btn.configure(state="normal"),
                    next_btn.configure(state="normal")
                ))

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
