function async_call() {
  let text = $("textarea[name='text']");
  let name = $("input[name='name']");
  let csrf = $("input[name='csrfmiddlewaretoken']");
  let answer = $("p[name='response']");
  answer.val('');
  answer.hide();
  $("div[name='spinner").show();
  $.ajax({
    type: 'POST',
    url: "/embedding_training_async/",
    data: {
      text: text.val(),
      name: name.val(),
      csrfmiddlewaretoken: csrf.val(),
    },
    success: function (response) {
      answer.text(response);
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