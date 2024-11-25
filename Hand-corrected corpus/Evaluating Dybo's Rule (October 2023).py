from itertools import product

#This script takes a corpus of Abkhaz verb forms as input,
#and asks, for each verb, whether there is any underlying
#representation such that, when Dybo's Rule is applied,
#the correct stress pattern is predicted.
#Dybo's Rule is defined as assigning primary stress to
#the leftmost accent that is not immediately followed
#by another accent. If no accent exists, stress is
#root-final.
#I closely follow Spruit (1986), who claims that there is
#one accent per element. For the functional morphemes
#in my corpus, they are all monoelemental, but roots
#and preverbs may have multiple elements. An element
#is a sequence CV(V), or a C (if not immediately
#followed by a vowel), or a V (if not immediately
#preceded by a consonant).
#I begin with the implementation of the following system
#for underlying accents, a simplification of Spruit's (1986)
#proposal without accentual allomorphy:
#C1 = unaccented, C2 = accented, C3 = unaccented (but на is
#accented), DEF = accented, INF = accented, NEG = unaccented,
#DYN is accented, DYN.IMP is unaccented, ABS is accented,
#NEG.ABS is unaccented, DYN.FIN is unaccented
#The code contains several sections which can be left in or
#commented out for implementing other variations of Abkhaz
#stress assignment.

accentStatus = {}

#Specify the accent of each functional morpheme
#A = accented, U = unaccented
accentStatus["DEF"] = "A"
accentStatus["INF"] = "A"

accentStatus["C1"] = "U"
accentStatus["C2"] = "A"
accentStatus["C3"] = "U"
accentStatus["NEG"] = "U"

accentStatus["DYN"] = "A"
accentStatus["DYN.FIN"] = "U"
accentStatus["DYN.IMP"] = "U"
accentStatus["ABS"] = "A"
accentStatus["NEG.ABS"] = "U"

#This function takes a phonological string (e.g. A-CaaCa-Ca)
#and a corresponding gloss string (e.g. DEF-R-INF), and a
#morpheme that appears in the gloss (e.g. R), and returns
#a phonological string and gloss string where the morpheme
#m has been divided into elements: [A-Caa-Ca-Ca, DEF-R0-R1-INF]
def parseElements(phonString, glossString, m, causative):

    #Get the phonological shape of m (e.g. CaaCa)
    phonList = phonString.split("-")
    glossList = glossString.split("-")
    phonMorpheme = phonList[glossList.index(m)]

    #Remove information about vowel quality (irrelevant)
    phonMorpheme = phonMorpheme.replace("A", "V")
    phonMorpheme = phonMorpheme.replace("Y", "V")
    phonMorpheme = phonMorpheme.replace("a", "v")
    phonMorpheme = phonMorpheme.replace("y", "v")

    #Add hyphens corresponding to element boundaries

##    #Edge case to deal with the causative prefix:
##    #it's always the first segment of the "root"
##    if causative and m == "R":
##
##        #Edge case for stressed causative prefix CY
##        if phonMorpheme.startswith("CY"):
##
##            phonMorpheme = phonMorpheme[:2] + "-" + phonMorpheme[2:]
##
##        #Non-edge case: causative is just C
##        else:
##
##            phonMorpheme = phonMorpheme[0] + "-" + phonMorpheme[1:]

    #Postvocalic boundary
    phonMorpheme = phonMorpheme.replace("V", "V-")    
    phonMorpheme = phonMorpheme.replace("v", "v-")

    #Add boundaries in consonant clusters
    while "CC" in phonMorpheme:

        phonMorpheme = phonMorpheme.replace("CC", "C-C")

    #Remove redundant boundaries
    while "--" in phonMorpheme:    

        phonMorpheme = phonMorpheme.replace("--", "-")

    #Treat vv as a single element (following Spruit 1986)
    #*Stressed* long vowels don't occur in the corpus,
    #so we can limit ourselves to lowercase v here
    phonMorpheme = phonMorpheme.replace("v-v", "vv")

    #Get rid of element boundary after final vowel
    if phonMorpheme.endswith("v-") or phonMorpheme.endswith("V-"):

        phonMorpheme = phonMorpheme[:-1]

    #Update phonList with the newly parsed form
    phonList[glossList.index(m)] = phonMorpheme

    #Add corresponding hyphens to the gloss
    newMorphemeGloss = ""

    #The number of root elements is the number of hyphens
    #in phonMorpheme plus one    
    for i in range(phonMorpheme.count("-") + 1):

        newMorphemeGloss += m + str(i) + "-"

    if newMorphemeGloss.endswith("-"):

        newMorphemeGloss = newMorphemeGloss[:-1]

    #Replace the old gloss with the new gloss
    glossList[glossList.index(m)] = newMorphemeGloss

    #Return new forms
    return ["-".join(phonList), "-".join(glossList)]

