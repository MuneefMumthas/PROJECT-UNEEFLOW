import customtkinter as ctk
import config
from PIL import Image, ImageTk



class MainMenuScreen:
    
    def __init__(self):
        pass

    #Method for main menu
    def main_menu(self):

        #main frame
        main_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        main_frame.pack(fill="both", expand=True)

        from screens.import_screen import ImportScreen
        #Buttons
        build_model_button = ctk.CTkButton(main_frame, text="Build a Model", font=("Arial", 14), command=lambda: ImportScreen().show_import_screen(), width=200, height=50)
        build_model_button.pack(pady=(250,0))

        build_hint = ctk.CTkLabel(main_frame, text="Start a new ML workflow", font=("Arial", 11), text_color="gray60")
        build_hint.pack(pady=(0,30))

        from screens.model_test_screen import ModelTestScreen

        test_model_button = ctk.CTkButton(main_frame, text="Test a Model", font=("Arial", 14), command=lambda: ModelTestScreen().show_model_test_screen(), width=200, height=50)
        test_model_button.pack(pady=(10, 0))

        test_hint = ctk.CTkLabel(main_frame, text="Predict using a pretrained UneeFlow model", font=("Arial", 11), text_color="gray60")
        test_hint.pack(pady=(0,0))

        footer = ctk.CTkLabel(main_frame, text="© 2025 UNEEFLOW - v1.0", font=("Arial", 11), text_color="gray60")
        footer.pack(side="bottom", pady=15)

    def back_to_main_menu(self):
        #removing all widgets from the window
        for widget in config.main_window.winfo_children():
            widget.destroy()
        
        #showing the main menu
        self.main_menu()
