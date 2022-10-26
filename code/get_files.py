#get policy data

import csv
from interruptingcow import timeout
import os
from lxml.html import fromstring
import requests
from selenium import webdriver


f=open("../policy_17952.csv",'r')
reader=csv.reader(f,delimiter=',')
policy={}
for row in reader:
	policy[row[0]]=row[1]

f.close()
policy['B07DZT5YX9']=policy['\xef\xbb\xbfB07DZT5YX9']
del policy['\xef\xbb\xbfB07DZT5YX9']


############################## get other kinds of document ################################
#get pdf,doc,docx,txt,rtf files

brokenrtf=[]
for i in policy:
	try:
		if policy[i][-4:]=='.rtf':
			try:
				with timeout(30, exception=RuntimeError):
				wget.download(policy[i],'../lab/7_alexa_acsac/policy/rtf/'+i+'.rtf')
			except RuntimeError:
				brokenrtf.append(i)
				continue
	except:
		brokenrtfrtf.append(i)
		continue

#get pdf

brokenpdf=[]
for i in policy:
	try:
		if policy[i][-4:]=='.pdf':
			try:
				with timeout(30, exception=RuntimeError):
					os.system('curl -L "'+policy[i]+'" >'+'policy/pdf/'+i+'.pdf')
			except RuntimeError:
				brokenpdf.append(i)
				continue
	except:
		brokenpdf.append(i)
		continue


#get google drive

names=os.listdir('policy/google_drive/')
brokengoogle=[]
for i in policy:
	if 'drive.google.com' in policy[i]:
		try:
		if i+'.pdf' in names or i+'.docx' in names or i+'.txt' in names or i+'.doc' in names:
			continue
			print(i)
			with timeout(30, exception=RuntimeError):
				r=requests.get(policy[i])
				tree = fromstring(r.content)
				filetype = tree.findtext('.//title').split('.')[1].split()[0]
				id=max(policy[i].split('/'),key=len).split('=')[-1]
				os.system('curl -L "https://docs.google.com/uc?export=download&id='+id+'" >'+'policy/google_drive/'+i+'.'+filetype)
		except:
			brokengoogle.append(i)
			continue
            

#get google docs

for i in policy:
	if 'docs.google.com' in policy[i]:
		print(i)
		a=str(requests.get(policy[i])._content)
		content=''
		while a.find('"s":')!=-1:
			b=a[a.find('"s":')+5:-1]
			content=content+b[0:b.find('},{')]
			a=b
			content=content.replace('\\\\n',' ')
			content=content.replace('\xe2\x80\xaf',' ')
			content=content.replace('\xe2\x80\x9c','" ')
			content=content.replace('\xe2\x80\x9d','"')
			content=content.replace('\xe2\x80\x99','\'')
			content=content.replace('\\xe2\\x80\\xaf',' ')
			content=content.replace('\\xe2\\x80\\x9c','" ')
			content=content.replace('\\xe2\\x80\\x9d','"')
			content=content.replace('\\xe2\\x80\\x99','\'')
			content=content.replace('\\n','\n')
			content=content.replace('\\','')
		f=open('policy/google_doc/'+i+'.txt','w')
		f.write(content)
		f.close()


#get broken google docs

names=os.listdir('policy/google_doc')
google_docs=[]
broken_google_docs=[]
for i in policy:
	if 'docs.google.com' in policy[i]:
		google_docs.append(i)


############################## get html pages #######################################
#get html id
pdf=[]
doc=[]
docx=[]
txt=[]
rtf=[]
google_docs=[]
google_drive=[]

for i in policy:
	if policy[i][-4:]=='.pdf':
		pdf.append(i)
	if policy[i][-4:]=='.doc':
		doc.append(i)
	if policy[i][-5:]=='.docx':
		docx.append(i)
	if policy[i][-4:]=='.txt':
		txt.append(i)
	if policy[i][-4:]=='.rtf':
		rtf.append(i)
	if 'docs.google.com' in policy[i]:
		google_docs.append(i)
	if 'drive.google.com' in policy[i]:
		google_drive.append(i)

html=set(policy.keys())-set(pdf)-set(doc)-set(docx)-set(txt)-set(rtf)-set(google_docs)-set(google_drive)

