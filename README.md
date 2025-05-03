# Project-7
Group members:
- Evelyn Landau
- Daniel Kalvaitis
- Benjamin Zheng
- Sophiya Singh
- Shiv Patel
- Jennifer Fomenko

Sponsors:
- Professor Qian Yang
- Dr. Mu-Ping Nieh
- Graham Roberts

Frontend Docker Commands:

From SASGUI-Frontend:
- docker build --tag sasgui-frontend . 
- docker run --name frontend -d -p 5173:5173 sasgui-frontend

From root folder:
- docker build --tag sasgui-backend . 
- docker run --name backend -d -p 5000:5000 sasgui-backend

NOTE: To change the port the container is exposed on, change the first port number in the 
docker run command, E.G to change the backend to port 8080 do:
- docker run --name backend -d -p 8080:5000 sasgui-backend
- If this app is redeployed or the port numbers change, VITE_VM_URL in .env in the SASGUI-Frontend folder will need to be changed to match the new backend URL and/or port, and the cors allowed origins on line 351 of api.py in the root folder will need to be changed to match the new frontend URL and/or port. The docker containers will then need to be rebuilt and re-run