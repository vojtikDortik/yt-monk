<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->




<!-- PROJECT LOGO -->
<br />
<div align="center">


<h align="center" style="font-size: 40px">YT Monk</h>

  <p align="center">
    A YouTube video and playlist downloader made in Python.
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
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This little project started when I wanted to download a playlist from YouTube. For downloading single videos, I always use [Cobalt.tools](cobalt.tools), because it is ad-free and open-source, but it is still missing something... a playlist downloader. I tried a few other YT downloaders to download a playlist, but I wasn't happy with their functioanlity. 

<img src="images/cobalt.png" alt="Logo" width=auto height=200>

([Cobalt.tools](cobalt.tools) website)

So I decided to make my own YT video and playlist downloader in Python.

### Making the program
First, I downloaded a [testing video](https://www.youtube.com/watch?v=9bZkp7q19f0) and captured the network traffic from [Cobalt.tools](cobalt.tools), because I wanted to know, how do they download videos:

<img src="images/network.png" alt="Logo" width=auto height=180>
<img src="images/request.png" alt="Logo" width=auto height=200>

(the network traffic capture)

Based on that capture, I found out, that the user recieves the video as a stream of data from `olly.imput.net/api`. Now I need to know how to make the request to their API to get the stream URL, so I looked into the JavaScript code, that was downloading the videos:

<img src="images/code1.png" alt="Logo" width=auto height=600>
<img src="images/code2.png" alt="Logo" width=auto height=170>

(JavaScript code of the website)

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


Then I just made some more functions and it was done.







<!-- GETTING STARTED -->
## Installation

Now I will show you how to use my code as an application or as a python library.

### Getting the app

1. Clone the repo:

    ```sh
    git clone https://github.com/vojtikDortik/yt-monk.git
    ```

2. Install required libraries:

    ```sh
    pip install -r requirements.txt
    ```

3. Edit the `options.json` file. (you can leave it on the default optins)




### Getting the library

1. Download these three files:

    * `ytMonk.py`
    * `options.json`
    * `requirements.txt`

2. Install required libraries:

    ```sh
    pip install -r requirements.txt
    ```

3. Edit the `options.json` file. (you can leave it on the default optins)









<!-- USAGE EXAMPLES -->
## Usage
Here are some basic examples of using my code

### Using as an application
When you run the `ytMonk.py` file
  ```python
  python ytMonk.py
  ```

you will get prompted to enter the URL

```
Enter video URL (q to quit): 
```

You can enter video or playlist URL (the program will detect the URL type) or `q` to quit the loop.

### Using as a Python library

Import the library and define the `downloader` object:
```python
import ytMonk

downloader = ytMonk.YT_Downloader()
```

Downloading a video:


```python
video_url = 'https://www.youtube.com/watch?v=9bZkp7q19f0' 

downloader.downloadVideo(video_url)
```

Downloading a playlist:

```python
playlist_url = 'https://www.youtube.com/playlist?list=PL2_OBreMn7FrDzinpFROg9vwc9FI_F6ev' 

downloader.downloadPlaylist(playlist_url)
```










<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.











<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/vojtikDortik/yt-monk.svg?style=for-the-badge
[contributors-url]: https://github.com/vojtikDortik/yt-monk/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/vojtikDortik/yt-monk.svg?style=for-the-badge
[forks-url]: https://github.com/vojtikDortik/yt-monk/network/members
[stars-shield]: https://img.shields.io/github/stars/vojtikDortik/yt-monk.svg?style=for-the-badge
[stars-url]: https://github.com/vojtikDortik/yt-monk/stargazers
[issues-shield]: https://img.shields.io/github/issues/vojtikDortik/yt-monk.svg?style=for-the-badge
[issues-url]: https://github.com/vojtikDortik/yt-monk/issues
[license-shield]: https://img.shields.io/github/license/vojtikDortik/yt-monk.svg?style=for-the-badge
[license-url]: https://github.com/vojtikDortik/yt-monk/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 