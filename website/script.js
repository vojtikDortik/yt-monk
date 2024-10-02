function showOverlay(text) {
    document.getElementById('overlay-text').innerHTML = text;
    // document.getElementById('overlay').style.display = 'flex';
    document.getElementById('overlay').style.top = 0;
}

function closeOverlay() {
    document.getElementById('overlay').style.top = '100%';
}

function downloadFile(url, filename) {
    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => console.error('Download failed:', error));
}






document.querySelectorAll('.border-button').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default anchor click behavior
        const option = e.target.innerText;

        let filename = 'file';

        let tutorialText = '';

        switch (option) {
            case 'Chrome Extension':
                filename = 'yt-monk_chrome-extension.zip';
                tutorialText = `





                    <h3>Getting the Chrome Extension</h3>
                    <ol>
                        <li>Download the zipped version of the Chrome extension.</li>
                        <li>Unzip the downloaded file to access the extension folder.</li>
                        <li>Open Chrome and navigate to <code>chrome://extensions/</code>.</li>
                        <li>Enable Developer mode in the top right corner.</li>
                        <li>Click on Load unpacked in the left top corner.</li>
                        <li>Select the extension directory (the folder containing <code>manifest.json</code>).</li>
                        <li>When you visit a YouTube video, look for the <strong>MonkLoad</strong> button to download videos.</li>
                    </ol>`;
                break;
            case 'EXE File':
                filename = 'yt-monk-app.exe';
                tutorialText = `
                    <h3>Getting the Windows Executable</h3>
                    <ol>
                        <li>Click to download the <strong>yt_monk.exe</strong> file.</li>
                        <li>Locate the downloaded file and double-click to run it.</li>
                        <li>If Windows warns you about the file, click on <strong>More info</strong> and then <strong>Run anyway</strong>.</li>
                        <li>Follow the on-screen prompts to enter a YouTube video or playlist URL.</li>
                    </ol>`;
                break;
            case 'Python Script':
                filename = 'yt-monk_python.py';
                tutorialText = `
                    <h3>Getting the Python File</h3>
                    <ol>
                        <li>Download <strong>yt_monk.py</strong> and <strong>requirements.txt</strong>.</li>
                        <li>Open your terminal and run:</li>
                        <pre><code>pip install -r requirements.txt</code></pre>
                        <li>To execute the script, run:</li>
                        <pre><code>python yt_monk.py</code></pre>
                        <li>You will be prompted to enter a video or playlist URL. Enter the desired URL and hit enter to start downloading.</li>
                    </ol>`;
                break;
            case 'PyPi Package':
                tutorialText = `
                    <h3>Getting the Library</h3>
                    <ol>
                        <li>To install the library, open your terminal and run:</li>
                        <pre><code>pip install yt-monk</code></pre>
                        <li>For more information, visit the PyPi project site: <a href="https://pypi.org/project/yt-monk/" target="_blank">yt-monk</a>.</li>
                        <li>You can now use the library in your Python scripts. See the README for examples on how to implement it.</li>
                    </ol>`;
                break;
            default:
                tutorialText = '<p>No tutorial available for this option.</p>';
            

            
        }

        
        if (filename != 'file') {downloadFile(button.href, filename);}
        

        showOverlay(tutorialText);
    });
});