#get html page
#this broken html is not accurate and deleted

k=0
brokenhtml=[]
for i in html:
	try:
		try:
			with timeout(30, exception=RuntimeError):
				print(k)
				k=k+1
				os.system('curl -L "'+policy[i]+'" >'+'policy/html/'+i+'.html')
		except RuntimeError:
			brokenhtml.append(i)
			continue
	except:
		brokenhtml.append(i)
		continue


############################## transfer all to txt ################################
#transfer pdf to txt

'''
pip install textract
for read pdf

import textract
text = textract.process('path/to/pdf/file', method='pdfminer')

'''

import PyPDF2
import os

a=os.listdir('policy/all_files')
b=os.listdir('policy/pdftotxt')
pdf_broken=[]
for i in a:
	if i[-4:]=='.pdf' and (i[:-4]+'.txt' in b)==False:
		print(i)
		c=os.system('pdftotext policy/all_files/'+i+' policy/pdftotxt/'+i[:-4]+'.txt')
		if c!=0:
			pdf_broken.append(i)


#transfer doc to txt

import docx2txt

docx_broken=[]
a=os.listdir('policy/all_files')
for i in a:
	if i[-5:]=='.docx':
		try:
			print(i)
			text=docx2txt.process("policy/all_files/"+i)
			content=text.encode('utf-8')
			content=content.replace('\\\\n',' ')
			content=content.replace('\xe2\x80\xaf',' ')
			content=content.replace('\xe2\x80\x9c','" ')
			content=content.replace('\xe2\x80\x9d','"')
			content=content.replace('\xe2\x80\x99','\'')
			content=content.replace('\\xe2\\x80\\xaf',' ')
			content=content.replace('\\xe2\\x80\\x9c','" ')
			content=content.replace('\\xe2\\x80\\x9d','"')
			content=content.replace('\\xe2\\x80\\x99','\'')
			content=content.replace('\\n','\n')
			content=content.replace('\\','')
			f=open('policy/docxtotxt/'+i[:-5]+'.txt','w')
			f.write(content)
			f.close()
		except:
			docx_broken.append(i)
			continue


#get 0 size html page

b=os.listdir('policy/html/')

html_broken=[]
for i in b:
	if os.stat('policy/htmltotxt/'+i).st_size==0:
		html_broken2.append(i[:-5])


#transfer html to txt

import html2text
import os

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images=True
b=os.listdir('policy/html/')
c=os.listdir('policy/htmltotxt/')
k=0
html_broken=[]
for i in b:
	try:
		try:
			with timeout(30, exception=RuntimeError):
				if (i[:-4]+'.txt' in c)==False:
					f=open('policy/html/'+i,'r')
					a=f.read()
					f.close()
					f=open('policy/htmltotxt/'+i[:-4]+'.txt','w')
					f.write(h.handle(a))
					f.close()
				k=k+1
				print(k)
		except RuntimeError:
			html_broken.append(i)
			continue
	except:
		html_broken.append(i)
		continue


for i in html_broken:
	f=open('policy/html/'+i,'r',encoding='iso-8859-15')
	a=f.read()
	f.close()
	f=open('policy/htmltotxt/'+i[:-5]+'.txt','w')
	f.write(h.handle(a))
	f.close()

#delete some useless part in txt
b=os.listdir('policy/htmltotxt')
for i in b:
	f=open('policy/htmltotxt/'+i,'r')
	a=f.read()
	f.close()
	a=a[0:a.find('*[')]
	f=open('policy/htmltotxt/'+i,'w')
	f.write(a)
	f.close()


#get js html pages
b=os.listdir('policy/htmltotxt/')
js=[]
for i in b:
	f=open('policy/htmltotxt/'+i,'r')
	a=f.read()
	f.close()
	if 'JavaScript' in a and os.stat('policy/htmltotxt/'+i).st_size<1000:
		js.append(i[:-4])


#re-get html with js
from selenium import webdriver

driver = webdriver.Chrome()
jsbroken=[]
k=0
for i in js:
	try:
		print(k)
		k=k+1
		driver.set_page_load_timeout(10)
		try:
			driver.get(policy[i])
			time.sleep(5)
			content=driver.page_source.encode('utf-8')
			f=open('policy/htmljs/'+i+'.html','w')
			f.write(content)
			f.close()
		except TimeoutException as e:
			print("Page load Timeout Occured. Quiting !!!")
			jsbroken.append(i)
	except:
		x=0
		jsbroken.append(i)


