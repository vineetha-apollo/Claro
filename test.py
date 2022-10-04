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


f = Figlet()
console = Console()
print(Fore.CYAN,f.renderText('C  L  A  R  O'))

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
        ]
        answers = prompt(task_add)
        name = answers.get('task_name')
        desc = answers.get('task_desc')
        models.Tasks.create(title=name,status='Pending',priority='priority',description=desc)
        print(Back.GREEN,'*** task created successfully ***')
        print(Style.RESET_ALL)
        
    elif answers.get("user_option") == "Delete":
        Delete()
    elif answers.get("user_option") == "View":
        List()
    elif answers.get("user_option") == "Update":
        Update()
    elif answers.get("user_option") == "Go back to the main menu":
        MainMenu()
    PreviousActions('tasks')
   

def PreviousActions(actiontype):
    list_ques=[
            {
                'type': 'list',
                'name': 'user_option',
                'message': 'Choose an action',
                'choices': ["Go back to the previous menu","Go back to the main menu"]
            },
        ]
    answers = prompt(list_ques) 
    if answers.get("user_option") == "Go back to the previous menu":
        if actiontype == 'tasks' :
            Tasks()
        elif actiontype == 'lists':
            List()
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
    PreviousActions('tasks')

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
    PreviousActions('lists')

def Update(a, b):
    print(a / b)

def get_content(user):
   
    """Extract text from user dict."""
    title = user["title"].upper()
    t_id = user["task_id"]
    desc = f"{user['description']}"
    status = user["status"]
    if status == 'Pending':
        color = 'red'
    elif status == 'Completed':
        color = 'green'
    return f"[b][yellow]{t_id}.{title}[/b]\n[white]{desc}\n[i][{color}]{status}"
   
def main():
    # answers = prompt(questions, style=custom_style_3)
    answers = prompt(questions)

    if answers.get("user_option") == "Tasks":
        Tasks()
    elif answers.get("user_option") == "Users":
        Delete(a, b)
    elif answers.get("user_option") == "Groups":
        List(a, b)
    elif answers.get("user_option") == "Meetings":
        Update(a, b)


if __name__ == "__main__":
    main()



    