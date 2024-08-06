# Deriving the latest base image
FROM python:3.10
# FROM --platform=linux/amd64 python:3.10

# Any working directory can be chosen as per choice like '/' or '/home' etc
WORKDIR /

# COPY the remote file at working directory in container
ADD main.py ./
# Now the structure looks like this '/usr/app/src/test.py'

RUN pip install --upgrade pip

RUN python -m pip install selenium webdriver_manager deep-translator
#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./main.py"]