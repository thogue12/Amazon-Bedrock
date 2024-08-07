FROM python:3.13.0b4-bookworm

WORKDIR D:\AWS\AWS Projects\Amazon Bedrock\main-claudev2.py

COPY  requirements.txt ./

EXPOSE 8501

CMD [ "streamlit", "run" "main-claudev2.py" ]