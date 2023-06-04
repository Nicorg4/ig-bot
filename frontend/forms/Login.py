import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
import requests

class Login(tk.Frame):
    def verify(self):
        user = self.user.get()
        password = self.password.get()
        
        # Make an HTTP POST request to the login endpoint
        url = 'http://localhost:8000/login'  # Replace with your server's URL
        data = {'username': user, 'password': password}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            # Login successful
            self.controller.show_frame("NewCycle")
        else:
            # Login failed
            messagebox.showerror(message="Password is incorrect", title="Message")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.controller.title('Login')
        self.config(bg='#fcfcfc')
        

        logo = utl.read_image("./images/logo.png", (200, 200))

        # frame_logo
        frame_logo = tk.Frame(self, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg='#3a7ff6')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#3a7ff6')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # frame_form
        frame_form = tk.Frame(self, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height = 50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Login", font=('Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height = 50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        user_label = tk.Label(frame_form_fill, text="User", font=('Times', 14) ,fg="#666a88", bg='#fcfcfc', anchor="w")
        user_label.pack(fill=tk.X, padx=20, pady=5)
        self.user = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.user.pack(fill=tk.X, padx=20, pady=10)

        password_label = tk.Label(frame_form_fill, text="Password", font=('Times', 14), fg="#666a88", bg='#fcfcfc' , anchor="w")
        password_label.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        login = tk.Button(frame_form_fill, text="Login", font=('Times', 15, BOLD), bg='#3a7ff6', bd=0, fg="#fff", command=self.verify)
        login.pack(fill=tk.X, padx=20, pady=20)        
        login.bind("<Return>", (lambda event: self.verify()))

        register = tk.Button(frame_form_fill, text="Register", font=('Times', 15, BOLD), bg='#3a5ff6', bd=0, fg="#fff", command=lambda: controller.show_frame("Register"))
        register.pack(fill=tk.X, padx=20, pady=20)


        newCycle = tk.Button(frame_form_fill, text="Create new cycle", font=('Times', 15, BOLD), bg='#3a5ff6', bd=0, fg="#fff", command=lambda: controller.show_frame("NewCycle"))
        newCycle.pack(fill=tk.X, padx=20, pady=20)

        newigAccount = tk.Button(frame_form_fill, text="Create new ig account", font=('Times', 15, BOLD), bg='#3a5ff6', bd=0, fg="#fff", command=lambda: controller.show_frame("NewIgAccount"))
        newigAccount.pack(fill=tk.X, padx=20, pady=20)