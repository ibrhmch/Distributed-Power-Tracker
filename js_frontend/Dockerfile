FROM ubuntu:22.04

RUN apt update -y
RUN apt install nodejs -y
RUN apt install npm -y


RUN mkdir app
WORKDIR /usr/app
# RUN cd app

RUN git clone https://github.com/ibrhmch/SolarDataVisualizer.git
RUN cd SolarDataVisualizer
WORKDIR /usr/app/SolarDataVisualizer
RUN npm install 

CMD npm start

