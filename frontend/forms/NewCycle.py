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

        # Canvas for scrollable frame
        canvas = tk.Canvas(frame_form, bg='#fcfcfc')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for canvas
        scrollbar = ttk.Scrollbar(frame_form, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Bind the mouse wheel event to the canvas
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Scrollable frame
        self.scrollable_frame = tk.Frame(canvas, bg='#fcfcfc')
        self.scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        # Add first two dropdowns
        self.add_dropdown(self.scrollable_frame, "Destination Type", self.accounts)
        self.add_dropdown(self.scrollable_frame, "Destination", ["Option A", "Option B", "Option C"])

        # Create add more dropdowns button
        self.add_button = tk.Button(self.scrollable_frame, text='+', command=self.add_more_dropdowns)
        self.add_button.pack()

    def add_dropdown(self, frame, label, values):
        dropdown_label = tk.Label(frame, text=label, font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        dropdown_label.pack(fill=tk.X, padx=200, pady=5)
        dropdown = ttk.Combobox(frame, font=('Times', 14), values=values, state="readonly")
        dropdown.bind('<MouseWheel>', lambda e: 'break')  # Prevent default behavior
        dropdown.pack(fill=tk.X, padx=20, pady=10)
        

    def add_more_dropdowns(self):
        self.add_button.destroy()
        self.add_dropdown(self.scrollable_frame, "Destination Type", self.accounts)
        self.add_dropdown(self.scrollable_frame, "Destination", ["Option A", "Option B", "Option C"])
        self.add_button = tk.Button(self.scrollable_frame, text='+', command=self.add_more_dropdowns)
        self.add_button.pack()

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
