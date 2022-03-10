# syntax=docker/dockerfile:1

FROM python:3-alpine

RUN pip install --upgrade pip

# Add user to avoid pip errors
RUN adduser -D pythonUser
USER pythonUser
WORKDIR /home/pythonUser

# Copy Python Scripts
COPY --chown=pythonUser:pythonUser backend.py .
COPY --chown=pythonUser:pythonUser database.py .
COPY --chown=pythonUser:pythonUser requirements.txt .

RUN pip install --user -r requirements.txt

ENV PATH="/home/pythonUser/.local/bin:${PATH}"

COPY --chown=pythonUser:pythonUser . .


CMD [ "python3", "./backend.py" ]
