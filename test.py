from turtle import width
from InquirerPy import prompt
# from examples import *

from InquirerPy.validator import *
from prompt_toolkit.validation import Validator, ValidationError
import sqlite3
import models
import pandas as pd
import json 
from pyfiglet import Figlet
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
import orm_sqlite 
from colorama import *
import random
import datetime


f = Figlet()
console = Console()

print(Fore.CYAN,f.renderText('W E L C O M E  T O  C  L  A  R  O'))
# print(Fore.CYAN,f.renderText('C  L  A  R  O'))

# con = sqlite3.connect("db_file.sqlite3")
# cur = con.cursor()
# q = f'''CREATE TABLE IF NOT EXISTS tasks (
#     task_id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     start_date DATE,
#     due_date DATE,
#     status TINYINT NOT NULL,
#     priority TINYINT NOT NULL,
#     description TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# )'''
# cur.execute(q)






questions = [
    {
        'type': 'list',
        'name': 'user_option',
        'message': 'Welcome to claro,How do u want to use claro today?',
        'choices': ["Tasks","Users","Groups", "Meetings"]
    },

    # {
    #     'type': "input",
    #     "name": "a",
    #     "message": "Enter the first number",
    #     "validate": NumberValidator,
    #     "filter": lambda val: int(val)
    # },
    
    # {
    #     'type': "input",
    #     "name": "task_name",
    #     "message": "Enter the Task name",
    #     "validate": EmptyInputValidator,
    #     "filter": lambda val: str(val)
    # },


    # {
    #     'type': "input",
    #     "desc": "task_descripton",
    #     "message": "Enter the Task description",
    #     "validate": EmptyInputValidator,
    #     "filter": lambda val: str(val)
    # },


]

def Tasks():
    list_ques=[
            {
                'type': 'list',
                'name': 'user_option',
                'message': 'Choose an option to perform a task',
                'choices': ["Create","View","Update","Delete","Go back to the main menu"]
            },
        ]
    answers = prompt(list_ques)
    if answers.get("user_option") == "Create":
        task_add = [
            {
                'type': "input",
                "name": "task_name",
                "message": "Enter the Task name",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            },
            {
                'type': "input",
                "name": "task_desc",
                "message": "Enter the Task description",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            },
            {
                'type': "list",
                "name": "task_start",
                "message": "Choose when to start the task - ",
                'choices':['Now', 'Later']
            },
        ]
        answers = prompt(task_add)
        name = answers.get('task_name')
        desc = answers.get('task_desc')
        task_start = answers.get('task_start')
        if task_start == 'Now':
            end_dates = [
                {
                    'type': "input",
                    "name": "end_date",
                    "message": "Enter the End date (optional)",
                    
                },
            ]
            end_date_answers = prompt(end_dates)
            end_date = end_date_answers.get('end_date')
            models.Tasks.create(title=name,status='Pending',priority='priority',description=desc,start_date=datetime.datetime.today(),due_date=end_date)
        elif task_start == 'Later':
            models.Tasks.create(title=name,status='Pending',priority='priority',description=desc)

        print(Back.GREEN,'*** Task created successfully ***')
        print(Style.RESET_ALL)
        
    elif answers.get("user_option") == "Delete":
        Delete()
    elif answers.get("user_option") == "View":
        List()
    elif answers.get("user_option") == "Update":
        Update()
    elif answers.get("user_option") == "Go back to the main menu":
        MainMenu()
    PreviousActions('tasks','Tasks')
   

def PreviousActions(actiontype,modeltype):
    list_ques=[
            {
                'type': 'list',
                'name': 'user_option',
                'message': 'Choose an action',
                'choices': ["Go back to the previous menu","Go back to the main menu"]
            },
        ]
    answers = prompt(list_ques) 
    if modeltype == 'Tasks':
        if answers.get("user_option") == "Go back to the previous menu":
            if actiontype == 'tasks' :
                Tasks()
            elif actiontype == 'lists':
                List()
        elif answers.get("user_option") == "Go back to the main menu":
            MainMenu()
    elif modeltype == 'Groups':
        if answers.get("user_option") == "Go back to the previous menu":
            if actiontype == 'tasks' :
                Groups()
           
        elif answers.get("user_option") == "Go back to the main menu":
            MainMenu()
    
