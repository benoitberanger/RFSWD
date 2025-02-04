# builtin modules
import os
import pathlib
import csv

cwd = os.getcwd()

# fetch all .csv files
all_files = sorted(pathlib.Path(cwd).rglob('*csv'))
if len(all_files)==0:
    raise RuntimeError(f'No .csv file recurivelty from this dir : {cwd}')

# read all files & store data
seq = []
for filepath in all_files:
    with open(file=filepath, mode='r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for seq_dict in reader:
            seq.append(seq_dict)

# rowname = seq[0].keys()
# with open('list_columns.txt', mode='w') as fid:
#     for row_idx, row_name in enumerate(rowname):
#         # print(f"{row_idx} {row_name}")
#         fid.writelines(f"{row_idx} {row_name} \n")

n = len(seq)
len_SeqName :int = 0
len_ProtName:int = 0
for idx in range(n):
    len_SeqName  = max(len(seq[idx][ 'SeqName']),len_SeqName)
    len_ProtName = max(len(seq[idx]['ProtName']),len_ProtName)

LIM_Head     : float =  3.2
LIM_HeadLocal: float = 20.0

for idx in range(n):
    if '%AdjustSeq%' not in seq[idx]['SeqName']:

        Head_value_WperKg = float(seq[idx]['AspVal[2][0]'])
        Head_relative_WperKg = Head_value_WperKg / LIM_Head

        HeadLocal_value_WperKg = float(seq[idx]['AspVal[3][0]'])
        HeadLocal_relative_WperKg = HeadLocal_value_WperKg / LIM_HeadLocal

        line = (
            f"{seq[idx]['PatID']} {seq[idx]['Mass']:2s} {seq[idx]['Age']:3s} {seq[idx]['Size']:4s} {seq[idx]['Sex']} " 
            f"{seq[idx]['Date']} {seq[idx]['Time']} {seq[idx]['SeqName']:{len_SeqName}s} {seq[idx]['ProtName']:{len_ProtName}s} - "
            f"PREDICTED (W/Kg ~ relative): Head ({Head_value_WperKg: 7.3f} ~ {Head_relative_WperKg: 7.3f}) HeadLocal ({HeadLocal_value_WperKg: 7.3f} ~ {HeadLocal_relative_WperKg: 7.3f})"
               )
        
        print(line)
        