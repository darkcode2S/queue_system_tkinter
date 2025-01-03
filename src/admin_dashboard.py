import customtkinter as ctk
import tkinter as tk
from tkinter import BOTTOM, END, HORIZONTAL, RIGHT, VERTICAL, Event, PhotoImage, Scrollbar, StringVar, ttk
from PIL import Image 
from tkinter import messagebox
import re
import bcrypt
from center_window import center_window
from db import create_connection
from mysql.connector import Error

# Initialize the main application window
admin = ctk.CTk()
admin.title("Admin")
admin.iconbitmap("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico")


# Set appearance mode and color theme (Light/Dark modes)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")
# Center the window on the screen
window_width = 1000
window_height = 550
screen_width = admin.winfo_screenwidth()
screen_height = admin.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
admin.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Show the sensitive data warning message
# messagebox.showinfo("Info", "Please be aware that you are accessing sensitive data.")


# Configure the style
style = ttk.Style()
style.configure("Treeview", 
                background="#f0f0f0",
                foreground="black",
                rowheight=25,
                fieldbackground="#f0f0f0")
style.configure("Treeview.Heading", 
                background="lightblue",  # Green background for headings
                foreground="#000",
                font=("Arial", 10, "bold"))  # Bold font for headings
style.map("Treeview", 
          background=[('selected', '#0078D7')])  # Highlight selected row

# Define alternating row colors
style.configure("evenrow", background="white")
style.configure("oddrow", background="#D3D3D3")  # Light gray background for odd rows


# Create the main frame for content
main_frame = ctk.CTkFrame(admin, width=700, height=300)
main_frame.pack(side="left", expand=True, fill="both")

# Sidebar frame
sidebar_frame = ctk.CTkFrame(main_frame, width=200, height=300, fg_color="transparent")
sidebar_frame.pack(side="left", fill="both", padx="20")

logo_icon = ctk.CTkImage(light_image=Image.open("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.png"),
                     dark_image=Image.open("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.png"),
                     size=(60, 60))  # Resize to 24x24 pixels

logo_ncmc = ctk.CTkLabel(sidebar_frame, image=logo_icon, text="")
logo_ncmc.pack(pady=(20,5))

table_label = ctk.CTkLabel(
    sidebar_frame,
    text="Tables",
    font=ctk.CTkFont(),
    text_color="#000000",
    anchor="w"  # Use "w" for west (left)
)
table_label.pack(anchor="w", padx=(8, 0), pady=(10, 0))

# Create dropdown menu for selecting members, queue, and passwords
dropdown_var = ctk.StringVar(value="Queue")
dropdown = ctk.CTkOptionMenu(sidebar_frame, variable=dropdown_var, 
                              values=["Queue", 'Students', 
                                      "Members", "Operators"], 
                              fg_color="#fff",
                              text_color="#000",
                              dropdown_fg_color="#fff",
                              button_color="orange",
                              dropdown_hover_color="orange",
                              button_hover_color="#de9420",
                              anchor="s",
                              command=lambda choice: update_table(choice))
dropdown.pack(pady=(0, 10))

# #button icon 
# add_icon = ctk.CTkImage(light_image=Image.open("add-button.png"),
#                      dark_image=Image.open("add-button.png"),
#                      size=(24, 24))  # Resize to 24x24 pixels
# update_icon = ctk.CTkImage(light_image=Image.open("update.png"),
#                      dark_image=Image.open("update.png"),
#                      size=(24, 24))  # Resize to 24x24 pixels
# remove_icon = ctk.CTkImage(light_image=Image.open("trash-can.png"),
#                      dark_image=Image.open("trash-can.png"),
#                      size=(24, 24))  # Resize to 24x24 pixels
# settings_icon = ctk.CTkImage(light_image=Image.open("settings.png"),
#                      dark_image=Image.open("settings.png"),
#                      size=(24, 24))  # Resize to 24x24 pixels
# logout_icon = ctk.CTkImage(light_image=Image.open("log-out.png"),
#                      dark_image=Image.open("log-out.png"),
#                      size=(24, 24))  # Resize to 24x24 pixels

# Create buttons for adding, deleting, and updating records
add_button = ctk.CTkButton(sidebar_frame, text="  Add Record  ", compound="left", text_color="#000", fg_color="white", hover_color="#de9420", command=lambda: add_record())
add_button.pack(pady=10)

update_button = ctk.CTkButton(sidebar_frame, text="Update Record",  compound="left", text_color="#000", fg_color="white", hover_color="#de9420", command=lambda: update_record())
update_button.pack(pady=10)

remove_button = ctk.CTkButton(sidebar_frame, text="Remove Record", compound="left", text_color="#000", fg_color="white", hover_color="#de9420", command=lambda: remove_record())
remove_button.pack(pady=10)

settings_button = ctk.CTkButton(sidebar_frame, text="  Settings  ", compound="left", text_color="#000", fg_color="white", hover_color="#de9420", command=lambda: settings_for_admin())
settings_button.pack(pady=10)

logout_button = ctk.CTkButton(sidebar_frame, text="  Log out  ", compound="left", text_color="#fff", fg_color="#1768ff", hover_color="#de9420", command=lambda: confirm_logout())
logout_button.pack(side="bottom", pady='30')

# Table Frame to handle all table
table_frame = ctk.CTkFrame(main_frame, width=500, height=300, fg_color='lightgray')
table_frame.pack(side="right", fill="both", expand=True)

#Navbar frame
search_icon = ctk.CTkImage(light_image=Image.open("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\search.png"),#seach ison
                     dark_image=Image.open("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\search.png"),
                     size=(15, 15))  # Resize to 24x24 pixels

nav_frame = ctk.CTkFrame(table_frame, width=800, height=60, fg_color='#d68b26')
nav_frame.pack(side='top', fill='x')

title_label = ctk.CTkLabel(nav_frame,
                            text='Queue table',
                            anchor='w',
                            compound='left', 
                            text_color='#fff',
                            font=ctk.CTkFont(size=15, weight="bold"))
title_label.pack(side='left',pady=20, padx=20)

cancel_search = ctk.CTkButton(nav_frame, text='Cancel', width=50, command=lambda: cancel_search_action())
cancel_search.pack(side='right',pady=20, padx=(5,20))
cancel_search.configure(state="disabled")

search_button = ctk.CTkButton(nav_frame,
                              text='Search  ',
                              image=search_icon,
                              anchor='w', 
                              width=50, 
                              command=lambda: search())
search_button.pack(side='right',pady=20, padx=(5,0))

search_bar = ctk.CTkEntry(nav_frame, width=250, placeholder_text='Search ID...')
search_bar.pack(side='right',pady=20, padx=(20,0))

show_info = ctk.CTkButton(table_frame, 
                          text='Show info', 
                          width=60,
                          command=lambda: show_data())
show_info.pack(side='top', anchor='e', pady=(10, 0), padx=10)

from tkinter.scrolledtext import ScrolledText

from tkinter.scrolledtext import ScrolledText

def show_data():
    if dropdown_var.get() == "Queue":
        global item_values
        selected_item = table.selection()  

        if selected_item: 
            item_values = table.item(selected_item[0], 'values')  
            print(f"Selected values: {item_values}")  
        else:
            print("No item selected") 

        if not selected_item:  
            messagebox.showwarning("Warning", "Please select an item from the table first.")
            return  
                
        mini = tk.Toplevel(admin)
        mini.title("Information")
        mini.iconbitmap('C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico')

        center_window(300, 300, mini)

        # Create ScrolledText widget
        scrolled_text = ScrolledText(mini, wrap=tk.WORD, width=40, height=15)
        scrolled_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configure tags for bold text
        scrolled_text.tag_configure("bold", font=("Helvetica", 10, "bold"))

        # Insert each line with bold field names
        lines = [
            ("Queue number: ", item_values[0]),
            ("Created at: ", item_values[1]),
            ("School ID: ", item_values[2]),
            ("Full name: ", item_values[3]),
            ("Transaction: ", item_values[4]),
            ("Affiliation: ", item_values[5]),
            ("Phone: ", item_values[6]),
            ("Purpose: ", item_values[7]),
            ("Compilation time: ", item_values[8]),
            ("Status: ", item_values[9]),
        ]

        for label, value in lines:
            scrolled_text.insert(tk.END, label, "bold")  # Insert the field name with bold formatting
            scrolled_text.insert(tk.END, f"{value}\n")   # Insert the corresponding value

        scrolled_text.config(state=tk.DISABLED)  # Make the text read-only

        mini.grab_set()


    elif dropdown_var.get() == "Students":

        if not selected_item_values:  
            messagebox.showwarning("Warning", "Please select an item from the table first.")
            return  

        # Create a new Toplevel window
        mono = tk.Toplevel(admin)
        mono.title("Information")
        mono.iconbitmap('C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico')

        # Center the window
        center_window(300, 200, mono)

        # Create a ScrolledText widget for displaying the information
        scrolled_text = ScrolledText(mono, wrap=tk.WORD, width=40, height=10)
        scrolled_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configure tags for bold text
        scrolled_text.tag_configure("bold", font=("Helvetica", 10, "bold"))

        # Prepare the information to be displayed
        labels_values = [
            ("School ID: ", selected_item_values[1]),
            ("Full name: ", selected_item_values[2]),
            ("Course: ", selected_item_values[3]),
            ("Year level: ", selected_item_values[4]),
        ]

        # Insert the information into the ScrolledText widget
        for label, value in labels_values:
            scrolled_text.insert(tk.END, label, "bold")  # Insert the field name with bold formatting
            scrolled_text.insert(tk.END, f"{value}\n")   # Insert the corresponding value

        # Make the text read-only
        scrolled_text.config(state=tk.DISABLED)

        # Make the window modal (block interaction with parent)
        mono.grab_set()

    elif dropdown_var.get() == "Members":
        if not select_member_value:  
            messagebox.showwarning("Warning", "Please select an item from the table first.")
            return  

        # Create a new Toplevel window
        mono = tk.Toplevel(admin)
        mono.title("Information")
        mono.iconbitmap('C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico')

        # Center the window
        center_window(300, 300, mono)

        # Create a ScrolledText widget for displaying the information
        scrolled_text = ScrolledText(mono, wrap=tk.WORD, width=40, height=10)
        scrolled_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configure tags for bold text
        scrolled_text.tag_configure("bold", font=("Helvetica", 10, "bold"))

        # Prepare the information to be displayed
        member_info = [
            ("School ID: ", select_member_value[1]),
            ("Full name: ", select_member_value[2]),
            ("Affiliation: ", select_member_value[3]),
            ("Role: ", select_member_value[4]),
            ("Office: ", select_member_value[5]),
        ]

        # Insert each label and value into the ScrolledText widget
        for label, value in member_info:
            scrolled_text.insert(tk.END, label, "bold")  # Insert the label with bold formatting
            scrolled_text.insert(tk.END, f"{value}\n")   # Insert the corresponding value

        # Make the text read-only
        scrolled_text.config(state=tk.DISABLED)

        # Make the window modal (block interaction with parent)
        mono.grab_set()

    elif dropdown_var.get() == "Operators":

        # Check if an item is selected
        if not item_values:  
            messagebox.showwarning("Warning", "Please select an item from the table first.")
            return  

        # Create a new Toplevel window
        mono = tk.Toplevel(admin)
        mono.title("Information")
        mono.iconbitmap('C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico')

        # Center the window
        center_window(300, 300, mono)

        # Create a ScrolledText widget for displaying the information
        scrolled_text = ScrolledText(mono, wrap=tk.WORD, width=40, height=10)
        scrolled_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configure tags for bold text
        scrolled_text.tag_configure("bold", font=("Helvetica", 10, "bold"))

        # Prepare the information to be displayed
        item_info = [
            ("School ID: ", item_values[1]),
            ("Full name: ", item_values[2]),
            ("Operate area: ", item_values[3]),
            ("Phone: ", item_values[4]),
            ("Username: ", item_values[5]),
            ("Password: ", item_values[6]),
        ]

        # Insert each label and value into the ScrolledText widget
        for label, value in item_info:
            scrolled_text.insert(tk.END, label, "bold")  # Insert the label with bold formatting
            scrolled_text.insert(tk.END, f"{value}\n")   # Insert the corresponding value

        # Make the text read-only
        scrolled_text.config(state=tk.DISABLED)

        # Make the window modal (block interaction with parent)
        mono.grab_set()
    
    else:
        messagebox.showwarning("Warning", "Please select data")


    
