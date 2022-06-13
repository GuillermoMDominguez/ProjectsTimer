# -*- coding: utf-8 -*-
"""
Created on Sat May 14 17:55:49 2022

@author: guill
"""
#Requires Python 3.7+
from dataclasses import dataclass
from typing import List
from datetime import datetime,timedelta
import os
import sys

"""
Data container for the project information, we only save seconds worked,
and generate a human-friendly description only when asked
The data is simple enough that can be serialized with the format:
    {name}:{seconds}
"""
@dataclass
class Project:
    name: str
    seconds: int
    
    def getPrintout(self) -> str:
        return f"{self.name}: {str(timedelta(seconds=self.seconds))}"
    def toString(self) -> str:
        return f"{self.name}:{self.seconds}"
    def fromString(data : str): #Returns a new instance of project
        name,seconds = data.split(':',1)
        return Project(name,int(float(seconds)))
"""
Class that manages a list of projects, encapsulates access to current working projects
and is in charge of updating their information
"""  
class ProjectManager:
    projects: List[Project]
    
    def __init__(self,projects : List[Project]):
        self.projects = projects
    
    def NewProject(self,name : str) -> None:
        p = Project(name,0)
        self.projects.append(p)
        
    def DeleteProject(self,name : str) -> None:
        self.projects = [p for p in self.projects if p.name != name]
        
    def CheckForProject(self,name : str) -> bool:
        return next((True for x in self.projects if x.name == name),False)
    
    def AddTimeToProject(self,name : str,seconds : int) -> None:
        p = next((p for p in self.projects if p.name == name),None)
        if p:
            p.seconds += seconds
            
    def GetPrintList(self) -> List[str]:
        prints = []
        for p in self.projects:
            prints.append(p.getPrintout())
        return prints
    
    def GetProjectPrintout(self,name : str) -> str:
        return next((x.getPrintout() for x in self.projects if x.name == name),'Not found')
    
    def GetSaveList(self) -> List[str]:
        return [p.toString() for p in self.projects]
"""
#Functions to save and restore state, the project manager generates a list
#with the string representation of every project, and this functions use
#this informations to recover the state
#Note that we don't save fractions of a second worked
"""
def SaveProjects(manager : ProjectManager):
    projects = manager.GetSaveList()
    try:
        f = open('Projects.data','w')
        print("Recording session")
        for p in projects:
            f.write(p + '\n')
        print("Saving complete!")
    except OSError as e:
        print("Error on saving process, the work session could not be recorded")
        print(e)
    finally:
        f.close()
def RestoreProjects() -> ProjectManager:
    projects = []
    if os.path.exists('Projects.data'):
        try:
            f = open('Projects.data','r')
            print("Restoring projects")
            for line in f:
                projects.append(Project.fromString(line))
            print("Projects restored")
        except OSError as e:
            print("Error restoring projects, starting clean session")
            print(e)
            projects = []
        finally:
            f.close()
    return ProjectManager(projects)

def main():
    #We restore current projects or initialize clean session
    manager = RestoreProjects()
    
    #REPL, process input one line at a time
    keepRunning = True
    while keepRunning:
        line : str = input('>')
        verb,*args = line.split(' ',1)
        if verb == "quit":
            keepRunning = False
        elif verb == "new":
            if not(args):
                print('Expected name of new project')
            else:
                name : str = args[0].replace(' ','_')
                manager.NewProject(name)
        elif verb == 'print':
            if not(args):
                print('Expected name of project or all')
            else:
                p = args[0]
                if p == 'all':
                    print(manager.GetPrintList())
                else:
                    print(manager.GetProjectPrintout(args[0]))
        elif verb == "start":
            if not(args):
                print("Expected name of the project to work in")
            elif not(manager.CheckForProject(args[0])):
                print("Unknown project name, use view all to see current projects")
            else:
                start = datetime.now()
                done = False
                name = args[0]
                print(f"Started working on project {name}")
                while not(done):
                    line = input()
                    if line == 'stop':
                        print(f"Stopping work on project {name}")
                        done = True
                    else:
                        print("Unknown command, to stop current project use command stop")
                end = datetime.now()
                delta = end - start
                seconds_worked = delta.total_seconds()
                manager.AddTimeToProject(name, seconds_worked)
        elif verb == "delete":
            name = args[0]
            if not(name):
                print("Expected name of project to delete")
            elif not(manager.CheckForProject(name)):
                print(f"Unknown project '{name}'")
            else:
                confirm = input("This will delete any saved data on the project, Continue?[Y/n]")
                if confirm.upper() == "Y":
                    manager.DeleteProject(name)
        elif verb == "panic": #Exit without recording current session
            confirm = input("Exiting current session without saving, are you sure? [Y/n]")
            if confirm.upper() == "Y":
                sys.exit("Panic'ed")
        elif verb == "help":
            print("Project Watch 1.0\nValid commands:\n \tnew [name] -> Creates new project with name=[name]\n\
 \tstart [name] -> Start recording work on project [name]\n\
 \tprint [all/name] -> Prints information on either all projects or a specific project\n\
 \tdelete [name] -> Deletes project info, NOT UNDOABLE\n\
 \thelp -> Shows this help info\n\
 \tquit -> Saves changes and exits program\n\
 \tpanic -> Exit program without saving, so changes are lost")
        else:
            print(f"Unknown command {verb}{args}, use help to see available commands")
    #Save session changes and exit program
    SaveProjects(manager)
    print("Bye!")
    

if __name__ == "__main__":
    main()
else:
    print("This is a CLI application, meant to be run independently")