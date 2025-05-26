import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import categories as c
import init_database as indata


def auto_apply_rules():
    cr_list = []
    bs_list = []
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT appliedTo, category FROM categoryRules")
    cr_records = c.fetchall()

    c.execute("SELECT description, category FROM bankStatement")
    bs_records = c.fetchall()

    # Add to lists
    for x in cr_records:
        cr_list.append([x[0], x[1]])

    for x in bs_records:
        pass
        bs_list.append([x[0], x[1]])

    for bs in bs_list:
        for cr in cr_list:
            if bs[1] == 'Delete':
                query = ("DELETE FROM bankStatement WHERE description = ?")
                c.execute(query, (bs[0],))
    
            elif cr[0] == bs[0] and bs[1] == 'Please Select':
                query = ("UPDATE bankStatement SET category = ? WHERE description = ?")

                c.execute(query, (cr[1], bs[0]))
                
    # Commit changes
    conn.commit()
    conn.close()

def auto_add_rule(rule_name, apply, category):
    if category == 'Please Select':
        messagebox.showwarning('Category', 'Please Select A Category For The Rule')
    else:
        # Create a database or connect to one that exists
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("INSERT INTO categoryRules VALUES (:ruleName, :appliedTo, :category)",
        {
            'ruleName' : rule_name,
            'appliedTo' : apply,
            'category' : category
        })

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

