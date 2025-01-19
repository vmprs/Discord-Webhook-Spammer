import subprocess
import sys

# Function to check and install required modules
def check_and_install(module):
    try:
        __import__(module)
    except ImportError:
        print(f"{module} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# Check and install required modules
check_and_install('requests')
# tkinter is part of the standard library in Python and doesn't require installation via pip
# We only check requests since tkinter is usually pre-installed with Python.

# Proceed to the main GUI
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import threading
import time

class DiscordWebhookSpammer:
    def __init__(self, master):
        self.master = master
        self.running = False
        self.count = 0
        self.master.title("Discord Webhook Spammer")
        master.geometry("650x450")  # Set width to 650 and height to 450
        master.resizable(False, False)

        self.label = tk.Label(master, text="Enter Discord Webhook URL:")
        self.label.pack()

        self.webhook_url_entry = tk.Entry(master, width=70)
        self.webhook_url_entry.pack(pady=5)

        self.icon_label = tk.Label(master, text="Enter Avatar URL (optional):")
        self.icon_label.pack()

        self.icon_entry = tk.Entry(master, width=70)
        self.icon_entry.pack(pady=5)

        self.message_label = tk.Label(master, text="Enter your message:")
        self.message_label.pack()

        self.message_entry = tk.Text(master, height=5, width=70)
        self.message_entry.pack(pady=5)

        self.times_label = tk.Label(master, text="Number of times to send:")
        self.times_label.pack()

        self.times_entry = tk.Entry(master, width=10)
        self.times_entry.pack(pady=5)

        self.send_button = tk.Button(master, text="Start Spamming", command=self.start_spamming)
        self.send_button.pack(pady=20)

        self.stop_button = tk.Button(master, text="Stop Spamming", command=self.stop_spamming, state=tk.DISABLED)
        self.stop_button.pack(pady=20)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

        # Progress bar
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(master, variable=self.progress, maximum=100, length=500)
        self.progress_bar.pack(pady=10)

    def start_spamming(self):
        webhook_url = self.webhook_url_entry.get()
        icon_url = self.icon_entry.get().strip()
        message = self.message_entry.get("1.0", tk.END).strip()
        times = self.times_entry.get().strip()

        # Validate inputs
        if not webhook_url or not message or not times.isdigit():
            messagebox.showwarning("Input Error", "Please enter a webhook URL, a message, and a valid number of times.")
            return

        count = int(times)

        # Reset progress
        self.progress.set(0)

        # Enable the stop button
        self.stop_button.config(state=tk.NORMAL)

        # Disable the start button
        self.send_button.config(state=tk.DISABLED)

        # Create a thread to avoid blocking the GUI
        threading.Thread(target=self.spam_message, args=(webhook_url, icon_url, message, count)).start()

    def spam_message(self, webhook_url, icon_url, message, count):
        for i in range(count):
            payload = {'content': message}
            if icon_url:
                payload['avatar_url'] = icon_url

            try:
                response = requests.post(webhook_url, json=payload)

                if response.status_code == 204:
                    self.update_status("Message sent successfully!")
                elif response.status_code == 429:  # Rate limit
                    self.update_status("Rate limit exceeded. Please wait.")
                    break  # Stop sending if rate limited
                else:
                    self.update_status(f"Failed to send message. Status code: {response.status_code}")

            except Exception as e:
                self.update_status(f"Error: {e}")

            # Update the progress bar
            self.update_progress((i + 1) / count * 100)

            # Sleep for a short time to control the sending rate
            time.sleep(0.1)

        # Reset button states after spamming is done
        self.send_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_status(self, status):
        self.status_label.config(text=status)

    def update_progress(self, value):
        self.progress.set(value)
        self.progress_bar.update()  # Update the GUI to reflect progress changes

    def stop_spamming(self):
        # Disable the stop button
        self.stop_button.config(state=tk.DISABLED)

        # Enable the start button
        self.send_button.config(state=tk.NORMAL)
        self.progress.set(0)  # Reset progress bar when stopped

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordWebhookSpammer(root)
    root.mainloop()