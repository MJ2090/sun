function play_fetch() {
    let original_iamge = document.querySelector("input[name='image_f']");
    let csrf = document.querySelector("input[name='csrfmiddlewaretoken']");
    let llm_model = document.querySelector("select[name='llm_model']");
    let question = document.querySelector("textarea[name='response_question']")
    let answer = document.querySelector("textarea[name='response_answer']")

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

function play_init() {
    document.querySelector(".send-button").addEventListener('click', function () {
        play_fetch();
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

$(document).ready(function () {
    play_init();
})