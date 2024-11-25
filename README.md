# abkhaz-verbs
Python code for an Abkhaz verb corpus

## Description

This repository contains a series of Python 3 scripts to be run in order, which create a corpus database of seven inflected forms each for several hundred Abkhaz verbs. I also provide a hand-corrected final corpus, as well as a script for evaluating linguistic theories of stress placement against the data. For a more complete description, see the details in Andersson (2024).

## Input and output format

The input is a plaintext version of Yanagisawa's (2010) dictionary of Abkhaz. The output of the corpus creation scripts is a plaintext file containing information about one verb on each tab-separated line. Each of the seven inflected forms of each verb is represented three times: once in Abkhaz orthography (e.g. с-аа-гЫло-ит), once in a phonological transcription scheme where C = consonant, g = glide or high vowel (e.g. C-aa-CYCo-gC), and once in a glossed form which shows which slots in the Abkhaz verbal template are filled (e.g. C1-PREV-R.DYN-DYN.FIN). Hyphens represent morpheme boundaries, capitalisation represents stress. After these 7 x 3 = 21 columns, the hand-corrected corpus contains additional information about the verb's argument structure, grammatical information, and a translation. 

## Acknowledgements

This work was only possible thanks to Tamio Yanagisawa, who kindly provided me with a PDF version of his dictionary. I am grateful to him for sharing his work with me, and for giving me permission to share the final corpus I have created.

## How to cite

Please cite the following when using data or code from this repository: the ultimate source of the data, my work describing the corpus, and this GitHub repo. Suggested citations:

Andersson, S. (2024). abkhaz-verbs. GitHub repository: <https://github.com/SJAndersson/abkhaz-verbs> [Accessed YYYY-MM-DD]

Andersson, S. (2024). The Phonetics and Phonology of Abkhaz Word Stress. PhD Dissertation: Yale University.

Yanagisawa, T. (with Tsvinaria-Abramishivili, A.). (2010). Analytic Dictionary of Abkhaz. Hitsuji Shobo.
