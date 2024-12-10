# Use the official Python 3.11 image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire app folder and models into the container
COPY ./app4.py /app/app4.py
COPY ./models /app/models

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["Streamlit", "run", "app4.py", "--server.port=8501", "--server.address=0.0.0.0"]