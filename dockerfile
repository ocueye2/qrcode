FROM  python:3.12.3-slim


WORKDIR /app

# clone repo
clone . .

RUN pip install flask

# Make port 8080 available to the world outside this container
EXPOSE 7123

WORKDIR /app/musicserver
# Run app.py when the container launches
CMD ["python", "contact.py"]
