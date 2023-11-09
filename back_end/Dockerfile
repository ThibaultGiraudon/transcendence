FROM	python:3.8

# Set the working directory
WORKDIR	/usr/src/app/

# Install dependencies
COPY	./requirements.txt ./
RUN		pip install --no-cache -r requirements.txt

# Copy the project
COPY	./ ./

EXPOSE	8000