#transfer html with js to txt
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images=True
b=os.listdir('policy/htmljs/')
c=os.listdir('policy/htmljstotxt/')
k=0
htmljs_broken=[]
for i in b:
	try:
		try:
			with timeout(30, exception=RuntimeError):
				if (i[:-4]+'.txt' in c)==False:
					f=open('policy/htmljs/'+i,'r')
					a=f.read()
					f.close()
					f=open('policy/htmljstotxt/'+i[:-5]+'.txt','w')
					f.write(h.handle(a))
					f.close()
				k=k+1
				print(k)
		except RuntimeError:
			htmljs_broken.append(i)
			continue
	except:
		htmljs_broken.append(i)
		continue


for i in htmljs_broken:
	f=open('policy/htmljs/'+i,'r',encoding='iso-8859-15')
	a=f.read()
	f.close()
	f=open('policy/htmljstotxt/'+i[:-5]+'.txt','w')
	f.write(h.handle(a))
	f.close()



#check whether broken pages in others can visit
f=open('policy/broken.txt','r')
a=f.read().split('\n')[:-1]
f.close()
goodinbroken=[]
for i in a:
	try:
		print(i)
		with timeout(10, exception=RuntimeError):
			if requests.get(policy[i]).status_code==200:
				goodinbroken.append(i)
	except:
		continue

#get html in others and transfer to txt
f=open('policy/goodinbroken.txt','r')
goodinbroken=f.read().split('\n')[:-1]
f.close()
driver = webdriver.Chrome()
goodinbroken_broken=[]
k=0
for i in goodinbroken:
	try:
		print(k)
		k=k+1
		driver.set_page_load_timeout(10)
		try:
			driver.get(policy[i])
			time.sleep(5)
			content=driver.page_source.encode('utf-8')
			f=open('policy/goodinbroken/'+i+'.html','w')
			f.write(content)
			f.close()
		except TimeoutException as e:
			print("Page load Timeout Occured. Quiting !!!")
	except:
		x=0

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images=True
b=os.listdir('policy/goodinbroken/')
c=os.listdir('policy/goodinbrokentotxt/')
k=0
htmljs_broken=[]
for i in b:
	try:
		try:
			with timeout(30, exception=RuntimeError):
				if (i[:-4]+'.txt' in c)==False:
					f=open('policy/goodinbroken/'+i,'r')
					a=f.read()
					f.close()
					f=open('policy/goodinbrokentotxt/'+i[:-5]+'.txt','w')
					f.write(h.handle(a))
					f.close()
				k=k+1
				print(k)
		except RuntimeError:
			htmljs_broken.append(i)
			continue
	except:
		htmljs_broken.append(i)
		continue





###################### html zero data check ############################

b=os.listdir('policy/htmltotxt/')
goodinhtml=[]
k=0
for i in b:
	if os.stat('policy/htmltotxt/'+i).st_size<10 and (i in goodinhtml)==False:
		print(k)
		k=k+1
		try:
			with timeout(10, exception=RuntimeError):
				if requests.get(policy[i[:-4]]).status_code==200:
					goodinhtml.append(i)
		except:
			continue

driver = webdriver.Chrome()
k=0
for i in goodinhtml:
	try:
		print(k)
		k=k+1
		driver.set_page_load_timeout(10)
		try:
			driver.get(policy[i])
			time.sleep(2)
			content=driver.page_source.encode('utf-8')
			f=open('policy/goodinhtml/'+i+'.html','w')
			f.write(content)
			f.close()
		except TimeoutException as e:
			print("Page load Timeout Occured. Quiting !!!")
	except:
		x=0

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images=True
b=os.listdir('policy/goodinhtml/')
c=os.listdir('policy/goodinhtmltotxt/')
k=0
htmljs_broken=[]
for i in b:
	try:
		try:
			with timeout(30, exception=RuntimeError):
				if (i[:-4]+'.txt' in c)==False:
					f=open('policy/goodinhtml/'+i,'r')
					a=f.read()
					f.close()
					f=open('policy/goodinhtmltotxt/'+i[:-5]+'.txt','w')
					f.write(h.handle(a))
					f.close()
				k=k+1
				print(k)
		except RuntimeError:
			htmljs_broken.append(i)
			continue
	except:
		htmljs_broken.append(i)
		continue


