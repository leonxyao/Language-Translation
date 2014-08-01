from itertools import islice
from collections import Counter
import collections	
import unicodedata
import re

N=50000
with open("english.txt") as myfile:
    english =list(islice(myfile,N))

with open("french.txt") as myfile:
	french = list(islice(myfile,N))

english_frequencies = Counter()
french_frequencies = Counter()
for index in range(N):
	french[index] = french[index].replace('\'','\' ')
	french[index] = french[index].replace('-',' ')
	english[index] = english[index].replace('-',' ')
	french[index] = french[index].replace(' du ', ' de la ')
	french[index] = french[index].replace(' des ', ' de les ')
	french[index] = french[index].replace(' aux ', ' a les ')
	french[index] = french[index].replace(' au ', ' a le ')
	french[index] = french[index].replace('n\'', 'ne')
	french[index] = french[index].replace('j\'', 'je')
	french[index] = french[index].replace('d\'', 'de')
	french[index] = french[index].replace('s\'', 'se')
	french[index] = french[index].replace('t\'', 'te')
	french[index] = re.sub('[!@#$.()]', '', french[index])
	french[index] = french[index].replace('\xc3\xa9', 'e')
	french[index] = french[index].replace('\xc3\xa0', 'a')
	french[index] = french[index].replace('\xc3\xaa', 'e')
	french[index] = french[index].replace('\xc3\xa8', 'e')
	french[index] = french[index].replace('\xc3\xa2', 'a')
	french[index] = french[index].replace('\xc3\xb4', 'o')
	french[index] = french[index].replace('\xc3\xae', 'i')
	french[index] = french[index].replace('\xc3\xaf', 'i')
	french[index] = french[index].replace('\xc3\xa7', 'c')
	french[index] = french[index].replace('\xc2\xad', ' ')

	english[index] = re.sub('[!@#$.()?:]', '', english[index])
	for word in english[index].strip().split():
		english_frequencies[word.lower()]+=1
	for mot in french[index].strip().split():
		french_frequencies[mot.lower()]+=1



english_translation = {}
for index in range(N):
	for word in english[index].strip().split():
		for mot in french[index].strip().split():
			mot = mot.lower()
			word = word.lower()
			mot_count = french_frequencies[mot]
			word_count = english_frequencies[word]
			sum_count = mot_count+word_count
			#if abs(float(mot_count)/sum_count - float(word_count)/sum_count) > 0.45: continue
			if not(mot_count <= word_count + float(N)/1000 and mot_count >= word_count - float(N)/1000): continue
			if word not in english_translation:
				word_counter = Counter()
				word_counter[mot]+=1
				english_translation[word] = word_counter

			else:
				english_translation[word][mot]+=1
for word in english_translation:
	print word,":", "Translations: ", english_translation[word].most_common(3)


#Use jaccard distance to find words that have around the same frequencies or union/intersection. Also try preprocessing to change du-> de le, l' etc. 
#use one iteration just to calculate the frequencies of single words