import datetime
from habit import HabitTracker

def generate_predefined_data():
    """
    Requirements:
    - 5 predefined habits (min 1 weekly, 1 daily) 
    - Generate 4 weeks of example tracking data
    - Different streak types (broken, unbroken)
    """
    tracker = HabitTracker()
    # Reset existing database for cleanliness
    tracker.habits = []
    
    today = datetime.datetime.now()
    # Exactly 4 weeks (28 days) ago timeline origin
    start_date = today - datetime.timedelta(days=28)
    
    # 1) Daily Habit - Unbroken 4 weeks
    h1 = tracker.add_habit("Drink 2L Water", "daily")
    h1.creation_date = (start_date - datetime.timedelta(days=1)).isoformat()
    h1.completion_history = []
    # 28 continuous check-offs
    for i in range(28):
        dt = (start_date + datetime.timedelta(days=i)).isoformat()
        h1.completion_history.append(dt)
        
    # 2) Daily Habit - Broken Streak (Multiple resets)
    h2 = tracker.add_habit("Jogging 3km", "daily")
    h2.creation_date = (start_date - datetime.timedelta(days=1)).isoformat()
    h2.completion_history = []
    # Completed days 0-10, miss some, then 15-20
    for i in range(11):
        h2.completion_history.append((start_date + datetime.timedelta(days=i)).isoformat())
    for i in range(15, 21):
        h2.completion_history.append((start_date + datetime.timedelta(days=i)).isoformat())

    # 3) Weekly Habit - Unbroken 4 weeks
    h3 = tracker.add_habit("Deep Cleaning", "weekly")
    h3.creation_date = (start_date - datetime.timedelta(days=1)).isoformat()
    h3.completion_history = []
    # One check-off every 7 days (4 times total covering 4 weeks)
    for i in range(4):
        h3.completion_history.append((start_date + datetime.timedelta(days=i*7)).isoformat())
        
    # 4) Weekly Habit - Broken Streak
    h4 = tracker.add_habit("Call Family", "weekly")
    h4.creation_date = (start_date - datetime.timedelta(days=1)).isoformat()
    h4.completion_history = []
    # Completed week 1 and week 3, missing week 2
    h4.completion_history.append(start_date.isoformat())
    h4.completion_history.append((start_date + datetime.timedelta(days=14)).isoformat())
    h4.completion_history.append((start_date + datetime.timedelta(days=21)).isoformat())

    # 5) Daily Habit - Small recent active streak
    h5 = tracker.add_habit("Read 15 Pages", "daily")
    # Even if created 4 weeks ago, barely checked off
    h5.creation_date = (start_date - datetime.timedelta(days=1)).isoformat()
    h5.completion_history = []
    h5.completion_history.append((today - datetime.timedelta(days=2)).isoformat())
    h5.completion_history.append((today - datetime.timedelta(days=1)).isoformat())
    h5.completion_history.append(today.isoformat())

    tracker.save_data()
    print("Successfully generated 5 test habits with 4 weeks of sample tracking data.")
    print("Data saved to persistence layer (habits.json).")

if __name__ == "__main__":
    generate_predefined_data()
