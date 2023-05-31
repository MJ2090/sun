function async_call() {
  let original_pdf = document.querySelector("input[name='file_f']");
  let text = $("textarea[name='text']");
  let name = $("input[name='name']");
  let csrf = $("input[name='csrfmiddlewaretoken']");
  let answer = $("p[name='response']");
  answer.val('');
  answer.hide();
  $("div[name='spinner").show();

  const request_data = new FormData();
  request_data.append('text', text.val());
  request_data.append('name', name.val());
  request_data.append('csrfmiddlewaretoken', csrf.val());
  if (original_pdf.files.length > 0) {
    for (let index = 0; index < original_pdf.files.length; index++) {
      request_data.append('original_pdf_'+index, original_pdf.files[index]);
    }
  }
  fetch("/embedding_training_async/", {
    method: "POST",
    body: request_data,
  }).then(response => response.json()).then((response) => {
    answer.text(response.result);
    $("div[name='spinner").hide();
    answer.show();
  });
}

function init() {
  document.querySelector("input[name='file_f']").setAttribute('accept', 'application/pdf');
  $('.send-button').click(function () {
    async_call();
    return false;
  });
}

$(document).ready(function () {
  init();
})