for i in htmljs_broken:
	f=open('policy/goodinhtml/'+i,'r',encoding='iso-8859-15')
	a=f.read()
	f.close()
	f=open('policy/goodinhtmltotxt/'+i[:-5]+'.txt','w')
	f.write(h.handle(a))
	f.close()


########################## check result #####################################
b=os.listdir('policy/result/')
goodinhtml=[]
k=0
for i in b:
	if os.stat('policy/result/'+i).st_size<10:
		print(k)
		k=k+1
		try:
			with timeout(10, exception=RuntimeError):
				if requests.get(policy[i[:-4]]).status_code==200:
					goodinhtml.append(i)
					print(i)
		except:
			continue


driver = webdriver.Chrome()
k=0
for i in goodinhtml:
	try:
		print(k)
		k=k+1
		driver.set_page_load_timeout(10)
		try:
			driver.get(policy[i[:-4]])
			time.sleep(2)
			content=driver.page_source.encode('utf-8')
			f=open('policy/goodinresult/'+i[:-4]+'.html','w')
			f.write(content)
			f.close()
		except TimeoutException as e:
			print("Page load Timeout Occured. Quiting !!!")
	except:
		x=0

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images=True
b=os.listdir('policy/goodinresult/')
c=os.listdir('policy/goodinresulttotxt/')
k=0
htmljs_broken=[]
for i in b:
#	try:
	try:
		with timeout(30, exception=RuntimeError):
			if (i[:-4]+'.txt' in c)==False:
				f=open('policy/goodinresult/'+i,'r')
				a=f.read()
				f.close()
				f=open('policy/goodinresulttotxt/'+i[:-5]+'.txt','w')
				f.write(h.handle(a))
				f.close()
			k=k+1
			print(k)
	except RuntimeError:
		htmljs_broken.append(i)
		continue
	except:
		htmljs_broken.append(i)
		continue


for i in htmljs_broken:
	f=open('policy/goodinresult/'+i,'r',encoding='iso-8859-15')
	a=f.read()
	f.close()
	f=open('policy/goodinresulttotxt/'+i[:-5]+'.txt','w')
	f.write(h.handle(a))
	f.close()

###################### remove all other language #############################

from nltk.corpus import words

b=os.listdir('policy/result')

f=open('words.txt','r')
words=f.read().split('\n')[:-1]
f.close()
foreign=[]
m=0
for i in b:
	print(m)
	m=m+1
	f=open('policy/result/'+i,'r')
	a=f.read().lower()
	f.close()
	d=a.split()
	if set(d)-(set(d)-set(words))==set([]):
		foreign.append(i)

for i in foreign:
	os.system('rm policy/result/'+i)

foreign={}
m=0
for i in b:
	print(m)
	m=m+1
	f=open('policy/result/'+i,'r',encoding='iso-8859-15')
	a=f.read().lower()
	f.close()
	res=re.findall(r'\w+', a) 
	k=0
	for j in res:
		if j in words:
			k=k+1
	foreign[i]=k/len(res)

for i in foreign:
	if foreign[i]<0.5:
		os.system('rm policy/result/'+i)

###################### get no data pages as broken links #####################

b=os.listdir('policy/result')
broken=[]
m=0
for i in b:
	print(m)
	m=m+1
	f=open('policy/result/'+i,'r')
	a=f.read()
	f.close()
	k=0
	for j in range(0,len(a)):
		try:
			if a[j].isupper()==True:
				k=1
				break			
		except:
			continue
	if k==0:
		broken.append(i)

for i in broken:
	os.system('rm policy/result/'+i)


############################# get 404 and page not found ################################

domain=[]
for i in b:
	f=open('policy/result/'+i,'r')
	a=f.read().lower()
	f.close()
	if 'privacy' not in a and 'policy' not in a and ('404' in a or '403' in a or 'not exist' in a or 'page not found' in a):
		domain.append(i)

