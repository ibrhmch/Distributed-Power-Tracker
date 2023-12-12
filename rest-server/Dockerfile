FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask flask-cors psycopg2 jsonpickle redis requests

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["python3", "rest-server.py"]