#This function takes in a gloss string(e.g. "DEF-R0-R1-R2-INF")
#and returns the number of morphemes that start with m. For example,
#for m = "R", this function returns 2. It counts the number of
#elements that are in the morpheme m in glossString
def countElements(glossString, m):

    glossList = glossString.split("-")
    counter = 0

    for g in glossList:

        if g.startswith(m):

            counter += 1

    return counter

#This function takes in a list of accents (e.g. ["A", "U", "A"])
#and a corresponding list of glosses (e.g. ["DEF", "R0", "INF"]),
#and applies Dybo's Rule to the form. It returns an integer: the
#index of the element that Dybo's Rule predicts should carry
#primary stress
def applyDybo(accentList, glossList):

    #If there is no accent, stress is root-final
    if "A" not in accentList:

        #Loop through the glossList backwards to quickly
        #find the final element glossed as part of the root
        for i in range(len(glossList) - 1, -1, -1):

            #If this is part of the root
            if glossList[i].startswith("R"):

                #It's the final element of the root since we're
                #looping backwards, so just return this index:
                #stress is on the final element of the root
                return i

    #If there is at least one underlying accent, we apply Dybo's Rule
    #proper, stressing the leftmost accent not immediately followed
    #by an accent
    else:

        #Go through each accent from left to right
        for i in range(len(accentList)):

            #If this is the final accent, and we haven't
            #assigned stress yet, this is the morpheme
            #that should be stressed
            if i == len(accentList) - 1:

                return i

            #For any non-final element
            else:

                #Assign stress here if it's an A followed by a U
                if accentList[i] == "A" and accentList[i + 1] == "U":

                    return i

#This is the function to evaluate Dybo's Rule against a verb's 7 forms.
#It takes in a verb (all forms, orthography, phonology,
#gloss), and a list of accents for each element in the root,
#and an optional list of accents for each element in the preverb,
#and returns a number between 0 and 7 (both inclusive) for
#how many of the verb's forms had their stress correctly
#predicted.
def evaluateDybo(v, rAccent, pAccent = []):

    evaluation = []
    methods = []

    #Look at all seven verb forms (the orthography has
    #indices starting at 0 and going up by 3)
    for i in [0, 3, 6, 9, 12, 15, 18]:

        method = "C"

        #Extract phonology and gloss information
        #We make a copy oldGlossList, since we'll
        #modify glossList in the code below, but we
        #still want access to the original (in particular,
        #to know where the root is so we can assign root-
        #final stress if needed)
        phonList = v[i + 1].split("-")
        glossList = v[i + 2].split("-")
        oldGlossList = glossList[::]

        #Replace the glosses with the accent of the relevant
        #morpheme
        for j in range(len(glossList)):

            #If this element is part of the root
            if glossList[j].startswith("R"):

                #Replace with the relevant accent specification
                #from the rAccent list
                glossList[j] = rAccent[int(glossList[j][1:])]

            #If this element is part of the preverb
            elif glossList[j].startswith("PREV"):

                #Replace with the relevant accent specification
                #from the pAccent list
                glossList[j] = pAccent[int(glossList[j][4:])]

            #If this is a functional morpheme
            else:

                #Special code for C3 (н)а, which exceptionally is accented
                #This code overgenerates, and treats C3 ҳа as A rather than U,
                #I've left this error in at the moment since this morpheme doesn't
                #occur in my data at all
                if glossList[j] == "C3" and phonList[j] in ["CA", "Ca", "A", "a"]:

                    glossList[j] = "A"

                #Make C3 accented in causatives (Spruit 1986: 71)
                elif glossList[j] == "C3" and v[24] == "Y":

                    glossList[j] = "A"
                    method = "A"

                #The negative prefix (NEG, but not when i = 6,
                #which is the negative suffix in the present tense)
                #is accented in causatives (Spruit 1986: 72)
                elif glossList[j] == "NEG" and not i == 6 and v[24] == "Y":

                    glossList[j] = "A"
                    method = "A"

                #The negative prefix is accented for C1-C2-R roots
                elif glossList[j] == "NEG" and not i == 6 and v[21] == "C1-C2-R":

                    glossList[j] = "A"
                    method = "A"

                #Use the dictionary accentStatus to look up the
                #accent status of this morpheme if none of the above
                #edge cases apply
                else:

                    glossList[j] = accentStatus[glossList[j]]

        #Now we can pass the list of accents (e.g. [A, U, U, A]) to a
        #function which will tell us which morpheme Dybo's Rule
        #predicts will be stressed, and compare that against the
        #actual corpus data

        #Implement pre-stress
        #1) Single-element absolutive-only unaccented verb roots without preverbs
        if countElements("-".join(oldGlossList), "R") == 1 and glossList[oldGlossList.index("R0")] == "U" and "PREV" not in v[21] and "C2" not in oldGlossList and "C3" not in oldGlossList:

            stressIndex = oldGlossList.index("R0") - 1
            method = "A"

        #2) Non-accent-initial absolutive-only verbs with a causative and no preverbs
        elif glossList[oldGlossList.index("R0")] == "U" and v[24] == "Y" and "PREV" not in v[21] and "C2" not in oldGlossList and "C3" not in oldGlossList:

            stressIndex = oldGlossList.index("R0") - 1
            method = "A"

        #Elsewhere case: Dybo's Rule
        else:
            
            stressIndex = applyDybo(glossList, oldGlossList)

        #Consistent initial stress
        #stressIndex = 0

        #Consistent final stress
        #stressIndex = len(glossList) - 1

        #Consistent root-initial stress
        #stressIndex = oldGlossList.index("R0")

        #Consistent root-final stress
        #for i in range(len(oldGlossList) - 1, -1, -1):

            #if oldGlossList[i].startswith("R"):

                #stressIndex = i

                #break

        #Now we have a prediction, and we want to check if it matches
        #the data. Does the predicted morpheme have a stressed vowel
        #(marked by a capital letter A, Y, V, G, E)?
        if True in [bool(x in phonList[stressIndex]) for x in ["A", "Y", "V", "G", "E"]]:

            #If yes, add 1 for a correct prediction
            evaluation.append(1)

        else:
            
            #If no, add 0 for an incorrect prediction
            evaluation.append(0)

        methods.append(method)

    return [evaluation, methods]

