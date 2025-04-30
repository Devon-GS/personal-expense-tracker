import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def cat_managment():
    # PROGRAM
    catagory = Tk()
    catagory.title('Catagory Management')
    catagory.geometry("1000x500")

    # SETUP TREE VIEW
    # Add Some Style
    style = ttk.Style()

    # Pick A Theme
    style.theme_use('default')

    # Configure the Treeview Colors
    style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3")

    # Change Selected Color
    style.map('Treeview',
    background=[('selected', "#347083")])

    # Create a Treeview Frame
    tree_frame = Frame(catagory)
    tree_frame.pack(pady=10)

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Columns
    my_tree['columns'] = ("ID", "Catagory Description")

    # Format Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=50)
    my_tree.column("Catagory Description", anchor=W, width=140)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Catagory Description", text="Catagory Description", anchor=W)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    # GET DATA FROM DATABASE CATAGORY
    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    def query_database():
        # Create a database or connect to one that exists
        conn = sqlite3.connect('database.db')

        # Create a cursor instance
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM catagory")
        records = c.fetchall()
        
        # Add our data to the screen
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('oddrow',))
            # increment counter
            count += 1

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()    

    # SETUP ENTRY BOXES AND BUTTONS
    # Add Record Entry Boxes
    data_frame = LabelFrame(catagory, text="Record")
    data_frame.pack(fill="x", expand="yes", padx=20)

    id_label = Label(data_frame, text="ID")
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry = Entry(data_frame)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    cd_label = Label(data_frame, text="Catagory Description")
    cd_label.grid(row=0, column=2, padx=10, pady=10)
    cd_entry = Entry(data_frame)
    cd_entry.grid(row=0, column=3, padx=10, pady=10)

    # FUNCTIONS FOR BUTTONS

    # Update record
    def update_record():
        # Grab the record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(id_entry.get(), cd_entry.get(),))

        # Create a database or connect to one that exists
        conn = sqlite3.connect('database.db')

        # Create a cursor instance
        c = conn.cursor()

        c.execute('''UPDATE catagory SET catagory = :catagory WHERE oid = :oid''',
            {
                'catagory' : cd_entry.get(),
                'oid' : id_entry.get()
            })

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Clear entry boxes
        id_entry.delete(0, END)
        cd_entry.delete(0, END)

    # Add record
    def add_record():
        # Create a database or connect to one that exists
        conn = sqlite3.connect('database.db')

        # Create a cursor instance
        c = conn.cursor()

        c.execute("INSERT INTO catagory VALUES (:catagory)", {'catagory' : cd_entry.get()})

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Clear entry boxes
        id_entry.delete(0, END)
        cd_entry.delete(0, END)
      
        # Clear Tree View
        my_tree.delete(*my_tree.get_children())

        # Get data from database again
        query_database()
        get_cat_data()

    # Remove One Record
    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)

        # Create a database or connect to one that exists
        conn = sqlite3.connect('database.db')

        # Create a cursor instance
        c = conn.cursor()

        c.execute("DELETE FROM catagory WHERE oid=" + id_entry.get())

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Clear the entry boxes
        clear_entries()

        # Messagebox confirmation
        messagebox.showinfo('Deleted!', 'Your Record Has Been Deleted')

    # Clear entry boxes
    def clear_entries():
        id_entry.config(state="normal")
        id_entry.delete(0, END)
        cd_entry.delete(0, END)

    # Select Record
    def select_record(e):
        # Clear entry boxes
        id_entry.delete(0, END)
        cd_entry.delete(0, END)
        
        # Grab record Number
        selected = my_tree.focus()
        # Grab record values
        values = my_tree.item(selected, 'values')

        # output to entry boxes
        id_entry.insert(0, values[0])
        id_entry.config(state="readonly")
        cd_entry.insert(0, values[1])

    # Add Buttons
    button_frame = LabelFrame(catagory, text="Commands")
    button_frame.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame, text="Update Record", command=update_record)
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame, text="Add Record", command=add_record)
    add_button.grid(row=0, column=1, padx=10, pady=10)

    # remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
    # remove_all_button.grid(row=0, column=2, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    remove_many_button = Button(button_frame, text="Remove Many Selected", state='disabled')
    remove_many_button.grid(row=0, column=4, padx=10, pady=10)

    clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    clear_record_button.grid(row=0, column=7, padx=10, pady=10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>", select_record)

    # Load data 
    query_database()

    # RUN PROGRAM
    catagory.mainloop()  

def get_cat_data():
    catagories = []
    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT * FROM catagory")
    records = c.fetchall()

    for cat in records:
        catagories.append(cat[0])

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()    

    return tuple(catagories)