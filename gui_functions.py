# gui_functions.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk


def open_file(input_type_var, input_text, input_image_label):
    """
    Opens a file dialog for the "Open" menu button.
    It runs the same function as the "Browse" button.
    """
    selected_type = input_type_var.get()
    layout_type = None  # Assign a default value

    # We'll use the "Text-to-Image" layout logic for the menu open button,
    # as it has a dynamic input type.
    if selected_type == "Text":
        layout_type = "Text-to-Image"
    elif selected_type == "Image":
        layout_type = "Text-to-Image"

    if layout_type:
        open_file_dialog(input_type_var, input_text, input_image_label, layout_type)
    else:
        messagebox.showerror("Error", "Unsupported input type.")


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

    if selected_model == "Image-to-Text":
        # Create the new widgets for the "Image-to-Text" layout
        browse_button = ttk.Button(user_input_frame, text="Browse")
        input_image_label = ttk.Label(user_input_frame, background="gray")
        text_output_box = tk.Text(model_output_frame, height=10, width=30)

        # Pack the new widgets and buttons
        browse_button.pack(pady=10)
        input_image_label.pack(fill="both", expand=True)
        text_output_box.pack(fill="both", expand=True)

        bottom_button_frame = ttk.Frame(user_input_frame)
        bottom_button_frame.pack(fill="x", pady=5)
        run_model1_button = ttk.Button(bottom_button_frame, text="Run Model 1")
        run_model1_button.pack(side="left", padx=(0, 5))
        run_model2_button = ttk.Button(bottom_button_frame, text="Run Model 2")
        run_model2_button.pack(side="left", padx=(0, 5))
        clear_button = ttk.Button(bottom_button_frame, text="Clear")
        clear_button.pack(side="right")

        # We need to link the buttons to the new widgets
        browse_button.config(
            command=lambda: open_file_dialog(input_type_var, None, input_image_label, layout_type="Image-to-Text"))
        run_model1_button.config(
            command=lambda: run_model(1, "Image-to-Text", None, input_image_label, None, text_output_box, None,
                                      input_type_var))
        run_model2_button.config(
            command=lambda: run_model(2, "Image-to-Text", None, input_image_label, None, text_output_box, None,
                                      input_type_var))
        clear_button.config(command=lambda: clear_fields(None, input_image_label, None, text_output_box, None))

    elif selected_model == "Text-to-Image":
        # The existing "Text-to-Image" layout logic

        # Force the radio button to "Text" mode
        input_type_var.set("Text")

        # Create the buttons and widgets for this layout
        button_container = ttk.Frame(user_input_frame)
        button_container.pack(fill="x", pady=(0, 5))
        text_radio = ttk.Radiobutton(button_container, text="Text", variable=input_type_var, value="Text")
        image_radio = ttk.Radiobutton(button_container, text="Image", variable=input_type_var, value="Image")
        text_radio.pack(side="left", padx=(0, 5))
        image_radio.pack(side="left")
        browse_button = ttk.Button(button_container, text="Browse")
        browse_button.pack(side="right")

        input_text = tk.Text(user_input_frame, height=10, width=40)
        input_image_label = ttk.Label(user_input_frame, background="gray")
        single_line_textbox = tk.Text(user_input_frame, height=1)
        output_text = tk.Text(model_output_frame, height=10, width=30)
        output_image_label = ttk.Label(model_output_frame, background="gray")

        # Initial layout setup
        input_text.pack(fill="both", expand=True)
        output_text.pack(fill="both", expand=True)

        bottom_button_frame = ttk.Frame(user_input_frame)
        bottom_button_frame.pack(fill="x", pady=5)
        run_model1_button = ttk.Button(bottom_button_frame, text="Run Model 1")
        run_model1_button.pack(side="left", padx=(0, 5))
        run_model2_button = ttk.Button(bottom_button_frame, text="Run Model 2")
        run_model2_button.pack(side="left", padx=(0, 5))
        clear_button = ttk.Button(bottom_button_frame, text="Clear")
        clear_button.pack(side="right")

        # Re-link the buttons and variable trace
        input_type_var.trace_add("write",
                                 lambda *args: handle_input_type_change(input_type_var, input_text, input_image_label,
                                                                        single_line_textbox, output_text,
                                                                        output_image_label))
        browse_button.config(command=lambda: open_file_dialog(input_type_var, input_text, input_image_label,
                                                              layout_type="Text-to-Image"))
        run_model1_button.config(
            command=lambda: run_model(1, "Text-to-Image", input_text, input_image_label, single_line_textbox,
                                      output_text, output_image_label, input_type_var))
        run_model2_button.config(
            command=lambda: run_model(2, "Text-to-Image", input_text, input_image_label, single_line_textbox,
                                      output_text, output_image_label, input_type_var))
        clear_button.config(
            command=lambda: clear_fields(input_text, input_image_label, single_line_textbox, output_text,
                                         output_image_label))


def handle_input_type_change(input_type_var, input_text, input_image_label, single_line_textbox, output_text,
                             output_image_label):
    # This function is now only used for the "Text-to-Image" layout
    selected_type = input_type_var.get()

    if selected_type == "Text":
        if input_image_label.winfo_exists():
            input_image_label.pack_forget()
        if single_line_textbox.winfo_exists():
            single_line_textbox.pack_forget()
        if input_text.winfo_exists():
            input_text.pack(fill="both", expand=True)
        if output_image_label.winfo_exists():
            output_image_label.pack_forget()
        if output_text.winfo_exists():
            output_text.pack(fill="both", expand=True)

    elif selected_type == "Image":
        if input_text.winfo_exists():
            input_text.pack_forget()
        if input_image_label.winfo_exists():
            input_image_label.pack(fill="both", expand=True)
        if single_line_textbox.winfo_exists():
            single_line_textbox.pack(fill="x", pady=(5, 0))
        if output_text.winfo_exists():
            output_text.pack_forget()
        if output_image_label.winfo_exists():
            output_image_label.pack(fill="both", expand=True)



