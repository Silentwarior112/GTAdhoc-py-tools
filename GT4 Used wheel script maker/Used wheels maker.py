import tkinter as tk
from tkinter import scrolledtext
import random

def convert_list_to_sections(input_list, num_sections, max_entries_per_section, split_by_four_letters):
    sections = []
    if num_sections <= 0 and max_entries_per_section <= 0 and not split_by_four_letters:
        return sections

    if split_by_four_letters:
        sections_dict = {}
        for item in input_list:
            key = item[:4]
            if key not in sections_dict:
                sections_dict[key] = []
            sections_dict[key].append(item)
        
        sections = list(sections_dict.values())
    else:
        if num_sections > 0:
            # Calculate the number of elements in each section
            elements_per_section = len(input_list) // num_sections
            remainder = len(input_list) % num_sections

            # Populate the sections
            start_index = 0
            for i in range(num_sections):
                end_index = start_index + elements_per_section + (1 if i < remainder else 0)
                section = input_list[start_index:end_index]
                sections.append(section)
                start_index = end_index
        else:
            # Divide the list based on maximum entries per section
            for i in range(0, len(input_list), max_entries_per_section):
                section = input_list[i:i+max_entries_per_section]
                sections.append(section)

    return sections

def format_output(sections):
    formatted_output = ""
    for i, section in enumerate(sections):
        formatted_output += f"    static used{i:02d}_carnum = {len(section)};\n\n"
        formatted_output += f"    static used{i:02d}_carlist = [\n"
        for item in section:
            formatted_output += f"       \"{item}\",\n"
        formatted_output += "    ];\n\n"
    return formatted_output

def process_input():
    input_text = input_textbox.get("1.0", tk.END)
    input_list = [line.strip() for line in input_text.split("\n") if line.strip()]
    
    if randomize_checkbox_var.get():
        random.shuffle(input_list)
    
    num_sections = int(section_entry.get()) if section_type.get() == "Sections" else 0
    max_entries_per_section = int(section_entry.get()) if section_type.get() == "Max Entries per Section" else 0
    split_by_four_letters = section_type.get() == "Split by First 4 Letters"
    
    sections = convert_list_to_sections(input_list, num_sections, max_entries_per_section, split_by_four_letters)
    formatted_output = format_output(sections)
    output_textbox.delete("1.0", tk.END)
    output_textbox.insert("1.0", formatted_output)

# Create the main window
root = tk.Tk()
root.title("List to Sections Converter")

# Input Textbox
input_label = tk.Label(root, text="Paste the input list below:")
input_label.pack()
input_textbox = scrolledtext.ScrolledText(root, width=50, height=10)
input_textbox.pack()

# Section Type Radiobuttons
section_type = tk.StringVar(value="Sections")

section_type_label = tk.Label(root, text="Choose section division method:")
section_type_label.pack()

sections_radio = tk.Radiobutton(root, text="Define Number of Sections", variable=section_type, value="Sections")
sections_radio.pack()

max_entries_radio = tk.Radiobutton(root, text="Define Max Entries per Section", variable=section_type, value="Max Entries per Section")
max_entries_radio.pack()

split_by_four_radio = tk.Radiobutton(root, text="Split by First 4 Letters", variable=section_type, value="Split by First 4 Letters")
split_by_four_radio.pack()

# Number of Sections or Max Entries Entry
section_label = tk.Label(root, text="Enter the number of sections or max entries per section:")
section_label.pack()
section_entry = tk.Entry(root)
section_entry.pack()

# Randomize Checkbox
randomize_checkbox_var = tk.BooleanVar()
randomize_checkbox = tk.Checkbutton(root, text="Randomize Input List", variable=randomize_checkbox_var)
randomize_checkbox.pack()

# Process Button
process_button = tk.Button(root, text="Process", command=process_input)
process_button.pack()

# Output Textbox
output_label = tk.Label(root, text="Formatted Output:")
output_label.pack()
output_textbox = scrolledtext.ScrolledText(root, width=50, height=20)
output_textbox.pack()

# Run the main event loop
root.mainloop()
