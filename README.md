# TasksOrganizer
This application will support you to keep on track your daily tasks, show you the best way to approach them 

Introduction

The main idea is create an app that you can list and organize your daily tasks (personal and professional), with a low effort however with a good traceability and organization, something simple like create comments in the "Notepad", but 
with a big impact to manage these tasks, especially because can be combined with different organization techniques (is more one tool in your tool box set).
Basically the app is a Database, organized in a logic way that you can include the tasks and can classify based on their priority in your life, complexity (how long time you need to dedicate on) and focused to accomplish the due date, the most interest part is create a weight matrix/algorithm that based on these info be able to ranking the tasks and suggest an order to approach them in a efficient way.

Some basic requirements for this project are:

Run in Windows and Linux
Don't need to install (just a simple executable file)
Be simple and effective, do not overcomplicate and able to offer you suggestions

What you will find in each folder:
Code: Project Code (Python scripts, configuration file)
DevEnvironment: The requirements.txt will help you to install all you need in your Python environment
ProjectManagement: Excel sheet that I describe how it works the wheight matrix, SW requirements and Backlog to tracking the SW improvements, bug fixes and etc...

To start in this project:

1 - Download all the softwares

2 - Install Python, pip and VSCode  

3 - Install git

4 - Clone the project from github

5 - Start to use and develop




Python (Code language)

To download Python:

https://www.python.org/downloads/



Install pip:

To install from the file using pip:

python3 -m pip install -r requirements.txt



Install Virtual Environment:

How to create a Virtual Environment:

https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments



Git (Software Version Control)

To install git

https://git-scm.com/downloads



Software Development (Tool to coding)

Install Visual Code Studio:

https://code.visualstudio.com/download



To manipulate the database during the app development I suggest you to use:

https://sqlitebrowser.org/dl/




How to use the app (The Graphic Interface):


1 - Press "Create A New Database", give a name for this new database 

2 - Press "Open Database" and point the database that you already created to unlock the tabs: Tasks Management, Filters, Statistics


Tasks Management: 


- Include New Task: Include a new task, just fill the fields properly

- Edit Task: Here you can edit the task, when you want to change the status from "Active" to "Done" use this feature

- Update Rank: When you want to force the system to calculate the rank value, in general you don't need to use this button because when you include a new task or edit it runs automatically, however if you do this manually directly to the database you will need to update the rank calculation

- Generate Daily Task List: You create a list with 5 tasks, 1 is the "Eat the frog" and 4 are tasks with highest rank (this is calibratable, there is a file to do it)

- List Dependencies: Will list all the tasks with dependence 


Filters:


You can define in "Filters" a specific filter that you want to apply and press "Show The List With Filter Applied"


Statistics: 


You can generate a Pizza Graph with the app statistics
