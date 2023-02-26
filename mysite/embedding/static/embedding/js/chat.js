function init() {
    $('.send-button').click(function(){
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
                textarea.append(response);
                textarea.prop( "disabled", false );
                textarea.focus();
            },
        })
    });
}

$(document).ready(function () {
    init();
})