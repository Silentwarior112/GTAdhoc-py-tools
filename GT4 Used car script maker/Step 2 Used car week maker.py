import csv
import os
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def generate_script(input_file, num_dealers, dealer_ranges, num_weeks, prevent_duplicates, sort_option):
    # Read input CSV file
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader if row]  # Exclude empty rows
        guarantee_list = set(tuple(row) for row in rows)

    # Initialize output scripts
    output_scripts = []

    # Iterate over weeks
    for week in range(num_weeks):
        output_script = f"module UsedCarData\n{{\n"
    
        # Track selected entries for guaranteeing unique entries
        selected_entries = []
        week = []

        # Iterate over dealers
        for dealer_idx in range(num_dealers):
            # Retrieve dealer's quantity and year range
            min_quantity, max_quantity, min_year, max_year = dealer_ranges[dealer_idx]
    
            # Filter rows based on the dealer's year range
            available_rows = [row for row in rows if min_year <= int(row[2]) <= max_year]
            guarantee_rows = list(row for row in guarantee_list if min_year <= int(row[2]) <= max_year)
            
            # Randomly select quantity within the range for the dealer
            quantity = min(max_quantity, len(available_rows), random.randint(min_quantity, max_quantity))
    
            dealer_name = f"usedcar_{str(dealer_idx).zfill(2)}"
            output_script += f"\tstatic {dealer_name}_carnum = {quantity};\n"
            output_script += f"\tstatic {dealer_name}_carlist = [\n"
            total_quantity = quantity
            dupe_loop_counter = 0
    
            # Select random entries from the filtered rows for the dealer
            while quantity > 0:
                selected_entry = None
                while not selected_entry:
                    if guarantee_rows:
                        entry = random.choice(guarantee_rows)
                        entry_label = entry[0]  # Extract label from entry
                        entry_color = entry[4]
                        # Check if the entry has been selected before and if it's a duplicate
                        if prevent_duplicates and entry_label in week:
                            print (f"Guarantee logic: Duplicate car `{entry_label}` picked in the same week. Trying again...")
                            # Fallback logic when guarantee list runs low
                            if dupe_loop_counter > total_quantity:
                                specific_rows = [row for row in available_rows if row not in selected_entries]
                                entry = random.choice(specific_rows)
                                entry_label = entry[0]  # Extract label from entry
                                entry_color = entry[4]
                                if prevent_duplicates and entry_label in week:
                                    print (f"Guarantee2 logic: Duplicate car `{entry_label}` picked in the same week. Trying again...")
                                    continue
                                selected_entry = entry
                                print (f"Guarantee2 logic: Picked `{entry_label}` Variation {entry_color}")
                                selected_entries.append(selected_entry)
                                week.append(entry_label)
                            else:
                                dupe_loop_counter += 1
                                continue
                        else:
                            selected_entry = entry
                            print (f"Guarantee logic: Picked `{entry_label}` Variation {entry_color}")
                            selected_entries.append(selected_entry)
                            week.append(entry_label)
                            guarantee_list.discard(selected_entry)
                    else:
                        entry = random.choice(available_rows)
                        entry_label = entry[0]  # Extract label from entry
                        entry_color = entry[4]
                        # Check if the entry has been selected before and if it's a duplicate
                        if prevent_duplicates and entry_label in week:
                            print (f"Random logic: Duplicate car `{entry_label}` picked in the same week. Trying again...")
                            continue
                        selected_entry = entry
                        print (f"Random logic: Picked `{entry_label}` Variation {entry_color}")
                        selected_entries.append(selected_entry)
                        week.append(entry_label)
                quantity -= 1
            
            if sort_option == "year":
                selected_entries_list = sorted(selected_entries, key=lambda entry: entry[2])
            elif sort_option == "price":
                selected_entries_list = sorted(selected_entries, key=lambda entry: entry[1])
            elif sort_option == "random":
                selected_entries_list = list(selected_entries)
                
            for entry in selected_entries_list:
                usedcar_value = entry[0]
                output_script += f'\t\t"{usedcar_value}",\n'
            
            output_script += f"\t];\n"
            output_script += f"\tstatic color_{str(dealer_idx).zfill(2)}_carnum = {total_quantity};\n"
            output_script += f"\tstatic color_{str(dealer_idx).zfill(2)}_carlist = [\n"
    
            for entry in selected_entries_list:
                color_value = int(entry[4]) - 1 # Script reads VarOrder from 0 instead of 1, Adhoc Toolchain doesn't account for this so we do it here
                output_script += f'\t\t"{color_value}",\n'
    
            output_script += f"\t];\n\n"
            
            week.clear()
            selected_entries.clear()
            
        output_script += "}\n"
        output_scripts.append(output_script)

    return output_scripts


