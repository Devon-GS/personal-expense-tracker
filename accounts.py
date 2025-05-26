import re
import sqlite3
from tkinter import *
from tkinter import ttk
from weakref import ref


class Accounts(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        def query_database():
            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            c.execute("SELECT amount, category FROM bankStatement")
            bank_records = c.fetchall()

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Sort Category and Amounts
            if len(bank_records) > 0:
                cat_total = {}

                for x in bank_records:
                    if x[1] not in cat_total.keys():
                        cat_total[x[1]] = 0.0
                        cat_total[x[1]] += float(x[0])
                    else:
                        cat_total[x[1]] += float(x[0])

                cat_total['Uncategorised'] = cat_total.pop('Please Select')

                cat_total_sorted = dict(sorted(cat_total.items()))

                # Add our data to the table
                global count
                count = 0

                for key, value in cat_total_sorted.items():
                    if value < 0.0:
                        value = "{:.2f}".format(value*-1,)

                    if count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(key, round(float(value), 2)), tags=('evenrow',))
                    else:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(key, round(float(value), 2)), tags=('oddrow',))
                    # increment counter
                    count += 1

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
        my_tree['columns'] = ("Category", "Total Amount")

        # Format Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Category", anchor=W, width=250)
        my_tree.column("Total Amount", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Category", text="ID", anchor=W)
        my_tree.heading("Total Amount", text="Total Amount", anchor=W)

        # Create Striped Row Tags
        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="lightblue")

        # Add Refresh Button
        def refresh():
            # Clear Tree View
            my_tree.delete(*my_tree.get_children())
            # Get data from database
            query_database()

        refresh_button = Button(self, text="Refresh", command=refresh)
        refresh_button.pack()

        # Get data from database
        query_database()        