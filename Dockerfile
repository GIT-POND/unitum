# THIS DOCKERFILE CREATES A CUSTOM DOCKER IMAGE
FROM python:3.10.4

# Establish working dir on custom python image
WORKDIR /usr/src/app

# Copy reqs first so its cached, thus only last layers are re-run
COPY requirements.txt ./

# Install reqs on image
RUN pip install -r requirements.txt

# Copy our own directory to python image's working directory
COPY . .

# Establish commmand to run container
CMD ["uvicorn", "App.main:app", "--host", "0.0.0.0", "--port", "8000" ]