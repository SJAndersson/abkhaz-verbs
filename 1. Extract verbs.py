#The aim of this script is to extract the infinitive, pres. (positive and
#negative), imperative (positive and negative), and absolutive (pos./neg.)
#from an Abkhaz dictionary. It also provides
#the gloss template, e.g. C1-C2-Prev[erb]-R[oot] for each form.
#It takes full dictionary.txt as input
#It produces the outputs as verb forms.txt
#without converting to orthography
#NOTE: the input must have all 114 labile verbs manually changed so that
#they don't contain [labile] and do contain one instance only of [tr. or
#[intr. immediately after the headword

#Reading the dictionary contents into a string
s = ""

with open("full dictionary (manual labile replacement).txt", encoding="utf-8") as f:

    s = f.read()

#Splitting it up at verb entries
#All verb entries, as far as I can tell, have [tr. or [intr.
#immediately after the headword now
#I'm replacing these strings by [verb] and using that to split
s = s.replace("[tr.", "[verb]")
s = s.replace("[intr.", "[verb]")

#Some verbs have a bracketed number between headword and grammatical
#tag. We want to get rid of those, because the code below depends on
#these things being directly adjacent.
s = s.replace(" (1)", "")

#Some forms are split across pages, so we want to remove page numbers
#These are of the form \n- page.number.here -\n, and there are 589 pages.
#I moved this code up a bit, because I was having problems with page
#boundaries immediately preceded by # because of the code block below
#this one. 
for i in range(1, 590, 1):

    s = s.replace("\n- " + str(i) + " -\n", "\n")

#Some " / " strings are crucial because they split up positive and negative
#verb forms. But they're variably read as " # " rather than " / ", so I
#fix that here. Some slashes also straddle newlines, so we fix that too.
#Sometimes a space doesn't show up on one side of the symbol, so I fix that.
s = s.replace("# ", " # ")
s = s.replace("  ", " ")
s = s.replace(" #\n", " /\n")
s = s.replace(" /\n", " / ")
s = s.replace("\n# ", "\n/ ")
s = s.replace("\n/ ", " / ")
s = s.replace(" # ", " / ")

#Some forms separated by comma and newline rather than comma and space
#don't get picked up. I can easily fix that later, but I can also
#just fix it here
s = s.replace(",\n", ", ")

#Good verb entries contain " / ", which is usually followed by a negative form.
#But some just have the slash without a following negative, and move straight on
#to the next tense. These are something like "[pres.] blah / [past]". So we get
#rid of " / [" in favor of "[" here to solve this problem
s = s.replace(" / [", "[")

#glossStr can either contain -S for stem or -R for root. We normalize to -R.
s = s.replace("-S", "-R")

#One form has " (poten.) " before the negative, get rid of that
s = s.replace(" (poten.)", "")

#Some forms don't contain "1." before the definition, fix that
s = s.replace("to bore", "1. to bore")
s = s.replace("to smoke", "1. to smoke")

#One verb has " (a¡mla) " 'hunger' before the absolutive, fix that
s = s.replace(" (a¡mla) ", " ")

#Some verbs have " (C1) " before absolutive forms
s = s.replace(" (C1) ", " ")

sList = s.split("[verb]")

#We want to go through this list, and extract forms for any verb where all
#relevant forms exist. Since headwords precede the [verb] string that we're
#splitting by, a headword and its conjugated forms will appear at different,
#but immediately adjacent, places in sList. 
#We loop by index to be able to access earlier entries easily
#(Or actually I changed the code so that's irrelevant now, but whatever)

tempHeadWord = ""
headword = False
realInf = ""
realPresAff = ""
realPresNeg = ""
realImpAff = ""
realImpNeg = ""
realAbsAff = ""
realAbsNeg = ""
glossStr = ""
conjFull = ""
conjPres = ""
conjImp = ""
conjAbs = ""
glossFull = ""
output = ""
startIndex = 0
conjIndex = 0

allowedGlossStr = ["C1-R", "C1-Prev-R", "C1-Prev-Prev-R", "C1-C2-R", "C1-C2-Prev-R", "C1-C2-Prev-Prev-R", "C1-C3-R", "C1-Prev-C3-R", "C1-Prev-Prev-C3-R", "C1-C2-C3-R", "C1-C2-Prev-C3-R", "C1-C2-Prev-Prev-C3-R"]