def MainMenu():
    main()    

def DeleteConfirm(id):
    task_delete_confirm =[
        {
            'type': "input",
            "name": "confirm",
            "message": "Are you sure, want to delete the task (y/N):",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        }
    ]
    task_delete_confirm_prompt = prompt(task_delete_confirm)
    task_confirm_data = task_delete_confirm_prompt.get('confirm')
    # print(task_confirm_data,'afsdf')
    modal = models.Tasks
    if task_confirm_data == 'y':
        try:
            task = modal.get(modal.task_id == id)
            task.delete_instance() 
            # task = modal.select().filter(modal.task_id == id)
            print(Fore.GREEN,'Task deleted suceesfully',task)
            print(Style.RESET_ALL)
        
        except:
            # task = 'No Task matched with this task ID'
            # console.print(Fore.RED,'Something went wrong, Please try again....')
            console.print(Fore.RED,'Given task id does not exist, please try again')
            
    elif task_confirm_data == 'N':
        console.print(Fore.BLUE,'Given task is not deleted')
    else:
        print(Fore.RED,'Please enter (y/N), to confirm the deletion')
        task_delete_confirm_prompt = prompt(task_delete_confirm)    

def UpdateConfirm(id,task_column,task_update_data):
    task_update_confirm =[
        {
            'type': "input",
            "name": "confirm",
            "message": "Are you sure, want to update the task status (y/N):",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        }
    ]
    task_update_confirm_prompt = prompt(task_update_confirm)
    task_confirm_data = task_update_confirm_prompt.get('confirm')
    task_confirm_data.capitalize()
    modal = models.Tasks
    if task_confirm_data == 'Y':
        # try:
        task = modal.get(modal.task_id == id)
        if task_column == 'Status':
            task.status = task_update_data
        elif task_column == 'Start Date':
            task.start_at = task_update_data
        elif task_column == 'End Date':
            task.end_at = task_update_data
        task.save()
        
        # task = modal.select().filter(modal.task_id == id)
        print(Fore.GREEN,'Task updated',task)
        print(Style.RESET_ALL)
        
        # except:
        #     # task = 'No Task matched with this task ID'
        #     # console.print(Fore.RED,'Something went wrong, Please try again....')
        #     print(Fore.RED,'Given task id does not exist, please try again')
            
    elif task_confirm_data == 'N':
        print(Fore.BLUE,'Given task status is not updated')
    else:
        print(Fore.RED,'Please enter (y/N), to confirm the updation')
        task_update_confirm_prompt = prompt(task_update_confirm)
    PreviousActions('tasks','Tasks')

def Delete():
    task_delete =[
    {
       'type': "input",
        "name": "task_id",
        "message": "Enter the Task ID",
        "validate": EmptyInputValidator(),
        "filter": lambda val: str(val)
    }
   ]
    response = []
    task_lst = models.Tasks.select()
    for l in task_lst.dicts():
        response.append(l)
    console = Console()
    print(Fore.BLUE,'Please select the task id from the below list to delete a task')
    user_renderables = [Panel(get_content(user), expand=True) if user["status"] == 'Pending' or user["status"] == 'Completed' else '' for user in response]
    console.print(Columns(user_renderables))


    answers = prompt(task_delete)
    id = int(answers.get('task_id'))

    task_delete_confirm =[
        {
            'type': "input",
            "name": "confirm",
            "message": "Are you sure, want to delete the task (y/N):",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        }
    ]
    task_delete_confirm_prompt = prompt(task_delete_confirm)
    task_confirm_data = task_delete_confirm_prompt.get('confirm')
    # print(task_confirm_data,'afsdf')
    modal = models.Tasks
    if task_confirm_data == 'y':
        try:
            task = modal.get(modal.task_id == id)
            task.delete_instance() 
            # task = modal.select().filter(modal.task_id == id)
            print(Fore.GREEN,'Task deleted suceesfully',task)
            print(Style.RESET_ALL)
        
        except:
            # task = 'No Task matched with this task ID'
            # console.print(Fore.RED,'Something went wrong, Please try again....')
            print(Fore.RED,'Given task id does not exist, please try again')
            
    elif task_confirm_data == 'N':
        print(Fore.BLUE,'Given task is not deleted')
    else:
        print(Fore.RED,'Please enter (y/N), to confirm the deletion')
        # task_delete_confirm_prompt = prompt(task_delete_confirm) 
        DeleteConfirm(id)
    PreviousActions('tasks','Tasks')

