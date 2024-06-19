FROM python:3

# Install the function's dependencies using file requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.handler" ]
