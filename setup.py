from setuptools import setup, find_packages

setup(
    name="yt_monk",
    version="0.1.1-alpha",
    author="Vojtech",  # Add your name
    author_email="officialvojta@gmail.com",  # Add your email
    description="A simple Python package for downloading videos and playlists from YouTube",
    long_description=open('pypi_readme.md').read(),  # Add long description from README
    long_description_content_type='text/markdown',  # Specify the format of the long description
    url="https://github.com/vojtikDortik/yt-monk",  # Add the URL of the project
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",  # Change based on your development status
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[  # Add your package's dependencies here
        'requests>=2.24.0',
        'pytube>=10.0.0'
    ],
    entry_points={
        'console_scripts': [
            'yt-monk=yt_monk.cli:main',  # Replace `your_module` and `main` with your module and function if applicable
        ],
    },
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    keywords="youtube downloader video playlist",
)
