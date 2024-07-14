import spacy
import csv
import os

# Load the small English pipeline
nlp = spacy.load("en_core_web_sm")

downloaded = []
input_file=None
input_files=os.listdir("")
for item in input_files:
    if not item.startswith("concordance-download_"):continue
    if not item.endswith(".txt"):continue
    input_file=item
    break
if input_file==None:
    raise Exception(f"Could not find an input file in {input_files}")
output_file=input_file.replace("concordance-download_","collocation_novels_").replace(".txt",".csv")
with open(input_file) as f:
    lines = f.readlines()

for i in range(len(lines)):
    if i == 0:continue  # header
    tokens = lines[i].strip().split("\t")
    line = " ".join(tokens[2:5])
    downloaded.append(line)

# Prepare the CSV file
with open(output_file, mode="w", newline="") as csv_file:
    fieldnames = ["Original Text", "Relevant Span", "Relevant Noun", "Relevant Lemma"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Process a text
    for text in downloaded:
        doc = nlp(text)

        # Iterate over the tokens
        for token in doc:
            # Print the text and the predicted part-of-speech tag
            if token.text == "novel":
                min_span = token.i
                max_span = token.i + 1
                head_token = token.head
                noun = None

                for order in range(4):
                    if head_token.pos_ == "NOUN" and noun is None:
                        noun = head_token

                    min_span = min(min_span, head_token.i)
                    max_span = max(max_span, head_token.i)
                    head_token = head_token.head

                    
                relevant_span = doc[min_span:max_span+1]
                relevant_noun = "N/A" if noun is None else noun
                relevant_lemma = "N/A" if noun is None else noun.lemma_

                writer.writerow({
                    "Original Text": text,
                    "Relevant Span": relevant_span,
                    "Relevant Noun": relevant_noun,
                    "Relevant Lemma": relevant_lemma
                })

                #print()
                #print("Original text:\n\t", text)
                #print("Relevant span:\n\t", relevant_span)
                #print("Relevant noun:\n\t", relevant_noun)
                #print("Relevant lemma:\n\t", relevant_lemma)
                
                break
