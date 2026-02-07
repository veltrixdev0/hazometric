'''

BUILD:
python -m PyInstaller main.py --onefile --add-data "utils;utils" --add-data "save;save" --noconsole

LOAD JSON:
data = readJSON(os.path.join(SAVE_PATH, "userData.json"))

'''
from customtkinter import *
from utils.readJSON import *
from utils.addJSON import *

from PIL import Image

## // CONFIGS // ##
ABS_PATH = os.path.dirname(os.path.abspath(__file__)) # Get absolute path
SAVE_PATH = os.path.join(ABS_PATH, "save")
theme_initialized = False

# Store references to game buttons for fast access
game_buttons = {}

# Load save data from startup
saveLatest = readJSON(os.path.join(SAVE_PATH, "userData.json"))

# Reload JSON after changes
def reloadJSON():
    global saveLatest
    saveLatest = readJSON(os.path.join(SAVE_PATH, "userData.json")) 

def runPath(application): # Run Path to .exe or other application
    print(f"Running {application}") # Debug
    os.startfile(application) # Starts the file

def welcomeFrame():
    # Welcome Frame
    welcome_frame = CTkFrame(master=tab_view_frame.tab("Welcome"))
    welcome_frame.grid(sticky="nsew", padx=20, pady=20)

    welcome_frame.grid_columnconfigure(0, weight=1)  # Center Horizontallz
    welcome_frame.grid_rowconfigure((0,1,2), weight=1)  # Distribute vertical space

    # Welcome Text Label
    welcome_label = CTkLabel(master=welcome_frame, text="Welcome!", font=CTkFont(size=28, weight="bold"))
    welcome_label.grid(row=0, column=0, pady=(40,10))

    # Welcome Desc Text Label
    welcome_desc_label = CTkLabel(master=welcome_frame, text="Start by adding games or accessing them.", font=CTkFont(size=16), wraplength=400)
    welcome_desc_label.grid(row=1, column=0, pady=(0,40))

def addAndSet(title, desc): # Adds the tab for the game card
    if title not in tab_view_frame._tab_dict: # Prevents duplicate tabs   
        tab_view_frame.add(title) # Adds the tab
        gameViewFrame(title, desc) # Adds the game stuff

    tab_view_frame.set(title) # Sets it to the tab automatically

def removeAndSetBackToHome(title): # Sets back at home
    if title in tab_view_frame._tab_dict: # Checks if title is in tab view frame
        tab_view_frame.delete(title)
        tab_view_frame.set("Welcome")
    else:
        print(f"{title} not found in tab_view_frame") # Error

def find_widgets_by_text(parent, text): # Finds all widgets by text
    matches = []
    for w in parent.winfo_children(): # Gets all widgets
        try:
            if w.cget("text") == text: # Checks the text
                matches.append(w)
        except ctk_tk.tkinter.TclError: # Checks if error
            # widget does not support "text"
            print("Error in CTk.")
            
        # Recursively search children
        matches.extend(find_widgets_by_text(w, text))
    return matches


def removeFromLibrary(title): # Removes from library
    removeJSON(os.path.join(SAVE_PATH, "userData.json"), title) # The Function from another file
    reloadJSON() # Refresh after removval

    # Destroy the buttons after stored reference instead of searching tree
    if title in game_buttons:
        game_buttons[title].destroy()
        del game_buttons[title]

    removeAndSetBackToHome(title) # Sets back at home

