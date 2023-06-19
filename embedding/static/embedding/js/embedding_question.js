function embedding_question_fetch() {
  let question = $("textarea[name='question']");
  let character = $("select[name='character']");
  let csrf = $("input[name='csrfmiddlewaretoken']");
  let answer = $("textarea[name='answer']");
  answer.val('');
  answer.hide();
  $("div[name='spinner']").show();

  let context_p = document.querySelector("p[name='answer_context']");
  if (context_p) {
    context_p.innerHTML = '...';
  }

  const request_data = new FormData();
  request_data.append('question', question.val());
  request_data.append('character', character.val());
  request_data.append('csrfmiddlewaretoken', csrf.val());
  fetch("/embedding_question_async/", {
    method: "POST",
    body: request_data,
  }).then(response => response.json()).then((response) => {
    let data = response;
    let my_answer = data.answer
    answer.val(my_answer);
    $("div[name='spinner']").hide();
    answer.show();

    let context = data.context;
    let context_p = document.querySelector("p[name='answer_context']");
    if (context_p) {
      context_p.innerHTML = '';
      context.forEach(e => {
        context_p.innerHTML += e + '<br></br>';
      })
    }
  });
}

function embedding_question_init() {
  $('.send-button').click(function () {
    embedding_question_fetch();
    return false;
  });

  $("textarea[name='question']").keydown(function (e) {
    if (e.keyCode == 13) {
      embedding_question_fetch();
      return false;
    }
  });
}

$(document).ready(function () {
  embedding_question_init();
})