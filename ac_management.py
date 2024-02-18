import tkinter as tk
import time

class TableManagementSystem:
    def __init__(self, num_tables):
        self.num_tables = num_tables
        self.tables = {table_num: None for table_num in range(1, num_tables + 1)}

    def take_table(self, table_num):
        if table_num not in self.tables:
            return f"Table {table_num} does not exist."

        if self.tables[table_num] is not None:
            return f"Table {table_num} is already taken."

        current_time = time.time()
        self.tables[table_num] = current_time
        return f"Table {table_num} taken at {time.ctime(current_time)}."

    def release_table(self, table_num):
        if table_num not in self.tables:
            return f"Table {table_num} does not exist."

        if self.tables[table_num] is None:
            return f"Table {table_num} is not taken."

        current_time = time.time()
        duration = current_time - self.tables[table_num]
        self.tables[table_num] = None
        return f"Table {table_num} released after {duration:.2f} seconds."

    def get_table_status(self, table_num):
        if table_num not in self.tables:
            return "Does not exist"
        elif self.tables[table_num] is None:
            return "Available"
        else:
            return "Taken"

    def get_all_table_statuses(self):
        return {table_num: self.get_table_status(table_num) for table_num in self.tables.keys()}

    def calculate_acs_needed(self):
        num_tables_taken = sum(1 for status in self.tables.values() if status is not None)
        if num_tables_taken < 3:
            return 1
        elif num_tables_taken < 6:
            return 2
        elif num_tables_taken < 8:
            return 3
        else:
            return 4

def update_stopwatch():
    table_statuses = restaurant.get_all_table_statuses()
    for table_num, status in table_statuses.items():
        if status == "Taken":
            duration = time.time() - restaurant.tables[table_num]
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            stopwatch_text = f"{hours:02}:{minutes:02}:{seconds:02}"
            table_labels[table_num - 1].config(text=f"Table {table_num}\nTaken: {stopwatch_text}")
    window.after(1000, update_stopwatch)

def table_clicked(table_num):
    if restaurant.get_table_status(table_num) == "Available":
        result = restaurant.take_table(table_num)
    else:
        result = restaurant.release_table(table_num)
    result_label.config(text=result)
    update_table_status()

    # Update the number of air conditioners needed
    acs_needed_label.config(text=f"Air Conditioners Needed: {restaurant.calculate_acs_needed()}")

def update_table_status():
    table_statuses = restaurant.get_all_table_statuses()
    for table_num, status in table_statuses.items():
        if status == "Available":
            table_labels[table_num - 1].config(bg="green", text=f"Table {table_num}\nAvailable")
        elif status == "Taken":
            duration = time.time() - restaurant.tables[table_num]
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            stopwatch_text = f"{hours:02}:{minutes:02}:{seconds:02}"
            table_labels[table_num - 1].config(bg="red", text=f"Table {table_num}\nTaken: {stopwatch_text}")

# Create a Tkinter window
window = tk.Tk()
window.title("Table Management System")

# Create a TableManagementSystem instance
restaurant = TableManagementSystem(num_tables=10)

# Create widgets
table_labels = []
for i in range(1, 11):
    row_num = (i - 1) // 5  # Calculate the row number for the current table
    col_num = (i - 1) % 5   # Calculate the column number for the current table

    table_frame = tk.Frame(window, width=150, height=100, relief="solid", borderwidth=1)
    table_frame.grid(row=row_num, column=col_num, padx=5, pady=5)

    table_label = tk.Label(table_frame, text=f"Table {i}\nAvailable", width=15, height=5, relief="solid", borderwidth=1)
    table_label.pack(expand=True, fill="both")

    table_label.bind("<Button-1>", lambda event, table_num=i: table_clicked(table_num))
    table_labels.append(table_label)

result_label = tk.Label(window, text="", wraplength=200)
result_label.grid(row=2, column=0, columnspan=5, pady=5)

# Label to display the number of air conditioners needed
acs_needed_label = tk.Label(window, text="", wraplength=200)
acs_needed_label.grid(row=3, column=0, columnspan=5, pady=5)

# Start the stopwatch
update_stopwatch()

# Start the Tkinter event loop
window.mainloop()
