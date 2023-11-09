# Elective Project Python - AS23 - Group11

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import re


# Define the path for the contacts file
contacts_file_path = 'contacts.json'

# Load contacts from the file if it exists
def load_contacts():
    if os.path.exists(contacts_file_path):
        with open(contacts_file_path, 'r') as file:
            return json.load(file)
    return {}

# Save contacts to the file
def save_contacts(contacts):
    with open(contacts_file_path, 'w') as file:
        json.dump(contacts, file, indent=4)

# Initialize the contacts
contacts = load_contacts()

# Adding and Editing a Contact - inclusive Errormessage and Validation
def add_or_edit_contact(name, phone, email, edit=False):
    # Name validation: Accept only letters
    if not re.match(r'^[A-Za-z\s]+$', name):
        messagebox.showerror("Error", "Invalid name. Please use only letters (A-Z, a-z) and spaces.")
        return

    # Phone validation: Accept only numbers
    if not re.match(r'^[0-9]+$', phone):
        messagebox.showerror("Error", "Invalid phone. Please use only numbers (0-9).")
        return

    # Email validation: Accept only valid email addresses
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        messagebox.showerror("Error", "Invalid email address. Please use a valid email format (e.g., name@example.com).")
        return

    # Check if editing an existing contact
    if edit and name not in contacts:
        messagebox.showerror("Error", "Contact does not exist.")
        return

    # Add or edit the contact
    contacts[name] = {'phone': phone, 'email': email}
    save_contacts(contacts)
    refresh_contacts_list()
    messagebox.showinfo("Success", "Contact has been added." if not edit else "Contact has been updated.")


# Define the function to delete a contact
def delete_contact(name):
    if name in contacts:
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            del contacts[name]
            save_contacts(contacts)
            refresh_contacts_list()
            messagebox.showinfo("Success", "Contact has been deleted.")
    else:
        messagebox.showerror("Error", "Contact does not exist.")

# Define the function to search for a contact
def search_contact():
    name = simpledialog.askstring("Search Contact", "Enter the name of the contact:")
    if name in contacts:
        contact_info = contacts[name]
        messagebox.showinfo("Contact Found",
                            f"Name: {name}\nPhone: {contact_info['phone']}\nEmail: {contact_info['email']}")
    else:
        messagebox.showerror("Error", "Contact not found.")

# Define the function to refresh the contacts list on the GUI
def refresh_contacts_list():
    contacts_listbox.delete(0, tk.END)
    # Display names in alphabetical order
    for name in sorted(contacts.keys()):
        contacts_listbox.insert(tk.END, name)

# Define the function to create the add/edit contact form
def open_add_edit_contact_form(edit=False):
    selected = contacts_listbox.curselection()
    if edit and not selected:
        messagebox.showerror("Error", "No contact selected for editing.")
        return
    contact_name = contacts_listbox.get(selected[0]) if selected else ""

    # Create a new window for adding/editing contacts
    add_edit_window = tk.Toplevel(root)
    add_edit_window.title("Edit Contact" if edit else "Add Contact")

    # Name Entry
    tk.Label(add_edit_window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_edit_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.insert(0, contact_name)
    name_entry.config(state='readonly' if edit else 'normal')

    # Phone Entry
    tk.Label(add_edit_window, text="Phone:").grid(row=1, column=0, padx=10, pady=5)
    phone_entry = tk.Entry(add_edit_window)
    phone_entry.grid(row=1, column=1, padx=10, pady=5)
    phone_entry.insert(0, contacts[contact_name]['phone'] if edit else "")

    # Email Entry
    tk.Label(add_edit_window, text="Email:").grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(add_edit_window)
    email_entry.grid(row=2, column=1, padx=10, pady=5)
    email_entry.insert(0, contacts[contact_name]['email'] if edit else "")

    # Save Button
    save_button_text = "Save" if edit else "Add"
    save_button_bg = '#ff6f61' if edit else '#f39c12'  # Warm red for delete, warm orange for edit
    save_button = tk.Button(add_edit_window, text=save_button_text,
                            command=lambda: add_or_edit_contact(name_entry.get(),
                                                                phone_entry.get(),
                                                                email_entry.get(), edit),
                            bg=save_button_bg, fg='white', padx=10, pady=5)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)



# Create the main window
root = tk.Tk()
root.title("Simple Contact Book")
root.configure(bg='#e0e0e0')  # Set background color to grey

# Listbox to display contacts
contacts_listbox = tk.Listbox(root, width=50, height=15, selectbackground='#2980b9', bg='#e0e0e0')
contacts_listbox.pack(pady=10)

# Frame to organize buttons with a grey background
frame = tk.Frame(root, bg='#e0e0e0')
frame.pack(pady=10)

# Add Contact Button
add_contact_button = tk.Button(frame, text="Add Contact", command=lambda: open_add_edit_contact_form(edit=False),
                               bg='#f39c12', fg='white', padx=10, pady=5)
add_contact_button.pack(side=tk.LEFT, padx=5)

# Edit Contact Button
edit_contact_button = tk.Button(frame, text="Edit Contact", command=lambda: open_add_edit_contact_form(edit=True),
                                bg='#E67B35', fg='white', padx=10, pady=5)
edit_contact_button.pack(side=tk.LEFT, padx=5)

# Delete Contact Button
delete_contact_button = tk.Button(frame, text="Delete Contact", command=lambda: delete_contact(contacts_listbox.get(tk.ANCHOR)),
                                  bg='#e74c3c', fg='white', padx=10, pady=5)
delete_contact_button.pack(side=tk.LEFT, padx=5)

# Search Contact Button
search_contact_button = tk.Button(frame, text="Search Contact", command=search_contact,
                                  bg='#3498db', fg='white', padx=10, pady=5)
search_contact_button.pack(side=tk.LEFT, padx=5)

# Refresh the contacts list
refresh_contacts_list()

# Run the application
root.mainloop()

# Create the main window
root = tk.Tk()
root.title("Simple Contact Book")
root.configure(bg='#e0e0e0')  # Set background color to grey

# Listbox to display contacts
contacts_listbox = tk.Listbox(root, width=50, height=15, selectbackground='#2980b9', bg='#e0e0e0')
contacts_listbox.pack(pady=10)

# Frame to organize buttons with a grey background
frame = tk.Frame(root, bg='#e0e0e0')
frame.pack(pady=10)

# Add Contact Button
add_contact_button = tk.Button(frame, text="Add Contact", command=lambda: open_add_edit_contact_form(edit=False),
                               bg='#f39c12', fg='white', padx=10, pady=5)
add_contact_button.pack(side=tk.LEFT, padx=5)

# Edit Contact Button
edit_contact_button = tk.Button(frame, text="Edit Contact", command=lambda: open_add_edit_contact_form(edit=True),
                                bg='#E67B35', fg='white', padx=10, pady=5)
edit_contact_button.pack(side=tk.LEFT, padx=5)

# Delete Contact Button
delete_contact_button = tk.Button(frame, text="Delete Contact", command=lambda: delete_contact(contacts_listbox.get(tk.ANCHOR)),
                                  bg='#e74c3c', fg='white', padx=10, pady=5)
delete_contact_button.pack(side=tk.LEFT, padx=5)

# Search Contact Button
search_contact_button = tk.Button(frame, text="Search Contact", command=search_contact,
                                  bg='#3498db', fg='white', padx=10, pady=5)
search_contact_button.pack(side=tk.LEFT, padx=5)

# Refresh the contacts list
refresh_contacts_list()

# Run the application
root.mainloop()
