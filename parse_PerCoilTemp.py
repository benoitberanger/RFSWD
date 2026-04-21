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

        idx      : int       = -1
        start_idx: int       = -1
        timestamp: list[str] = []
        sensors  : dict      = {}
        tname    : list[str] = []

        # fetch all values
        for line in Data[idxData].line:

            type: str = line['%MARKER%']
            # on Terra.X in XA60, here are the 3 `marker` :
            # RFCELK2364_SAT::PerCoilTemperaturesIF
            # RFCELK2364_SAT::PerCoilTemperaturesIF-OVC
            # RFCELK2364_SAT::PerCoilTemperaturesIF-Cables
            # one of each is written at each "request"
            if type.find('RFCELK2364_SAT::PerCoilTemperaturesIF') == -1:
                continue

            idx += 1

            # only save 1 timestamp for each 3 "request" since they are always bundled (and written in ~1ms)
            if type == 'RFCELK2364_SAT::PerCoilTemperaturesIF':
                timestamp.append(line['%TIME%' ])
                tname    .append(line['%TNAME%'])
                if start_idx == -1:
                    start_idx = idx

            # get content and clean it
            raw_line: str = line['%USERTEXT%']
            sensor_content: str = raw_line.replace('Current coil temperatures: ', '')
            end_of_ascii: int = sensor_content.find('\x80')
            if end_of_ascii > -1:
                sensor_content = sensor_content[:end_of_ascii]

            # parse the sensor content of the line, such as`` GC_AVG: 20.81, GC1: 21.00, GC2: 20.50``
            data: list[str] = sensor_content.split(', ')
            for sensordata in data:

                label, value = sensordata.split(': ')

                # new sensor label ? add it
                if label not in sensors.keys():
                    sensors[label] = []

                value = float(value)
                sensors[label].append(value)

        # prepare spacing for the TNAME
        unique_tname = set(tname)
        n_letters_unique_tname = [len(name) for name in unique_tname]
        len_tname: int = max(n_letters_unique_tname)

        # reorder sensor list
        labels = sensors.keys()
        labels = sorted(labels)

        N = len(timestamp)

        # print
        for idx in range(start_idx, N-start_idx):
            display: str = f"{timestamp[idx]} - "

            display += f"{tname[idx]:{len_tname}s} - "

            for label in labels:
                value = sensors[label][idx]
                if isinstance(value, float):
                    temperature = ColorFormater(GetColor(value, 16, 84), "{:6.2f}".format(value))
                else: 
                    temperature = ''
                display += f"{label} {temperature}  "

            print(display)

    return

if __name__ == '__main__':

    main()
