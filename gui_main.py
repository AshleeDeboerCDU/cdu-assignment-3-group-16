import tkinter as tk
from tkinter import ttk
import models

# Import the functions separate file
import gui_functions


# Create the main window
root = tk.Tk()
root.title("Tkinter AI GUI")
root.geometry("800x800") # Adjust size as needed

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Menu Bar
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=lambda: gui_functions.exit_app(root))

# Create Models menu
models_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Models", menu=models_menu)
models_menu.add_command(label="Load Model", command=lambda: gui_functions.load_selected_model(model_combo, input_type_var, user_input_frame, model_output_frame))

# Create Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=gui_functions.show_about)

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Model Selection
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Create a frame for the Model Selection section
model_selection_frame = ttk.Frame(root, padding="10")
model_selection_frame.pack(fill="x", padx=10, pady=5)

# Model Selection label
model_label = ttk.Label(model_selection_frame, text="Model Selection:")
model_label.pack(side="left", padx=(0, 5))

# Dropdown for model selection
model_configs = models.ModelConfigs(r"model_info.json")
model_options = [k for k in model_configs.show_configs().keys()]
model_combo = ttk.Combobox(model_selection_frame, values=model_options)
model_combo.set("Text-To-Image")
model_combo.pack(side="left", fill="x", expand=True, padx=(0, 10))

# Load Model button
load_button = ttk.Button(model_selection_frame, text="Load Model", command=lambda: gui_functions.load_selected_model(model_combo, input_type_var, user_input_frame, model_output_frame))
load_button.pack(side="right")


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Main Sections Frame
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

main_sections_frame = ttk.Frame(root, padding="10")
main_sections_frame.pack(fill="both", expand=True, padx=10, pady=5)

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   User Input Section
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# We'll give this frame a fixed width
user_input_frame = ttk.LabelFrame(main_sections_frame, text="User Input Section", padding="10", width=350)
user_input_frame.pack(side="left", fill="both", padx=(0, 5))
user_input_frame.pack_propagate(False) # Prevents the frame from resizing to fit its contents

input_type_var = tk.StringVar(value="Text")

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Model Output Section
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# We'll give this frame a fixed width as well
model_output_frame = ttk.LabelFrame(main_sections_frame, text="Model Output Section", padding="10", width=350)
model_output_frame.pack(side="right", fill="both", padx=(5, 0))
model_output_frame.pack_propagate(False) # Prevents the frame from resizing to fit its contents

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Initial Layout Creation
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# We will call the load_selected_model function once at the start to create the initial layout
# We're passing a placeholder for input_text and other widgets because they will be created by the function
gui_functions.load_selected_model(model_combo, input_type_var, user_input_frame, model_output_frame)


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Info Sections
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

info_sections_frame = ttk.Frame(root, padding="10")
info_sections_frame.pack(fill="x", padx=10, pady=5)

# Create Selected Model Info section
model_info_frame = ttk.LabelFrame(info_sections_frame, text="Model Information & Explanation", padding="10")
model_info_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

# Selected Model Info sub-frame
selected_info_frame = ttk.LabelFrame(model_info_frame, text="Selected Model Info:", padding="10")
selected_info_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

# Display points for Selected Model Info
model_name_label = ttk.Label(selected_info_frame, text="• Model Name")
model_name_label.pack(anchor="w")

category_label = ttk.Label(selected_info_frame, text="• Category (Text, Vision, Audio)")
category_label.pack(anchor="w")

description_label = ttk.Label(selected_info_frame, text="• Short Description")
description_label.pack(anchor="w")

# OOP Concepts Explanation sub-frame
oop_concepts_frame = ttk.LabelFrame(model_info_frame, text="OOP Concepts Explanation:", padding="10")
oop_concepts_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

# Display points for OOP Concepts
multiple_inheritance_label = ttk.Label(oop_concepts_frame, text="• Where Multiple Inheritance are used")
multiple_inheritance_label.pack(anchor="w")

encapsulation_label = ttk.Label(oop_concepts_frame, text="• Why Encapsulation was applied")
encapsulation_label.pack(anchor="w")

polymorphism_label = ttk.Label(oop_concepts_frame, text="• How Polymorphism and Method Overriding are shown")
polymorphism_label.pack(anchor="w")

decorators_label = ttk.Label(oop_concepts_frame, text="• Where Multiple Decorators are applied")
decorators_label.pack(anchor="w")

# Create a frame for notes
notes_frame = ttk.Frame(root, padding="10")
notes_frame.pack(fill="x", padx=10, pady=5)

notes_label = ttk.Label(notes_frame, text="Notes Extra notes, instructions, or references.")
notes_label.pack(side="left")


# Start the main loop
root.mainloop()