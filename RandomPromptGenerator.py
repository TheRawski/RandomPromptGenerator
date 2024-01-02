import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
import customtkinter
import random
import pyperclip
from random_word import RandomWords
from PIL import Image
import sys, os


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generate_random_output(prefix_inputs, used_inputs):
    output = []
    random.shuffle(prefix_inputs)  # Shuffle the order of prefix inputs
    random.shuffle(used_inputs)  # Shuffle the order of used inputs
    choice_var_int = int(option_menu.get())

    for input in prefix_inputs + used_inputs:
        num_parentheses = random.randint(0, choice_var_int)  # Randomly choose the number of parentheses to add
        parentheses = "(" * num_parentheses + input + ")" * num_parentheses
        output.append(parentheses)

    result = ", ".join(output)
    return result


def generate_output():
    output = generate_random_output(prefix_inputs, used_inputs)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)

def add_input():
    user_input = input_text.get(1.0, tk.END).strip()
    if user_input != "":
        input_without_parentheses = user_input.replace("(", "").replace(")", "")
        inputs = input_without_parentheses.split(", ")
        for input in inputs:
            if input.strip() != "":
                used_inputs.append(input.strip())
        update_input_list()
        input_text.delete(1.0, tk.END)

def paste_input():
    input_text.insert(tk.END, pyperclip.paste())

def copy_to_clipboard():
    result = output_text.get(1.0, tk.END).strip()
    pyperclip.copy(result)

def generate_random_input():
    r = RandomWords()
    random_generated_word = (r.get_random_word())
    used_inputs.append(random_generated_word.strip())
    update_input_list()

def select_all_inputs():
    input_listbox.selection_set(0, tk.END)

def select_all_prefix():
    prefix_listbox.selection_set(0, tk.END)

def select_all_unused():
    unused_listbox.selection_set(0, tk.END)

def remove_input():
    selected_indices = input_listbox.curselection()
    if selected_indices:
        selected_indices = list(selected_indices)
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            used_inputs.pop(index)
        update_input_list()

def remove_prefix():
    selected_indices = prefix_listbox.curselection()
    if selected_indices:
        selected_indices = list(selected_indices)
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            prefix_inputs.pop(index)
        update_prefix_list()

def remove_unused():
    selected_indices = unused_listbox.curselection()
    if selected_indices:
        selected_indices = list(selected_indices)
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            unused_inputs.pop(index)
        update_unused_list()

def remove_duplicates():
    used_inputs[:] = list(set(used_inputs))
    update_input_list()
    prefix_inputs[:] = list(set(prefix_inputs))
    update_prefix_list()
    unused_inputs[:] = list(set(unused_inputs))
    update_unused_list()

def update_input_list():
    input_listbox.delete(0, tk.END)
    for input in used_inputs:
        input_listbox.insert(tk.END, input)

def update_prefix_list():
    prefix_listbox.delete(0, tk.END)
    for input in prefix_inputs:
        prefix_listbox.insert(tk.END, input)

def update_unused_list():
    unused_listbox.delete(0, tk.END)
    for input in unused_inputs:
        unused_listbox.insert(tk.END, input)


def move_input_to_prefix():
    selected_indices = input_listbox.curselection()
    if selected_indices:
        selected_indices = list(selected_indices)
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            input_text = input_listbox.get(index)
            prefix_listbox.insert(tk.END, input_text)
            input_listbox.delete(index)
            if input_text in used_inputs:
                used_inputs.remove(input_text)
            elif input_text in unused_inputs:
                unused_inputs.remove(input_text)
            prefix_inputs.append(input_text)

def move_input_to_unused():
    selected_indices = input_listbox.curselection()
    if selected_indices:
        selected_indices = list(selected_indices)
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            input_text = input_listbox.get(index)
            unused_listbox.insert(tk.END, input_text)
            input_listbox.delete(index)
            if input_text in used_inputs:
                used_inputs.remove(input_text)
            elif input_text in prefix_inputs:
                prefix_inputs.remove(input_text)
            unused_inputs.append(input_text)


def move_prefix_to_used():
    selected_indices = prefix_listbox.curselection()
    if selected_indices:
        selected_indices = list(selected_indices)
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            input_text = prefix_listbox.get(index)
            input_listbox.insert(tk.END, input_text)
            prefix_listbox.delete(index)
            prefix_inputs.remove(input_text)
            used_inputs.append(input_text)

def move_unused_to_used():
    selected_indices = unused_listbox.curselection()
    if selected_indices:
        selected_indices = list(selected_indices)
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            input_text = unused_listbox.get(index)
            input_listbox.insert(tk.END, input_text)
            unused_listbox.delete(index)
            unused_inputs.remove(input_text)
            used_inputs.append(input_text)

