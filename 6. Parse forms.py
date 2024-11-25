#This script takes forms with correct morpheme boundaries
#as input, and outputs individual glosses for every verb
#form, as well as a rough phonological transcription.
import random

dictIn = ["А", "Ы", "У", "И", "Е", "О", "ә", "ь", "б", "в", "г", "ҕ", "д", "ж", "з", "ӡ", "к", "қ", "ҟ", "л", "м", "н", "п", "ҧ", "р", "с", "т", "ҭ", "ф", "х", "ҳ", "ц", "ҵ", "ч", "ҷ", "ҽ", "ш", "ҩ", "ҿ", "џ", "ҕ", "а", "ы", "е", "о", "и", "у"]
dictOt = ["A", "Y", "G", "G", "E", "O", "", "", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "a", "y", "e", "o", "g", "g"]

#Return a phonological version of each form transcribed
#as follows: all consonants are replaced by C. All vowels
#are retained as is, except high vowels/glides are G if
#stressed, and g elsewhere.
def getPhonology(st):

    for i in range(len(dictIn)):

        st = st.replace(dictIn[i], dictOt[i])

    return st

s = ""

with open("5. morpheme boundaries.txt", encoding="utf-8") as f:

    s = f.read()

sList = s.split("\n")

sOut = ""

#This list (see 4.5) has all of the possible verb categories
#we're dealing with. Every verb entry in the dataset will
#end in one of these number strings, which correspond one-to-
#one with verb categories.
possibleGlosses = ['2221323', '2331323', '3332434', '3442434', '4443545', '4553545', '2332434', '2442434', '3443545', '3553545', '4554656', '4664656', '2331423', '2441423', '3442534', '3552534', '4553645', '4663645', '2442534', '2552534', '3553645', '3663645', '4664756', '4774756']

#These are the old gloss strings associated with each of the
#numbers in possibleGlosses. They are in the same order. We
#use these to add the gloss strings back in at the end of
#each row.
glossStrings = ["C1-R", "C1-R", "C1-PREV-R", "C1-PREV-R", "C1-PREV-PREV2-R", "C1-PREV-PREV2-R", "C1-C2-R", "C1-C2-R", "C1-C2-PREV-R", "C1-C2-PREV-R","C1-C2-PREV-PREV2-R", "C1-C2-PREV-PREV2-R", "C1-C3-R", "C1-C3-R", "C1-PREV-C3-R", "C1-PREV-C3-R", "C1-PREV-PREV2-C3-R", "C1-PREV-PREV2-C3-R", "C1-C2-C3-R", "C1-C2-C3-R", "C1-C2-PREV-C3-R", "C1-C2-PREV-C3-R", "C1-C2-PREV-PREV2-C3-R", "C1-C2-PREV-PREV2-C3-R"]

