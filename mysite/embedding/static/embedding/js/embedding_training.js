function async_call() {
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
  fetch("/embedding_training_async/", {
    method: "POST",
    body: request_data,
  }).then(response => response.json()).then((response) => {
    answer.text(response);
    $("div[name='spinner").hide();
    answer.show();
  });
}

function init() {
  $('.send-button').click(function () {
    async_call();
    return false;
  });
}

$(document).ready(function () {
  init();
})