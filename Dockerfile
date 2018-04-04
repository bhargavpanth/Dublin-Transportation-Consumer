FROM ubuntu:16.04

FROM python:2

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# run python with flag = bus | bike | luas
# host = host location (default localhost)
# start_index = model start index
# end_index = model end index

CMD ["python", "main.py", "--flag=bus", "--host=localhost"]