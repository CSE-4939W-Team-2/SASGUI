# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /python-docker
RUN pip3 install flask
RUN pip3 install flask-cors
RUN pip3 install sasmodels
COPY /backend /python-docker/backend
COPY /database /python-docker/database
COPY /full_model /python-docker/full_model
COPY ["/hierarchical_SAS_analysis-main 2", "/python-docker/hierarchical_SAS_analysis-main 2"]
WORKDIR /python-docker/backend
CMD [ "python3", "-m" , "flask", "--app", "api", "run", "--host=0.0.0.0"]