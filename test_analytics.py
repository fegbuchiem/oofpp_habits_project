import pytest
import datetime
from habit import Habit
import analytics

@pytest.fixture
def sample_habits():
    # Setup Pre-defined dummy models
    h1 = Habit("Daily 1", "daily")
    today = datetime.datetime.now()
    h1.completion_history = [(today - datetime.timedelta(days=i)).isoformat() for i in range(5)]
    
    h2 = Habit("Weekly 1", "weekly")
    
    h3 = Habit("Daily 2", "daily")
    h3.completion_history = [(today - datetime.timedelta(days=i)).isoformat() for i in range(10)]
    return [h1, h2, h3]

def test_get_all_habits(sample_habits):
    result = analytics.get_all_habits(sample_habits)
    assert len(result) == 3
    # FP check: returned list should not mutate or be same object reference to original array block
    assert result is not sample_habits

def test_get_habits_by_periodicity(sample_habits):
    dailies = analytics.get_habits_by_periodicity(sample_habits, "daily")
    weeklies = analytics.get_habits_by_periodicity(sample_habits, "weekly")
    assert len(dailies) == 2
    assert len(weeklies) == 1

def test_get_longest_streak_habit(sample_habits):
    # h3 has exactly 10 checkoffs strictly daily without break
    longest = analytics.get_longest_streak_habit(sample_habits[2])
    assert longest == 10

def test_get_longest_streak_all(sample_habits):
    # Out of 5 (h1), 0 (h2), 10 (h3) -> 10 should win
    longest = analytics.get_longest_streak_all(sample_habits)
    assert longest == 10
