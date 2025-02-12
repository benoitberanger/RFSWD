# intented python version : 3.9

# builtin modules
import os
import pathlib
import csv

# config
MARSDIR      : str   = '/opt/medcom/log/'
LIM_HEAD     : float =  3.2
LIM_HEADLOCAL: float = 20.0

if os.path.exists(MARSDIR):
    target_dir = MARSDIR
else:
    target_dir = os.getcwd()

# fetch all .csv files
all_files = sorted(pathlib.Path(target_dir).rglob('RFSWD*csv'))
if len(all_files)==0:
    raise RuntimeError(f'No .csv file found recurivelty from this dir : {target_dir}')

# read all files & store data
seq: list[dict] = []
for filepath in all_files:
    with open(file=filepath, mode='r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for seq_dict in reader:
            seq.append(seq_dict)

# for debugging :
# rowname = seq[0].keys()
# with open('list_columns.txt', mode='w') as fid:
#     for row_idx, row_name in enumerate(rowname):
#         # print(f"{row_idx} {row_name}")
#         fid.writelines(f"{row_idx} {row_name} \n")

n           : int = len(seq)
len_SeqName : int = 0
len_ProtName: int = 0
for idx in range(n):
    len_SeqName  = max(len(seq[idx][ 'SeqName']),len_SeqName)
    len_ProtName = max(len(seq[idx]['ProtName']),len_ProtName)

for idx in range(n):
    if '%AdjustSeq%'  in seq[idx]['SeqName']: continue
    if '%ServiceSeq%' in seq[idx]['SeqName']: continue

    if len(seq[idx]['AspVal[2][0]'])>0:
        Head_value_WperKg = float(seq[idx]['AspVal[2][0]'])
    else:
        Head_value_WperKg = -2
    Head_relative_WperKg = Head_value_WperKg / LIM_HEAD

    if len(seq[idx]['AspVal[3][0]'])>0:
        HeadLocal_value_WperKg = float(seq[idx]['AspVal[3][0]'])
    else:
        HeadLocal_value_WperKg = -2
    HeadLocal_relative_WperKg = HeadLocal_value_WperKg / LIM_HEADLOCAL

    line = (
        f"{seq[idx]['Mass']:2s} {seq[idx]['Age']:3s} {seq[idx]['Size']:4s} {seq[idx]['Sex']} " 
        f"{seq[idx]['Date']} {seq[idx]['Time']} {seq[idx]['SeqName']:{len_SeqName}s} {seq[idx]['ProtName']:{len_ProtName}s} - "
        f"PREDICTED (W/Kg ~ relative): Head ({Head_value_WperKg: 7.3f} ~ {Head_relative_WperKg: 7.3f}) HeadLocal ({HeadLocal_value_WperKg: 7.3f} ~ {HeadLocal_relative_WperKg: 7.3f})"
            )
    
    print(line)
        