function async_call() {
  let question = $("textarea[name='question']");
  let character = $("select[name='character']");
  let csrf = $("input[name='csrfmiddlewaretoken']");
  let answer = $("textarea[name='answer']");
  answer.val('');
  answer.hide();
  $("div[name='spinner").show();
  $.ajax({
    type: 'POST',
    url: "/embedding_question_async/",
    data: {
      question: question.val(),
      character: character.val(),
      csrfmiddlewaretoken: csrf.val(),
    },
    success: function (response) {
      answer.val(response);
      $("div[name='spinner").hide();
      answer.show();
    },
  })
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