import pandas as pd

file_name_excel="1991datatable.xlsx"
file_name_txt="all_lemma.txt"
year="1991"

df = pd.read_excel(file_name_excel)



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

    
frequencies=[]

for i in range(len(df["Relevant Lemma"].values)):
    lemma=df["Relevant Lemma"].values[i]
    key=lemma+"::"+year
    print(f"{key=}")
    if key in map_lemmas.keys():
        print(f"{map_lemmas[key]=}")
        frequency=int(map_lemmas[key][2]) / int(map_lemmas[key][4])
        
    else:
        print(f"{key} not found")
        frequency="N/A"
    print(f"{frequency=}")
    frequencies.append(frequency)
    print("\n")
    
df.insert(3, "Frequency of overall Lemma", frequencies, True)

df.to_excel("Out_"+file_name_excel, index=False)

