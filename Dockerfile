FROM python:3
ADD plugpower.py /
ADD pytuya /pytuya
RUN pip install Crypto
RUN pip install pyaes
ENV PYTHONPATH "${PYTONPATH}:/pytuya"
CMD [ "python", "./plugpower.py" ]
