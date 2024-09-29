# Reminder Application

#### Video Demo: https://youtu.be/xfYxMB9kzv8

A simple reminder application that allows users to set, view, edit, search, and delete reminders. The application uses voice notifications and saves reminders in a JSON file for persistence.

## Features

- Set reminders with a title, description, date, and time.
- View all active reminders.
- Edit existing reminders.
- Search reminders by title or date.
- Delete reminders.
- Voice notifications for reminders.
- Log file for tracking saved reminders.

## Requirements

To run this application, you need the following dependencies:

- `Python 3.x`
- `pyttsx3`
- `datetime`
- `dateutil.parser`

You can install the required packages using:

```bash
pip install -r requirements.txt
```

## Files

- **project.py**: The main application script.
- **list.json**: Stores reminders in JSON format.
- **requirements.txt**: Lists the required Python packages.
- **reminder.log**: Log file capturing application events.

## Usage

1. Run the application:
   ```bash
   python project.py
   ```

2. Follow the prompts to add, view, edit, search, or delete reminders.

3. Reminders will be saved in `list.json` and can be reviewed upon the next application start.

## Explanation of Code

The Reminder Application consists of several key components:

1. **Setting Reminders**:
   - The `set_task()` function prompts the user for reminder details (title, description, date, and time).
   - It validates the inputs using `time_check()` and `date_check()` functions to ensure correct formats.
   - Valid reminders are appended to the `details` list and saved in `list.json` using the `save_list()` function.

2. **Storing and Loading Reminders**:
   - Reminders are stored in a JSON file (`list.json`). The `load_list()` function reads this file at the start of the application to retrieve existing reminders.

3. **Checking Reminders**:
   - The `check_reminders()` function runs in a separate thread, checking every minute if the current time matches any reminder's scheduled time.
   - When a match is found, it calls the `alert()` function to notify the user with a voice prompt and a pop-up.

4. **Viewing and Managing Reminders**:
   - Users can view reminders through the `view()` function, edit them with `edit()`, search using the `search()` function, and delete them with `delete()`.
   - Each operation updates the `details` list and saves changes back to `list.json`.

5. **Thread Safety with Tkinter**:
   - The application uses a `queue` to safely handle message pop-ups in the main Tkinter thread. The `process_message_queue()` function processes this queue to show alerts.

6. **Logging**:
   - The application logs events (like saving reminders) to a log file (`reminder.log`) using Python's `logging` module, providing a record of actions taken by the application.