def List():
    list_ques=[
            {
                'type': 'list',
                'name': 'user_res',
                'message': 'Choose options to GET tasks list',
                'choices': ["All","Completed","Pending","Go back to the previous menu","Go back to the main menu"]
            },
        ]
    answers = prompt(list_ques)
    res = answers.get('user_res')
    response = []
    task_lst = models.Tasks.select()
    for l in task_lst.dicts():
        response.append(l)
    console = Console()
 
    if res == 'All':
        user_renderables = [Panel(get_content(user), expand=True) if user["status"] == 'Pending' or user["status"] == 'Completed' else '' for user in response]
        console.print(Columns(user_renderables))
    elif res == 'Completed':
        user_renderables = [Panel(get_content(user), expand=True) if user["status"] == 'Completed' else '' for user in response]
        console.print(Columns(user_renderables))
    elif res == 'Pending':
        user_renderables = [Panel(get_content(user), expand=True) if user["status"] == 'Pending' else '' for user in response]
        console.print(Columns(user_renderables))
    elif res == 'Go back to the previous menu':
        Tasks()
    elif res == 'Go back to the main menu':
        MainMenu()
    PreviousActions('lists','Tasks')

def ViewGroups():
   
    response = []
    task_lst = models.Groups.select()
    for l in task_lst.dicts():
        response.append(l)
    console = Console()
 
    
    user_renderables = [Panel(get_content_group(user), expand=True) if user["status"] == 'Pending' or user["status"] == 'Completed' else '' for user in response]
    console.print(Columns(user_renderables))
    
    PreviousActions('tasks','Groups')

def Update():
    task_update =[
        {
            'type': "input",
            "name": "task_id",
            "message": "Enter the Task ID",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        }
   ]
    task_update_column =[
        {
            'type': "list",
            "name": "task_column",
            "message": "What do you want to update?",
            "choices":['Status','Start Date','End Date'],
        }
   ]
    response = []
    task_lst = models.Tasks.select()
    for l in task_lst.dicts():
        response.append(l)
    console = Console()
    print(Fore.BLUE,'Please select the task id from the below list to update a task status')
    user_renderables = [Panel(get_content(user), expand=True) if user["status"] == 'Pending' or user["status"] == 'Completed' else '' for user in response]
    console.print(Columns(user_renderables))


    answers = prompt(task_update)
    id = int(answers.get('task_id'))

    task_update_column_answer = prompt(task_update_column)
    task_column= task_update_column_answer.get('task_column')

    if task_column == 'Status':
       
        task_update_column_enter =[
            {
                'type': "list",
                "name": "task_status",
                "message": "Change the task status to - ",
                "choices":['Pending','Completed'],
            }
        ]
        task_update_status = prompt(task_update_column_enter)
        task_update_data= task_update_status.get('task_status')
    elif task_column == 'Start Date':
        task_update_column_enter =[
            {
                'type': "input",
                "name": "task_start_date",
                "message": "Enter the Start Date",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            }
        ]
        task_update_status = prompt(task_update_column_enter)
        task_update_data= task_update_status.get('task_start_date')
    elif task_column == 'End Date':
        task_update_column_enter =[
            {
                'type': "input",
                "name": "task_end_date",
                "message": "Enter the End Date",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            }
        ]
        task_update_status = prompt(task_update_column_enter)
        task_update_data = task_update_status.get('task_end_date')

    task_update_confirm =[
        {
            'type': "input",
            "name": "confirm",
            "message": "Are you sure, want to update the task status (y/N):",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        }
    ]
    task_update_confirm_prompt = prompt(task_update_confirm)
    task_confirm_data = task_update_confirm_prompt.get('confirm')
    task_confirm_data = task_confirm_data.capitalize()
    print(task_confirm_data,'afsdf')
    modal = models.Tasks
    if task_confirm_data == 'Y':
        # try:
        task = modal.get(modal.task_id == id)
        if task_column == 'Status':
            task.status = task_update_data
        elif task_column == 'Start Date':
            task.start_date = task_update_data
        elif task_column == 'End Date':
            task.due_date = task_update_data
        task.save()
        
        tasksss = modal.select().filter(modal.task_id == id)
        print(tasksss,'fdsgfgsfdf')
        print(Fore.GREEN,'Task updated',task)
        print(Style.RESET_ALL)
        
        # except:
        #     # task = 'No Task matched with this task ID'
        #     # console.print(Fore.RED,'Something went wrong, Please try again....')
        #     print(Fore.RED,'Given task id does not exist, please try again')
            
    elif task_confirm_data == 'N':
        print(Fore.BLUE,'Given task status is not updated')
    else:
        print(Fore.RED,'Please enter (y/N), to confirm the updation')
        # task_delete_confirm_prompt = prompt(task_delete_confirm) 
        UpdateConfirm(id,task_column,task_update_data)
    PreviousActions('tasks','Tasks')