f=open('404.txt','w')
for i in domain:
	f.write(i)
	f.write('\n')

f.close()

for i in domain:
	os.system('rm policy/result/'+i)

remove=[]
for i in b:
	f=open('policy/result/'+i,'r')
	a=f.read().lower()
	f.close()
	if 'page has removed' in a or 'not found' in a:
		remove.append(i)

f=open('404.txt','a')
for i in remove:
	f.write(i)
	f.write('\n')

f.close()

for i in remove:
	os.system('rm policy/result/'+i)

patch=[]
for i in b:
	f=open('policy/result/'+i,'r')
	a=f.read().lower()
	f.close()
	if 'this page has moved to  patch.com.' in a:
		patch.append(i)


#patch data process
f=open('patch.txt','r')
patchdata=f.read()
f.close()
content=patchdata
content=content.replace('\\\\n',' ')
content=content.replace('\xe2\x80\xaf',' ')
content=content.replace('\xe2\x80\x9c','" ')
content=content.replace('\xe2\x80\x9d','"')
content=content.replace('\xe2\x80\x99','\'')
content=content.replace('\\xe2\\x80\\xaf',' ')
content=content.replace('\\xe2\\x80\\x9c','" ')
content=content.replace('\\xe2\\x80\\x9d','"')
content=content.replace('\\xe2\\x80\\x99','\'')
content=content.replace('\\n','\n')
content=content.replace('\\','')

for i in patch:
	f=open('policy/result/'+i,'w')
	f.write(content)
	f.close()


b=os.listdir('policy/result')
ad=[]
for i in b:
	f=open('policy/result/'+i,'r',encoding='iso-8859-15')
	a=f.read().lower()
	f.close()
	if 'privacy' not in a and 'policy' not in a and 'skill' not in a and 'data' not in a:
		ad.append(i)


f=open('policy/broken.txt','a')
for i in ad:
	f2=open('policy/result/'+i,'r',encoding='iso-8859-15')
	a=f2.read().lower()
	f2.close()
	if 'error' in a:
		f.write(i[:-4])
		f.write('\n')

f.close()

for i in ad:
	f2=open('policy/result/'+i,'r',encoding='iso-8859-15')
	a=f2.read().lower()
	f2.close()
	if 'error' in a:
		os.system('rm policy/result/'+i)



############################# preprocess policy data #############################
import nltk.data
import csv

tokenizer = nltk.data.load('/home/song/nltk_data/tokenizers/punkt/english.pickle')
b=os.listdir('result')
b.sort()

with open('sentence_pol.csv', 'w', newline='') as csvfile:
	for i in b:
		print(i)
		f=open('result/'+i,'r',encoding='iso-8859-15')
		a=f.read()
		f.close()
		sentences=tokenizer.tokenize(a)
		writer = csv.writer(csvfile)
		for j in range(0,len(sentences)):
			writer.writerow([i[:-4],sentences[j].replace('\n',' ')])


############################# preprocess description data #############################
f=open("../skills_3_6_64720.csv",'r')
reader=csv.reader(f,delimiter=',')
des={}
for row in reader:
	des[row[0]]=row[7]

f.close()



with open('sentence_des.csv', 'w', newline='') as csvfile:
	deskeys=sorted(des.keys())
	for i in deskeys:
		sentences=tokenizer.tokenize(des[i])
		writer = csv.writer(csvfile)
		for j in range(0,len(sentences)):
			writer.writerow([str(i),str(sentences[j].replace('\n',' '))])

########################### check policy accuracy ############################################

import nltk.data
import csv
import os
import json

tokenizer = nltk.data.load('/home/song/nltk_data/tokenizers/punkt/english.pickle')
b=os.listdir('result')
b.sort()

sentenceid=[]
sentences=[]
for i in b:
	f=open('result/'+i,'r',encoding='iso-8859-15')
	a=f.read()
	f.close()
	sentence=tokenizer.tokenize(a)
	for j in sentence:
		sentenceid.append(i[:-4])
		sentences.append(j)

#f=open('policy.txt','r')
f=open('policy_processed.txt','r')
result=f.read().split('\n')[:-1]
f.close()


