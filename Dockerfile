From python:3.8.3-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN cp mason_app.hex ./scripts/
CMD python scripts/verify_package.py