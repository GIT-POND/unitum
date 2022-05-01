FROM python:3.9.12

# Establish working dir on image
WORKDIR /usr/src/app

# Copy reqs first so its cached, thus only last layers are re-run
COPY requirements.txt ./

# Install reqs on image
RUN pip install -r requirements.txt

# Copy our dir to image's working dir
COPY . .

# Establish commmand to run container
CMD ["uvicorn", "App.main:app", "--host", "0.0.0.0", "--port", "8000" ]