import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry
import os
import yaml
import matplotlib
matplotlib.use('TkAgg',force=True)      #I put this but I still have the problem...
from matplotlib import pyplot as plt
import numpy as np

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

    # Function to close the database connection and the Tkinter window
    def onClosing():
        # global filePath

        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     # Close the database connection
        #     #sqliteConnection.close()    
        #     print("Deu certo!!!")        
        #     # Destroy the Tkinter window
        #     root.destroy()
        root.destroy()
        None

    # Create Tkinter window
    root = tk.Tk()
    root.title("Task's Database (SQLite)")

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
    tree.column('Deadline', width=80, anchor='center')
    tree.column('Main Task ID', width=80, anchor='center')
    tree.column('Blockers', width=150, anchor='w')
    tree.column('Created', width=80, anchor='center')
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

    # Bind the on_closing function to the window close event
    root.protocol("WM_DELETE_WINDOW", onClosing)

    # Add Treeview to window and start the Tkinter main loop
    tree.pack(fill=tk.BOTH, expand=True)    
    root.mainloop()

def getProfileSettings(profile_name):
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, 'config.yaml')

    #Load configuration from YAML file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        
    profiles = config.get('profiles', {})
    return profiles.get(profile_name, {})

class TasksOrganizer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tasks Organizer")
        self.geometry("600x350")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        self.createSystemConfigurationTab()        
        self.createTasksManagementTab()
        self.createFiltersTab()

        self.createStatisticsTab()
        # Bind the NotebookTabChanged event to the handler
        self.notebook.bind('<<NotebookTabChanged>>', self.onTabChanged)            

        self.createAboutTab()

    def createSystemConfigurationTabDeletar(self):
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="System Configuration")
        
        # Add vertical space
        ttk.Label(tab1, text="").pack()

        systemConfigFrame = ttk.LabelFrame(tab1, text="System Configuration")
        systemConfigFrame.pack(fill="both", expand="yes", padx=20, pady=10)

        self.createANewDatabaseButton = ttk.Button(systemConfigFrame, text="Create A New Database", command=self.createNewDatabase)
        self.createANewDatabaseButton.pack(fill=tk.X, anchor=tk.W, padx=10, pady=5)
        
        openDatabaseFrame = ttk.Frame(systemConfigFrame)
        openDatabaseFrame.pack(fill=tk.X, padx=10, pady=5)

        self.openDatabaseFromButton = ttk.Button(openDatabaseFrame, text="Open Database", command=self.openDatabase)
        self.openDatabaseFromButton.pack(side=tk.LEFT, fill=tk.X)

        self.databasePathEntry = ttk.Entry(openDatabaseFrame, width=50)
        self.databasePathEntry.insert(0, "Empty")        
        self.databasePathEntry.pack(side=tk.LEFT, padx=5)

    def createSystemConfigurationTab(self):
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="System Configuration")
    
        # Add vertical space
        ttk.Label(tab1, text="").grid(row=0, column=0, pady=(20, 0))  # Adding vertical space

        systemConfigFrame = ttk.LabelFrame(tab1, text="System Configuration")
        systemConfigFrame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Define a standard width for the buttons
        buttonWidth = 25

        self.createANewDatabaseButton = ttk.Button(systemConfigFrame, text="Create A New Database", command=self.createNewDatabase, width=buttonWidth)
        self.createANewDatabaseButton.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    
        openDatabaseFrame = ttk.Frame(systemConfigFrame)
        openDatabaseFrame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.openDatabaseFromButton = ttk.Button(openDatabaseFrame, text="Open Database", command=self.openDatabase, width=buttonWidth)
        self.openDatabaseFromButton.grid(row=0, column=0, sticky="w")

        self.databasePathEntry = ttk.Entry(openDatabaseFrame, width=50)
        self.databasePathEntry.insert(0, "Empty")        
        self.databasePathEntry.grid(row=0, column=1, padx=5, sticky="ew")

        openDatabaseFrame.grid_columnconfigure(1, weight=1)  # Make the entry box expand to fill available space

        systemConfigFrame.grid_columnconfigure(0, weight=1)  # Make the label frame expand to fill available space
        tab1.grid_columnconfigure(0, weight=1)  # Make the tab expand to fill available space

        
    def createTasksManagementTab(self):
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Tasks Management", state="disabled")
        
        # Add vertical space
        ttk.Label(self.tab2, text="").pack()

        tasksManagementFrame = ttk.LabelFrame(self.tab2, text="App functionalities")
        tasksManagementFrame.pack(fill="both", expand="yes", padx=20, pady=10)
        
        buttonNames = ["Include New Task", "Edit Task", "Update Rank", "Generate Daily Task List", "List Dependencies"]
        buttonCommands = [self.includeNewTask, self.editTask, self.updateRankNew, self.generateDailyTaskList, self.listDependencies]
        maxButtonWidth = max([len(name) for name in buttonNames])

        for name, command in zip(buttonNames, buttonCommands):
            button = ttk.Button(tasksManagementFrame, text=name, command=command, width=maxButtonWidth)
            button.pack(fill=tk.X, anchor=tk.W, padx=10, pady=5)

    def createFiltersTab(self):
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Filters", state="disabled")
        
        # Add vertical space
        ttk.Label(self.tab3, text="").pack()

        filterFrame = ttk.Frame(self.tab3)
        filterFrame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(filterFrame, text="Filters").pack(side=tk.LEFT)

        filterOptions = [
            "NoFilter", "FilterTasksByRank", "FilterTasksStatusActive", "FilterTasksStatusBlocked",
            "FilterTasksByMostDelayedTasks", "FilterTasksByPriority", "FilterTasksByComplexity", 
            "FilterTasksByCriticality", "FilterTasksStatusDone", "FilterTasksStatusAborted", 
            "FilterTasksbyDateCreated"
        ]
        self.filtersCombobox = ttk.Combobox(filterFrame, values=filterOptions, width=max([len(option) for option in filterOptions]))
        self.filtersCombobox.pack(side=tk.LEFT, padx=5)

        self.showTheListWithFilterAppliedButton = ttk.Button(filterFrame, text="Show The List With Filter Applied", command=self.applyFilter)
        self.showTheListWithFilterAppliedButton.pack(side=tk.LEFT, padx=5)

    
    def createStatisticsTab(self):        
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="Statistics", state="disabled")
        
        # Add vertical space
        ttk.Label(self.tab4, text="").pack()

        ttk.Label(self.tab4, text="Here you can find information about the active database").pack(anchor=tk.W, padx=10, pady=5)

        statisticsFields = ["Aborted", "Active", "Blocked", "Done"]
        self.statisticsEntries = {}
        for field in statisticsFields:
            frame = ttk.Frame(self.tab4)
            frame.pack(anchor=tk.W, padx=10, pady=5)
            ttk.Label(frame, text=f"Tasks with status equal {field}").pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=10, state='readonly')
            entry.pack(side=tk.LEFT, padx=5)
            self.statisticsEntries[field.lower()] = entry

        #Extra lines
        frame = ttk.Frame(self.tab4)
        frame.pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(frame, text=f"Tasks with dependencies").pack(side=tk.LEFT)
        entry = ttk.Entry(frame, width=10, state='readonly')
        entry.pack(side=tk.LEFT, padx=5)
        self.statisticsEntries['dependencies'] = entry    

        frame = ttk.Frame(self.tab4)
        frame.pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(frame, text=f"Total task number").pack(side=tk.LEFT)
        entry = ttk.Entry(frame, width=10, state='readonly')
        entry.pack(side=tk.LEFT, padx=5)
        self.statisticsEntries['total'] = entry
        
        self.generateTheGraphButton = ttk.Button(self.tab4, text="Generate The Graph", command=self.generateTheGraph)
        self.generateTheGraphButton.pack(anchor=tk.W, padx=10, pady=5)

    def onTabChanged(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Statistics":
            self.onStatistics()

    def fill_statistics_entries(self, stats):
        for field, value in stats.items():
            entry = self.statisticsEntries.get(field)
            if entry:
                entry.config(state='normal')  # Enable editing
                entry.delete(0, tk.END)  # Clear current content
                entry.insert(0, str(value))  # Insert the new value
                entry.config(state='readonly')  # Disable editing again 

    def onStatistics(self):
        global filePath

        #Open the database
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Aborted';")
            nAborted = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Active';")
            nActive = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Blocked';")
            nBlocked = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Done';")
            nDone = cursor.fetchone()[0]

            query = """
                SELECT COUNT(*) FROM tasks
                WHERE ((main_task_id IS NOT NULL) AND (status = "Active" OR status = "Blocked"));
                """         
            cursor.execute(query) 
            nDependencies = cursor.fetchone()[0]
            #nDependencies = 10

            cursor.execute("SELECT COUNT(*) FROM tasks;")
            nTotal = cursor.fetchone()[0]
            #nTotal = nTotal - 1 #Discount the line empty but with ID
        except sqlite3.error as error:
            nDependencies = 0            

        #Close the database
        sqliteConnection.close()

        # Simulate filling the entries with data
        self.fill_statistics_entries({
            'aborted': nAborted,
            'active': nActive,            
            'blocked': nBlocked,
            'done': nDone,
            'dependencies': nDependencies,
            'total': nTotal
        }) 

    def generateTheGraph(self):
        global filePath, fileName

        #The order can't be changed because it is important in createGraphic() function 
        status_list = ('Aborted','Active','Blocked','Done')  

        #Open the database
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()

        #Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2)
        graph_title = 'Information about task database: ' + fileName
        fig.suptitle(graph_title, fontsize=20)

        #Function to format info to plot data
        def autopct_format(values):
            def my_format(pct):
                total = sum(values)
                val = int(round(pct*total/100.0))
                return '{:.1f}%\n({v:d})'.format(pct, v=val)
            return my_format	

        #Read data from database
        statusList = []
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Aborted';")
        nAborted = cursor.fetchall()
        statusList.append(nAborted[0])
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Active';")
        nActive = cursor.fetchall()
        statusList.append(nActive[0])
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Blocked';")
        nBlocked = cursor.fetchall()
        statusList.append(nBlocked[0])
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Done';")
        nDone = cursor.fetchall()
        statusList.append(nDone[0])	

        y = statusList

        graph1list = []	

        #In test, forcing the tuple should be a list... :^)
        tuple_read = [1,2,3,4]

        for x in range(4):
            tuple_read = y[x]
            data = tuple_read[0]
            graph1list.append(data)		
        
        y = np.array(graph1list)	

        #Configure the graph 1 (Main)
        mylabels = status_list
        mycolors = ["m", "b", "lightblue", "lightgreen"] 
        myexplode = [0, 0, 0, 0]
        textprops = {"fontsize":10} # Font size of text in pie chart	

        #plt.pie(y, labels = mylabels, colors = mycolors, explode = myexplode, shadow = True, startangle=270, radius = 1.2, autopct=autopct_format(y), textprops =textprops)
        ax2.pie(y, labels = mylabels, colors = mycolors, explode = myexplode, shadow = True, startangle=270, radius = 0.8, autopct=autopct_format(y), textprops =textprops)
        
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE (status = 'Active' AND (rank > 100));")
        y = cursor.fetchall() 
        
        graph2list = []	

        
        #Esse trecho está dando pau e eu preciso entender o que está acontecendo, o codigo no else é que está funcionando
        # if y[0] == (0,):
        #     tuple_read.append(1) 
        #     graph2list.append(1)
        #     graph2list.append(37)
        # else:	
        #     tuple_read = y[0]
        #     graph2list.append(tuple_read[0])
        #     graph2list.append(graph1list[1]-graph2list[0])	

        #In test...
        tuple_read = y[0]
        graph2list.append(tuple_read[0])
        graph2list.append(graph1list[1]-graph1list[0])
        
        #Configure the graph 2 (Secondary)
        mylabels = ["Critical","Non Critical"]
        mycolors = ["r", "#FFFF00"] #Yellow in HEX code #FFFF00
        myexplode = [0.1, 0]
        textprops = {"fontsize":15} # Font size of text in pie chart	
        
        new_var = ax1.pie(graph2list, labels = mylabels, colors = mycolors, explode = myexplode, shadow = True, startangle=90, radius = 1.0, autopct=autopct_format(graph2list), textprops =textprops)
        ax1.legend(title = "Status 'Active'", loc="upper left")

        plt.show(block=False)
        # plt.draw()
        # plt.pause(0.001)

    def createAboutTab(self):
        tab5 = ttk.Frame(self.notebook)
        self.notebook.add(tab5, text="About")
        
        # Add vertical space
        ttk.Label(tab5, text="").pack()

        ttk.Label(tab5, text="Software Version 1.0").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(tab5, text="This software was idealized and created by Fabio Jerena").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(tab5, text="Sweden, 2024-07-22").pack(anchor=tk.W, padx=10, pady=5)

        # Placeholder for logo image
        # Automatically discover the script directory
        scriptDir = os.path.dirname(os.path.abspath(__file__))        
        # Construct the full path to the image file
        imagePath = os.path.join(scriptDir, "logo.gif")
        self.logoImage = tk.PhotoImage(file=imagePath)  # Add your logo file path here
        ttk.Label(tab5, image=self.logoImage).pack(anchor=tk.W, padx=10, pady=5)

    def createNewDatabase(self):
        newDbWindow = tk.Toplevel(self)
        newDbWindow.title("Create a new database")

        ttk.Label(newDbWindow, text="Define a name for the new database").grid(row=0, column=0, padx=10, pady=5)
        self.newDbNameEntry = ttk.Entry(newDbWindow, width=50)
        self.newDbNameEntry.grid(row=0, column=1, padx=10, pady=5)

        #saveAsButton = ttk.Button(newDbWindow, text="Save As", command=self.saveAsNewDatabase)
        saveAsButton = ttk.Button(newDbWindow, text="Save As", command=lambda nw=newDbWindow: self.saveAsNewDatabase(nw))
        saveAsButton.grid(row=0, column=2, padx=10, pady=5)

    def saveAsNewDatabase(self, newDbWindow):
        global dbName

        dbName = self.newDbNameEntry.get()
        filePath = filedialog.asksaveasfilename(defaultextension=".db", initialfile=dbName,
                                                filetypes=[("SQLite Database", "*.db")])
                
        if filePath:
            sqliteConnection = sqlite3.connect(filePath)
            # Creating cursor object using connection object
            cursor = sqliteConnection.cursor()
            
            #Create a new database with the field that I need
            query = """
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label VARCHAR(50) NOT NULL,
                description VARCHAR(255) NOT NULL,
                priority INTEGER NOT NULL,
                complexity INTEGER NOT NULL, 
                deadline VARCHAR,
                main_task_id INTEGER,  
                blockers VARCHAR(255), 	
                created VARCHAR,    	
                delay INTEGER,
                rank REAL,    	
                status VARCHAR NOT NULL,	
                comments VARCHAR(255));		
            """	

            cursor.execute(query)
            sqliteConnection.close()            

            messagebox.showinfo("Database Created", f"Database {dbName} created successfully at {filePath}")

            #Close the form
            newDbWindow.destroy()            

    def openDatabase(self):
        global filePath,fileName

        filePath = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])

        if filePath:
            try:
                #sqliteConnection = sqlite3.connect(filePath)
                #cursor = sqliteConnection.cursor()
                self.databasePathEntry.delete(0, tk.END)
                #My test
                # Get the base name (file name with extension)
                baseName = os.path.basename(filePath)
                # Split the base name to separate the name and the extension
                fileName, _ = os.path.splitext(baseName)
                #self.databasePathEntry.insert(0, filePath)
                self.databasePathEntry.insert(0, fileName)                
                #cursor.execute('SELECT * FROM tasks')
                #rows = cursor.fetchall()
                messagebox.showinfo("Information", f"Database loaded from {filePath}")
                #display_table(rows)    
                self.notebook.add(self.tab2, text="Tasks Management", state="normal")  
                self.notebook.add(self.tab3, text="Filters", state="normal")   
                self.notebook.add(self.tab4, text="Statistics", state="normal")  
                
            except sqlite3.Error as e:
                self.databasePathEntry.delete(0, tk.END)
                self.databasePathEntry.insert(0, "Empty")
                messagebox.showerror("Error", f"Failed to load database: {e}")
            
            finally:               
                #sqliteConnection.close()
                
                # After closing connection object, we 
                # will print "the sqlite connection is 
                # closed"
                print("The database is already open!")
                

    def getNextTaskID(self):
        global filePath

        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT MAX(id) FROM tasks")
        maxId = cursor.fetchone()[0]
        sqliteConnection.close()
        if maxId is None:
            return 1
        else:
            return maxId + 1    

    def includeNewTask(self):
        self.newTaskWindow = tk.Toplevel(self)
        self.newTaskWindow.title("New Task")        
        lastTaskid = self.getNextTaskID()

        self.labels = [
            ("Task ID number", tk.Entry(self.newTaskWindow, width=4, state='normal'), lastTaskid),
            ("Label", tk.Entry(self.newTaskWindow, width=50), ""),
            ("Description", tk.Text(self.newTaskWindow, width=32, height=8), ""),
            ("Priority", ttk.Combobox(self.newTaskWindow, values=["Very_Low", "Low", "Medium", "High", "Very_High"]), "Very_High"),
            ("Complexity", ttk.Combobox(self.newTaskWindow, values=["Super_Slow", "Slow", "Medium", "Fast", "Super_Fast"]), "Super_Fast"),
            ("Deadline", tk.Entry(self.newTaskWindow, state='normal'), datetime.now().strftime("%Y-%m-%d")),
            ("Main Task ID", tk.Entry(self.newTaskWindow, width=4), ""),
            ("Blockers", tk.Text(self.newTaskWindow, width=32, height=8), ""),
            ("Created", tk.Entry(self.newTaskWindow, state = 'normal'), datetime.now().strftime("%Y-%m-%d")),
            ("Status", ttk.Combobox(self.newTaskWindow, values=["Active", "Aborted", "Blocked", "Done"]), "Active")                      
        ]

        for i, (label, widget, default_value) in enumerate(self.labels):
            ttk.Label(self.newTaskWindow, text=label).grid(row=i, column=0, padx=10, pady=5)
            widget.grid(row=i, column=1, padx=10, pady=5)
            if isinstance(widget, tk.Entry):
                widget.insert(0, default_value)
            elif isinstance(widget, ttk.Combobox):
                widget.set(default_value)

        self.createNewTaskButton = ttk.Button(self.newTaskWindow, text="Create New Task", command=self.saveNewTask)
        self.createNewTaskButton.grid(row=len(self.labels), column=0, columnspan=2, pady=10)    

         # Bind the Label Entry to the length check function
        self.LabelEntry = self.labels[1][1]
        self.LabelEntry.bind("<KeyRelease>", self.checkLengthLabel)

        # Bind the Description textbox to the length check function
        self.TextboxDescription = self.labels[2][1]
        self.TextboxDescription.bind("<KeyRelease>", self.checkLengthDescription)  

        # Bind the Blockers textbox to the length check function
        self.TextboxBlockers = self.labels[7][1]
        self.TextboxBlockers.bind("<KeyRelease>", self.checkLengthBlockers)
    
    def checkLengthLabel(self, event):
        # Get the current content of the Description textbox
        content = self.LabelEntry.get()
        
        # Check if the length exceeds 255 characters
        if len(content) > 50:
            # If so, remove the extra characters
            self.LabelEntry.delete(0, tk.END)
            self.LabelEntry.insert(0, content[:50])

    def checkLengthDescription(self, event):
        # Get the current content of the Description textbox
        content = self.TextboxDescription.get("1.0", tk.END)
        
        # Check if the length exceeds 255 characters
        if len(content) > 255:
            # If so, remove the extra characters
            self.TextboxDescription.delete("1.0 + 255c", tk.END)     

    def checkLengthBlockers(self, event):
        # Get the current content of the Description textbox
        content = self.TextboxBlockers.get("1.0", tk.END)
        
        # Check if the length exceeds 255 characters
        if len(content) > 255:
            # If so, remove the extra characters
            self.TextboxBlockers.delete("1.0 + 255c", tk.END)         

    def saveNewTask(self):
        task_values = {}
        for label, widget, default_value in self.labels:
            if isinstance(widget, tk.Entry):
                task_values[label] = widget.get()
            elif isinstance(widget, tk.Text):
                task_values[label] = widget.get("1.0", tk.END).strip()
            elif isinstance(widget, ttk.Combobox):
                task_values[label] = widget.get()
            elif isinstance(widget, DateEntry):
                date_value = widget.get_date()
                task_values[label] = date_value if date_value else None

        # for label, widget, default_value in self.labels:
        #     if isinstance(widget, tk.Entry):
        #         task_values[label] = widget.get()
        #     elif isinstance(widget, tk.Text):
        #         task_values[label] = widget.get("1.0", tk.END).strip()
        #     elif isinstance(widget, ttk.Combobox):
        #         task_values[label] = widget.get()
        #     elif isinstance(widget, DateEntry):
        #         task_values[label] = widget.get_date().strftime("%Y-%m-%d")
        #     elif isinstance(widget, tk.Label):
        #         task_values[label] = widget.cget("text")        
                
        if task_values['Deadline'] == "":
            task_values['Deadline'] = None
        if task_values['Main Task ID'] == "":
            task_values['Main Task ID'] = None
        if task_values['Blockers'] == "":
            task_values['Blockers'] = None     
        #Includ a new one
        task_values['Comments'] = None
        # Database insertion
        self.insertTaskIntoDatabase(task_values)

        #Message to inform the user if the database was updated correctly        
        messagebox.showinfo("Information", "The new task was included in the database with success!!!")

        #Close the form after to insert the new task
        self.newTaskWindow.destroy()

        #Update the rank after to include a new task
        self.updateRankNew()

    def insertTaskIntoDatabase(self, task_values):
        global filePath

        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label VARCHAR(50) NOT NULL,
            description VARCHAR(255) NOT NULL,
            priority INTEGER NOT NULL,
            complexity INTEGER NOT NULL, 
            deadline VARCHAR,
            main_task_id INTEGER,  
            blockers VARCHAR(255), 	
            created VARCHAR,    	
            delay INTEGER,
            rank REAL,    	
            status VARCHAR NOT NULL,	
            comments VARCHAR(255));		
        """	
        cursor.execute(query)
        
        cursor.execute('''INSERT INTO tasks (label, description, priority, complexity, deadline, main_task_id, blockers, created, status, comments) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (task_values["Label"], task_values["Description"], 
                           task_values["Priority"], task_values["Complexity"], task_values["Deadline"], 
                           task_values["Main Task ID"], task_values["Blockers"], task_values["Created"], task_values["Status"], task_values["Comments"]))
         
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()    

    def getAllTaskIDs(self):
        global filePath

        conn = sqlite3.connect(filePath)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks")
        taskIDs = [row[0] for row in cursor.fetchall()]
        conn.close()
        return taskIDs

    def editTask(self):
        self.taskIDs = self.getAllTaskIDs()
        self.editTaskWindow = tk.Toplevel(self)
        self.editTaskWindow.title("Edit Task")

        self.labels = [
            ("Task ID", ttk.Combobox(self.editTaskWindow, values=self.taskIDs), ""),
            ("Label", tk.Entry(self.editTaskWindow, width=50), ""),
            ("Description", tk.Text(self.editTaskWindow, width=32, height=8), ""),
            ("Priority", ttk.Combobox(self.editTaskWindow, values=["Very_Low", "Low", "Medium", "High", "Very_High"]), ""),
            ("Complexity", ttk.Combobox(self.editTaskWindow, values=["Super_Slow", "Slow", "Medium", "Fast", "Super_Fast"]), ""),
            ("Deadline", tk.Entry(self.editTaskWindow, state='normal'), ""),
            ("Main Task ID", tk.Entry(self.editTaskWindow, width=4), ""),
            ("Blockers", tk.Text(self.editTaskWindow, width=32, height=8), ""),
            ("Created", tk.Entry(self.editTaskWindow, state = 'normal'), ""),
            ("Status", ttk.Combobox(self.editTaskWindow, values=["Active", "Aborted", "Blocked", "Done"]), ""),
            ("Comments", tk.Text(self.editTaskWindow, width=32, height=8), "")
        ]

        self.widgets = {}
        for i, (label, widget, default_value) in enumerate(self.labels):
            ttk.Label(self.editTaskWindow, text=label).grid(row=i, column=0, padx=10, pady=5)
            widget.grid(row=i, column=1, padx=10, pady=5)
            self.widgets[label] = widget
            if isinstance(widget, tk.Entry):
                widget.insert(0, default_value)

        self.searchByIDButton = ttk.Button(self.editTaskWindow, text="Search by ID", command=self.searchByID)        
        self.searchByIDButton.grid(row=0, column=2, padx=10, pady=5)

        self.editTaskButton = ttk.Button(self.editTaskWindow, text="Edit Task", command=self.saveEditedTask)
        self.editTaskButton.grid(row=len(self.labels), column=0, columnspan=2, pady=10)        

    def searchByID(self):
        global filePath

        task_id = self.widgets["Task ID"].get()
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT id, label, description, priority, complexity, deadline, main_task_id, blockers, created, status, comments FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        sqliteConnection.close()        

        if task:
            columns = ["Task ID", "Label", "Description", "Priority", "Complexity", "Deadline", "Main Task ID", "Blockers", "Created", "Status", "Comments"]
            for col, value in zip(columns, task):
                widget = self.widgets[col]
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                    if value == None:
                        value = ""
                    widget.insert(0, value)
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    if value == None:
                        value = ""
                    widget.insert("1.0", value)
                elif isinstance(widget, ttk.Combobox):
                    if value == None:
                        value = ""
                    widget.set(value)
        else:
            tk.messagebox.showerror("Error", "Task ID not found!")   

    def saveEditedTask(self):
        task_values = {}
        for label, widget, default_value in self.labels:
            if isinstance(widget, tk.Entry):
                task_values[label] = widget.get()
            elif isinstance(widget, tk.Text):
                task_values[label] = widget.get("1.0", tk.END).strip()
            elif isinstance(widget, ttk.Combobox):
                task_values[label] = widget.get()
            elif isinstance(widget, DateEntry):
                date_value = widget.get_date()
                task_values[label] = date_value if date_value else None

        if task_values['Deadline'] == "":
            task_values['Deadline'] = None      
        if task_values['Main Task ID'] == "":
            task_values['Main Task ID'] = None
        if task_values['Blockers'] == "":
            task_values['Blockers'] = None    
        if task_values['Comments'] == "":
            task_values['Comments'] = None
        
        # Database insertion
        self.updateTaskIntoDatabase(task_values)

        #Message to inform the user if the database was updated correctly        
        messagebox.showinfo("Information", "The task edited was updated with success!!!")

        #Close the form after edit the task
        self.editTaskWindow.destroy()

        #Update the rank after to edit a task
        self.updateRankNew()

    def updateTaskIntoDatabase(self, task_values):
        global filePath

        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
                
        cursor.execute('''UPDATE tasks SET label=?, description=?, priority=?, complexity=?, deadline=?, main_task_id=?, blockers=?, created=?, status=?, comments=? 
                          WHERE id=?''', 
                          (task_values["Label"], task_values["Description"], 
                           task_values["Priority"], task_values["Complexity"], task_values["Deadline"], 
                           task_values["Main Task ID"], task_values["Blockers"], task_values["Created"], task_values["Status"], task_values["Comments"], task_values["Task ID"]))
         
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

    def updateRank(self):
        global filePath

        #Open the yaml file with the configuration
        profile_settings = getProfileSettings('Personal')
                
        if not profile_settings:
            raise ValueError(f"Profile '{'Personal'}' not found in the configuration.")

        #Recovery the information from the yaml file
        weights = profile_settings.get('weights', {})
        weight_priority = weights.get('priority', None)
        weight_complexity = weights.get('complexity', None)
        weight_delay = weights.get('delay', None)
        relevance_offset = profile_settings.get('relevance_offset', None) #When you passed the deadline
        deadline_slope = profile_settings.get('deadline_slope', None) #prioritize tasks with deadline
                
        # The main idea in this query is increase the index when a task has a deadline defined, the tasks 
        # with deadline must be prioritized over the tasks that theres's no deadline filled, when the
        # deadline was expired, a big step is added to the index, increasing the task index (became a ultra-high priority)

        query = """
        UPDATE tasks
        SET 
        delay = julianday(date()) - julianday(created), 
        rank = ROUND(((priority * ?) + (complexity * ?) + (delay * ?)) + 
            CASE 
                WHEN deadline IS NOT NULL THEN
                    CASE
                        WHEN julianday(date()) > julianday(deadline) THEN
                            (? + (julianday(date()) - julianday(deadline)))
                        ELSE
                            (delay * ?)
                    END
                ELSE
                    0            
            END, 2) 
        WHERE (status = "Active" OR status = "Blocked");
        """

        #Connect to the database
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()

        # Executing the query with the weight variables
        cursor.execute(query, (weight_priority, weight_complexity, weight_delay, relevance_offset, deadline_slope))

        # Committing the transaction
        sqliteConnection.commit()
        sqliteConnection.close()    

        #Message to inform the user if the database was updated correctly        
        messagebox.showinfo("Information", "The Rank was updated with success!!!")

    # Function to check if a string is a valid date
    def isValidDate(self, dateStr):
        try:
            if dateStr == None:
                return False
            else:
                datetime.strptime(dateStr, '%Y-%m-%d')
                return True
        except ValueError:
            return False
    
    def updateRankNew(self):
        global filePath

        # Dictionary mapping priority text to numeric values
        priorityList = {
            "Very_Low":1,
            "Low":2,
            "Medium":3,
            "High":5,
            "Very_High":8
        }

        complexityList = {
            "Super_Slow":1, 
			"Slow":2, 
			"Medium":3, 
			"Fast":5, 
			"Super_Fast":8
        }  

        #Open the yaml file with the configuration
        profile_settings = getProfileSettings('Personal')
                
        if not profile_settings:
            raise ValueError(f"Profile '{'Personal'}' not found in the configuration.")

        #Recovery the information from the yaml file
        weights = profile_settings.get('weights', {})
        weight_priority = weights.get('priority', None)
        weight_complexity = weights.get('complexity', None)
        weight_delay = weights.get('delay', None)
        relevance_offset = profile_settings.get('relevance_offset', None) #When you passed the deadline
        deadline_slope = profile_settings.get('deadline_slope', None) #prioritize tasks with deadline

        # Connect to the SQLite database
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()        

        # Query to fetch priority and delay from the tasks table
        query = """
        SELECT id, priority, complexity, deadline, created FROM tasks
        WHERE status = "Active" OR status = "Blocked";
        """   
        cursor.execute(query)
        rows = cursor.fetchall() 

        # Iterate through the rows and calculate the new values
        for row in rows:
            taskId = row[0]
            priorityText = row[1]
            complexityText = row[2]
            deadlineStr = row[3]
            createdStr = row[4]

            created = datetime.strptime(createdStr, '%Y-%m-%d')
            delay = (datetime.now().date() - created.date()).days

            # Get the numeric value for the priority text
            priorityValue = priorityList.get(priorityText, 0)

            # Get the numeric value for the priority text
            complexityValue = complexityList.get(complexityText, 0)
            
            if self.isValidDate(deadlineStr):
                deadline = datetime.strptime(deadlineStr, '%Y-%m-%d')
                # Calculate the difference in days
                daysDifference = (deadline.date()-datetime.now().date()).days
                # Calculate the result 
                if daysDifference >= 0:
                    rankCalculation = (priorityValue*weight_priority)+(complexityValue*weight_complexity)+(delay*weight_delay)+(delay*deadline_slope)
                else:
                    rankCalculation = (priorityValue*weight_priority)+(complexityValue*weight_complexity)+(delay*weight_delay)+relevance_offset-daysDifference
            else:
                # Calculate the result 
                rankCalculation = (priorityValue*weight_priority)+(complexityValue*weight_complexity)+(delay*weight_delay)
            
            rankCalculationRounded = round(rankCalculation,2)
            # Update the tasks table with the calculated result
            cursor.execute("UPDATE tasks SET delay = ?, rank = ? WHERE id = ?", (delay, rankCalculationRounded, taskId))
            # Commit the transaction to save changes
            sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()

        #Message to inform the user if the database was updated correctly        
        messagebox.showinfo("Information", "The Rank was updated with success!!!")        

    def generateDailyTaskList(self):
        global filePath

        # Connect to the SQLite database
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()        

        # Query to fetch priority and delay fromopendatabeopenthe tasks table
        query = """
        SELECT * FROM tasks
        WHERE (status = "Active") ORDER BY rank DESC LIMIT 5;
        """   
        cursor.execute(query)
        rows = cursor.fetchall()     
        display_table(rows)    

    def listDependencies(self):
        global filePath

        # Connect to the SQLite database
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()        

        # Query to fetch priority and delay from the tasks table
        query = """
        SELECT * FROM tasks
        WHERE ((main_task_id IS NOT NULL) AND (status = "Active" OR status = "Blocked"));
        """
        cursor.execute(query)
        rows = cursor.fetchall()     
        display_table(rows)   

    def applyFilter(self):
        global filePath

        if self.filtersCombobox.get():
            # Connect to the SQLite database
            sqliteConnection = sqlite3.connect(filePath)
            cursor = sqliteConnection.cursor()        

            # Dictionary mapping words to specific SQL queries
            queryDict = {
                'NoFilter': "SELECT * FROM tasks",
                'FilterTasksByPriority': "SELECT * FROM tasks ORDER by priority DESC",
                'FilterTasksByComplexity': "SELECT * FROM tasks ORDER by complexity DESC",            
                'FilterTasksByRank': "SELECT * from tasks ORDER BY rank DESC",
                'FilterTasksByMostDelayedTasks': "SELECT * FROM tasks ORDER BY delay DESC",
                'FilterTasksByCriticality': "SELECT * FROM tasks WHERE (julianday(deadline) > julianday(date()))",
                'FilterTasksStatusActive': "SELECT * FROM tasks WHERE status = 'Active'",
                'FilterTasksStatusAborted': "SELECT * FROM tasks WHERE status = 'Aborted'",
                'FilterTasksStatusBlocked': "SELECT * FROM tasks WHERE status = 'Blocked'",
                'FilterTasksStatusDone': "SELECT * FROM tasks WHERE status = 'Done'",
                'FilterTasksbyDateCreated': "SELECT * FROM tasks ORDER BY created"      
            }

            # Query to fetch priority and delay from the tasks table
            query = queryDict.get(self.filtersCombobox.get(), None)       
            cursor.execute(query)
            rows = cursor.fetchall()     
            display_table(rows)          
        else:
            messagebox.showinfo("Attention!!!","Please select a value from the combobox before to apply a filter")

if __name__ == "__main__":
    app = TasksOrganizer()
    app.mainloop()