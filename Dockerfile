# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Set environment variables for Telegram and Dailymotion credentials
ENV TELEGRAM_API_ID=<your-telegram-api-id>
ENV TELEGRAM_API_HASH=<your-telegram-api-hash>
ENV TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
ENV DAILYMO_USER=<your-dailymotion-username>
ENV DAILYMO_PASS=<your-dailymotion-password>
ENV DAILYMO_API_KEY=<your-dailymotion-api-key>
ENV DAILYMO_API_SECRET=<your-dailymotion-api-secret>

# Run the application
CMD ["python", "main.py"]
