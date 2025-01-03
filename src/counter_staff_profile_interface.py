import importlib
import time
import customtkinter as ctk
import tkinter as tk
from db import create_connection
from mysql.connector import Error
from PIL import Image
from tkinter import messagebox

def counter_staff_home(op_name, op_area, op_id):
    from operator_cashier_dashboard import cashier_window
    from operator_pnc_dashboard import pnc_window
    from operator_sc_dashboard import sc_window

    counter_staff = ctk.CTk()
    counter_staff.title("Counter Staff")
    counter_staff.iconbitmap("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico")

    # Set appearance mode and color theme (Light/Dark modes)
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")

    # Center the window on the screen
    window_width = 800
    window_height = 440
    screen_width = counter_staff.winfo_screenwidth()
    screen_height = counter_staff.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    counter_staff.geometry(f"{window_width}x{window_height}+{x}+{y}")

    counter_staff.columnconfigure(0, weight=1)
    counter_staff.columnconfigure(1, weight=1)
    counter_staff.rowconfigure(0, weight=1)

    # Load the original image for the background and create a CTkImage
    original_image = Image.open("C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\building1.jpg")

    # Function to resize the image dynamically based on the frame size
    def resize_image(event):
        # Get the new size of the left frame
        new_width = left_frame.winfo_width()
        new_height = left_frame.winfo_height()

        # Resize the image to fit the new dimensions
        resized_image = original_image.resize((new_width, new_height))
        
        # Create a CTkImage instead of ImageTk.PhotoImage
        new_ctk_image = ctk.CTkImage(light_image=resized_image, size=(new_width, new_height))

        # Update the image in the label
        image_label.configure(image=new_ctk_image)
        image_label.image = new_ctk_image  # Keep a reference to avoid garbage collection

    # Create the left frame--------------------------------------------------------------------------------------
    left_frame = ctk.CTkFrame(counter_staff, width=350)
    left_frame.grid(row=0, column=0, sticky='news')

    # Create a label inside the left frame to display the background image
    image_label = ctk.CTkLabel(left_frame, text="")
    image_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Fill the label across the frame

    # Bind the resize event to the left frame to dynamically resize the image
    left_frame.bind("<Configure>", resize_image)

    # Create the right frame--------------------------------------------------------------------------------------
    right_frame = ctk.CTkFrame(counter_staff, fg_color='transparent')
    right_frame.grid(row=0, column=1, sticky='news')

    content_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
    content_frame.pack(expand=True)


    try:
         conn = create_connection()
         cursor = conn.cursor()

         query = "SELECT * FROM operator WHERE full_name = %s"
         cursor.execute(query, (op_name,))
         data = cursor.fetchone()

         op = data[3]

         conn.commit()
         print(data)
    except Error as err:
         print(f"Error: {err}")
    finally:
            # Ensure the cursor and connection are properly closed
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    title_label = ctk.CTkLabel(content_frame ,
                                text='Welcome back!',
                                font=ctk.CTkFont(size=50, weight="bold"))
    title_label.pack(pady=20, padx=20)

    name_label = ctk.CTkLabel(content_frame ,
                                text=op_name,
                                font=ctk.CTkFont(size=20, weight="bold"))
    name_label.pack(pady=(20,0), padx=20)

    serving_office = ctk.CTkLabel(content_frame,
                                text='Serving Office')
    serving_office.pack(padx=20)

    affi_label = ctk.CTkLabel(content_frame ,
                                text=op,
                                font=ctk.CTkFont(size=20, weight="bold"))
    affi_label.pack(pady=(10,0), padx=20)

    serving_office = ctk.CTkLabel(content_frame,
                                text='Serving Window')
    serving_office.pack(padx=20)

    #button frame--------------------------------------------------------------------------------------------
    button_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
    button_frame.pack(expand=True, pady=(20,0))

    switch_btn = ctk.CTkButton(button_frame, 
                            text='Switch Office', 
                            fg_color="#d68b26", 
                            hover_color="#a45e14",
                            height=35,
                            command=lambda: button_click_event(counter_staff, op_name, op_area, op_id))
    switch_btn.pack(side='left',pady=20, padx=20)

    standby_btn = ctk.CTkButton(button_frame, 
                                text='Stand by', 
                                fg_color="#d68b26", 
                                hover_color="#a45e14",
                                height=35,
                                command=lambda: stand_by(counter_staff,op_name, op, op_id))
    standby_btn.pack(side='left',pady=20, padx=20)

    logout_btn = ctk.CTkButton(content_frame, 
                            text='Log out',
                            fg_color="#d68b26",
                            height=35,
                            command=lambda: confirm_logout(counter_staff), 
                            hover_color="#a45e14")
    logout_btn.pack(side='top',pady=20, padx=20)

