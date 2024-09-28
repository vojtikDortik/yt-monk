



<!-- PROJECT LOGO -->

<div align="center">


<h1 align="center" style="font-size: 40px">YouTube Monk</h1>


  <p align="center">
    A YouTube video and playlist downloader made in Python.
    <br />
    <br />
    <a href="https://github.com/vojtikDortik/yt-monk/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    -
    <a href="https://github.com/vojtikDortik/yt-monk/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>




<!-- GETTING STARTED -->
## Installing the library

To install the library from PyPi, just run this command:

```sh
pip install yt-monk
```





<!-- USAGE EXAMPLES -->
## Usage

Import the library and define the `downloader` object:
```python
import yt_monk

downloader = yt_monk.Downloader()
```

<br>

#### Setting the options:

You can set the options using keyword arguments when defining the object:

```python
downloader = yt_monk.Downloader(quality='720', codec='av1')
```

or you can set it using the `options.useCustom` function:

```python
downloader = yt_monk.Downloader()

downloader.options.useCustom(quality='720', codec='av1')
```

<br>

#### Here are all the options you can set:

codec -> `"h264"`, `"av1"`, `"vp9"`

quality -> `"max"`, `"2160"`, `"1440"`, `"1080"`, `"720"`, `"480"`, `"360"`, `"240"`, `"144"`

file_name -> this can be set to any valid filename. you can use placeholders: `<videoTitle>`, `<selectedQuality>`, `<selectedCodec>`

file_type -> the file type can be either `"video"` or `"audio"`

audio_format -> `"mp3"`, `"ogg"`, `"wav"`, `"opus"`

mute_audio -> `True` or `False`

overwrite_files -> this tells the program to overwrite existing files: `True` or `False`

overwrite_directories -> this tells the program to overwrite existing directories: `True` or `False`

download_directory -> the directory that the downloaded files will be saved to. you can use placeholder for default download directory like `C:\users\name\Downloads\` on windows: `<defaultDirectory>`

ask_for_input -> if enabled, the code will ask whether or not to overwrite a file or a directory: `True` or `False`

<br>

#### Using JSON options file:
Alternatively, you can use a json file to set the options. You can download an example [`options.json`](https://github.com/vojtikDortik/yt-monk/blob/master/yt_monk/options.json) file here. Then just tell the code to use the JSON file:

```python
downloader = yt_monk.Downloader(json_path=r'path/to/options.json')
```

or you can do it like this:

```python
downloader = yt_monk.Downloader()

downloader.options.useJson(json_path=r'path/to/options.json')
```

<br>

#### Downloading a video:


```python
video_url = 'https://www.youtube.com/watch?v=9bZkp7q19f0' 

downloader.downloadVideo(video_url)
```
<br>

#### Downloading a playlist:

```python
playlist_url = 'https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi' 

downloader.downloadPlaylist(playlist_url)
```










<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE.txt`](https://github.com/vojtikDortik/yt-monk/blob/master/LICENSE.txt) for more information.





