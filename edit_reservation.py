import tkinter as tk
from tkinter import messagebox
import re
from database import get_reservation, update_reservation, delete_reservation

DATE_REGEX = r"^\d{4}-\d{2}-\d{2}$"  # YYYY-MM-DD

class EditReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightblue", padx=30, pady=30)
        self.controller = controller
        self.current_id = None
        self._build_form()

    def _build_form(self):
        tk.Label(self, text="Edit Reservation",bg="lightblue",fg="black", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        labels = ["Name", "Flight Number", "Departure", "Destination", "Date (YYYY-MM-DD)", "Seat Number"]
        self.vars = {key: tk.StringVar() for key in labels}

        for i, key in enumerate(labels, start=1):
            tk.Label(self, text=key + ":",bg="lightblue",fg="black",).grid(row=i, column=0, sticky="e", padx=(0, 8), pady=6)
            entry = tk.Entry(self, textvariable=self.vars[key], width=35)
            entry.grid(row=i, column=1, sticky="w", pady=6)

        btn_back = tk.Button(self, text="Back", bg="darkblue",fg="white", command=lambda: self.controller.show_frame("ReservationsPage"))
        btnupdate = tk.Button(self, text="Update", bg="darkblue",fg="white", command=self.update)
        btndelete = tk.Button(self, text="Delete", bg="darkblue",fg="white", command=self.delete)

        btn_back.grid(row=len(labels)+1, column=0, pady=15, sticky="w")
        btndelete.grid(row=len(labels)+1, column=1, pady=15, sticky="e")
        btnupdate.grid(row=len(labels)+2, column=1, pady=(0,15), sticky="e")

        for c in range(2):
            self.columnconfigure(c, weight=1)

    def load(self, res_id: int):
        self.current_id = res_id
        row = get_reservation(res_id)
        if not row:
            messagebox.showerror("Not found", "Reservation no longer exists.")
            self.controller.show_frame("ReservationsPage")
            return
        _, name, flight, departure, destination, date, seat = row
        self.vars["Name"].set(name)
        self.vars["Flight Number"].set(flight)
        self.vars["Departure"].set(departure)
        self.vars["Destination"].set(destination)
        self.vars["Date (YYYY-MM-DD)"].set(date)
        self.vars["Seat Number"].set(seat)

    def update(self):
        if self.current_id is None:
            return
        name = self.vars["Name"].get().strip()
        flight_number = self.vars["Flight Number"].get().strip()
        departure = self.vars["Departure"].get().strip()
        destination = self.vars["Destination"].get().strip()
        date = self.vars["Date (YYYY-MM-DD)"].get().strip()
        seat_number = self.vars["Seat Number"].get().strip()

        if not all([name, flight_number, departure, destination, date, seat_number]):
            messagebox.showerror("Validation", "All fields are required.")
            return
        if not re.match(DATE_REGEX, date):
            messagebox.showerror("Validation", "Date must be in format YYYY-MM-DD.")
            return

        update_reservation(self.current_id, name, flight_number, departure, destination, date, seat_number)
        messagebox.showinfo("Updated", "Reservation updated successfully!")
        self.controller.show_frame("ReservationsPage")
        self.controller.frames["ReservationsPage"].refresh()

    def delete(self):
        if self.current_id is None:
            return
        if messagebox.askyesno("Confirm", "Delete this reservation?"):
            delete_reservation(self.current_id)
            messagebox.showinfo("Deleted", "Reservation deleted.")
            self.controller.show_frame("ReservationsPage")
            self.controller.frames["ReservationsPage"].refresh()