def get_content(user):
       
    """Extract text from user dict."""
    title = user["title"].upper()
    t_id = user["task_id"]
    desc = f"{user['description']}"
    status = user["status"]
    start_date = user["start_date"]
    end_date = user["due_date"]
    if status == 'Pending':
        color = 'red'
    elif status == 'Completed':
        color = 'green'
    return f"[b][yellow]{t_id}.{title}[/b]\n[white]{desc}\n[i][{color}]{status}\n[blue]{start_date} to {end_date}"

def get_content_group(user):
   
    """Extract text from user dict."""
    title = user["title"].upper()
    t_id = user["group_id"]
    desc = f"{user['description']}"
    # status = user["status"]
    
    # if status == 'Pending':
    #     color = 'red'
    # elif status == 'Completed':
    #     color = 'green'
    return f"[b][yellow]{t_id}.{title}[/b]\n[white]{desc}"
   


def Groups():
    list_ques=[
        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Choose an option to perform an action on Groups',
            'choices': ["Create","View","Update","Delete","Go back to the main menu"]
        },
    ]
    
    answers = prompt(list_ques)
    if answers.get("user_option") == "Create":
        grp_add = [
            {
                'type': "input",
                "name": "grp_name",
                "message": "Enter the Group name",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            },
            {
                'type': "input",
                "name": "grp_desc",
                "message": "Enter the description",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            },
            {
                'type': "list",
                "name": "grp_add_users",
                "message": "Want to add users to the group, choose an option - ",
                'choices':['Add Now', 'Add Later']
            },
        ]
        answers = prompt(grp_add)
        name = answers.get('grp_name')
        desc = answers.get('grp_desc')
        grp_add_users = answers.get('grp_add_users')
        if grp_add_users == 'Add Now':
            pass
        elif grp_add_users == 'Add Later':
            models.Groups.create(title=name,status='Pending',priority='priority',description=desc)

        print(Back.GREEN,'*** Group created successfully ***')
        print(Style.RESET_ALL)
        
    # elif answers.get("user_option") == "Delete":
    #     Delete()
    elif answers.get("user_option") == "View":
        ViewGroups()
    # elif answers.get("user_option") == "Update":
    #     Update()
    elif answers.get("user_option") == "Go back to the main menu":
        MainMenu()
    PreviousActions('tasks','Groups')
   



def main():
    # answers = prompt(questions, style=custom_style_3)
    answers = prompt(questions)

    if answers.get("user_option") == "Tasks":
        Tasks()
    elif answers.get("user_option") == "Users":
        Delete(a, b)
    elif answers.get("user_option") == "Groups":
        Groups()
    elif answers.get("user_option") == "Meetings":
        Update(a, b)


if __name__ == "__main__":
    main()



    