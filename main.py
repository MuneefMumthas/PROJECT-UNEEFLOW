import tkinter as tk

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_pos = (screen_width - width) // 2
    y_pos = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")


#creating the main window
root = tk.Tk()
root.title("UNEEFLOW")
center_window(root, 500, 500)

#setting the logo
root.iconbitmap("U Logo.ico")


#running the main window
root.mainloop()
