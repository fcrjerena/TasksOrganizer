import sqlite3
import tkinter as tk
from tkinter import ttk

# Function to fetch data from SQLite database
def fetch_data():
    conn = sqlite3.connect('PersonalTasksList.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to display data in the table
def display_table(data):
    def sort_column(tree, col, reverse):
        # Get the data to sort
        l = [(tree.set(k, col), k) for k in tree.get_children('')]

        # Convert data to numbers if the column is 'Comments'
        if col == 'ID':
            l = [(float(val), k) if val else (0, k) for val, k in l]

        # Sort the data
        l.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Reverse sort next time
        tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

    def sort_column1(tree, col, reverse):
        # Get the data to sort
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        # Sort the data
        l.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Reverse sort next time
        tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

    def search_table():
        query = search_var.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        for row in data:
            if query in str(row).lower():
                tree.insert('', tk.END, values=row)    

    # Create Tkinter window
    root = tk.Tk()
    root.title("SQLite Data Table")

    # Create a style and configure the Treeview for alternating row colors
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.map('Treeview', background=[('selected', 'lightblue')])

    # Create frame for the search bar
    search_frame = tk.Frame(root)
    search_frame.pack(side=tk.TOP, fill=tk.X)

    # Create search bar
    search_label = tk.Label(search_frame, text="Search:")
    search_label.pack(side=tk.LEFT, padx=10)
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    search_button = tk.Button(search_frame, text="Search", command=search_table)
    search_button.pack(side=tk.LEFT, padx=10)

    # Create Treeview widget
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(tree_frame, columns=('ID', 'Label', 'Description', 'Priority', 'Complexity', 'Deadline', 'Main Task ID', 'Blockers', 'Created', 'Delay', 'Rank', 'Status', 'Comments'), show='headings', style="Treeview")
    tree.heading('ID', text='ID', command=lambda: sort_column(tree, 'ID', False))
    tree.heading('Label', text='Label', command=lambda: sort_column(tree, 'Label', False))
    tree.heading('Description', text='Description', command=lambda: sort_column(tree, 'Description', False))
    tree.heading('Priority', text='Priority', command=lambda: sort_column(tree, 'Priority', False))
    tree.heading('Complexity', text='Complexity', command=lambda: sort_column(tree, 'Complexity', False))
    tree.heading('Deadline', text='Deadline', command=lambda: sort_column(tree, 'Deadline', False))
    tree.heading('Main Task ID', text='Main Task ID', command=lambda: sort_column(tree, 'Main Task ID', False))
    tree.heading('Blockers', text='Blockers', command=lambda: sort_column(tree, 'Blockers', False))
    tree.heading('Created', text='Created', command=lambda: sort_column(tree, 'Created', False))
    tree.heading('Delay', text='Delay', command=lambda: sort_column(tree, 'Delay', False))
    tree.heading('Rank', text='Rank', command=lambda: sort_column(tree, 'Rank', False))
    tree.heading('Status', text='Status', command=lambda: sort_column(tree, 'Status', False))
    tree.heading('Comments', text='Comments', command=lambda: sort_column(tree, 'Comments', False))

    # Set column widths
    tree.column('ID', width=50, anchor='center')
    tree.column('Label', width=150, anchor='center')
    tree.column('Description', width=255, anchor='w')
    tree.column('Priority', width=80, anchor='center')
    tree.column('Complexity', width=80, anchor='center')
    tree.column('Deadline', width=100, anchor='center')
    tree.column('Main Task ID', width=50, anchor='center')
    tree.column('Blockers', width=255, anchor='w')
    tree.column('Created', width=100, anchor='center')
    tree.column('Delay', width=50, anchor='center')
    tree.column('Rank', width=50, anchor='center')
    tree.column('Status', width=50, anchor='center')
    tree.column('Comments', width=255, anchor='w')

    # Add vertical scrollbar
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # Add horizontal scrollbar
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hsb.set)

    # Insert data into Treeview with alternating row colors
    for i, row in enumerate(data):
        tree.insert('', tk.END, values=row, tags=('oddrow',) if i % 2 == 0 else ('evenrow',))

    # Configure tag colors for alternating row effect
    tree.tag_configure('oddrow', background='lightgrey')
    tree.tag_configure('evenrow', background='white')

    # Add Treeview to window and start the Tkinter main loop
    tree.pack(fill=tk.BOTH, expand=True)    
    root.mainloop()

# Fetch data and display table
data = fetch_data()
display_table(data)



