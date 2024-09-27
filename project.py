import sys
import pyttsx3
from datetime import date,datetime
import time
import dateutil.parser
import json

details = list()
keys = ["title", "description", "date", "time"]
reminder = dict.fromkeys(keys, None)
def load_list():
    try:
        with open("list.json",'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_list(reminders):
    with open('list.json', 'w') as f:
        json.dump(reminders, f, indent=4)

def main():
    global details
    details= load_list()
    print("Which function you want to perform? \n 1) Add a task\n 2) View tasks\n 3) Edit any task\n 4) Search a task\n 5) Delete a task\n 6) Exit")
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            switch(choice)
        except ValueError:
            print("Enter valid operation")

def switch(choice):
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

def edit():
    editing_title = input("Enter the title of task which you want to edit: ").strip().lower()
    for reminder in details:
        if reminder['title'] == editing_title:
            details.remove(reminder)
            print("Edit the details of your data: \n")
            set_task()
        else:
            print("such task does not exist!")
            engine = pyttsx3.init()
            engine.say("such task does not exist!")
            engine.runAndWait()

def set_task():
    print("\n       SET THE TASK                  ")
    title = input("\nTitle of task: ").strip().lower()
    desc = input("Description of task: ")
    input_date = input("Date: ")
    time = input("Time(HH:MM): ")

       
    if time_check(time) and date_check(input_date): 
        reminder = {
            'title' : title,
            'description' : desc,
            "date" : input_date,
            "time" : time
        }  
        details.append(reminder)
        print("Data is stored successfully!")
        engine = pyttsx3.init()
        engine.say("Data is stored successfully!")
        engine.runAndWait()
    else:
        print("There was an issue with the date or time. Please try again.")
        engine = pyttsx3.init()
        engine.say("There was an issue with the date or time. Please try again.")
        engine.runAndWait()
        set_task()

def view():
    if not details:
        print("No tasks to show")
        return False
    else:
        
        print("-------------------YOUR TASKS---------------------\n")
        for i, reminder in enumerate(details):
            print(f"{i+1}. {reminder['title']}\n   {reminder['description']}\n   on {reminder['date']} at {reminder['time']}")
            print("----------------------------------------------")

def time_check(time):
    try:
        hour,minute = time.split(":")
        hour= int(hour)
        minute = int(minute)
        if minute < 61 and minute > 0 and hour <= 24:
            return True
        else:
            print("Time is not mentioned properly.\n Re-Enter the data")
            engine = pyttsx3.init()
            engine.say("Time is not mentioned properly.Re-Enter the data")
            engine.runAndWait()
            return False
    except:
        print("Invalid format!")
        return False

def date_check(input_date):
    try:
        parsed_date = dateutil.parser.parse(input_date)
        today_date = date.today()
        if today_date > parsed_date.date():
            print("The date has already passed!")
            engine = pyttsx3.init()
            engine.say("The date has already passed!")
            engine.runAndWait()
            return False
        else:
            return True
    except:
        print("Invalid format!")
        return False


def search():
    choice = input("Do you want to search by \n1)Title \n2)Date\nEnter your choice: ")
    
    if choice == "1":
        text = input("Enter the title: ")
        found = False
        for reminder in details:
            if reminder['title'].lower() == text.lower():
                print("-------------------DETAILS-------------------\n")
                print(f"\n Title={reminder['title']}\nDescription={reminder['description']}\non {reminder['date']} at {reminder['time']}")
                print("\n---------------------------------------------")
                engine = pyttsx3.init()
                engine.say(f"Reminder '{reminder['title']}' found!")
                engine.runAndWait()
                found = True
        if not found:
            print(f"No task found with the title '{text}'")
            engine = pyttsx3.init()
            engine.say(f"No task found with the title '{text}'")
            engine.runAndWait()
    elif choice == "2":
        date_search = input("Enter your date: ")
        found = False
        for reminder in details:
            if reminder['date'] == date_search:
                print("-------------------DETAILS-------------------\n")
                print(f"Title={reminder['title']}\nDescription={reminder['description']}\non {reminder['date']} at {reminder['time']}")
                print("\n---------------------------------------------")
                engine = pyttsx3.init()
                engine.say(f"Task '{reminder['date']}' found!")
                engine.runAndWait()
                found = True
        if not found:
            print("No task found with the mentioned date")
            engine = pyttsx3.init()
            engine.say("No task found with the mentioned date")
            engine.runAndWait()
    else:
        print("Invalid option")
        engine = pyttsx3.init()
        engine.say("Invalid option")
        engine.runAndWait()

def delete():
    
    global details

    if not details:
        print("No tasks to delete!")
        engine = pyttsx3.init()
        engine.say("No tasks to delete!")
        engine.runAndWait()
        return

    delete_title = input("Enter the title of the task you want to delete: ").strip().lower()

    found = False
    for reminder in details:
        if reminder['title'].lower() == delete_title:
            details.remove(reminder)
            save_list(details)
            found = True
            print(f"Task '{delete_title}' deleted successfully!")
            engine = pyttsx3.init()
            engine.say(f"Task '{delete_title}' deleted successfully!")
            engine.runAndWait()
            break

    if not found:
        print(f"No task found with the title '{delete_title}'")
        engine = pyttsx3.init()
        engine.say(f"No task found with the title '{delete_title}'")
        engine.runAndWait()
        

if __name__ == "__main__":
    main()