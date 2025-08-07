import customtkinter as ctk
from tkinter import messagebox
from CTkScrollableDropdown import CTkScrollableDropdown
import config


class TargetVarScreen:
    def __init__(self):
        pass

    #Step 2: Selecting the target variable
    #This function is used to select the target variable from the dataframe
    #################################################################################################################################### 
    def step_2_select_target_variable(self):

        
        config.current_step = "step 2"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()
        
        #loading frame to show while the section is being created
        #this is done to avoid flickering of the screen/ delay
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(pady=40)

        #creating a frame for the entire dataframe section
        entire_targetvar_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_targetvar_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_targetvar_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button to return to Step 1
        from screens.df_preview_screen import DFPreviewScreen
        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=lambda: DFPreviewScreen().show_dataframe(config.df))
        back_button.pack(side="left", padx=10)

        #label for Step 2
        heading_label = ctk.CTkLabel(top_frame, text="Step 2: Select Target Variable", font=("Arial", 16, "bold"))
        heading_label.pack(side="left", expand=True)

        #next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_targetvar_section, fg_color="gray10")
        middle_frame.pack(pady=30)

        #dropdown selection for the target variable
        dropdown_frame = ctk.CTkFrame(middle_frame, fg_color="gray10")
        dropdown_frame.pack(pady=50)

        ctk.CTkLabel(dropdown_frame, text="Select Target Variable:", font=("Arial", 16), text_color="white").pack(side="left", padx=10)

        values=list(config.df.columns)
        target_variable = ctk.StringVar()
        target_dropdown = ctk.CTkComboBox(dropdown_frame, variable=target_variable, state="readonly", corner_radius=30, font=("Arial", 14), justify="center", width=180)
        target_dropdown.pack(side="left")

        #attaching the scrollable dropdown to the combo box
        CTkScrollableDropdown(target_dropdown, values=values, justify="left", button_color="transparent")

        #adjusting the internal entry’s grid padding
        target_dropdown._entry.grid_configure(padx=(10,45))

        #function to store selection when "Next" is clicked
        def save_selected_target_var():

            from screens.input_var_screen import InputVarScreen

            config.selected_target_variable = target_variable.get()

            if not config.selected_target_variable:
                #showing an error message if next button clicked without selecting a target variable
                messagebox.showerror("Error", "Please select a target variable!")
                return
            
            #printting the selected target variable for debugging
            print(f"Selected Target Variable: {config.selected_target_variable}")
            InputVarScreen().step_3_select_input_variables()

        next_button.configure(command=save_selected_target_var)

        

        def handle_answer(answer: str):

            print("UneeSeek says:", answer)

            #stoping and hiding the progress bar
            progress_bar.stop()
            progress_bar.pack_forget()

            #showing the AI response in a label
            response = f"UneeSeek: {answer}"
            response_lable = ctk.CTkLabel(middle_frame, text="", text_color="#3a7ebf", wraplength=500, font=("Arial", 14), justify="left")

            response_lable.pack(side="bottom", pady=10)
            
            from model.chat_bot import ChatBot
            ChatBot().animate_text(response_lable, response, delay=30)


            #enabling the back and next buttons after the AI response
            back_button.configure(state="normal")
            next_button.configure(state="normal")


        progress_bar = ctk.CTkProgressBar(middle_frame, mode="indeterminate", width=100)

        def prompt():

            #showing the progress bar while waiting for the AI response
            ai_button.pack_forget()
            progress_bar.pack(side="bottom", pady=10)
            progress_bar.start()

            #disabling the back and next buttons while waiting for the AI response
            back_button.configure(state="disabled")
            next_button.configure(state="disabled")

            #prompting the AI to answer the question
            config.chat_bot.ask(
                "You are a concise assistant. Never reveal your chain-of-thought—"
                "only output the single-sentence answer for someone with no coding knowledge.\n\n"
                "Why do we need to select a target variable for machine learning?\n\n", 
                handle_answer
            )

        #Ask ai button
        ai_button = ctk.CTkButton(middle_frame, text="Why?, Ask UneeSeek AI", font=("Arial", 14), command=lambda: prompt())
        ai_button.pack(side="bottom", pady=10)

        #forget
        loading_frame.pack_forget()
        #showing the entire section after all the widgets are created
        entire_targetvar_section.pack(fill="both", expand=True)
    #################################################################################################################################### 
