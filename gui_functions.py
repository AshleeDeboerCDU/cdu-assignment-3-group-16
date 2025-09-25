# gui_functions.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
# Assuming the models import is correct for context
from models import AIModelFactory, ModelConfigs, TextToImage, TextGeneration
import io  # Needed for Image saving logic


def exit_app(root):
    """Exits the application gracefully."""
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.quit()


def show_about():
    """Displays information about the application."""
    print("About dialog opened")
    messagebox.showinfo("About", "Tkinter AI GUI\nVersion 1.0\nCreated by Group 16")


def load_selected_model(model_combo, input_type_var, user_input_frame, model_output_frame):
    """
    Displays a messagebox with the selected item from the combobox.
    It also changes the GUI layout based on the model.
    """
    selected_model = model_combo.get()
    messagebox.showinfo("Model Loaded", f"{selected_model} Loaded")
    # Model initialisation
    model_configs = ModelConfigs(r"model_info.json")
    model_factory = AIModelFactory()
    model_configs.show_configs()

    # Clear all existing widgets from the frames to prepare for the new layout
    for widget in user_input_frame.winfo_children():
        widget.destroy()
    for widget in model_output_frame.winfo_children():
        widget.destroy()

    # Get the trace name for the old trace so we can delete it
    trace_name = input_type_var.trace_info()
    for mode, name in trace_name:
        if name and mode == "w":
            input_type_var.trace_vdelete("w", name)

    if selected_model == "Text-Generation":
        # Init model
        text_generator = model_factory.get_text_generation_model(model_configs)
        assert text_generator is not None, "Failed to load Text Generation model."

        # Create the widgets for the "Text-Generation" layout
        button_container = ttk.Frame(user_input_frame)
        button_container.pack(fill="x", pady=(0, 5))

        # *** Widgets ***
        input_text = tk.Text(user_input_frame, height=10, width=40)
        text_output_box = tk.Text(model_output_frame, height=10, width=30)

        # NOTE: Set unused variables to None for clear_fields
        output_image_label = None

        # Pack the new widgets and buttons
        input_text.pack(fill="both", expand=True)
        text_output_box.pack(fill="both", expand=True)

        # Output Button Frame (contains Save button)
        output_button_frame = ttk.Frame(model_output_frame)
        output_button_frame.pack(fill="x", pady=(5, 0))  # Pack at the bottom

        # Save Button (Text-Generation)
        save_button_output = ttk.Button(output_button_frame, text="Save Text")
        save_button_output.pack(side="left")

        bottom_button_frame = ttk.Frame(user_input_frame)
        bottom_button_frame.pack(fill="x", pady=5)
        run_model1_button = ttk.Button(bottom_button_frame, text=f"Generate {selected_model} Output")
        run_model1_button.pack(side="left", padx=(0, 5))

        clear_button = ttk.Button(bottom_button_frame, text="Clear")
        clear_button.pack(side="right")

        # We need to link the buttons to the new widgets
        run_model1_button.config(
            command=lambda: run_text_generation_model(text_generator, input_text, text_output_box))

        clear_button.config(
            command=lambda: clear_fields(input_text, text_output_box,
                                         output_image_label))

        # Link Save button
        save_button_output.config(command=lambda: save_text_output(text_output_box))

    elif selected_model == "Text-To-Image":
        # The existing "Text-To-Image" layout logic, now simplified for Text-Only Input
        image_generator = model_factory.get_text_to_image_model(model_configs)
        assert image_generator is not None, "Failed to load Text-to-Image model."

        # Force the input type to "Text"
        input_type_var.set("Text")

        # Create the buttons and widgets for this layout
        button_container = ttk.Frame(user_input_frame)
        button_container.pack(fill="x", pady=(0, 5))

        # *** CHANGE: Remove radio buttons and Image input logic ***
        input_prompt_label = ttk.Label(button_container, text="Text Prompt:")
        input_prompt_label.pack(side="left", padx=(0, 5))
        browse_button = ttk.Button(button_container, text="Load Text File")  # Renamed for clarity
        browse_button.pack(side="right")

        # *** Widgets for Text Input and Image Output ***
        input_text = tk.Text(user_input_frame, height=10, width=40)
        # We need to store the actual PIL image for saving, not just the label.
        # We'll attach it to the label as an attribute later.
        output_image_label = ttk.Label(model_output_frame, background="gray")
        output_image_label.pil_image = None  # New attribute to hold the PIL image

        # NOTE: Set unused variables to None for clear_fields
        output_text = None

        # Initial layout setup
        output_image_label.pack(fill="both", expand=True)  # Pack image first
        input_text.pack(fill="both", expand=True)

        # Output Button Frame (contains Save button)
        output_button_frame = ttk.Frame(model_output_frame)
        output_button_frame.pack(fill="x", pady=(5, 0))  # Pack at the bottom

        # Save Button (Text-To-Image)
        save_button_output = ttk.Button(output_button_frame, text="Save Image")
        save_button_output.pack(side="left")

        bottom_button_frame = ttk.Frame(user_input_frame)
        bottom_button_frame.pack(fill="x", pady=5)
        run_model1_button = ttk.Button(bottom_button_frame, text=f"Generate {selected_model} Output")
        run_model1_button.pack(side="left", padx=(0, 5))

        clear_button = ttk.Button(bottom_button_frame, text="Clear")
        clear_button.pack(side="right")

        browse_button.config(command=lambda: open_file_dialog(input_type_var, input_text, input_image_label,
                                                              layout_type="Text-To-Image"))

        run_model1_button.config(
            command=lambda: run_image_generation_model(image_generator, input_text, output_text, output_image_label)
        )

        clear_button.config(
            command=lambda: clear_fields(input_text, output_text,
                                         output_image_label)
        )

        # Link Save button
        save_button_output.config(command=lambda: save_image_output(output_image_label))


