import re
import fitz
import os

def pdf2text(file_path):
    
    text=list()
    spans=list()
    doc = fitz.open(file_path)
    for page in doc:
        blocks = page.getText("dict")["blocks"]       
        for block in blocks: 
            if block['type'] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text.append(span['text'])
                        spans.append(span)                   
    return spans, text, file_path


def get_pdf(folderpath):
    headers_Bold=list()
    wholespans=list()
    whole_doc_text=list()
    file_names= list()
    nFiles = len(os.listdir(folderpath))
 
    for f in os.listdir(folderpath):
        filepath = os.path.join(folderpath, f)
        try:
            spans, text, file_path= pdf2text(filepath)
            wholespans.append(spans)
            whole_doc_text.append(text)
            headers_Bold.append(get_headers(spans))
            file_names.append(file_path)
        except:
            continue
            
    #print("No. of files = ", nFiles)
    #print("No. of parsed files = ", len(whole_doc_text)) 
    return file_names , headers_Bold, whole_doc_text, wholespans

def get_headers(spans):
    headers_Bold=list()
    for s in spans:
        if "Bold" in s['font'] or "Italic" in s['font'] or "Black" in s['font'] :
            text=re.sub("[^a-zA-Z ]","",s['text'])
            text=text.lower().lstrip().rstrip()
            if len(text.split())<=3 and text != "" :
                add=text
                headers_Bold.append(add)
            
    return headers_Bold
