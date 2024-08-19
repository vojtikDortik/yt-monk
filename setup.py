from setuptools import setup, find_packages

setup(
name="yt-monk",
version="0.1.0",
description="A simple Python package for downloading videos and playlists from youtube",
packages=find_packages(),
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
python_requires=">=3.6",
)