def clear_fields(input_text, output_text, output_image_label):
    if input_text:
        input_text.delete("1.0", tk.END)
    if output_text:
        output_text.delete("1.0", tk.END)

    if output_image_label:
        output_image_label.config(image="")
        output_image_label.image = None
        output_image_label.pil_image = None  # Also clear the PIL image reference

def open_file(input_type_var, input_text, input_image_label):
    """
    Opens a file dialog for the "Open" menu button.
    It runs the same function as the "Browse" button.
    """
    selected_type = input_type_var.get()
    layout_type = None

    if selected_type == "Text":
        layout_type = "Text-To-Image"


    if layout_type:
        open_file_dialog(input_type_var, input_text, input_image_label, layout_type)
    else:
        # This will happen if the model is Text-To-Image but input_type_var is not "Text"
        # (which shouldn't happen based on load_selected_model) or if no model is loaded.
        messagebox.showerror("Error", "Unsupported model or input type for file operation.")


def open_file_dialog(input_type_var, input_text, input_image_label, layout_type, new_width=None):

    # Logic for Text Input Model
    if layout_type in ("Text-To-Image", "Text-Generation"):

        if input_text is None:
            messagebox.showerror("Error", "Input text area not found.")
            return

        # Use input_text.master as the parent window for the file dialog.
        parent_widget = input_text.master

        filetypes = (
            ("Text files", "*.txt"),
            ("All files", "*.*")
        )
        filepath = filedialog.askopenfilename(
            parent=parent_widget,
            title="Open a text file",
            initialdir="/",
            filetypes=filetypes
        )

        if filepath:
            try:
                with open(filepath, 'r') as file:
                    content = file.read()
                    input_text.delete("1.0", tk.END)
                    input_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("File Error", f"Could not read file: {e}")


def run_image_generation_model(model_object: TextToImage, input_text, output_text, output_image_label):
    text_input = input_text.get("1.0", "end-1c").strip()

    if not text_input:
        messagebox.showwarning("Input Error", "Please enter a text prompt to generate an image.")
        return

    # 1. Generate the PIL Image object
    # The TextToImage model's generate_image() returns a PIL Image
    pil_image = model_object.generate_image(text_input)

    # 2. Store the PIL image directly on the label for saving later
    output_image_label.pil_image = pil_image

    # 3. Resize and convert the PIL Image for Tkinter display

    # Get the container's current size (after it has been packed)
    # Use winfo_width/height from the label itself, or its master
    container_width = output_image_label.winfo_width()
    container_height = output_image_label.winfo_height()

    if container_width <= 1 or container_height <= 1:
        # Fallback in case width/height hasn't been determined yet
        container_width = 300
        container_height = 300

    aspect_ratio = pil_image.width / pil_image.height

    # Calculate new dimensions to fit the container while maintaining aspect ratio
    if (container_width / aspect_ratio) <= container_height:
        new_width = container_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = container_height
        new_width = int(new_height * aspect_ratio)

    # Resize using Image.LANCZOS for high quality
    resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

    # Convert to PhotoImage for Tkinter
    tk_image = ImageTk.PhotoImage(resized_image)

    # 4. Configure the label
    output_image_label.config(image=tk_image)

    # IMPORTANT: Keep a reference to the PhotoImage object to prevent garbage collection
    output_image_label.image = tk_image



def run_text_generation_model(model_object: TextGeneration, input_text, output_text):
    messagebox.showinfo("Model Run", "Running Image-to-Text Model")
    generated_text = model_object.generate_response(input_text)[0]['generated_text']
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, generated_text)


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Save Functions
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

def save_text_output(output_text_widget):
    """Saves the content of the text widget to a file."""
    content = output_text_widget.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Save Error", "No text to save.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save Text Output"
    )

    if filepath:
        try:
            with open(filepath, 'w') as file:
                file.write(content)
            messagebox.showinfo("Save Success", f"Text successfully saved to {filepath}")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save file: {e}")


def save_image_output(output_image_label):
    """Saves the PIL image attached to the label to a file."""
    # Retrieve the PIL image object
    pil_image = getattr(output_image_label, 'pil_image', None)

    if pil_image is None:
        messagebox.showwarning("Save Error", "No image has been generated yet.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        ],
        title="Save Image Output"
    )

    if filepath:
        try:
            # Use the save method of the PIL Image object
            pil_image.save(filepath)
            messagebox.showinfo("Save Success", f"Image successfully saved to {filepath}")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save image: {e}")