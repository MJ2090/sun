function async_call() {
    let textarea = $("textarea[name='message']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    textarea.prop( "disabled", true );
    $.ajax({
        type: 'POST',
        url: "/sendchat/",
        data: {message: textarea.val(),
                csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            textarea.val( response);
            textarea.prop( "disabled", false );
            textarea.focus();
            $('.word-count').text(response.length + ' chars');
        },
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