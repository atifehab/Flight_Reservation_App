import tkinter as tk
from tkinter import ttk
from database import init_db
from home import HomePage
from booking import BookingPage
from reservations import ReservationsPage
from edit_reservation import EditReservationPage


APP_TITLE = "Flight Reservation App"
APP_SIZE = "1080x720"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.minsize(720, 480)
        
        
        style = ttk.Style(self)
        # Try a nicer theme if available
        try:
            style.theme_use("clam")
        except Exception:
            pass

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F, name in [
            (HomePage, "HomePage"),
            (BookingPage, "BookingPage"),
            (ReservationsPage, "ReservationsPage"),
            (EditReservationPage, "EditReservationPage"),
        ]:
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Initialize Database
        init_db()

        self.show_frame("HomePage")

    def show_frame(self, name: str):
        frame = self.frames[name]
        if name == "ReservationsPage":
            frame.refresh()
        frame.tkraise()

    def load_edit_page(self, res_id: int):
        edit_frame: EditReservationPage = self.frames["EditReservationPage"]
        edit_frame.load(res_id)

if __name__ == "__main__":
    app = App()
    app.bind("<Escape>", lambda e: app.destroy())
    app.mainloop()
