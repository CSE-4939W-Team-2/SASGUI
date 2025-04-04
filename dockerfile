# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /python-docker
RUN pip3 install flask==2.2.5
RUN pip3 install flask-cors
RUN pip3 install sasmodels
RUN pip3 install scikit-learn
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install structlog
COPY /database /python-docker/database
COPY /full_model /python-docker/full_model
COPY /api.py /python-docker
COPY /q_200.txt /python-docker
COPY ["/hierarchical_SAS_analysis-main 2", "/python-docker/hierarchical_SAS_analysis-main 2"]
CMD [ "python3", "-m" , "flask", "--app", "api", "run", "--host=0.0.0.0"]