import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import json
import os
import threading
from plyer import notification

DATA_FILE = os.path.join(os.path.expanduser("~"), "date_notifier_data.json")

class DateNotifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("هشدار تاریخ مشخص")

        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, "yyyy-mm-dd")
        self.date_entry.pack(pady=5)

        self.note_entry = tk.Entry(root, width=40)
        self.note_entry.insert(0, "متن یادآوری")
        self.note_entry.pack(pady=5)

        self.multi_dates_button = tk.Button(root, text="افزودن هشدار برای چند تاریخ", command=self.add_multiple_dates)
        self.multi_dates_button.pack(pady=5)

        self.add_button = tk.Button(root, text="افزودن هشدار", command=self.add_date)
        self.add_button.pack(pady=5)

        self.status = tk.Label(root, text="")
        self.status.pack()

        self.load_dates()
        self.start_checker()

    def load_dates(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                self.dates = json.load(f)
        else:
            self.dates = []

    def save_dates(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.dates, f)

    def add_date(self):
        date_str = self.date_entry.get()
        note = self.note_entry.get()
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            self.dates.append({"date": date_str, "note": note})
            self.save_dates()
            self.status.config(text=f"هشدار ذخیره شد برای {date_str}")
        except ValueError:
            self.status.config(text="تاریخ نامعتبر است. فرمت باید yyyy-mm-dd باشد.")

    def add_multiple_dates(self):
        note = self.note_entry.get()
        dates_str = simpledialog.askstring("تاریخ ها", "تاریخ‌ها را با ویرگول جدا کنید (yyyy-mm-dd,yyyy-mm-dd,...):")
        if dates_str:
            for date_str in dates_str.split(','):
                date_str = date_str.strip()
                try:
                    datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    self.dates.append({"date": date_str, "note": note})
                except ValueError:
                    continue
            self.save_dates()
            self.status.config(text="هشدارها ذخیره شدند.")

    def start_checker(self):
        def check_dates():
            today = datetime.date.today().isoformat()
            for item in self.dates:
                if item["date"] == today:
                    notification.notify(title="یادآوری تاریخ", message=item["note"], timeout=10)
            threading.Timer(3600, check_dates).start()  # چک کردن هر ساعت

        check_dates()

if __name__ == "__main__":
    root = tk.Tk()
    app = DateNotifierApp(root)
    root.mainloop()
