# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code into the container
COPY . /app/

# Expose port 8000 for FastAPI
EXPOSE 8000

# OPTIONAL: Copy your .env if you'd rather bake it into the container
# Otherwise you can mount it in at runtime
# COPY .env /app/

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
