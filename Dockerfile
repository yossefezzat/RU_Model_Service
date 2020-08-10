FROM python:3.6
RUN pip3 install nltk
RUN pip3 install PyMuPDF
RUN pip3 install textdistance
RUN pip3 install gensim
RUN pip3 install spacy
RUN pip install fitz

FROM node:12
# Create app directory
WORKDIR /server

COPY package*.json ./

RUN npm install

# Bundle app source
COPY src ./src
COPY config ./config


EXPOSE 3000
CMD [ "npm", "run" , "winDev"]