#button fucntion of buttom frame--------------------------------------------------------------------------------
    def stand_by(counter_staff, op_name, op, op_id):

        if op == 'Cashier service':
            counter_staff.destroy()
            cashier_window(op_name, op_area, op_id)
        elif op == 'Promisorry note coordinator':
             counter_staff.destroy()
             pnc_window(op_name, op_area, op_id)
        elif op == 'Scholarship coordinator':
             counter_staff.destroy()
             sc_window(op_name, op_area, op_id)
        else:
             print("Error: Invalid operation area")           
    
    # Run the application
    counter_staff.mainloop()


def confirm_logout(counter_staff):
        response = messagebox.askyesno("Log out", "Are you sure you want to log out?")

        if response:
            counter_staff.destroy()
            from admin_operator_main import example
            example()
        else:
            print("Logout canceled.")

# Function to create a dialog with radio buttons----------------------------------------------------------------------------
def button_click_event(counter_staff, op_name, op_area, op_id):
        from operator_sc_dashboard import sc_window
        from operator_cashier_dashboard import cashier_window
        from operator_pnc_dashboard import pnc_window

        dialog = tk.Toplevel()
        dialog.title("Select a Office")
        dialog.iconbitmap('C:\\Users\\QHTF\\OneDrive\\Desktop\\new_queue_system\\QMS-python-gui-main\\old-logo.ico')
        dialog.resizable(False, False)

        window_width = 300
        window_height = 280
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create a label for the dialog with a cool font and color
        label = ctk.CTkLabel(dialog, text="Choose a Office", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        # Create a StringVar to hold the selected radio button value
        selected_option = tk.StringVar(value="Cashier service")

        # Create the radio buttons with custom styling
        radio1 = ctk.CTkRadioButton(dialog, 
                                    text="  Cashier service", 
                                    variable=selected_option, 
                                    value="Cashier service", 
                                    fg_color="#d68b26", 
                                    hover_color="#d68b26")
        radio1.pack(padx=30,pady=10, anchor='w')

        radio2 = ctk.CTkRadioButton(dialog, 
                                    text="  Scholarship coordinator", 
                                    variable=selected_option, 
                                    value="Scholarship coordinator",
                                    fg_color="#d68b26", 
                                    hover_color="#d68b26")
        radio2.pack(padx=30,pady=10, anchor='w')

        radio3 = ctk.CTkRadioButton(dialog, 
                                    text="  Promissory note coordinator", 
                                    variable=selected_option, 
                                    value="Promisorry note coordinator", 
                                    fg_color="#d68b26", 
                                    hover_color="#d68b26")
        radio3.pack(padx=30,pady=10, anchor='w')
        
        #Switch office
        def confirm_selection():
            print("Selected service:", selected_option.get())
            dialog.destroy()  # Close the dialog window

            conn = create_connection()
            if conn is None:
                print("Failed to connect to the database.")
                return

            cursor = conn.cursor()

            selected = selected_option.get()  # Make sure selected option is captured

            try:
                # Check what option is selected and run the appropriate query
                if selected == 'Cashier service':
                    query = "UPDATE operator SET operate_area = %s WHERE id = %s"
                    cursor.execute(query, (selected, op_id))  # Assuming op_area is defined
                    conn.commit()
                    counter_staff.destroy()  # Close current window
                    cashier_window(op_name, op_area, op_id)  # Open cashier window
                    print("Success: Cashier service updated")
                    
                elif selected == 'Scholarship coordinator':
                    query = "UPDATE operator SET operate_area = %s WHERE id = %s"
                    cursor.execute(query, (selected, op_id))  # Assuming op_area is defined
                    conn.commit()
                    counter_staff.destroy()  # Close current window
                    sc_window(op_name, op_area, op_id)  # Open scholarship coordinator window
                    print("Success: Scholarship coordinator updated")

                elif selected == 'Promisorry note coordinator':
                    query = "UPDATE operator SET operate_area = %s WHERE id = %s"
                    cursor.execute(query, (selected, op_id))  # Assuming op_area is defined
                    conn.commit()
                    counter_staff.destroy()  # Close current window
                    pnc_window(op_name, op_area, op_id)  # Open scholarship coordinator window
                    print("Success: Scholarship coordinator updated")
                else:
                    print("Invalid selection.")
            except Error as err:
                print(f"Error: {err}")
            finally:
                # Ensure the cursor and connection are properly closed
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        # Create a button to confirm selection with custom styling
        confirm_button = ctk.CTkButton(dialog, 
                                    text="Confirm", 
                                    command=confirm_selection,
                                    fg_color="#d68b26", 
                                    hover_color="#a45e14")
        confirm_button.pack(pady=20)

        dialog.grab_set()
