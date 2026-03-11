import customtkinter as ctk
from tkinter import messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SleepApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daniel's PC Timer")
        self.root.geometry("400x450")
        
        self.after_id = None
        self.remaining_seconds = 0

        self.label_title = ctk.CTkLabel(root, text="Set Sleep Timer", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)
        
        # יצירת ה-Frame לקלט
        self.input_frame = ctk.CTkFrame(root)
        self.input_frame.pack(pady=10, padx=40, fill="x")

        # פקודת המרכוז: נותן משקל שווה לכל העמודות בפריים
        self.input_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # כותרות מעל התיבות
        ctk.CTkLabel(self.input_frame, text="Hours").grid(row=0, column=0, pady=(10, 0))
        ctk.CTkLabel(self.input_frame, text="Minutes").grid(row=0, column=1, pady=(10, 0))
        ctk.CTkLabel(self.input_frame, text="Seconds").grid(row=0, column=2, pady=(10, 0))

        # תיבות קלט
        self.h_entry = ctk.CTkEntry(self.input_frame, width=70, justify="center", placeholder_text="0")
        self.h_entry.grid(row=1, column=0, padx=5, pady=15)
        
        self.m_entry = ctk.CTkEntry(self.input_frame, width=70, justify="center", placeholder_text="0")
        self.m_entry.grid(row=1, column=1, padx=5, pady=15)
        
        self.s_entry = ctk.CTkEntry(self.input_frame, width=70, justify="center", placeholder_text="0")
        self.s_entry.grid(row=1, column=2, padx=5, pady=15)

        self.status_label = ctk.CTkLabel(root, text="Status: Ready", font=("Arial", 16), text_color="#3498db")
        self.status_label.pack(pady=20)

        self.start_btn = ctk.CTkButton(root, text="Start Timer", command=self.start_timer, 
                                       fg_color="#2ecc71", hover_color="#27ae60", width=200, corner_radius=10)
        self.start_btn.pack(pady=10)

        self.stop_btn = ctk.CTkButton(root, text="Stop / Cancel", command=self.stop_timer, 
                                      fg_color="#e74c3c", hover_color="#c0392b", width=200, corner_radius=10)
        self.stop_btn.pack(pady=10)

        self.exit_btn = ctk.CTkButton(root, text="Exit Application", command=self.exit_app, 
                                      fg_color="#555555", hover_color="#333333", width=200, corner_radius=10)
        self.exit_btn.pack(pady=10)

    def format_time(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def update_countdown(self):
        if self.remaining_seconds > 0:
            self.status_label.configure(text=f"Time left: {self.format_time(self.remaining_seconds)}", text_color="#e67e22")
            self.remaining_seconds -= 1
            self.after_id = self.root.after(1000, self.update_countdown)
        else:
            self.do_sleep()

    def start_timer(self):
        try:
            h = int(self.h_entry.get() or 0)
            m = int(self.m_entry.get() or 0)
            s = int(self.s_entry.get() or 0)
            self.remaining_seconds = (h * 3600) + (m * 60) + s
            
            if self.remaining_seconds <= 0:
                messagebox.showwarning("Error", "Please enter a valid time!")
                return

            self.start_btn.configure(state="disabled")
            self.update_countdown()
            
        except ValueError:
            messagebox.showerror("Error", "Numbers only, Daniel!")

    def stop_timer(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
            self.remaining_seconds = 0
            self.status_label.configure(text="Status: Cancelled", text_color="#3498db")
            self.start_btn.configure(state="normal")
            messagebox.showinfo("Cancelled", "Sleep timer stopped.")

    def exit_app(self):
        if self.after_id:
            if messagebox.askokcancel("Exit", "Timer is running. Are you sure you want to exit?"):
                self.root.destroy()
        else:
            self.root.destroy()

    def do_sleep(self):
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

if __name__ == "__main__":
    root = ctk.CTk()
    app = SleepApp(root)
    root.mainloop()