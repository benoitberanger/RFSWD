# intented python version : 3.9

# builtin modules
import os
import pathlib
import csv

###############################################################################
# config
###############################################################################
MARSDIR: str   = '/opt/medcom/log/'

###############################################################################
# local functions & classes
###############################################################################

class FileData:
    def __init__(self) -> None:
        self.filepath: str        = ''
        self.line    : list[dict] = []

    @property
    def nLine(self) -> int:
        return len(self.line)


def ColorFormater(rgb: tuple[int,int,int], value: any) -> str:
        return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{value}\033[0m"


def GetColor(value: float, min_value: float, max_value: float) -> tuple[int, int, int]:
    
    if value < min_value: return  50,50, 50
    if value > max_value: return 255, 0,255

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
        
    return r, g, b


###############################################################################
# main
###############################################################################
def main() -> None:

    if os.path.exists(MARSDIR):
        target_dir = MARSDIR
    else:
        target_dir = os.getcwd()

    expr: str = '*PerCoilTemp*log'

    # fetch all .csv files
    all_files = sorted(pathlib.Path(target_dir).rglob(expr))
    if len(all_files)==0:
        raise RuntimeError(f'No {expr} file found recurivelty from this dir : {target_dir}')

    # read all files & store data
    Data: list[FileData] = []
    for nData, filepath in enumerate(all_files):
        with open(file=filepath, mode='r') as logfile:
            reader = csv.DictReader(f=logfile, delimiter='|')
            filedata = FileData()
            filedata.filepath = str(filepath)
            for line in reader:
                filedata.line.append(line)
            Data.append(filedata)

    # loop over each file
    for idxData in range(len(Data)):
        print(Data[idxData].filepath)

        idx      : int       = 0
        timestamp: list[str] = []
        sensors  : dict      = {}
        
        # fetch all values
        for line in Data[idxData].line:

            type: str = line['%TNAME%']
            if type.find('CoilTempLog') == -1:
                continue
            elif type == 'CoilTempLog':
                timestamp.append(line['%TIME%'])
                idx += 1
            
            content: str = line['%USERTEXT%']

            content = content.replace('Current coil temperatures: ', '')
            data: list[str] = content.split(', ')
            
            for sensordata in data:

                # eject weird temps, such as `GC12: 20.75 \x80 Masks - GC1_4: 0xffff`
                try:
                    label, value = sensordata.split(': ')
                except ValueError:
                    continue

                # new sensor label ? add it
                if label not in sensors.keys():
                    sensors[label] = []

                # some values are HEX, dont know why
                try:
                    value = float(value)
                except ValueError:
                    pass
                sensors[label].append(value)

        # check length of the data found for each sensor
        N: int = 1e9
        for label in sensors.keys():
            N = min(N, len(sensors[label]))
        N = min(N, len(timestamp))

        # reorder sensor list
        labels = sensors.keys()
        labels = sorted(labels)

        # print
        for idx in range(N):
            display: str = f"{timestamp[idx]} - "

            for label in labels:
                value = sensors[label][idx]
                if isinstance(value, float):
                    temperature = ColorFormater(GetColor(value, 16, 84), "{:5.2f}".format(value))
                else: 
                    temperature = ''
                display += f"{label} {temperature}  "

            print(display)

    return

if __name__ == '__main__':

    main()
