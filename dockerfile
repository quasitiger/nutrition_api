FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY api.py api.py
COPY api_v2.py api_v2.py
COPY food_nutrition.db food_nutrition.db
# COPY 통합 식품영양성분DB_음식_20230715.xlsx
# CMD ["python3", "data_handler.py"]

CMD ["python3", "api.py"]