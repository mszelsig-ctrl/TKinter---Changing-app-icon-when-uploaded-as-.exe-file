import tkinter as tk
import winsound
from tkinter import WORD
from PIL import Image, ImageTk
import webbrowser
import tempfile
import shutil
import sys, os

import sys, os, tempfile, shutil

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_icon_for_tk(icon_name):
    """Extract icon to a real temp file so Tkinter can load it."""
    src = resource_path(icon_name)
    tmp_icon = os.path.join(tempfile.gettempdir(), icon_name)
    shutil.copyfile(src, tmp_icon)
    return tmp_icon



def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.attributes("-alpha", 0.0)
    splash.configure(bg=BG_COLOR)

    w, h = 420, 260
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")

    canvas = tk.Canvas(splash, width=w, height=h, highlightthickness=0, bg=BG_COLOR)
    canvas.pack()

    try:
        emblem = Image.open(resource_path("RMPLOGO1.png"))
        scale_factor = 150 / emblem.height
        new_w = int(emblem.width * scale_factor)
        new_h = int(emblem.height * scale_factor)
        emblem = emblem.resize((new_w, new_h), Image.LANCZOS)
        emblem_img = ImageTk.PhotoImage(emblem)
    except Exception as e:
        print("Error loading emblem:", e)
        emblem_img = None
        new_w = 150
        new_h = 150

    emblem_x = w // 2
    emblem_y = h // 2 - 40


    neon_radius = new_h // 2 + 8
    canvas.create_oval(
        emblem_x - neon_radius, emblem_y - neon_radius,
        emblem_x + neon_radius, emblem_y + neon_radius,
        outline="#8A0018", 
        width=4,
        tags="neon"
    )



    halo_colors = [
        "#3A0008", "#4A000A", "#5A000C", "#6A000E",
        "#7A0010", "#8A0012", "#9A0014", "#AA0016"
    ]

    for i, color in enumerate(halo_colors):
        radius = neon_radius + 10 + i * 6
        canvas.create_oval(
            emblem_x - radius, emblem_y - radius,
            emblem_x + radius, emblem_y + radius,
            fill=color, outline="", tags="halo"
        )


    if emblem_img:
        splash.emblem_img = emblem_img 
        canvas.create_image(emblem_x, emblem_y, image=splash.emblem_img, tags="emblem")
    else:
        canvas.create_text(
            emblem_x, emblem_y,
            text="RMP",
            fill=FG_COLOR,
            font=("Times", 48, "bold"),
            tags="emblem"
        )

    pulse_colors = ["#4A000A", "#5A000C", "#6A000E", "#5A000C", "#4A000A"]
    pulse_index = 0

    def pulse():
        nonlocal pulse_index

        canvas.delete("pulse")

        radius = neon_radius + 60
        canvas.create_oval(
            emblem_x - radius, emblem_y - radius,
            emblem_x + radius, emblem_y + radius,
            fill=pulse_colors[pulse_index],
            outline="",
            tags="pulse"
        )

        canvas.tag_lower("pulse", "halo")
        canvas.tag_lower("pulse", "neon")
        canvas.tag_lower("pulse", "emblem")

        pulse_index = (pulse_index + 1) % len(pulse_colors)
        splash.after(120, pulse)

    pulse()

    canvas.create_text(
        w/2, h/2 + 60,
        text="[___]\nVirtual Tryout Guide",
        fill=FG_COLOR,
        font=("Times", 22, "bold"),
        justify="center",
        tags="title"
    )

    play_splash_sound(resource_path("splash_sound.wav"))

    for i in range(0, 11):
        splash.attributes("-alpha", i / 10)
        splash.update()
        splash.after(40)

    splash.after(1500)

    for i in range(10, -1, -1):
        splash.attributes("-alpha", i / 10)
        splash.update()
        splash.after(40)

    splash.destroy()

def play_splash_sound(path):
    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)


def open_google_doc():
    import webbrowser
    webbrowser.open("https://docs.google.com/document/d/1-M482TIJ4udg3N6T_Eds-lFKcf_37nx1OV9yvQB72UM/edit?tab=t.0")


BG_COLOR = "#9B1C31"
FG_COLOR = "white"
FONT_MAIN = ("Times", 20, "bold")
FONT_LABEL = ("Times", 16, "bold")


PAGES = [
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".?",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    ".",
    "."
]

NUM_PAGES = len(PAGES)

# ---------- APP SETUP ----------

root = tk.Tk()
root.withdraw()
show_splash()
root.destroy()



window1 = tk.Tk()
window1.title("Tryout Notebook")
window1.iconbitmap(load_icon_for_tk("RMPLOGO1.ico"))
window1.minsize(700, 600)
window1.configure(bg=BG_COLOR)

