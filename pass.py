import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip
from tkinter import Menu
import tkinter.messagebox as messagebox

# Custom validation function to check if a value is an integer
def is_integer(value):
    if value=='':
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function to generate a random password and copy it to the clipboard
def generate_password():
    user_input = user_input_entry.get()
    length = length_entry.get()
    
    try:
        length = int(length)
    except:
        length = random.randint(5,150)
    print(length)
    if length > 150:
        messagebox.showerror("Invalid Input", "Password length cannot exceed 150 characters.")
        return
   

    low_complexity = complexity_var_low.get()
    medium_complexity = complexity_var_medium.get()
    high_complexity = complexity_var_high.get()
    
    # Determine the character set based on the selected complexity levels
    characters = ""

    if low_complexity:
        characters += string.ascii_letters

    if medium_complexity:
        characters += string.digits

    if high_complexity:
        characters += string.punctuation

    exclude_chars = exclude_entry.get()
    
    # Remove excluded characters from the character set
    characters = ''.join(char for char in characters if char not in exclude_chars)
    
    # Initialize final_password
    final_password = ""

    # Generate a password with user input included
    total_length = length + len(user_input)
    try:
        generated_password = ''.join(random.choice(characters) for each in range(total_length))
        final_password = user_input + generated_password
    except:
        messagebox.showerror("Error", "Please Select Complexities.")

    result_label.config(text="Generated Password:\n" + final_password)  # Add \n for text wrapping
    
    # Copy the generated password to the clipboard
    pyperclip.copy(final_password)



# Function to save username, password, and website to an .env file
def save_account():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if website == '':
        messagebox.showerror("Error", "Please enter a website.")
        return
    if username == '':
        messagebox.showerror("Error", "Please enter a username to be stored.")
        return
    if password == '':
        messagebox.showerror("Error", "Please enter a password to be stored.")
        return

    # Save the account details to .env file
    with open('accounts.env', 'a') as env_file:
        env_file.write(f'{website}={username}:{password}\n')
    
    update_account_list()
    messagebox.showinfo("Success", "Login Successfully Saved!")

# Function to remove the selected entry from the account list
def remove_account():
    selected_item = accounts_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an account to remove.")
        return

    selected_index = selected_item[0]
    account_values = accounts_tree.item(selected_index, "values")
    website = account_values[0]
    username = account_values[1]
    password = account_values[2]

    confirmation = messagebox.askyesno("Delete Account?", f"Are you sure you want to delete the account for?\nWebsite: '{website}'\nUsername: '{username}'\nPassword: '{password}'")

    if confirmation:
        # Remove the selected account from the Treeview
        accounts_tree.delete(selected_index)

        # Rebuild the .env file with the updated list
        with open('accounts.env', 'w') as env_file:
            for item in accounts_tree.get_children():
                values = accounts_tree.item(item, "values")
                website = values[0]
                username = values[1]
                password = values[2]
                env_file.write(f'{website}={username}:{password}\n')


# Function to update the account list
def update_account_list():
    accounts_tree.delete(*accounts_tree.get_children())
    with open('accounts.env', 'r') as env_file:
        for line in env_file:
            parts = line.strip().split('=')
            if len(parts) == 2:
                website, login = parts
                username, password = login.split(':')
                accounts_tree.insert("", "end", values=(website, username, password))


# Function to search for an account by website or username
def search_accounts():
    search_query = search_entry.get().lower()
    # Clear the Treeview before populating it with search results
    for item in accounts_tree.get_children():
        accounts_tree.delete(item)
    
    with open('accounts.env', 'r') as env_file:
        for line in env_file:
            website, login = line.strip().split('=')
            username, password = login.split(':')
            if search_query in website.lower() or search_query in username.lower():
                # Insert the search result into the Treeview
                accounts_tree.insert("", "end", values=(website, username, password))

# Function to show the password generation section
def show_generate_password():
    generate_password_frame.pack()
    manage_accounts_frame.pack_forget()
    view_accounts_frame.pack_forget()

# Function to show the account management section
def show_manage_accounts():
    generate_password_frame.pack_forget()
    manage_accounts_frame.pack()
    view_accounts_frame.pack_forget()
    update_account_list()

# Function to show the account view section
def show_view_accounts():
    generate_password_frame.pack_forget()
    manage_accounts_frame.pack_forget()
    view_accounts_frame.pack()
    update_account_list()

# Function to clear the fields
def clear_fields():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    

# Create the main window
root = tk.Tk()

#root.resizable(False, False)
root.title("Ethan's Password Manager")

# Set the window size
root.geometry("450x375")  # Width x Height

# Create a menu
menu = Menu(root)
root.config(menu=menu)

# Create menu items
menu.add_command(label="Generate Password", command=show_generate_password)
menu.add_command(label="Add New Account", command=show_manage_accounts)
menu.add_command(label="View Accounts", command=show_view_accounts)

# Frame for password generation
generate_password_frame = tk.Frame(root)

