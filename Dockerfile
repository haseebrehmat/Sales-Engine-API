FROM python:3.9

RUN pip install --upgrade pip

# Set the working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    unzip \
    libxi6 \
    libgconf-2-4 \
    default-jdk \
    libxslt-dev \
    libxml2 \
    libxml2-dev \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    libxrender1 \
    xfonts-75dpi \
    xfonts-base \
    xauth \
    unzip \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    fonts-liberation \
    gpg \
    ca-certificates \
    apt-transport-https \
    software-properties-common

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Install Chrome WebDriver
RUN wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O /tmp/chromedriver_version && \
    wget -q https://chromedriver.storage.googleapis.com/$(cat /tmp/chromedriver_version)/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ /app

WORKDIR /app

# Install wait-for-it script
RUN wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh


COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
EXPOSE 8000