# GRID WEIGHTS
window1.grid_rowconfigure(0, weight=0)
window1.grid_rowconfigure(1, weight=0)
window1.grid_rowconfigure(2, weight=1)   # text + sidebar
window1.grid_rowconfigure(3, weight=0)   # nav bar
window1.grid_rowconfigure(4, weight=0)   # bottom bar
window1.grid_rowconfigure(5, weight=0)   # theme button

window1.grid_columnconfigure(0, weight=0)
window1.grid_columnconfigure(1, weight=1)

current_page = 1


# ---------- AUTOCOMPLETE ----------

def clear_autocomplete():
    """Hide autocomplete and move layout back up."""
    for widget in autocomplete_frame.winfo_children():
        widget.destroy()

    autocomplete_frame.grid_remove()

    # Move text + sidebar back up
    sidebar_container.grid(row=2, column=0, sticky="nsw")
    text_widget.grid(row=2, column=1, sticky="nsew")


def update_autocomplete(event=None):
    query = search_entry.get().lower().strip()

    clear_autocomplete()

    if not query:
        return

    autocomplete_frame.grid(row=1, column=1, sticky="nw")

    matches = []
    for i, text in enumerate(PAGES):
        if query in text.lower():
            matches.append((i + 1, text[:50] + "..."))

    for page_num, preview in matches[:8]:
        btn = tk.Button(
            autocomplete_frame,
            text=f"Page {page_num}: {preview}",
            anchor="w",
            bg="#B22234",
            fg="white",
            relief="flat",
            command=lambda p=page_num: (show_page(p), clear_autocomplete())
        )
        btn.pack(fill="x")


autocomplete_frame = tk.Frame(window1, bg=BG_COLOR)
autocomplete_frame.grid_remove()

# ---------- SEARCH BAR ----------

search_frame = tk.Frame(window1, bg=BG_COLOR)
search_frame.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

search_entry = tk.Entry(search_frame, font=("Times", 16), width=15)
search_entry.pack(side="left", padx=5)
search_entry.bind("<KeyRelease>", update_autocomplete)

def search_pages():
    query = search_entry.get().lower().strip()
    if not query:
        return

    for i, text in enumerate(PAGES):
        if query in text.lower():
            show_page(i + 1)
            clear_autocomplete()
            return

search_button = tk.Button(
    search_frame,
    text="🔍",
    command=search_pages,
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Times", 16, "bold"),
    relief="flat"
)
search_button.pack(side="left", padx=5)
# ---------- PAGE LABEL ----------

page_label = tk.Label(
    window1,
    text="Page 1",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_LABEL,
)
page_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

# ---------- TEXT WIDGET ----------

text_widget = tk.Text(
    window1,
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_MAIN,
    wrap=WORD
)
text_widget.grid(row=2, column=1, sticky="nsew")

# ---------- SIDEBAR ----------
SIDEBAR_WIDTH = 160

sidebar_container = tk.Frame(window1, bg=BG_COLOR, width=SIDEBAR_WIDTH)
sidebar_container.grid(row=2, column=0, sticky="nsw")
sidebar_container.grid_propagate(False)

sidebar_open = True

sidebar_canvas = tk.Canvas(
    sidebar_container,
    bg=BG_COLOR,
    highlightthickness=0,
    borderwidth=0,
    width=SIDEBAR_WIDTH - 15
)
sidebar_canvas.pack(side="left", fill="y")

sidebar_scrollbar = tk.Scrollbar(
    sidebar_container,
    orient="vertical",
    command=sidebar_canvas.yview
)
sidebar_scrollbar.pack(side="right", fill="y")

sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)

sidebar_frame = tk.Frame(sidebar_canvas, bg=BG_COLOR)
sidebar_canvas.create_window((0, 0), window=sidebar_frame, anchor="nw")

def update_scroll_region(event):
    sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))

sidebar_frame.bind("<Configure>", update_scroll_region)

sidebar_buttons = []

def add_hover_effect(widget):
    def on_enter(e):
        widget['bg'] = "#B22234"
    def on_leave(e):
        idx = sidebar_buttons.index(widget)
        widget['bg'] = "#7A1627" if idx == current_page - 1 else BG_COLOR
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

for i in range(NUM_PAGES):
    btn = tk.Button(
        sidebar_frame,
        text=f"Page {i+1}",
        command=lambda p=i+1: show_page(p),
        bg=BG_COLOR,
        fg=FG_COLOR,
        font=("Times", 14),
        relief="flat"
    )
    btn.pack(fill="x", pady=1)
    sidebar_buttons.append(btn)
    add_hover_effect(btn)

# ---------- NAVIGATION BAR ----------

nav_frame = tk.Frame(window1, bg=BG_COLOR)
nav_frame.grid(row=3, column=1, pady=10, sticky="w")

