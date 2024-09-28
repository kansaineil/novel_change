import pandas
import split_file_reader
import tarfile
import pprint
import os

#

file_name_excel="../novel_collocates_1985-2020.xlsx"
file_name_csv_out="../novel_collocates_1985-2020_out.csv"
file_name_txt="all_lemma.txt.dir"


print(f"Reading content of {file_name_excel} ...")
excel_table = pandas.read_excel(file_name_excel)

relevant_lemma_year_counts={}
for i in range(len(excel_table["Relevant Lemma"].values)):
    relevant_lemma=excel_table["Relevant Lemma"].values[i]
    year=excel_table["Year"].values[i]
    relevant_lemma_year=f"{year}::{relevant_lemma}"
    if not relevant_lemma_year in relevant_lemma_year_counts.keys():
        relevant_lemma_year_counts[relevant_lemma_year]=1 #first time found
    else:
        relevant_lemma_year_counts[relevant_lemma_year]+=1 #found again


# files larger that 100 MB cannot be stored in Github
# if that's the case, the file is split in 10MB parts with 7-zip
#  and stored in a folder
# foldername is file_name_txt with ".dir" at the end
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


with open(file_name_csv_out,"w") as f:
    print("Year,Relevant Lemma,Collocation Frequency,Lemma Frequency",file=f)
    for key in relevant_lemma_year_counts.keys():
        year=key[0:4]
        relevant_lemma=key[6:]
        count=relevant_lemma_year_counts[key]
        key2=f"{relevant_lemma}::{year}"
        lemma_frequency=map_lemmas[key2][2] if key2 in map_lemmas.keys() else "N/A"
        print(f"{year},{relevant_lemma},{count},{lemma_frequency}",file=f)
print(f"{file_name_csv_out}")

