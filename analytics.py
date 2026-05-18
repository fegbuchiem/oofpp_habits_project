from functools import reduce
from typing import List
import datetime

# We expect these analytics functions to act on a list of Habit objects.
# To obey pure Functional Programming principles, they do not mutate state and avoid side-effects.

def get_all_habits(habits: List) -> List:
    return list(habits)

def get_habits_by_periodicity(habits: List, period: str) -> List:
    return list(filter(lambda h: h.periodicity == period.lower(), habits))

def _calculate_longest_streak(completion_history: List[str], periodicity: str) -> int:
    if not completion_history:
        return 0
        
    # Process ISO strings to unique date objects
    dts = sorted([datetime.datetime.fromisoformat(ts) for ts in completion_history])
    if not dts:
        return 0
        
    max_streak = 1
    current_streak = 1
    
    if periodicity == 'hourly':
        items = sorted(list(set(datetime.datetime(d.year, d.month, d.day, d.hour) for d in dts)))
        for i in range(1, len(items)):
            diff = (items[i] - items[i-1]).total_seconds() / 3600
            if diff == 1: current_streak += 1
            elif diff > 1: current_streak = 1
            max_streak = max(max_streak, current_streak)
            
    elif periodicity == 'daily':
        items = sorted(list(set(d.date() for d in dts)))
        for i in range(1, len(items)):
            diff = (items[i] - items[i-1]).days
            if diff == 1: current_streak += 1
            elif diff > 1: current_streak = 1
            max_streak = max(max_streak, current_streak)
            
    elif periodicity == 'weekly':
        weeks = sorted(list(set(d.date().isocalendar() for d in dts)))
        for i in range(1, len(weeks)):
            year_diff = weeks[i][0] - weeks[i-1][0]
            week_diff = weeks[i][1] - weeks[i-1][1]
            if year_diff == 0 and week_diff == 1: current_streak += 1
            elif year_diff == 1 and ((weeks[i-1][1] in [52, 53]) and weeks[i][1] == 1): current_streak += 1
            else: current_streak = 1
            max_streak = max(max_streak, current_streak)
            
    elif periodicity == 'monthly':
        months = sorted(list(set((d.year, d.month) for d in dts)))
        for i in range(1, len(months)):
            diff = (months[i][0] - months[i-1][0]) * 12 + (months[i][1] - months[i-1][1])
            if diff == 1: current_streak += 1
            elif diff > 1: current_streak = 1
            max_streak = max(max_streak, current_streak)
            
    return max_streak

def get_longest_streak_habit(habit) -> int:
    return _calculate_longest_streak(habit.completion_history, habit.periodicity)

def get_longest_streak_all(habits: List) -> int:
    if not habits:
        return 0
    streaks = map(lambda h: get_longest_streak_habit(h), habits)
    return reduce(lambda x, y: max(x, y), streaks, 0)