f=open('gt.txt','r')
gt=f.read().split('\n')[:-1]
f.close()

gt2={}
for i in gt:
	gt2[int(i.split('\t')[0])]=json.loads(i.split('\t')[1])

gt=gt2

result2={}
for i in gt:
	result2[i]=json.loads(result[i])

result=result2

gts=[0]*12
results=[0]*12
tps=[0]*12

for i in range(0,12):
	for j in gt:
		if i in gt[j]:
			gts[i]=gts[i]+1
		if i in result[j]:
			results[i]=results[i]+1
		if i in gt[j] and i in result[j]:
			tps[i]=tps[i]+1

f=open('model_result.txt','w')
for i in range(0,12):
	try:
		precision=tps[i]/results[i]
		recall=tps[i]/gts[i]
		F1=2/(1/precision+1/recall)
		print(i, precision, recall, F1)
		f.write(str(i))
		f.write('\t')
		f.write(str(precision))
		f.write('\t')
		f.write(str(recall))
		f.write('\t')
		f.write(str(F1))
		f.write('\n')
	except:
		x=0

print(sum(tps)/sum(results), sum(tps)/sum(gts), 2/(sum(results)/sum(tps)+sum(gts)/sum(tps)))

f.write('total'+'\t'+str(sum(tps)/sum(results))+'\t'+str(sum(tps)/sum(gts))+'\t'+str(2/(sum(results)/sum(tps)+sum(gts)/sum(tps)))+'\n')


# get GT
randomdata={}
for i in range(0,100):
	randomdata[int(random.random()*len(sentences))]=0

k=1
for i in randomdata:
	print(k)
	k=k+1
	print(sentences[i])
	randomdata[i]=input()


######################## get first class data collection training data ###############