def gameViewFrame(title, description):
    # Game View Frame
    game_view_frame = CTkFrame(master=tab_view_frame.tab(title))
    game_view_frame.grid(sticky="nsew", padx=10, pady=10)

    game_view_frame.grid_columnconfigure(0, weight=1)
    game_view_frame.grid_rowconfigure(0, weight=0)
    game_view_frame.grid_rowconfigure(1, weight=0)
    game_view_frame.grid_rowconfigure(2, weight=0)
    game_view_frame.grid_rowconfigure(3, weight=0)
    game_view_frame.grid_rowconfigure(4, weight=1)

    # Game View Title
    game_view_title = CTkLabel(master=game_view_frame, text=title, font=CTkFont(size=22, weight="bold"), anchor="w")
    game_view_title.grid(row=0, column=0, sticky="w", padx=15, pady=(10,5))

    # Game View Description
    game_view_description = CTkLabel(master=game_view_frame, text=description, font=CTkFont(size=14), anchor="w", wraplength=300)
    game_view_description.grid(row=1, column=0, sticky="w", padx=15, pady=(0,15))

    # Get the latest save
    saveLatestJSON = readJSON(os.path.join(SAVE_PATH, "userData.json"))

    # Fetch the game info from JSON
    game = saveLatest.get("games", {}).get(title) # Cache JSON
    if not game:
        print(f"Game '{title}' not found in JSON.")
        return  # Exit early if game not found

    # Frame Button Game View
    game_view_frame_button = CTkFrame(master=game_view_frame, fg_color="transparent")
    game_view_frame_button.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
    game_view_frame_button.grid_rowconfigure((0,1,2), weight=1)

    # Game View Play Button
    game_view_play_button = CTkButton(
        master=game_view_frame_button,
        text="Play",
        command=lambda: runPath(game["path"]), # Run path
        fg_color="#4CAF50",  # Play color
        hover_color="#45A049" # Play hover color
    )
    game_view_play_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    # Close tab button
    game_view_close_tab_button = CTkButton(
        master=game_view_frame_button,
        text="Close this tab",
        command=lambda: removeAndSetBackToHome(title),
        fg_color="#FF9800",  # Orange color
        hover_color="#e68a00" # Orange hover color
    )
    game_view_close_tab_button.grid(row=1, column=0, sticky="ew", padx=5,pady=5)

    # Remove from Library button
    game_view_remove_from_library_button = CTkButton(
        master=game_view_frame_button,
        text="Remove from library",
        width=50,
        command=lambda: removeFromLibrary(title),
        fg_color="#f44336", # Warning color
        hover_color="#da190b" # Warning hover color
    )
    game_view_remove_from_library_button.grid(row=2, column=0, sticky="ew", padx=5,pady=5)


def addGameFrame(parent, title, description, logo, row): # Game Card
    # Game Card Button
    btn = CTkButton(master=parent, text=f"▶ {title}", command=lambda: addAndSet(title=title, desc=description))
    btn.grid(sticky="ew", pady=6, padx=5, row=row, column=0)
    # Store reference for fast removal
    game_buttons[title] = btn

def addLibraryWindow():
    # Variables Configuration
    path = ""
    title = ""
    description = ""

    # Create a new top-level window
    library_window = CTkToplevel()
    library_window.title("Add to Library")

    library_window.geometry("290x250")
    library_window.minsize(290, 250)
    library_window.maxsize(290, 250)

    library_window.focus_force()
    library_window.transient(app)

    # Frame inside top-level
    main_add_library_frame = CTkFrame(master=library_window)
    main_add_library_frame.grid(sticky="nsew",padx=15, pady=15)
    main_add_library_frame.grid_columnconfigure(0, weight=1)

    # Helper function to create label + button in a horizontal layout
    def createLabeledButton(row, label_text, btn_text, command):
        # Container frame for label + button
        container = CTkFrame(master=main_add_library_frame, fg_color="#3c3c3c", corner_radius=6)
        container.grid(sticky="ew", pady=5, padx=5)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)

        # Label (left side)
        label = CTkLabel(master=container, text=label_text, anchor="w", wraplength=100)
        label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Button (right side)
        btn = CTkButton(master=container, text=btn_text, width=100, command=command)
        btn.grid(row=0, column=1, padx=10, pady=5)
        return label

    # Path
    add_library_path_label = createLabeledButton(
        0,
        f"Path: {path}",
        "Choose exe",
        lambda: choosePath(add_library_path_label)
    )

    def choosePath(label): # Dialog for the path
        dialog = CTkInputDialog(text="Type in the path of the exe:", title="Path to exe")
        pathVar = dialog.get_input()
        if pathVar:
            label.configure(text=f"Path: {pathVar}")

    # Title
    add_library_title_label = createLabeledButton(
        1,
        f"Title: {title}",
        "Choose title",
        lambda: chooseTitle(add_library_title_label)
    )

    def chooseTitle(label): # Dialog for the title
        dialog = CTkInputDialog(text="Type in the title of the application:", title="Title of the application")
        titleVar = dialog.get_input()
        if titleVar:
            label.configure(text=f"Title: {titleVar}")

    # Description
    add_library_description_label = createLabeledButton(
        2,
        f"Description: {description}",
        "Choose description",
        lambda: chooseDescription(add_library_description_label)
    )

    def chooseDescription(label): # Dialog for the description
        dialog = CTkInputDialog(text="Type in the description of the application:", title="Description of the application")
        descriptionVar = dialog.get_input()
        if descriptionVar:
            label.configure(text=f"Description: {descriptionVar}")

    # Confirm Button
    confirm_button = CTkButton(
        master=library_window,
        text="Add to library",
        command=lambda: addGameToJSON()
    )
    confirm_button.grid(row=1, column=0, pady=15)

    def addGameToJSON():
        # Get values from labels
        path_text = add_library_path_label.cget("text").replace("Path: ", "")
        title_text = add_library_title_label.cget("text").replace("Title: ", "")
        description_text = add_library_description_label.cget("text").replace("Description: ", "")

        if title_text and path_text:  # simple check
            writeJSON(
                os.path.join(SAVE_PATH, "userData.json"),
                {"title": title_text, "description": description_text, "path": path_text},
                title_text
            )
            reloadJSON()  # Reload after adding

            # Gets the exact number of game frames
            row_index = len(games_scroll_frame.winfo_children()) 

            # Add Game Frame
            addGameFrame(games_scroll_frame, title_text, description_text, False, row_index)

