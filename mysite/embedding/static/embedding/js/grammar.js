function async_call() {
    let original_text = $("textarea[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let fixed_text = $("textarea[name='fixed_text']");
    fixed_text.val('');
    fixed_text.hide();
    $("div[name='spinner").show();
    $.ajax({
        type: 'POST',
        url: "/send_grammar/",
        data: {
            original_text: original_text.val(),
            csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            fixed_text.val(response);
            $("div[name='spinner").hide();
            fixed_text.show();
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