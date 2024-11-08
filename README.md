



<!-- PROJECT LOGO -->

<div align="center">


<h1 align="center" style="font-size: 40px">YouTube Monk</h1>


  <p align="center">
    <img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/logo_transparent_full_size.png?raw=true" width=50% height=auto>
    <br />
    A YouTube video and playlist downloader made in Python (or JS).
    <br />
    <br />
    <a href="https://github.com/vojtikDortik/yt-monk/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/vojtikDortik/yt-monk/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#important">Important</a>
    </li>
    <li><a href="#downloads">Downloads</a></li>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## Important

!! - This doesn't work anymore. sorry. I might try to make it work again, but not for now - !!



## Downloads
#### TL;DR:

### Chrome extension
This is probalby the most usable part of my project. You can download the video directly on YouTube using a button added by the JavaScript code. You can also change the options in the popup. 


[Download zip](https://github.com/vojtikDortik/yt-monk/blob/master/dist/chrome_extension.zip) and follow the <a href="#getting-started">`instructions`</a> or install on `Chrome Store` (I'll add this soon)


### Python library 
This is very useful for writing your own code with downloading youtube videos. For more info about the library, check the <a href="#usage">`usage`</a>. 

`Install using pip:`
```sh
pip install yt-monk
```

PyPi project site: [`yt-monk`](https://pypi.org/project/yt-monk/)



### Simple EXE file
This is just a test of windows executable app. It can download videos and playlists. You can not set the options yet - it is using the defaults. 

[Download here](https://github.com/vojtikDortik/yt-monk/blob/master/dist/yt_monk.exe) 

### Simple Python file
This is basically the same as the EXE file, but it is not built to EXE, so you can view and edit the code. You can use custom settings if you download the example `options.json` file and add `json_path='path_to/options.json'` argument to the main function.

`Downloading:`\
The code: [`yt_monk.py`](https://github.com/vojtikDortik/yt-monk/blob/master/yt_monk/yt_monk.py)\
Requiered libraries: [`requirements.txt`](https://github.com/vojtikDortik/yt-monk/blob/master/requirements.txt)\
The options file: [`options.json`](https://github.com/vojtikDortik/yt-monk/blob/master/examples/options.json)







<br>


<!-- ABOUT THE PROJECT -->
## About The Project

This little project began when I wanted to download a playlist from YouTube. For downloading single videos, I always use [cobalt.tools](https://cobalt.tools), because it is ad-free and open-source, but it is still missing something... a playlist downloader. I tried a few other YT downloaders to download a playlist, but I wasn't happy with their functionality. 

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/cobalt.png?raw=true" width=100% height=auto style="max-width: 800px">

([cobalt](https://cobalt.tools) website)

So I decided to make my own YT video and playlist downloader in Python.

### Making the program
First, I downloaded a [testing video](https://www.youtube.com/watch?v=9bZkp7q19f0) and captured the network traffic from [cobalt](https://cobalt.tools), because I wanted to know how do they download videos:

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/network.png?raw=true" width=auto height=100% style="max-height: 200px">

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/request.png?raw=true" width=auto height=100% style="max-height: 250px">

(the network traffic capture)

Based on that capture, I found out, that the user recieves the video as a stream of data from `olly.imput.net/api`. Now I need to know how to make the request to their API to get the stream URL, so I looked into the JavaScript code, that was downloading the videos:

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/code1.png?raw=true" width=100% height=auto style="max-width: 700px">

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/code2.png?raw=true" width=100% height=auto style="max-width: 450px">

(some of the JavaScript code of the website)

Now that I know how to get the stream URL, I can recreate it in python:
```python
response = json.loads(requests.post(self.api_url, headers=headers, data=json.dumps(data)).text)
if response['status'] == 'stream':
  stream_url = response['url']
```
And capture the stream to a file:

```python
def captureStream(self, stream_url, file_path):
  with requests.get(stream_url, stream=True) as r:
    r.raise_for_status()
      with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
          f.write(chunk)
```


Then I just made some more functions.



### To-do 

- [ ] Upload extension to chrome store
- [x] Make a js chrome extension 
- [x] Make an exe app
- [x] Reorganize files
- [x] Make a python package work
- [x] Upload the package to PyPi






<!-- GETTING STARTED -->
## Getting Started

Now you have 4 options: download it as an exe file and run it on Windows without the need to install Python or you can download the Python file and run that. You can also install it as a python library and use it in your code. The final option and the most usable one is using it as a Chrome extension (I am still working on that - it is test version).

### Getting the Chrome extension


I will upload it to Chrome Store soon (hopefully)

<br>

1. Download the [zipped version](https://github.com/vojtikDortik/yt-monk/blob/master/dist/chrome_extension.zip) of the Chrome extension

2. Unzip it

3. Enable `Developer mode` in Chrome in the right top corner of [`chrome://extensions/`](chrome://extensions/)

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/chrome_developed_mode.png?raw=true" width=300px height=auto style="max-width: 300px">

4. Click on `Load unpacked` in the left top corner

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/chrome_load_unpacked.png?raw=true" width=300px height=auto style="max-width: 450px">

5. Select the extension directory (the directory that has `manifest.json` inside)

6. That is it!

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/chrome_extension.png?raw=true" width=300px height=auto style="max-width: 450px">

### Getting the library

To install [the library from PyPi](https://pypi.org/project/yt-monk/), just run this command

```sh
pip install yt-monk
```



### Getting the Windows executable

1. Download [`yt_monk.exe`](https://github.com/vojtikDortik/yt-monk/blob/master/dist/yt_monk.exe)
2. Run it on Windows
3. Windows might mark it as a , so just click on `More info` and then click on `Run anyway` (I could try to fix that, but it is not my main goal now and also idk how to fix it)

    If you realy don't trust it (I get it), you can download the python code or the [PyPi package](https://pypi.org/project/yt-monk/)

### Getting the Python file

1. Download [`yt_monk.py`](https://github.com/vojtikDortik/yt-monk/blob/master/yt_monk/yt_monk.py) and [`requirements.txt`](https://github.com/vojtikDortik/yt-monk/blob/master/requirements.txt)

2. Install [`requirements.txt`](https://github.com/vojtikDortik/yt-monk/blob/master/requirements.txt) using pip:
    ```sh
    pip install -r requirements.txt
    ```

3. Run it using python:

    ```python
    python yt_monk.py
    ```






<!-- USAGE EXAMPLES -->
## Usage
Here are some basic examples of using my code

### Using as an application
When you run [`yt_monk.py`](https://github.com/vojtikDortik/yt-monk/blob/master/yt_monk/yt_monk.py) or [`yt_monk.exe`](https://github.com/vojtikDortik/yt-monk/blob/master/dist/yt_monk.exe) or use the [package](https://pypi.org/project/yt-monk/) as a cli app, you will get prompted to enter the URL

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/cmd_usage.png?raw=true" width=100% height=auto style="max-width: 800px">

You can enter video or playlist URL (the program will detect the URL type) or `q` to quit the loop.




### Using as a Python library

Import the library and define the `downloader` object:
```python
import yt_monk

downloader = yt_monk.Downloader()
```

<br>

#### Setting the options:

You can set it using keyword arguments when defining the object:

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





### Using the Chrome extension

The extension has 2 main functions: a popup and adding a button directly to YouTube website

<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/screenshot_button_2.png?raw=true" width=100% height=auto >
<img src="https://github.com/vojtikDortik/yt-monk/blob/master/images/popup.png?raw=true" width=300px height=auto style="max-width: 450px">

When you open a youtube video, it automatically adds a button saying `MonkLoad`, but you can change that text in the popup options. If you click that button, it downloads the video using the default options.

You can also click the extension in the right top corner to display a popup with pre-filled url of the video, or you can just enter it manually.

You can edit the options using the popup window. 


``try turning on the cats button :)``


<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE.txt`](https://github.com/vojtikDortik/yt-monk/blob/master/LICENSE.txt) for more information





