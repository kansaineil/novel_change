import pandas as pd

file_name_excel="1991datatable.xlsx"
file_name_txt="all_lemma.txt"
year="1991"


# read all_lemma.txt and create a map where key is "lemma:year" and value is token from that line

# tokens[0] is the index
# tokens[1] is the lemma
# tokens[2] is the total matches for that lemma
# tokens[3] is the year for
# tokens[4] is the total matches for all lemmas

with open(file_name_txt, encoding="utf-8") as  f:
    lines=f.readlines()

map_lemmas={}

for i in range(len(lines)):
    if i==0:continue
    if lines[i].strip()=="":continue
    tokens=lines[i].strip().split("\t")
    
    #print(f"{tokens=}")
    key=tokens[1]+"::"+tokens[3]
    #print(f"{key=}")
    map_lemmas[key]=tokens

    
lemma_totals=[]

#match data`
# read the excel file line by line
# for each "Relevant Lemma" find the total matches in the year and add them in a new column
# the new column has the header count of all lemma_tokens
df = pd.read_excel(file_name_excel)

for i in range(len(df["Relevant Lemma"].values)):
    lemma=df["Relevant Lemma"].values[i]
    key=lemma+"::"+year
    print(f"{key=}")
    if key in map_lemmas.keys():
        print(f"{map_lemmas[key]=}")
        lemmatotal=int(map_lemmas[key][2])
        
    else:
        print(f"{key} not found")
        lemmatotal="N/A"
    print(f"{lemmatotal=}")
    lemma_totals.append(lemmatotal)
    print("\n")

#add data in excel
    
df.insert(3, "count_of_all_lemma_tokens", lemma_totals, True)

# save excel file in the output file

df.to_excel("Out_"+file_name_excel, index=False)

