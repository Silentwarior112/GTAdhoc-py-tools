import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from concurrent.futures import ProcessPoolExecutor
import configparser

# Function to load or create the configuration file
def load_config():
    config = configparser.ConfigParser()
    if os.path.exists('batchcompiler_config.ini'):
        config.read('batchcompiler_config.ini')
    else:
        config['Directories'] = {
            'adhoc_exe_path': '',
            'ad_files_dir': '',
            'output_dir': ''
        }
        with open('batchcompiler_config.ini', 'w') as configfile:
            config.write(configfile)
    return config

# Function to save the last used directories to the config file
def save_config(config):
    with open('batchcompiler_config.ini', 'w') as configfile:
        config.write(configfile)

def compile_ad_file(adhoc_exe_path, ad_files_dir, output_dir, ad_file, adhoc_version, compiled_files):
    ad_path = os.path.join(ad_files_dir, ad_file)
    adc_file = ad_file.replace('.ad', '.adc')
    adc_path = os.path.join(output_dir, adc_file)
    
    # Command to compile .ad file to .adc
    command = [
        adhoc_exe_path,
        'build',
        '-i', ad_path,
        '-o', adc_path,
        '-v', str(adhoc_version)
    ]
    
    # Run the command and capture the output
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
        compiled_files.append(ad_file)
    except subprocess.CalledProcessError as e:
        print("Error occurred while compiling", ad_file)
        print("Error message:", e.stderr)

def compile_ad_files(adhoc_exe_path, ad_files_dir, output_dir, adhoc_version, compiled_files_var):
    # List all .ad files in the directory
    ad_files = [f for f in os.listdir(ad_files_dir) if f.endswith('.ad')]
    compiled_files = []
    
    with ProcessPoolExecutor() as executor:
        # Submit compile task for each ad file
        futures = []
        for ad_file in ad_files:
            futures.append(executor.submit(compile_ad_file, adhoc_exe_path, ad_files_dir, output_dir, ad_file, adhoc_version, compiled_files))
        
        # Wait for all tasks to complete
        for future in futures:
            future.result()
    
    compiled_files_var.set(compiled_files)
    # Display popup when process is finished
    messagebox.showinfo("Success!", f"Compilation Complete.")

# Function to open directory dialog and update last used directory in the config file
def open_directory_dialog(entry_var, config, key, file_types=None):
    if file_types is None:
        file_types = [("All Files", "*.*")]
    directory_path = filedialog.askopenfilename(title=f"Select {key} File", initialdir=entry_var.get() or config['Directories'][key], filetypes=file_types)
    if directory_path:
        entry_var.set(directory_path)
        config['Directories'][key] = directory_path
        save_config(config)

# Function to open directory dialog and update last used directory in the config file
def open_folder_dialog(entry_var, config, key):
    directory_path = filedialog.askdirectory(title=f"Select {key} Directory", initialdir=entry_var.get() or config['Directories'][key])
    if directory_path:
        entry_var.set(directory_path)
        config['Directories'][key] = directory_path
        save_config(config)

def on_closing(root):
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Adhoc Toolchain Batch Compiler")
    root.geometry("640x480")  # Set window size
    
    adhoc_versions = {
        7: "Version 7 (GT4O/TT)",
        10: "Version 10 (GTHD/GT5 Prologue)",
        12: "Version 12 (GTPSP/GT5/GT6/GT Sport)"
    }
    
    adhoc_version_var = tk.IntVar(root, value=7)
    compiled_files_var = tk.StringVar()
    
    label = tk.Label(root, text="Select Adhoc Version:")
    label.pack(pady=5)
    
    option_menu = tk.OptionMenu(root, adhoc_version_var, *adhoc_versions.keys(), command=lambda _: None)
    option_menu.pack(pady=5)
    option_menu['menu'].delete(0, 'end')
    for version in adhoc_versions:
        option_menu['menu'].add_command(label=adhoc_versions[version], command=tk._setit(adhoc_version_var, version))
    
    config = load_config()
    
    adhoc_exe_entry_var = tk.StringVar(value=config['Directories']['adhoc_exe_path'])
    ad_files_entry_var = tk.StringVar(value=config['Directories']['ad_files_dir'])
    output_entry_var = tk.StringVar(value=config['Directories']['output_dir'])
    
    adhoc_exe_label = tk.Label(root, text="Adhoc.exe Path:")
    adhoc_exe_label.pack(pady=5)
    adhoc_exe_entry = tk.Entry(root, textvariable=adhoc_exe_entry_var, state='readonly')
    adhoc_exe_entry.pack(pady=5, padx=10, fill='x', expand=True)
    adhoc_exe_button = tk.Button(root, text="Browse", command=lambda: open_directory_dialog(adhoc_exe_entry_var, config, 'adhoc_exe_path', [("Executable Files", "*.exe")]))
    adhoc_exe_button.pack(pady=5, padx=10, fill='x', expand=True)
    
    ad_files_label = tk.Label(root, text="AD Files Directory:")
    ad_files_label.pack(pady=5)
    ad_files_entry = tk.Entry(root, textvariable=ad_files_entry_var, state='readonly')
    ad_files_entry.pack(pady=5, padx=10, fill='x', expand=True)
    ad_files_button = tk.Button(root, text="Browse", command=lambda: open_folder_dialog(ad_files_entry_var, config, 'ad_files_dir'))
    ad_files_button.pack(pady=5, padx=10, fill='x', expand=True)
    
    output_label = tk.Label(root, text="Output Directory:")
    output_label.pack(pady=5)
    output_entry = tk.Entry(root, textvariable=output_entry_var, state='readonly')
    output_entry.pack(pady=5, padx=10, fill='x', expand=True)
    output_button = tk.Button(root, text="Browse", command=lambda: open_folder_dialog(output_entry_var, config, 'output_dir'))
    output_button.pack(pady=5, padx=10, fill='x', expand=True)
    
    button = tk.Button(root, text="Compile AD Files", command=lambda: compile_ad_files(adhoc_exe_entry_var.get(), ad_files_entry_var.get(), output_entry_var.get(), adhoc_version_var.get(), compiled_files_var))
    button.pack(pady=20)
    
    root.mainloop()
