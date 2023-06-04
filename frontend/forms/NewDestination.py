import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import requests


class NewDestination(tk.Frame):
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
        title = tk.Label(frame_form_top, text="New Destination", font=('Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Type selection dropdown
        type_label = tk.Label(frame_form, text="Type", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        type_label.pack(fill=tk.X, padx=20, pady=5)

        self.type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(frame_form, font=('Times', 14), textvariable=self.type_var, state='readonly')
        type_dropdown['values'] = ['Location', 'Place', 'Hashtag']
        type_dropdown.bind('<<ComboboxSelected>>', self.update_fields)
        type_dropdown.pack(fill=tk.X, padx=20, pady=10)

        # Fields for Location type
        self.location_id_label = tk.Label(frame_form, text="Location ID", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.location_id_entry = ttk.Entry(frame_form, font=('Times', 14))

        self.location_name_label = tk.Label(frame_form, text="Location Name", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.location_name_entry = ttk.Entry(frame_form, font=('Times', 14))

        # Fields for Place type
        self.place_name_label = tk.Label(frame_form, text="Place Name", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.place_name_entry = ttk.Entry(frame_form, font=('Times', 14))

        # Fields for Hashtag type
        self.hashtag_name_label = tk.Label(frame_form, text="Hashtag Name", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.hashtag_name_entry = ttk.Entry(frame_form, font=('Times', 14))

        # Submit button
        submit_button = tk.Button(self, text="Submit", font=('Times', 15, BOLD), bg='#3a7ff6', bd=0, fg="#fff", command=self.submit_destination)
        submit_button.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

    def update_fields(self, event):
        selected_type = self.type_var.get()

        # Hide all fields
        self.location_id_label.pack_forget()
        self.location_id_entry.pack_forget()

        self.location_name_label.pack_forget()
        self.location_name_entry.pack_forget()

        self.place_name_label.pack_forget()
        self.place_name_entry.pack_forget()

        self.hashtag_name_label.pack_forget()
        self.hashtag_name_entry.pack_forget()

        # Show fields based on selected type
        if selected_type == 'Location':
            self.location_id_label.pack(fill=tk.X, padx=20, pady=5)
            self.location_id_entry.pack(fill=tk.X, padx=20, pady=10)
            self.location_name_label.pack(fill=tk.X, padx=20, pady=5)
            self.location_name_entry.pack(fill=tk.X, padx=20, pady=10)

        elif selected_type == 'Place':
            self.place_name_label.pack(fill=tk.X, padx=20, pady=5)
            self.place_name_entry.pack(fill=tk.X, padx=20, pady=10)

        elif selected_type == 'Hashtag':
            self.hashtag_name_label.pack(fill=tk.X, padx=20, pady=5)
            self.hashtag_name_entry.pack(fill=tk.X, padx=20, pady=10)

    def submit_destination(self):
        destination_type = self.type_var.get()

        if destination_type == 'Location':
            location_id = self.location_id_entry.get()
            location_name = self.location_name_entry.get()
            place_name = ""
            hashtag_name = ""

        elif destination_type == 'Place':
            location_id = ""
            location_name = ""
            place_name = self.place_name_entry.get()
            hashtag_name = ""

        elif destination_type == 'Hashtag':
            location_id = ""
            location_name = ""
            place_name = ""
            hashtag_name = self.hashtag_name_entry.get()

        # Prepare the data for registration
        data = {
            'locationId': location_id,
            'locationName': location_name,
            'placeName': place_name,
            'hashtag': hashtag_name,
            'type': destination_type
        }

        url = 'http://localhost:8000/register-destination'

        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                print('Destination registered successfully')
                # Reset the form fields
                self.type_var.set('')
                self.location_id_entry.delete(0, tk.END)
                self.location_name_entry.delete(0, tk.END)
                self.place_name_entry.delete(0, tk.END)
                self.hashtag_name_entry.delete(0, tk.END)
            else:
                print('Error in destination registration:', response.status_code)
                messagebox.showerror(message='Error in destination registration', title='Error')

        except requests.exceptions.RequestException as e:
            print('Error in destination registration:', str(e))
            messagebox.showerror(message='Error in destination registration', title='Error')
