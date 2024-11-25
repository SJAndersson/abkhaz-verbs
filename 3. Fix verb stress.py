#This script takes verb forms clean.txt as input, and outputs the same words
#in the same format, but with stresses fixed so they're consistent. The output
#is saved in verb forms clean stress.txt. It removes words with
#stress on aa, since these stresses were supplied based on etymology rather
#than speaker judgments. Words with multiple stresses can have stress in either
#place. This script keeps these as is, with multiple stress marks.
#There are no forms where stress is not supplied because the word is mono-
#vocalic.

s = ""

with open("2. cleaned.txt", encoding="utf-8") as f:

    s = f.read()

sList = s.split("\n")

#Loop through all rows, i.e. all sets of seven verb forms
for entry in sList:

    #Verb forms are split by tabs within lines
    #We skip the column that has glosses
    for verb in entry.split("\t")[:-1]:

        #Forms that have no stress need to have their
        #rows thrown out. Same goes for forms with stress
        #on aa. Stress is marked by ¡
        if "¡" not in verb or "a¡a" in verb or "aa¡" in verb:

            #We modify the string in place, as in earlier scripts
            s = s.replace(entry, "")
            
            #Once we've removed a row, we don't have
            #to keep checking other things in it
            break

#Right now, there are empty rows where removed verbs used to be.
#I thought I could get rid of those above, but something didn't
#work. So I'm doing a cheaty solution here instead, to get rid of
#multiple \n newline characters.

while "\n\n" in s:

    s = s.replace("\n\n", "\n")

with open("3. stresses.txt", encoding="utf-8", mode="w") as f:

    f.write(s)
