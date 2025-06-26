from File import Directory
from typing import Union
import csv

# Global Variables used to control style pallete of text output on CLI
red = '\033[31m'
green = '\033[32m'
end = '\033[0m'

def write_log(logs: dict, log_file: str) -> None:
    '''
    Function to record all Activity done bt the program
        - Prints Operations results to user.
        - Save all logs in external files with all operations details
        
    Parameters
    ----------
        logs: dict
            dict object contains operations details
        log_file: str
            Must be from `Download`, `PDF`, `Video`, `Image`, `Audio`, `Main`, `Rename`
    '''

    headers = ["File", "Process", "State", "Message", "Save Location", "Error", "Datetime"]
    if log_file == 'Download':
        headers.remove("File")
        headers.insert(0, 'URL')
    elif log_file == 'Rename':
        headers.remove('Process')
        headers.remove('Save Location')
    if log_file in ['Image', 'Video', 'Audio']:
        info = [logs.get(i) for i in headers+['Insiders']]
    else:
        info = [logs.get(i) for i in headers]

    if logs.get('State'):
        print(f'✅ {green}{logs.get('Message')}{end}')
    else:
        if isinstance(logs.get('Error'), str):
            print(f"❌ {red}{logs.get('Error')}{end}")
        elif isinstance(logs.get('Error'), list):
            for e in logs.get('Error'):
                print(f"❌ {red}{e}{end}")

    with open(f'Media Files Manager/Logs/{log_file}.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(info)


def initialize_env() -> None:
    '''Initialize Program Enviroment
    - Making Necessary Directories to save output files of different app operations
    - Making Necessary Files to record the logs'''

    dirs = ['Media Files Manager/Extract Images', 'Media Files Manager/PDF to Office',
            'Media Files Manager/Logs', 'Media Files Manager/Image Convertion',
            'Media Files Manager/Extract GIFs', 'Media Files Manager/Downloads',
            'Media Files Manager/Video Thumbnail', 'Media Files Manager/Audio Thumbnail',
            'Media Files Manager/Temp', 'Media Files Manager/Extracted Audio']

    for i in dirs:
        d = Directory(i)
        d.make()
    
    log_files = ["Download", "PDF", 'Video', 'Image', 'Audio', 'Main', 'Rename']
    for lf in log_files:
        try:
            with open(f'Media Files Manager/Logs/{lf}.csv', 'x', newline='') as f:
                writer = csv.writer(f)
                basic = ["File", "Process", "State", "Message", "Save Location", "Error", "Datetime"]

                if lf == 'Download':
                    basic.remove("File")
                    basic.insert(0, 'URL')
                elif lf == 'Rename':
                    basic.remove('Process')
                    basic.remove('Save Location')
                elif lf in ['Image', 'Video', 'Audio']:
                    basic = basic + ['Insiders']
                
                writer.writerow(basic)
        except:
            pass