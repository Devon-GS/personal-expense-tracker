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

            c.execute("SELECT * FROM category")
            cat_records = c.fetchall()

            # Commit changes
            conn.commit()
            conn.close()

            # Sort Category and Amounts
            if len(bank_records) > 0:
                cat_total = {}

                # Add from category
                for x in cat_records:
                    cat = x[0]
                    budget = x[1]

                    if "Please Select" not in cat_total.keys():
                        cat_total["Please Select"] = [0.0]  
                        cat_total["Please Select"].append('None')

                    elif cat not in cat_total.keys():
                        cat_total[cat] = [0.0]  
                        cat_total[cat].append(budget)

                # Add from bankstatements
                for x in bank_records:
                    amount = x[0]
                    cat = x[1]

                    cat_total[cat][0] += float(amount)
                
                # # Change name and order dict
                cat_total['Uncategorised'] = cat_total.pop('Please Select')
        
                cat_total_sorted = dict(sorted(cat_total.items()))

                # Add our data to the table
                global count
                count = 0

                for key, value in cat_total_sorted.items():
                    amount = value[0]
                    budget = value[1]

                    # Format amount
                    if amount < 0.0:
                        amount = "{:.2f}".format(amount*-1,)

                    # Check over/under/near
                    if budget == 'None':
                        budget = '-'
                        over_under = '-'
                    # elif amt >= (float(bud) - float(2000)) or amt <= bud:
                        # if with in certain percent of budget
                    elif float(amount) < float(budget) :
                        over_under = 'Within'
                    else:
                        over_under = 'OVER'

                    # Display Data In Table
                    if count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(key, round(float(amount), 2), budget, over_under), tags=('evenrow',))
                    else:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(key, round(float(amount), 2), budget, over_under), tags=('oddrow',))
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
        my_tree['columns'] = ("Category", "Total Amount", "Category Budget", "Within / Over")

        # Format Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Category", anchor=W, width=250)
        my_tree.column("Total Amount", anchor=W, width=140)
        my_tree.column("Category Budget", anchor=W, width=140)
        my_tree.column("Within / Over", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Category", text="Category", anchor=W)
        my_tree.heading("Total Amount", text="Total Amount", anchor=W)
        my_tree.heading("Category Budget", text="Category Budget", anchor=W)
        my_tree.heading("Within / Over", text="Within / Over", anchor=W)

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