# TabView for students , padx=(0, 20)
tab_view = ctk.CTkTabview(table_frame, width=500, height=300, anchor="nw", fg_color='lightgray')
tab_view.pack_forget()  # Initially hide the tab view

# Dictionary to store table references for each tab
tables = {}

# List of tabs to create dynamically
tab_list = ["BSCS", "BS-CRIM", "BSSW", "BSEE", "BSMT", "BSM", "BEED", "BSED", "BSBA", "BSHM", "BSA", "BAPS"]


selected_item_values = None  # Variable to store the currently selected item values

# Function to handle selection from the table
def on_item_selected(event, tab_name):
    global selected_item_values  # Use the global variable to store selected values
    selected_table = tables[tab_name]  # Get the table reference
    selected_item = selected_table.selection()  # Get selected item
    if selected_item:
        selected_item_values = selected_table.item(selected_item, "values")  # Get the values of the selected item
        print(f"Selected Item from {tab_name}: {selected_item_values}")  # Process or display the selected values


# Function to dynamically create tabs and tables for students
for tab_name in tab_list:
    tab_view.add(tab_name)  # Add the tab
    table_student = ttk.Treeview(tab_view.tab(tab_name), show="headings")
    table_student['columns'] = ('id','School ID', 'Full name', 'Course', 'Year&level')
    
    table_student.column("#0", width=0, stretch="no")
    table_student.column("id", anchor="center", width=0, stretch=tk.NO)
    table_student.column("School ID", anchor="center", width=80)
    table_student.column("Full name", anchor="center", width=80)
    table_student.column("Course", anchor="center", width=80)
    table_student.column("Year&level", anchor="center", width=80)
    # , width=0, stretch=tk.NO
    table_student.heading("#0", text="")
    table_student.heading("id", text="id")
    table_student.heading("School ID", text="School ID")
    table_student.heading("Full name", text="Full name")
    table_student.heading("Course", text="Course")
    table_student.heading("Year&level", text="Year Level")

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(tab_view.tab(tab_name), orient="vertical", command=table_student.yview)
    table_student.configure(yscroll=scrollbar.set)

    # Pack the Treeview and scrollbar
    table_student.pack(fill="both", expand=True, side="left", padx=(20, 0))
    scrollbar.pack(fill="y", side="right")
    
    # table_student.pack(fill="both", expand=True, padx=20)
    
    # Bind the selection event to the table , pady=(0, 20)
    table_student.bind("<<TreeviewSelect>>", lambda event, tab_name=tab_name: on_item_selected(event, tab_name))
    
    tables[tab_name] = table_student  # Store the table reference for each tab


 # Create tabs and tables dynamically

table = ttk.Treeview(table_frame)
table.pack(fill="both", expand=True, pady=20, padx=20)

#queue table logic-----------------------------------------------------------------------------------------------
def fetch_queue_data():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT  queue_number, created_at, school_id, full_name, transaction, affiliation, phone, purpose_of_visit, compilation_time, voided FROM queue_admin")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# Remove all existing rows from the TreeView table
def clear_table(table):
    # Remove all existing rows from the TreeView table
    for row in table.get_children():
        table.delete(row)

#Queue table-----------------------------------------------------------------------------------------------
table['columns'] = ('Queue number',
                        'Created at', 
                        'School ID',
                        'Full name', 
                        'Transaction', 
                        'Affiliation',
                        'Phone',
                        'Purpose of visit',
                        'Compilation time', 
                        'Voided')  

# Horizontal and vertical scrollbars
scrollbarx = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
scrollbary = Scrollbar(table, orient=VERTICAL, command=table.yview)

# Configure scrollbars to work with the table
table.configure(xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set)

# Place scrollbars
scrollbarx.pack(side='bottom', fill='x')
scrollbary.pack(side='right', fill='y')

table.column("#0", width=0, stretch="no")  # Hide the first column
table.column("Queue number", anchor="center", width=110, stretch="no")
table.column("Created at", anchor="center", stretch="no")
table.column("School ID", anchor="center", width=100, stretch="no")
table.column("Full name", anchor="center", stretch="no")
table.column("Transaction", anchor="center", stretch="no")
table.column("Affiliation", anchor="center", width=100, stretch="no")
table.column("Phone", anchor="center", width=100, stretch="no")
table.column("Purpose of visit", anchor="center", stretch="no")
table.column("Compilation time", anchor="center", stretch="no")
table.column("Voided", anchor="center", width=100, stretch="no")

table.heading("#0", text="")
table.heading("Queue number", text="Queue Number") 
table.heading("Created at", text="Created at") # Use correct name for heading too
table.heading("School ID", text="School ID")
table.heading("Full name", text="Full name")
table.heading("Transaction", text="Transaction")
table.heading("Affiliation", text="Affiliation")
table.heading("Phone", text="Phone")
table.heading("Purpose of visit", text="Purpose of visit")
table.heading("Compilation time", text="Compilation Time")
table.heading("Voided", text="Status")

# Fetch and display data
data = fetch_queue_data()
for row in data:
    table.insert("", "end", values=row)

item_values = None

#get value wehn selected operator table
def on_item_selected_password(event):
    global item_values
    selected_item = table.selection()  # Get the selected items (returns a tuple)

    if selected_item:  # Check if any item is selected
        item_values = table.item(selected_item[0], 'values')  # Get the values of the selected item
        print(f"Selected values: {item_values}")  # Do something with the values
    else:
        print("No item selected")  # Handle the case where no item is selected

table.bind("<<TreeviewSelect>>", on_item_selected_password)
#queue table logic-----------------------------------------------------------------------------------------------

# Create Treeview tables inside each Tab
# TabView for Members
tab_member = ctk.CTkTabview(table_frame, width=500, height=300, anchor="nw" , fg_color='lightgray')
tab_member.pack_forget()  # Initially hide the tab view

# Dictionary to store table references for each tab
member_tables = {}

# List of tabs to create dynamically
member_list = ['School staff', 'School faculty']


select_member_value = None  # Variable to store the currently selected item values

# Function to handle selection from the table
def member_selected(event, member_name):
    global select_member_value  # Use the global variable to store selected values
    selected_table = member_tables[member_name]  # Get the table reference
    selected_item = selected_table.selection()  # Get selected item
    if selected_item:
        select_member_value = selected_table.item(selected_item, "values")  # Get the values of the selected item
        print(f"Selected Item from {member_name}: {select_member_value}")  # Process or display the selected values


# Function to dynamically create tabs and tables for members
for member_name in member_list:
    tab_member.add(member_name)  # Add the tab
    table_member = ttk.Treeview(tab_member.tab(member_name), show="headings")
    table_member['columns'] = ('id','School ID', 'Full name', 'Affiliation', 'Role', 'Office')
    
    table_member.column("#0", width=0, stretch="no")
    table_member.column("id", anchor="center", width=0, stretch=tk.NO)
    table_member.column("School ID", anchor="center", width=80)
    table_member.column("Full name", anchor="center", width=80)
    table_member.column("Affiliation", anchor="center", width=80)
    table_member.column("Role", anchor="center", width=80)
    table_member.column("Office", anchor="center", width=80)
    
    table_member.heading("#0", text="")
    table_member.heading("id", text="id")
    table_member.heading("School ID", text="School ID")
    table_member.heading("Full name", text="Full name")
    table_member.heading("Affiliation", text="Affiliation")
    table_member.heading("Role", text="Role")
    table_member.heading("Office", text="Office")
    
    # table_member.pack(fill="both", expand=True, padx=20)
    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(tab_member.tab(member_name), orient="vertical", command=table_member.yview)
    table_student.configure(yscroll=scrollbar.set)

    # Pack the Treeview and scrollbar
    table_member.pack(fill="both", expand=True, side="left", padx=(20, 0))
    scrollbar.pack(fill="y", side="right")
    
    # Bind the selection event to the table , pady=(0, 20) 
    table_member.bind("<<TreeviewSelect>>", lambda event, member_name=member_name: member_selected(event, member_name))
    
    member_tables[member_name] = table_member  # Store the table reference for each tab