def open_file_dialog(input_type_var, input_text, input_image_label, layout_type, new_width=None):
    # This function is now only used for the "Image-to-Text" and "Text-to-Image" layouts

    if layout_type == "Image-to-Text":
        filetypes = (
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All files", "*.*")
        )
        filepath = filedialog.askopenfilename(
            title="Open an image file",
            initialdir="/",
            filetypes=filetypes
        )
        if filepath:
            original_image = Image.open(filepath)
            container_width = input_image_label.winfo_width()
            container_height = input_image_label.winfo_height()
            aspect_ratio = original_image.width / original_image.height
            if (container_width / aspect_ratio) <= container_height:
                new_width = container_width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = container_height
                new_width = int(new_height * aspect_ratio)
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_image)
            input_image_label.config(image=tk_image)
            input_image_label.image = tk_image

    elif layout_type == "Text-to-Image":
        selected_type = input_type_var.get()
        if selected_type == "Text":
            filetypes = (
                ("Text files", "*.txt"),
                ("All files", "*.*")
            )
            filepath = filedialog.askopenfilename(
                title="Open a text file",
                initialdir="/",
                filetypes=filetypes
            )
            if filepath:
                with open(filepath, 'r') as file:
                    content = file.read()
                    input_text.delete("1.0", tk.END)
                    input_text.insert(tk.END, content)

        elif selected_type == "Image":
            filetypes = (
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("All files", "*.*")
            )
            filepath = filedialog.askopenfilename(
                title="Open an image file",
                initialdir="/",
                filetypes=filetypes
            )
            if filepath:
                original_image = Image.open(filepath)

                # The fix: Get the container dimensions from the parent frame after it's drawn
                container_width = input_image_label.master.winfo_width()
                container_height = input_image_label.master.winfo_height()

                if container_width > 0 and container_height > 0:
                    aspect_ratio = original_image.width / original_image.height
                    if (container_width / aspect_ratio) <= container_height:
                        new_width = container_width
                        new_height = int(new_width / aspect_ratio)
                    else:
                        new_height = container_height
                        new_width = int(new_width * aspect_ratio)
                    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
                    tk_image = ImageTk.PhotoImage(resized_image)
                    input_image_label.config(image=tk_image)
                    input_image_label.image = tk_image
                else:
                    messagebox.showerror("Error", "Could not get a valid size for the image container.")


def clear_fields(input_text, input_image_label, single_line_textbox, output_text, output_image_label):
    if input_text:
        input_text.delete("1.0", tk.END)
    if single_line_textbox:
        single_line_textbox.delete("1.0", tk.END)
    if output_text:
        output_text.delete("1.0", tk.END)

    if input_image_label:
        input_image_label.config(image="")
        input_image_label.image = None
    if output_image_label:
        output_image_label.config(image="")
        output_image_label.image = None


def run_model(model_number, layout_type, input_text, input_image_label, single_line_textbox, output_text,
              output_image_label, input_type_var):
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                                                                                                             #
    #   PLACE MODEL 1 or MODEL 2 CODE HERE                                                                        #
    #                                                                                                             #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    if layout_type == "Text-to-Image":
        selected_type = input_type_var.get()

        if selected_type == "Text":
            # For Text-to-Image model, Text input
            #
            # The Text input is contained in the 'input_text' variable.
            # Example: text_data = input_text.get("1.0", "end-1c")
            #
            # The output textbox is in the 'output_text' variable.
            # Example: output_text.delete("1.0", tk.END)
            #          output_text.insert(tk.END, "Your output text here")
            #
            # The output image box is in the 'output_image_label' variable.
            #
            # Example: output_image_label.config(image=generated_image)
            #          output_image_label.image = generated_image
            #
            # Your model code goes below this line

            text_input = input_text.get("1.0", "end-1c")
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, text_input)

        elif selected_type == "Image":
            # For Text-to-Image model, Image input (with text prompt)
            #
            # The image is in the 'input_image_label.image' variable.
            # The text prompt is in the 'single_line_textbox' variable.
            # Example: image_data = input_image_label.image
            #          text_prompt = single_line_textbox.get("1.0", "end-1c")
            #
            # The output textbox is in the 'output_text' variable.
            # The output image box is in the 'output_image_label' variable.
            #
            # Your model code goes below this line

            image_input = input_image_label.image
            text_input = single_line_textbox.get("1.0", "end-1c")
            output_image_label.config(image=image_input)
            output_image_label.image = image_input
            messagebox.showinfo("Model Run",
                                f"Running image through Model {model_number} with the following text commands: {text_input}")

    elif layout_type == "Image-to-Text":
        # For Image-to-Text model
        #
        # The image is in the 'input_image_label.image' variable.
        # Example: image_data = input_image_label.image
        #
        # The output textbox is in the 'output_text' variable.
        #
        # Your model code goes below this line

        if output_text:
            messagebox.showinfo("Model Run", f"Running Image-to-Text Model {model_number}")
            generated_text = "This is a placeholder for the text generated from the image."
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, generated_text)

        else:  # This is the "Text-to-Image" layout
            image_input = input_image_label.image
            text_input = single_line_textbox.get("1.0", "end-1c")
            output_image_label.config(image=image_input)
            output_image_label.image = image_input
            messagebox.showinfo("Model Run",
                                f"Running image through Model {model_number} with the following text commands: {text_input}")