def make_scrollbar_styles(
        troughcolor='gray',
        background='gray',
        arrowcolor='white',
        disabledcolor='gray'
) -> tuple[str, str]:
    """
    Style the scrollbars.  Usage:
        parent_frame = ... # tk.Frame(...) or tk.Tk() or whatever you're using for the parent
        hstyle, vstyle = make_scrollbar_styles()
        vbar = ttk.Scrollbar(parent_frame, orient='vertical', style=vstyle)
        hbar = ttk.Scrollbar(parent_frame, orient='horizontal', style=hstyle)
    """
    style = Style()

    for is_hori in (True, False):
        v = "Horizontal" if is_hori else "Vertical"
        style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.trough', 'from', 'default')
        style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.thumb', 'from', 'default')
        # style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.leftarrow', 'from', 'default')
        # style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.rightarrow', 'from', 'default')
        style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.uparrow', 'from', 'default')
        style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.downarrow', 'from', 'default')
        style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.grip', 'from', 'default')
        style.layout(
            f'CustomScrollbarStyle.{v}.TScrollbar',
            [(f'CustomScrollbarStyle.{v}.Scrollbar.trough', {
                'children': [
                    # Commenting in these 2 lines adds arrows (at least horizontally)
                    (f'CustomScrollbarStyle.{v}.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}) if is_hori else (f'CustomScrollbarStyle.{v}.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}),
                    (f'CustomScrollbarStyle.{v}.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''})  if is_hori else (f'CustomScrollbarStyle.{v}.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}),
                    (f'CustomScrollbarStyle.{v}.Scrollbar.thumb', {
                        'unit': '1',
                        'children': [(f'CustomScrollbarStyle.{v}.Scrollbar.grip', {'sticky': ''})],
                        'sticky': 'nswe'}
                     )
                ],
                'sticky': 'we' if is_hori else 'ns'}),
             ])
        style.configure(f'CustomScrollbarStyle.{v}.TScrollbar', troughcolor=troughcolor, background=background, arrowcolor=arrowcolor)
        # Comment in the following to customize disable/active colors, whatever that means
        style.map(f'CustomScrollbarStyle.{v}.TScrollbar', background=[('pressed', '!disabled', disabledcolor), ('active', 'gray')])
    return "CustomScrollbarStyle.Horizontal.TScrollbar", "CustomScrollbarStyle.Vertical.TScrollbar"


# def option_menu_callback(choice):
#     print("clicked", choice)
#     choice_var_int = int(option_menu.get())
#     print(choice_var_int)



def open_about_window():
    width = 940
    height = 590
    about_window = customtkinter.CTkToplevel()
    about_window.overrideredirect(True)
    about_window.geometry("%dx%d+%d+%d" % (200, 300, root.winfo_x() + width/2.5, root.winfo_y() + height/4))
    about_image_label = customtkinter.CTkLabel(about_window, image=about_image, text="")
    about_image_label.grid(row=0, column=0, columnspan=2, sticky="ns")
    about_textbox = customtkinter.CTkTextbox(about_window)
    about_textbox.grid(row=1, column=0, columnspan=2, sticky="nsew")
    about_textbox.insert("0.0", "Random Prompt Generator was made by TheRawski with some help from ChatGPT, https://github.com/TheRawski/RandomPromptGenerator")
    about_textbox.configure(state="disabled", wrap="word")
    about_window.grab_set()
    close_button = customtkinter.CTkButton(about_window, text="Close", command=about_window.destroy)
    close_button.grid(row=2, column=0, columnspan=2, pady=10)




used_inputs = []
prefix_inputs = []
unused_inputs = []
choice_var_int = 0
about_image = customtkinter.CTkImage(dark_image=Image.open(resource_path('app.ico')), size=(48,48))

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title("Random Prompt Generator")
root.resizable(False, False)
root.iconbitmap(resource_path('app.ico'))

choice_var = customtkinter.StringVar(value="0")



title_frame = customtkinter.CTkFrame(root)
title_frame.grid(row=0, column=0, sticky="n")
title_text = customtkinter.CTkLabel(title_frame, text="(((Random Prompt Generator)))", font=customtkinter.CTkFont(family="Courier", size=20, weight="bold"))
title_text.grid(row=0, column=0, pady=(10), sticky="we")



input_frame = customtkinter.CTkFrame(root)
input_frame.grid_columnconfigure(1, weight=1)

