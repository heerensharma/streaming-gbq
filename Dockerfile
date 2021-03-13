FROM python:3.9.2-slim
LABEL author="Heeren Sharma <heerensharma@yahoo.com>"
# Upgrading pip
RUN pip install -U pip

# Install library dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# Creating mount path for specific data file
RUN mkdir /main_data_bucket

# COPY CODE BASE
COPY . /src
ENV PYTHONPATH "${PYTHONPATH}:/src"
ENV PYTHONUNBUFFERED "1"

# Unit tests
RUN pytest /src/tests
RUN echo "All tests passed!"
