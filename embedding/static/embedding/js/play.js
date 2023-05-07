'use strict';

let video = null;
let canvas;
let button;

function play_init() {
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

const constraints = {
    audio: false,
    video: true
};

function handleSuccess(stream) {
    window.stream = stream; // make stream available to browser console
    video.srcObject = stream;
}

function handleError(error) {
    console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
}

navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);

$(document).ready(function () {
    play_init();
})