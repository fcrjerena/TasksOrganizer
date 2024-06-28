import sqlite3              #Importing Sqlite3 Module
from datetime import date   #to have the function date available in my code
#import datetime
import traceback            #treat error
import sys                  #treat error
import yaml
#Graphic solution
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg',force=True)      #I put this but I still have the problem...
from matplotlib import pyplot as plt
import numpy as np
from dataclasses import dataclass  
import os.path  #To save file
import os
import tkinter as tk
from tkinter import filedialog

#Dictionaries to use with a Visual User Interface
priority_list = {"Very_Low":1, 
				 "Low":2,
				 "Medium":3,
				 "High":5,
				 "Very_High":8} 
  
complexity_list = {"Super_Slow":1, 
				   "Slow":2, 
				   "Medium":3, 
				   "Fast":5, 
				   "Super_Fast":8}   

#The order can't be changed because it is important in createGraphic() function 
status_list = ('Aborted','Active','Blocked','Done')

@dataclass
class task:
	def __init__(self, id, label, description, priority, complexity, deadline, main_task_id, blockers):
		self.id = id                                    #ID will be included automatically by SQLite query...
		self.label = label                              #Text that describe the task that should be done
		self.description = description					#Task description
		self.priority = priority                        #Define the task priority
		self.complexity = complexity                    #Define the task complexity (how fast you can perform the task)
		self.deadline = deadline						#Limit to finish the task
		self.main_task_id = main_task_id                #This task should be closed before to attend the MainTask
		self.blockers = blockers                        #Text to describe what is blocking the task (provide info to close the task)
		self.created = date.today()                     #Date that the task was included in the table		
		self.delay = 0                                  #How delayed the task in relation when it was opened
		self.rank = 0                                   #Rank to classify which order the task should be treated		
		self.status = "Active"                          #Task status (to understand what needs to be done)
		self.comments = None                            #It should use when you finished the task or as you want

def createNewDatabase(name):
	global sqliteConnection, cursor

	name = name + ".db"
	# Making a connection between sqlite3 
	# database and Python Program
	sqliteConnection = sqlite3.connect(name)
		
	# If sqlite3 makes a connection with python
	# program then it will print "Connected to SQLite"
	# Otherwise it will show errors
	print("Connected to SQLite")

	# Getting all tables from sqlite_master
	query = """SELECT name FROM sqlite_master  
  	WHERE type='table';"""

	# Creating cursor object using connection object
	cursor = sqliteConnection.cursor()
	
	# executing our sql query
	cursor.execute(query)
	print("List of tables\n")
	
	# printing all tables list
	print(cursor.fetchall())

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
	sqliteConnection.commit() 

def includeNewTask(conn, task):
	query = '''INSERT OR IGNORE INTO tasks
			  (label,description,priority,complexity,deadline,main_task_id,blockers,created,delay,rank,status,comments)		
              VALUES (?,?,?,?,?,?,?,?,?,?,?,?);			  	  
              '''
	cursor = conn.cursor()
	cursor.execute(query, task)
	conn.commit()

