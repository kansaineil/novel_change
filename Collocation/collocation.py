import spacy
import scispacy
import csv

# Load the SciSpacy large model
nlp = spacy.load("en_core_sci_lg")

downloaded = []
with open("../../concordance-download_1985.txt") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if i == 0: continue  # header
    tokens = lines[i].strip().split("\t")
    line = " ".join(tokens[2:5])
    downloaded.append(line)

# Prepare the CSV file
with open("collocation_novels_1985sci.csv", mode="w", newline="") as csv_file:
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
            
