import pytest
import os
import datetime
from habit import Habit, HabitTracker

def test_habit_creation():
    h = Habit("Test Task", "daily")
    assert h.task_description == "Test Task"
    assert h.periodicity == "daily"
    assert len(h.completion_history) == 0

def test_habit_check_off():
    h = Habit("Test Task", "weekly")
    h.check_off()
    assert len(h.completion_history) == 1

def test_habit_daily_streak():
    h = Habit("Daily Task", "daily")
    today = datetime.datetime.now()
    h.completion_history = [(today - datetime.timedelta(days=2)).isoformat(),
                            (today - datetime.timedelta(days=1)).isoformat(),
                            today.isoformat()]
    assert h.get_streak() == 3

def test_habit_is_broken():
    h = Habit("Daily Task", "daily")
    # Set creation to 3 days ago, and NO completions ensures daily task breaks
    h.creation_date = (datetime.datetime.now() - datetime.timedelta(days=3)).isoformat()
    assert h.is_broken() == True

    # Test broken with completions
    h2 = Habit("Daily Task", "daily")
    today = datetime.datetime.now()
    h2.completion_history = [(today - datetime.timedelta(days=5)).isoformat(),
                             (today - datetime.timedelta(days=4)).isoformat()]
    assert h2.is_broken() == True

def test_habit_tracker_persistence():
    test_file = "test_habits.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    tracker = HabitTracker(test_file)
    tracker.add_habit("Persistent Task", "daily")
    assert len(tracker.habits) == 1
    
    # Reload tracker from file
    tracker2 = HabitTracker(test_file)
    assert len(tracker2.habits) == 1
    assert tracker2.habits[0].task_description == "Persistent Task"
    
    if os.path.exists(test_file):
        os.remove(test_file)