global course_name
# Function to add unique data to a table
def add_unique_data_to_table(tree, data):
    existing_data = [tree.item(item, 'values') for item in tree.get_children()]
    
    for record in data:
        if record not in existing_data:  # Check if the record is already present
            tree.insert("", "end", values=record)  # Insert only if not present

#display data in each tables of students by course from database
def fetch_students_by_course(course_name):
    connection = create_connection()  # Create the database connection
    if connection is None:
        print("Failed to connect to the database.")
        return []

    cursor = connection.cursor()
    query = "SELECT id, school_id, full_name, course, year_level FROM student WHERE course = %s"  # Query to fetch students by course
    cursor.execute(query, (course_name,))  # Execute the query with the course name

    students = cursor.fetchall()  # Fetch all results
    cursor.close()
    connection.close()
    return students  # Return the list of students

def fetch_members_data(member_item_name):
    connection = create_connection()  # Create the database connection
    if connection is None:
        print("Failed to connect to the database.")
        return []

    cursor = connection.cursor()
    query = "SELECT id, school_id, full_name, affiliation, role, office FROM member WHERE office = %s"  # Query to fetch students by course
    cursor.execute(query, (member_item_name,))  # Execute the query with the course name

    member = cursor.fetchall()  # Fetch all results
    cursor.close()
    connection.close()
    return member  # Return the list of students


# Update table based on selection
def update_table(choice):
    # Clear current table data
    for item in table.get_children():
        table.delete(item)
    
    # Hide the tab views initially
    tab_view.pack_forget()
    tab_member.pack_forget()
    table.pack(fill="both", expand=True, pady=20, padx=20)

    # Configure the appropriate columns for the selected table , pady=20
    if choice == "Members":
        table.pack_forget()
        tab_member.pack(fill="both", expand=True, pady=(0,20))  # Show the tab view for students

        title_label.configure(text="Members table")
        close_admin_frame()
  
        #Unhide this wedgit
        cancel_search.pack(side='right',pady=20, padx=(5,20))
        search_button.pack(side='right',pady=20, padx=(5,0))
        search_bar.pack(side='right',pady=20, padx=(20,0))
           
            
        # Clear previous data in each student tab
        for member_name in member_list:
            member_tables[member_name].delete(*member_tables[member_name].get_children())

            # Fetch students from the database for each course and insert into the relevant table
        for member_item_name in member_list:
            member_data = fetch_members_data(member_item_name)  # Fetch data for each course
                
            if member_data:
                for member in member_data:
                     # Insert each student record into the corresponding Treeview
                    member_tables[member_item_name].insert("", "end", values=member)
            else:
                messagebox.showinfo('Show info',f"No students found for the course: {member_item_name}")

    elif choice == "Queue":
        tab_member.pack_forget()

        title_label.configure(text="Queue table")
        close_admin_frame()

        #Unhide this wedgit
        cancel_search.pack(side='right',pady=20, padx=(5,20))
        search_button.pack(side='right',pady=20, padx=(5,0))
        search_bar.pack(side='right',pady=20, padx=(20,0))

        def fetch_queue_data():
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT  queue_number, created_at, school_id, full_name, transaction, affiliation, phone, purpose_of_visit, compilation_time, voided FROM queue_admin")
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
    

        # Remove all existing rows from the TreeView table
        def clear_table(table):
            # Remove all existing rows from the TreeView table
            for row in table.get_children():
                table.delete(row)
        #Queue table

        table['columns'] = ('Queue number',
                                'Created at',
                                'School ID',
                                'Full name', 
                                'Transaction', 
                                'Affiliation',
                                'Phone',
                                'Purpose of visit',
                                'Compilation time', 
                                'Voided')  
        table.column("#0", width=0, stretch="no")  # Hide the first column
        table.column("Queue number", anchor="center", width=110, stretch="no")
        table.column("Created at", anchor="center", stretch="no")
        table.column("School ID", anchor="center", width=100, stretch="no")
        table.column("Full name", anchor="center", stretch="no")
        table.column("Transaction", anchor="center", stretch="no")
        table.column("Affiliation", anchor="center", width=100, stretch="no")
        table.column("Phone", anchor="center", width=100, stretch="no")
        table.column("Purpose of visit", anchor="center", stretch="no")
        table.column("Compilation time", anchor="center", stretch="no")
        table.column("Voided", anchor="center", width=100, stretch="no")


        table.heading("#0", text="")
        table.heading("Queue number", text="Queue Number") 
        table.heading("Created at", text="Created at") # Use correct name for heading too
        table.heading("School ID", text="School ID")
        table.heading("Full name", text="Full name")
        table.heading("Transaction", text="Transaction")
        table.heading("Affiliation", text="Affiliation")
        table.heading("Phone", text="Phone")
        table.heading("Purpose of visit", text="Purpose of visit")
        table.heading("Compilation time", text="Compilation Time")
        table.heading("Voided", text="Voided")

        # Fetch and display data
        data = fetch_queue_data()
        for row in data:
            table.insert("", "end", values=row)

        item_values1 = None

        #get value wehn selected operator table
        def on_item_selected_password(event):
            global item_values1
            selected_item = table.selection()  # Get the selected items (returns a tuple)

            if selected_item:  # Check if any item is selected
                item_values1 = table.item(selected_item[0], 'values')  # Get the values of the selected item
                print(f"Selected values: {item_values1}")  # Do something with the values
            else:
                print("No item selected")  # Handle the case where no item is selected

        table.bind("<<TreeviewSelect>>", on_item_selected_password)

    elif choice == "Operators":
        # tab_member.pack_forget()
        define_password_columns()
        title_label.configure(text="Oprators table")
        close_admin_frame()

        global item_values
        item_values = None

        #Unhide this wedgit
        cancel_search.pack(side='right',pady=20, padx=(5,20))
        search_button.pack(side='right',pady=20, padx=(5,0))
        search_bar.pack(side='right',pady=20, padx=(20,0))
            
    elif choice == "Students":
            table.pack_forget()
            tab_view.pack(fill="both", expand=True, pady=(0,20))  # Show the tab view for students

            title_label.configure(text="Students table")
            close_admin_frame()

            #Unhide this wedgit
            cancel_search.pack(side='right',pady=20, padx=(5,20))
            search_button.pack(side='right',pady=20, padx=(5,0))
            search_bar.pack(side='right',pady=20, padx=(20,0))
                
            # Clear previous data in each student tab
            for tab_name in tab_list:
                tables[tab_name].delete(*tables[tab_name].get_children())

            # Fetch students from the database for each course and insert into the relevant table
            for course_name in tab_list:
                students_data = fetch_students_by_course(course_name)  # Fetch data for each course
                if students_data:
                    for student in students_data:
                        # Insert each student record into the corresponding Treeview
                        tables[course_name].insert("", "end", values=student)
                else:
                    messagebox.showinfo('Show info',f"No students found for the course: {course_name}")
  
#Cancel the search of operator
def update_operator_table(data=None):
    # Clear existing entries in the table
    table.delete(*table.get_children())
    
    # Fetch data if not provided (used for initial loading)
    if data is None:
        data = fetch_data()
    
    # Insert the fetched data into the table
    for row in data:
        table.insert("", "end", values=row)

cancel_clicked = False

#search functionality
def search():
    global cancel_clicked

    connection = create_connection()  # Create the database connection
    if connection is None:
        print("Failed to connect to the database.")
        return []

    cursor = connection.cursor()

    search_value = search_bar.get().strip()  # Get the input and remove leading/trailing spaces

    school_id_pattern = r'^\d{2}-\d{4}$'

    if not search_value:  # Check if the search bar is empty
        messagebox.showinfo("Input Error", "Please enter a value to search")  # Show a message if it's empty
        return  # Exit the function if there's no input
            
    elif not re.match(school_id_pattern, search_value):
        messagebox.showerror("Search field", "Error: Invalid school ID format. Please use 'XX-XXXX' format (e.g., '00-0000').")
        search_bar.delete(0, tk.END)
        return  # Exit the function if validation fails  
    
    search_value = "%" + search_value + "%"  # Add wildcards for the LIKE clause

    # A flag to check if any results were found
    results_found = False

    if dropdown_var.get() == "Students":

        # After a search, re-enable the cancel button
        cancel_search.configure(state="normal")
        cancel_clicked = False# Reset flag for future cancel operations
        # Use a parameterized query to prevent SQL injection
        query = "SELECT id, school_id, full_name, course, year_level FROM student WHERE school_id LIKE %s"
        
        cursor.execute(query, (search_value,))
        results = cursor.fetchall()  # Fetch all matching results

        # Clear existing entries in each table
        for tab_name, table_student in tables.items():
            table_student.delete(*table_student.get_children())  # Clear existing entries

            # # Check if results are empty
            # if not results:
            #     messagebox.showinfo("Search Result", "User does not exist")  # Show popup message
            # else:
            #     # Insert the new search results into the current tab's table_student
            #     for row in results:
            #         table_student.insert("", "end", values=row)
            if results:
                results_found = True  # Mark that we found results
                for row in results:
                    table_student.insert("", "end", values=row)

    elif dropdown_var.get() == "Members":
                # After a search, re-enable the cancel button
        cancel_search.configure(state="normal")
        cancel_clicked = False# Reset flag for future cancel operations

        # Use a parameterized query to prevent SQL injection
        query = "SELECT id, school_id, full_name, affiliation, role, office FROM member WHERE school_id LIKE %s"
        
        cursor.execute(query, (search_value,))
        results = cursor.fetchall()  # Fetch all matching results

        # Clear existing entries in each table
        for tab_name, table_member in member_tables.items():
            table_member.delete(*table_member.get_children())  # Clear existing entries

            # # Check if results are empty
            # if not results:
            #     messagebox.showinfo("Search Result", "User does not exist")  # Show popup message
            # else:
            #     # Insert the new search results into the current tab's table_member
            #     for row in results:
            #         table_member.insert("", "end", values=row)
            if results:
                results_found = True  # Mark that we found results
                for row in results:
                    table_member.insert("", "end", values=row)

    elif dropdown_var.get() == "Operators":

                # After a search, re-enable the cancel button
        cancel_search.configure(state="normal")
        cancel_clicked = False# Reset flag for future cancel operations
        
        connection = create_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return []

        cursor = connection.cursor()

        search_value = search_bar.get().strip()  # Get and strip the search input

        if not search_value:  # Check if the search input is empty
            messagebox.showinfo("Input Error", "Please enter a value to search")
            return

        search_value = "%" + search_value + "%"  # Add wildcards for LIKE clause

        # Execute the search query for Operators
        query = "SELECT id, school_id, full_name, operate_area, phone_number, username, password FROM operator WHERE school_id LIKE %s"
        
        cursor.execute(query, (search_value,))
        results = cursor.fetchall()  # Fetch all matching results

        # Clear and update the Operator table with search results
        update_operator_table(results)

        if results:
            results_found = True  # Mark that we found results

    elif dropdown_var.get() == "Queue":
                # After a search, re-enable the cancel button
        cancel_search.configure(state="normal")
        cancel_clicked = False# Reset flag for future cancel operations
        
        connection = create_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return []

        cursor = connection.cursor()

        search_value = search_bar.get().strip()  # Get and strip the search input

        if not search_value:  # Check if the search input is empty
            messagebox.showinfo("Input Error", "Please enter a value to search")
            return

        search_value = "%" + search_value + "%"  # Add wildcards for LIKE clause

        # Execute the search query for Operators
        query = "SELECT  queue_number, created_at, school_id, full_name, transaction, affiliation, phone, purpose_of_visit, compilation_time, voided FROM queue_admin WHERE school_id LIKE %s"
        cursor.execute(query, (search_value,))
        results = cursor.fetchall()  # Fetch all matching results

        # Clear and update the Operator table with search results
        update_operator_table(results)

        if results:
            results_found = True  # Mark that we found results

    # Show a message if no results were found across all categories
    if not results_found:
        messagebox.showinfo("Search Result", "User does not exist")  # Show a message box indicating no results found
                    
    search_bar.delete(0, tk.END)  # Clear the search bar after the search is performed

    cursor.close()  # Close the cursor
    connection.close()  # Close the connection 
  
