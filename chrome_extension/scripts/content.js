// Function to download the video using the provided URL
function getTabUrl(callback) {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      const currentTab = tabs[0]; // There will be only one in this array
      const url = currentTab.url;
      callback(url);
  });
}

function getElementByXpath(path) {
  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function getOptions() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(
      { quality: "1080", codec: "h264", audioFormat: "wav", fileType: "video" }, // Default values
      (items) => {
        // Assign the retrieved values
        const quality = items.quality;
        const codec = items.codec;
        const audioFormat = items.audioFormat;
        const audioOnly = (items.fileType == "audio");

        console.log("lol", quality, codec, audioFormat);
        resolve({ quality, codec, audioFormat, audioOnly });
      }
    );
  });
}

async function downloadVideo(url) {
  const apiUrl = 'https://olly.imput.net/api/json';


  try {
    const { quality, codec, audioFormat, audioOnly } = await getOptions(); // Wait for the options to be retrieved

    console.log("Retrieved options:", quality, codec, audioFormat, audioOnly);

    const options = {
      url: url,
      vCodec: codec,
      vQuality: quality,
      aFormat: audioFormat,
      filenamePattern: 'basic',
      isAudioOnly: audioOnly,
      isTTFullAudio: false,
      isAudioMuted: false,
      disableMetadata: false,
      dubLang: 'en'
    };

    const response = await fetch(apiUrl, {
      method: 'POST',
      body: JSON.stringify(options),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    if (data.status === 'stream' && data.url) {
      // Create a hidden <a> element and trigger a download
      const link = document.createElement('a');
      link.href = data.url;
      document.body.appendChild(link);
      link.click();
      link.remove();
    } else {
      console.error('Stream URL not available or incorrect status');
    }
  } catch (error) {
    console.error('Error downloading video:', error);
  }
}

// Function to inject the custom button
function addCustomButton() {
  // Create the button element
  const btn = document.createElement('button');
  btn.id = 'yt-monk-download';
  btn.className = 'yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading';
  chrome.storage.sync.get(
    {buttonText: "MonkLoad" }, // Default values
    (items) => { 
      btn.setAttribute('aria-label', items.buttonText);
      btn.setAttribute('title', items.buttonText);
    });
  btn.style.marginLeft = '6px';
  btn.style.marginRight = '6px';

  const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  icon.setAttribute('width', '24');
  icon.setAttribute('height', '24');
  icon.setAttribute('viewBox', '0 0 24 24');
  icon.setAttribute('fill', 'none');
  icon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');

  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('fill-rule', 'evenodd');
  path.setAttribute('clip-rule', 'evenodd');
  path.setAttribute('d', 'M17 18v1H6v-1h11zm-.5-6.6-.7-.7-3.8 3.7V4h-1v10.4l-3.8-3.8-.7.7 5 5 5-4.9z');
  path.setAttribute('fill', '#FFFFFF');
  icon.appendChild(path);

  const iconContainer = document.createElement('div');
  iconContainer.className = 'yt-spec-button-shape-next__icon';
  iconContainer.setAttribute('aria-hidden', 'true');
  iconContainer.appendChild(icon);
  btn.appendChild(iconContainer);


  // const iconContainer = document.createElement('div');
  // iconContainer.className = 'yt-spec-button-shape-next__icon';
  // iconContainer.setAttribute('aria-hidden', 'true');
  // const icon = document.createElement('img');
  // icon.src = 'https://img.icons8.com/?size=100&id=14100&format=png&color=FFFFFF'; // Replace with your SVG URL
  // icon.setAttribute('d', 'M17 18v1H6v-1h11zm-.5-6.6-.7-.7-3.8 3.7V4h-1v10.4l-3.8-3.8-.7.7 5 5 5-4.9z')
  // icon.style.width = '24px';
  // icon.style.height = '24px';
  // icon.alt = 'Download Video'; // Provide alternative text for accessibility
  // iconContainer.appendChild(icon);
  // btn.appendChild(iconContainer);

  const textContent = document.createElement('div');
  textContent.className = 'yt-spec-button-shape-next__button-text-content';
  chrome.storage.sync.get(
    {buttonText: "MonkLoad" }, // Default values
    (items) => { textContent.innerText = items.buttonText; });
      
  btn.appendChild(textContent);

  const feedbackShape = document.createElement('yt-touch-feedback-shape');
  feedbackShape.style.borderRadius = 'inherit';

  const feedbackShapeContainer = document.createElement('div');
  feedbackShapeContainer.className = 'yt-spec-touch-feedback-shape yt-spec-touch-feedback-shape--touch-response';
  feedbackShapeContainer.setAttribute('aria-hidden', 'true');

  const feedbackStroke = document.createElement('div');
  feedbackStroke.className = 'yt-spec-touch-feedback-shape__stroke';

  const feedbackFill = document.createElement('div');
  feedbackFill.className = 'yt-spec-touch-feedback-shape__fill';

  feedbackShapeContainer.appendChild(feedbackStroke);
  feedbackShapeContainer.appendChild(feedbackFill);
  feedbackShape.appendChild(feedbackShapeContainer);
  btn.appendChild(feedbackShape);

  const container = getElementByXpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]');
  if (container) {
    container.style.position = 'relative';
    container.appendChild(btn);

    // Move the button to be the 2nd child element
    const firstChild = container.children[1];
    if (firstChild) {
      container.insertBefore(btn, firstChild);
    }

    btn.addEventListener('click', () => {
      const url = window.location.href;
      downloadVideo(url);
      
    });
  }
  else {
    console.log('buhuh');
  }
}


function watchUrlChanges() {

  new MutationObserver(() => {
    const url = location.href;
    // const parent = document.querySelector("#top-level-buttons-computed > yt-button-view-model");
    const parent = getElementByXpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]');
    const button = document.querySelector('#yt-monk-download');

    if ((parent) && (url.startsWith('https://www.youtube.com/watch?') && (!button))) {
      console.log('lolmao');
      addCustomButton(); // Re-run the script when URL changes
    }
  }).observe(document, { subtree: true, childList: true });
}


watchUrlChanges()