# intented python version : 3.9

# builtin modules
import os
import pathlib
import csv


###############################################################################
# config
MARSDIR      : str   = '/opt/medcom/log/'
LIM_HEAD     : float =  3.2
LIM_HEADLOCAL: float = 20.0


###############################################################################
# local functions & classes
class FileData:
    def __init__(self) -> None:
        self.filepath: str = ''
        self.Sex     : int = -1
        self.Size    : int = -1
        self.Mass    : int = -1
        self.Age     : int = -1
        self.Seq     : list[dict] = []
    
    @property
    def nSeq(self) -> int:
        return len(self.Seq)

###############################################################################
def ColorFormater(
            r: int,
            g: int,
            b: int,
            value: float
            ) -> str:
        return f"\033[38;2;{r};{g};{b}m{value}\033[0m"

###############################################################################
def ColorizeFloat(value: float, min_value: float, max_value: float) -> str:
    
    if value < min_value: return ColorFormater(50,50,50, value)
    if value > max_value: return ColorFormater(255,0,255, value)

    r,g,b = 1,1,1

    if (value < min_value): value = min_value
    if (value > max_value): value = max_value

    dv = max_value - min_value

    if (value < (min_value + 0.25 * dv)):
        r = 0
        g = 4 * (value - min_value) / dv
    elif (value < (min_value + 0.5 * dv)):
        r = 0
        b = 1 + 4 * (min_value + 0.25 * dv - value) / dv
    elif (value < (min_value + 0.75 * dv)):
        r = 4 * (value - min_value - 0.5 * dv) / dv
        b = 0
    else:
        g = 1 + 4 * (min_value + 0.75 * dv - value) / dv
        b = 0

    r = int(255*r)
    g = int(255*g)
    b = int(255*b)
        
    return ColorFormater(r,g,b, value)


###############################################################################
def main():

    if os.path.exists(MARSDIR):
        target_dir = MARSDIR
    else:
        target_dir = os.getcwd()

    # fetch all .csv files
    all_files = sorted(pathlib.Path(target_dir).rglob('RFSWD*csv'))
    if len(all_files)==0:
        raise RuntimeError(f'No .csv file found recurivelty from this dir : {target_dir}')

    # read all files & store data
    Data: list[FileData] = []
    for nData, filepath in enumerate(all_files):
        with open(file=filepath, mode='r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            filedata = FileData()
            filedata.filepath = str(filepath)
            for seq_dict in reader:
                filedata.Seq.append(seq_dict)
            if filedata.nSeq>0:
                filedata.Sex  = int  (seq_dict['Sex' ]) if seq_dict['Sex' ].strip() else 0
                filedata.Size = float(seq_dict['Size']) if seq_dict['Size'].strip() else 0
                filedata.Mass = float(seq_dict['Mass']) if seq_dict['Mass'].strip() else 0
                filedata.Age  = int  (seq_dict['Age' ]) if seq_dict['Age' ].strip() else 0
            Data.append(filedata)
            
    # for debugging :
    # rowname = seq_dict.keys()
    # with open('list_columns.txt', mode='w') as fid:
    #     for row_idx, row_name in enumerate(rowname):
    #         # print(f"{row_idx} {row_name}")
    #         fid.writelines(f"{row_idx} {row_name} \n")

    nData       : int = len(Data)
    len_SeqName : int = 0
    len_ProtName: int = 0
    for idxData in range(nData):
        for seq in Data[idxData].Seq:
            len_SeqName  = max(len(seq[ 'SeqName']),len_SeqName)
            len_ProtName = max(len(seq['ProtName']),len_ProtName)

    for idxData in range(nData):
        header = f"Sex={Data[idxData].Sex:2d}  Mass={Data[idxData].Mass:3.0f}  Size={Data[idxData].Size:5.2f}  Age={Data[idxData].Age:3d}  file={Data[idxData].filepath}"
        print(header)

        for seq in Data[idxData].Seq:
            if '%AdjustSeq%'  in seq['SeqName']: continue
            if '%ServiceSeq%' in seq['SeqName']: continue

            if len(seq['AspVal[2][0]'])>0:
                Head_value_WperKg = float(seq['AspVal[2][0]'])
            else:
                Head_value_WperKg = -2
            Head_relative_WperKg = Head_value_WperKg / LIM_HEAD

            if len(seq['AspVal[3][0]'])>0:
                HeadLocal_value_WperKg = float(seq['AspVal[3][0]'])
            else:
                HeadLocal_value_WperKg = -2
            HeadLocal_relative_WperKg = HeadLocal_value_WperKg / LIM_HEADLOCAL

            line = (
                f"{seq['Date']} {seq['Time']} {seq['SeqName']:{len_SeqName}s} {seq['ProtName']:{len_ProtName}s} - "
                f"PREDICTED (W/Kg ~ relative): Head ({Head_value_WperKg: 7.3f} ~ {Head_relative_WperKg: 7.3f}) HeadLocal ({HeadLocal_value_WperKg: 7.3f} ~ {HeadLocal_relative_WperKg: 7.3f})"
                )
            print(line)




###############################################################################
if __name__ == '__main__':

    # to test colors
    #
    # values = range(-3, 23)
    # for val in values:
    #     print(ColorizeFloat(val, 0, 20))

    main()