def go_next():
    show_page(current_page + 1)

def go_prev():
    show_page(current_page - 1)

prev_button = tk.Button(
    nav_frame,
    text="Open previous page",
    command=go_prev,
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_MAIN,
)
prev_button.pack(side="left", padx=5)

next_button = tk.Button(
    nav_frame,
    text="Open next page",
    command=go_next,
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_MAIN,
)
next_button.pack(side="left", padx=5)

def save_page():
    with open(f"page_{current_page}.txt", "w", encoding="utf-8") as f:
        f.write(text_widget.get("1.0", "end-1c"))

save_button = tk.Button(
    nav_frame,
    text="Save Page",
    command=save_page,
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_MAIN
)
save_button.pack(side="left", padx=5)

# ---------- BOTTOM BAR ----------

bottom_frame = tk.Frame(window1, bg=BG_COLOR)
bottom_frame.grid(row=4, column=1, pady=10, sticky="w")

def copy(text_widget):
    window1.clipboard_clear()
    window1.clipboard_append(text_widget.get("1.0", "end-1c"))

def paste(text_widget):
    try:
        text_widget.insert("insert", window1.clipboard_get())
    except:
        pass

copy_button = tk.Button(
    bottom_frame,
    text="Copy",
    command=lambda: copy(text_widget),
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_MAIN,
)
copy_button.pack(side="left", padx=5)

paste_button = tk.Button(
    bottom_frame,
    text="Paste",
    command=lambda: paste(text_widget),
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_MAIN,
)
paste_button.pack(side="left", padx=5)

hyperlink_button = tk.Button(
    bottom_frame,
    text="Open Tryout Doc",
    command=open_google_doc,
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_MAIN,
)
hyperlink_button.pack(side="left", padx=5)

# ---------- THEME BUTTON ----------

def toggle_theme():
    global BG_COLOR, FG_COLOR

    if BG_COLOR == "#9B1C31":
        BG_COLOR = "white"
        FG_COLOR = "black"
    else:
        BG_COLOR = "#9B1C31"
        FG_COLOR = "white"

    window1.configure(bg=BG_COLOR)
    page_label.configure(bg=BG_COLOR, fg=FG_COLOR)
    text_widget.configure(bg=BG_COLOR, fg=FG_COLOR)
    for btn in [prev_button, next_button, save_button, copy_button, paste_button, hyperlink_button]:
        btn.configure(bg=BG_COLOR, fg=FG_COLOR)
    for btn in sidebar_buttons:
        btn.configure(bg=BG_COLOR, fg=FG_COLOR)

theme_button = tk.Button(
    window1,
    text="Toggle Theme",
    command=toggle_theme,
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=FONT_MAIN
)
theme_button.grid(row=5, column=1, sticky="w", padx=5, pady=5)



# ---------- SIDEBAR SCROLLING ----------

scroll_speed = 0

def smooth_scroll():
    global scroll_speed
    if scroll_speed != 0:
        sidebar_canvas.yview_scroll(int(scroll_speed), "units")
        scroll_speed = int(scroll_speed * 0.9)
        window1.after(15, smooth_scroll)

def on_mousewheel(event):
    global scroll_speed
    delta = int(-1 * (event.delta / 120))
    scroll_speed += delta
    smooth_scroll()

sidebar_canvas.bind_all("<MouseWheel>", on_mousewheel)



# ---------- SHOW PAGE ----------

def show_page(page_number: int):
    global current_page
    if page_number < 1 or page_number > NUM_PAGES:
        return

    current_page = page_number
    page_label.config(text=f"Page {current_page}")

    text_widget.delete("1.0", "end")
    text_widget.insert("1.0", PAGES[current_page - 1])

    prev_button.config(state="normal" if current_page > 1 else "disabled")
    next_button.config(state="normal" if current_page < NUM_PAGES else "disabled")

    for idx, btn in enumerate(sidebar_buttons):
        btn.config(bg="#7A1627" if idx == current_page - 1 else BG_COLOR)



def toggle_sidebar():
    global sidebar_open

    if sidebar_open:
        # Collapse sidebar
        sidebar_container.grid_remove()
        sidebar_open = False
    else:
        # Expand sidebar
        sidebar_container.grid(row=2, column=0, sticky="nsw")
        sidebar_open = True


# ---------- SETTINGS MENU ----------
menubar = tk.Menu(window1)

settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Toggle Theme", command=toggle_theme)
settings_menu.add_command(label="Toggle Sidebar", command=toggle_sidebar)
settings_menu.add_separator()
settings_menu.add_command(label="Open Tryout Doc", command=open_google_doc)

menubar.add_cascade(label="Settings", menu=settings_menu)
window1.config(menu=menubar)


show_page(1)

window1.mainloop()
