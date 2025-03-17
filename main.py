import tkinter as tk
from tkinter import filedialog, messagebox
import time
from PIL import Image, ImageTk


#Method  to center a window as tkinter does not have a built-in method for this
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_pos = (screen_width - width) // 2
    y_pos = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    window.resizable(False, False)


#creating the main window
root = tk.Tk()
root.title("UNEEFLOW")
center_window(root, 500, 500)

#setting the logo
root.iconbitmap("U Logo.ico")

#Splash Screen- this will act as a loading screen before the main window
##########################################################################################

#hiding the app at the start for the splash screen
root.withdraw()

splash = tk.Toplevel()

#centering the splash window
center_window(splash, 500, 500)
splash.overrideredirect(True)  

#loading the uneeflow logo as splash
splash_img = Image.open("UNEE FLOW LOGO.png")
splash_img = splash_img.resize((500, 500), Image.LANCZOS)
splash_bg = ImageTk.PhotoImage(splash_img)

splash_label = tk.Label(splash, image=splash_bg)
splash_label.pack()

#waiting time before the main window
splash.update()
time.sleep(1.5)

#removing the splash and showing the main window
splash.destroy()
root.deiconify()

##########################################################################################


# Buttons
build_model_button = tk.Button(root, text="Build a Model", font=("Arial", 14), command=None)
build_model_button.pack(pady=10)

test_model_button = tk.Button(root, text="Test a Model", font=("Arial", 14), command=None)
test_model_button.pack(pady=10)


#running the main window
root.mainloop()
