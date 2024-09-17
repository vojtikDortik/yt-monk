import requests
import json
import os
from pytube import Playlist, YouTube
from shutil import rmtree
from pathlib import Path


class Downloader:
    def __init__(self, json_path: str = None, **options):
        if not isinstance(json_path, (str, type(None))):
            raise TypeError("json_path must be a string or None")
        
        self.all_file_extensions = ["mp3", "ogg", "wav", "opus", 'mp4', 'webm']

        self.api_url = 'https://olly.imput.net/api/json'

        self.options = self.Options(json_path=json_path, options=options)


    class Options:
        def __init__(self, json_path: str, options):
            if not isinstance(json_path, (str, type(None))):
                raise TypeError("json_path must be a string or None")
            if not isinstance(options, dict):
                raise TypeError("options must be a dictionary")
            self.useDefault()
            if json_path is not None:
                if os.path.exists(json_path):
                    self.useJson(json_path)

                elif not os.path.exists(json_path):
                    raise Exception('Invalid path')

            if options != {}:
                self.useCustom(**options)
            
            
            

            
        name_variables = ["<videoTitle>", "<selectedQuality>", "<selectedCodec>"]
        allowed_file_types = ['video', "audio"]
        allowed_quality = ["max", "2160", "1440", "1080", "720", "480", "360", "240", "144"]
        allowed_codecs = ["h264", "av1", "vp9"]
        allowed_audio_formats = ["mp3", "ogg", "wav", "opus"]

        default_codec = "h264"
        default_quality = "1080"
        default_file_name = "<videoTitle> - <selectedQuality>"
        default_file_type = "video"
        default_audio_format = "wav"
        default_mute_audio = False
        default_overwrite_files = False
        default_overwrite_directories = False
        default_download_directory = str(Path.home() / "Downloads")
        default_ask_for_input = False


        def useCustom(self, **options):
            empty_dict = {
                'codec': None,
                'quality': None,
                'file_name': None,
                'file_type': None,
                'audio_format': None,
                'mute_audio': None,
                'overwrite_files': None,
                'overwrite_directories': None,
                'download_directory': None,
                'ask_for_input': None
            }


            new_options = empty_dict
            for option in options:
                new_options[option] = options[option]
            
            self.codec = new_options['codec'] if new_options['codec'] is not None else self.default_codec
            self.quality = new_options['quality'] if new_options['quality'] is not None else self.default_quality
            self.file_name = new_options['file_name'] if new_options['file_name'] is not None else self.default_file_name
            self.file_type = new_options['file_type'] if new_options['file_type'] is not None else self.default_file_type
            self.audio_format = new_options['audio_format'] if new_options['audio_format'] is not None else self.default_audio_format
            self.mute_audio = new_options['mute_audio'] if new_options['mute_audio'] is not None else self.default_mute_audio
            self.overwrite_files = new_options['overwrite_files'] if new_options['overwrite_files'] is not None else self.default_overwrite_files
            self.overwrite_directories = new_options['overwrite_directories'] if new_options['overwrite_directories'] is not None else self.default_overwrite_directories
            self.download_directory = new_options['download_directory'] if new_options['download_directory'] is not None else self.default_download_directory
            self.ask_for_input = new_options['ask_for_input'] if new_options['ask_for_input'] is not None else self.default_ask_for_input

            self.correctOptions()


        def useDefault(self):
            self.codec = self.default_codec
            self.quality = self.default_quality
            self.file_name = self.default_file_name
            self.file_type = self.default_file_type
            self.audio_format = self.default_audio_format
            self.mute_audio = self.default_mute_audio
            self.overwrite_files = self.default_overwrite_files
            self.overwrite_directories = self.default_overwrite_directories
            self.download_directory = self.default_download_directory
            self.ask_for_input = self.default_ask_for_input


        def useJson(self, path):
            if not isinstance(path, str):
                raise TypeError("path must be a string")
            try:
                with open(path, 'r') as f:
                    options = json.load(f)
                    options['download_directory'] = options['download_directory'].replace('<defaultDirectory>', self.default_download_directory)
                    self.useCustom(**options)
            except Exception as e:
                raise Exception(f'There was something wrong while importing the json file: {e}')

        def correctOptions(self):
            if not self.codec in self.allowed_codecs: raise Exception('Something is wrong with codec value')
            if not self.file_type in self.allowed_file_types: raise Exception('Something is wrong with file_type value')
            if not self.quality in self.allowed_quality: raise Exception('Something is wrong with quality value')
            if not self.audio_format in self.allowed_audio_formats: raise Exception('Something is wrong with audio_format value')
            if not isinstance(self.mute_audio, bool): raise Exception('Something is wrong with mute_audio value')
            if not isinstance(self.overwrite_files, bool): raise Exception('Something is wrong with overwrite_files value')
            if not isinstance(self.overwrite_directories, bool): raise Exception('Something is wrong with overwrite_directories value')
            if not isinstance(self.ask_for_input, bool): raise Exception('Something is wrong with ask_for_input value')
            if not os.path.exists(self.download_directory): raise Exception('Something is wrong with download_directory value')





    def downloadVideo(self, url, ask_for_input: bool = None, filename: str = None, download_directory: str = None, overwrite_files: bool = None):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        if ask_for_input is not None and not isinstance(ask_for_input, bool):
            raise TypeError("ask_for_input must be a boolean or None")
        if filename is not None and not isinstance(filename, str):
            raise TypeError("filename must be a string or None")
        if download_directory is not None and not isinstance(download_directory, str):
            raise TypeError("download_directory must be a string or None")
        if overwrite_files is not None and not isinstance(overwrite_files, bool):
            raise TypeError("overwrite_files must be a boolean or None")
        
        download_directory = download_directory if download_directory is not None else self.options.download_directory
        ask_for_input = ask_for_input if ask_for_input is not None else self.options.ask_for_input
        overwrite_files = overwrite_files if overwrite_files is not None else self.options.overwrite_files

        if not self.getUrlType(url) == 'video': raise Exception("That URL doesn't seem to be a YouTube video")

        filename = self.correctFilename(filename) if filename is not None else self.createFilename(url)

        download_directory_content = os.listdir(download_directory)

        if ask_for_input:
            while not overwrite_files and filename in download_directory_content:
                action = input(f'File "{filename}" already exists.\nDo you want to overwrite it (y/n) or rename it (r): ')
                if action.lower() not in ('y', 'n', 'r'):
                    continue

                if action.lower() == 'n':
                    print('Canceling download')
                    return
                elif action.lower() == 'r': filename = self.correctFilename(input('Enter a new filename: '))
                elif action.lower() == 'y': break

        elif not overwrite_files and filename in download_directory_content:
            raise Exception(f"Can't overwrite file named {filename}. If you want to overwrite it, add this as an argument: overwrite_files=True")


        file_path = os.path.join(download_directory, filename)

        stream_url = self.getStreamUrl(url)

        print(f'Downloading "{filename}"')

        self.captureStream(stream_url, file_path)

        print(f'Downloaded "{filename}" to {download_directory}')



    def captureStream(self, stream_url: str, file_path: str):
        if not isinstance(stream_url, str):
            raise TypeError("stream_url must be a string")
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        
        with requests.get(stream_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)


    def download(self, url: str):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        
        url = self.correctUrl(url)
        url_type = self.getUrlType(url)
        #print(url_type)
        if url_type == 'playlist':
            self.downloadPlaylist(url)
        elif url_type == 'video':
            self.downloadVideo(url)
        else: raise Exception("The URL doesn't seem to be right")

    def getUrlType(self, url: str):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        
        if url is None: return None
        if 'https://www.youtube.com/playlist?' in url:
            return 'playlist'
        elif 'https://www.youtube.com/watch' in url:
            return 'video'
        else:
            return None
        
    def correctUrl(self, url: str):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        
        if 'youtube.com/' not in url: raise Exception("The URL doesn't seem to be a YouTube URL")
        if 'https://www.' not in url and url.startswith('youtube.com/'):
            #print(url)
            url = 'https://www.' + url
        elif 'https://' not in url and url.startswith('www.youtube.com/'):
            #print(url)
            url = 'https://' + url
        return url


    def downloadPlaylist(self, url: str, ask_for_input: bool = None, make_new_directory: bool = True, new_directory_name: str = None, 
                         filename_pattern: str = None, download_directory: str = None, overwrite_files: bool = None,
                         overwrite_directories: bool = None):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        if ask_for_input is not None and not isinstance(ask_for_input, bool):
            raise TypeError("ask_for_input must be a boolean or None")
        if filename_pattern is not None and not isinstance(filename_pattern, str):
            raise TypeError("filename_pattern must be a string or None")
        if download_directory is not None and not isinstance(download_directory, str):
            raise TypeError("download_directory must be a string or None")
        if overwrite_files is not None and not isinstance(overwrite_files, bool):
            raise TypeError("overwrite_files must be a boolean or None")
        if overwrite_directories is not None and not isinstance(overwrite_directories, bool):
            raise TypeError("overwrite_directories must be a boolean or None")
        if make_new_directory is not None and not isinstance(make_new_directory, bool):
            raise TypeError("make_new_directory must be a boolean or None")
        if new_directory_name is not None and not isinstance(new_directory_name, str):
            raise TypeError("new_directory_name must be a string or None")
        
        download_directory = download_directory if download_directory is not None else self.options.download_directory
        ask_for_input = ask_for_input if ask_for_input is not None else self.options.ask_for_input
        overwrite_files = overwrite_files if overwrite_files is not None else self.options.overwrite_files
        overwrite_directories = overwrite_directories if overwrite_directories is not None else self.options.overwrite_directories

        if self.getUrlType(url) == 'playlist':
            playlist = Playlist(url)
        else:
            raise Exception("That URL doesn't seem to be a YouTube playlist")

        if make_new_directory:
            if new_directory_name is None:
                download_directory = self.makeDirectory(self.correctDirectoryName(playlist.title), download_directory, overwrite_directories=overwrite_directories)
            elif new_directory_name is not None:
                download_directory = self.makeDirectory(self.correctDirectoryName(new_directory_name), download_directory, overwrite_directories=overwrite_directories)
            if download_directory is None:
                return

        for i in range(len(playlist)):
            print(f'-- Downloading video ({i+1}/{len(playlist)}) --')
            # ask_for_input: bool = None, filename: str = None, download_directory: str = None, overwrite_files: bool = None
            if filename_pattern is None: self.downloadVideo(playlist[i], download_directory=download_directory, ask_for_input=ask_for_input, overwrite_files=overwrite_files)
            elif isinstance(filename_pattern, str): self.downloadVideo(playlist[i], download_directory=download_directory, ask_for_input=ask_for_input, filename=filename_pattern.replace('<videoNumber>', str(i+1)), overwrite_files=overwrite_files)
            print()


    def makeDirectory(self, directory_name: str, parent_directory: str, overwrite_directories: bool = None):
        # Type checks
        if not isinstance(directory_name, str):
            raise TypeError("directory_name must be a string")
        if not isinstance(parent_directory, str):
            raise TypeError("parent_directory must be a string")
        if overwrite_directories is not None and not isinstance(overwrite_directories, bool):
            raise TypeError("overwrite_directories must be a boolean or None")

        overwrite_directories = overwrite_directories if overwrite_directories is not None else self.options.overwrite_directories

        directory_path = os.path.join(parent_directory, directory_name)
        directory_exists = directory_name in os.listdir(parent_directory)

        if directory_exists:
            if overwrite_directories:
                rmtree(directory_path)
                os.mkdir(directory_path)
        else:
            os.mkdir(directory_path)

        return directory_path





    def getStreamUrl(self, url: str):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        
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
                if response['text'] == "it seems like this service is not supported yet or your link is invalid. have you pasted the right link?":
                    raise Exception('There is something wrong with the URL. Make sure it is a YouTube video URL')
                
        if not done: 
            print("Couldn't download the video")
            raise Exception("Couldn't download the video")

        
        return stream_url

    def correctFilename(self, filename: str):
        if not isinstance(filename, str):
            raise TypeError("filename must be a string")
        
        invalid_chars = r'[\/:*?"<>|]'
        correct_filename = filename
        for invalid_char in invalid_chars:
            correct_filename = correct_filename.replace(invalid_char, '')

        correct_filename = self.correctExtension(correct_filename)

        return correct_filename

    def correctDirectoryName(self, name: str):
        if not isinstance(name, str):
            raise TypeError("url must be a string")
        
        invalid_chars = r'[\/:*?"<>|]'
        correct_directory_name = name
        for invalid_char in invalid_chars:
            correct_directory_name = correct_directory_name.replace(invalid_char, '')
        return correct_directory_name

    def createFilename(self, url: str = None, correct_filename: bool = True):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        
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



    def correctExtension(self, filename: str):
        if not isinstance(filename, str):
            raise TypeError("filename must be a string")
        
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



    def getVideoTitle(self, url: str):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        video = YouTube(url)
        return video.title


    def main(self):
        while True:
            url = input('Enter video URL (q to quit): ')
            if url.lower() == 'q':
                break
            try:
                self.download(url)
            except Exception as e:
                print(f'Something went wrong while downloading: \n{e}')

            print()





if __name__ == '__main__':
    downloader = Downloader(ask_for_input=True)
    downloader.main()


    








