b=os.listdir('annotations')
names=[i[:-4] for i in b]
for i in names:
	f=open('sanitized_policies/'+i+'.html','r')
	a=f.read()
	f.close()
	while '<' in a and '>' in a:
		a=a.replace(a[a.find('<'):a.find('>')+1],'')
	c=a.split('|||')
	first_class={}
	f=open("annotations/"+i+'.csv','r')
	reader=csv.reader(f,delimiter=',')
	for row in reader:
		if row[5]=='First Party Collection/Use':
			if c[int(row[4])] in first_class:
				first_class[c[int(row[4])]].append(json.loads(row[6])['Personal Information Type']['value'])
			else:
				first_class[c[int(row[4])]]=[json.loads(row[6])['Personal Information Type']['value']]
	f.close()
	sentenceid=list(first_class.keys())
	with open('my_data/'+i+'.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		k=0
		for j in range(0,len(sentenceid)):
			for k in set(first_class[sentenceid[j]]):
				writer.writerow([j,sentenceid[j],k])


######################## get first class data collection testing data ####################

b=os.listdir('result')
b.sort()
sentenceid=[]
sentences=[]
for i in b:
	f=open('result/'+i,'r',encoding='iso-8859-15')
	a=f.read()
	f.close()
	sentence=tokenizer.tokenize(a)
	for j in sentence:
		sentenceid.append(i[:-4])
		sentences.append(j)
	


f=open('policy_processed.txt','r')
result=f.read().split('\n')[:-1]
f.close()

data=[]
for i in range(0,len(sentences)):
	if 0 in json.loads(result[i]):
		data.append((sentenceid[i],sentences[i]))

with open('first_class.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	for j in data:
		writer.writerow([j[0],j[1]])


########################### check first_class accuracy ##################################

import nltk.data
import csv
import os

b=os.listdir('result')
b.sort()
sentenceid=[]
sentences=[]
for i in b:
	f=open('result/'+i,'r',encoding='iso-8859-15')
	a=f.read()
	f.close()
	sentence=tokenizer.tokenize(a)
	for j in sentence:
		sentenceid.append(i[:-4])
		sentences.append(j)
	


f=open('policy.txt','r')
result=f.read().split('\n')[:-1]
f.close()

data=[]
for i in range(0,len(sentences)):
	if 0 in json.loads(result[i]):
		data.append((sentenceid[i],sentences[i]))

sentenceid=[]
sentences=[]
for i in data:
	sentenceid.append(i[0])
	sentences.append(i[1])


f=open('first_class.txt','r')
result=f.read().split('\n')[:-1]
f.close()

for i in range(0,100):
	if 6 in json.loads(result[i]):
		print(sentences[i],result[i])

result2=[]
for i in result:
	result2.append(json.loads(i))

result=result2

randomdata={}
for i in range(0,100):
	randomdata[int(random.random()*len(sentences))]=0

k=1
for i in randomdata:
	print(k)
	k=k+1
	print(sentences[i])
	randomdata[i]=input()


gt={}
for i in randomdata:
	gt[i]=[]

for i in randomdata:
	for j in randomdata[i].split(','):
		gt[i].append(int(j))

for i in gt:
	if len(result[i])==0:
		result[i]=[2]


k=0
for i in gt:
	for j in result[i]:
		if j in gt[i]:
			k=k+1


############################## process CNN result ###############################
import nltk.data
import csv
import os
tokenizer = nltk.data.load('/home/song/nltk_data/tokenizers/punkt/english.pickle')

b=os.listdir('result')
b.sort()

sentenceid=[]
sentences=[]
for i in b:
	f=open('result/'+i,'r',encoding='iso-8859-15')
	a=f.read()
	f.close()
	sentence=tokenizer.tokenize(a)
	for j in sentence:
		sentenceid.append(i[:-4])
		sentences.append(j)

f=open('policy.txt','r')
result=f.read().split('\n')[:-1]
f.close()
result2=[]
for i in result:
	result2.append(json.loads(i))

result=result2

## first, change all no result to type 10

for i in range(0,len(result)):
	if result[i]==[]:
		result[i]=[10]

## second, dele all result of short sentence

for i in range(0,len(result)):
	if len(sentences[i])<10:
		result[i]=[]

f=open('policy_processed.txt','w')
for i in result:
	f.write(str(i))
	f.write('\n')

f.close()


############################## checking no data practice files  ##########################

f=open('result2_policysentence22.txt','r')
practice=f.read().split('\n')[:-1]
f.close()
zero={}
for i in practice:
	if i.split('\t')[1]=='0':
		zero[i.split('\t')[0]]=0

for i in zero:
	f=open('../policy/result/'+i+'.txt','r')
	zero[i]=f.read()
	f.close()

k=0
for i in zero:
	if 'privacy' not in zero[i] and 'policy' not in zero[i]:
		k=k+1


from selenium import webdriver

driver = webdriver.Chrome()
broken=[]
k=0
for i in zero:
	try:
		print(k)
		k=k+1
		driver.set_page_load_timeout(10)
		try:
			driver.get(policy[i])
			time.sleep(3)
			content=driver.page_source.encode('utf-8')
			f=open('no_data_practice/'+i+'.html','w')
			f.write(content)
			f.close()
		except TimeoutException as e:
			print("Page load Timeout Occured. Quiting !!!")
			broken.append(i)
	except:
		x=0
		broken.append(i)

import html2text

h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images=True

b=os.listdir('.')
type1=[]
type2=[]
type4=[]
type5=[]
for i in b:
	f=open(i,'r')
	a=f.read()
	f.close()
	data=h.handle(a).lower()
	try:
		title=data.split('#')[1].split('\n')[0]
		if 'privacy policy' in title.lower():
			if 'http' in data and 'privacy policy' in data:
				a=data[0:data.find('http')]
				a=a[::-1]
				a=a[0:a.find('[')]
				a=a[::-1]
				if 'privacy policy' in a:
					type2.append(i)
				else:
					type1.append(i)
			else:
				type1.append(i)
		elif 'no' in title.lower():
			type4.append(i)
		else:
			type5.append(i)
	except:
		if 'privacy policy' in data:
			if 'http' in data:
				a=data[0:data.find('http')]
				a=a[::-1]
				a=a[0:a.find('[')]
				a[::-1]
				if 'privacy policy' in a:
					type2.append(i)
				else:
					type1.append(i)
			else:
				type1.append(i)
		else:
			type5.append(i)




########################## get offical skills #####################################

import csv

f=open("skills_3_6_64720.csv",'r')
reader=csv.reader(f,delimiter=',')
skillid=[]
name={}
category={}
developer={}
description={}
policy={}
for row in reader:
	skillid.append(row[0])
	name[row[0]]=row[1]
	category[row[0]]=row[2]
	developer[row[0]]=row[3]
	description[row[0]]=row[7]
	policy[row[0]]=row[8]

f.close()

official={}
for i in developer:
	if 'amazon' in developer[i].lower():
		official[i]=developer[i]

f.close()


########################## get developer #####################################

policys={}
for i in policy:
	if policy[i]!='null':
		policys[i]=policy[i]

duplicate={}
for i in policys:
	if list(policys.values()).count(policys[i])>1:
		duplicate[i]=policys[i]

duplicatedeveloper={}
for i in duplicate:
	duplicatedeveloper[i]=developer[i]

developernames=set(list(duplicatedeveloper.values()))
developernames2={}
for i in developernames:
	developernames2[i]=0

for i in duplicatedeveloper:
	developernames2[duplicatedeveloper[i]]=developernames2[duplicatedeveloper[i]]+1

a = sorted(test.items(), key=lambda kv: kv[1],reverse=True)

noduplicatedevelper=[]
for i in developer:
	if developer[i] not in developernames2:
		noduplicatedevelper.append(developer[i])


for i in test:
	if i+'.txt' in b:
		f=open('policy/result/'+i+'.txt','r',encoding='iso-8859-15')
		a=f.read()
		f.close()
		if 'collect' in a:
			k=k+1

for i in policy:
	m=m+1
	print(m)
	try:
		pol=policy[i]
		result[i]=compare(pol)
		print(i,result[i])
		f=open('result4_nopolicy.txt','a')
		a=f.write(i)
		a=f.write('\t')
		if result[i]==[]:
			a=f.write('0')
		else:
			a=f.write(str(result[i]).replace('\n',''))	
		a=f.write('\n')
		f.close()
	except:
		break


import re

wordList = re.sub("[^\w]", " ",  a).split()



test=[]
for i in name2:
	if name2[i] in name.values():
		test.append(name2[i])

test2=[]
for i in test:
	for j in name:
		if name[j]==i:
			a=developer[j][3:]
	for j in name3:
		if name3[j]==i:
			b=developer3[j]
	if a==b:
		test2.append(i)

test3=[]
for i in test2:
	for j in name:
		if name[j]==i:
			a=description[j][-10:-1]
	for j in name2:
		if name2[j]==i:
			b=description2[j][-10:-1]
	if a==b:
		test3.append(i)

test4=[]
for i in test3:
	for j in name:
		if name[j]==i:
			print(policy[j])
	for j in name2:
		if name2[j]==i:
			print(policy2[j])
	print('\n')

for i in name:
	if i+'.txt' in b:
		f=open('../../acsac/policy/result/'+i+'.txt','r',encoding='iso-8859-15')
		a=f.read()
		f.close()
		if 'skill' in a.lower():
			k=k+1

for i in name2:
	if name2[i]+'.txt' in c:
		f=open('all_policy_content/all_policy_content/'+name2[i]+'.txt','r',encoding='iso-8859-15')
		a=f.read()
		f.close()
		if name2[i].lower() in a.lower():
			k=k+1

## get category of skills in dataset

categorylist.append('Business & Finance')
categorylist.append('Communication')
categorylist.append('Connected Car')
categorylist.append('Education & Reference')
categorylist.append('Food & Drink')
categorylist.append('Games & Trivia')
categorylist.append('Health & Fitness')
categorylist.append('Home Services')
categorylist.append('Kids')
categorylist.append('Lifestyle')
categorylist.append('Local')
categorylist.append('Movies & TV')
categorylist.append('Music & Audio')
categorylist.append('News')
categorylist.append('Novelty & Humor')
categorylist.append('Productivity')
categorylist.append('Shopping')
categorylist.append('Smart Home')
categorylist.append('Social')
categorylist.append('Sports')
categorylist.append('Travel & Transportation')
categorylist.append('Utilities')
categorylist.append('Weather')


for j in categorylist:
	k=0
	for i in category2:
		if j in category2[i]:
			k=k+1
	print(j,k)


for j in categorylist:
	k=0
	for i in category2:
		if j in category2[i] and policy[i]!='null':
			k=k+1
	print(j,'\t',k)
