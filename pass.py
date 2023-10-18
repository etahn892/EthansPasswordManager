import tkinter as tk
import random
import string
import pyperclip
from tkinter import Menu
import tkinter.messagebox as messagebox

# Custom validation function to check if a value is an integer
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function to generate a random password and copy it to the clipboard
def generate_password():
    user_input = user_input_entry.get()
    length = length_entry.get()
    
    if not is_integer(length):
        messagebox.showerror("Invalid Input", "Password length must be an integer.")
        return
    
    length = int(length)

    if length > 256:
        messagebox.showerror("Invalid Input", "Password length cannot exceed 256 characters.")
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
    
    # Generate a password with user input included
    remaining_length = length - len(user_input)
    try:
        generated_password = ''.join(random.choice(characters) for _ in range(remaining_length))
        final_password = user_input + generated_password
    except:
        pass
    
    result_label.config(text="Generated Password:\n" + final_password)  # Add \n for text wrapping
    
    # Copy the generated password to the clipboard
    pyperclip.copy(final_password)


# Function to save username, password, and website to an .env file
def save_account():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    
    # Save the account details to .env file
    with open('.env', 'a') as env_file:
        env_file.write(f'{website}={username}:{password}\n')
    
    update_account_list()

# Function to remove the selected entry from the account list
def remove_account():
    selected_item = accounts_list.curselection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an account to remove.")
        return
    
    selected_index = selected_item[0]
    accounts_list.delete(selected_index)
    
    # Rebuild the .env file with the updated list
    with open('.env', 'w') as env_file:
        for i in range(accounts_list.size()):
            env_file.write(accounts_list.get(i) + '\n')

# Function to update the account list
def update_account_list():
    accounts_list.delete(0, tk.END)
    with open('.env', 'r') as env_file:
        for line in env_file:
            parts = line.strip().split('=')
            if len(parts) == 2:
                website, login = parts
                username, password = login.split(':')
                accounts_list.insert(tk.END, f'Website: {website}, Username: {username}, Password: {password}')
            else:
                pass

# Function to search for an account by website or username
def search_accounts():
    search_query = search_entry.get().lower()
    accounts_list.delete(0, tk.END)
    with open('.env', 'r') as env_file:
        for line in env_file:
            website, login = line.strip().split('=')
            username, password = login.split(':')
            if search_query in website.lower() or search_query in username.lower():
                accounts_list.insert(tk.END, f'Website: {website}, Username: {username}, Password: {password}')

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

# Create the main window
root = tk.Tk()
root.title("Password Manager")

# Set the window size
root.geometry("500x350")  # Width x Height

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
user_input_label.pack()
user_input_entry = tk.Entry(generate_password_frame)
user_input_entry.pack()

# Label and Entry for password length
length_label = tk.Label(generate_password_frame, text="Password Length:")
length_label.pack()
length_entry = tk.Entry(generate_password_frame)
length_entry.pack()

# Validation for password length (accepts only integers)
validate_length = root.register(is_integer)
length_entry.config(validate="key", validatecommand=(validate_length, "%P"))

# Label and Entry for excluded characters
exclude_label = tk.Label(generate_password_frame, text="Exclude Characters:")
exclude_label.pack()
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
low_complexity.pack()
medium_complexity.pack()
high_complexity.pack()




# Label to display the generated password with text wrapping
result_label = tk.Label(generate_password_frame, text="", wraplength=350)  # Adjust wraplength as needed
result_label.pack(pady=10)

# Generate Password button
generate_password_button = tk.Button(generate_password_frame, text="Generate Password", command=generate_password)
generate_password_button.pack(pady=10)
# Frame for account management
manage_accounts_frame = tk.Frame(root)

# Label, Entry, and Button for managing accounts
website_label = tk.Label(manage_accounts_frame, text="Website/Company:")
website_label.pack()
website_entry = tk.Entry(manage_accounts_frame)
website_entry.pack()

username_label = tk.Label(manage_accounts_frame, text="Username:")
username_label.pack()
username_entry = tk.Entry(manage_accounts_frame)
username_entry.pack()

password_label = tk.Label(manage_accounts_frame, text="Password:")
password_label.pack()
password_entry = tk.Entry(manage_accounts_frame, show="*")  # Password field
password_entry.pack()

save_account_button = tk.Button(manage_accounts_frame, text="Save Account", command=save_account)
save_account_button.pack()

# Frame for account view
view_accounts_frame = tk.Frame(root)

# Label and Entry for searching accounts
search_label = tk.Label(view_accounts_frame, text="Search by Website or Username:")
search_label.pack()
search_entry = tk.Entry(view_accounts_frame)
search_entry.pack()

# Search button
search_button = tk.Button(view_accounts_frame, text="Search", command=search_accounts)
search_button.pack()

# Listbox to display account details
accounts_list = tk.Listbox(view_accounts_frame, selectmode=tk.SINGLE, height=10, width=50)
accounts_list.pack()

# Scrollbar for the account list
scrollbar = tk.Scrollbar(view_accounts_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the Listbox and Scrollbar to work together
accounts_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=accounts_list.yview)

remove_button = tk.Button(view_accounts_frame, text="Remove", command=remove_account)
remove_button.pack()

# Initially, show the password generation section
show_generate_password()

# Start the Tkinter main loop
root.mainloop()
