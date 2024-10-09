import json, os, sys
from tkinter import Tk, filedialog, Button, Label
from pathlib import Path
script_dir = Path(__file__).parent.absolute()

USERPROFILE = os.environ['USERPROFILE']
unmodded_bibite = {}
converted_bibite = {}
Template_Bibite = {}

window = Tk()
window.title('Convert Template To Modded')
window.geometry('700x400')

def openTemplateBibite(): # Open the template to use as template when converting
    global Template_Bibite
    Template_Bibite_Path = filedialog.askopenfilename(initialdir = f'{Template_BB8_folder}' , filetypes=[("Executable files", "*.bb8template")], title="Choose a bibite template to use as template when converting")
    if Template_Bibite_Path == '':
        return
    with open(Template_Bibite_Path, "r") as bibite_file:
        Template_Bibite = json.load(bibite_file)
    open_template_label.config(text=f'Opened Template: {os.path.basename(Template_Bibite_Path)}') # Display opened bibite template

def loadBibite(): # Open the bibite you want to convert
    global unmodded_bibite
    Bibite_Path = filedialog.askopenfilename(initialdir = f'{USERPROFILE}/AppData/LocalLow/The Bibites/The Bibites/Bibites/Templates' , filetypes=[("Executable files", "*.bb8template")], title="Choose a bibite template to convert")
    if Bibite_Path == '':
        return
    with open(Bibite_Path, "r") as bibite_file:
        unmodded_bibite = json.load(bibite_file)
    open_bibite_label.config(text=f'Opened: {os.path.basename(Bibite_Path)}')

def saveBibite():
    Bibite_Path = filedialog.askopenfilename(initialdir = f'{USERPROFILE}/AppData/LocalLow/The Bibites/The Bibites/Bibites/Templates' , filetypes=[("Executable files", "*.bb8template")], title="Choose a bibite template to overwrite with the converted bibite")
    with open(Bibite_Path, "w") as bibite_file:
        json.dump(converted_bibite, bibite_file, indent=4)

def convertBibite(): # Convert the bibite to be compatible with the modded template
    global converted_bibite, unmodded_bibite, Template_Bibite

    # Copy the original bibite to preserve the original structure
    converted_bibite = unmodded_bibite.copy()

    # Flag to track if changes were made
    changes_made = False

    # Iterate through each node in the template and ensure the converted bibite has the same structure
    for template_node in Template_Bibite["nodes"]:
        index = template_node["Index"]
        corresponding_node = next((n for n in converted_bibite["nodes"] if n["Index"] == index), None)

        if not corresponding_node:
            # Node is missing in the unmodded bibite, insert it
            converted_bibite["nodes"].append(template_node)
            print(f"Added missing node with index {template_node['Index']}.")
            changes_made = True

    # Sort nodes based on the Index to maintain order after modifications
    converted_bibite["nodes"].sort(key=lambda n: n["Index"])

    # Update synapses with new node indices
    for synapse in converted_bibite["synapses"]:
        for template_node in Template_Bibite["nodes"]:
            if synapse['NodeIn'] == template_node['Index']:
                print(f"Updated NodeIn from {synapse['NodeIn']} to {template_node['Index']}")
                synapse['NodeIn'] = template_node['Index']

            if synapse['NodeOut'] == template_node['Index']:
                print(f"Updated NodeOut from {synapse['NodeOut']} to {template_node['Index']}")
                synapse['NodeOut'] = template_node['Index']

    # Check and update the version number if needed
    if converted_bibite["version"] != Template_Bibite["version"]:
        converted_bibite["version"] = Template_Bibite["version"]
        print(f"Updated version to {Template_Bibite['version']}")
        changes_made = True

    # Display status update in the UI
    converted_bibite["name"]
    if changes_made:
        status_label.config(text="Conversion completed successfully!")
    else:
        status_label.config(text="No changes were made during conversion.")

    # Print the converted bibite to the console for debugging
    print(json.dumps(converted_bibite, indent=4))

if getattr(sys, 'frozen', False):
    # Running as compiled executable
    Template_BB8_folder = 'Template bb8'
else:
    # Running as a standalone Python script
    Template_BB8_folder = f'{script_dir}/Template bb8'

if not os.path.exists(Template_BB8_folder):
    os.makedirs(Template_BB8_folder)

open_template_label = Label(window, text="No Template open to use as refrence", font=("Arial", 15))
open_template_label.pack(pady=10)

open_bibite_label = Label(window, text="No bibite open", font=("Arial", 15))
open_bibite_label.pack(pady=10)

open_template_button = Button(window, text="Open Template Bibite", command=openTemplateBibite, font=("Arial", 12))
open_template_button.pack(pady=10)

load_bibite_button = Button(window, text="Open bibite you want to convert", command=loadBibite, font=("Arial", 12))
load_bibite_button.pack(pady=10)

convert_bibite_button = Button(window, text="Convert bibite", command=convertBibite, font=("Arial", 12))
convert_bibite_button.pack(pady=10)

convert_bibite_button = Button(window, text="Save converted bibite", command=saveBibite, font=("Arial", 12))
convert_bibite_button.pack(pady=10)

# Status Label
status_label = Label(window, text="", font=("Arial", 12))
status_label.pack(side="bottom", anchor="s", pady=20)

# Runs the app
window.mainloop()