#This nightmarish list has the full glosses for every form
#for every verb category. The verb categories are listed in
#the exact same order as in possibleGlosses above. In other
#words, for some index i, a verb with the gloss information
#possibleGlosses[i] is a list of full glosses specified in
#fullGlosses[i]
fullGlosses = [
    ["DEF-R-INF", "C1-R.DYN-DYN.FIN", "C1-R.DYN-NEG", "C1-R", "C1-NEG-R-DYN.IMP", "C1-R-ABS", "C1-NEG-R-NEG.ABS"],
    ["DEF-R-INF", "C1-R-DYN-DYN.FIN", "C1-R-DYN-NEG", "C1-R", "C1-NEG-R-DYN.IMP", "C1-R-ABS", "C1-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-PREV-R.DYN-DYN.FIN", "C1-PREV-R.DYN-NEG", "C1-PREV-R", "C1-PREV-NEG-R-DYN.IMP", "C1-PREV-R-ABS", "C1-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-PREV-R-DYN-DYN.FIN", "C1-PREV-R-DYN-NEG", "C1-PREV-R", "C1-PREV-NEG-R-DYN.IMP", "C1-PREV-R-ABS", "C1-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-PREV2-R-INF", "C1-PREV-PREV2-R.DYN-DYN.FIN", "C1-PREV-PREV2-R.DYN-NEG", "C1-PREV-PREV2-R", "C1-PREV-PREV2-NEG-R-DYN.IMP", "C1-PREV-PREV2-R-ABS", "C1-PREV-PREV2-NEG-R-NEG.ABS"],
    ["DEF-PREV-PREV2-R-INF", "C1-PREV-PREV2-R-DYN-DYN.FIN", "C1-PREV-PREV2-R-DYN-NEG", "C1-PREV-PREV2-R", "C1-PREV-PREV2-NEG-R-DYN.IMP", "C1-PREV-PREV2-R-ABS", "C1-PREV-PREV2-NEG-R-NEG.ABS"],
    ["DEF-R-INF", "C1-C2-R.DYN-DYN.FIN", "C1-C2-R.DYN-NEG", "C1-C2-R", "C1-C2-NEG-R-DYN.IMP", "C1-C2-R-ABS", "C1-C2-NEG-R-NEG.ABS"],
    ["DEF-R-INF", "C1-C2-R-DYN-DYN.FIN", "C1-C2-R-DYN-NEG", "C1-C2-R", "C1-C2-NEG-R-DYN.IMP", "C1-C2-R-ABS", "C1-C2-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-C2-PREV-R.DYN-DYN.FIN", "C1-C2-PREV-R.DYN-NEG", "C1-C2-PREV-R", "C1-C2-PREV-NEG-R-DYN.IMP", "C1-C2-PREV-R-ABS", "C1-C2-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-C2-PREV-R-DYN-DYN.FIN", "C1-C2-PREV-R-DYN-NEG", "C1-C2-PREV-R", "C1-C2-PREV-NEG-R-DYN.IMP", "C1-C2-PREV-R-ABS", "C1-C2-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-PREV2-R-INF", "C1-C2-PREV-PREV2-R.DYN-DYN.FIN", "C1-C2-PREV-PREV2-R.DYN-NEG", "C1-C2-PREV-PREV2-R", "C1-C2-PREV-PREV2-NEG-R-DYN.IMP", "C1-C2-PREV-PREV2-R-ABS", "C1-C2-PREV-PREV2-NEG-R-NEG.ABS"],
    ["DEF-PREV-PREV2-R-INF", "C1-C2-PREV-PREV2-R-DYN-DYN.FIN", "C1-C2-PREV-PREV2-R-DYN-NEG", "C1-C2-PREV-PREV2-R", "C1-C2-PREV-PREV2-NEG-R-DYN.IMP", "C1-C2-PREV-PREV2-R-ABS", "C1-C2-PREV-PREV2-NEG-R-NEG.ABS"],
    ["DEF-R-INF", "C1-C3-R.DYN-DYN.FIN", "C1-C3-R.DYN-NEG", "C1-R", "C1-C3-NEG-R-DYN.IMP", "C1-R-ABS", "C1-NEG-R-NEG.ABS"],
    ["DEF-R-INF", "C1-C3-R-DYN-DYN.FIN", "C1-C3-R-DYN-NEG", "C1-R", "C1-C3-NEG-R-DYN.IMP", "C1-R-ABS", "C1-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-PREV-C3-R.DYN-DYN.FIN", "C1-PREV-C3-R.DYN-NEG", "C1-PREV-R", "C1-PREV-C3-NEG-R-DYN.IMP", "C1-PREV-R-ABS", "C1-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-PREV-C3-R-DYN-DYN.FIN", "C1-PREV-C3-R-DYN-NEG", "C1-PREV-R", "C1-PREV-C3-NEG-R-DYN.IMP", "C1-PREV-R-ABS", "C1-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-PREV2-R-INF", "C1-PREV-PREV2-C3-R.DYN-DYN.FIN", "C1-PREV-PREV2-C3-R.DYN-NEG", "C1-PREV-PREV2-R", "C1-PREV-PREV2-C3-NEG-R-DYN.IMP", "C1-PREV-PREV2-R-ABS", "C1-PREV-PREV2-NEG-R-NEG.ABS"],
    ["DEF-PREV-PREV2-R-INF", "C1-PREV-PREV2-C3-R-DYN-DYN.FIN", "C1-PREV-PREV2-C3-R-DYN-NEG", "C1-PREV-PREV2-R", "C1-PREV-PREV2-C3-NEG-R-DYN.IMP", "C1-PREV-PREV2-R-ABS", "C1-PREV-PREV2-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-C2-PREV-C3-R.DYN-DYN.FIN", "C1-C2-PREV-C3-R.DYN-NEG", "C1-C2-PREV-R", "C1-C2-PREV-C3-NEG-R-DYN.IMP", "C1-C2-PREV-R-ABS", "C1-C2-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-C2-PREV-C3-R-DYN-DYN.FIN", "C1-C2-PREV-C3-R-DYN-NEG", "C1-C2-PREV-R", "C1-C2-PREV-C3-NEG-R-DYN.IMP", "C1-C2-PREV-R-ABS", "C1-C2-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-C2-PREV-C3-R.DYN-DYN.FIN", "C1-C2-PREV-C3-R.DYN-NEG", "C1-C2-PREV-R", "C1-C2-PREV-C3-NEG-R-DYN.IMP", "C1-C2-PREV-R-ABS", "C1-C2-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-R-INF", "C1-C2-PREV-C3-R-DYN-DYN.FIN", "C1-C2-PREV-C3-R-DYN-NEG", "C1-C2-PREV-R", "C1-C2-PREV-C3-NEG-R-DYN.IMP", "C1-C2-PREV-R-ABS", "C1-C2-PREV-NEG-R-NEG.ABS"],
    ["DEF-PREV-PREV2-R-INF", "C1-C2-PREV-PREV2-C3-R.DYN-DYN.FIN", "C1-C2-PREV-PREV2-C3-R.DYN-NEG", "C1-C2-PREV-PREV2-R", "C1-C2-PREV-PREV2-C3-NEG-R-DYN.IMP", "C1-C2-PREV-PREV2-R-ABS", "C1-C2-PREV-PREV2-NEG-R-NEG.ABS"],
    ["DEF-PREV-PREV2-R-INF", "C1-C2-PREV-PREV2-C3-R-DYN-DYN.FIN", "C1-C2-PREV-PREV2-C3-R-DYN-NEG", "C1-C2-PREV-PREV2-R", "C1-C2-PREV-PREV2-C3-NEG-R-DYN.IMP", "C1-C2-PREV-PREV2-R-ABS", "C1-C2-PREV-PREV2-NEG-R-NEG.ABS"]
    ]

tempForms = []
tempGloss = ""
tempIndex = 0

#Loop through all rows of the dataset
for entry in sList:
    
    #Get the verb forms
    tempForms = entry.split("\t")[:-1]
    #Get the number string of glosses
    tempGloss = str(entry.split("\t")[-1])
    #Get the index of tempGloss in possibleGlosses
    tempIndex = possibleGlosses.index(tempGloss)
    #Add the orthography, phonology, and gloss for each form
    for i in range(len(tempForms)):

        sOut += tempForms[i] + "\t" + getPhonology(tempForms[i]) + "\t" + fullGlosses[tempIndex][i] + "\t"

    #Add the gloss string and start a new line for the next row
    sOut += glossStrings[possibleGlosses.index(tempGloss)]+ "\n"

with open("6. parsed forms.txt", encoding="utf-8", mode="w") as f:

    f.write(sOut[:-1])
