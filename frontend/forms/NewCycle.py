import tkinter as tk
from tkinter import ttk
import requests

class NewCycle(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.config(bg='#fcfcfc')

        # Fetch the list of account usernames
        self.accounts = self.get_accounts()

        # frame_form
        frame_form = tk.Frame(self, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="top", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="New Cycle", font=('Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        dropdown1_label = tk.Label(frame_form_fill, text="Dropdown 1", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        dropdown1_label.pack(fill=tk.X, padx=20, pady=5)
        self.dropdown1 = ttk.Combobox(frame_form_fill, font=('Times', 14), values=self.accounts)
        self.dropdown1.pack(fill=tk.X, padx=20, pady=10)

        dropdown2_label = tk.Label(frame_form_fill, text="Dropdown 2", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        dropdown2_label.pack(fill=tk.X, padx=20, pady=5)
        self.dropdown2 = ttk.Combobox(frame_form_fill, font=('Times', 14), values=["Option A", "Option B", "Option C"])
        self.dropdown2.pack(fill=tk.X, padx=20, pady=10)

        submit = tk.Button(frame_form_fill, text="Submit", font=('Times', 15, 'bold'), bg='#3a7ff6', bd=0, fg="#fff", command=self.submit_data)
        submit.pack(fill=tk.X, padx=20, pady=20)

    def submit_data(self):
        dropdown1_value = self.dropdown1.get()
        dropdown2_value = self.dropdown2.get()

        # Now you can process these values
        print(f"Dropdown 1: {dropdown1_value}, Dropdown 2: {dropdown2_value}")


    def get_accounts(self):
        url = 'http://localhost:8000/get-accounts'  # Replace this with your API endpoint
        try:
            response = requests.get(url)
            if response.status_code == 200:
                accounts = response.json()['accounts']
                usernames = [account['username'] for account in accounts]
                return usernames
            else:
                print(f'Error: received status code {response.status_code}')
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return []
        return []
