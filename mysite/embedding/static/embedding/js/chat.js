function async_call() {
    let textarea = $("textarea[name='message']");
    let password = $("input[name='password']");
    let character = $("select[name='character']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    textarea.prop( "disabled", true );
    character.prop( "disabled", true );
    $.ajax({
        type: 'POST',
        url: "/sendchat/",
        data: {password: password.val(),
            message: textarea.val(),
            character: character.val(),
            csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            textarea.val( response);
            textarea.prop( "disabled", false );
            textarea.focus();
            $('.word-count').text(response.length + ' chars');
        },
        error: function (response) {
            textarea.prop( "disabled", false );
        }
    })
}

function init() {
    $('.send-button').click(function(){
        async_call();
    });

    $("textarea[name='message']").keydown(function(e){
        if(e.keyCode == 13) {
            async_call();
        }
    });
}

$(document).ready(function () {
    init();
})