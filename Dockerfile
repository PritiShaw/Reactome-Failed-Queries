FROM openjdk:8

WORKDIR /src

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

COPY ./src/ /src/

RUN pip install -r requirements.txt
CMD python script.py