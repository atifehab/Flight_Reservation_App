import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self,master,controller):
        super().__init__(master,bg= "lightblue", padx=30, pady=30)
        self.controller = controller
        title = tk.Label(self, text="Flight Reservation System",bg= "lightblue",fg= "black", font=("Segoe UI", 20, "bold"))
        subtitle = tk.Label(self, text="Book your flights and manage your reservations with our simple application.",bg= "lightblue",fg= "black", font=("Segoe UI", 10))
        
        btn_book = tk.Button(self, text="Book Flight",bg= "darkblue",fg= "white", command=lambda: controller.show_frame("BookingPage"))
        btn_view = tk.Button(self, text="View Reservations",bg= "darkblue",fg= "white", command=lambda: controller.show_frame("ReservationsPage"))

        title.grid(row=0, column=0, columnspan=2, pady=(0, 6))
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        btn_book.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        btn_view.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        