# Function to define columns for the Operator table
def fetch_data():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, school_id, full_name, operate_area, phone_number, username, password, role FROM operator")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# Remove all existing rows from the TreeView table
def clear_table(table):
    # Remove all existing rows from the TreeView table
    for row in table.get_children():
        table.delete(row)

# Function to cancel search and reload all data
def cancel_search_action():
    global cancel_clicked  # Declare the variable as global at the beginning

    if dropdown_var.get() == "Operators":
        if cancel_clicked:
            return  # If already clicked once, do nothing
        
        data = fetch_data()  # Fetch all data from the operator table
        update_operator_table(data)  # Refresh the table with all data
        search_bar.delete(0, tk.END)  # Clear the search bar
        # Disable the cancel button after one use
        cancel_search.configure(state="disabled")
        cancel_clicked = True  # Set the flag to prevent further clicks

    elif dropdown_var.get() == "Students":
        if cancel_clicked:
            return  # If already clicked once, do nothing

        connection = create_connection()  # Create the database connection
        if connection is None:
            print("Failed to connect to the database.")
            return []

        # Clear all student tables to prevent duplication
        for course_name in tab_list:
            clear_table(tables[course_name])  # Clear the TreeView for the course
            students_data = fetch_students_by_course(course_name)  # Fetch data for each course
            if students_data:
                for student in students_data:
                    # Insert each student record into the corresponding TreeView
                    tables[course_name].insert("", "end", values=student)
            else:
                messagebox.showinfo('Show info', f"No students found for the course: {course_name}")

        cursor = connection.cursor()

        # Fetch all student data for each course (you can adjust the query as needed)
        query = "SELECT school_id, full_name, course, year_level FROM student WHERE course = %s"
        cursor.execute(query, (course_name,))
        students = cursor.fetchall()

        # Disable the cancel button after one use
        cancel_search.configure(state="disabled")
        cancel_clicked = True  # Set the flag to prevent further clicks

        cursor.close()
        connection.close()

        return students  # Return the list of students

    elif dropdown_var.get() == "Members":
        if cancel_clicked:
            return  # If already clicked once, do nothing
            
        connection = create_connection()  # Create the database connection
        if connection is None:
            print("Failed to connect to the database.")
            return []
        
        # Clear previous data in each member tab
        for member_name in member_list:
            clear_table(member_tables[member_name]) 
            # Fetch members from the database for each member and insert into the relevant table
            member_data = fetch_members_data(member_name)  # Fetch data for each member
            
            if member_data:
                for member in member_data:
                    # Insert each member record into the corresponding Treeview
                    member_tables[member_name].insert("", "end", values=member)
            else:
                messagebox.showinfo('Show info', f"No members found for: {member_name}")

        cursor = connection.cursor()
        query = "SELECT school_id, full_name, affiliation, role, office FROM member WHERE office = %s"  # Query to fetch members by office
        cursor.execute(query, (member_name,))  # Execute the query with the office name

        members = cursor.fetchall()  # Fetch all results

        # Disable the cancel button after one use
        cancel_search.configure(state="disabled")
        cancel_clicked = True  # Set the flag to prevent further clicks

        cursor.close()
        connection.close()
        return members  # Return the list of members
    
    elif dropdown_var.get() == "Queue":
        if cancel_clicked:
            return  # If already clicked once, do nothing
        
        data = fetch_queue_data()  # Fetch all data from the operator table
        update_operator_table(data)  # Refresh the table with all data
        search_bar.delete(0, tk.END)  # Clear the search bar
        # Disable the cancel button after one use
        cancel_search.configure(state="disabled")
        cancel_clicked = True  # Set the flag to prevent further clicks
 
# Operator table
def define_password_columns():
    table['columns'] = ('id','School ID', 'Full name', 'Operate area', 'Phone','Username', 'Password')
    table.column("#0", width=0, stretch="no")  # Hide the first column
    table.column("id", anchor="center", width=0, stretch="no")
    table.column("School ID", anchor="center", stretch="no")
    table.column("Full name", anchor="center", stretch="no")
    table.column("Operate area", anchor="center", stretch="no")
    table.column("Phone", anchor="center", stretch="no")
    table.column("Username", anchor="center", stretch="no")
    table.column("Password", anchor="center", stretch="no")

    table.heading("#0", text="", anchor="center")
    table.heading("id", text="id")
    table.heading("School ID", text="School ID")
    table.heading("Full name", text="Full name")
    table.heading("Operate area", text="Operate area")
    table.heading("Phone", text="Phone")
    table.heading("Username", text="Username")
    table.heading("Password", text="Password")

    # Fetch and display data
    data = fetch_data()
    for row in data:
        table.insert("", "end", values=row)

    item_values = None

    #get value wehn selected operator table
    def on_item_selected_password(event):
        global item_values
        selected_item = table.selection()  # Get the selected items (returns a tuple)

        if selected_item:  # Check if any item is selected
            item_values = table.item(selected_item[0], 'values')  # Get the values of the selected item
            print(f"Selected values: {item_values}")  # Do something with the values
        else:
            print("No item selected")  # Handle the case where no item is selected

    table.bind("<<TreeviewSelect>>", on_item_selected_password)

#Action for close window to cancel seleted values for every tables
def close_window_add_student(add_window):
    """Function to handle window close and reset selected item values."""
    global selected_item_values
    selected_item_values = None  # Reset the selected item values
    add_window.destroy()  # Close the window

def close_window_add_member(add_window):
    """Function to handle window close and reset selected item values."""
    global select_member_value
    select_member_value = None
    add_window.destroy()  # Close the window

def close_window_add_operator(add_window):
    """Function to handle window close and reset selected item values."""
    global item_values
    item_values = None
    add_window.destroy()  # Close the window