def updateTask(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    query = ''' UPDATE tasks
              SET 
			  	  label = ?,
				  description = ?,
				  priority = ?,
				  complexity = ?,	
				  deadline = ?,		  
				  main_task_id = ?,			  				  
				  blockers = ?,
				  created = ?,
				  delay = ?,
				  rank = ?,
				  status = ?,
				  comments = ?
              WHERE id = ?'''
	
    cursor = conn.cursor()

	# Execute the query
    cursor.execute(query, task)

    conn.commit()

def activeTasks():
    query = """
    SELECT * FROM tasks WHERE status = "Active");
    """   
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    activeTasks = cursor.fetchall()  

    return activeTasks	

def blockedTasks():
    query = """
    SELECT * FROM tasks WHERE status = "Blocked");
    """   
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    blockedTasks = cursor.fetchall()  

    return blockedTasks	

def abortedTasks():
    query = """
    SELECT * FROM tasks WHERE status = "Aborted");
    """   
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    abortedTasks = cursor.fetchall()  

    return abortedTasks	

def doneTasks():
    query = """
    SELECT * FROM tasks WHERE status = "Done");
    """   
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    doneTasks = cursor.fetchall()  

    return doneTasks

def mostDelayedTasks():
    query = """
    SELECT * FROM tasks WHERE status = "Active" ORDER BY delay DESC);
    """   
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    mostDelayedTasks = cursor.fetchall()  

    return mostDelayedTasks	

def sortTasksByRank():
	query = "SELECT * from tasks ORDER BY rank DESC"

	# Execute the query	
	cursor.execute(query)
	
	# Fetch all results
	sortTasksByRank = cursor.fetchall()
	
	return sortTasksByRank	

def getTasksWithMainTaskIdNotNull():
    query = """
    SELECT * FROM tasks
    WHERE ((main_task_id IS NOT NULL) AND (status = "Active" OR status = "Blocked"));
    """  
	
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    tasksWithMainTaskIdNotNull = cursor.fetchall()  

    return tasksWithMainTaskIdNotNull

def getCorrespondingTasks(mainTaskIds):
    query = f"""
    SELECT * FROM tasks
    WHERE id IN ({','.join(['?']*len(mainTaskIds))});
    """

    # Execute the query
    cursor.execute(query, mainTaskIds)
    
    # Fetch all results
    correspondingTasks = cursor.fetchall()   
    
    return correspondingTasks

def printDependencies():
	# Get tasks with main_task_id not null
	tasksWithMainTaskId = getTasksWithMainTaskIdNotNull()
	
	# Extract the mainTaskIds
	mainTaskIds = [task[6] for task in tasksWithMainTaskId]  # Assuming main_task_id is the third column
    
    # Get corresponding tasks
	correspondingTasks = getCorrespondingTasks(mainTaskIds)
    
    # Print the results
	print("\nTasks with main_task_id is not null:")	
	for task in tasksWithMainTaskId:
		print(task)

	print("\nCorresponding tasks with IDs in main_task_id:")
	for task in correspondingTasks:
		print(task)

def getProfileSettings(profileName):
	script_dir = os.path.dirname(__file__)
	config_path = os.path.join(script_dir, 'config.yaml')

	#Load configuration from YAML file
	with open(config_path, 'r') as file:
		config = yaml.safe_load(file)
	
	profiles = config.get('profiles', {})
	return profiles.get(profileName, {})

def updateRules(profileName):	
	#Open the yaml file with the configuration
	profileSettings = getProfileSettings(profileName)
	if not profileSettings:
		raise ValueError(f"Profile '{profileName}' not found in the configuration.")

	#Recovery the information from the yaml file
	weights = profileSettings.get('weights', {})
	weightPriority = weights.get('priority', None)
	weightComplexity = weights.get('complexity', None)
	weightDelay = weights.get('delay', None)
	relevanceOffset = profileSettings.get('relevance_offset', None) #When you passed the deadline
	deadlineSlope = profileSettings.get('deadline_slope', None) #prioritize tasks with deadline
	
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

	# Executing the query with the weight variables
	cursor.execute(query, (weightPriority, weightComplexity, weightDelay, relevanceOffset, deadlineSlope))

	# Committing the transaction
	sqliteConnection.commit()

def getTasks(profileName): 
	#Open the yaml file with the configuration
	profileSettings = getProfileSettings(profileName)
	if not profileSettings:
		raise ValueError(f"Profile '{profileName}' not found in the configuration.")

	#Recovery the information from the yaml file
	tasklist = profileSettings.get('tasklist', {})
	ToDo = tasklist.get('ToDo', None)
	EatTheFrog = tasklist.get('EatTheFrog', None)
	number = ToDo + EatTheFrog  
	number = str(number)
	
    # SQL query to select tasks with status "Active" and order by rank in descending order
	query = '''
        SELECT * FROM tasks
        WHERE Status = 'Active'
        ORDER BY Rank DESC
        LIMIT ?
    '''
	
	cursor = sqliteConnection.execute(query,number)
	
	# Fetch all results
	tasks = cursor.fetchall()
    
    # Close the connection
    #sqliteConnection.close()
	return tasks

def categorizeTasks(tasks):
    categorizedTasks = {
        "Eat the frog": [],
        "List daily to do": []
    }
    
    if tasks:
		#Here, I should include a code that can create something like tasks[0:x] and tasks[x:]
        categorizedTasks["Eat the frog"].append(tasks[0])  # The highest rank task
        categorizedTasks["List daily to do"] = tasks[1:]   # The rest of the tasks
    
    return categorizedTasks

def getMainTasks(taskIds):
    cursor = sqliteConnection.cursor()

    # Create a string with placeholders for each task_id
    placeholders = ','.join(['?'] * len(taskIds))

    # SQL query to select tasks where ID matches any in the taskIds list
    cursor.execute(f'''
        SELECT * FROM tasks
        WHERE ID IN ({placeholders})
    ''', taskIds)
    
    # Fetch all results
    mainTasks = cursor.fetchall()   
    
    return mainTasks

def createDailyList(profileName):
	tasks = getTasks(profileName)
	categorizedTasks = categorizeTasks(tasks)
	
	print("\nEat the frog")
	for task in categorizedTasks["Eat the frog"]:
		print(task)
	
	print("\nList daily to do:")
	for task in categorizedTasks["List daily to do"]:
		print(task)
		
	# Check for main_task_id and fetch corresponding main tasks
	mainTaskIds = [task[6] for task in tasks if task[6] is not None]
	if mainTaskIds:
		mainTasks = getMainTasks(mainTaskIds)
	
		print("\nDependencies:")
		for mainTask in mainTasks:
			print(mainTask)	

def createGraphic(title):
	#Create a figure with two subplots
	fig, (ax1, ax2) = plt.subplots(1, 2)
	graph_title = 'Information about task database: ' + title
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
	if y[0] == (0,):
		tuple_read.append(1) 
		graph2list.append(1)
		graph2list.append(37)
	else:	
		tuple_read = y[0]
		graph2list.append(tuple_read[0])
		graph2list.append(graph1list[1]-graph2list[0])	
	
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

def listDailyToDo(file_name):
	cursor.execute("SELECT * FROM tasks WHERE (status = 'Active') ORDER BY rank DESC LIMIT 5;")
	response = cursor.fetchall()
	
	#Create a new file .txt
	f= open(file_name,"w+")

	#Title
	f.write("Most important - My list of tasks ("+str(date.today())+"): \r\n")  
	f.write("[ID][Label]                              [Description]\r\n")     

	for n in range(len(response)):
		internalTuples = response[n]
		rowEdited = "["+str(internalTuples[0])+"]["+internalTuples[1]+"] -> "+internalTuples[2]+"\r"		
		f.write(rowEdited)

	f.close()
	#os.system("notepad.exe " + file_name)

def saveAsDialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(title="Save As", defaultextension=".txt",
                                             filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    return file_path

#Terminal input
try:		
	ans = True
	while ans:
		print("Which database you want to run and update:\r\n")		
		print("1.Personal Database")
		print("2.Professional Database")
		print("3.Do both 1 & 2")
		print("4.Create a new one")
		print("5.Exit/Quit\r\n")
    	
		ans = input("What would you like to do?")

		if ans=="1":
			createNewDatabase("PersonalTasksList")
			updateRules('Personal')				
			createDailyList('Personal')
			#printDependencies()									
			listDailyToDo("ToDo_Personal.txt")
			createGraphic("Personal")
			ans = None
		elif ans=="2":
			createNewDatabase("ProfessionalTasksList")
			updateRules('Professional')		
			createDailyList('Professional')	
			#printDependencies()			
			listDailyToDo("ToDo_Professional.txt")
			createGraphic("Professional")
			ans = None
		elif ans=="3":
			#Start 1
			createNewDatabase("PersonalTasksList")
			updateRules('Personal')				
			createDailyList('Personal')
			#printDependencies()									
			listDailyToDo("ToDo_Personal.txt")
			createGraphic("Personal")
			#Start 2
			createNewDatabase("ProfessionalTasksList")
			updateRules('Professional')		
			createDailyList('Professional')	
			#printDependencies()			
			listDailyToDo("ToDo_Professional.txt")
			createGraphic("Professional")
			ans = None
		elif ans=="4":
			databaseName = input("New Database Name?")
			#save_path = 'C:/Users/fjerena/Documents/FabioPythonDevelopment/'
			save_path = saveAsDialog()
			completeName = os.path.join(save_path, databaseName + ".db") 			
			createNewDatabase(databaseName)			
			ans = None
		elif ans=="5":
			print("\n Goodbye")
			ans = None
		else:
			print("\n Not Valid Choice Try again")		

except sqlite3.Error as error:
	print("Failed to execute the above query", error)  #Should I keep this line???
	"""
	print("Failed to insert data into sqlite table")
	print("Exception class is: ", error.__class__*)
	print("Exception is", error.args)
	print('Printing detailed SQLite exception traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))
	"""
	
finally:
	# Inside Finally Block, If connection is
	# open, we need to close it
	if sqliteConnection:
		
		# using close() method, we will close 
		# the connection
		sqliteConnection.close()
		
		# After closing connection object, we 
		# will print "the sqlite connection is 
		# closed"
		print("The SQlite connection is closed!")

		plt.show()