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

def runPath(application): # Run Path to .exe or other application
    print(f"Running {application}") # Debug
    os.startfile(application) # Starts the file

def welcomeFrame():
    # Welcome Frame
    welcome_frame = CTkFrame(master=tab_view_frame.tab("Welcome"))
    welcome_frame.grid(sticky="nsew")

    # Welcome Text Label
    welcome_label = CTkLabel(master=welcome_frame, text="Welcome!")
    welcome_label.grid()

    # Welcome Desc Text Label
    welcome_desc_label = CTkLabel(master=welcome_frame, text="Start by adding games or accessing them.")
    welcome_desc_label.grid()

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
    
    buttons = find_widgets_by_text(games_scroll_frame, title) # Gets all the buttons
    for button in buttons: # Buttons for loop
        button.destroy() # destroys all buttons

    removeAndSetBackToHome(title) # Sets back at home


def gameViewFrame(title, description):
    # Game View Frame
    game_view_frame = CTkFrame(master=tab_view_frame.tab(title))
    game_view_frame.grid(sticky="nsew")

    game_view_frame.grid_columnconfigure(0, weight=1)
    game_view_frame.grid_rowconfigure(0, weight=1)

    # Game View Title
    game_view_title = CTkLabel(master=game_view_frame, text=title)
    game_view_title.grid(row=0, column=0, sticky="w")

    # Game View Description
    game_view_description = CTkLabel(master=game_view_frame, text=description)
    game_view_description.grid(row=1, column=0, sticky="w")

    # Get the latest save
    saveLatestJSON = readJSON(os.path.join(SAVE_PATH, "userData.json"))

    # Fetch the game info from JSON
    game = saveLatestJSON.get("games", {}).get(title)
    if not game:
        print(f"Game '{title}' not found in JSON.")
        return  # Exit early if game not found

    # Game View Play Button
    game_view_play_button = CTkButton(
        master=game_view_frame,
        text="Play",
        command=lambda: runPath(game["path"])  # Now we have the correct game dictionary
    )
    game_view_play_button.grid(row=2, column=0, sticky="e", pady=5)

    # Close tab button
    game_view_close_tab_button = CTkButton(
        master=game_view_frame,
        text="Close this tab",
        width=50,
        command=lambda: removeAndSetBackToHome(title)
    )
    game_view_close_tab_button.grid(row=3, column=0, pady=3)

    # Remove from Library button
    game_view_remove_from_library_button = CTkButton(
        master=game_view_frame,
        text="Remove from library",
        width=50,
        command=lambda: removeFromLibrary(title)
    )
    game_view_remove_from_library_button.grid(row=4, column=0, pady=3)


def addGameFrame(parent, title, description, logo, row): # Game Card
    # Gets the latest save
    saveLatest = readJSON(os.path.join(SAVE_PATH, "userData.json"))

    # Game Card Button
    game_card_frame = CTkButton(master=parent, text=title, command=lambda: addAndSet(title=title, desc=description))
    game_card_frame.grid(sticky="ew", pady=4, row=row, column=0)

