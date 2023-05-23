function play_fetch_image() {
  let original_iamge = document.querySelector("input[name='image_f']");
  let csrf = document.querySelector("input[name='csrfmiddlewaretoken']");
  let llm_model_value = get_llm_model();
  let question = document.querySelector("textarea[name='response_question']")
  let answer = document.querySelector("textarea[name='response_answer']")

  if (original_iamge.files.length == 0) {
    return;
  }

  question.value = '';
  answer.value = '';

  const request_data = new FormData();
  request_data.append('original_iamge', original_iamge.files[0]);
  request_data.append('csrfmiddlewaretoken', csrf.value);
  request_data.append('llm_model', llm_model_value);

  spinner = document.querySelector("div[name='spinner']");
  spinner.style.display = 'block';
  fetch("/play_image_async/", {
    method: "POST",
    body: request_data,
  }).then(response => response.json()).then((response) => {
    let data = response;
    question.value = data.question;
    spinner.style.display = 'none';
  });
}

function play_fetch_question() {
  let csrf = document.querySelector("input[name='csrfmiddlewaretoken']");
  let llm_model_value = get_llm_model();
  let question = document.querySelector("textarea[name='response_question']")
  let answer = document.querySelector("textarea[name='response_answer']")

  if (question.value == '') {
    return;
  }

  answer.value = '';

  const request_data = new FormData();
  request_data.append('original_question', question.value);
  request_data.append('csrfmiddlewaretoken', csrf.value);
  request_data.append('llm_model', llm_model_value);

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

function get_llm_model() {
  document.querySelectorAll("input[type='radio']").forEach(item => {
    if (item.getAttribute('checked') == true) {
      return item.value;
    }
  });
  return 'kuai';
}

function quiz_init() {
  document.querySelectorAll("input[type='radio']").forEach(item => {
    item.classList.add('form-check-input','me-2');
  });

  document.querySelector("input[type='radio']").setAttribute('checked', true);
  document.querySelector(".send-button-image").addEventListener('click', function () {
    play_fetch_image();
  });

  document.querySelector(".send-button-question").addEventListener('click', function () {
    play_fetch_question();
  });

  document.querySelector(".play-choose-button").addEventListener('click', function () {
    document.querySelector("input[name='image_f']").click();
  });

  document.querySelector("input[name='image_f']").addEventListener("change", function (e) {
    let reader = new FileReader();
    document.querySelector(".image-container").style.display = 'block';
    var fileName = document.querySelector("input[name='image_f']").value.split('/').pop().split('\\').pop();
    document.querySelector("#play-choose-text").value = fileName;

    reader.onload = function (event) {
      document.getElementById("imagePreview").src = event.target.result;
    }

    // read the image file as a data URL.
    reader.readAsDataURL(this.files[0]);
  });
  $('[data-toggle="tooltip"]').tooltip();

  var bt = document.getElementById('clipboard-icon-answer');
  let s = new bootstrap.Tooltip(bt);
  document.querySelector("#clipboard-icon-answer").addEventListener('click', copy_clipboard_answer);
}

function copy_clipboard_answer(e) {
  let answer = document.querySelector("textarea[name='response_answer']")
  answer.select();
  answer.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(answer.value);
  let bt = document.getElementById('clipboard-icon-answer');
  bt.setAttribute('data-bs-original-title', 'Copied!');
  bootstrap.Tooltip.getInstance(bt).show();

  setTimeout(() => {
    bootstrap.Tooltip.getInstance(bt).hide();
    bt.setAttribute('data-bs-original-title', 'Copy to clipboard');
  }, 1000);
}

$(document).ready(function () {
  quiz_init();
})