# Habit Tracking Application - Python Backend Portfolio Project

This is a Habit Tracking Application built purely in Python 3, adhering strictly to object-oriented and functional programming paradigms for the IU university assignment.

## Installation Instructions

1. Ensure you have **Python 3.7+** installed correctly on your system.
2. Clone or unpack the repository into your preferred local directory.
3. Establish a standard Python virtual environment (optional but highly recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # or
   .\venv\Scripts\activate   # Windows
   ```
4. Install exactly one required third-party dependency for testing:
   ```bash
   pip install pytest
   ```

## Predefined Test Data Generation

To populate your `habits.json` database with exactly 5 predefined active habits containing 4 weeks of historical mock data (validating streaks and breaks):

```bash
python test_data_generator.py
```

## Running the Application

To start the pure Python CLI interactive experience:

```bash
python main.py
```

## Usage Examples

1. **Creating a Habit:** Select Option `1` in the menu. Enter your goal (e.g. "Read 10 pages") and define the periodicity (`daily` or `weekly`).
2. **Checking off tasks:** Select Option `2`. The CLI will print active routines and whether their streaks are fundamentally broken. Target an index to mark it as successfully completed for today.
3. **Analyzing:** Enter Option `4` to invoke the Functional Programming analytics. You can pull the max historical streaks across single items, entire tracking histories, or filter by periodic schemas.

## Testing Instructions

Automated validity verifications of streak evaluation calculus and functional programming bounds mapping sit inside `test_habit.py` and `test_analytics.py`. Evaluate via pytest:

```bash
pytest
```
