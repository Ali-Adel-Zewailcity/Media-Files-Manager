# Importing necessary Libraries
from time import ctime
import sys
from File import Directory
from pdf import PDF
from video import Video, Audio, embed_thumbnail_in_folder
from download import Download
from images import ImageOperations
from logs import write_log, initialize_env
from user_input_handler import while_input, proceed

# Gloab Variables used to handle print statements pallete.
r = '\033[31m'
g = '\033[32m'
y = '\033[33m'
b = '\033[34m'
redbg = '\033[41m'
greenbg = '\033[42m'
yellowbg = '\033[43m'
bluebg = '\033[44m'
whitebg = '\033[47m'
u = '\033[4m'
i = '\033[3m'
s = '\033[2m'
bold = '\033[1m'
e = '\033[0m'


def edit_pdf() -> None:
    condition = True
    while condition:
        print("\n1 Merge PDF files")
        print("2 Split PDF file")
        print("3 Extract Images from PDF file")
        print("4 Delete pages from PDF file")
        print("5 Convert PDF to Office")
        print("6 Return Home")
        
        x = input(f"{b}Choose from [1, 2, 3, 4, 5, 6]: {e}")
        condition = while_input(x, ['1','2','3','4','5','6'])
    
    if x in ['2','3','4','5']:
        pdf = PDF(input(f"\n{b}Please enter PDF File Path: {e}"))
        if x == '2':
            start = input(f"{b}Enter Start Page number: {e}")
            end_P = input(f"{b}Enter End Page number: {e}")
            save = input(f"{b}Enter existing save Path: {e}{s}e.g. {u}D:\\Myname\\{e} ")

            if proceed():
                result = pdf.split_pdf(start, end_P, save)
                write_log(result, 'PDF')

        elif x == '3':
            if proceed():
                result = pdf.pdf_extract_images()
                write_log(result, 'PDF')

        elif x == '4':
            delete = input(f"{b}Indicate pages to delete:{e} {s}e.g. single page:{u}2{e}{s} range:{u}1-8{e}{s} index:{u}1,8,5,7{e} ")

            if proceed():
                result = pdf.pdf_pages_delete(delete)
                write_log(result, 'PDF')

        elif x == '5':
            print(f"{i}Conversion available to pptx/xlsx/docx{e}")
            
            condition = True
            while condition:
                convert_to = input(f"{b}Enter conversion type: {e}").lower()
                condition = while_input(convert_to, ('pptx','xlsx','docx'))
            
            if proceed():
                result = pdf.convert_pdf(convert_to)
                write_log(result, 'PDF')

    elif x == '1':
        paths = input(f"\n{b}Please enter PDF Files Paths seperated by {e}'{bold},{e}' {b}:{e} ").split(',')
        save = input(f"{b}Enter existing save Path and output file name: {e}\n{s}e.g. {u}D:\\Myname\\file.pdf{e} ")

        if proceed():
            result = PDF(" ").merge_pdf(paths, save)
            write_log(result, 'PDF')

    elif x == '6':
        return None


def edit_images() -> None:
    print(f'\n{s}Supported Types:{bold}', *ImageOperations._supported, sep=" ", end=f"{e}")
    
    img = ImageOperations(input(f"\n{b}Enter Image Path: {e}"))
    
    condition = True
    while condition:
        convert_to = input(f"{b}Convet Image to{e} {s}Choose from supported types{e} ")
        condition = while_input(convert_to, ImageOperations._supported)
    
    if proceed():
        result = img.convert_image(convert_to)
        write_log(result, 'Image')


def rename() -> None:
    print(f'\n{s}This option is to remove or replace a list of character in all files\' names in specific directory{e}')
    dir = Directory(input(f"{b}Enter Folder path:{e} "))
    remove = input(f"{b}Enter characters to be removed:{e} ")
    replace = input(f"{b}Enter Characters to be replaced with removed ones{e} {s}(if not press enter):{e} ")
    
    if proceed():
        write_log(dir.allDirectory(remove, replace), "Rename")
    return None



