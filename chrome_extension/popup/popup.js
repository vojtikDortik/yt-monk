// Define utility functions at the top
function getTabUrl(callback) {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentTab = tabs[0]; // There will be only one in this array
    const url = currentTab.url;
    callback(url);
  });
}

async function getStreamUrl(apiUrl, options) {
  try {
    let response = await fetch(apiUrl, {
      method: "POST",
      body: JSON.stringify(options),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }

    let data = await response.json();
    if (data.status === "stream" && data.url) {
      return data.url;
    } else {
      throw new Error("Stream URL not available or incorrect status");
    }
  } catch (error) {
    console.error("Error getting stream URL:", error);
    throw error;
  }
}

async function downloadStream(streamUrl) {
  try {
    const link = document.createElement("a");
    link.href = streamUrl;
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error("Error downloading video:", error);
  }
}

function listen() {
  document.getElementById("downloadBtn").addEventListener("click", async function () {
    const input = document.getElementById("input");
    input.classList.remove("input-error");
    input.classList.add("normal-input");

    const url = input.value;
    const apiUrl = "https://olly.imput.net/api/json";
    const btn = document.getElementById("downloadBtn");

    try {
      // Retrieve saved options before downloading
      chrome.storage.sync.get(
        { quality: "1080", codec: "h264", audioFormat: "wav" }, // Default values
        (items) => {
          // download section
          btn.disabled = true;
          btn.innerText = "Downloading...";

          // Use saved options
          let options = {
            url: url,
            vCodec: items.codec || "h264",
            vQuality: items.quality || "1080",
            aFormat: items.audioFormat || "wav",
            filenamePattern: "pretty",
            isAudioOnly: false,
            isTTFullAudio: false,
            isAudioMuted: false,
            disableMetadata: false,
            dubLang: "en",
          };

          getStreamUrl(apiUrl, options)
            .then((streamUrl) => downloadStream(streamUrl))
            .catch((error) => {
              console.error(error);
              input.classList.remove("normal-input");
              input.classList.add("input-error");
            })
            .finally(() => {
              btn.disabled = false;
              btn.innerText = "Download";
            });
        }
      );
    } catch (error) {
      input.classList.remove("normal-input");
      input.classList.add("input-error");
      btn.disabled = false;
      btn.innerText = "Download";
    }
  });

  document.getElementById("optionsBtn").addEventListener("click", function () {
    document.getElementById("optionsPanel").classList.add("show");

    chrome.storage.sync.get(
      { quality: "1080", codec: "h264", audioFormat: "wav" }, // Default values
      (items) => {
        document.getElementById("quality").value = items.quality;
        document.getElementById("codec").value = items.codec;
        document.getElementById("audioFormat").value = items.audioFormat;
      }
    );
  });

  document.getElementById("closeOptionsBtn").addEventListener("click", function () {
    document.getElementById("optionsPanel").classList.remove("show");
  });

  document.getElementById("closeExtensionBtn").addEventListener("click", function () {
    window.close();
  });

  document.getElementById("saveOptionsBtn").addEventListener("click", function () {
    const quality = document.getElementById("quality").value;
    const codec = document.getElementById("codec").value;
    const audioFormat = document.getElementById("audioFormat").value;

    chrome.storage.sync.set({ quality, codec, audioFormat, edited: true }, () => {
      console.log("Options saved");
    });
  });
}

getTabUrl(function (url) {
  const input = document.getElementById("input");
  if (url.startsWith("https://www.youtube.com/watch?")) {
    input.value = url;
  }

  listen();
});
