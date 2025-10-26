import customtkinter as ctk
import config



class MainMenuScreen:
    
    def __init__(self):
        pass

    #Method for main menu
    def main_menu(self):
        from screens.import_screen import ImportScreen
        #Buttons
        build_model_button = ctk.CTkButton(config.main_window, text="Build a Model", font=("Arial", 14), command=lambda: ImportScreen().show_import_screen(), width=200, height=50)
        build_model_button.pack(pady=(250,30))

        test_model_button = ctk.CTkButton(config.main_window, text="Test a Model", font=("Arial", 14), command=None, width=200, height=50)
        test_model_button.pack(pady=10)


    def back_to_main_menu(self):
        #removing all widgets from the window
        for widget in config.main_window.winfo_children():
            widget.destroy()
        
        #showing the main menu
        self.main_menu()
