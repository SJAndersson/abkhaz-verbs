#This script uses earlier code from the QP, specifically from
#extract all definite-indefinite pairs.py, to convert the mangled
#OCR from the dictionary to actual Abkhaz orthography. Its input
#is verb forms clean stress.txt, and the output is in the same
#format, with the same words in it, as verb forms clean stress
#orthography.txt. Note that it's important that glosses are
#upper-case for this script to run properly. Otherwise
#Prev in glosses will come out with some cyrillic characters.

s = ""

with open("3. stresses.txt", encoding="utf-8") as f:

    s = f.read()

#These dictionaries are matched in number and order, so that dictIn[i]
#should be replaced by dictOut[i]. The list must be iterated through
#in ascending order of indices, because there are some crucial orderings.

#Note that dictIn and dictOut are different from these variables
#in other versions of this script in other folders. The old ones
#contained replacements for morpheme boundaries, which we don't
#want to get rid of right now.
dictIn = ["a¡", "y¡", "u¡", "i¡", "e¡", "o¡", ";", "´", "ә", "ь", "b", "v", "g", "ҕ", "d", "'", "z", "ӡ", "k", "º", "ҟ", "l", "m", "n", "p", "ҧ", "r", "s", "t", "ҭ", "f", "x", "≈", "c", "ҵ", "h", "˙", "ҽ", "w", "ҩ", "ҿ", "ç", "∞", "a", "y", "e", "o", "i", "u"]
dictOut = ["А", "Ы", "У", "И", "Е", "О", "ь", "ә", "ә", "ь", "б", "в", "г", "ҕ", "д", "ж", "з", "ӡ", "к", "қ", "ҟ", "л", "м", "н", "п", "ҧ", "р", "с", "т", "ҭ", "ф", "х", "ҳ", "ц", "ҵ", "ч", "ҷ", "ҽ", "ш", "ҩ", "ҿ", "џ", "ҕ", "а", "ы", "е", "о", "и", "у"]

for i in range(len(dictIn)):

    s = s.replace(dictIn[i], dictOut[i])

with open("4. orthography.txt", encoding="utf-8", mode="w") as f:

    f.write(s)
