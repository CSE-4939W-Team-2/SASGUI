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