FROM python:3.12
WORKDIR /app
COPY . .
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements.txt
RUN apt update && apt install -y curl make
RUN make mig
#CMD python3 main.py
CMD ["python3" ,"main.py"]