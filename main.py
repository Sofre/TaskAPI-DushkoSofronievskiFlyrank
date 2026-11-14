from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# List with Directory at O(n)List to O(1)Directory
tasks_list = [ 

        {"id":1 , "title":"Go out with girlfriend", "done":True },
        {"id":2 , "title":"Write documentation for Beetle Club Web Application ", "done":False },
        {"id":3 , "title":"Create a CRUD API ", "done":False }

        ]

# commit 0
# commit 1
# commit 2
# define endpoints 

@app.get("/tasks/search")
def search_taskbyWord(word:str):
        # take all tasks
        results = [] # if more than one task has the same word
        for task in tasks_list:
                for wrd in task["title"].split():
                        if wrd.lower() == word.lower():
                                results.append(task)
                                break
                
        return f"msg: The word {word} can't be found in any tasks. "


@app.get("/tasks/done")
def search_by_complete(stat_complete:bool):
        results = []
        for task in tasks_list:
                if task["done"] == True:
                        results.append(task)
        
        return f"msg: No tasks are done"

@app.get("/")
def read_root():
        return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/tasks/health")
def server_status():
        return {"status: OK"}


# Get stats for tasks
@app.get("/tasks/stats")
def stats4tasks():
       
        counter = 0
        counter_false = 0
        counter_true = 0
        for task in enumerate(tasks_list):
               

                if task["done"]:
                        counter_true+=1
                else:
                        counter_false+=1 
                        

        counter = counter_true + counter_false
                
        
        return {
                "total": counter,
                "done": counter_true,
                "open": counter_false
                }

# Get all tasks GET
# /tasks
@app.get("/tasks")
def get_tasks():
    if len(tasks_list) == 0:
        return {"message: No such task can be found"}
    else:
        return tasks_list

# GET tasl by ID
# ID guard on expected dataype of Int
@app.get("/tasks/{id}")
def get_taskId(id: int):
        for tisk in tasks_list:
                if tisk["id"] == id:
                   return tisk
                
        return {"message: No such task can be found"}


# POST endpoint
@app.post("/tasks")
async def insert_task(request:Request):   
       
        body = await request.json()  

        if body is None:
                raise HTTPException(
                        status_code=400,
                        detail=f"Unknown field: {field}"
                        )

        required_fields = ["title"] # hard checks the required data needed to come in


        for field in required_fields:
                if field not in body:
                        raise HTTPException( # hanndles gracefull errors for missing fields
                                status_code=400,
                                detail=f"Missing required field: {field}"
                        )

        for field in body:
                if field not in required_fields:
                        raise HTTPException( # handdles gracefull errors for uknown fields 
                                status_code=422,
                                detail=f"Unknown field: {field}"
                                )
        
       
      

        
        new_insert = {}     
        new_insert = body.copy() 
        

        last_id = max((task["id"] for task in tasks_list), default=0) # Comment: Gets max without needing to negative index. Negative index is faster might cause breakge in few instances
        new_insert = {
                "id": last_id + 1,
                **body
        } # fix to map out id first in row
        new_insert["done"] = False
        # Comment:  Maps out the rest of the body
        tasks_list.append(new_insert)
        
        return {"message":f"New fiedl add with id : {last_id+1}"}



@app.delete("/tasks")
def delete_tasks():
        if len(task_list) == 0:
                return "Memory space is already zero!!"
        
        
        tasks_list.clear()
        return {
                "msg: Memory Cleaned",
                "Current memory size is :", len(tasks_list) 
        }
        

@app.delete("/tasks/{id}")
def delete_taskId(id: int):
        for index, task in enumerate(tasks_list):
                if task["id"] == id:
                        tasks_list.pop(index)
                        
                        return {
                                "message": "Task has been removed",
                                "current_list_size": len(tasks_list),
                                
                                }
        
        raise HTTPException(
                status_code=404,
                detail=f"Task not found with id: {id} "
        )




# Status bar

# PUT FOR ALL
@app.put("/tasks/{id}")
async def change_task(id:int, request:Request):
    
        body = await request.json()  

        if body is None:
                raise HTTPException(
                        status_code=401,
                        detail=f"Unknown field: {field}"
                        )

        required_fields = ["title"] # hard checks the required data needed to come in 
                                    # In our case because we limited to a one string and a boolean that we will keep for state change its going to sit for title
                                    # Required fields should be only the fields in this case that use informative change , not state change, nor a id copy is required 
                                    # Id should be best used for other functions
        for field in required_fields: # checks the required_field list
                if field not in body:
                        raise HTTPException( # hanndles gracefull errors for missing fields
                                status_code=400,
                                detail=f"Missing required field: {field}"
                        )

        for field in body: # checks the response body
                if field not in required_fields:
                        raise HTTPException( # handdles gracefull errors for uknown fields 
                                status_code=401,
                                detail=f"Unknown field: {field}"
                                )
        

        for index, task in enumerate(tasks_list): # enumirate identifes the physical postion in the python list
                if task["id"] == id:
                        persist_bool = tasks_list[index]["done"]
                        new_task = body.copy() # sends 0 on boolean
                        new_insert = {
                                "id": id,
                                **body
                                }
                        tasks_list[index]["title"] = new_task["title"]
                        tasks_list[index]["done"] = persist_bool # This must be persisted 
                        return new_task 
        
        raise HTTPException(
                status_code=404,
                detail=f"Task with id: {id} not found! "
        )
                        
        


# PATCH FOR done: STATUS BOOL

@app.patch("/tasks/{id}")
async def update_status_task(id:int, request:Request):
        body = await request.json()  
        
        if body is None:
                raise HTTPException(
                        status_code=401,
                        detail=f"Unknown field: {field}"
                        )
        
        required_fields=["title","done"]

      
        for field in body:
                if field not in required_fields:
                        raise HTTPException(
                                status_code=400,
                                detail="msg: Unknown field"
                        )
 
           
        # Validate datatype: Boolean
        if not isinstance(body["done"], bool):
                raise HTTPException(
                        status_code=400,
                        detail="Done must be a boolean"
                        )
        
        
       
        for index, task in enumerate(tasks_list):
                current_state = tasks_list[index]["done"]
                persist_title = tasks_list[index]["title"]

                new_task = body.copy() # sends 0 on boolean

                if current_state == body["done"]:
                        return "msg: You must switch state"
                
                new_insert = {
                        "id": id,
                        **body
                }
             
                tasks_list[index]["done"] = new_task["done"]
                tasks_list[index]["task"] = persist_title
                return f"msg: State switched : {tasks_list[index]["done"]}"
                        



        

                        

# Filtering endpoints = for string's
# Filterine with query paramters = booleans




# README - testing

# Commit per 6 stages


        





        

        



        
                
     
        
