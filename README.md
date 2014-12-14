Python library for accessing for bugherd.com API
=======

If you use bugherd.com for tracking bugs and work items, you can use this python library to extract and create tasks using python.
This library implements MOST of the API v2 interface as defined at https://www.bugherd.com/api_v2.  
The library does not yet support comments or attachments on tasks.  APIs will be 
added to also help with registering and unregistering a webhook.

Installation
---


    $ git clone https://github.com/brooksc/bugherd.git

Usage
---

    from bugherd import BugHerd
    
    bh = BugHerd(api_key) # replace with your key from bugherd settings
    
    bh.organization() # returns data on your account
    
    # no project_id is required when operating across multiple projects
    
    bh.projects().list() # returns list of projects
    
    bh.projects().create(name, devurl) # create a project
    
    # project_id is required for project specific information
    
    bh.projects(project_id).details() # check project metadata
    
    # similarly, no task_id is required to list or create a task
    
    bh.projects(project_id).task().list() # List of projects
    
    bh.projects(project_id).task().create(description) # create task, can set other fields
    
    # task_id is required to manipulate a specific task
    
    bh.projects(project_id).task(task_id)
    
Tests
----

tests.py implements a set of unit tests.  You can update this with your api_key 
to validate the library is working against your instance.


