#This script takes orthographic forms as inputs, and outputs
#the same forms, in the same order, but with all the correct
#morpheme boundaries. This is a partly automatic, partly
#manual process. Glossing information is removed by this
#script currently, because it can be reconstructed more
#accurately from the correct morpheme boundaries than from
#the dictionary's glossing information.
import random

s = ""

with open("4. orthography.txt", encoding="utf-8") as f:

    s = f.read()

#Function to fix negative morphemes in some form f
#Returns the fixed form
#Note: this assumes we know that the stem/preverb
#don't contain "м"
def fixNegatives(f):

    #There are a bunch of ways in which the negative
    #might be perfectly fine already. We check those
    #and if we're fine, just return the input.
    
    if "-м-" in f:

        return f

    elif "-мы-" in f:

        return f

    elif "-мЫ-" in f:

        return f

    elif "-м(ы)-" in f:

        return f

    #If there's a problem with the negative parsing
    else:

        #Fix problem for schwaful version of marker
        if "мы" in f or "мЫ" in f or "м(ы)" in f:

            #Surround the negative marker with boundaries
            f = f.replace("мы", "-мы-")
            f = f.replace("мЫ", "-мЫ-")
            f = f.replace("м(ы)", "-м(ы)-")

            #Get rid of extra boundaries
            while "--" in f:

                f = f.replace("--", "-")

            #Return fixed form
            return f

        #Same thing for schwaless version
        if "м" in f:

            f = f.replace("м", "-м-")

            while "--" in f:

                f = f.replace("--", "-")

        return f

#This function takes a list of verb forms as input,
#and tries to see if any morphemes contained within
#each form can be broken down into other morphemes
#from the forms. It returns the result as a list
def reparse(tf):

    stringTF = "\t".join(tf)

    #Set up a lexicon of morphemes, I'm seeding it
    #here with some we know already
    lexicon = ["уа", "уе", "ит", "кәа", "уА", "уЕ", "кәА"]

    #I'm ignoring the masdar here, because there's
    #some annoying overparsing based on small morphemes
    #like а- and -ра
    for item in tf[1:]:

        lexicon = lexicon + item.split("-")

    lexicon = list(set(lexicon))

    #Check whether any morpheme can be treated
    #as the concatenation of other morphemes
    for m in lexicon:

        #Technically 2-character strings could be
        #morphologically complex, but I restrict
        #myself to length 3 or more to prevent
        #too much overparsing
        if len(m) > 2:

            for tempIndex in range(1, len(m)):

                if m[:tempIndex] in lexicon and m[tempIndex:] in lexicon:

                    stringTF = stringTF.replace(m, m[:tempIndex] + "-" + m[tempIndex:])

                    break

    return stringTF.split("\t")

#This function takes a list of verb forms as input
#and returns a list with how many morpheme boundaries
#each form has.
def getBoundaries(tf):

    tempBoundaries = []

    for item in tf:

        tempBoundaries.append(item.count("-"))

    return tempBoundaries

#These lists are from script 4.5,
#see there for details. Basically they're
#counts of how many morpheme boundaries
#particular verb categories should contain.
boundaryCounts = [[2, 2, 2, 1, 3, 2, 3], [2, 3, 3, 1, 3, 2, 3], [3, 3, 3, 2, 4, 3, 4], [3, 4, 4, 2, 4, 3, 4], [4, 4, 4, 3, 5, 4, 5], [4, 5, 5, 3, 5, 4, 5], [2, 3, 3, 2, 4, 3, 4], [2, 4, 4, 2, 4, 3, 4], [3, 4, 4, 3, 5, 4, 5], [3, 5, 5, 3, 5, 4, 5], [4, 5, 5, 4, 6, 5, 6], [4, 6, 6, 4, 6, 5, 6], [2, 3, 3, 1, 4, 2, 3], [2, 4, 4, 1, 4, 2, 3], [3, 4, 4, 2, 5, 3, 4], [3, 5, 5, 2, 5, 3, 4], [4, 5, 5, 3, 6, 4, 5], [4, 6, 6, 3, 6, 4, 5], [2, 4, 4, 2, 5, 3, 4], [2, 5, 5, 2, 5, 3, 4], [3, 5, 5, 3, 6, 4, 5], [3, 6, 6, 3, 6, 4, 5], [4, 6, 6, 4, 7, 5, 6], [4, 7, 7, 4, 7, 5, 6]]

