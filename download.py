import yt_dlp
from time import ctime
from tabulate import tabulate
from user_input_handler import proceed, while_input
from typing import Tuple

# Global Variables used to control style pallete of text output on CLI
y = '\033[33m'
b = '\033[34m'
s = '\033[2m'
bold = '\033[1m'
end = '\033[0m'


class Download:
    def __init__(self, URL: str):
        self.URL = URL
    
    def _download(self, ydl_opts: dict) -> Tuple[int, str]:
        '''Downlods a video or a playlist from it's URL'''
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.URL])
            return 1, ''
        except yt_dlp.utils.DownloadError as e:
            return 0, f'Downloading process failed: {e}'
        except Exception as e:
            return 0, f"An unexpected error occurred: {e}"


    def download(self, media_type: str) -> dict:
        '''
        Manages the Whole process of downloading process from gathering the downloading informations
        and initializing yt_dlp options that specifying downloading informations
        
        Parameters
        ----------
            media_type (str)
                requires two values only
                    - `video` for Video/Song downloading
                    - `playlist` for Playlists downloading
        '''
        now = ctime()
        if media_type == "playlist":
            ydl_opts = {
                'skip_download': True,          # Don't download the video
                'playlistend': 1,
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(self.URL, download=False)
                except Exception as e:
                    return {'URL': self.URL, 'Process': 'Playlist Download', 'State': 0,
                    'Error': f"An unexcepected error occured: {e}", 'Datetime': now}
                data = {"title": info.get("title"),
                        "description": info.get("description"),
                        "modified_date": info.get("modified_date"),
                        "view_count": info.get("view_count"),
                        "playlist_count": info.get("playlist_count"),
                        "channel": info.get("channel"),
                        'uploader': info.get("uploader"),
                        'thumbnail ': info.get("thumbnail"),
                        "webpage_url_domain": info.get("webpage_url_domain"),
                        "_type": info.get("_type")
                        }

                if data["_type"] != "playlist" or data["playlist_count"] == None:
                    print(data['title'], self.URL, sep='\n')
                    return {'File': self.URL, 'Process': 'Playlist Download', 'State': 0,
                    'Error': "Invalid Object Type! URL don't belong to Playlist.", 'Datetime': now}

                for i in list(data.keys()):
                    print(f"{y}{i}: {end}", data[i])
                
                ydl_options = specify_options(None, "playlist")

                print(f'\n{bold}{ydl_options}{end}\n')
                if proceed():
                    success, string = self._download(ydl_options)
                else:
                    return {'URL': self.URL, 'Process': 'Playlist Download', 'State': 0,
                    'Error': f"Download Process Cancelled", 'Datetime': now}
                if success:
                    return {'URL': self.URL, 'Process': 'Playlist Download', 'State': 1,
                    'Message': "Playlist Downloaded Successfully",
                    'Save Location': f'Media Files Manager/Downloads/{data['title']}', 'Datetime': now}
                else:
                    return {'URL': self.URL, 'Process': 'Playlist Download', 'State': 0,
                    'Error': string, 'Datetime': now}


        if media_type == "video":
            ydl_opts = {
                'skip_download': True,
                'playlistend': 1,
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(self.URL, download=False)
                except Exception as e:
                    return {'URL': self.URL, 'Process': 'Video/Audio Download', 'State': 0,
                    'Error': f"An unexcepected error occured: {e}", 'Datetime': now}

                data = {"title": info.get("title"),
                        "description": info.get("description"),
                        "view_count": info.get("view_count"),
                        "like_count": info.get("like_count"),
                        "upload_date": info.get("upload_date"),
                        "channel": info.get("channel"),
                        "uploader": info.get("uploader"),
                        'duration': info.get("duration"),
                        'thumbnail ': info.get("thumbnail"),
                        "webpage_url_domain": info.get("webpage_url_domain"),
                        "_type": info.get("_type"),
                        "playlist_count": info.get("playlist_count")
                        }

                if data["_type"] == "playlist" or data["playlist_count"] != None:
                    print(data['title'], self.URL, sep='\n')
                    return {'URL': self.URL, 'Process': 'Video/Audio Download', 'State': 0,
                    'Error': "Invalid Object Type! URL don't belong to Video.", 'Datetime': now}
                
                for i in list(data.keys())[:-2]:
                    print(f"\033[33m{i}: \033[0m", data[i])
                
                formats = []
                for f in info['formats']:
                    filesize = f.get('filesize')
                    if filesize:
                        filesize = str(round(filesize / (1024*1024), 2)) + "MB"
                    formats.append((f['format_id'], f.get('ext'), f.get('height'), f.get('format_note'), f.get('quality'), filesize))

                headers = ['format_id', 'ext', 'height', 'format_note', 'quality', 'filesize']
                print(f'{tabulate(formats, headers=headers, tablefmt="rounded_outline")}\n')
                
                format_ids = list(zip(*formats))[0]

                ydl_options = specify_options(format_ids, "video")
                
                print(f'\n{bold}{ydl_options}{end}\n')

                if proceed():
                    success, string = self._download(ydl_options)
                else:
                    return {'URL': self.URL, 'Process': 'Video/Audio Download', 'State': 0,
                    'Error': "Download process Cancelled", 'Datetime': now}
                if success:
                    return {'URL': self.URL, 'Process': 'Video/Audio Download', 'State': 1,
                    'Message': "Video/Audio Downloaded Successfully",
                    'Save Location': f'Media Files Manager/Downloads/{data['uploader']}', 'Datetime': now}
                else:
                    return {'URL': self.URL, 'Process': 'Video/Audio Download', 'State': 0,
                    'Error': string, 'Datetime': now}



def specify_options(formats: list | None, media_type: str) -> dict:
    base_dir = 'Media Files Manager/Downloads'

    if media_type == "playlist":
        condition = True
        while condition:
            x = input(f"{b}Choose Videos quality:{end} {s}360, 480, 720, 1080, 1440, 2160 {end}")
            condition = while_input(x, ['360', '480', '720', '1080', '1440', '2160'])
        
        output_format = f'bestvideo[height<={x}]+bestaudio'
        
        output_title = f'{base_dir}/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s'
        choose_videos = input(f"{b}Choose downloaded videos by:{end} {s}(all, playlistend, playlist_items) {end}")
        while choose_videos not in ['all', 'playlistend', 'playlist_items']:
            choose_videos = input(f"{b}Choose downloaded videos by:{end} {s}(all, playlistend, playlist_items) {end}")
        if choose_videos == "playlistend":
            playlistend = int(input(f"{b}Enter videos downloaded limit: {end}"))
        elif choose_videos == "playlist_items":
            playlist_items = input(f"{b}choose videos index e.g. 1,2,3: {end}")

    if media_type == "video":
        f_condition = True
        while f_condition:
            f_condition = False
            output_format = input(f"{b}Choose format {end}{s}(choose 1 or merge with \"+\"):{end} ")
            for f in output_format.split("+"):
                print(f)
                if (f not in formats) and ('best' not in f.lower()):
                    f_condition = True

        output_title = f"{base_dir}/%(title)s.%(ext)s"

    if media_type == "video" or media_type == "playlist":
        subtitles = bool(int(input(f"{b}Embed Subtitle{end} {s}(1/0):{end} ")))
        while subtitles not in [True, False]:
            subtitles = bool(int(input(f"{b}Embed Subtitle{end} {s}(1/0):{end} ")))
        if subtitles:
            subtitleslangs = input(f'{b}enter subtitles langs seperated by ",":{end} ').split(",")

    merge_format = input(f"{b}Enter Merge Format:{end} {s}(only mp3 and mp4 available or type \"original\") {end}")
    while merge_format not in ['mp3', 'mp4', 'original']:
        merge_format = input(f"{b}Enter Merge Format:{end} {s}(only mp3 and mp4 available or type \"original\") {end}")

    ydl_opts = {'format': output_format, 'outtmpl': output_title,
                'ffmpeg_location': 'C:\\bin',}
    
    mp3_postprocessors = {'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128'}

    metadata = {'key': 'FFmpegMetadata'}
    
    if media_type == "playlist":
        if merge_format == 'mp3':
            if choose_videos == 'playlistend':
                ydl_opts['playlistend'] = playlistend

            elif choose_videos == 'playlist_items':
                ydl_opts['playlist_items'] = playlist_items

            ydl_opts['ignoreerrors'] = True
            ydl_opts['postprocessors'] = [mp3_postprocessors, metadata]

        elif merge_format == 'mp4':
            if not subtitles:

                if choose_videos == 'playlistend':
                    ydl_opts['playlistend'] = playlistend

                elif choose_videos == 'playlist_items':
                    ydl_opts['playlist_items'] = playlist_items

                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['ignoreerrors'] = True
                ydl_opts['postprocessors'] = [metadata]

            elif subtitles:
                if choose_videos == 'all':
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'merge_output_format': 'mp4',
                                'ignoreerrors': True,
                                'writesubtitles': subtitles,
                                'subtitleslangs': subtitleslangs,
                                'subtitlesformat': 'vtt',
                                'postprocessors' : [{'key': 'FFmpegMetadata'}, {'key': 'FFmpegEmbedSubtitle'}]}
                elif choose_videos == 'playlistend':
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'playlistend': playlistend,
                                'merge_output_format': 'mp4',
                                'ignoreerrors': True,
                                'writesubtitles': subtitles,
                                'subtitleslangs': subtitleslangs,
                                'subtitlesformat': 'vtt',
                                'postprocessors' : [{'key': 'FFmpegMetadata'}, {'key': 'FFmpegEmbedSubtitle'}]}
                elif choose_videos == 'playlist_items':
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'playlist_items': playlist_items,
                                'merge_output_format': 'mp4',
                                'ignoreerrors': True,
                                'writesubtitles': subtitles,
                                'subtitleslangs': subtitleslangs,
                                'subtitlesformat': 'vtt',
                                'postprocessors' : [{'key': 'FFmpegMetadata'}, {'key': 'FFmpegEmbedSubtitle'}]}
        elif merge_format == 'original':
            if not subtitles:
                if choose_videos == 'all': 
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'ignoreerrors': True,
                                'postprocessors' : [{'key': 'FFmpegMetadata'}]}
                elif choose_videos == 'playlistend':
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'playlistend': playlistend,
                                'ignoreerrors': True,
                                'postprocessors' : [{'key': 'FFmpegMetadata'}]}
                elif choose_videos == 'playlist_items':
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'playlist_items': playlist_items,
                                'ignoreerrors': True,
                                'postprocessors' : [{'key': 'FFmpegMetadata'}]}
            elif subtitles:
                if choose_videos == 'all': 
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'ignoreerrors': True,
                                'writesubtitles': subtitles,
                                'subtitleslangs': subtitleslangs,
                                'subtitlesformat': 'vtt',
                                'postprocessors' : [{'key': 'FFmpegMetadata'}, {'key': 'FFmpegEmbedSubtitle'}]}
                elif choose_videos == 'playlistend':
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'playlistend': playlistend,
                                'ignoreerrors': True,
                                'writesubtitles': subtitles,
                                'subtitleslangs': subtitleslangs,
                                'subtitlesformat': 'vtt',
                                'postprocessors' : [{'key': 'FFmpegMetadata'}, {'key': 'FFmpegEmbedSubtitle'}]}
                elif choose_videos == 'playlist_items':
                    ydl_opts = {'format': output_format,
                                'outtmpl': output_title,
                                'ffmpeg_location': 'C:\\bin',
                                'playlist_items': playlist_items,
                                'ignoreerrors': True,
                                'writesubtitles': subtitles,
                                'subtitleslangs': subtitleslangs,
                                'subtitlesformat': 'vtt',
                                'postprocessors' : [{'key': 'FFmpegMetadata'}, {'key': 'FFmpegEmbedSubtitle'}]}
        return ydl_opts
    
    
    if media_type == 'video':
        if merge_format == 'original':
            if subtitles:
                ydl_opts = {'format': output_format,
                            'outtmpl': output_title,
                            'ffmpeg_location': 'C:\\bin',
                            'writesubtitles': subtitles,
                            'subtitleslangs': subtitleslangs,
                            'subtitlesformat': 'vtt',
                            'postprocessors' : [{'key': 'FFmpegMetadata'}, {'key': 'FFmpegEmbedSubtitle'}]}
            elif not subtitles:
                ydl_opts = {'format': output_format,
                            'outtmpl': output_title,
                            'ffmpeg_location': 'C:\\bin',
                            'postprocessors' : [{'key': 'FFmpegMetadata'}]}
        elif merge_format == 'mp4':
            if subtitles:
                ydl_opts = {'format': output_format,
                            'outtmpl': output_title,
                            'ffmpeg_location': 'C:\\bin',
                            'merge_output_format': 'mp4',
                            'writesubtitles': subtitles,
                            'subtitleslangs': subtitleslangs,
                            'subtitlesformat': 'vtt',
                            'postprocessors' : [{'key': 'FFmpegMetadata'}, {'key': 'FFmpegEmbedSubtitle'}]}
            elif not subtitles:
                ydl_opts = {'format': output_format,
                            'outtmpl': output_title,
                            'ffmpeg_location': 'C:\\bin',
                            'merge_output_format': 'mp4',
                            'postprocessors' : [{'key': 'FFmpegMetadata'}]}
        elif merge_format == 'mp3':
            ydl_opts = {'format': output_format,
                        'outtmpl': output_title,
                        'ffmpeg_location': 'C:\\bin',
                        'postprocessors' : [{'key': 'FFmpegExtractAudio',
                                            'preferredcodec': 'mp3',
                                            'preferredquality': '128'
                                            },
                                            {'key': 'FFmpegMetadata'}]}
        return ydl_opts