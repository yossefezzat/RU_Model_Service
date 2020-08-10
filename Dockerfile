FROM node:12-stretch-slim
# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN apt-get install --yes python
RUN npm install
RUN apt-get install python3-pip 
RUN pip install PyMuPDF
RUN pip install nltk
RUN pip install textdistance
RUN pip install fitz
RUN pip install gensim
RUN pip install multiprocessing
RUN pip install spacy


# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE 3000
CMD [ "npm", "run", "winDev" ]