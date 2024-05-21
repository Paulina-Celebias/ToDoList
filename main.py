import webview 
import json
import uuid

window = webview.create_window('To Do List', 'assets/index.html', width = 400, height = 640)


def creatListElement(parent, task):
    completedAttribute = ''
    if (task['completed']):
        completedAttribute = 'checked'
        
    htmlString = '''<div class='listElement'><input id='{0}' type='checkbox' {1} /><label for='{0}'>{2}</label><button data-id='{0}'><img src='bin.png' /></button></div>'''.format(task['id'], completedAttribute, task['taskName'])    
    window.dom.create_element(htmlString, parent)

def loadData():
    data = open('data.json')
    data = json.load(data)
    return data

def onTaskToggle(event):
    # For every task in task list ...
    for task in taskList:
        # ... we are looking for ID matching input ID ...
        if (task['id'] == event['target']['id']):
            # ... and updating completed state in our main data object.
            task['completed'] = event['target']['checked']
            saveTaskList()
    
def onRemoveClick(event):
    # For every task in task list ...
    for task in taskList:
        # ... we are looking for ID matching input ID ...
        if (task['id'] == event['currentTarget']['attributes']['data-id']):
            result = window.create_confirmation_dialog('Warning!', 'Are you sure you want to remove this task?')
            if result:
                taskList.remove(task)
                refreshList()
                saveTaskList()
    
def refreshList():
    # Finding element in html with 'list' id
    list = window.dom.get_element('#list')
    # Clearing that element
    list.empty()
    
    # For each task we are creating list element
    for task in taskList:
        creatListElement(list, task)
    
    # Finding every checkbox input in the list
    listElementsInputs = window.dom.get_elements('#list .listElement input')
    
    # Attaching change event listener to inputs
    for inputElement in listElementsInputs:
        inputElement.on('change', onTaskToggle)
        
    # Finding every button in the list
    listElementsButtons = window.dom.get_elements('#list .listElement button')
    
    # Attaching click event listener to buttons
    for button in listElementsButtons:
        button.on('click', onRemoveClick)    

def saveTaskList():
    # Saving current list state to file
    # Turning main data object into JSON string
    taskJSON = json.dumps(taskList, indent=4)
    dataJSON = open('data.json', 'w')
    dataJSON.write(taskJSON)
    dataJSON.close()

def submitNewTask(event=None):
    # Find input with name of the new task
    input = window.dom.get_element('#action input')
    # Creating new task object / generating uuid.
    newTask = {'id': str(uuid.uuid1()), 'taskName': input.value, 'completed': False}
    taskList.append(newTask)
    saveTaskList()
    refreshList()
    input.value = ''
    
def keyDownEffect(event):
    # Check if pressed key is 'enter' 
    if event['key'] == 'Enter':
        submitNewTask()

def onDocumentReady():
    refreshList()
    
    # Finding button responsible for adding new tasks.
    button = window.dom.get_element('#action button')
    button.on('click', submitNewTask)
        
    # Find input in actions
    input = window.dom.get_element('#action input')
    # Attatch keydown event to input
    input.on('keydown', keyDownEffect)
    
 
taskList = loadData()
webview.start(onDocumentReady)