# Dockerfile

# Use the official Python image as a base image
FROM python:3.9-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install necessary packages and dependencies
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get update && apt-get install -y \
        apt-utils \
        postgresql-client \
        gdal-bin \
        libgdal-dev \
        libspatialindex-dev \
        nodejs \
        wget \
        gnupg \
    && npm install --global yarn \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 libcairo2 libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
RUN mkdir /code
WORKDIR /code

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /code/


# Install Python dependencies
RUN pip install pipenv && pipenv install --system

# Copy the rest of the application code
COPY . /code/

# Give executable permission
RUN chmod a+x /code/Driver/chromedriver.exe

CMD ["uwsgi", "--ini", "uwsgi.ini" ]