def addLibraryWindow():
    # Variables Configuration
    path = ""
    title = ""
    description = ""

    # Create a new top-level window
    library_window = CTkToplevel()
    library_window.title("Add to Library")
    library_window.geometry("400x300")

    library_window.grid_columnconfigure(0, weight=1)
    library_window.grid_rowconfigure(0, weight=1)

    library_window.focus_force()
    library_window.transient(app)

    # Frame inside top-level
    main_add_library_frame = CTkFrame(master=library_window)
    main_add_library_frame.grid(sticky="ew",padx=10, pady=10, row=0, column=0)
    main_add_library_frame.grid_columnconfigure(0, weight=1)
    main_add_library_frame.grid_rowconfigure(0, weight=1)

    # Path label
    add_library_path_label = CTkLabel(master=main_add_library_frame, text=f"Path: {path}")
    add_library_path_label.grid(row=0, column=0, sticky="w", pady=5)

    # Button to open dialog
    choose_path_button = CTkButton(master=main_add_library_frame, text="Choose exe", command=lambda: choosePath(add_library_path_label))
    choose_path_button.grid(row=1, column=0, pady=5)

    def choosePath(label): # Dialog for the path
        dialog = CTkInputDialog(text="Type in the path of the exe:", title="Path to exe")
        pathVar = dialog.get_input()
        if pathVar:
            label.configure(text=f"Path: {pathVar}")

    # Title label
    add_library_title_label = CTkLabel(master=main_add_library_frame, text=f"Title: {title}")
    add_library_title_label.grid(row=2, column=0, sticky="w", pady=5)

    # Button to open dialog
    choose_title_button = CTkButton(master=main_add_library_frame, text="Choose title", command=lambda: chooseTitle(add_library_title_label))
    choose_title_button.grid(row=3, column=0, pady=5)

    def chooseTitle(label): # Dialog for the path
        dialog = CTkInputDialog(text="Type in the title of the application:", title="Title of the application")
        titleVar = dialog.get_input()
        if titleVar:
            label.configure(text=f"Title: {titleVar}")

    # Description label
    add_library_description_label = CTkLabel(master=main_add_library_frame, text=f"Description: {description}")
    add_library_description_label.grid(row=4, column=0, sticky="w", pady=5)

    # Button to open dialog
    choose_description_button = CTkButton(master=main_add_library_frame, text="Choose description", command=lambda: chooseDescription(add_library_description_label))
    choose_description_button.grid(row=5, column=0, pady=5)

    def chooseDescription(label): # Dialog for the path
        dialog = CTkInputDialog(text="Type in the description of the application:", title="Description of the application")
        descriptionVar = dialog.get_input()
        if descriptionVar:
            label.configure(text=f"Description: {descriptionVar}")

    # Confirm Button
    confirm_button = CTkButton(master=library_window, text="Confirm", command=lambda: addGameToJSON())
    confirm_button.grid(row=6, column=0, pady=5)

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

            # Gets the exact number of game frames
            row_index = len(games_scroll_frame.winfo_children()) 

            # Add Game Frame
            addGameFrame(games_scroll_frame, title_text, description_text, False, row_index)

def changeTheme(theme_or_var, update=False):
    # Determine if input is StringVar or string
    if isinstance(theme_or_var, StringVar):
        theme = theme_or_var.get()
    else:
        theme = theme_or_var  # assume string

    set_appearance_mode(theme)

    # Check if update is needed
    if update:
        app.update_idletasks()

    # Update JSON if needed
    if update:
        addSetting(os.path.join(SAVE_PATH, "userData.json"), "theme", theme)


def addSettingsWindow(isDarkModeOn="dark"): # Settings window
    # Settings toplevel window configuration
    settings_window = CTkToplevel()
    settings_window.title("Add to Library")
    settings_window.geometry("400x300")

    settings_window.grid_columnconfigure(0, weight=1)
    settings_window.grid_rowconfigure(0, weight=1)

    settings_window.focus_force()
    settings_window.transient(app)

    # Frame inside top-level
    main_settings_frame = CTkFrame(master=settings_window)
    main_settings_frame.grid(sticky="ew",padx=10, pady=10, row=0, column=0)
    main_settings_frame.grid_columnconfigure(0, weight=1)
    main_settings_frame.grid_rowconfigure(0, weight=1)

    # Dark mode check box
    darkmode_var = StringVar(value=isDarkModeOn)
    dark_mode_check_box = CTkCheckBox(
        master=main_settings_frame,
        text="Dark Mode",
        variable=darkmode_var,
        onvalue="dark",
        offvalue="light",
        command=lambda: changeTheme(darkmode_var, update=True)
    )
    dark_mode_check_box.grid(row=0, column=0)


# Load save data from latest session
saveLatest = readJSON(os.path.join(SAVE_PATH, "userData.json"))

# Main App Configuration

changeTheme(saveLatest["settings"]["theme"], update=False)

app = CTk()
app.title("hazometric")

app.geometry("700x550")
app.maxsize(700,550)
app.minsize(700,550)

app.grid_columnconfigure(0, weight=0) # Configures the grid columns
app.grid_columnconfigure(1, weight=1) # Configures the grid columns
app.grid_rowconfigure(0, weight=1) # Configures the grid rows
app.grid_rowconfigure(1, weight=0) # Configures the grid rows

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
games_settings_button = CTkButton(master=utils_frame, text="Settings", command=lambda: addSettingsWindow(saveLatest["settings"]["theme"]))
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