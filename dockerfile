# Use slim Python image
FROM python:3.11-slim

# Install Chrome + Chromedriver + dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgbm1 \
    libgtk-3-0 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set display port for Chrome (headless mode)
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Start Flask app using Gunicorn
# Change to APIwebScrapingPopUp:app if you prefer that file
CMD ["gunicorn", "-w", "2", "APIwebScraping:app", "--bind", "0.0.0.0:8000"]

