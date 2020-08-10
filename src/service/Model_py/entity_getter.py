import spacy
import os
import re

word_file = os.path.join('D:\CV-Shortlisting-Data-Cleaning\curriculum_vitae_data-master\word', '1100.docx')
document = docx.Document(word_file)

spacy_nlp = spacy.load('en_core_web_sm')
text = "youssef ayman bought a Toyota camry 2019 model in Toronto Ezzat ayman in January 2020 at a cost of $38000"

def get_name(text):
    doc = spacy_nlp(text)
    for entity in doc.ents:
        if entity.label_ in ["PERSON"]:
            return entity
    return None
    

#needs str casting
def get_email(text):
    email = None
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if match is not None:
        email = match.group(0)
    return email










'''
for para in document.paragraphs:
    doc = spacy_nlp(para.text.strip())
    for i in doc.ents:
        entry = str(i.lemma_).lower()
        text = text.replace(str(i).lower(), "")
        if i.label_ in ["PERSON"]:
            print(entry)
            
            
'''




