import os
import csv
from interruptingcow import timeout
import requests
from lxml.html import fromstring
import PyPDF2
from google_drive_downloader import GoogleDriveDownloader as gdd
import time
import docx2txt

def get_skill_policy(filename):
    f=open(filename)
    reader=csv.reader(f)
    for row in reader:
        break
    column=0
    for i in range(0,len(row)):
        if 'privacy' in row[i]:
            column=i
    policy={}
    for row in reader:
        if row[column]=='' or row[column]=='null':
            continue
        policy[row[0]]=row[column]
    f.close()
    return policy


def split_data_type(policy):
    pdf=[]
    txt=[]
    google_docs=[]
    google_drive=[]
    html=[]
    for i in policy:
        if policy[i][-4:]=='.pdf':
            pdf.append(i)
        if policy[i][-4:]=='.txt':
            txt.append(i)
        if 'docs.google.com' in policy[i]:
            google_docs.append(i)
        if 'drive.google.com' in policy[i]:
            google_drive.append(i)
    html=list(set(policy.keys())-set(pdf)-set(txt)-set(google_docs)-set(google_drive))
    return pdf,txt,google_docs,google_drive,html
 

########## start to download all data types ############

def get_pdf(pdf, policy):
    os.system('mkdir policy/pdf')
    for i in pdf:
        try:
            try:
                with timeout(30, exception=RuntimeError):
                    os.system('curl -L "'+policy[i]+'" >'+'policy/pdf/'+i+'.pdf')
            except RuntimeError:
                continue
        except:
            continue


def get_txt(txt, policy):
    os.system('mkdir policy/txt')
    for i in txt:
        try:
            try:
                with timeout(30, exception=RuntimeError):
                    if 'github' in policy[i]:
                        os.system('curl -L "'+policy[i]+'" >'+'policy/txt/'+i+'.html')
                    else:
                        os.system('curl -L "'+policy[i]+'" >'+'policy/txt/'+i+'.txt')
            except RuntimeError:
                continue
        except:
            continue


def get_google_drive(google_drive, policy):
    os.system('mkdir policy/google_drive')
    for i in google_drive:
        try:
            with timeout(30, exception=RuntimeError):
                r=requests.get(policy[i])
                tree = fromstring(r.content)
                title = tree.findtext('.//title')
                id = max(policy[i].split('/'), key = len).split('=')[-1]
                if '.' in title:
                    filetype = title.split('.')[-1].split()[0]
                    os.system('curl -L "https://docs.google.com/uc?export=download&id='+id+'" >'+'policy/google_drive/'+i+'.'+filetype)
                else:
                    os.system('curl -L "https://docs.google.com/document/export?format=docx&id='+id+'" >'+'policy/google_drive/'+i+'.docx')
        except:
            continue


def get_google_docs(google_docs, policy):
    os.system('mkdir policy/google_docs')
    for i in google_docs:
        try:
            with timeout(30, exception=RuntimeError):
                id=max(policy[i].split('/'),key=len).split('=')[-1]
                os.system('curl -L "https://docs.google.com/document/export?format=doc&id='+id+'" >'+'policy/google_docs/'+i+'.docx')
        except:
            continue


def get_html(html, policy):
    os.system('mkdir policy/html')
    for i in html:
        try:
            try:
                with timeout(30, exception=RuntimeError):
                    os.system('curl -L "'+policy[i]+'" >'+'policy/html/'+i+'.html')
            except RuntimeError:
                continue
        except:
            continue


#def get_html_with_javascript():


def get_html_with_voiceflow(policy):
    for i in policy:
        if 'creator.voiceflow.com' in policy[i]:
            os.system('cp policy/voiceflow.txt policy/html/'+i+'.txt')


########## start to transfoer all types to txt ############

def pdf_to_txt():
    os.system('mkdir policy/pdf_to_txt')
    b=os.listdir('policy/pdf')
    for i in b:
        try:
            pdf = PyPDF2.PdfFileReader(open('policy/pdf/'+i, "rb"))
#            c=os.system('pdftotext policy/pdf/'+i+' policy/pdf_to_txt/'+i[:-4]+'.txt')
            content = ''
            for page in pdf.pages:
                content=content + page.extractText()
            f=open('policy/pdf_to_txt/'+i[:-4]+'.txt','w')
            x=f.write(content.encode('ascii', 'ignore').decode('ascii'))
            f.close()
        except:
            continue


def google_docs_to_txt():
    os.system('mkdir policy/google_docs_to_txt')
    b=os.listdir('policy/google_docs')
    for i in b:
        try:
            text=docx2txt.process("policy/google_docs/"+i)
            content=text.encode('utf-8')
            f=open('policy/google_docs_to_txt/'+i[:-5]+'.txt','w')
            f.write(content)
            f.close()
        except:
            continue


def google_drive_to_txt():
    os.system('mkdir policy/google_drive_to_txt')
    b = os.listdir('policy/google_drive')
    for i in b: 
        try:
            if '.pdf' in i:
                pdf = pyPdf.PdfFileReader(open('policy/google_drive/'+i, "rb"))
                content = ''
                for page in pdf.pages:
                    content=content + page.extractText()
                f=open('policy/google_drive_to_txt/'+i[:-4]+'.txt','w')
                x=f.write(content.encode('ascii', 'ignore').decode('ascii'))
                f.close()
            if '.docx' in i:
                text=docx2txt.process("policy/google_drive/"+i)
                content=text.encode('utf-8')
                f=open('policy/google_drive_to_txt/'+i[:-5]+'.txt','w')
                x=f.write(content)
                f.close()
            if '.txt' in i:
                os.system('cp policy/google_drive/'+i+' policy/google_drive_to_txt/'+i)
        except:
            continue


def txt_to_txt():
    os.system('mkdir policy/txt_to_txt')
    os.system('python2 ../../Downloads/HtmlToPlaintext-master/DockerImage/code/Preprocessor.py --input "policy/txt" --output "policy/txt_to_txt"')
 

def html_to_txt():
    os.system('mkdir policy/html_to_txt')
    os.system('python2 ../../Downloads/HtmlToPlaintext-master/DockerImage/code/Preprocessor.py --input "policy/html" --output "policy/html_to_txt"')


def put_all_together():
    os.system('mkdir policy/all_txt')
    b=os.listdir('policy')
    for i in b:
        if 'to_txt' in i:
            c=os.listdir('policy/' + i)
            for j in c:
                os.system('cp policy/'+i+'/'+j+' policy/all_txt/'+j)


def main():
    skill_policy = get_skill_policy('dataset_9_13_68846.csv')
#    action_policy = get_skill_policy('action_16002.csv')

#    pdf, txt, google_docs, google_drive, html = split_data_type(skill_policy)
#    get_pdf(pdf, skill_policy)
#    get_txt(txt, skill_policy)
#    get_google_docs(google_docs, skill_policy)
#    get_google_drive(google_drive, skill_policy)
#    get_html(html, skill_policy)
    get_html_with_voiceflow(skill_policy)

#    pdf_to_txt()
#    google_docs_to_txt()
#    google_drive_to_txt()
    html_to_txt()
    txt_to_txt()

    put_all_together()


if __name__ == "__main__":
	main()


# all(19566/9956): html, pdf (513/94), google doc (285/5312), google drive (155/133), txt (103/6)
# html (78%), google doc (18.7%), pdf (2%), google drive (1%), txt (0.3%)
# policy_get: 360/403
# policy_get_failed: 73/97
# all: 433/500=86.6%  (87.6%)
'''
('txt', 96)
('pdf', 64)
('html', 87)
('google_docs', 91)
('google_drive', 90)
'''
