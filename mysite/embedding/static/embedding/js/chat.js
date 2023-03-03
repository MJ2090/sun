function async_call() {
    let new_msg = $("input[name='message']");
    let character = $("select[name='character']");
    let model = $("select[name='training_model']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let old_msg = $(".dialogue");
    let history_msg = [];
    let role = "user";
    for (let i=0; i<old_msg.length; i++) {
        let dic = {"role": role, "content": old_msg.get(i).innerText}
        history_msg.push(dic);
        if (role == "user") {
            role = "assistant";
        } else {
            role = "user";
        }
    }
    let history = JSON.stringify(history_msg)
    new_msg.prop( "disabled", true );
    character.prop( "disabled", true );
    let new_msg_text = new_msg.val();
    new_msg.val('');

    let content = $('.message-container');

    let human_title = $("div[name='human_title']").clone();
    content.append(human_title.get(0));

    let human_msg = $("p[name='human_msg']").clone();
    human_msg.addClass("dialogue");
    human_msg.text(new_msg_text);
    content.append(human_msg.get(0));

    $.ajax({
        type: 'POST',
        url: "/sendchat/",
        data: {message: new_msg_text,
            character: character.val(),
            history: history,
            csrfmiddlewaretoken: csrf.val(),
            model: model.val(),
        },
        success: function (response) {
            new_msg.prop( "disabled", false );
            new_msg.focus();
            $('.word-count').text(response.length + ' chars');
            let content = $('.message-container');

            let ai_title = $("div[name='ai_title']").clone();
            content.append(ai_title.get(0));

            let ai_msg = $("p[name='ai_msg']").clone();
            ai_msg.text(response);
            ai_msg.addClass("dialogue");
            content.append(ai_msg.get(0));
        },
    })
}

function init() {
    $('.send-button').click(function(){
        async_call();
    });

    $("input[name='message']").keydown(function(e){
        if(e.keyCode == 13) {
            async_call();
            return false;
        }
    });
}

$(document).ready(function () {
    init();
})