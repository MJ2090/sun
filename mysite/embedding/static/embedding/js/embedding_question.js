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
      let data = JSON.parse(response);
      let my_answer = data.answer
      let audio_address = data.audio_address
      answer.val(my_answer);
      $("div[name='spinner").hide();
      answer.show();

      if (enable_speech[0].checked && audio_address != '') {
        let source = $("source[name='source']");
        source.attr('src', '/static/embedding/media/' + audio_address + '.mp3');
        let audio = $("audio[name='audio']");
        audio[0].load();
      }
    },
  })
}

function init() {
  // Audio play starts
  $("input[name='enable_speech']").click(function () {
    if (!this.checked) {
      let audio = $("audio[name='audio'");
      audio[0].pause();
    }
  });

  $("input[name='show_controls']").click(function () {
    let audio = $("audio[name='audio'").toggle(this.checked);
  });

  $("audio[name='audio'").on('canplaythrough', function () {
    this.play();
  });
  // Audio play ends

  $('.send-button').click(function () {
    async_call();
    return false;
  });
}

$(document).ready(function () {
  init();
})