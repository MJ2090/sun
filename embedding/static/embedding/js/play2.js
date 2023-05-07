'use strict';



let videoElement;
let videoSelect;
let selectors;
let video = null;
let canvas;
let button;

function play_init() {
    videoElement = document.querySelector('video');
    videoSelect = document.querySelector('select#videoSource');
    selectors = [videoSelect];
    navigator.mediaDevices.enumerateDevices().then(gotDevices).catch(handleError);
    videoSelect.onchange = start;
    start();
}

function snapshot_play_init() {
    // Put variables in global scope to make them available to the browser console.
    video = document.querySelector('video');
    canvas = window.canvas = document.querySelector('canvas');
    canvas.width = 480;
    canvas.height = 360;
    button = document.querySelector('.screenshot-button');
    button.onclick = function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        // link.download = 'canvas_image.png';
        // link.click();


        var image = canvas.toDataURL('image/png');
        const request_data = new FormData();
        request_data.append('image', image);
        fetch("/play/", {
            method: "POST",
            body: request_data,
        }).then(response => response.json()).then((response) => {
            let s=0;
        });
    };
}


function gotDevices(deviceInfos) {
    // Handles being called several times to update labels. Preserve values.
    const values = selectors.map(select => select.value);
    selectors.forEach(select => {
        while (select.firstChild) {
            select.removeChild(select.firstChild);
        }
    });
    for (let i = 0; i !== deviceInfos.length; ++i) {
        const deviceInfo = deviceInfos[i];
        const option = document.createElement('option');
        option.value = deviceInfo.deviceId;
        if (deviceInfo.kind === 'videoinput') {
            option.text = deviceInfo.label || `camera ${videoSelect.length + 1}`;
            videoSelect.appendChild(option);
        } else {
            console.log('Some other kind of source/device: ', deviceInfo);
        }
    }
    selectors.forEach((select, selectorIndex) => {
        if (Array.prototype.slice.call(select.childNodes).some(n => n.value === values[selectorIndex])) {
            select.value = values[selectorIndex];
        }
    });
}

function gotStream(stream) {
    window.stream = stream; // make stream available to console
    videoElement.srcObject = stream;
    return navigator.mediaDevices.enumerateDevices();
}

function handleError(error) {
    console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
}

function start() {
    if (window.stream) {
        window.stream.getTracks().forEach(track => {
            track.stop();
        });
    }
    const videoSource = videoSelect.value;
    const constraints = {
        video: { deviceId: videoSource ? { exact: videoSource } : undefined }
    };
    navigator.mediaDevices.getUserMedia(constraints).then(gotStream).then(gotDevices).catch(handleError);
}


$(document).ready(function () {
    play_init();
    snapshot_play_init();
})