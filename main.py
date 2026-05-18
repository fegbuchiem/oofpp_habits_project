import sys
from habit import HabitTracker
import analytics

def print_help():
    """Prints the integrated command-line application documentation."""
    print("\n--- Help: How to Create and Manage Habits ---")
    print("1. To CREATE a new habit, select option [1] from the main menu.")
    print("   You will be asked to enter a 'Task Description' (e.g., 'Read a book')")
    print("   and a 'Periodicity' ('hourly', 'daily', 'weekly', or 'monthly').")
    print("2. To CHECK-OFF a habit, select option [2], then choose the habit's ID/Index.")
    print("3. To DELETE a habit, select option [3].")
    print("4. To ANALYZE your habits (streaks, periodicities), select option [4].")
    print("* At ANY prompt, type 'b' to go back to the previous menu, or 'q' / 'exit' to quit the app entirely.")
    print("---------------------------------------------")

def get_input(prompt: str) -> str:
    """
    Custom input wrapper to gracefully handle global back/exit commands.
    Returns 'BACK_ACTION' string if the user requests moving backward in the menu.
    """
    val = input(prompt).strip()
    low = val.lower()
    if low in ['q', 'quit', 'exit']:
        print("\nExiting Aabit. Run again soon to keep your streaks alive!")
        sys.exit(0)
    if low in ['b', 'back']:
        return "BACK_ACTION"
    return val

def print_welcome_sequence():
    """Displays a professional ASCII welcome and onboarding sequence."""
    print(r"""
    █████╗  █████╗ ██████╗ ██╗████████╗
   ██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝
   ███████║███████║██████╦╝██║   ██║   
   ██╔══██║██╔══██║██╔══██╗██║   ██║   
   ██║  ██║██║  ██║██████╦╝██║   ██║   
   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝   
===============================================
    """)
    print("Welcome to Aabit - The Professional Habit Tracking Ecosystem.\n")
    name = input("To get started, please enter your name: ").strip()
    if not name:
        name = "Hustler"
    print(f"\nHello, {name}! Let's build some powerful routines together.\n")
    print("--- About Aabit ---")
    print("Aabit allows you to architect and meticulously track your personal or professional habits.")
    print("With this tool, you can:")
    print("  • Create routines with Hourly, Daily, Weekly, or Monthly periodicities.")
    print("  • Check-off tasks on the fly to build unshakeable historical streaks.")
    print("  • Dive deep into powerful Analytics to monitor your exact progress and identify broken streaks.")
    print("  • Manage your entire lifestyle completely offline with instant JSON persistence.")
    print("-------------------\n")
    input("[Press Enter to proceed to the Main Menu...]")

def main():
    """Main interactive input loop fulfilling the CLI requirements."""
    tracker = HabitTracker()
    
    print_welcome_sequence()
    
    while True:
        print("\n=== Aabit Main Menu ===")
        print("1. Create New Habit")
        print("2. Check-off/Complete Habit")
        print("3. Delete Habit")
        print("4. View Analytics")
        print("5. Help & Documentation")
        print("6. Exit")
        
        choice = get_input("Select an option (1-6): ")
        if choice == 'BACK_ACTION':
            continue
            
        if choice == '1':
            task = get_input("Enter task description [Type 'b' to go back, 'q' to exit]: ")
            if task == 'BACK_ACTION': continue
            
            periodicity = get_input("Enter periodicity ('hourly', 'daily', 'weekly', 'monthly') [Type 'b' to go back, 'q' to exit]: ")
            if periodicity == 'BACK_ACTION': continue
            
            periodicity = periodicity.lower()
            if periodicity not in ['hourly', 'daily', 'weekly', 'monthly']:
                print("Invalid periodicity. Please choose 'hourly', 'daily', 'weekly', or 'monthly'.")
                continue
            habit = tracker.add_habit(task, periodicity)
            print(f"Success! Habit '{habit.task_description}' created.")
            
        elif choice == '2':
            if not tracker.habits:
                print("No active habits to check off.")
                continue
            for i, h in enumerate(tracker.habits):
                status = "BROKEN" if h.is_broken() else "Active"
                print(f"[{i}] {h.task_description} ({h.periodicity}) | Status: {status} | Streak: {h.get_streak()}")
            
            idx_str = get_input("\nEnter the index number to check off [Type 'b' to go back, 'q' to exit]: ")
            if idx_str == 'BACK_ACTION': continue
            
            try:
                idx = int(idx_str)
                habit = tracker.habits[idx]
                habit.check_off()
                tracker.save_data()
                print(f"Great! '{habit.task_description}' checked off. Current streak: {habit.get_streak()}")
            except (ValueError, IndexError):
                print("Invalid index selection.")
                
        elif choice == '3':
            if not tracker.habits:
                print("No active habits to delete.")
                continue
            for i, h in enumerate(tracker.habits):
                print(f"[{i}] {h.task_description} ({h.periodicity})")
            
            idx_str = get_input("\nEnter the index number to delete [Type 'b' to go back, 'q' to exit]: ")
            if idx_str == 'BACK_ACTION': continue
            
            try:
                idx = int(idx_str)
                habit_id = tracker.habits[idx].id
                tracker.delete_habit(habit_id)
                print("Habit securely deleted from persistence storage.")
            except (ValueError, IndexError):
                print("Invalid index selection.")
                
        elif choice == '4':
            print("\n--- Analytics Engine Menu ---")
            print("1. List all currently tracked habits")
            print("2. Return matching habits by periodicity")
            print("3. Return longest streak across all tracked habits")
            print("4. Return longest streak for a specific habit")
            print("5. Return to Main Menu")
            
            a_choice = get_input("\nSelect analytics query (1-5): ")
            if a_choice == '5' or a_choice == 'BACK_ACTION': continue
            
            if a_choice == '1':
                habits = analytics.get_all_habits(tracker.habits)
                print("\n[ All Tracked Habits ]")
                for h in habits:
                    print(f"- {h.task_description} ({h.periodicity})")
            elif a_choice == '2':
                period = get_input("Enter periodicity to filter by ('hourly', 'daily', 'weekly', 'monthly') [Type 'b' to go back, 'q' to exit]: ")
                if period == 'BACK_ACTION': continue
                
                filtered = analytics.get_habits_by_periodicity(tracker.habits, period.lower())
                print(f"\n[ Habits with '{period}' periodicity ]")
                for h in filtered:
                    print(f"- {h.task_description}")
            elif a_choice == '3':
                max_all = analytics.get_longest_streak_all(tracker.habits)
                print(f"\n=> Longest historical streak across ALL habits is: {max_all}")
            elif a_choice == '4':
                if not tracker.habits:
                    print("No active habits to analyze.")
                    continue
                for i, h in enumerate(tracker.habits):
                    print(f"[{i}] {h.task_description}")
                
                idx_str = get_input("\nEnter habit index to check streak [Type 'b' to go back, 'q' to exit]: ")
                if idx_str == 'BACK_ACTION': continue
                
                try:
                    idx = int(idx_str)
                    habit = tracker.habits[idx]
                    longest = analytics.get_longest_streak_habit(habit)
                    print(f"\n=> Longest historical streak for '{habit.task_description}' is: {longest}")
                except (ValueError, IndexError):
                    print("Invalid index selection.")
            else:
                print("Invalid analytics option. Returning to main menu.")
                
        elif choice == '5':
            print_help()
            
        elif choice == '6':
            print("\nExiting Aabit. Run again soon to keep your streaks alive!")
            sys.exit(0)
            
        else:
            print("Invalid selector. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting gracefully...")
        sys.exit(0)
