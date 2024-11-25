#This file takes verb forms.txt as its input,
#and outputs the same data in the same format,
#but with punctuation and other extraneous
#things removed. The output is in
#verb forms clean.txt

s = ""
sList = []

#Read the file into a string
with open("1. verb forms.txt", encoding="utf-8") as f:

    s = f.read()

#There are various indications of optionality
#within forms. We want to get rid of these, so
#we just have a replace command for each one.
#Optional forms are separated by #. Below I keep
#the first option arbitrarily, except I keep
#feminine forms for imperatives
s = s.replace("s#z", "s")
s = s.replace("z#s", "z")
s = s.replace("zy#sy", "zy")
s = s.replace("sy#zy", "sy")
s = s.replace("s#(z)", "s")
s = s.replace("sy#(zy)", "sy")
s = s.replace("a#r", "a")
s = s.replace("u#b#w", "b")
s = s.replace("u#by", "by")
s = s.replace("u#b", "b")
s = s.replace("a¡#ry¡", "a¡")
s = s.replace("a#y", "a")

#Some optional forms are separated by /. Here we
#fix those as well.
s = s.replace("sy¡/zy¡", "sy¡")
s = s.replace("z/s", "z")

#Two forms somehow contain "Abs." for no reason
s = s.replace("Abs.", "")

#One form contains equals signs for optionality
s = s.replace("∞yzy=∞yz", "∞yz(y)")
s = s.replace("∞yzy¡=∞yzy", "∞yzy¡")
s = s.replace("∞yzy¡=∞yz(y)", "∞yzy¡")
s = s.replace("∞yzy¡=∞yz", "∞yzy¡")

#One form contains a random palatalization sign
s = s.replace("n!;", "n")

#Two forms have English "or" at the end of abs. neg.
s = s.replace("-k´aor", "-k´a")

#We do some punctuation removal here, where we need
#to remove characters independently of where in a verb
#form they occur. # is only included here because we've
#dealt with the important # cases above. Semi-colons occur
#legitimately as a diacritic, but also randomly after @.
s = s.replace("@;", "@")
s = s.replace("<", "")
s = s.replace("@", "")
s = s.replace("{", "")
s = s.replace("}", "")
s = s.replace("]", "")
s = s.replace("*", "")
s = s.replace("!", "")
s = s.replace(".", "")
s = s.replace("#", "")

#Some strings contain parenthesized forms for optionality.
#A few of these we want to actually deal with, and this is
#done below. Most are parentheses we don't care about, e.g.
#extra info about ungrammatical forms, versions of the
#negative with an intensifier, and just things that should
#be part of the next word, but a space was missed. After
#dealing with the cases we want to deal with, everything
#after ( in a string is garbage, and can be thrown out.

#Keep optional a, which occurs in optionally truncatable
#imperatives.
#This is an arbitrary decision. It probably results in
#some more uniformity across the paradigm.
s = s.replace("(a)", "a")

#Change the brackets around optional schwa, so these
#don't get deleted. We'll change them back later.
s = s.replace("(y)", "{y}")

#I think this only affects one verb, stem aai. It's an
#arbitrary decision. Again it results in more paradigm
#uniformity.
s = s.replace("(i)", "i")

#One imperative has an optional repeated 2sg marker
#it looks like. Don't know what that's about, but I'm
#removing it arbitrarily.
s = s.replace("(by)", "")

#Remove the optional intensifier in some negatives.
s = s.replace("(ӡa-)", "")

#Later on, we'll want glosses to be upper case.
#That's kind of standard anyway. So we implement
#that here.
s = s.replace("Prev", "PREV")

#Other replacements have to be done based on where
#in a form something occurs. We deal with these by
#just looping through each form. For that we need
#a list of forms.
#Split it so that each verb entry (seven forms)
#constitutes one item in the list
sList = s.split("\n")

for entry in sList:

    #Verb forms are split by tabs within lines
    #We look at all except the last column, since
    #that's reserved for glosses
    for verb in entry.split("\t")[:-1]:

        #Get rid of numbers
        for i in range(1, 10):

            if str(i) in verb:

                s = s.replace(verb, verb.replace(str(i), ""))
                verb = verb.replace(str(i), "")
        
        #Get rid of commas and anything after them
        if "," in verb:
            #We do replacements straight on the string
            s = s.replace(verb, verb[:verb.index(",")])
            #Every time we replace something, we need to
            #update verb. If not, we're going to try to
            #replace strings that don't exist if a single
            #verb has multiple replacements.
            verb = verb[:verb.index(",")]

        #> and text after that character is garbage
        if ">" in verb:

            s = s.replace(verb, verb[:verb.index(">")])
            verb = verb[:verb.index(">")]

        #Any open parentheses left now have garbage to
        #their right. So we throw that away.
        if "(" in verb:

            s = s.replace(verb, verb[:verb.index("(")])
            verb = verb[:verb.index("(")]
        
        #Remove final right parentheses. Some of these are
        #just random punctuation. Others are part of a
        #genuine parenthetical, but we got rid of the
        #rest of the parenthetical earlier
        if verb.endswith(")"):

            s = s.replace(verb, verb[:-1])
            verb = verb[:-1]

        #Open square brackets are also nonsense
        if "[" in verb:

            s = s.replace(verb, verb[:verb.index("[")])
            verb = verb[:verb.index("[")]

#Replace brackets around optional schwa, back to normal.
s = s.replace("{y}", "(y)")

#Save the results
with open("2. cleaned.txt", encoding="utf-8", mode="w") as f:

    f.write(s)
