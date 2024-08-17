import pandas
import split_file_reader
import tarfile
import pprint
import os

file_name_excel="1991datatable.xlsx"
file_name_txt="all_lemma.txt.dir"
year="1991"

# files larger that 100 MB cannot be stored in Github
# if that's the case, the file is split in 10MB parts with 7-zip
#  and stored in a folder
# foldername is file_name_txt with ".dir" appended at the end
if file_name_txt.endswith(".dir"):
    file_name_txt_dir=file_name_txt
    file_name_txt=file_name_txt[0:-4]
    print(f"{file_name_txt} is stored in parts in {file_name_txt_dir}")
    filepaths=[]
    for item in os.listdir(file_name_txt_dir):
        filepaths.append(f"{file_name_txt_dir}/{item}")
    

    print(f"Checking content of {file_name_txt_dir} ...")
    with split_file_reader.SplitFileReader(filepaths, mode="rb") as fin:
        with tarfile.open(mode="r|*", fileobj=fin) as tar:
            for member in tar:
                
                if member.name == file_name_txt:
                    print(f"\t- {member.name}")
                else:
                    raise Exception(f"Unexpected file found: {member.name}")

    print(f"Extracting content of {file_name_txt_dir} ...")

    with split_file_reader.SplitFileReader(filepaths, mode="rb") as fin:
        with tarfile.open(mode="r|*", fileobj=fin) as tar:
            tar.extractall()




# read all_lemma.txt and create a map where key is "lemma:year" and value is token from that line

# tokens[0] is the index
# tokens[1] is the lemma
# tokens[2] is the total matches for that lemma
# tokens[3] is the year for
# tokens[4] is the total matches for all lemmas

print(f"Reading content of {file_name_txt} ...")
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

print(f"Reading content of {file_name_excel} ...")
excel_table = pandas.read_excel(file_name_excel)


print(f"Add count_off_all_lemma_tokens column")
for i in range(len(excel_table["Relevant Lemma"].values)):
    lemma=excel_table["Relevant Lemma"].values[i]
    key=lemma+"::"+year
    #print(f"{key=}")
    if key in map_lemmas.keys():
        #print(f"{map_lemmas[key]=}")
        lemmatotal=int(map_lemmas[key][2])
        
    else:
        #print(f"{key} not found")
        lemmatotal="N/A"
    #print(f"{lemmatotal=}")
    lemma_totals.append(lemmatotal)
    #print("\n")

#add data in excel table
    
excel_table.insert(3, "count_of_all_lemma_tokens", lemma_totals, True)

# save excel table in the output file

out_file_name_excel="Out_"+file_name_excel
print(f"Writing modified content to {out_file_name_excel} ...")
excel_table.to_excel(out_file_name_excel, index=False)

