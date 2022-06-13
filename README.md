# Projects Watch
A minimal CLI tool for keeping track of time spend on sideprojects. Works with Python 3.7+

# Usage
Run this tool with python3 on the command line, type "help" to see available commands. Type "new (name of project)" to
start a new project, then use "start (name of project)" to start tracking the time spent while working. Once finished, type
"stop" to stop the timer, and quit to save your session. The project data is saved locally on a "Projects.data" file, in the same
directory where the tool is run.

# Valid commands:
*new (name)*: Creates new project with name=(name)  
*start [name]*: Start recording work on project [name]  
*print (all/name)*: Prints information on either all projects or a specific project  
*delete (name)*: Deletes project info, NOT UNDOABLE  
*help*: Shows available commands  
*quit*: Saves changes and exits program  
*panic*: Exit program without saving, so changes are lost  
