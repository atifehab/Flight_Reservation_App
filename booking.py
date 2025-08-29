import tkinter as tk
from tkinter import messagebox
import re
from database import create_reservation

DATE_REGEX = r"^\d{4}-\d{2}-\d{2}$"  #YEAR-MONTH-DAY

class BookingPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="lightblue", padx=30, pady=30)
        self.controller = controller
        self.build_form()

    def build_form(self):
        tk.Label(self, text="Book a Flight",bg="lightblue",fg="black", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        labels = ["Name", "Flight Number", "Departure", "Destination", "Date", "Seat Number"]
        self.vars = {key: tk.StringVar() for key in labels}
        self.entries = {}
        
        placeholders = {
            "Name": "Enter your full name",
            "Flight Number": "e.g. MS146",
            "Departure": "e.g. Cairo",
            "Destination": "e.g. Barcelona",
            "Date": "YYYY-MM-DD",
            "Seat Number": "e.g. 7A"
        }
        
        for i, key in enumerate(labels, start=1):
            tk.Label(self, text=key + ":",bg="lightblue",fg="black",).grid(row=i, column=0, sticky="e", padx=(0, 8), pady=6)
            entry = tk.Entry(self,fg="gray", textvariable=self.vars[key], width=35)
            entry.grid(row=i, column=1, sticky="w", pady=6)
            entry.insert(0, placeholders[key])
            entry.bind("<FocusIn>", lambda e, ph=placeholders[key]: self.clear_placeholder(e, ph))
            entry.bind("<FocusOut>", lambda e, ph=placeholders[key]: self.add_placeholder(e, ph))
            self.entries[key] = entry
        
        btn_save = tk.Button(self, text="Submit", bg="darkblue",fg="white", command=self.submit)
        btn_back = tk.Button(self, text="Back", bg="darkblue",fg="white", command=lambda: self.controller.show_frame("HomePage"))

        btn_back.grid(row=len(labels)+1, column=0, pady=15, sticky="w")
        btn_save.grid(row=len(labels)+1, column=1, pady=15, sticky="e")

        for c in range(2):
            self.columnconfigure(c, weight=1)
            
    def clear_placeholder(self, event, placeholder):
        """Remove placeholder when clicking inside"""
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(self, event, placeholder):
        """Restore placeholder if empty after leaving"""
        entry = event.widget
        if entry.get().strip() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")


    def submit(self):
        name = self.vars["Name"].get().strip()
        flight_number = self.vars["Flight Number"].get().strip()
        departure = self.vars["Departure"].get().strip()
        destination = self.vars["Destination"].get().strip()
        date = self.vars["Date"].get().strip()
        seat_number = self.vars["Seat Number"].get().strip()

        if not all([name, flight_number, departure, destination, date, seat_number]):
            messagebox.showerror("Validation", "All fields are required.")
            return
        if not re.match(DATE_REGEX, date):
            messagebox.showerror("Validation", "Date must be in format YYYY-MM-DD.")
            return

        try:
            create_reservation(name, flight_number, departure, destination, date, seat_number)
            messagebox.showinfo("Success", "Reservation created successfully!")
            for var in self.vars.values():
                var.set("")
            self.controller.show_frame("ReservationsPage")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save reservation.\n{e}")