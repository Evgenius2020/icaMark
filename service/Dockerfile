FROM python

ENV KERAS_BACKEND=theano

RUN pip3 install --upgrade pip
RUN pip3 install keras==2.2.4
RUN pip3 install theano
RUN pip3 install flask
RUN pip3 install Pillow

COPY src .
COPY model .

CMD ["python", "-u", "main.py"]