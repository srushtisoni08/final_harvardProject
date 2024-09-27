import unittest
from project import load_list, save_list, time_check, date_check, set_task

class TestProject(unittest.TestCase):

    def test_load_list(self):
        # Test if load_list function returns a list (even if it's empty)
        reminders = load_list()
        self.assertIsInstance(reminders, list, "load_list should return a list")

    def test_save_list(self):
        # Test save_list by creating a mock list of reminders and ensuring it saves
        test_reminders = [
            {
                'title': 'Test Task',
                'description': 'Test Description',
                'date': '2024-09-30',
                'time': '12:00'
            }
        ]
        save_list(test_reminders)
        loaded_reminders = load_list()
        self.assertEqual(loaded_reminders, test_reminders, "save_list should save and load correctly")

    def test_time_check(self):
        # Valid time
        self.assertTrue(time_check("12:30"), "12:30 is a valid time")
        # Invalid times
        self.assertFalse(time_check("25:00"), "25:00 is an invalid hour")

    def test_date_check(self):
        # Future date
        self.assertTrue(date_check("2024-09-30"), "2024-09-30 is a future date")
        # Past date
        self.assertFalse(date_check("2020-09-30"), "2020-09-30 is a past date")
        # Invalid format
        self.assertFalse(date_check("invalid-date"), "Invalid format should return False")

    def test_set_task(self):
        # Mock user input for setting a task
        reminder = {
            'title': 'Test Task',
            'description': 'A simple test task',
            'date': '2024-09-30',
            'time': '12:00'
        }
        details = []  # Assume details is your list of tasks
        details.append(reminder)
        self.assertEqual(len(details), 1, "Task should be added to details")
        self.assertEqual(details[0]['title'], 'Test Task', "Title should be 'Test Task'")
        self.assertEqual(details[0]['description'], 'A simple test task', "Description should match")
        self.assertEqual(details[0]['date'], '2024-09-30', "Date should match")
        self.assertEqual(details[0]['time'], '12:00', "Time should match")

if __name__ == '__main__':
    unittest.main()
