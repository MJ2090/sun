function play_fetch_image() {
    let original_iamge = document.querySelector("input[name='image_f']");
    let csrf = document.querySelector("input[name='csrfmiddlewaretoken']");
    let llm_model = document.querySelector("select[name='llm_model']");
    let question = document.querySelector("textarea[name='response_question']")
    let answer = document.querySelector("textarea[name='response_answer']")

    if (original_iamge.files.length==0) {
        return;
    }

    question.value = '';
    answer.value = '';

    const request_data = new FormData();
    request_data.append('original_iamge', original_iamge.files[0]);
    request_data.append('csrfmiddlewaretoken', csrf.value);
    request_data.append('llm_model', llm_model.value);

    spinner = document.querySelector("div[name='spinner']");
    spinner.style.display = 'block';
    fetch("/play_async/", {
        method: "POST",
        body: request_data,
    }).then(response => response.json()).then((response) => {
        let data = response;
        question.value = data.question;
        answer.value = data.answer;
        spinner.style.display = 'none';
    });
}

function play_fetch_question() {
    let csrf = document.querySelector("input[name='csrfmiddlewaretoken']");
    let llm_model = document.querySelector("select[name='llm_model']");
    let question = document.querySelector("textarea[name='response_question']")
    let answer = document.querySelector("textarea[name='response_answer']")

    if (question.value=='') {
        return;
    }

    answer.value = '';

    const request_data = new FormData();
    request_data.append('original_question', question.value);
    request_data.append('csrfmiddlewaretoken', csrf.value);
    request_data.append('llm_model', llm_model.value);

    spinner = document.querySelector("div[name='spinner_question']");
    spinner.style.display = 'block';
    fetch("/play_question_async/", {
        method: "POST",
        body: request_data,
    }).then(response => response.json()).then((response) => {
        let data = response;
        answer.value = data.answer;
        spinner.style.display = 'none';
    });
}

function play_init() {
    document.querySelector(".send-button-image").addEventListener('click', function () {
        play_fetch_image();
    });

    document.querySelector(".send-button-question").addEventListener('click', function () {
        play_fetch_question();
    });

    document.querySelector("input[name='image_f']").addEventListener("change", function(e) {
        let reader = new FileReader();
        document.querySelector(".image-container").style.display = 'block';
      
        reader.onload = function(event) {
          document.getElementById("imagePreview").src = event.target.result;
        }
        
        // read the image file as a data URL.
        reader.readAsDataURL(this.files[0]);
      });
}

function initResizeElement() {
    var cover = document.querySelector(".cover");
    var element = null;
    var startY, startHeight;
    var bottom = document.createElement("div");
    bottom.className = "resizer-bottom";
    cover.appendChild(bottom);
    bottom.addEventListener("mousedown", initDrag, false);
    bottom.parentPopup = cover;
    
    function initDrag(e) {
      element = this.parentPopup;
      startY = e.clientY;
      startHeight = parseInt(
        document.defaultView.getComputedStyle(element).height,
        10
      );
      document.documentElement.addEventListener("mousemove", doDrag, false);
      document.documentElement.addEventListener("mouseup", stopDrag, false);
    }
  
    function doDrag(e) {
      element.style.height = startHeight + e.clientY - startY + "px";
    }
  
    function stopDrag() {
      document.documentElement.removeEventListener("mousemove", doDrag, false);
      document.documentElement.removeEventListener("mouseup", stopDrag, false);
    }
  }
  

$(document).ready(function () {
    play_init();
    //initResizeElement();
})