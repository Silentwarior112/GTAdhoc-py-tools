import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

def generic_car_to_genericlist1(input_file):
    # Hardcoded column indices to read
    columns_to_read = [1, 4, 5]  # Python index starts from 0, so 2nd column is index 1, 5th is index 4, 6th is index 5

    # Define output file name
    output_file = os.path.join("database", "list_step_1.csv")

    # Read input CSV and write selected columns to output CSV
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        next(reader)  # Skip header row
        
        for row in reader:
            selected_row = [row[i] for i in columns_to_read]
            writer.writerow(selected_row)

    print(f"Selected columns from '{input_file}' saved to '{output_file}'.")
    
def process_files_and_create_genericlist2(american_file, generic_list1_file):
    # Define output file name for generic_list2
    generic_list2_file = os.path.join("database", "list_step_2.csv")

    # Create a dictionary to store Label-Variation ID mappings
    label_variation_map = {}

    # Read American CSV file and store Label-Variation ID mappings
    with open(american_file, 'r') as american_csv:
        american_reader = csv.reader(american_csv)
        next(american_reader)  # Skip header row
        for row in american_reader:
            label = row[1]  # Column 2 = Label
            variation_id = row[2]  # Column 3 = Variation ID
            label_variation_map[label] = variation_id

    # Read generic_list1 CSV file, append Variation IDs, and save to generic_list2
    with open(generic_list1_file, 'r') as generic_list1_csv, \
            open(generic_list2_file, 'w', newline='') as generic_list2_csv:
        generic_list1_reader = csv.reader(generic_list1_csv)
        generic_list2_writer = csv.writer(generic_list2_csv)

        # Iterate over rows in generic_list1
        for row in generic_list1_reader:
            label = row[0]  # Assuming Label is in column 1
            if label in label_variation_map:
                variation_id = label_variation_map[label]
                row.append(variation_id)  # Append Variation ID to the row
            generic_list2_writer.writerow(row)

    print(f"Variation IDs added to list_step_1 and saved as list_step_2: '{generic_list2_file}'.")
    
