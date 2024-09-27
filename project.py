import sys
import pyttsx3
from datetime import datetime
import time
import json
import logging
import threading
import tkinter as tk
from tkinter import messagebox
import queue

# Global tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window initially

# Set up logging
logging.basicConfig(filename='reminder.log', level=logging.INFO)

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Create a queue for thread-safe messagebox handling
message_queue = queue.Queue()

# Function to show an alert with a pop-up and voice
def alert(title, description, engine):
    print(f"Reminder: {title} - {description}")
    engine.say(f"Reminder for {title}: {description}")
    engine.runAndWait()

    # Add the reminder to the queue to be processed by the main thread
    message_queue.put((title, description))

# Function to process the messagebox queue on the main thread
def process_message_queue():
    try:
        while True:
            title, description = message_queue.get_nowait()
            messagebox.showinfo(f"Reminder: {title}", description)
    except queue.Empty:
        pass
    root.after(100, process_message_queue)

# Function to save reminders to a JSON file
def save_list(reminders):
    with open('list.json', 'w') as f:
        json.dump(reminders, f, indent=4)
    logging.info("Reminders saved to JSON file")

# Function to load reminders from a JSON file
def load_list():
    try:
        with open("list.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to check reminders in the background thread
def check_reminders():
    global details
    while True:
        now = datetime.now()
        for reminder in details:
            reminder_time = datetime.strptime(reminder["date"] + " " + reminder["time"], "%Y-%m-%d %H:%M")
            if now >= reminder_time:
                print(f"Reminder triggered: {reminder['title']}")
                alert(reminder["title"], reminder["description"], engine)
                details.remove(reminder)
                save_list(details)
        time.sleep(60)  # Check every minute

# Function to add a new task
def set_task():
    print("\n       SET THE REMINDER                  ")
    title = input("\nTitle of task: ").strip().lower()
    desc = input("Description of task: ")
    input_date = input("Date(YYYY-MM-DD): ")
    time_input = input("Time(HH:MM): ")

    if time_check(time_input) and date_check(input_date):
        reminder = {
            'title': title,
            'description': desc,
            'date': input_date,
            'time': time_input
        }
        details.append(reminder)
        print("Data is stored successfully!")
        engine.say("Data is stored successfully!")
        engine.runAndWait()
    else:
        print("There was an issue with the date or time. Please try again.")
        engine.say("There was an issue with the date or time. Please try again.")
        engine.runAndWait()
        set_task()

# Function to view all tasks
def view():
    if not details:
        print("No tasks to show")
        return
    else:
        print("-------------------YOUR REMINDERS---------------------\n")
        for i, reminder in enumerate(details):
            print(f"{i+1}. {reminder['title']}\n   {reminder['description']}\n   on {reminder['date']} at {reminder['time']}")
            print("--------------------------------------------------")

# Function to edit a task
def edit():
    editing_title = input("Enter the title of task you want to edit: ").strip().lower()
    for reminder in details:
        if reminder['title'] == editing_title:
            details.remove(reminder)
            print("Edit the details of your data: \n")
            set_task()
            return
    print("Such task does not exist!")
    engine.say("Such task does not exist!")
    engine.runAndWait()

# Function to search for a task
def search():
    choice = input("Do you want to search by \n1)Title \n2)Date\nEnter your choice: ")
    if choice == "1":
        text = input("Enter the title: ").strip().lower()
        found = False
        for reminder in details:
            if reminder['title'] == text:
                print("-------------------DETAILS-------------------\n")
                print(f"\n Title={reminder['title']}\nDescription={reminder['description']}\non {reminder['date']} at {reminder['time']}")
                print("\n---------------------------------------------")
                engine.say(f"Reminder '{reminder['title']}' found!")
                engine.runAndWait()
                found = True
        if not found:
            print(f"No task found with the title '{text}'")
            engine.say(f"No task found with the title '{text}'")
            engine.runAndWait()
    elif choice == "2":
        date_search = input("Enter the date: ").strip()
        found = False
        for reminder in details:
            if reminder['date'] == date_search:
                print("-------------------DETAILS-------------------\n")
                print(f"Title={reminder['title']}\nDescription={reminder['description']}\non {reminder['date']} at {reminder['time']}")
                print("\n---------------------------------------------")
                engine.say(f"Task for {reminder['date']} found!")
                engine.runAndWait()
                found = True
        if not found:
            print("No task found with the mentioned date")
            engine.say("No task found with the mentioned date")
            engine.runAndWait()
    else:
        print("Invalid option")
        engine.say("Invalid option")
        engine.runAndWait()

# Function to delete a task
def delete():
    delete_title = input("Enter the title of the task you want to delete: ").strip().lower()
    found = False
    for reminder in details:
        if reminder['title'] == delete_title:
            details.remove(reminder)
            save_list(details)
            found = True
            print(f"Task '{delete_title}' deleted successfully!")
            engine.say(f"Task '{delete_title}' deleted successfully!")
            engine.runAndWait()
            return
    if not found:
        print(f"No task found with the title '{delete_title}'")
        engine.say(f"No task found with the title '{delete_title}'")
        engine.runAndWait()

# Time validation function
def time_check(time_input):
    try:
        hour, minute = map(int, time_input.split(':'))
        if len(time_input) != 5 or hour < 0 or hour > 23 or minute < 0 or minute > 59:
            print("Invalid time format! Please use HH:MM.")
            return False
        return True
    except ValueError:
        print("Invalid time format! Please use HH:MM.")
        return False

# Date validation function
def date_check(input_date):
    try:
        year, month, day = map(int, input_date.split('-'))
        if len(input_date) != 10 or month < 1 or month > 12 or day < 1 or day > 31:
            print("Invalid date format! Please use YYYY-MM-DD.")
            return False
        return True
    except ValueError:
        print("Invalid date format! Please use YYYY-MM-DD.")
        return False

# Main function
def main():
    global details
    details = load_list()

    # Start the reminder checking thread
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

    print("Which function you want to perform? \n 1) Add a task\n 2) View tasks\n 3) Edit any task\n 4) Search a task\n 5) Delete a task\n 6) Exit")
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                set_task()
            elif choice == 2:
                view()
            elif choice == 3:
                edit()
            elif choice == 4:
                search()
            elif choice == 5:
                delete()
            elif choice == 6:
                save_list(details)
                sys.exit(0)
            else:
                print("Invalid option")
        except ValueError:
            print("Enter a valid operation")

if __name__ == "__main__":
    # Start the tkinter after loop to process the queue
    root.after(100, process_message_queue)
    main()

    # Start the tkinter main loop
    root.mainloop()
