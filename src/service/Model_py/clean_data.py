import re
import textdistance
from ReadPDFs import get_pdf 
from entity_getter import get_name , get_email
import json
import sys 

folderpath = sys.argv[1]
ontology = sys.argv[2]
others = sys.argv[3]

def clean_data(text):
    text=re.sub("[^a-zA-Z0-9\+\# ]"," ",text)
    text=text.lower().lstrip().rstrip()
    return text


def outoffile():
    f=open(ontology,"r")
    skills=f.read().splitlines()
    f1=open(others,"r")
    otherheaders=f1.read().splitlines()
    return skills, otherheaders


def get_skill_header(headers,skills):
    list_of_skills=list()
    for header in headers:
        skills_weight=list()
        for No_of_skill in range (len(skills)):
            skills_weight.append( (header, textdistance.jaro_winkler(header,skills[No_of_skill])) )
            #if reached the end of skills sort them and get the highest prob.only
            if No_of_skill== len(skills)-1:
                list_of_skills.append(max(skills_weight,key=lambda x: x[1]))

    skill_element= max(list_of_skills,key=lambda x: x[1])
    skill=skill_element[0]
    headers.remove(skill)
    return skill


def get_otherHeaders(headers,otherHeaders):
    list_of_chosen_Headers=set()
    list_of_otherHeaders=list()
    for header in headers:
        otherHeaders_weight=list()
        for No_of_otherH in range (len(otherHeaders)):
            otherHeaders_weight.append((header,textdistance.jaro_winkler(header,otherHeaders[No_of_otherH])))
            if No_of_otherH == len(otherHeaders)-1:
                list_of_otherHeaders.append(max(otherHeaders_weight,key=lambda y: y[1]))
                
    list_of_otherHeaders.sort(key=lambda y: y[1], reverse = True)
    for header in list_of_otherHeaders:
        if header[1]>0.7:
            list_of_chosen_Headers.add(header[0])
            
    return list_of_chosen_Headers
    
def real_headers(headers,skills,otherHeaders):
    skill=get_skill_header(headers,skills)
    
    list_of_chosen_Headers=get_otherHeaders(headers,otherHeaders)
    list_of_chosen_Headers.add(skill)
    #print(list_of_chosen_Headers)
    return skill,list_of_chosen_Headers

def indices(doc,headers):
    headers_with_indexes=list()
    for header in headers:
        for index in range(len(doc)):
            if header in doc[index]['text'].lower():
                if "Bold" in doc[index]['font'] or "Italic" in doc[index]['font'] or "Black" in doc[index]['font'] :
                    headers_with_indexes.append((header,index))
                    break
                
    headers_with_indexes.sort(key=lambda y: y[1])         
    return headers_with_indexes


def extract_content(headers_with_indexes,docx):
    content=list()
    
    for header_index in range(len(headers_with_indexes)):
        if header_index==len(headers_with_indexes)-1:
            last_header_index=headers_with_indexes[header_index][1]+1
            content.append((headers_with_indexes[header_index][0],clean_data(str(docx[last_header_index:]))))
            break
        previous_header=headers_with_indexes[header_index][1]+1
        next_header=headers_with_indexes[header_index+1][1]
        content.append((headers_with_indexes[header_index][0],clean_data(str(docx[previous_header:next_header]))))
      
    return content

def get_CV_Content(CV_doc,headers,spans,skills_ontology,otherHeaders_ontology):
    cv_content=list()
    skill,final_headers=real_headers(headers,skills_ontology,otherHeaders_ontology)
    headers_with_indices=indices(spans,final_headers)
    cv_content=extract_content(headers_with_indices,CV_doc)
    return skill, cv_content

def get_skill_content(all_content,skill):
    skill_content=""
    for section in range(len(all_content)):
        if skill in all_content[section][0]:
            skill_content = all_content[section]
    return skill_content

def get_All_CVs_Contents(folderpath):
    All_Cvs_Contents = list()
    All_Cvs_skills_Contents = list()
    file_names, headers, CVs_doc, spans = get_pdf(folderpath)
    skills_ontology, otherHeaders_ontology = outoffile()
   
    for i in range(len(CVs_doc)): 
        try:
            skill,cv_content = get_CV_Content(CVs_doc[i],headers[i],spans[i],skills_ontology,otherHeaders_ontology)
            skill_content = get_skill_content(cv_content,skill)
            email = ('email' , get_email(str(CVs_doc[i])))
            name = ('name' , get_name(str(CVs_doc[i])))
            file_name = ('file' , str(file_names[i]))
            All_Cvs_Contents.append(cv_content)
            All_Cvs_skills_Contents.append( (skill_content, email, name, file_name) )
        except:
            continue
    
    return file_names, All_Cvs_skills_Contents, All_Cvs_Contents  


file_names, All_Cvs_skills_Contents, All_Cvs_Contents = get_All_CVs_Contents(folderpath)


resumes = list()
for i in range(len(All_Cvs_skills_Contents)):
    try:
        data = {
            'job_skills': All_Cvs_skills_Contents[i][0][1],
            'all_content': list(All_Cvs_Contents[i]),
            'file_name': str(All_Cvs_skills_Contents[i][3][1]),
            'email': All_Cvs_skills_Contents[i][1][1],
            'name': str(All_Cvs_skills_Contents[i][2][1]),
            'weight': 0
        }
        resumes.append(data)
    except:
        continue

all_resumes = {
    'resumes': resumes
}

print(json.dumps(all_resumes))









