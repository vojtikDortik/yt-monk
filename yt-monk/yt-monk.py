from bs4 import BeautifulSoup as bs
import requests
import json
import os
from pytube import Playlist, YouTube
from pytube.exceptions import RegexMatchError
from shutil import rmtree
from pathlib import Path


class YT_Downloader:
    def __init__(self):

        self.all_file_extensions = ["mp3", "ogg", "wav", "opus", 'mp4', 'webm']

        self.api_url = 'https://olly.imput.net/api/json'

        self.options = self.Options()


    class Options:
        def __init__(self):
            self.name_variables = ["<videoTitle>", "<selectedQuality>", "<selectedCodec>"]
            self.allowed_file_types = ['video', "audio"]
            self.allowed_quality = ["max", "2160", "1440", "1080", "720", "480", "360", "240", "144"]
            self.allowed_codecs = ["h264", "av1", "vp9"]
            self.allowed_audio_formats = ["mp3", "ogg", "wav", "opus"]

            self.default = self.Default(self)

            try:
                self.useJson()
                self.correctOptions()
            except Exception as e:
                print(f'Something went wrong while loading json options: \n{e}')
                self.default.use()



        class Default:
            def __init__(self, options):
                self.codec = "av1"
                self.quality = "1080"
                self.file_name = "titleVar"
                self.file_type = "video"
                self.audio_format = "wav"
                self.mute_audio = False
                self.overwrite_files = True
                self.download_directory = str(Path.home() / "Downloads")

                self.options = options

            def use(self):
                self.options.codec = self.codec
                self.options.quality = self.quality
                self.options.file_name = self.file_name
                self.options.file_type = self.file_type
                self.options.audio_format = self.audio_format
                self.options.mute_audio = self.mute_audio
                self.options.overwrite_files = self.overwrite_files


        def useJson(self):
            with open('options.json', 'r') as f:
                options = json.load(f)
                self.codec = options['codec']
                self.quality = options['quality']
                self.file_name = options['file_name']
                self.file_type = options['file_type']
                self.audio_format = options['audio_format']
                self.mute_audio = options['mute_audio']
                self.overwrite_files = options['overwrite_files']
                self.download_directory = options['download_directory'].replace('<defaultDirectory>', self.default.download_directory)


        def correctOptions(self):
            if not self.codec in self.allowed_codecs: self.codec = self.default.codec
            if not self.file_type in self.allowed_file_types: self.file_type = self.default.file_type
            if not self.quality in self.allowed_quality: self.quality = self.default.quality
            if not self.audio_format in self.allowed_audio_formats: self.audio_format = self.default.audio_format
            if not isinstance(self.mute_audio, bool): self.mute_audio = self.default.mute_audio
            if not isinstance(self.overwrite_files, bool): self.overwrite_files = self.default.overwrite_files


    def downloadVideo(self, url, filename=None, download_directory=None):

        download_directory = download_directory if download_directory is not None else self.options.download_directory

        filename = self.correctFilename(filename) if filename is not None else self.createFilename(url)

        download_directory_content = os.listdir(download_directory)

        while not self.options.overwrite_files and filename in download_directory_content:
            action = input(f'File "{filename}" already exists.\nDo you want to overwrite it (y/n) or rename it (r): ')
            if action.lower() not in ('y', 'n', 'r'):
                continue

            if action.lower() == 'n':
                print('Canceling download')
                return
            elif action.lower() == 'r': filename = self.correctFilename(input('Enter a new filename: '))
            elif action.lower() == 'y': break

        file_path = os.path.join(download_directory, filename)

        stream_url = self.getStreamUrl(url)

        print(f'Downloading "{filename}"')

        self.captureStream(stream_url, file_path)

        print(f'Downloaded "{filename}" to {download_directory}')



    def captureStream(self, stream_url, file_path):
        with requests.get(stream_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)


    def download(self, url):
        url = self.correctUrl(url)
        url_type = self.getUrlType(url)
        #print(url_type)
        if url_type == 'playlist':
            self.downloadPlaylist(url)
        elif url_type == 'video':
            self.downloadVideo(url)
        else: print("The URL doesn't seem to be right")

    def getUrlType(self, url):
        if url is None: return None
        if 'https://www.youtube.com/playlist?' in url:
            return 'playlist'
        elif 'https://www.youtube.com/watch' in url:
            return 'video'
        else:
            return None
        
    def correctUrl(self, url):
        if 'youtube.com/' not in url: return None
        if 'https://www.' not in url and url.startswith('youtube.com/'):
            #print(url)
            url = 'https://www.' + url
        elif 'https://' not in url and url.startswith('www.youtube.com/'):
            #print(url)
            url = 'https://' + url
        return url


    def downloadPlaylist(self, url, make_new_directory=True, new_directory_name=None,filename_pattern=None, download_directory=None):
        download_directory = download_directory if download_directory is not None else self.options.download_directory

        playlist = Playlist(url)

        if make_new_directory:
            if new_directory_name is None:
                download_directory = self.makeDirectory(self.correctDirectoryName(playlist.title), download_directory)
            elif new_directory_name is not None:
                download_directory = self.makeDirectory(self.correctDirectoryName(new_directory_name), download_directory)
            if download_directory is None:
                return

        for i in range(len(playlist)):
            print(f'-- Downloading video ({i+1}/{len(playlist)}) --')
            if filename_pattern is None: self.downloadVideo(playlist[i], download_directory=download_directory)
            elif isinstance(filename_pattern, str): self.downloadVideo(playlist[i], download_directory=download_directory, filename=filename_pattern.replace('numberVar', str(i+1)))
            else: print('something wrong with filepattern')
            print()


    def makeDirectory(self, directory_name, parent_directory):
        directory_content = os.listdir(parent_directory)
        while directory_name in directory_content:
            action = input(f'Directory "{directory_name}" already exists.\nDo you want to overwrite it (y/n) or make a new name: ')
            if action.lower() == 'n':
                print('Canceling download')
                return None

            elif action.lower() == 'y':
                rmtree(os.path.join(parent_directory, directory_name))
                break

            else:
                directory_name = self.correctDirectoryName(action)
                continue



        path = os.path.join(parent_directory, directory_name)
        os.mkdir(path)
        return path





    def getStreamUrl(self, url):
        data = {
            "url": url,
            "vCodec": self.options.codec,
            "vQuality": self.options.quality,
            "aFormat": self.options.audio_format,  
            "filenamePattern": "classic",
            "isAudioOnly": True if self.options.file_type == 'audio' else False,
            "isAudioMuted": self.options.mute_audio,  
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        done = False
        for _ in range(2):
            response = json.loads(requests.post(self.api_url, headers=headers, data=json.dumps(data)).text)
            if response['status'] == 'stream':
                stream_url = response['url']
                done = True
                break
            elif response['status'] == 'error':
                if response['text'] == "i couldn't find anything to download with your settings. try another codec or quality in settings!" and data['vCodec'] == 'av1':
                    data['vCodec'] = 'h264'
        if not done: print("Couldn't download the video")

        return stream_url

    def correctFilename(self, filename):
        invalid_chars = r'[\/:*?"<>|]'
        correct_filename = filename
        for invalid_char in invalid_chars:
            correct_filename = correct_filename.replace(invalid_char, '')

        correct_filename = self.correctExtension(correct_filename)

        return correct_filename

    def correctDirectoryName(self, name):
        invalid_chars = r'[\/:*?"<>|]'
        correct_directory_name = name
        for invalid_char in invalid_chars:
            correct_directory_name = correct_directory_name.replace(invalid_char, '')
        return correct_directory_name

    def createFilename(self, url=None, correct_filename=True):
        filename = self.options.file_name

        name_variables_dict = {variable: None for variable in self.options.name_variables}

        if '<videoTitle>' in filename and url is not None:
            name_variables_dict['<videoTitle>'] = self.getVideoTitle(url)
        else: name_variables_dict['<videoTitle>'] = 'badVideoTitle'
        name_variables_dict['<selectedCodec>'] = self.options.codec
        name_variables_dict['<selectedQuality>'] = self.options.quality + 'p'
        
        name_variables_dict['2160p'] = '4k'
        name_variables_dict['maxp'] = '8k'

        for variable in name_variables_dict:
            filename = filename.replace(variable, name_variables_dict[variable])

        if correct_filename: filename = self.correctFilename(filename)

        return filename



    def correctExtension(self, filename):
        has_extension = any(filename.endswith(f".{ext}") for ext in self.all_file_extensions)

        if self.options.file_type == 'video':
            if self.options.codec == 'vp9': correct_extension = 'webm'
            elif self.options.codec in ('h264', 'av1'): correct_extension = 'mp4'
            else: raise Exception('idk')
        elif self.options.file_type == 'audio': correct_extension = self.options.audio_format
        else: raise Exception('idk')

        if has_extension:
            base_name = filename.rsplit('.', 1)[0]
            return f"{base_name}.{correct_extension}"
        else:
            return f"{filename}.{correct_extension}"



    def getVideoTitle(self, url):
        video = YouTube(url)
        return video.title


    def main(self):
        while True:
            url = input('\nEnter video URL (q to quit): ')
            if url.lower() == 'q':
                break
            try:
                self.download(url)
            except Exception as e:
                print(f'Something went wrong while downloading') #: \n{e}')






if __name__ == '__main__':
    downloader = YT_Downloader()
    downloader.main()

    # tests
    # https://www.youtube.com/playlist?list=PLx0VWrfG-rXnSgP2YP7kKTcDf45RjXiUu
    # https://www.youtube.com/watch?v=C7SdOgyOepw&list=PLx0VWrfG-rXnSgP2YP7kKTcDf45RjXiUu








































