let image_model = null;
let question_modal = null;

function play_fetch_image() {
  show_modal(image_model, true);
  let original_image = document.querySelector("input[name='image_f']");
  let csrf = document.querySelector("input[name='csrfmiddlewaretoken']");
  let llm_model_value = get_llm_model();
  let question = document.querySelector("textarea[name='response_question']")
  let answer = document.querySelector("textarea[name='response_answer']")

  if (original_image.files.length == 0) {
    return;
  }

  question.value = '';
  answer.value = '';

  const request_data = new FormData();
  request_data.append('original_image', original_image.files[0]);
  request_data.append('csrfmiddlewaretoken', csrf.value);
  request_data.append('llm_model', llm_model_value);

  fetch("/quiz_image_async/", {
    method: "POST",
    body: request_data,
  })
    .then(response => response.json())
    .then((response) => {
      let data = response;
      question.value = data.question;
    })
    .finally(() => {
      show_modal(image_model, false);
    });
}

function play_fetch_question() {
  show_modal(question_model, true);
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

  fetch("/quiz_question_async/", {
    method: "POST",
    body: request_data,
  })
    .then(response => response.json())
    .then((response) => {
      let data = response;
      answer.value = data.answer;
    })
    .finally(() => {
      show_modal(question_model, false);
    });
}

function get_llm_model() {
  let c = document.querySelectorAll("input[type='radio']:checked");
  if (c.length > 0) {
    return c[0].value;
  }
  return 'kuai';
}

function quiz_init() {
  image_model = new bootstrap.Modal('#imageModal', {});
  question_model = new bootstrap.Modal('#questionModal', {});

  document.querySelector("input[type='radio']").setAttribute('checked', true);
  document.querySelector(".send-button-question").addEventListener('click', function () {
    play_fetch_question();
  });

  document.querySelector(".play-choose-button").addEventListener('click', function () {
    document.querySelector("input[name='image_f']").click();
  });

  document.querySelector("input[name='image_f']").addEventListener("change", function (e) {
    let reader = new FileReader();
    var fileName = document.querySelector("input[name='image_f']").value.split('/').pop().split('\\').pop();
    document.querySelector("#play-choose-text").value = fileName;

    reader.readAsDataURL(this.files[0]);
    play_fetch_image();
  });
  $('[data-toggle="tooltip"]').tooltip();

  var bt = document.getElementById('clipboard-icon-answer');
  let s = new bootstrap.Tooltip(bt);
  document.querySelector("#clipboard-icon-answer").addEventListener('click', copy_clipboard_answer);
}

function show_modal(modal, show) {
  if (show) {
    modal.show();
  } else {
    modal.hide();
  }
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