input_frame.grid(row=1, column=0, sticky='nsew')
input_label = customtkinter.CTkLabel(input_frame, text="Enter inputs (separated by comma, space)")
input_label.grid(row=0, column=0, columnspan=6, padx=10, sticky="w")

input_text = customtkinter.CTkTextbox(input_frame, height=1)
input_text.grid(row=1, column=0, columnspan=6, pady=(0, 5), padx=10, sticky="ew")

about_button = customtkinter.CTkButton(input_frame, width= 70, height=20, fg_color="#8d591f", hover_color="#553513", text="About", command=open_about_window)
about_button.grid(row=0, column=1, padx=10, sticky='e')

input_button_frame = customtkinter.CTkFrame(input_frame)
input_button_frame.grid_columnconfigure(0, weight=1)
input_button_frame.grid_columnconfigure(1, weight=1)
input_button_frame.grid_columnconfigure(2, weight=1)
input_button_frame.grid_columnconfigure(3, weight=1)
input_button_frame.grid_columnconfigure(4, weight=1)
input_button_frame.grid_columnconfigure(5, weight=1)


input_button_frame.grid(row=2, column=0, columnspan=6, sticky="ew")

random_word_button = customtkinter.CTkButton(input_button_frame, text="Add Random Word", command=generate_random_input)
random_word_button.grid(row=0, column=0, columnspan=2, padx=(10, 5), pady=5, sticky='ew')

paste_button = customtkinter.CTkButton(input_button_frame, text="Paste from Clipboard", command=paste_input, font=customtkinter.CTkFont(weight="bold"))
paste_button.grid(row=0, column=5, columnspan=1, padx=5, pady=5, sticky='e')

add_button = customtkinter.CTkButton(input_button_frame, text="Add", command=add_input, font=customtkinter.CTkFont(weight="bold"))
add_button.grid(row=0, column=6, columnspan=1, padx=(5, 10), pady=5, sticky='e')


all_listbox_frame = customtkinter.CTkFrame(root)
all_listbox_frame.grid(row=4, column=0, padx=(10))
hstyle, vstyle = make_scrollbar_styles()
# style = ttk.Style()
# style.map("Vertical.TScrollbar", background=[('pressed', '!disabled', 'pink'), ('active', 'orange')])
# style.theme_use('classic')
# style.configure("Vertical.TScrollbar", arrowcolor="white", background="black", bordercolor="black", darkcolor="white", foreground="black", lightcolor="black", troughcolor="black")
# , background="black", bordercolor="black", arrowcolor="black"

prefix_listbox_frame = customtkinter.CTkFrame(all_listbox_frame)
prefix_listbox_frame.grid(row=0, column=0, columnspan=2, sticky="ns")
prefix_listbox_label = customtkinter.CTkLabel(prefix_listbox_frame, text="Prefix Inputs")
prefix_listbox_label.grid(row=0, column=0, columnspan=2, sticky="ew")
prefix_listbox = tk.Listbox(prefix_listbox_frame, width=50, height=10, selectmode=tk.MULTIPLE, selectbackground="#1f538d", selectforeground="white", bg="#181c1e", foreground="white")
prefix_listbox.grid(row=1, column=0)
prefix_scrollbar = ttk.Scrollbar(prefix_listbox_frame, orient='vertical', style=vstyle)
prefix_scrollbar.grid(row=1, column=0, sticky="nse")
prefix_listbox.config(yscrollcommand=prefix_scrollbar.set)
prefix_scrollbar.config(command=prefix_listbox.yview)

move_prefix_to_used_button = customtkinter.CTkButton(prefix_listbox_frame, text="Move to Used >>", command=move_prefix_to_used)
move_prefix_to_used_button.grid(row=2, column=0, pady=(5))

remove_prefix_button = customtkinter.CTkButton(prefix_listbox_frame, text="Remove", command=remove_prefix)
remove_prefix_button.grid(row=3, column=0, pady=(5), padx=(10), sticky='w')

select_all_prefix_button = customtkinter.CTkButton(prefix_listbox_frame, text="Select All", command=select_all_prefix)
select_all_prefix_button.grid(row=3, column=0, pady=(5), padx=(10), sticky='e')


input_listbox_frame = customtkinter.CTkFrame(all_listbox_frame)
input_listbox_frame.grid(row=0, column=2, columnspan=2, sticky="ns")
input_listbox_label = customtkinter.CTkLabel(input_listbox_frame, text="Used Inputs")
input_listbox_label.grid(row=0, column=2, columnspan=2, sticky="ew")
input_listbox = tk.Listbox(input_listbox_frame, width=50, height=10, selectmode=tk.MULTIPLE, selectbackground="#1f538d", selectforeground="white", bg="#181c1e", foreground="white")
input_listbox.grid(row=1, column=2)
input_scrollbar = ttk.Scrollbar(input_listbox_frame, orient='vertical', style=vstyle)
input_scrollbar.grid(row=1, column=2, sticky="nse")
input_listbox.config(yscrollcommand=input_scrollbar.set)
input_scrollbar.config(command=input_listbox.yview)