def edit_videos() -> None:
    condition = True
    while condition:
        print("\n1 Change Thumbnail of video files")
        print("2 Generate GIF from Video")
        print("3 Extract Audio from Video")
        print("4 Return Home")
        
        x = input(f"{b}Choose from [1, 2, 3, 4]: {e}")
        condition = while_input(x, ['1','2','3','4'])

    if x == '4':
        return None
    if x == '1':
        condition = True
        while condition:
            y = input(f"{b}Single/Batch{e} {s+bold}(1/2):{e} ").lower()
            condition = while_input(y, ['single', 'batch', '1', '2'])
        
        if y in ('batch', '2'):
            folder = Directory(input(f"{b}Enter Folder Path:{e} "))
            image = ImageOperations(input(f"{b}Enter Image file path:{e} "))
            
            if proceed():
                result = embed_thumbnail_in_folder(folder, image, 'Video')
                write_log(result, 'Video')
        else:
            vid = Video(input(f"{b}Enter Video file Path:{e} "))
            image = ImageOperations(input(f"{b}Enter Image file path:{e} "))
            
            if proceed():
                result = vid.embed_thumbnail_video(image)
                write_log(result, 'Video')

    else:
        vid = Video(input(f"\n{b}Enter Video Path: {e}"))

        if x == '2':
            print(f"{s}Enter time in the any following format {bold}HH:MM:SS, MM:SS {e+s}or {bold}SS{e}")
            start = input(f"{b}Start Time: {e}")
            end = input(f"{b}End Time: {e}")

            scale = None
            if input(f"{b}Do you want to Scale Image ({e}Y\\n{b}):{e} ").lower() == 'y':
                scale = input(f"{b}Enter new width: {e}")

            if proceed():
                result = vid.generate_gif(start, end, scale)
                write_log(result, 'Video')
        elif x == '3':
            if proceed():
                result = vid.extract_original_audio()
                write_log(result, 'Video')



def edit_audio() -> None:
    condition = True
    while condition:
        print("\n1 Change Thumbnail of Audio files")
        print("2 Return Home")
        
        x = input(f"{b}Choose from [1, 2]: {e}")
        condition = while_input(x, ['1','2'])

    if x == '2':
        return None
    if x == '1':
        condition = True
        while condition:
            y = input(f"{b}Single/Batch{e} {s+bold}(1/2):{e} ").lower()
            condition = while_input(y, ['single', 'batch', '1', '2'])
        
        if y in ('batch', '2'):
            folder = Directory(input(f"{b}Enter Folder Path:{e} "))
            image = ImageOperations(input(f"{b}Enter Image file path:{e} "))
            
            if proceed():
                result = embed_thumbnail_in_folder(folder, image, 'Audio')
                write_log(result, 'Audio')
        else:
            audio = Audio(input(f"{b}Enter Audio file Path:{e} "))
            image = ImageOperations(input(f"{b}Enter Image file path:{e} "))
            
            if proceed():
                result = audio.embed_thumbnail_audio(image)
                write_log(result, 'Audio')



def download_media() -> None:
    condition = True
    while condition:
        print("\n1 Downlaod a Video/Song")
        print("2 Download a Playlist")
        print("3 Return Home")
    
        x = input(f"{b}Choose from [1, 2, 3]: {e}")
        condition = while_input(x, ['1','2','3'])
    
    if x == "1":
        video_urls = input(f"\n{b}Enter Video/Song Url:{e} ").split(',')

        for video_url in video_urls:
            vid = Download(video_url)
            
            result = vid.download('video')
            write_log(result, 'Download')
    elif x == "2":
        playlist_url = Download(input(f"\n{b}Enter Playlist Url: {e}"))
        result = playlist_url.download('playlist')

        write_log(result, 'Download')

    elif x == "3":
        return None


if __name__ == "__main__":
    print(f"{bold}{g}Welcome to Media Files Manager{e}")
    initialize_env()

    while True:
        condition = True
        while condition:
            print("\n1 Dowanload Media Files")
            print("2 Edit PDF Files")
            print("3 Edit Video Files")
            print("4 Image Convertion")
            print("5 Edit Audio Files")
            print("6 Rename Files in a Folder")
            print("7 Quit")
            
            x = input(f"{b}Choose from [1, 2, 3, 4, 5, 6, 7]: {e}")
            condition = while_input(x, ['1','2','3','4','5','6','7'])

        try:
            if x == "7":
                sys.exit()
            if x == "6":
                rename()
            elif x == "5":
                edit_audio()
            elif x == "4":
                edit_images()
            elif x == "3":
                edit_videos()
            elif x == "2":
                edit_pdf()
            elif x == "1":
                download_media()
        except Exception as error:
            try:
                log = {"Process":f'{x}', "State":0, "Error":f"Occured Error in main module {error}", "Datetime": ctime()}
                write_log(log, 'Main')
            except:
                print(f'Failed to record that Error')