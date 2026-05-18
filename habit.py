import uuid
import json
import datetime
from typing import List, Dict, Optional

class Habit:
    """
    Class representing a single trackable habit.
    Adheres to Object-Oriented Programming principles.
    """
    
    def __init__(self, task_description: str, periodicity: str, creation_date: Optional[str] = None, completion_history: Optional[List[str]] = None, habit_id: Optional[str] = None):
        self.id = habit_id or str(uuid.uuid4())
        self.task_description = task_description
        self.periodicity = periodicity.lower()
        self.creation_date = creation_date or datetime.datetime.now().isoformat()
        self.completion_history = completion_history or []

    def get_creation_date(self) -> str:
        return self.creation_date

    def check_off(self, timestamp: Optional[str] = None):
        time_to_add = timestamp or datetime.datetime.now().isoformat()
        self.completion_history.append(time_to_add)

    def get_streak(self) -> int:
        if not self.completion_history:
            return 0
        dts = sorted([datetime.datetime.fromisoformat(ts) for ts in self.completion_history])
        streak = 1
        
        if self.periodicity == 'hourly':
            hours = sorted(list(set(datetime.datetime(d.year, d.month, d.day, d.hour) for d in dts)))
            for i in range(1, len(hours)):
                diff = (hours[i] - hours[i-1]).total_seconds() / 3600
                if diff == 1: streak += 1
                elif diff > 1: streak = 1
                
        elif self.periodicity == 'daily':
            dates = sorted(list(set(d.date() for d in dts)))
            for i in range(1, len(dates)):
                diff = (dates[i] - dates[i-1]).days
                if diff == 1: streak += 1
                elif diff > 1: streak = 1
                
        elif self.periodicity == 'weekly':
            weeks = sorted(list(set(d.date().isocalendar() for d in dts)))
            for i in range(1, len(weeks)):
                year_diff = weeks[i][0] - weeks[i-1][0]
                week_diff = weeks[i][1] - weeks[i-1][1]
                if year_diff == 0 and week_diff == 1: streak += 1
                elif year_diff == 1 and ((weeks[i-1][1] in [52, 53]) and weeks[i][1] == 1): streak += 1
                else: streak = 1
                
        elif self.periodicity == 'monthly':
            months = sorted(list(set((d.year, d.month) for d in dts)))
            for i in range(1, len(months)):
                diff = (months[i][0] - months[i-1][0]) * 12 + (months[i][1] - months[i-1][1])
                if diff == 1: streak += 1
                elif diff > 1: streak = 1
                
        return streak

    def is_broken(self) -> bool:
        today = datetime.datetime.now()
        
        if not self.completion_history:
            ref = datetime.datetime.fromisoformat(self.creation_date)
        else:
            dts = sorted([datetime.datetime.fromisoformat(ts) for ts in self.completion_history])
            ref = dts[-1]
            
        if self.periodicity == 'hourly':
            ref_hour = datetime.datetime(ref.year, ref.month, ref.day, ref.hour)
            today_hour = datetime.datetime(today.year, today.month, today.day, today.hour)
            return (today_hour - ref_hour).total_seconds() / 3600 > 1

        elif self.periodicity == 'daily':
            return (today.date() - ref.date()).days > 1
            
        elif self.periodicity == 'weekly':
            cy, cw, _ = ref.date().isocalendar()
            ty, tw, _ = today.date().isocalendar()
            if ty == cy:
                return (tw - cw) > 1
            elif ty == cy + 1:
                return not (cw in [52, 53] and tw == 1)
            else:
                return True
                
        elif self.periodicity == 'monthly':
            return ((today.year - ref.year) * 12 + (today.month - ref.month)) > 1
            
        return False

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "task_description": self.task_description,
            "periodicity": self.periodicity,
            "creation_date": self.creation_date,
            "completion_history": self.completion_history
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            task_description=data['task_description'],
            periodicity=data['periodicity'],
            creation_date=data['creation_date'],
            completion_history=data['completion_history'],
            habit_id=data['id']
        )

class HabitTracker:
    def __init__(self, storage_file: str = "habits.json"):
        self.storage_file = storage_file
        self.habits: List[Habit] = []
        self.load_data()

    def add_habit(self, task_description: str, periodicity: str) -> Habit:
        habit = Habit(task_description, periodicity)
        self.habits.append(habit)
        self.save_data()
        return habit
        
    def delete_habit(self, habit_id: str):
        self.habits = [h for h in self.habits if h.id != habit_id]
        self.save_data()

    def get_habit_by_id(self, habit_id: str) -> Optional[Habit]:
        for h in self.habits:
            if h.id == habit_id:
                return h
        return None

    def save_data(self):
        with open(self.storage_file, 'w') as f:
            json.dump([h.to_dict() for h in self.habits], f, indent=4)

    def load_data(self):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.habits = [Habit.from_dict(d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.habits = []
