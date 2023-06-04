import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import requests

class NewIgAccount(tk.Frame):
    def register_ig_account(self):
        username = self.username.get()
        password = self.password.get()
        
        url = 'http://localhost:8000/register-account'  # Replace with your server's register endpoint
        headers = {'User-Agent': 'Mozilla/5.0'}  # Example user agent
        params = {'username': username, 'password': password, 'owner': 0}
        
        try:
            response = requests.post(url, headers=headers, json=params)
            
            if response.status_code == 200:
                # Request was successful
                data = response.json()
                # Process the response data here
                self.controller.show_frame("NewCycle")
            else:
                # Request failed
                print('Error in the request:', response.status_code)
                
        except requests.exceptions.RequestException as e:
            # An error occurred while making the request
            print('Error in the request:', str(e))

        # For now, we will just print the values
        print(f"Username: {username}, Password: {password}")

    def go_to_login(self):
        self.controller.show_frame("Login")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.config(bg='#fcfcfc')

        # frame_form
        frame_form = tk.Frame(self, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="top", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="New Ig Account", font=('Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        username_label = tk.Label(frame_form_fill, text="Username", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        username_label.pack(fill=tk.X, padx=20, pady=5)
        self.username = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.username.pack(fill=tk.X, padx=20, pady=10)

        password_label = tk.Label(frame_form_fill, text="Password", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        password_label.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        register = tk.Button(frame_form_fill, text="Register", font=('Times', 15, BOLD), bg='#3a7ff6', bd=0, fg="#fff", command=self.register_ig_account)
        register.pack(fill=tk.X, padx=20, pady=20)

        back_to_login = tk.Button(frame_form_fill, text="Back to Login", font=('Times', 15, BOLD), bg='#3a5ff6', bd=0, fg="#fff", command=self.go_to_login)
        back_to_login.pack(fill=tk.X, padx=20, pady=20)