for i in range(len(sList)):

    #If this condition is true, we have a verb, and now we need to check
    #that all conjugated forms are present
    if headword:
        #print("tempHeadword")
        #input(tempHeadword)
        headword = False
        #conjFull is the string containing all conjugated forms somewhere
        conjFull = sList[i]

        #If there are non-finite forms, we want to make sure presents
        #are not non-finite. This index helps us do this check by
        #seeing where the "Non-" part of "Non-fin." occurs.
        if "Non-" in conjFull:

            conjIndex = conjFull.index("Non-")

        else:

            conjIndex = 100000

        #This is to get the glossStr, which always appear in the first line
        #of a verb entry
        glossFull = conjFull.split("\n")[0]
        #print("glossFull")
        #input(glossFull)
        #-R is always part of the glossStr, so its presence indicates we
        #have a glossStr to extract
        if "-R" in glossFull:

            #A well-formed glossStr starts with either [C or [Prev
            if "[C" in glossFull:

                startIndex = glossFull.index("[C") + 1

            elif "[Prev" in glossFull:

                startIndex = glossFull.index("[Prev") + 1

            else:

                startIndex = -1

            #If we have a seemingly well-formed glossStr
            if startIndex > -1:

                #Extract it
                glossStr = glossFull[startIndex:glossFull.index("-R") + 2]
                
                #We want to make sure we have a glossStr we can understand. So we
                #only allow a few different ones. We have to get rid of parentheses
                #and other junk first though.

                #These are things that shouldn't be in parentheses
                glossStr = glossStr.replace("(C1)", "C1")
                glossStr = glossStr.replace("(C2)", "C2")

                #Anything else in parentheses we should ignore. This assumes there
                #is only one set of parentheses left, which I think is always true.
                if "(" in glossStr:
                    
                    glossStr = glossStr[:glossStr.index("(")] + glossStr[glossStr.index(")") + 1:]

                #print("glossStr")
                #input(glossStr)

                #Now we need to check we have one of the allowed glossStr strings left:
                if glossStr in allowedGlossStr:

                    #These three start strings tell us we're dealing with simple verb cases rather than weird
                    #reflexives, subjective version verbs, and so on
                    if conjFull.startswith("]") or conjFull.startswith(" dynamic]"):
                        #Make sure all TAM combinations are found
                        if "[pres.]" in conjFull and "[imper.]" in conjFull and "Abs." in conjFull:

                            #This string contains the present forms
                            conjPres = conjFull[conjFull.index("[pres.]") + 7:conjFull.index("[imper.]")]
                            #This string contains the imperative forms
                            conjImp = conjFull[conjFull.index("[imper.]") + 8:conjFull.index("Abs.")]
                            #This string contains the absolutive forms (up to definition of verb,
                            #which starts with "1."
                            conjAbs = conjFull[conjFull.index("Abs.") + 4:conjFull.index("1.")]

                            #Make sure all verbs have negative forms for each TAM combination
                            #These are indicacted with " / " between positive and negative forms
                            if " / " in conjPres and " / " in conjImp and " / " in conjAbs:
                                #Get rid of statives, because more morphology is too hard.
                                if "-up" not in conjPres and "-u¡p" not in conjPres:

                                    #At this point we know all forms are present, and we can save them
                                    #We only split by " ", because some verb forms will have newlines
                                    #in the middle, and we don't want to cut those up into two
                                    #We also want to get rid of them afterwards with a replace command
                                    #because otherwise, they'll mess up the output file
                                    realInf = tempHeadword.replace("\n", "")
                                    realPresAff = conjPres.strip().split(" ")[0].replace("\n", "")
                                    realPresNeg = conjPres[conjPres.index(" / ") + 3:].split(" ")[0].replace("\n", "")
                                    realImpAff = conjImp.strip().split(" ")[0].replace("\n", "")
                                    realImpNeg = conjImp[conjImp.index(" / ") + 3:].split(" ")[0].replace("\n", "")
                                    realAbsAff = conjAbs.strip().split(" ")[0].replace("\n", "")
                                    realAbsNeg = conjAbs[conjAbs.index(" / ") + 3:].split(" ")[0].replace("\n", "")

                                    #print("Output")
                                    #input(" ".join([realInf, realPresAff, realPresNeg, realPastAff, realPastNeg, realImpAff, realImpNeg]))

                                    #Some verbs are of the form object, new word, verbal complex, and I only extract the first word
                                    #This means all verb forms are given as the same, just the object. We ignore those by checking
                                    #that forms are non-identical
                                    if not realPresAff == realPresNeg:
                                        #Save the verb forms in a tab-separated string
                                        output += "\t".join([realInf, realPresAff, realPresNeg, realImpAff, realImpNeg, realAbsAff, realAbsNeg, glossStr]) + "\n"

    #We check for potential verb headwords at the end of each item
    #since we split by verb tag, and the verb tag immediately
    #precedes each headword
    tempHeadword = sList[i].split()[-1]
    #We shouldn't include a morpheme boundary in this condition, because
    #verbs that underlyingly start in /a/ don't have this boundary.
    if tempHeadword.startswith("a"):
        #We can't check if it endswith the infinitive suffix because
        #some entries end in numbers for footnotes
        if "-ra" in tempHeadword or "-ra¡" in tempHeadword:
            #At this point we have a headword, and the next item will
            #contain the conjugated forms
            headword = True

#Save the outputs to a text file
with open("1. verb forms.txt", encoding="utf-8", mode="w") as f:
    #Ignore the last newline character
    f.write(output[:-1])           