class CategoryRules(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        def query_database():
            # Create a database or connect to one that exists
            conn = sqlite3.connect('database.db')

            # Create a cursor instance
            c = conn.cursor()

            c.execute("SELECT rowid, * FROM categoryRules")
            records = c.fetchall()
            
            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

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
        tree_frame = Frame(self)
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
        my_tree['columns'] = ("ID", "Rule Name", "Apply To", "Category")

        # Format Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Rule Name", anchor=W, width=140)
        my_tree.column("Apply To", anchor=W, width=140)
        my_tree.column("Category", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Rule Name", text="Rule Name", anchor=W)
        my_tree.heading("Apply To", text="Apply To", anchor=W)
        my_tree.heading("Category", text="Category", anchor=W)

        # Create Striped Row Tags
        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="lightblue")

        # SETUP ENTRY BOXES AND BUTTONS
        # Add Record Entry Boxes
        data_frame = LabelFrame(self, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame, state="readonly")
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        rule_name_label = Label(data_frame, text="Rule Name")
        rule_name_label.grid(row=0, column=2, padx=10, pady=10)
        rule_name_entry = Entry(data_frame)
        rule_name_entry.grid(row=0, column=3, padx=10, pady=10)

        apply_label = Label(data_frame, text="Apply to Description")
        apply_label.grid(row=0, column=4, padx=10, pady=10)
        apply_entry = Entry(data_frame)
        apply_entry.grid(row=0, column=5, padx=10, pady=10)

        # Add category to drop down
        cat_label = Label(data_frame, text="Category")
        cat_label.grid(row=0, column=6, padx=10, pady=10)

        def update_combobox_options():
            options = c.get_cat_data()
            cat_entry['values']= options

        n = StringVar()
        cat_entry = ttk.Combobox(data_frame, width = 18, textvariable = n, postcommand=update_combobox_options) 
        cat_entry.grid(row=0, column=7, padx=10, pady=10)

        # FUNCTIONS FOR BUTTONS
        def add_record():
                # Create a database or connect to one that exists
                conn = sqlite3.connect('database.db')
                c = conn.cursor()

                c.execute("INSERT INTO categoryRules VALUES (:ruleName, :appliedTo, :category)",
                {
                    'ruleName' : rule_name_entry.get(),
                    'appliedTo' : apply_entry.get(),
                    'category' : cat_entry.get()
                })

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                rule_name_entry.delete(0, END)
                apply_entry.delete(0, END)
                cat_entry.delete(0, END)

                # Clear Tree View
                my_tree.delete(*my_tree.get_children())

                # Get data from database again
                query_database()

            # Update record
        def update_record():
            # Grab the record number
            selected = my_tree.focus()
            # Update record
            my_tree.item(selected, text="", values=(id_entry.get(), rule_name_entry.get(), apply_entry.get(), cat_entry.get(),))

            # Create a database or connect to one that exists
            conn = sqlite3.connect('database.db')

            # Create a cursor instance
            c = conn.cursor()

            c.execute('''UPDATE categoryRules SET
                ruleName = :ruleName,
                appliedTo = :appliedTo,
                category = :category

                WHERE oid = :oid''',
                {
                    'ruleName' : rule_name_entry.get(),
                    'appliedTo' : apply_entry.get(),
                    'category' : cat_entry.get(),
                    'oid' : id_entry.get()
                })

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear entry boxes
            id_entry.config(state="normal")
            id_entry.delete(0, END)
            id_entry.config(state="readonly")
            rule_name_entry.delete(0, END)
            apply_entry.delete(0, END)
            cat_entry.delete(0, END)

        # Remove one record
        def remove_one():
            x = my_tree.selection()[0]
            my_tree.delete(x)

            # Create a database or connect to one that exists
            conn = sqlite3.connect('database.db')

            # Create a cursor instance
            c = conn.cursor()

            c.execute("DELETE FROM categoryRules WHERE oid=" + id_entry.get())

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear the entry boxes
            clear_entries()

            # Messagebox confirmation
            messagebox.showinfo('Deleted!', 'Your Record Has Been Deleted')
                
        # Remove all records
        def remove_all():
            # Messagebox Warning
            messagebox.showwarning('Delete Detected', 'YOU ARE ABOUT TO DELETE ALL RECORDS')

            response = messagebox.askyesno('Delete Detected', 'Are you sure you want to delete ALL RECORDS?')

            # Logic for message box
            if response == 1:
                for record in my_tree.get_children():
                    my_tree.delete(record)

                # Create a database or connect to one that exists
                conn = sqlite3.connect('database.db')

                # Create a cursor instance
                c = conn.cursor()

                c.execute("DROP TABLE categoryRules")

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear the entry boxes
                clear_entries()

                # Add back table to database
                indata.init_database()

        # Clear entry boxes
        def clear_entries():
            id_entry.config(state="normal")
            id_entry.delete(0, END)
            id_entry.config(state="readonly")
            rule_name_entry.delete(0, END)
            apply_entry.delete(0, END)
            cat_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.config(state="normal")
            id_entry.delete(0, END)
            rule_name_entry.delete(0, END)
            apply_entry.delete(0, END)
            cat_entry.delete(0, END)

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')

            # output to entry boxes
            id_entry.insert(0, values[0])
            id_entry.config(state="readonly")
            rule_name_entry.insert(0, values[1])
            apply_entry.insert(0, values[2])
            cat_entry.insert(0, values[3])

        # Add Buttons
        button_frame = LabelFrame(self, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        # add_button = Button(button_frame, text="Add Record", command=add_record)
        # add_button.grid(row=0, column=1, padx=10, pady=10)

        # remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
        # remove_all_button.grid(row=0, column=2, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
        remove_one_button.grid(row=0, column=3, padx=10, pady=10)

        # remove_many_button = Button(button_frame, text="Remove Many Selected", state='disabled')
        # remove_many_button.grid(row=0, column=4, padx=10, pady=10)

        # move_up_button = Button(button_frame, text="Accounts")
        # move_up_button.grid(row=0, column=5, padx=10, pady=10)

        # # move_down_button = Button(button_frame, text="Move Down", state='disabled')
        # # move_down_button.grid(row=0, column=6, padx=10, pady=10)

        # move_down_button = Button(button_frame, text="Category", command=c.cat_managment)
        # move_down_button.grid(row=0, column=6, padx=10, pady=10)

        clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        clear_record_button.grid(row=0, column=7, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Get data and disply
        query_database()
