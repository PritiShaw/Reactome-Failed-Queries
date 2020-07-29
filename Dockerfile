FROM rocker/shiny-verse:3.6.3


WORKDIR /src

# Install OpenJDK-11
RUN apt-get update && \
apt-get install -y --no-install-recommends openjdk-11-jre && \
apt-get install wget

COPY ./src/ /src/
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN rm get-pip.py
RUN pip3 install -r requirements.txt
CMD python3 script.py
