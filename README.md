
## TASK MANAGER

# GitHub Repository URL: 
https://github.com/himangipatel/py-task-manager

# Docker hub URL for docker image :
 https://hub.docker.com/r/himangi14/py-task-manager

# URL for Service API tier :

BASE_URL : http://34.31.253.101:5000/

Get List of tasks : http://34.31.253.101:5000/tasks

### Curl to Add Task in DB though API :
```base
 curl --location 'http://34.31.253.101:5000/tasks' \
--header 'Content-Type: application/json' \
--data-raw ' {
    "id": "11",
    "title": "Create User Profile Page",
    "assignedTo": "eve@example.com",
    "status": "To Do",
    "priority": "Medium",
    "startDate": "03Aug2025",
    "endDate": "13Aug2025"
  }'
```

###  Curl to delete task in DB from API :
 ```base
 curl --location --request DELETE 'http://localhost:5000/tasks/687f4ae21ba0ce89c5b26d2f'
 ```


###  Curl to Edit Task in Db from API :
   ```base
  curl --location --request PUT 'localhost:5000/tasks/687f4b4a4f49ca3de9b13be1' \
--header 'Content-Type: application/json' \
--data-raw '{
    "assignedTo": "charlie@example.com",
    "priority": "Medium",
    "status": "In Progress",
    "title": "Develop User Login",
    "startDate": "29Jul2025",
    "endDate": "09Aug2025"
}'
```

