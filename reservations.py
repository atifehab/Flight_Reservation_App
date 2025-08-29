import tkinter as tk
from tkinter import ttk,messagebox
from database import list_reservations, delete_reservation

class ReservationsPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="lightblue", padx=30, pady=30)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        header = tk.Label(self, text="All Reservations", bg="lightblue",fg="black", font=("Segoe UI", 16, "bold"))
        header.grid(row=0, column=0, sticky="w")

        self.tree = ttk.Treeview(self, columns=("id","name","flight","from","to","date","seat"), show="headings", height=12)
        for col, text, w in [
            ("id", "ID", 40),
            ("name","Name",140),
            ("flight","Flight #",80),
            ("from","From",100),
            ("to","To",100),
            ("date","Date",100),
            ("seat","Seat",60),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center")

        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)

        yscroll = tk.Scrollbar(self, orient="vertical", activebackground="blue", command=self.tree.yview)
        self.tree.configure(yscroll=yscroll.set)
        yscroll.grid(row=1, column=4, sticky="ns")

        btn_back = tk.Button(self, text="Back", bg="darkblue",fg="white", command=lambda: self.controller.show_frame("HomePage"))
        btn_refresh = tk.Button(self, text="Refresh", bg="darkblue",fg="white", command=self.refresh)
        btn_new = tk.Button(self, text="New Booking", bg="darkblue",fg="white", command=lambda: self.controller.show_frame("BookingPage"))
        btn_edit = tk.Button(self, text="Edit Selected", bg="darkblue",fg="white", command=self.edit_selected)
        btn_delete = tk.Button(self, text="Delete Selected", bg="darkblue",fg="white", command=self.delete_selected)

        btn_back.grid(row=2, column=0, pady=10, sticky="w")
        btn_refresh.grid(row=2, column=1, pady=10, sticky="w")
        btn_new.grid(row=2, column=2, pady=10, sticky="e")
        btn_edit.grid(row=3, column=2, pady=5, sticky="e")
        btn_delete.grid(row=3, column=3, pady=5, sticky="e")

        self.rowconfigure(1, weight=1)
        for c in range(4):
            self.columnconfigure(c, weight=1)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in list_reservations():
            self.tree.insert("", "end", values=r)

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a reservation first.")
            return None
        values = self.tree.item(sel[0], "values")
        return int(values[0])

    def edit_selected(self):
        res_id = self.get_selected_id()
        if res_id is None:
            return
        self.controller.load_edit_page(res_id)
        self.controller.show_frame("EditReservationPage")

    def delete_selected(self):
        res_id = self.get_selected_id()
        if res_id is None:
            return
        if messagebox.askyesno("Confirm", "Delete this reservation?"):
            delete_reservation(res_id)
            self.refresh()