move_to_prefix_button = customtkinter.CTkButton(input_listbox_frame, text="<< Move to Prefix", command=move_input_to_prefix)
move_to_prefix_button.grid(row=2, column=2, pady=(5), sticky='w')

move_to_unused_button = customtkinter.CTkButton(input_listbox_frame, text="Move to Unused >>", command=move_input_to_unused)
move_to_unused_button.grid(row=2, column=2, pady=(5), sticky='e')

remove_button = customtkinter.CTkButton(input_listbox_frame, text="Remove", command=remove_input)
remove_button.grid(row=3, column=2, pady=5, padx=(10), sticky='w')

select_all_button = customtkinter.CTkButton(input_listbox_frame, text="Select All", command=select_all_inputs)
select_all_button.grid(row=3, column=2, pady=(5), padx=(10), sticky='e')


remove_duplicates_button = customtkinter.CTkButton(input_listbox_frame, text="Remove Duplicates", command=remove_duplicates)
remove_duplicates_button.grid(row=4, column=0, columnspan=7, padx=10, pady=5, sticky='ns')




unused_listbox_frame = customtkinter.CTkFrame(all_listbox_frame)
unused_listbox_frame.grid(row=0, column=4, columnspan=2, sticky="ns")
unused_listbox_label = customtkinter.CTkLabel(unused_listbox_frame, text="Unused Inputs")
unused_listbox_label.grid(row=0, column=4, columnspan=2, sticky="ew")
unused_listbox = tk.Listbox(unused_listbox_frame, width=50, height=10, selectmode=tk.MULTIPLE, selectbackground="#1f538d", selectforeground="white", bg="#181c1e", foreground="white")
unused_listbox.grid(row=1, column=4)
unused_scrollbar = ttk.Scrollbar(unused_listbox_frame, orient='vertical', style=vstyle)
unused_scrollbar.grid(row=1, column=4, sticky="nse")
unused_listbox.config(yscrollcommand=unused_scrollbar.set)
unused_scrollbar.config(command=unused_listbox.yview)

move_unused_to_used_button = customtkinter.CTkButton(unused_listbox_frame, text="<< Move to Used", command=move_unused_to_used)
move_unused_to_used_button.grid(row=2, column=4, pady=(5))

remove_unused_button = customtkinter.CTkButton(unused_listbox_frame, text="Remove", command=remove_unused)
remove_unused_button.grid(row=3, column=4, pady=(5), padx=(10), sticky='w')

select_all_unused_button = customtkinter.CTkButton(unused_listbox_frame, text="Select All", command=select_all_unused)
select_all_unused_button.grid(row=3, column=4, pady=(5), padx=(10), sticky='e')

output_frame = customtkinter.CTkFrame(root)
output_frame.grid(row=5, column=0, columnspan=6, sticky='nsew')
output_frame.grid_columnconfigure(4, weight=5)

result_label = customtkinter.CTkLabel(output_frame, text="Generated Output", font=customtkinter.CTkFont(weight="bold"))
result_label.grid(row=0, column=0, padx=(10))

option_menu_label = customtkinter.CTkLabel(output_frame, text="Maximum amount of parentheses to use for emphasis:")
option_menu_label.grid(row=0, column=1, padx=(10), sticky='e')

option_menu = customtkinter.CTkOptionMenu(output_frame, width=50, values=["0", "1", "2", "3", "4"], variable=choice_var)
option_menu.grid(row=0, column=2, pady=5, sticky='w')



output_text = customtkinter.CTkTextbox(output_frame, height=5)
output_text.grid(row=1, column=0, columnspan=5, rowspan=5, padx=(10), pady=(0, 10), sticky="nsew")
output_text.configure(wrap="word")


generate_button = customtkinter.CTkButton(output_frame, fg_color="#8d591f", hover_color="#553513", text="Generate Output", command=generate_output, font=customtkinter.CTkFont(weight="bold"))
generate_button.grid(row=1, column=5, padx=(10), pady=(0, 5))

copy_button = customtkinter.CTkButton(output_frame, text="Copy to Clipboard", command=copy_to_clipboard, font=customtkinter.CTkFont(weight="bold"))
copy_button.grid(row=2, column=5, padx=(10), pady=(0, 10))


root.mainloop()