def open_ranges_window():
    global ranges_window
    global entry_min_quantities, entry_max_quantities, entry_min_years, entry_max_years
    
    # Destroy existing ranges window if it exists
    if ranges_window is not None:
        ranges_window.destroy()
    
    num_dealers = int(entry_num_dealers.get())
    
    ranges_window = tk.Toplevel(root)
    ranges_window.title("Dealer Ranges")
    
    # Dealer Quantity Ranges
    label_quantities = ttk.Label(ranges_window, text="Dealer Quantity Ranges:")
    label_quantities.grid(row=0, column=0, sticky=tk.W)

    entry_min_quantities = []
    entry_max_quantities = []
    for i in range(num_dealers):
        label_min = ttk.Label(ranges_window, text=f"Min for Dealer {i+1}:")
        label_min.grid(row=i+1, column=0, sticky=tk.W)
        entry_min = ttk.Entry(ranges_window, width=10)
        entry_min.grid(row=i+1, column=1, sticky=(tk.W, tk.E))
        entry_min_quantities.append(entry_min)

        label_max = ttk.Label(ranges_window, text=f"Max for Dealer {i+1}:")
        label_max.grid(row=i+1, column=2, sticky=tk.W)
        entry_max = ttk.Entry(ranges_window, width=10)
        entry_max.grid(row=i+1, column=3, sticky=(tk.W, tk.E))
        entry_max_quantities.append(entry_max)

    # Dealer Year Ranges
    label_year_ranges = ttk.Label(ranges_window, text="Dealer Year Ranges:")
    label_year_ranges.grid(row=num_dealers+1, column=0, sticky=tk.W)

    entry_min_years = []
    entry_max_years = []
    for i in range(num_dealers):
        label_min_year = ttk.Label(ranges_window, text=f"Min Year for Dealer {i+1}:")
        label_min_year.grid(row=num_dealers+2+i, column=0, sticky=tk.W)
        entry_min_year = ttk.Entry(ranges_window, width=10)
        entry_min_year.grid(row=num_dealers+2+i, column=1, sticky=(tk.W, tk.E))
        entry_min_years.append(entry_min_year)

        label_max_year = ttk.Label(ranges_window, text=f"Max Year for Dealer {i+1}:")
        label_max_year.grid(row=num_dealers+2+i, column=2, sticky=tk.W)
        entry_max_year = ttk.Entry(ranges_window, width=10)
        entry_max_year.grid(row=num_dealers+2+i, column=3, sticky=(tk.W, tk.E))
        entry_max_years.append(entry_max_year)

ranges_window = None
        
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def generate():
    input_file = entry_file_path.get()
    num_dealers = int(entry_num_dealers.get())
    num_weeks = int(entry_num_weeks.get())
    prevent_duplicates = prevent_duplicates_var.get()  # New checkbox variable
    sort_option = selected_sort_option.get()

    dealer_ranges = []
    for i in range(num_dealers):
        min_quantity = int(entry_min_quantities[i].get())
        max_quantity = int(entry_max_quantities[i].get())
        min_year = int(entry_min_years[i].get())  # Added
        max_year = int(entry_max_years[i].get())  # Added
        dealer_ranges.append((min_quantity, max_quantity, min_year, max_year))  # Modified

    # Create a folder for the output files if it doesn't exist
    output_folder = "usedcar_generated"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_scripts = generate_script(input_file, num_dealers, dealer_ranges, num_weeks, prevent_duplicates, sort_option)

    for idx, script in enumerate(output_scripts):
        output_file_path = os.path.join(output_folder, f"US_used{str(idx).zfill(4)}.ad")
        with open(output_file_path, "w") as script_file:
            script_file.write(script)
    messagebox.showinfo("Success", "Scripts generated successfully!")

# Create GUI
root = tk.Tk()
root.title("GT4 Used car week maker")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# File Path
label_file_path = ttk.Label(frame, text="Base list:")
label_file_path.grid(row=0, column=0, sticky=tk.W)
entry_file_path = ttk.Entry(frame, width=40)
entry_file_path.grid(row=0, column=1, sticky=(tk.W, tk.E))
btn_browse = ttk.Button(frame, text="Browse", command=browse_file)
btn_browse.grid(row=0, column=2, sticky=tk.W)

# Number of Dealers
label_num_dealers = ttk.Label(frame, text="Number of Dealers: (Default = 3)")
label_num_dealers.grid(row=1, column=0, sticky=tk.W)
entry_num_dealers = ttk.Entry(frame, width=10)
entry_num_dealers.grid(row=1, column=1, sticky=(tk.W, tk.E))
entry_num_dealers.insert(0, '3')

# Button to open ranges window
btn_open_ranges = ttk.Button(frame, text="Set Dealer Ranges", command=open_ranges_window)
btn_open_ranges.grid(row=2, column=0, columnspan=2, pady=(10, 0))

# Number of Weeks
label_num_weeks = ttk.Label(frame, text="Number of Weeks: (Default = 100)")
label_num_weeks.grid(row=10, column=0, sticky=tk.W)
entry_num_weeks = ttk.Entry(frame, width=10)
entry_num_weeks.grid(row=10, column=1, sticky=(tk.W, tk.E))
entry_num_weeks.insert(0, '100')

# Checkbox for Prevent Duplicates
prevent_duplicates_var = tk.BooleanVar()
chk_prevent_duplicates = ttk.Checkbutton(frame, text="Prevent duplicate cars within the same week", variable=prevent_duplicates_var)
chk_prevent_duplicates.grid(row=12, column=0, sticky=tk.W)

# Radio buttons for sorting options
selected_sort_option = tk.StringVar()

# Radio button for Random order in dealers
random_button = ttk.Radiobutton(frame, text="Random order in dealers", variable=selected_sort_option, value="random")
random_button.grid(row=13, column=0, sticky=tk.W)

# Radio button for Sort dealers by model year
year_button = ttk.Radiobutton(frame, text="Sort dealers by model year", variable=selected_sort_option, value="year")
year_button.grid(row=14, column=0, sticky=tk.W)

# Radio button for Sort dealers by price
price_button = ttk.Radiobutton(frame, text="Sort dealers by price", variable=selected_sort_option, value="price")
price_button.grid(row=15, column=0, sticky=tk.W)

# Generate Button
btn_generate = ttk.Button(frame, text="Generate Scripts", command=generate)
btn_generate.grid(row=16, column=0, columnspan=4, pady=(20, 0))

root.mainloop()
