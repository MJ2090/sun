function embedding_question_fetch() {
  let question = $("textarea[name='question']");
  let character = $("select[name='character']");
  let csrf = $("input[name='csrfmiddlewaretoken']");
  let answer = $("textarea[name='answer']");
  let enable_speech = $("input[name='enable_speech']");
  answer.val('');
  answer.hide();
  $("div[name='spinner").show();

  const request_data = new FormData();
  request_data.append('question', question.val());
  request_data.append('character', character.val());
  request_data.append('enable_speech', enable_speech[0].checked);
  request_data.append('csrfmiddlewaretoken', csrf.val());
  fetch("/embedding_question_async/", {
    method: "POST",
    body: request_data,
  }).then(response => response.json()).then((response) => {
    let data = response;
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
  });
}

function embedding_question_init() {
  // Audio play starts
  $("input[name='enable_speech']").click(function () {
    if (!this.checked) {
      let audio = $("audio[name='audio']");
      audio[0].pause();
    }
  });

  $("input[name='show_controls']").click(function () {
    let audio = $("audio[name='audio']").toggle(this.checked);
  });

  $("audio[name='audio']").on('canplaythrough', function () {
    this.play();
  });
  // Audio play ends

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