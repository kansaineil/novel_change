import sys
import os


import spacy
import scispacy
import csv

import time
import pprint

# Load the SciSpacy large model
nlp = spacy.load("en_core_sci_lg")

input_spec="batch_2561.txt"
output_specs="batch_2561.csv"

no_option=True
print(f"{sys.argv=}")
for i in range(len(sys.argv)):
    if sys.argv[i]=="-i":
        if i+1<len(sys.argv):
            input_spec=sys.argv[i+1]
            no_option=False
            break
print(f"{input_spec=}")

input_files=[]
if input_spec=="all":
    for item in os.listdir("."):
        if not item.startswith("concordance-download_"):continue
        if not item.endswith(".txt"):continue
        input_files.append(item)
else:
    input_files.append(input_spec)
    if no_option==False:
        for item in os.listdir("."):
            if not item.startswith("concordance-download_"):continue
            if not item.endswith(".txt"):continue
            if item==input_spec:continue
            os.unlink(item)

print(f"{input_files=}")

for input_file in input_files:
    print(f"Processing {input_file=} ...")
    downloaded = []
    with open(input_file) as f:
        lines = f.readlines()

    # Prepare the CSV file
    output_file=input_file.replace("concordance-download_","collocation_novels_").replace(".txt","_sci.csv")
    #Maria's choice of output
    if no_option==True:
        output_file=output_specs
    print(f"Processing {output_file=} ...")
    
    with open(output_file, mode="w", newline="") as csv_file:
        fieldnames = ["Index","Original Text", "Novel#", "Relevant Noun", "Relevant Lemma", "Position","Year"]
        
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        line_number = 0
        with open(input_file) as f:
            for file_line in f:
                
                if line_number % 1000 == 0:
                        print(line_number, time.ctime(time.time()))
                #if line_number == 0:
                    #line_number = line_number + 1
                    #continue  # header
                line_number = line_number + 1
                file_line=file_line.strip()
                if len(file_line)==0:continue
                tokens = file_line.strip().split("\t")
                sentence=tokens[1]
                sent_index=tokens[0]
                doc_sentence = nlp(sentence) # only the whole sentence
                abstract_year= tokens[2]
                novel_indeces = [] # indeces "novel" that occurs in doc_sentence
                # Iterate over the tokens
                for index, token in enumerate(doc_sentence):
                    # Check if the token is "novel"
                    if token.lemma_ == "novel":novel_indeces.append(index)
                    if token.lemma_ == "Novel":novel_indeces.append(index)
                #print(f"\n\n{line_number} \n {sentence} \n {novel_indeces}\n\n")
                for novel_index in novel_indeces:
                    position="N/A"
                    token=doc_sentence[novel_index]

                    # Check head tokens up to 2 levels up the dependency tree
                    noun = None
                    head_token = token.head
                    for _ in range(2):
                        if head_token.pos_ == "NOUN" and noun is None:
                            noun = head_token
                            if noun.i < token.i:
                                position = "predicative"
                            else:
                                position = "attributive"
                            break
                        head_token = head_token.head

                    # Check children tokens for predicative usage
                    for child in token.children:
                        if child.dep_ == "attr" and child.pos_ == "NOUN" and noun is None:
                            noun = child
                            if noun.i < token.i:
                                position = "predicative"
                            else:
                                position = "attributive"
                            break
                    # Check the head token's children for the nominal subject in predicative constructions
                    for child in token.head.children:
                        if child.dep_ == "nsubj" and (child.pos_ == "NOUN" or child.pos_ == "PRON") and noun is None:
                            noun = child
                            if noun.i < token.i:
                                position = "predicative"
                            else:
                                position = "attributive"
                            break

                    relevant_noun = "N/A" if noun is None else noun.text
                    relevant_lemma = "N/A" if noun is None else noun.lemma_
                    #fieldnames = ["Original Text", "Index", "Relevant Noun", "Relevant Lemma", "Position","Year"]
                    row={
                        "Index": sent_index,
                        "Original Text": sentence,
                        "Novel#" : novel_index,
                        "Relevant Noun": relevant_noun,
                        "Relevant Lemma": relevant_lemma,
                        "Position" : position,
                        "Year": abstract_year
                    }
                    writer.writerow(row)

                    
 
