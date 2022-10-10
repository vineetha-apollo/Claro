from turtle import width
from InquirerPy import get_style
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
import ast


style1 = {
    "questionmark": "#ff0000",
    "answermark": "#e5c000",
    "answer": "#61afef",
    "input": "#98c379",
    "question": "#ffff00",
    "answered_question": "#aaaa55",
    "instruction": "#2222aa",
    "long_instruction": "#abb2bf",
    "pointer": "#3414bb",
    "checkbox": "#98c3c9",
    "separator": "",
    "skipped": "#5c6370",
    "validator": "",
    "marker": "#e5c07b",
    "fuzzy_prompt": "#c678dd",
    "fuzzy_info": "#abb2bf",
    "fuzzy_border": "#4b5263",
    "fuzzy_match": "#c678dd",
    "spinner_pattern": "#e5c07b",
    "spinner_text": "",
}


f = Figlet(font='alligator')
console = Console()

# print(Fore.CYAN,f.renderText('W E L C O M E  T O  C  L  A  R  O'))
print()
print(Fore.BLUE,f.renderText('C L  A R O'))
print(Fore.RESET)

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
        'message': 'Welcome to claro, How do u want to use claro today?',
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
    answers = prompt(list_ques,style=style1)
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
        answers = prompt(task_add,style=style1)
        name = answers.get('task_name')
        desc = answers.get('task_desc')
        task_start = answers.get('task_start')
        if task_start == 'Now':
            end_dates = [
                {
                    'type': "input",
                    "name": "end_date",
                    "message": "Enter the End date in YYYY-MM-DD (optional input)",
                    
                },
            ]
            end_date_answers = prompt(end_dates,style=style1)
            end_date = end_date_answers.get('end_date')
            if end_date :
                end_date = end_date
            else : 
                end_date = None
            models.Tasks.create(title=name,status='Pending',priority='priority',description=desc,start_date=datetime.datetime.today(),due_date=end_date)
        elif task_start == 'Later':
            models.Tasks.create(title=name,status='Pending',priority='priority',description=desc,start_date=None,due_date=None)

        print(Fore.GREEN,'******************* Task created successfully *******************')
        print(Fore.RESET)
        
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
    answers = prompt(list_ques,style=style1) 
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
            "message": "Are you sure, want to delete the task (Y/N):",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        }
    ]
    task_delete_confirm_prompt = prompt(task_delete_confirm,style=style1)
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
        task_delete_confirm_prompt = prompt(task_delete_confirm,style=style1)    

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
    task_update_confirm_prompt = prompt(task_update_confirm,style=style1)
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
        task_update_confirm_prompt = prompt(task_update_confirm,style=style1)
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
    print(Fore.RESET)
    user_renderables = [Panel(get_content(user), expand=True) if user["status"] == 'Pending' or user["status"] == 'Completed' else '' for user in response]
    console.print(Columns(user_renderables))


    answers = prompt(task_delete,style=style1)
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
    task_delete_confirm_prompt = prompt(task_delete_confirm,style=style1)
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
    answers = prompt(list_ques,style=style1)
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
    task_lst = models.Group.select()
    for l in task_lst.dicts():
        response.append(l)
    console = Console()
    user_renderables = [Panel(get_content_group(user), expand=True) if user["status"] == 'Pending' or user["status"] == 'Completed' else '' for user in response]
    console.print(Columns(user_renderables))
    show_user_prompt = [
        {
            'type' : 'input',
            'name' : 'show_users_list',
            'message' : 'Want to see the users in groups, enter a group id - ', 
            
        }
    ]
    user_list_prompt = prompt(show_user_prompt,style=style1)
    show_users_list = user_list_prompt.get('show_users_list')
    try:
        userslist = []
        modal = models.Group
        group_users = modal.get(modal.group_id == show_users_list)
        try:
            if group_users:
                console.print(Columns([Panel(user, expand=True) for user in group_users]))
        except:
            print(Fore.RED,'Oops!, No user found in this Group',end='')
            print(Fore.RESET)
    except:
        pass
    # user_grp_list = ast.literal_eval(group_users.user_ids)
    # console.print(Columns([Panel(user, expand=True) for user in user_grp_list]))

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
    print(Fore.RESET)
    user_renderables = [Panel(get_content(user), expand=True) if user["status"] == 'Pending' or user["status"] == 'Completed' else '' for user in response]
    console.print(Columns(user_renderables))


    answers = prompt(task_update,style=style1)
    id = int(answers.get('task_id'))
    try:
        id_1 = models.Tasks.get(models.Tasks.task_id == id)
    except:
        id_1 = None
    if id_1:
        task_update_column_answer = prompt(task_update_column,style=style1)
        task_column= task_update_column_answer.get('task_column')
    else:
        task = 'No Task matched with this task ID'
        # print(Fore.RED,'Something went wrong, Please try again....')
        print(Fore.RED,'Given task id does not exist, please try again')
        print(Fore.RESET)
        task_column = None
        PreviousActions('tasks','Tasks')


    if task_column == 'Status':
       
        task_update_column_enter =[
            {
                'type': "list",
                "name": "task_status",
                "message": "Change the task status to - ",
                "choices":['Pending','Completed'],
            }
        ]
        task_update_status = prompt(task_update_column_enter,style=style1)
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
        task_update_status = prompt(task_update_column_enter,style=style1)
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
            "message": "Are you sure, want to update the task status (Y/N):",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        }
    ]
    task_update_confirm_prompt = prompt(task_update_confirm,style=style1)
    task_confirm_data = task_update_confirm_prompt.get('confirm')
    task_confirm_data = task_confirm_data.capitalize()
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
        print()
        print(Fore.GREEN,'*******************  Task updated  *******************')
        print(Style.RESET_ALL)
        
        # except:
        #     # task = 'No Task matched with this task ID'
        #     # console.print(Fore.RED,'Something went wrong, Please try again....')
        #     print(Fore.RED,'Given task id does not exist, please try again')
            
    elif task_confirm_data == 'N':
        print(Fore.BLUE,'Given task status is not updated')
    else:
        print(Fore.RED,'Please enter (Y/N), to confirm the updation')
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
    
    answers = prompt(list_ques,style=style1)
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
        answers = prompt(grp_add,style=style1)
        name = answers.get('grp_name')
        desc = answers.get('grp_desc')
        grp_add_users = answers.get('grp_add_users')
        if grp_add_users == 'Add Now':
            users = []
            usersdata = models.Users.select()
            for l in usersdata.dicts():
                users.append(l['username'])
            # print(users,'67568437658346')

            users_prompt = [
                 {
                    'type': "checkbox",
                    "name": "grp_add_users",
                    "message": "Select the users to add in the group (Note ; use 'space' key for select) ",
                    'choices':users
                },
            ]
            users_answers = prompt(users_prompt,style=style1)
            users_selected = users_answers.get('grp_add_users')
            models.Group.create(title=name,status='Pending',priority='priority',description=desc,user_ids=users_selected)
        elif grp_add_users == 'Add Later':
         
            models.Group.create(title=name,status='Pending',priority='priority',description=desc,user_ids=None)
            print()
        print(Back.GREEN,'**************** Group created successfully ****************',end='')
        print(Back.RESET)
        print()
    elif answers.get("user_option") == "View":
        ViewGroups()
        
    # elif answers.get("user_option") == "Delete":
    #     Delete()
    elif answers.get("user_option") == "Update":
        response = []
        task_lst = models.Group.select()

        for l in task_lst.dicts():
            response.append(l)
        console = Console()
        user_renderables = [Panel(get_content_group(user), expand=True)  for user in response]
        console.print(Columns(user_renderables))
        select_group = [{
                           
            'type': "input",
            "name": "group_select",
            "message": "Enter Group ID to update :",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        
        }]
        grp_select = prompt(select_group,style=style1)
        group_id = grp_select.get('group_select')
        show_groups = [
            {
                    'type': "list",
                    "name": "show_groups",
                    "message": "Choose action ",
                    'choices':['Add Users to Group']
                },
        ]
        user_list_prompt = prompt(show_groups,style=style1)
        group_edit = user_list_prompt.get('show_groups')
        
        if group_edit == 'Add Users to Group':
            row=models.Group.get(models.Group.group_id==group_id)
            try:
                usr_list = ast.literal_eval(row.user_ids)
            except:
                usr_list = []
           
            print(f'Users in {row.title}',end='')
            print(Fore.RESET)
            if usr_list is not None:
                console.print(Columns([Panel(user, expand=True) for user in usr_list]))
            else:
                print(Fore.RED,f'No user Found in this {row.title}',end='')
                print(Fore.RESET)

            users = []
            usersdata = models.Users.select()
            for l in usersdata.dicts():
              
                if l['username'] not in usr_list:
                    users.append(l['username'])
            # print(users,'67568437658346')

            users_prompt = [
                 {
                    'type': "checkbox",
                    "name": "grp_add_users",
                    "message": "Select the users to add in the group (Note : use 'space' key for select) ",
                    'choices':users
                },
            ]
            users_answers = prompt(users_prompt,style=style1)
            users_selected = users_answers.get('grp_add_users')
        
            console.print(Columns([Panel(user, expand=True) for user in users_selected]))
            row=models.Group.get(models.Group.group_id==group_id)
            try:
                use_lst = ast.literal_eval(row.user_ids)
            except:
                use_lst = []
      
            userss_selected=users_selected+use_lst
           
            row.user_ids=userss_selected
            row.save()
            print(Fore.GREEN,'********** Users Successfully added in this group **********')

        elif group_edit == 'Edit Group':
        
   
            select_group = [{
                            
                'type': "input",
                "name": "group_select",
                "message": "Enter Group ID to Delete :",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            
            }]
            grp_select = prompt(select_group,style=style1)
            grp_id = grp_select.get('group_select')
            task_delete_confirm =[
                {
                    'type': "input",
                    "name": "confirm",
                    "message": "Are you sure, want to Update the Group details (Y/N):",
                    "validate": EmptyInputValidator(),
                    "filter": lambda val: str(val)
                }
            ]
            task_delete_confirm_prompt = prompt(task_delete_confirm,style=style1)
            task_confirm_data = (task_delete_confirm_prompt.get('confirm'))
            if task_confirm_data == 'y' or task_confirm_data == 'Y':
                row=models.Group.get(models.Group.group_id==grp_id)
                
                row.delete_instance()
                print(Fore.GREEN,'********** Group Updated **********')

            PreviousActions('tasks','Groups')
    elif answers.get("user_option") == "Delete":
        response = []
        task_lst = models.Group.select()

        for l in task_lst.dicts():
            response.append(l)
        console = Console()
        user_renderables = [Panel(get_content_group(user), expand=True)  for user in response]
        console.print(Columns(user_renderables))
        select_group = [{
                           
            'type': "input",
            "name": "group_select",
            "message": "Enter Group ID to Delete :",
            "validate": EmptyInputValidator(),
            "filter": lambda val: str(val)
        
        }]
        grp_select = prompt(select_group,style=style1)
        grp_id = grp_select.get('group_select')
        task_delete_confirm =[
            {
                'type': "input",
                "name": "confirm",
                "message": "Are you sure, want to delete the Group (Y/N):",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            }
        ]
        task_delete_confirm_prompt = prompt(task_delete_confirm,style=style1)
        task_confirm_data = (task_delete_confirm_prompt.get('confirm'))
        if task_confirm_data == 'y' or task_confirm_data == 'Y':
            row=models.Group.get(models.Group.group_id==grp_id)
            row.delete_instance()
            print(Fore.GREEN,'********** Group Deleted **********')

    elif answers.get("user_option") == "Go back to the main menu":
        MainMenu()
    PreviousActions('tasks','Groups')
   
def Meetings():
    print(Fore.RED,'This option is available in coming version.....')
    print(Fore.RESET)
    MainMenu()

def Users():
    user_add = [
            {
                'type': "input",
                "name": "username",
                "message": "Enter your name",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            },
            {
                'type': "input",
                "name": "user_pwd",
                "message": "Enter the password",
                "validate": EmptyInputValidator(),
                "filter": lambda val: str(val)
            },
            
        ]
    
    answers = prompt(user_add,style=style1)
    username = answers.get('username')
    userpassword = answers.get('user_pwd')
    models.Users.create(username=username,password=userpassword,status=1)
    print(Fore.GREEN,'================ User created successfully ==================')
    PreviousActions('tasks','Groups')


def main():
    # answers = prompt(questions, style=custom_style_3)
    answers = prompt(questions,style=style1)

    if answers.get("user_option") == "Tasks":
        Tasks()
    elif answers.get("user_option") == "Users":
        Users()
    elif answers.get("user_option") == "Groups":
        Groups()
    elif answers.get("user_option") == "Meetings":
        Meetings()


if __name__ == "__main__":
    main()



    