#Make sure we can differentiate adjacent preverbs
s = s.replace("PREV-PREV", "PREV-PREV2")

sList = s.split("\n")
s = ""
sOut = ""

tempForms = []
#tempGloss = ""

for entry in sList:

    #A list for the conjugated forms
    tempForms = entry.split("\t")[:-1]
    #tempGloss = entry.split("\t")[-1]

    #Some morphemes will always be present in particular positions. We check
    #for these morpheme boundaries below, adding them in if they aren't
    #already present. The way to do this is that if a string is supposed
    #to start with, say, "ba-", then we want the third character to be "-".
    #If it's not, we add a "-" in that position. The morphemes are:
    #Masdar must have а- at the start and -ра at the end
    #Pres. aff. must have -ит at the end
    #Pres. neg. must have -м at the end
    #Imp. neg. must have -н at the end
    #Abs. aff. must have -ны at the end
    #Abs. neg. must have -кәа at the end
    if not tempForms[0][1] == "-":

        tempForms[0] = tempForms[0][0] + "-" + tempForms[0][1:]

    if not tempForms[0][-3] == "-":

        tempForms[0] = tempForms[0][:-2] + "-" + tempForms[0][-2:]

    if not tempForms[1][-3] == "-":

        tempForms[1] = tempForms[1][:-2] + "-" + tempForms[1][-2:]

    if not tempForms[2][-2] == "-":

        tempForms[2] = tempForms[2][:-1] + "-" + tempForms[2][-1]

    if not tempForms[4][-2] == "-":

        tempForms[4] = tempForms[4][:-1] + "-" + tempForms[4][-1]

    if not tempForms[5][-3] == "-":

        tempForms[5] = tempForms[5][:-2] + "-" + tempForms[5][-2:]

    if not tempForms[6][-4] == "-":

        tempForms[6] = tempForms[6][:-3] + "-" + tempForms[6][-3:]

    #Just making sure the neg. abs. ends in the right morpheme
    if not tempForms[6].endswith("кәа") and not tempForms[6].endswith("кәА"):

        continue

    #We still want to do more automatic parsing if we can
    #There are common errors with the negative not being
    #parsed correctly. So we want to make sure "м", the
    #negative marker, is included as a separate morpheme.
    #We have to be careful with that grapheme appearing
    #in roots and preverbs though!
    #We've dealt with the only instances where it's word-
    #final, so every negative form should contain "-м-" or
    #"-мы-" or "-мЫ-"

    #Only try to fix things if the masdar fails to contain
    #this phoneme. Otherwise we'll do it manually
    if "м" not in tempForms[0]:

        tempForms[4] = fixNegatives(tempForms[4])
        tempForms[6] = fixNegatives(tempForms[6])

    #Automatic parsing to make sure all the morpheme
    #boundaries are there
    tempForms = reparse(tempForms)

    #If there isn't a conjugation pattern that has this
    #pattern of morpheme boundaries
    if not getBoundaries(tempForms) in boundaryCounts:

        #The continue line tells us to just ignore verbs
        #that can't be automatically parsed. The commented-
        #out code below allows for manual fixing of these
        #forms, if desired in the future, as well as spot-
        #checking of the automatically-parsed forms
        continue

        #print("Input correct forms by copy-pasting and fixing.")
        #tempForms = input(", ".join(tempForms) + ": ").split(", ")
        #Note that we save user input as is, without checking
        #whether one of the templates is matched. So the next
        #script still has to weed out forms based on whether
        #they match one of the patterns or not

    #else: #Spot-check 10% of automatic parses

        #if random.random() < 0.1:
        
            #if len(input(", ".join(tempForms) + "; if correct, hit Enter, else type: ")) > 0:

                #print("Input correct forms by copy-pasting and fixing.")
                #tempForms = input(", ".join(tempForms) + ": ").split(", ")

    #Store in output variable
    sOut += "\t".join(tempForms) + "\t" + "".join(str(n) for n in getBoundaries(tempForms)) + "\n"

#Save output
with open("5. morpheme boundaries.txt", encoding="utf-8", mode="w") as f:

    #Ignore final newline so we don't get an empty line in the output
    f.write(sOut[:-1])
