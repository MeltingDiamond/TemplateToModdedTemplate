import json, os, sys, time
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

def convertBibite():  # Convert the bibite to be compatible with the modded template
    global converted_bibite, unmodded_bibite, Template_Bibite

    # Copy the original bibite to preserve the original structure
    converted_bibite = unmodded_bibite.copy()

    # Iterate over nodes in Template_Bibite to find missing nodes
    for template_node in Template_Bibite["nodes"]:
        # List to hold tuples of (original_index, new_index)
        changed_indexes = []

        index = template_node["Index"]
        
        # Check if this node exists in converted_bibite
        existing_node = next((converted_node for converted_node in converted_bibite["nodes"] if converted_node == template_node), None)

        if not existing_node:
            # If the node does not exist, insert it at the correct position
            # Find the insertion point
            insert_index = next((i for i, node in enumerate(converted_bibite["nodes"]) if node["Index"] >= index), len(converted_bibite["nodes"]))
            converted_bibite["nodes"].insert(insert_index, template_node)

            print(f"Inserted node with index {template_node['Index']} at index {insert_index}.")

            # Update indices of every node that follows by one
            for j in range(insert_index + 1, len(converted_bibite["nodes"])):
                original_following_index = converted_bibite["nodes"][j]["Index"]
                converted_bibite["nodes"][j]["Index"] += 1  # Increment index by 1
                changed_indexes.append((original_following_index, original_following_index + 1))
                print(f"Updated node index from {original_following_index} to {converted_bibite['nodes'][j]['Index']}.")

    # Update synapses based on changed node indexes
    if converted_bibite["synapses"] is not None:
        for synapse in converted_bibite["synapses"]:
            # Check if NodeIn needs to be changed
            for index, new_index in changed_indexes:
                if synapse['NodeIn'] == index:
                    synapse['NodeIn'] = new_index
                    print(f"Changed NodeIn from {index} to {new_index}")
                    break  # Exit the inner loop after changing

            # Check if NodeOut needs to be changed
            for index, new_index in changed_indexes:
                if synapse['NodeOut'] == index:
                    synapse['NodeOut'] = new_index
                    print(f"Changed NodeOut from {index} to {new_index}")
                    break  # Exit the inner loop after changing

    # Ensure version matches
    if converted_bibite["version"] != Template_Bibite["version"]:  # Update version if it is different
        converted_bibite["version"] = Template_Bibite["version"]

    # Update status label
    name = converted_bibite["name"]
    status_label.config(text=f"{name} converted hopefully it still works the same")
    
    # Print the bibite to the console for debugging
    print(json.dumps(converted_bibite, indent=4))

if getattr(sys, 'frozen', False):
    # Running as compiled executable
    Template_BB8_folder = 'Template bb8'
else:
    # Running as a standalone Python script
    Template_BB8_folder = f'{script_dir}/Template bb8'

if not os.path.exists(Template_BB8_folder): # Make folder if it does not exist
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
status_label.pack(side="bottom", anchor="s", pady=15)

# Runs the app
window.mainloop()