verbs = []

with open("Corpus (test).txt", encoding = "utf-8") as f:

    verbs = f.read().split("\n")

verb = []
tempScore = []
tempHighscore = []
tempHighAccents = ""
verbsCorrect = 0
verbsTotal = 0
totalCorrect = 0
totalTotal = 0
breakFlag = False

#Evaluate each verb
for v in verbs:

    verb = v.split("\t")
    breakFlag = False

    #Undo coalescence with the dynamic marker

    #If the verb has coalescence
    if "R.DYN" in verb[5]:

        #Undo coalescence in present affirmative and negative
        #That's forms in verb[3] and verb[6]
        for i in [3, 6]:

            #Undo coalescence in orthography (stressed/unstressed)
            #This isn't strictly necessary I think, the code will
            #run based on the phonology and gloss
            verb[i] = verb[i].replace("О", "а-уА")
            verb[i] = verb[i].replace("о", "а-уа")

            #Undo coalescence in phonology (stressed/unstressed)
            verb[i + 1] = verb[i + 1].replace("O", "a-CA")
            verb[i + 1] = verb[i + 1].replace("o", "a-Ca")

            #Undo coalescence in gloss
            verb[i + 2] = verb[i + 2].replace("R.DYN", "R-DYN")

    #Code for verbs with preverbs
    if "PREV" in verb[21]:

        ms = []
        tempScore = []
        tempHighscore = [0, 0, 0, 0, 0, 0, 0]

        #We need to know how many elements are in the preverb and root,
        #so that we know how many accent specifications they need. We
        #also check that this number doesn't vary across the seven forms,
        #since if it does, the preverb shows allomorphy that we can't
        #account for.
        #We do the same for the root, for the same reasons.
        numPrevElements = []
        numRootElements = []

        #This code breaks up both root and preverb into elements in each of the 7 forms
        for i in [0, 3, 6, 9, 12, 15, 18]:

            tempPhonString, tempGlossString = parseElements(verb[i + 1], verb[i + 2], "PREV", verb[24] == "Y")
            verb[i + 1] = tempPhonString
            verb[i + 2] = tempGlossString

            numPrevElements.append(countElements(tempGlossString, "PREV"))

            tempPhonString, tempGlossString = parseElements(verb[i + 1], verb[i + 2], "R", verb[24] == "Y")
            verb[i + 1] = tempPhonString
            verb[i + 2] = tempGlossString

            numRootElements.append(countElements(tempGlossString, "R"))

        #This code checks for preverb allomorphy, and exits if we find it, warning the user
        for i in range(1, len(numPrevElements)):

            if not numPrevElements[i] == numPrevElements[0]:

                print(f"{verb[0]} {verb[21]} {verb[23]}: PREVERB ALLOMORPHY. VERB NOT EVALUATED.")

                breakFlag = True

                break

        #This code checks for root allomorphy, and exits if we find it, warning the user
        if not breakFlag:

            for i in range(1, len(numRootElements)):

                if not numRootElements[i] == numRootElements[0]:

                    print(f"{verb[0]} {verb[21]} {verb[23]}: ROOT ALLOMORPHY. VERB NOT EVALUATED.")

                    breakFlag = True

                    break

        #This code skips the current verb if we've found root or preverb allomorphy
        if breakFlag:

            continue

        #Go through every possibility for accents of the preverb
        for prevAccent in product(["U", "A"], repeat = numPrevElements[0]):

            #Go through every possibility for accents of the root
            for rootAccent in product(["U", "A"], repeat = numRootElements[0]):

                #Edge case for causatives: they copy the accent of the following
                #root element (Spruit 1986: 70)
                if verb[24] == "Y":

                    if not rootAccent[0] == rootAccent[1]:

                        continue

                tempScore, ms = evaluateDybo(verb, rootAccent, prevAccent)

                #If we do better than our previous highscore
                if tempScore.count(1) > tempHighscore.count(1):

                    #Update highscore to current score
                    #Store the rootAccent that led to this score
                    tempHighscore = tempScore
                    tempHighAccents = [prevAccent, rootAccent]

                #We're never going to beat accounting for all 7 forms
                if tempHighscore.count(1) == 7:

                    print(verb[23] + " " + str(ms))

                    break

        #print(f"{verb[0]} {verb[21]} {verb[23]}: {tempHighscore} with {str(tempHighAccents)}")
        totalCorrect += tempHighscore.count(1)
        totalTotal += 7

        if tempHighscore.count(1) == 7:

            verbsCorrect += 1

        #else:

            #print(f"{verb[0]} {verb[21]} {verb[23]}: {tempHighscore} with {str(tempHighAccents)}")

        verbsTotal += 1

    #Code for verbs that lack preverbs
    else:

        ms = []
        tempScore = []
        tempHighscore = [0, 0, 0, 0, 0, 0, 0]

        numRootElements = []
        
        #This code breaks up the root into elements in each of the 7 forms
        for i in [0, 3, 6, 9, 12, 15, 18]:

            tempPhonString, tempGlossString = parseElements(verb[i + 1], verb[i + 2], "R", verb[24] == "Y")
            verb[i + 1] = tempPhonString
            verb[i + 2] = tempGlossString

            numRootElements.append(countElements(tempGlossString, "R"))

        #This code checks for root allomorphy, and exits if we find it, warning the user
        for i in range(1, len(numRootElements)):

            if not numRootElements[i] == numRootElements[0]:

                print(f"{verb[0]} {verb[21]} {verb[23]}: ROOT ALLOMORPHY. VERB NOT EVALUATED.")

                breakFlag = True

                break

        #This code skips the current verb if we've found root allomorphy
        if breakFlag:

            continue

        #Go through every possibility for accents of the root
        for rootAccent in product(["U", "A"], repeat = numRootElements[0]):

            #Edge case for causatives: they copy the accent of the following
            #root element (Spruit 1986: 70)
            if verb[24] == "Y":

                if not rootAccent[0] == rootAccent[1]:

                    continue

            #See how many forms this rootAccent accounts for
            tempScore, ms = evaluateDybo(verb, rootAccent)

            #If we do better than our previous highscore
            if tempScore.count(1) > tempHighscore.count(1):

                #Update highscore to current score
                #Store the rootAccent that led to this score
                tempHighscore = tempScore
                tempHighAccents = rootAccent

            #We're never going to beat accounting for all 7 forms
            if tempHighscore.count(1) == 7:

                print(verb[23] + " " + str(ms))

                break

        totalCorrect += tempHighscore.count(1)
        totalTotal += 7

        if tempHighscore.count(1) == 7:

            verbsCorrect += 1

        #else:

            #print(f"{verb[0]} {verb[21]} {verb[23]}: {tempHighscore} with {str(tempHighAccents)}")

        verbsTotal += 1

print(f"Total correct predictions: {totalCorrect}")
print(f"Total forms predicted: {totalTotal}")
print(f"Verbs with 7/7 correct predictions: {verbsCorrect}")
print(f"Verbs evaluated: {verbsTotal}")
