from collections import defaultdict
import json
import os
import random
from typing import Any
import uuid
from datetime import datetime
import sys
import matplotlib.pyplot as plt
import numpy as np


PROFILES_DIRECTORY = os.path.expanduser("~/profiles")
PROFILES_FILE = os.path.join(PROFILES_DIRECTORY, "profiles.json")

QUESTIONS = os.path.join(os.getcwd(), "src", "resources", "questions.json")


class App:
    def __init__(self) -> None:
        self.profiles: dict[str, str] = self.load_profiles()
        print(self.profiles)
        self.profile_name: str = None
        self.profile_data: dict[str, Any] = None

    def main_window(self) -> None:
        print("\nMenu:")
        print("0. Exit")
        print("1. Load a Profile")
        print("2. Create a Profile")
        print("3. Mood Analysis")
        print("4. Rating Analysis")

        choice = input("Enter your choice (0-4): ")
        if choice == "1":
            self.load_profile()
        elif choice == "2":
            self.create_profile()
        elif choice == "3":
            self.mood_analyis()
        elif choice == "4":
            self.rating_analysis()
        elif choice == "0":
            print("Exiting...")
            sys.exit()

        else:
            print("Invalid choice.")

    def get_icebreaker(self) -> str:
        with open(QUESTIONS, "r", encoding="utf-8") as infile:
            questions = json.loads(infile.read())
            random_number = random.randint(1, 500)
            question = questions[str(random_number)]
            return question

    def load_profiles(self) -> dict[str, Any]:
        if os.path.exists(PROFILES_FILE):
            with open(PROFILES_FILE, "r") as file:
                profiles = json.loads(file.read())
                if not profiles:
                    profiles = {}
        else:
            profiles = {}
        return profiles

    def save_profiles(self) -> None:
        if not os.path.exists(PROFILES_DIRECTORY):
            os.makedirs(PROFILES_DIRECTORY)
        with open(PROFILES_FILE, "w") as file:
            json.dump(self.profiles, file, indent=4)

    def create_profile(self) -> None:
        profile_name = input("Enter Profile Name: ").lower().replace(" ", "_")
        if profile_name:
            if profile_name in self.profiles:
                print("Profile already exists.")
            else:
                self.profiles[profile_name] = {"profile_name": profile_name, "questions": {}}
                self.save_profiles()
                print("Profile created successfully.")
        else:
            print("Invalid profile name.")
        self.main_window()

    def load_profile(self) -> None:
        if not self.profiles:
            print("No profiles found.")
            self.main_window()

        profile_names = list(self.profiles.keys())
        print("Available Profiles:")
        for i, name in enumerate(profile_names, start=1):
            print(f"{i}. {name}")

        profile_index = input("Select a profile (enter the index): ")
        if profile_index.isdigit():
            index = int(profile_index) - 1
            if 0 <= index < len(profile_names):
                self.profile_name = profile_names[index]
                self.profile_data = self.profiles[self.profile_name]
                self.fun_window()
            else:
                print("Invalid profile index.")
        else:
            print("Invalid input.")

    def fun_window(self) -> None:
        print("\n=== Fun Window ===")
        print("Enter 'fun' to retrieve a random ice breaker question.")
        print("Enter 'sad' if you're feeling sad.")

        while True:
            command = input("Enter a command: ")
            if command == "fun":
                self.get_random_question()
            elif command == "sad":
                self.record_sad()
            else:
                print("Invalid command.")

    def get_random_question(self) -> None:
        response = self.get_icebreaker()
        print("Ice Breaker Question:")
        print(response)

        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        answers = []
        answering = True
        while answering:
            print("Record answers (enter done to finish):")
            name = input("Name: ")
            if name == "done":
                answering = False
                break
            answer = input("Response: ")

            rating: str = input("Rate this answer (any number): ")
            try:
                rating = float(rating)
            except ValueError:
                print("Not an integer, assigning default.")
                rating = 420.0
            answers.append({"name": name, "answer": answer, "rating": rating})

        mood = input("How are you feeling (any number)? ")

        try:
            mood = float(mood)
        except ValueError:
            print("Not a number. Assigning default.")
            mood = -1.0

        self.profile_data["questions"][entry_id] = {
            "question": response,
            "timestamp": timestamp,
            "answers": answers,
            "fun_master": input("Today's Fun Master: "),
            "mood": mood,
            "rating": rating,
        }
        self.save_profiles()
        print("Question saved successfully.")
        self.main_window()

    def record_sad(self) -> None:
        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        self.profile_data["questions"][entry_id] = {
            "question": None,
            "timestamp": timestamp,
            "answers": [],
            "fun_master": None,
            "mood": 0,
        }
        self.save_profiles()
        print("That sucks.")
        self.main_window()

    def mood_analyis(self) -> None:
        # Prepare data for scatter plot
        profiles = []
        moods = []

        for profile_data in self.profiles.values():
            profile_name = profile_data["profile_name"]
            for question_data in profile_data["questions"].values():
                mood = question_data["mood"]
                profiles.append(profile_name)
                moods.append(mood)

        # Calculate mean mood for each profile
        profile_mean_moods = {}
        for profile in set(profiles):
            profile_moods = [mood for profile_, mood in zip(profiles, moods) if profile_ == profile]
            mean_mood = np.mean(profile_moods)
            profile_mean_moods[profile] = mean_mood

        # Define colors for each profile
        profile_colors = plt.cm.Set1(np.linspace(0, 1, len(profile_mean_moods)))

        # Plot mood vs. profile
        plt.scatter(profiles, moods)
        plt.xlabel("Profile")
        plt.ylabel("Mood")
        plt.title("Mood vs. Profile")
        plt.xticks(rotation=90)

        # Add mean mood analysis with color-coded lines
        for i, (profile, mean_mood) in enumerate(profile_mean_moods.items()):
            color = profile_colors[i]
            plt.axhline(y=mean_mood, color=color, linestyle="--", label=f"Mean Mood ({profile}): {mean_mood:.2f}")

        plt.legend()
        plt.tight_layout()
        plt.show()
        self.main_window()

    def rating_analysis(self):
        # Prepare data for visualization
        name_ratings = defaultdict(list)

        for profile_data in self.profiles.values():
            for question_data in profile_data["questions"].values():
                if "answers" in question_data:
                    for answer in question_data["answers"]:
                        name = answer["name"]
                        rating = answer["rating"]
                        name_ratings[name].append(rating)

        # Calculate max, min, and mean ratings
        names = []
        max_ratings = []
        min_ratings = []
        mean_ratings = []

        for name, ratings in name_ratings.items():
            names.append(name)
            max_rating = max(ratings)
            min_rating = min(ratings)
            mean_rating = sum(ratings) / len(ratings)
            max_ratings.append(max_rating)
            min_ratings.append(min_rating)
            mean_ratings.append(mean_rating)

        # Plot the max, min, and mean ratings by name
        x = range(len(names))
        width = 0.25

        plt.bar(x, max_ratings, width, label="Max")
        plt.bar(x, min_ratings, width, label="Min")
        plt.bar(x, mean_ratings, width, label="Mean")

        plt.xlabel("Name")
        plt.ylabel("Rating")
        plt.title("Rating by Name")
        plt.xticks(x, names, rotation=90)
        plt.legend()
        plt.tight_layout()
        plt.show()
        self.main_window()
