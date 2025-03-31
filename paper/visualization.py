import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data from results.csv
# Assume the CSV has columns: "Puzzle Type", "Correct Groups (4-word basis)", "Puzzle Solving Time", 
# "Difficulty (out of 10)", and "Hint Requests"
df = pd.read_csv('results.csv')

# Function to convert time data into minutes
def convert_to_minutes(time_str):
    if pd.isna(time_str) or str(time_str).strip() == '':
        return 0
    time_str = str(time_str).strip()
    if 'minutes' in time_str and 'seconds' in time_str:
        minutes = int(time_str.split('minutes')[0].strip())
        seconds = int(time_str.split('minutes')[1].replace('seconds', '').strip())
        return minutes + (seconds / 60)
    elif 'minutes' in time_str:
        return float(time_str.replace('minutes', '').strip())
    elif ':' in time_str:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes + (seconds / 60)
    return 0

# 1. Average Puzzle Solving Time Visualization
# Extract puzzle types and their solving times from the CSV
puzzle_types = df['Puzzle Type'].unique()
solving_times = {puzzle: [] for puzzle in puzzle_types}

# Group solving times by puzzle type
for index, row in df.iterrows():
    puzzle_type = row['Puzzle Type']
    time_str = row['Puzzle Solving Time']
    solving_times[puzzle_type].append(convert_to_minutes(time_str))

# Calculate average times (excluding zeros)
average_times = {}
for puzzle in puzzle_types:
    times = [t for t in solving_times[puzzle] if t > 0]  # Exclude zero times (missing data)
    average_times[puzzle] = np.mean(times) if times else 0

# Visualization for average solving time
plt.figure(figsize=(10, 6))
bars = plt.bar(list(average_times.keys()), list(average_times.values()), 
               color=['#FF9999', '#66B2FF', '#99FF99'])
plt.title('Average Puzzle Solving Time', fontsize=14, pad=15)
plt.xlabel('Puzzle Type', fontsize=12)
plt.ylabel('Average Time (minutes)', fontsize=12)
plt.grid(axis='y', alpha=0.75)

# Display values on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Print statistics for solving times
print("\nAverage Puzzle Solving Time Statistics:")
for puzzle, avg_time in average_times.items():
    print(f"{puzzle}: {avg_time:.2f} minutes")

# 2. Puzzle Correct Rate Comparison
# Calculate correct rates based on "Correct Groups (4-word basis)" (assuming 4 is full correct)
correct_counts = {puzzle: [] for puzzle in puzzle_types}
for index, row in df.iterrows():
    puzzle_type = row['Puzzle Type']
    correct_count = row['Correct Groups (4-word basis)']
    if pd.notna(correct_count):
        correct_counts[puzzle_type].append(correct_count)

correct_rates = []
for puzzle in puzzle_types:
    total_possible = len(correct_counts[puzzle]) * 4  # Each puzzle should have 4 correct groups max
    total_correct = sum(correct_counts[puzzle])
    rate = (total_correct / total_possible) * 100 if total_possible > 0 else 0
    correct_rates.append(rate)

# Visualization for correct rate
plt.figure(figsize=(10, 6))
bars = plt.bar(puzzle_types, correct_rates, color=['#FF9999', '#66B2FF', '#99FF99'])

plt.title('Puzzle Correct Rate Comparison', fontsize=14, pad=15)
plt.xlabel('Puzzle Type', fontsize=12)
plt.ylabel('Correct Rate (%)', fontsize=12)
plt.ylim(0, 100)

# Adding percentages on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}%',
             ha='center', va='bottom')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Print statistics for correct rates
print("\nPuzzle Correct Rate Statistics:")
for puzzle, rate in zip(puzzle_types, correct_rates):
    print(f"{puzzle}: {rate:.1f}% correct rate")

# 3. Average Difficulty Visualization
# Extract difficulty scores from CSV
difficulty_data = {puzzle: [] for puzzle in puzzle_types}
for index, row in df.iterrows():
    puzzle_type = row['Puzzle Type']
    difficulty = row['Difficulty (out of 10)']
    if pd.notna(difficulty):
        difficulty_data[puzzle_type].append(float(difficulty))

# Calculate average difficulty
avg_difficulties = {puzzle: np.mean(scores) if scores else 0 
                   for puzzle, scores in difficulty_data.items()}

# Visualization for difficulty
plt.figure(figsize=(10, 6))
plt.bar(list(avg_difficulties.keys()), list(avg_difficulties.values()), 
        color=['#FF9999', '#66B2FF', '#99FF99'])
plt.title('Average Difficulty per Puzzle (Out of 10)', fontsize=14)
plt.xlabel('Puzzle Type', fontsize=12)
plt.ylabel('Average Difficulty Score', fontsize=12)
plt.ylim(0, 10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Display average values above each bar
for i, v in enumerate(list(avg_difficulties.values())):
    plt.text(i, v + 0.2, f'{v:.2f}', ha='center', fontsize=12)

plt.show()

# Print statistics for difficulty
print("\nAverage Difficulty Statistics:")
for puzzle, avg_diff in avg_difficulties.items():
    print(f"{puzzle}: {avg_diff:.2f} out of 10")

# 4. Average Hint Requests Visualization
# Extract hint requests from CSV
hint_requests = {puzzle: [] for puzzle in puzzle_types}
for index, row in df.iterrows():
    puzzle_type = row['Puzzle Type']
    hints = row['Hint Requests']
    if pd.notna(hints):
        hint_requests[puzzle_type].append(float(hints) if str(hints).replace('.', '').isdigit() else 0)

# Calculate average hint requests
avg_hints = {puzzle: np.mean(requests) if requests else 0 
             for puzzle, requests in hint_requests.items()}

# Visualization for hint requests
plt.figure(figsize=(8, 6))
plt.bar(list(avg_hints.keys()), list(avg_hints.values()), 
        color=['#FF9999', '#66B2FF', '#99FF99'])
plt.title('Average Hint Requests per Puzzle', fontsize=14)
plt.xlabel('Puzzle Type', fontsize=12)
plt.ylabel('Average Number of Hint Requests', fontsize=12)
plt.ylim(0, max(list(avg_hints.values())) + 0.5)
for i, v in enumerate(list(avg_hints.values())):
    plt.text(i, v + 0.05, f'{v:.2f}', ha='center', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Print statistics for hint requests
print("\nAverage Hint Requests Statistics:")
for puzzle, avg_hint in avg_hints.items():
    print(f"{puzzle}: {avg_hint:.2f} hints")
