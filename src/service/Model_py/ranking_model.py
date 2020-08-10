
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import multiprocessing
import json
import sys
import json 

data = json.loads(sys.argv[1])
description = sys.argv[2]
#print(data[0]['resumes'][1]['job_skills'])


data_resumes = data[0]['resumes'] # returned to ranking Service

training_data = list()
for skill in data_resumes:
    training_data.append(skill['job_skills'])


'''
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['pdfCVs']
pdfCVs = db.pdfCVs

data = list(pdfCVs.find({}))
docs = list()
for doc in data:
    docs.append(doc['job_skills'])
    
print(len(docs))

'''

# Tokenization of each document
tokenized_doc = []
for d in training_data:
    tokenized_doc.append(word_tokenize(d.lower()))

# Convert tokenized document into gensim formated tagged data
tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_doc)]

model = Doc2Vec(tagged_data , 
                vector_size = 100, 
                window = 2, 
                min_count = 5, 
                workers= multiprocessing.cpu_count(),
                epochs = 20 
                )
# Save trained doc2vec model
#model.save("test_doc2vec.model")

## Load saved doc2vec model
#model= Doc2Vec.load("test_doc2vec.model")

test_doc = word_tokenize(description.lower())
results= model.docvecs.most_similar( positive=[model.infer_vector(test_doc)] , topn= len(training_data))

weighted_results = list()
for res in results:
    data_resumes[ res[0] ]['weight'] = res[1]
    weighted_CV = {
        'path': data_resumes[ res[0] ]['file_name'],
        'weight': data_resumes[ res[0] ]['weight'],
        'name': data_resumes[ res[0] ]['name'],
        'email': data_resumes[ res[0] ]['email'], 
        'class': ''
    }
    weighted_results.append(weighted_CV)

print(json.dumps( { 'cvs': weighted_results } ))