def step2_select():
    # Select American CSV file
    american_file = filedialog.askopenfilename(title="Select CAR_VARIATION_[region].csv",
                                               filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not american_file:
        return  # Exit if file selection canceled

    # Select generic_list1 CSV file
    generic_list1_file = filedialog.askopenfilename(title="Select the list_step_1 CSV file",
                                                     filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not generic_list1_file:
        return  # Exit if file selection canceled

    # Process files
    process_files_and_create_genericlist2(american_file, generic_list1_file)

def step1_select():
    file_path = filedialog.askopenfilename(title="Select GENERIC_CAR.csv",
                                           filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        generic_car_to_genericlist1(file_path)
        
def extract_labels(file_path):
    labels = []
    with open(file_path, 'r') as file:
        content = file.read()
        modules = re.findall(r'module\s+(NewCarData|LegendCarData|CompleteCarData|PresentData)\s*{([^}]*)}', content, re.DOTALL)
        for module_name, module_content in modules:
            statics = re.findall(r'static\s+(\w+)\s*=\s*\[([^]]*)\];', module_content)
            for static_name, static_values in statics:
                if module_name == "PresentData" and static_name != "content_carlist":
                    continue
                label_values = re.findall(r'"([^"]+)"', static_values)
                labels.extend(label_values)
    return sorted(list(set(labels)))

def browse_file():
    file_path = filedialog.askopenfilename(title="Select carlist.ad",
                                               filetypes=[("AD files", "*.ad"), ("All files", "*.*")])
    if file_path:
        labels = extract_labels(file_path)
        save_labels(labels)

def save_labels(labels):
    # Define the path to the ruleout_list.csv file
    labels_file = 'database/ruleout_list.csv'
    
    # Save labels to the labels.csv file
    with open(labels_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Labels'])
        for label in labels:
            writer.writerow([label])
    
    print("Rule out list created.")
            
def remove_labels_from_genericlist2(rule_out_file, generic_list2_file):
    # Define output file name for generic_list3
    generic_list3_file = os.path.join("database", "list_step_3.csv")

    # Read rule-out list and store labels
    rule_out_labels = set()
    with open(rule_out_file, 'r') as rule_out_csv:
        rule_out_reader = csv.reader(rule_out_csv)
        for row in rule_out_reader:
            rule_out_labels.add(row[0])  # Assuming Label is in column 1

    # Read generic_list2, remove rows with matching labels, and save as generic_list3
    with open(generic_list2_file, 'r') as generic_list2_csv, \
            open(generic_list3_file, 'w', newline='') as generic_list3_csv:
        generic_list2_reader = csv.reader(generic_list2_csv)
        generic_list3_writer = csv.writer(generic_list3_csv)

        # Iterate over rows in generic_list2
        for row in generic_list2_reader:
            label = row[0]  # Assuming Label is in column 1
            if label not in rule_out_labels:
                generic_list3_writer.writerow(row)

    print(f"Labels removed from list_step_2 and saved as list_step_3: '{generic_list3_file}'.")

def select_files_and_process():
    # Display warning popup
    response = messagebox.askquestion("Warning", "Make sure that you have accounted for special cases that appear in the used car dealership, and also somewhere else. Special cases include cars that only appear at specific weeks such as the black edition variants, or cars that appear in the used dealership, but have a prize-only special color variant, such as  mgf_vvc_97, etc. You can remove the special cases from the rule out list as needed, and make sure to take note of which cars you removed from it before continuing. That way, the next steps will generate the used car entries for them, then you can edit the outputted base list after step 5, and selectively remove the specific variations that you do not want to appear in the used dealership. Continue?", icon='warning')
    
    # Check user response
    if response == 'no':
        return  # Exit function if user cancels
        

    # Select rule-out CSV file
    rule_out_file = filedialog.askopenfilename(title="Select the Rule Out CSV file",
                                               filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not rule_out_file:
        return  # Exit if file selection canceled

    # Select generic_list2 CSV file
    generic_list2_file = filedialog.askopenfilename(title="Select the list_step_2 CSV file",
                                                     filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not generic_list2_file:
        return  # Exit if file selection canceled

    # Process files
    remove_labels_from_genericlist2(rule_out_file, generic_list2_file)
    
def generate_genericlist4_from_genericlist3(generic_list3_file, variation_file):
    # Define output file name for generic_list4
    generic_list4_file = os.path.join("database", "Base list.csv")

    # Create a dictionary to store Variation ID to VarOrders mappings
    variation_mapping = {}
    
    print ("Generating Base list...")

    # Read variation CSV file and store matching rows
    with open(variation_file, 'r') as variation_csv:
        variation_reader = csv.reader(variation_csv)
        next(variation_reader)  # Skip the header row
        for row in variation_reader:
            variation_id = row[0]
            var_order = row[3].strip()  # Assuming VarOrder is in column 4
            if variation_id in variation_mapping:
                variation_mapping[variation_id].append(var_order)
            else:
                variation_mapping[variation_id] = [var_order]

    # Collect rows for generic_list4
    rows_for_generic_list4 = []

    # Read generic_list3 CSV file and duplicate rows for each matching Variation ID
    with open(generic_list3_file, 'r') as generic_list3_csv:
        generic_list3_reader = csv.reader(generic_list3_csv)

        for row in generic_list3_reader:
            variation_id = row[3]  # Assuming Variation ID is in column 4
            var_orders = variation_mapping.get(variation_id, [])
            for var_order in var_orders:
                rows_for_generic_list4.append(row[:4] + [var_order])  # Add row to list for generic_list4

    # Write to generic_list4 CSV file
    with open(generic_list4_file, 'w', newline='') as generic_list4_csv:
        generic_list4_writer = csv.writer(generic_list4_csv)
    
        # Write rows to generic_list4
        generic_list4_writer.writerows(rows_for_generic_list4)
    
    print(f"Rows duplicated from list_step_3 and saved as Base list: '{generic_list4_file}'.")
    
    # Reopen generic_list4 CSV file for sorting
    with open(generic_list4_file, 'r', newline='') as generic_list4_csv:
        reader = csv.reader(generic_list4_csv)
        rows = list(reader)
    
    # Sort rows alphabetically by column 1
    sorted_rows = sorted(rows, key=lambda x: x[0])
    
    # Write sorted rows back to the generic_list4 CSV file
    with open(generic_list4_file, 'w', newline='') as generic_list4_csv:
        generic_list4_writer = csv.writer(generic_list4_csv)
    
    
        # Write sorted rows to generic_list4
        generic_list4_writer.writerows(sorted_rows)
    
    print(f"Base list sorted alphabetically by column 1.")

def select_files_and_process_for_step4():
    # Select generic_list3 CSV file
    generic_list3_file = filedialog.askopenfilename(title="Select the list_step_3 CSV file",
                                                     filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not generic_list3_file:
        return  # Exit if file selection canceled

    # Select variation CSV file
    variation_file = filedialog.askopenfilename(title="Select the VARIATION_[region] CSV file",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not variation_file:
        return  # Exit if file selection canceled

    # Process files
    generate_genericlist4_from_genericlist3(generic_list3_file, variation_file)

def main():
    # Create main window
    root = tk.Tk()
    root.title("GT4 Used car list maker")
    root.geometry("300x450")  # Set window size

    # Add button for step 1
    select_button = tk.Button(root, text="Step 1: Generic_car --> list_step_1", command=step1_select)
    select_button.pack(pady=20)
    
    # Add button for step 2
    process_button = tk.Button(root, text="Step 2: list_step_1 --> list_step_2", command=step2_select)
    process_button.pack(pady=20)
    
    # Add button for step 3
    process_button = tk.Button(root, text="Step 3: Create rule out list", command=browse_file)
    process_button.pack(pady=20)
    
    # Add button for step 4
    process_button = tk.Button(root, text="Step 4: Rule out cars", command=select_files_and_process)
    process_button.pack(pady=20)
    
    # Add button for step 5
    process_button = tk.Button(root, text="Step 5: Generate base list", command=select_files_and_process_for_step4)
    process_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
