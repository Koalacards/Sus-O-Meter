FROM python3

RUN python3 -m pip install -r requirements.txt

RUN python3 booter.py