#ACTION FROM DATABASE add records++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Placeholder functions for the buttons
def add_record():
    # Function to add a record to the database based on the current selected table
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()

    # Get the main window's geometry
    x = admin.winfo_x()
    y = admin.winfo_y()
    width = 320  # Desired width of the pop-up window
    height = 350  # Desired height of the pop-up window
    # Calculate the center position
    x_position = x + (admin.winfo_width() // 2) - (width // 2)
    y_position = y + (admin.winfo_height() // 2) - (height // 2)

    if dropdown_var.get() == "Students":
        add_window = tk.Toplevel(admin)
        add_window.geometry(f"{width}x{height}+{x_position}+{y_position}")
        add_window.title("Add Student")
        add_window.iconbitmap("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico")
        add_window.grab_set()  # Make the window modal

        add_window.resizable(False, False)

        add_window.protocol("WM_DELETE_WINDOW", lambda: close_window_add_student(add_window))

        # Create a frame for the input fields
        input_frame = ctk.CTkFrame(add_window, fg_color='transparent')
        input_frame.pack(expand=True, fill='y', pady=(10, 0))  # Center the frame in the window

        add_label = ctk.CTkLabel(input_frame, text='Add Record', font=ctk.CTkFont(size=20, weight="bold"))
        add_label.pack(padx=10, pady=10)

        # Create input fields for adding a student
        password_id_label = ctk.CTkLabel(input_frame, text='School ID', width=250, anchor='w')
        password_id_label.pack()
        input_schoolid = ctk.CTkEntry(input_frame, width=250, placeholder_text='School ID')
        input_schoolid.pack(padx=10)

        password_id_label = ctk.CTkLabel(input_frame, text='Full name', width=250, anchor='w')
        password_id_label.pack()
        input_fullname = ctk.CTkEntry(input_frame, width=250, placeholder_text='Full name')
        input_fullname.pack(padx=10)

        dropdown_course = ctk.StringVar(value="Select Course")
        dropdown_layout = ctk.CTkOptionMenu(input_frame, variable=dropdown_course, width=250,
                              values=[
                                      "BSCS", 
                                      'BS-CRIM', 
                                      "BSSW", 
                                      "BSEE",
                                      'BSMT',
                                      'BSM',
                                      'BEED',
                                      'BSED',
                                      'BSBA',
                                      'BSHM',
                                      'BSA',
                                      'BAPS'], 
                              fg_color="#fff",
                              text_color="#000",
                              dropdown_fg_color="#fff",
                              button_color="orange",
                              dropdown_hover_color="orange",
                              button_hover_color="#de9420")
        dropdown_layout.pack(padx=10, pady=10)

        dropdown_year = ctk.StringVar(value="Select Year level")
        dropdown_level = ctk.CTkOptionMenu(input_frame, variable=dropdown_year, width=250,
                              values=[
                                      "1st Year", 
                                      '2nd Year', 
                                      "3rd Year", 
                                      "4rth Year",
                                      '5th Year',
                                      '6th Year',
                                      '7th Year',
                                      '8th Year',
                                      '9th Year',
                                      '10th Year'], 
                              fg_color="#fff",
                              text_color="#000",
                              dropdown_fg_color="#fff",
                              button_color="orange",
                              dropdown_hover_color="orange",
                              button_hover_color="#de9420")
        dropdown_level.pack(padx=10, pady=10)

        # Button to add the student record
        add_button = ctk.CTkButton(input_frame, text="Add reacord",width=250, fg_color='#d68b26', command=lambda: insert_student_data(
            input_schoolid.get(),
            input_fullname.get(),
            dropdown_course.get(),
            dropdown_year.get(),
            connection,
            cursor,
            add_window  # Pass the add window to close it later
        ))
        add_button.pack(padx=10, pady=10)

    elif dropdown_var.get() == "Members":
        # Get the main window's geometry
        x = admin.winfo_x()
        y = admin.winfo_y()
        width = 320  # Desired width of the pop-up window
        height = 400  # Desired height of the pop-up window
        # Calculate the center position
        x_position = x + (admin.winfo_width() // 2) - (width // 2)
        y_position = y + (admin.winfo_height() // 2) - (height // 2)

        member_window = tk.Toplevel(admin)
        member_window.geometry(f"{width}x{height}+{x_position}+{y_position}")
        member_window.title("Add member")
        member_window.iconbitmap("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico")
        member_window.grab_set()  # Make the window modal

        member_window.resizable(False, False)

        member_window.protocol("WM_DELETE_WINDOW", lambda: close_window_add_member(member_window))

        # Create a frame for the input fields
        member_frame = ctk.CTkFrame(member_window, width=250, fg_color='transparent')
        member_frame.pack(expand=True, fill='x')  # Center the frame in the window

        # Create input fields for adding a member
        member_heading = ctk.CTkLabel(member_frame, text='Add member record', font=ctk.CTkFont(size=20, weight="bold"))
        member_heading.pack(padx=10)

        password_id_label = ctk.CTkLabel(member_frame, text='School ID', width=250, anchor='w')
        password_id_label.pack()
        member_id = ctk.CTkEntry(member_frame, width=250, placeholder_text='School ID')
        member_id.pack(padx=10)  # Centering

        password_id_label = ctk.CTkLabel(member_frame, text='Full name', width=250, anchor='w')
        password_id_label.pack()
        member_name = ctk.CTkEntry(member_frame, width=250, placeholder_text='Full name')
        member_name.pack(padx=10)  # Centering

        password_id_label = ctk.CTkLabel(member_frame, text='Affiliation', width=250, anchor='w')
        password_id_label.pack()
        member_aff = ctk.CTkEntry(member_frame, width=250, placeholder_text='Affiliation')
        member_aff.pack(padx=10)  # Centering

        password_id_label = ctk.CTkLabel(member_frame, text='Role', width=250, anchor='w')
        password_id_label.pack()
        member_role = ctk.CTkEntry(member_frame, width=250, placeholder_text='Role')
        member_role.pack(padx=10)  # Centering

        dropdown_member = ctk.StringVar(value="Select office")
        dropdown_member_layout = ctk.CTkOptionMenu(member_frame, variable=dropdown_member, width=250,
                              values=[
                                      'Select office',
                                      "School staff", 
                                      'School faculty'
                                     ], 
                              fg_color="#fff",
                              text_color="#000",
                              dropdown_fg_color="#fff",
                              button_color="orange",
                              dropdown_hover_color="orange",
                              button_hover_color="#de9420")
        dropdown_member_layout.pack(padx=10, pady=10)
        # Button to add the queue record
        add_member = ctk.CTkButton(member_frame, text="Add record",width=250,
                                   fg_color='#d68b26',
                                   command=lambda: insert_member_data(
                                        member_id.get(),
                                        member_name.get(),
                                        member_aff.get(),
                                        member_role.get(),
                                        dropdown_member.get(),
                                        connection,
                                        cursor,
                                        member_window  # Pass the add window to close it later
                                    ))  # Centering
        add_member.pack(padx=10, pady=10)

    elif dropdown_var.get() == "Operators":
        x = admin.winfo_x()
        y = admin.winfo_y()
        width = 320  # Desired width of the pop-up window
        height = 480  # Desired height of the pop-up window

        # Calculate the center position for both x and y
        x_position = x + (admin.winfo_width() // 2) - (width // 2)
        y_position = y + (admin.winfo_height() // 2) - (height // 2)

        password_window = tk.Toplevel(admin)
        password_window.geometry(f"{width}x{height}+{x_position}+{y_position}")
        password_window.title("Add oprators")
        password_window.iconbitmap("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico")
        password_window.grab_set()  # Make the window modal


        password_window.resizable(False, False)

        password_window.protocol("WM_DELETE_WINDOW", lambda: close_window_add_operator(password_window))

        # Create a frame for the input fields
        password_frame = ctk.CTkFrame(password_window, width=250, fg_color='transparent')
        password_frame.pack(expand=True, fill='both')  # Center the frame in the window

        # Create input fields for adding a member
        password_heading = ctk.CTkLabel(password_frame, text='Add operators record', font=ctk.CTkFont(size=20, weight="bold"))
        password_heading.pack(padx=10, pady=20)
        
        password_id_label = ctk.CTkLabel(password_frame, text='School ID', width=250, anchor='w')
        password_id_label.pack()
        password_id = ctk.CTkEntry(password_frame, width=250, placeholder_text='School ID')
        password_id.pack(padx=10)  # Centering

        password_name_label = ctk.CTkLabel(password_frame, text='Full name', width=250, anchor='w')
        password_name_label.pack()
        password_name = ctk.CTkEntry(password_frame, width=250, placeholder_text='Full name')
        password_name.pack(padx=10)  # Centering
        
        # pasword_operate_label = ctk.CTkLabel(password_frame, text='Opearate area', width=250, anchor='w')
        # pasword_operate_label.pack()        
        # pasword_operate = ctk.CTkEntry(password_frame, width=250, placeholder_text='Operate area')
        # pasword_operate.pack(padx=10)  # Centering

        dropdown_op = ctk.StringVar(value="Select area")
        dropdown_op_layout = ctk.CTkOptionMenu(password_frame, variable=dropdown_op, width=250,
                              values=[
                                      'Cashier service',
                                      'Scholarship coordinator', 
                                      'Promisorry note coordinator'
                                     ], 
                              fg_color="#fff",
                              text_color="#000",
                              dropdown_fg_color="#fff",
                              button_color="orange",
                              dropdown_hover_color="orange",
                              button_hover_color="#de9420")
        dropdown_op_layout.pack(padx=10, pady=10)

        password_num_label = ctk.CTkLabel(password_frame, text='Phone', width=250, anchor='w')
        password_num_label.pack()  
        password_num = ctk.CTkEntry(password_frame, width=250, placeholder_text='Phone')
        password_num.pack(padx=10)  # Centering

        password_username = ctk.CTkLabel(password_frame, text='Username', width=250, anchor='w')
        password_username.pack() 
        password_username = ctk.CTkEntry(password_frame, width=250, placeholder_text='Username')
        password_username.pack(padx=10)  # Centering

        password_password = ctk.CTkLabel(password_frame, text='Password', width=250, anchor='w')
        password_password.pack() 
        password_password = ctk.CTkEntry(password_frame, width=250, placeholder_text='Password')
        password_password.pack(padx=10)  # Centering

        #Button to add the queue record
        add_password = ctk.CTkButton(password_frame, text="Add operators",width=250, 
                                     fg_color='#d68b26',
                                   command=lambda: insert_password_data(
                                        password_id.get(),
                                        password_name.get(),
                                        dropdown_op.get(),
                                        password_num.get(),
                                        password_username.get(),
                                        password_password.get(),
                                        connection,
                                        cursor,
                                        password_window  # Pass the add window to close it later
                                    ))  # Centering
        add_password.pack(padx=10, pady=(20,0))
    else:
         messagebox.showwarning("Warning", "Only Students, Members and Operators table can activate the button records.")

        
#Database action query for add students
def insert_student_data(school_id, fullname, course, year, connection, cursor, add_window):
    try:
        school_id_pattern = r'^\d{2}-\d{4}$'
              # Input validation
        if not school_id or not fullname or not course or not year:
            messagebox.showerror("Add Record", "All fields are required.")
            return      
        elif course == 'Select Course' or year == 'Select Year & level':
           messagebox.showerror("Add Record", "All fields are required.")
           return
              
        # Validate school_id format
        elif not re.match(school_id_pattern, school_id):
            messagebox.showerror("Add Record", "Error: Invalid school ID format. Please use 'XX-XXXX' format (e.g., '00-0000').")
            return  # Exit the function if validation fails  
        
        check_id = "SELECT school_id FROM student WHERE school_id = %s"
        cursor.execute(check_id, (school_id,))
        result_id = cursor.fetchone()

        if result_id:        
            messagebox.showinfo("Warning",f"The ID {school_id} already exist.")
            return
          

        query = "INSERT INTO student (school_id, full_name, course, year_level) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (school_id, fullname, course, year))
        connection.commit()  # Commit the changes to the database
        update_table("Students")
        add_window.destroy()  # Close the add window
        messagebox.showinfo('Success',"Record added successfully")

        # Reset the selected item values
        global selected_item_values
        selected_item_values = None

        cursor.close()
        connection.close()
    except Error as err:  # Catch MySQL specific errors
        print(f"Error: {err}")  # Handle MySQL errors as warning

def insert_member_data(school_id, fullname, affiliation, role, office, connection, cursor, member_window):
    try:
        school_id_pattern = r'^\d{2}-\d{4}$'
              # Input validation
        if not school_id or not fullname or not affiliation or not role or not office:
            messagebox.showerror("Add Record", "All fields are required.")
            return      
        elif office == 'Select office':
           messagebox.showerror("Add member Record", "All fields are required.")
           return
              
        # Validate school_id format
        elif not re.match(school_id_pattern, school_id):
            messagebox.showerror("Add member Record", "Error: Invalid school ID format. Please use 'XX-XXXX' format (e.g., '00-0000').")
            return  # Exit the function if validation fails  
        
        check_id = "SELECT school_id FROM member WHERE school_id = %s"
        cursor.execute(check_id, (school_id,))
        result_id = cursor.fetchone()

        if result_id:        
            messagebox.showinfo("Warning",f"The ID {school_id} already exist.")
            return
          

        query = "INSERT INTO member (school_id, full_name, affiliation, role, office) VALUES (%s, %s, %s, %s,%s)"
        cursor.execute(query, (school_id, fullname, affiliation, role, office))
        connection.commit()  # Commit the changes to the database
        update_table("Members")
        member_window.destroy()  # Close the add window
        messagebox.showinfo('Success',"Record member added successfully")

        # Reset the selected item values
        global select_member_value
        select_member_value = None

        cursor.close()
        connection.close()
    except Error as err:  # Catch MySQL specific errors
        print(f"Error: {err}")  # Handle MySQL errors as warning def insert_password_data():

def insert_password_data(school_id, fullname, operate_area, phone_num, username, password, connection, cursor, password_window):
    try:
        school_id_pattern = r'^\d{2}-\d{4}$'
        phone_pattern = r'^\+?\d{10,15}$' 
        
        # Input validation
        if not school_id or not fullname or not operate_area or not phone_num or not username:
            messagebox.showerror("Add operator record", "All fields are required.")
            return  
        
        # Validate school_id format
        if not re.match(school_id_pattern, school_id):
            messagebox.showerror("Add operator record", "Error: Invalid school ID format. Please use 'XX-XXXX' format (e.g., '00-0000').")
            return
        
        # Validate phone number format
        if not re.match(phone_pattern, phone_num):
            messagebox.showerror("Add operator record", "Error: Invalid phone number format. Please enter a valid number with 10-15 digits.")
            return
        
        # Validate username and password length (minimum 4 characters)
        if len(username) < 4:
            messagebox.showerror("Add operator record", "Error: Username must be at least 4 characters long.")
            return
        
        if len(password) < 4:
            messagebox.showerror("Add operator record", "Error: Password must be at least 4 characters long.")
            return

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
              
        # Check if the username already exists in the database
        cursor.execute("SELECT username FROM operator WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            messagebox.showerror("Add operator record", "Error: Username already exists. Please choose a different username.")
            return
        
        check_id = "SELECT school_id FROM operator WHERE school_id = %s"
        cursor.execute(check_id, (school_id,))
        result_id = cursor.fetchone()

        if result_id:        
            messagebox.showinfo("Warning",f"The ID {school_id} already exist.")
            return

        # Insert the new operator data if validations pass
        query = """
        INSERT INTO operator (school_id, full_name, operate_area, phone_number, username, password, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (school_id, fullname, operate_area, phone_num, username, hashed_password, 'operator'))
        connection.commit()  # Commit the changes to the database
        update_table("Operators")  # Assuming update_table refreshes the data
        password_window.destroy()  # Close the password window
        
        messagebox.showinfo('Success', "Record operator added successfully")
        cursor.close()
        connection.close()
        
    except Error as err:  # Catch MySQL specific errors
        print(f"Error: {err}")  # Handle MySQL errors as warning
    
           
#update record
def update_record():
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()

    x = admin.winfo_x()
    y = admin.winfo_y()
    width = 320  # Desired width of the pop-up window
    height = 380  # Desired height of the pop-up window
    # Calculate the center position
    x_position = x + (admin.winfo_width() // 2) - (width // 2)
    y_position = y + (admin.winfo_height() // 2) - (height // 2)

    if dropdown_var.get() == "Students":
        global selected_item_values  # Access the selected item values
        if selected_item_values is None:
            messagebox.showwarning("Warning","No item selected for update.")
            return  # Exit if no item is selected

        x = admin.winfo_x()
        y = admin.winfo_y()
        width = 320  # Desired width of the pop-up window
        height = 350  # Desired height of the pop-up window
        # Calculate the center position
        x_position = x + (admin.winfo_width() // 2) - (width // 2)
        y_position = y + (admin.winfo_height() // 2) - (height // 2)

        # Create a modal update window
        update_window = tk.Toplevel(admin)
        update_window.geometry(f"{width}x{height}+{x_position}+{y_position}")
        update_window.title("Update Student")
        update_window.iconbitmap("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico")
        update_window.grab_set()  # Make the window modal
        update_window.resizable(False, False)

        update_window.protocol("WM_DELETE_WINDOW", lambda: close_window_add_student(update_window))

        # Create a frame for the input fields
        update_member_frame = ctk.CTkFrame(update_window, fg_color='transparent')
        update_member_frame.pack(expand=True, fill='y', pady=(10, 0))  # Center the frame in the window

        update_label = ctk.CTkLabel(update_member_frame, text='Update record', font=ctk.CTkFont(size=20, weight="bold"))
        update_label.pack(padx=10, pady=10)

        id = selected_item_values[0]

        # Create input fields for updating a student and set their initial values
        schoolid_text = ctk.CTkLabel(update_member_frame, text='School ID', width=250, anchor='w')
        schoolid_text.pack()
        update_schoolid = ctk.CTkEntry(update_member_frame, width=250, placeholder_text='School ID')
        update_schoolid.pack(padx=10)
        update_schoolid.insert(0, selected_item_values[1])  # Set the School ID

        fullname_text = ctk.CTkLabel(update_member_frame, text='Full name', width=250, anchor='w')
        fullname_text.pack()
        update_fullname = ctk.CTkEntry(update_member_frame, width=250, placeholder_text='Full name')
        update_fullname.pack(padx=10)
        update_fullname.insert(0, selected_item_values[2])  # Set the Full name


        update_course = ctk.StringVar(value="Select Course")
        couser_layout = ctk.CTkOptionMenu(update_member_frame, 
                                        variable=update_course, 
                                        width=250,
                                        values=[
                                            "BSCS", 
                                            'BS-CRIM', 
                                            "BSSW", 
                                            "BSEE",
                                            'BSMT',
                                            'BSM',
                                            'BEED',
                                            'BSED',
                                            'BSBA',
                                            'BSHM',
                                            'BSA',
                                            'BAPS'], 
                                        fg_color="#fff",
                                        text_color="#000",
                                        dropdown_fg_color="#fff",
                                        button_color="orange",
                                        dropdown_hover_color="orange",
                                        button_hover_color="#de9420")
        couser_layout.pack(padx=10, pady=10)
        update_course.set(selected_item_values[3])


        update_year = ctk.StringVar(value="Select Year level")
        year_layout = ctk.CTkOptionMenu(update_member_frame, variable=update_year, width=250,
                              values=[
                                      "1st Year", 
                                      '2nd Year', 
                                      "3rd Year", 
                                      "4rth Year",
                                      '5th Year',
                                      '6th Year',
                                      '7th Year',
                                      '8th Year',
                                      '9th Year',
                                      '10th Year'], 
                              fg_color="#fff",
                              text_color="#000",
                              dropdown_fg_color="#fff",
                              button_color="orange",
                              dropdown_hover_color="orange",
                              button_hover_color="#de9420")
        year_layout.pack(padx=10, pady=10)
        update_year.set(selected_item_values[4])

        # Update button with functionality
        update_button = ctk.CTkButton(
            update_member_frame,
            width=250,
            text='Update record',
            fg_color='#d68b26',
            command=lambda: save_changes_to_database(
                update_schoolid.get(),
                update_fullname.get(),
                update_course.get(),
                update_year.get(),
                id,
                connection,
                cursor,
                update_window  # Pass the update window to close it later
            )
        )
        update_button.pack(padx=10, pady=20)

    elif dropdown_var.get() == "Members":
        x = admin.winfo_x()
        y = admin.winfo_y()
        width = 320  # Desired width of the pop-up window
        height = 400  # Desired height of the pop-up window
        # Calculate the center position
        x_position = x + (admin.winfo_width() // 2) - (width // 2)
        y_position = y + (admin.winfo_height() // 2) - (height // 2)

        global select_member_value  # Access the selected item values
        if select_member_value is None:
            messagebox.showwarning("Warning","No item selected for update.")
            return  # Exit if no item is selected
        # Create a modal update window
        update_member = tk.Toplevel(admin)
        update_member.geometry(f"{width}x{height}+{x_position}+{y_position}")
        update_member.title("Update member")
        update_member.iconbitmap("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico")
        update_member.grab_set()  # Make the window modal
        update_member.resizable(False, False)

        update_member.protocol("WM_DELETE_WINDOW", lambda: close_window_add_member(update_member))

        # Create a frame for the input fields
        update_member_frame = ctk.CTkFrame(update_member, fg_color='transparent')
        update_member_frame.pack(expand=True, fill='y', pady=(10, 0))  # Center the frame in the window

        update_label = ctk.CTkLabel(update_member_frame, text='Update record', font=ctk.CTkFont(size=20, weight="bold"))
        update_label.pack()

        memberid = select_member_value[0]

        # Create input fields for updating a student and set their initial values
        schoolid_text = ctk.CTkLabel(update_member_frame, text='School ID', width=250, anchor='w')
        schoolid_text.pack()
        update_schoolid = ctk.CTkEntry(update_member_frame, width=250, placeholder_text='School ID')
        update_schoolid.pack(padx=10)
        update_schoolid.insert(0, select_member_value[1])  # Set the School ID

        fullname_text = ctk.CTkLabel(update_member_frame, text='Full name', width=250, anchor='w')
        fullname_text.pack()
        update_fullname = ctk.CTkEntry(update_member_frame, width=250, placeholder_text='Full name')
        update_fullname.pack(padx=10)
        update_fullname.insert(0, select_member_value[2])  # Set the Full name

        course_text = ctk.CTkLabel(update_member_frame, text='Affiliation', width=250, anchor='w')
        course_text.pack()
        update_course = ctk.CTkEntry(update_member_frame, width=250, placeholder_text='Affiliation')
        update_course.pack(padx=10)
        update_course.insert(0, select_member_value[3])  # Set the Course

        year_text = ctk.CTkLabel(update_member_frame, text='Role', width=250, anchor='w')
        year_text.pack()
        update_year = ctk.CTkEntry(update_member_frame, width=250, placeholder_text='Role')
        update_year.pack(padx=10)
        update_year.insert(0, select_member_value[4])  # Set the Year & Level


        office_member = ctk.StringVar(value="Select office")
        office_member_layout = ctk.CTkOptionMenu(update_member_frame, variable=office_member, width=250,
                              values=[
                                      "School staff", 
                                      'School faculty'
                                     ], 
                              fg_color="#fff",
                              text_color="#000",
                              dropdown_fg_color="#fff",
                              button_color="orange",
                              dropdown_hover_color="orange",
                              button_hover_color="#de9420")
        office_member_layout.pack(padx=10, pady=10)
        office_member.set(select_member_value[5])

        # Update button with functionality
        update_button = ctk.CTkButton(
            update_member_frame,
            width=250,
            fg_color='#d68b26',
            text='Update record',
            command=lambda: save_changes_member(
                update_schoolid.get(),
                update_fullname.get(),
                update_course.get(),
                update_year.get(),
                office_member.get(),
                memberid,
                connection,
                cursor,
                update_member  # Pass the update window to close it later
            )
        )
        update_button.pack(padx=10, pady=20)

    elif dropdown_var.get() == "Operators":
        global item_values  # Access the selected item values
        if item_values is None:
            messagebox.showwarning("Warning","No item selected for update.")
            return  # Exit if no item is selected
        
        x = admin.winfo_x()
        y = admin.winfo_y()
        width = 320  # Desired width of the pop-up window
        height = 480  # Desired height of the pop-up window

        # Calculate the center position for both x and y
        x_position = x + (admin.winfo_width() // 2) - (width // 2)
        y_position = y + (admin.winfo_height() // 2) - (height // 2)

        password_update = tk.Toplevel(admin)
        password_update.geometry(f"{width}x{height}+{x_position}+{y_position}")
        password_update.title("Update oprators")
        password_update.iconbitmap("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico")
        password_update.grab_set()  # Make the window modal

        password_update.resizable(False, False)

        password_update.protocol("WM_DELETE_WINDOW", lambda: close_window_add_operator(password_update))

        # Create a frame for the input fields
        password_operator = ctk.CTkFrame(password_update, width=250, fg_color='transparent')
        password_operator.pack(expand=True, fill='both')  # Center the frame in the window

        # Create input fields for adding a member
        password_heading = ctk.CTkLabel(password_operator, text='Update operators record',font=ctk.CTkFont(size=20, weight="bold"))
        password_heading.pack(padx=10, pady=20)

        id = item_values[0]

        password_password = ctk.CTkLabel(password_operator, text='School ID', width=250, anchor='w')
        password_password.pack() 
        password_id = ctk.CTkEntry(password_operator, width=250, placeholder_text='School ID')
        password_id.pack(padx=10)  # Centering
        password_id.insert(0, item_values[1])

        password_password = ctk.CTkLabel(password_operator, text='Full name', width=250, anchor='w')
        password_password.pack() 
        password_name = ctk.CTkEntry(password_operator, width=250, placeholder_text='Full name')
        password_name.pack(padx=10)  # Centering
        password_name.insert(0, item_values[2])

        password_password = ctk.CTkLabel(password_operator, text='Operate area', width=250, anchor='w')
        password_password.pack() 
        # pasword_operate = ctk.CTkEntry(password_operator, width=250, placeholder_text='Operate area')
        # pasword_operate.pack(padx=10)  # Centering
        # pasword_operate.insert(0, item_values[3])

        dropdown_op = ctk.StringVar(value="Select area")
        dropdown_op_layout = ctk.CTkOptionMenu(password_operator, variable=dropdown_op, width=250,
                              values=[
                                      'Cashier service',
                                      'Scholarship coordinator', 
                                      'Promisorry note coordinator'
                                     ], 
                              fg_color="#fff",
                              text_color="#000",
                              dropdown_fg_color="#fff",
                              button_color="orange",
                              dropdown_hover_color="orange",
                              button_hover_color="#de9420")
        dropdown_op_layout.pack(padx=10)
        dropdown_op.set(item_values[3])

        password_password = ctk.CTkLabel(password_operator, text='Phone', width=250, anchor='w')
        password_password.pack() 
        password_num = ctk.CTkEntry(password_operator, width=250, placeholder_text='Phone')
        password_num.pack(padx=10)  # Centering
        password_num.insert(0, item_values[4])
        
        password_password = ctk.CTkLabel(password_operator, text='Username', width=250, anchor='w')
        password_password.pack() 
        password_username = ctk.CTkEntry(password_operator, width=250, placeholder_text='Username')
        password_username.pack(padx=10)  # Centering
        password_username.insert(0, item_values[5])

        password_password = ctk.CTkLabel(password_operator, text='Password', width=250, anchor='w')
        password_password.pack() 
        password_password = ctk.CTkEntry(password_operator, width=250, placeholder_text='Password')
        password_password.pack(padx=10)  # Centering
        password_password.insert(0, item_values[6])

        # Button to add the queue record
        update_opearator = ctk.CTkButton(password_operator, text="Update operators",width=250,
                                                        fg_color='#d68b26',
                                                        command=lambda: update_password_data(
                                                            password_id.get(),
                                                            password_name.get(),
                                                            dropdown_op.get(),
                                                            password_num.get(),
                                                            password_username.get(),
                                                            password_password.get(),
                                                            id,
                                                            connection,
                                                            cursor,
                                                            password_update  # Pass the add window to close it later
                                                        ))  # Centering
        update_opearator.pack(padx=10, pady=(20,0))
    else:
        messagebox.showwarning("Warning", "Only Students, Members and Operators table can activate the button records.")


#Action of update in databse
def save_changes_to_database(school_id, fullname, course, year,id, conn, cursor, update):
    try:

        year_format = [
                '1st Year', 
                '2nd Year', 
                '3rd Year',
                '4rth Year', 
                '5th Year', 
                '6th Year', 
                '7th Year', 
                '8th Year', 
                '9th Year',
                '10th Year'
                ]
        
         # Input validation
        if not school_id or not fullname or not course or not year:
            messagebox.showerror("Update record", "All fields are required.")
            return      
        elif course not in tab_list:
           messagebox.showerror("Update record", "Please input valid Course")
           return
        elif year not in year_format:
           messagebox.showerror("Update record", "Please input valid Year level")
           return
        
        school_id_pattern = r'^\d{2}-\d{4}$'
        # Validate school_id format
        if not re.match(school_id_pattern, school_id):
            messagebox.showerror("Add Record", "Error: Invalid school ID format. Please use 'XX-XXXX' format (e.g., '00-0000').")
            return  # Exit the function if validation fails  
                                    

        query = "UPDATE student SET school_id = %s, full_name = %s, course =%s, year_level =%s WHERE id = %s"
        cursor.execute(query, (school_id, fullname, course, year, id))
        conn.commit()  # Commit the changes to the database       
        update_table("Students")
        update.destroy()  # Close the add window
        messagebox.showinfo('Success',"Record update successfully")

        # Reset the table selection
        if tab_view:
            selected_table = tables[course]  # Get the table for the updated course
            selected_table.selection_remove(selected_table.selection())  # Deselect any selected items

        # Reset the selected item values
        global selected_item_values
        selected_item_values = None

        cursor.close()
        conn.close()
    except Error as err:  # Catch MySQL specific errors
        print(f"Error: {err}")  # Handle MySQL errors as warnings

def save_changes_member(school_id, fullname, affiliation, role, office,memberid, conn, cursor, update):
    try:

        office_format = [
                'School staff', 
                'School faculty'
                ]
         # Input validation
        if not school_id or not fullname or not affiliation or not role or not office:
            messagebox.showerror("Update record member", "All fields are required.")
            return      
        
        elif office not in office_format:
           messagebox.showerror("Update record member", "Please input valid office")
           return   

        school_id_pattern = r'^\d{2}-\d{4}$'
        # Validate school_id format
        if not re.match(school_id_pattern, school_id):
            messagebox.showerror("Add Record", "Error: Invalid school ID format. Please use 'XX-XXXX' format (e.g., '00-0000').")
            return  # Exit the function if validation fails  
                                                              

        query = "UPDATE member SET school_id = %s, full_name = %s, affiliation =%s, role =%s, office =%s WHERE id = %s"
        cursor.execute(query, (school_id, fullname, affiliation, role, office, memberid))
        conn.commit()  # Commit the changes to the database       
        update_table("Members")
        update.destroy()  # Close the add window
        messagebox.showinfo('Success',"Record update successfully")


        # Reset the table selection
        if tab_member:
            selected_table = member_tables[office]  # Get the table for the updated course
            selected_table.selection_remove(selected_table.selection())  # Deselect any selected items

        # Reset the selected item values
        global select_member_value
        select_member_value = None


        cursor.close()
        conn.close()
    except Error as err:  # Catch MySQL specific errors
        print(f"Error: {err}")  # Handle MySQL errors as warnings update_password_data

def update_password_data(school_id, fullname, operate, phone, username, password,id, conn, cursor, update):
    try:

        phone_pattern = r'^\+?\d{10,15}$'

        if not school_id or not fullname or not operate or not phone or not username or not password:
            messagebox.showerror("Update record member", "All fields are required.")
            return      

        # Validate phone number format
        if not re.match(phone_pattern, phone):
            messagebox.showerror("Add operator record", "Error: Invalid phone number format. Please enter a valid number with 10-15 digits.")
            return
          
        # Validate username and password length (minimum 4 characters)
        if len(username) < 4:
            messagebox.showerror("Add operator record", "Error: Username must be at least 4 characters long.")
            return
        
        if len(password) < 4:
            messagebox.showerror("Add operator record", "Error: Password must be at least 4 characters long.")
            return  

        school_id_pattern = r'^\d{2}-\d{4}$'
        # Validate school_id format
        if not re.match(school_id_pattern, school_id):
            messagebox.showerror("Add Record", "Error: Invalid school ID format. Please use 'XX-XXXX' format (e.g., '00-0000').")
            return  # Exit the function if validation fails  
                                     
           
        # # Check if the username already exists in the database
        # cursor.execute("SELECT username FROM operator WHERE username = %s", (username,))
        # existing_user = cursor.fetchone()
        
        # if existing_user:
        #     messagebox.showerror("Add operator record", "Error: Username already exists. Please choose a different username.")
        #     return
        
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        query = "UPDATE operator SET school_id = %s, full_name = %s, operate_area =%s, phone_number =%s, username =%s, password =%s WHERE id = %s"
        cursor.execute(query, (school_id, fullname, operate, phone, username, hashed_password, id))
        conn.commit()  # Commit the changes to the database       
        update_table("Operators")
        update.destroy()  # Close the add window
        messagebox.showinfo('Success',"Record update successfully")


        # # Reset the table selection
        # if tab_member:
        #     selected_table = member_tables[office]  # Get the table for the updated course
        #     selected_table.selection_remove(selected_table.selection())  # Deselect any selected items

        # Reset the selected item values
        global item_values
        item_values = None


        cursor.close()
        conn.close()
    except Error as err:  # Catch MySQL specific errors
        print(f"Error: {err}")  # Handle MySQL errors as warnings update_password_data


#Remove record 
def remove_record():
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()

    if dropdown_var.get() == "Students":
        global selected_item_values  # Access the selected item values
        if selected_item_values is None:
           messagebox.showwarning("Warning","No item selected for remove.")
           return  # Exit if no item is selected

        global student_id
        student_id = selected_item_values[1]

        remove_data_from_database(student_id, connection, cursor)

    elif dropdown_var.get() == "Members":
        global select_member_value  # Access the selected item values
        if select_member_value is None:
           messagebox.showwarning("Warning","No item selected for remove.")
           return  # Exit if no item is selected
        
        global member_id
        member_id = select_member_value[1]
        remove_member_data(member_id, connection, cursor)

    elif dropdown_var.get() == "Operators":
        global item_values  # Access the selected item values
        if item_values is None:
           messagebox.showwarning("Warning","No item selected for remove.")
           return  # Exit if no item is selected
        
        global operator_id
        operator_id = item_values[1]
        remove_operator_data(operator_id, connection, cursor)

    else:
        messagebox.showwarning("Warning", "Only Students, Members and Operators table can activate the button records.")


#action query from database to remove records     
def remove_data_from_database(school_id, conn, cursor):
    remove_res = messagebox.askyesno("Confirm", f"Are you sure to remove this record {student_id}")
    if remove_res:
        try:
            # Prepare and execute the DELETE query
            query = "DELETE FROM `student` WHERE school_id = %s"
            cursor.execute(query, (school_id,))  # Use a tuple with only the school_id
            conn.commit()  # Commit the changes to the database

            print("Record removed successfully")
            update_table("Students")  # Update the displayed table (assuming this is defined elsewhere)
            
            global selected_item_values
            selected_item_values = None  # Clear the selected item after deletion

        except Error as err:  # Catch MySQL specific errors
            print(f"Error: {err}")  # Handle MySQL errors as warnings
        finally:
            cursor.close()  # Close the cursor
            conn.close()    # Close the connection
    else:
        print("Remove canceled.")

def remove_member_data(school_id, conn, cursor):
    remove_res = messagebox.askyesno("Confirm", f"Are you sure to remove this record {member_id}")
    if remove_res:
        try:
            # Prepare and execute the DELETE query
            query = "DELETE FROM `member` WHERE school_id = %s"
            cursor.execute(query, (school_id,))  # Use a tuple with only the school_id
            conn.commit()  # Commit the changes to the database

            print("Record removed successfully")
            update_table("Members")  # Update the displayed table (assuming this is defined elsewhere)     

            # Reset the selected item values
            global select_member_value
            select_member_value = None

        except Error as err:  # Catch MySQL specific errors
            print(f"Error: {err}")  # Handle MySQL errors as warnings
        finally:
            cursor.close()  # Close the cursor
            conn.close()    # Close the connection 
    else:
        print("Remove canceled.")

def remove_operator_data(school_id, conn, cursor):
    remove_res = messagebox.askyesno("Confirm", f"Are you sure to remove this record {operator_id}")
    if remove_res:
        try:
            # Prepare and execute the DELETE query
            query = "DELETE FROM `operator` WHERE school_id = %s"
            cursor.execute(query, (school_id,))  # Use a tuple with only the school_id
            conn.commit()  # Commit the changes to the database

            print("Record removed successfully")
            update_table("Operators")  # Update the displayed table (assuming this is defined elsewhere)     

            # Reset the selected item values
            global item_values
            item_values = None

        except Error as err:  # Catch MySQL specific errors
            print(f"Error: {err}")  # Handle MySQL errors as warnings
        finally:
            cursor.close()  # Close the cursor
            conn.close()    # Close the connection remove_operator_data
    else:
        print("Remove canceled.")

# admin settings
# Function to validate the current username and password
def validate_credentials(username, password):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return True
    else:
        return False
    
# Function to update username and password in the database
def update_credentials(old_username, old_password, new_username, new_password):
    if not validate_credentials(old_username, old_password):
        messagebox.showerror("Error", "Current username or password is incorrect.")
        return False

    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    update_query = "UPDATE admin SET username = %s, password = %s WHERE username = %s"
    try:
        cursor.execute(update_query, (new_username, new_password, old_username))
        connection.commit()
        messagebox.showinfo("Success", "Username and password updated successfully.")
        return True
    except Error as err:
        messagebox.showerror("Error", f"Failed to update: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

# Global variable to track if admin_frame is open
is_admin_frame_open = False
admin_frame = None  # Declare admin_frame globally

def settings_for_admin():
    global is_admin_frame_open, admin_frame  # Access the global variable
    # If the admin frame is already open, do nothing
    if is_admin_frame_open:
        return  # Exit the function if admin_frame is already open

    # Hide the previous table_frame
    table_frame.pack_forget()
    add_button.configure(state="disabled")
    update_button.configure(state="disabled")
    remove_button.configure(state="disabled")

    # Create and pack the admin frame
    admin_frame = ctk.CTkFrame(main_frame, fg_color='lightgray')
    admin_frame.pack(side="right", fill="both", expand=True)

    #navbar frame
    admin_navbar_frame = ctk.CTkFrame(admin_frame, width=800, height=60, fg_color='#d68b26')
    admin_navbar_frame.pack(side='top', fill='x')

    admin_navbar_label = ctk.CTkLabel(admin_navbar_frame,
                            text='Admin settings',
                            anchor='w', 
                            text_color='#fff',
                            font=ctk.CTkFont(size=15, weight="bold"))
    admin_navbar_label.pack(side='left',pady=20, padx=20)

    #Hero frame
    admin_hero_frame = ctk.CTkFrame(admin_frame, width=800, height=60, fg_color='#fff')
    admin_hero_frame.pack(expand=True, fill='both', pady=20, padx=20)


    # # Add a button to close the admin_frame
    # close_button = ctk.CTkButton(admin_hero_frame, text="Close", command=close_admin_frame)
    # close_button.pack(pady=10,padx=10, anchor='w')

    # Create and pack the label in the admin frame
    admin_label = ctk.CTkLabel(admin_hero_frame, text="Update admin username and password", font=ctk.CTkFont(size=20, weight="bold"))
    admin_label.pack(pady=10)

    form_frame = ctk.CTkFrame(admin_hero_frame, width=350, height=320)
    form_frame.pack(expand=True)

    #Current credintials
    form_label = ctk.CTkLabel(form_frame, text='Current usename')
    form_label.pack(pady=(30,0), padx=20, anchor='w')
    form_username = ctk.CTkEntry(form_frame, placeholder_text='Username', width=320)
    form_username.pack(padx=20)

    form_label = ctk.CTkLabel(form_frame, text='Current password')
    form_label.pack(pady=(10, 0), padx=20, anchor='w')
    form_pass = ctk.CTkEntry(form_frame, placeholder_text='Password', width=320)
    form_pass.pack(padx=20)

    #New credintials
    new_form_label = ctk.CTkLabel(form_frame, text='New username')
    new_form_label.pack(pady=(20,0), padx=20, anchor='w')
    new_form_username = ctk.CTkEntry(form_frame, placeholder_text='Username', width=320)
    new_form_username.pack(padx=20)

    new_form_label = ctk.CTkLabel(form_frame, text='New password')
    new_form_label.pack(pady=(10, 0), padx=20, anchor='w')
    new_form_password = ctk.CTkEntry(form_frame, placeholder_text='Password', width=320)
    new_form_password.pack(padx=20)
    
    # Function to clear all entry fields
    def clear_entries():
        form_username.delete(0, tk.END)
        form_pass.delete(0, tk.END)
        new_form_username.delete(0, tk.END)
        new_form_password.delete(0, tk.END)

    # Function to handle the update button click
    def on_update_button_click():
        old_username = form_username.get()
        old_password = form_pass.get()
        new_username = new_form_username.get()
        new_password = new_form_password.get()

        if not old_username or not old_password or not new_username or not new_password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if len(new_username) < 4:
            messagebox.showerror("Error", "Error: Username must be at least 4 characters long.")
            return
        
        if len(new_password) < 4:
            messagebox.showerror("Error", "Error: Password must be at least 4 characters long.")
            return  

        # Call the function to update credentials
        success = update_credentials(old_username, old_password, new_username, new_password)

        if success:
            clear_entries()  # Clear the input fields if update is successful


    form_button = ctk.CTkButton(form_frame, text='Save', fg_color='#d68b26', height=30, command=on_update_button_click)
    form_button.pack(pady=20, padx=20)

    # Set the flag to indicate that the admin frame is now open
    is_admin_frame_open = True

#to close admin frame
def close_admin_frame():
    global is_admin_frame_open, admin_frame

    # Use pack_forget to hide the admin_frame
    if admin_frame is not None:
        admin_frame.pack_forget()  # Hide the admin frame
    
    is_admin_frame_open = False  # Reset the flag to allow reopening
    table_frame.pack(side="right", fill="both", expand=True)

    add_button.configure(state="normal")
    update_button.configure(state="normal")
    remove_button.configure(state="normal")
   
#logout confirmation   
def confirm_logout():
    response = messagebox.askyesno("Log out", "Are you sure you want to log out?")
    if response:
        # Code to log out the user
        admin.destroy()
    else:
        print("Logout canceled.")


admin.mainloop()