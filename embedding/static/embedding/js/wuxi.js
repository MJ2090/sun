function fetch_documents() {
  let model = $("textarea[name='question']");
  let csrf = $("input[name='csrfmiddlewaretoken']");

  const request_data = new FormData();
  request_data.append('question', model.val());
  request_data.append('csrfmiddlewaretoken', csrf.val());
  fetch("/embedding_fetch_model_async/", {
    method: "POST",
    body: request_data,
  }).then(response => response.json()).then((response) => {
    let data = response;
    let my_answer = data.answer
    answer.val(my_answer);
    $("div[name='spinner").hide();
    answer.show();
  });
}

$(document).ready(function () {
  fetch_documents();
})