def changeTheme(theme_or_var, update=False):
    # Determine theme string
    theme = theme_or_var.get() if isinstance(theme_or_var, StringVar) else theme_or_var
    set_appearance_mode(theme)

    # Save to JSON if requested
    if update:
        addSetting(os.path.join(SAVE_PATH, "userData.json"), "theme", theme)
        app.update_idletasks()

def addSettingsWindow():
    # Load the latest theme directly from JSON
    currentTheme = saveLatest.get("settings", {}).get("theme", "dark")  # default to dark

    # Settings Window Configuration
    settings_window = CTkToplevel()
    settings_window.title("Settings")
    settings_window.geometry("400x200")
    settings_window.transient(app)
    settings_window.focus_force()

    # Main Frame For Settings
    main_frame = CTkFrame(settings_window)
    main_frame.grid(sticky="nsew", padx=10, pady=10)
    main_frame.grid_columnconfigure(0, weight=1)

    # String Variable for theme
    theme_var = StringVar(value=currentTheme)

    # Checkbox for dark mode
    dark_checkbox = CTkCheckBox(
        master=main_frame,
        text="Dark Mode",
        variable=theme_var,
        onvalue="dark",
        offvalue="light",
        command=lambda: changeTheme(theme_var, update=True) 
    )
    dark_checkbox.grid(row=0, column=0, pady=10)

# App Configuration
app = CTk()
app.title("hazometric")

app.geometry("700x550")
app.maxsize(700,550)
app.minsize(700,550)

app.grid_columnconfigure(0, weight=0) # Configures the grid columns
app.grid_columnconfigure(1, weight=1) # Configures the grid columns
app.grid_rowconfigure(0, weight=1) # Configures the grid rows
app.grid_rowconfigure(1, weight=0) # Configures the grid rows

changeTheme(saveLatest["settings"]["theme"], update=False)

# Games Scroll Frame
games_scroll_frame = CTkScrollableFrame(master=app, width=200, height=400)
games_scroll_frame.grid(row=0, column=0, padx=30)
games_scroll_frame.grid_columnconfigure(0, weight=1)

# Utils Frame
utils_frame = CTkFrame(master=app, width=100, height=100)
utils_frame.grid(row=1,column=0, sticky="ew", padx=5, pady=5)
utils_frame.grid_columnconfigure(0, weight=1)

# Add to library button
games_add_button = CTkButton(master=utils_frame, text="Add to library", command=lambda: addLibraryWindow())
games_add_button.grid(row=0, column=0, pady=5)

# Settings button
games_settings_button = CTkButton(master=utils_frame, text="Settings", command=lambda: addSettingsWindow())
games_settings_button.grid(row=1, column=0, pady=5)

# Tab View Frame
tab_view_frame = CTkTabview(master=app, width=350, height=400)
tab_view_frame.grid(row=0, column=1)

tab_view_frame.add("Welcome")
tab_view_frame.set("Welcome")

welcomeFrame() # Adds welcome

# Add game cards
for i, (game_id, game) in enumerate(saveLatest["games"].items()):
    addGameFrame(games_scroll_frame, game["title"], game["description"], False, i)
    print(type(game), game)



app.mainloop() # Keeps the app running