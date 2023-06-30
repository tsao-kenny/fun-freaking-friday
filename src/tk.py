import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
from datetime import datetime
import uuid
import requests


class ProfileWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Profile Manager")
        self.geometry("400x300")

        self.profiles_path = os.path.expanduser("~/profiles/profiles.json")
        self.profiles = {}
        self.profile_data = {}

        self.profile_name_var = tk.StringVar()
        self.profile_name_var.trace("w", self.load_profile_data)

        self.create_widgets()

    def create_widgets(self):
        profile_frame = ttk.Frame(self)
        profile_frame.pack(pady=10)

        profile_label = ttk.Label(profile_frame, text="Profile Name:")
        profile_label.pack(side=tk.LEFT)

        profile_listbox = ttk.Combobox(profile_frame, textvariable=self.profile_name_var)
        profile_listbox.pack(side=tk.LEFT)

        load_button = ttk.Button(self, text="Load", command=self.load_profile)
        load_button.pack(pady=10)

        create_button = ttk.Button(self, text="Create", command=self.create_profile)
        create_button.pack()

    def load_profile_data(self, *args):
        profile_name = self.profile_name_var.get()
        if profile_name:
            if os.path.exists(self.profiles_path):
                with open(self.profiles_path) as f:
                    self.profiles = json.load(f)
                    self.profile_data = self.profiles.get(profile_name, {})
            else:
                self.profiles = {}
                self.profile_data = {}

    def load_profile(self):
        profile_name = self.profile_name_var.get()
        if profile_name:
            if self.profile_data:
                fun_window = FunWindow(self, profile_name)
                # fun_window.show()
            else:
                messagebox.showwarning("Error", "Profile data not found.")

    def create_profile(self):
        profile_name = self.profile_name_var.get()
        if profile_name:
            profile_name = profile_name.lower().replace(" ", "_")
            if profile_name not in self.profiles:
                self.profiles[profile_name] = {"profile_name": profile_name, "questions": {}}
                self.profile_data = self.profiles[profile_name]
                self.save_profiles()
                messagebox.showinfo("Success", f"Profile '{profile_name}' created.")
            else:
                messagebox.showwarning("Error", "Profile already exists.")

    def save_profiles(self):
        profiles_data = {"profiles": self.profiles}
        with open(self.profiles_path, "w") as f:
            json.dump(profiles_data, f, indent=4)


class FunWindow(tk.Toplevel):
    def __init__(self, master, profile_name):
        super().__init__(master)
        self.title("Fun Window")
        self.geometry("400x400")

        self.profile_name = profile_name
        self.profile_data = master.profile_data.get("questions", {})

        self.question_text = tk.Text(self, height=5)
        self.question_text.pack(pady=10)

        fun_master_frame = ttk.Frame(self)
        fun_master_frame.pack(pady=10)

        fun_master_label = ttk.Label(fun_master_frame, text="Today's Fun Master:")
        fun_master_label.pack(side=tk.LEFT)

        self.fun_master_input = ttk.Entry(fun_master_frame)
        self.fun_master_input.pack(side=tk.LEFT)

        fun_button = ttk.Button(self, text="Fun", command=self.get_random_question)
        fun_button.pack()

        name_label = ttk.Label(self, text="Name:")
        name_label.pack()

        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()

        answer_label = ttk.Label(self, text="Answer:")
        answer_label.pack()

        self.answer_entry = ttk.Entry(self)
        self.answer_entry.pack()

        self.entries = []

        save_button = ttk.Button(self, text="Save", command=self.save_entry)
        save_button.pack()

        done_button = ttk.Button(self, text="Done", command=self.record_mood)
        done_button.pack(pady=10)

    def get_random_question(self):
        api_url = "https://api.example.com/questions"  # Replace with the actual API endpoint
        try:
            response = requests.get(api_url)
            data = response.json()
            question = data.get("question")
            self.question_text.delete("1.0", tk.END)
            self.question_text.insert(tk.END, question)
            self.add_question_entry(question)
        except requests.RequestException:
            messagebox.showwarning("Error", "Failed to retrieve a random question.")

    def add_question_entry(self, question):
        question_id = str(uuid.uuid4())
        self.profile_data[question_id] = {
            "question": question,
            "timestamp": str(datetime.now()),
            "answers": [],
            "fun_master": self.fun_master_input.get(),
            "mood": None,
        }

    def save_entry(self):
        name = self.name_entry.get().strip()
        answer = self.answer_entry.get().strip()
        if name and answer:
            question_id = list(self.profile_data.keys())[-1]
            entry_id = str(uuid.uuid4())
            entry = {"name": name, "answer": answer, "timestamp": str(datetime.now())}
            existing_answers = self.profile_data[question_id]["answers"]
            existing_names = [entry["name"] for entry in existing_answers]
            if name not in existing_names:
                existing_answers.append(entry)
                self.save_profiles()
                messagebox.showinfo("Success", "Entry saved.")
            else:
                messagebox.showwarning("Error", "Answer already exists for this name.")
        else:
            messagebox.showwarning("Error", "Name and answer cannot be empty.")

    def save_profiles(self):
        master = self.master
        master.profile_data["questions"] = self.profile_data
        master.save_profiles()

    def record_mood(self):
        mood = messagebox.askinteger("Mood", "How are you feeling? (1-10)")
        if 1 <= mood <= 10:
            question_id = list(self.profile_data.keys())[-1]
            self.profile_data[question_id]["mood"] = mood
            self.save_profiles()
            self.destroy()
        else:
            messagebox.showwarning("Error", "Invalid mood. Please enter a value between 1 and 10.")


if __name__ == "__main__":
    app = ProfileWindow()
    app.mainloop()