# Label and Entry for user input
user_input_label = tk.Label(generate_password_frame, text="Enter Your Text:")
user_input_label.pack(pady=5)
user_input_entry = tk.Entry(generate_password_frame)
user_input_entry.pack()

# Label and Entry for password length
length_label = tk.Label(generate_password_frame, text="Additional Password Length:")
length_label.pack(pady=5)
length_entry = tk.Entry(generate_password_frame)
length_entry.pack()

# Validation for password length (accepts only integers)
validate_length = root.register(is_integer)
length_entry.config(validate="key", validatecommand=(validate_length, "%P"))

# Label and Entry for excluded characters
exclude_label = tk.Label(generate_password_frame, text="Exclude Characters:")
exclude_label.pack(pady=5)
exclude_entry = tk.Entry(generate_password_frame)
exclude_entry.pack()

# Checkboxes for complexity
complexity_var_low = tk.BooleanVar(value=False)  # Define complexity_var_low with an initial value
complexity_var_medium = tk.BooleanVar(value=False)
complexity_var_high = tk.BooleanVar(value=False)

# Radio buttons for complexity
complexity_var = tk.StringVar(value="Low")
complexity_label = tk.Label(generate_password_frame, text="Complexity:")
complexity_label.pack()
low_complexity = tk.Checkbutton(generate_password_frame, text="Characters", variable=complexity_var_low)
medium_complexity = tk.Checkbutton(generate_password_frame, text="Digits", variable=complexity_var_medium)
high_complexity = tk.Checkbutton(generate_password_frame, text="Special Characters", variable=complexity_var_high)
low_complexity.pack(padx=10)
medium_complexity.pack(padx=10)
high_complexity.pack(padx=10)

# Generate Password button
generate_password_button = tk.Button(generate_password_frame, text="Generate Password", command=generate_password)
generate_password_button.pack(pady=10)

# Label to display the generated password with text wrapping
result_label = tk.Label(generate_password_frame, text="", wraplength=350)  # Adjust wraplength as needed
result_label.pack(pady=10)

# Center the frame in the window vertically and horizontally
generate_password_frame.pack(expand=True, fill='both')

# Frame for account management
manage_accounts_frame = tk.Frame(root)

# Label, Entry, and Button for managing accounts
website_label = tk.Label(manage_accounts_frame, text="Website/Company:")
website_label.pack(pady=10)
website_entry = tk.Entry(manage_accounts_frame)
website_entry.pack()

username_label = tk.Label(manage_accounts_frame, text="Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(manage_accounts_frame)
username_entry.pack()

password_label = tk.Label(manage_accounts_frame, text="Password:")
password_label.pack(pady=10)
password_entry = tk.Entry(manage_accounts_frame, show="*")  # Password field
password_entry.pack()

save_account_button = tk.Button(manage_accounts_frame, text="Save Account", command=lambda: [save_account(), clear_fields()])
save_account_button.pack(pady=10)

# Frame for account view
view_accounts_frame = tk.Frame(root)

# Label and Entry for searching accounts
search_label = tk.Label(view_accounts_frame, text="Search by Website or Username:")
search_label.pack()
search_entry = tk.Entry(view_accounts_frame)
search_entry.pack()

# Search button
search_button = tk.Button(view_accounts_frame, text="Search", command=search_accounts)
search_button.pack(pady=15)

# Create a frame to contain the Treeview with custom dimensions
tree_frame = ttk.Frame(view_accounts_frame)
tree_frame.pack(expand=True, fill="both", padx=10, pady=10)  # You can adjust padx and pady as needed

# Create a Treeview widget inside the frame with a fixed height (adjust as needed)
accounts_tree = ttk.Treeview(tree_frame, columns=("Website", "Username", "Password"), show="headings", height=5, selectmode="extended")
accounts_tree.heading("Website", text="Website", anchor="w")  # Use "anchor" to left-align the column headers
accounts_tree.heading("Username", text="Username", anchor="w")
accounts_tree.heading("Password", text="Password", anchor="w")

# Set the width of each column to 50 pixels
accounts_tree.column("Website", width=120)
accounts_tree.column("Username", width=120)
accounts_tree.column("Password", width=120)

accounts_tree.pack(side="left", fill="both", expand=True)

# Create vertical scrollbar
y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=accounts_tree.yview)
y_scrollbar.pack(side="right", fill="y")
accounts_tree.configure(yscrollcommand=y_scrollbar.set)

# Create horizontal scrollbar
x_scrollbar = ttk.Scrollbar(view_accounts_frame, orient="horizontal", command=accounts_tree.xview)
x_scrollbar.pack(side="bottom", fill="x")
accounts_tree.configure(xscrollcommand=x_scrollbar.set)

remove_button = tk.Button(view_accounts_frame, text="Remove", command=remove_account)
remove_button.pack(pady=10)

# Initially, show the password generation section
show_generate_password()

# Start the Tkinter main loop
root.mainloop()
