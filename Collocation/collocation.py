import sys
import os


import spacy
import scispacy
import csv

# Load the SciSpacy large model
nlp = spacy.load("en_core_sci_lg")

input_spec="concordance-download_1985.txt"
output_specs="maria_wahatever.csv"

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

    for i in range(len(lines)):
        if i == 0: continue  # header
        tokens = lines[i].strip().split("\t")
        line = " ".join(tokens[2:5])
        downloaded.append(line)

    # Prepare the CSV file
    output_file=input_file.replace("concordance-download_","collocation_novels_").replace(".txt","_sci.csv")
    #Maria's choice of output
    if no_option==True:
        output_file=output_specs
    print(f"Processing {output_file=} ...")
    with open(output_file, mode="w", newline="") as csv_file:
        fieldnames = ["Original Text", "Relevant Noun", "Relevant Lemma"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Process each text
        for text in downloaded:
            doc = nlp(text)

            # Iterate over the tokens
            for token in doc:
                # Check if the token is "novel"
                if token.text.lower() == "novel":
                    noun = None

                    # Check head tokens up to 2 levels up the dependency tree
                    head_token = token.head
                    for _ in range(2):
                        if head_token.pos_ == "NOUN" and noun is None:
                            noun = head_token
                        head_token = head_token.head

                    # Check children tokens for predicative usage
                    for child in token.children:
                        if child.dep_ == "attr" and child.pos_ == "NOUN":
                            noun = child

                    # Check the head token's children for the nominal subject in predicative constructions
                    for child in token.head.children:
                        if child.dep_ == "nsubj" and (child.pos_ == "NOUN" or child.pos_ == "PRON"):
                            noun = child

                    relevant_noun = "N/A" if noun is None else noun.text
                    relevant_lemma = "N/A" if noun is None else noun.lemma_

                    writer.writerow({
                        "Original Text": text,
                        "Relevant Noun": relevant_noun,
                        "Relevant Lemma": relevant_lemma
                    })

                    break
                    und_text
                    Exception(f'Error: Text not found in doc {str([token.text in doc])}')
                
