function async_call() {
    let original_text = $("textarea[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let translated_text = $("textarea[name='translated_text']");
    translated_text.val('');
    translated_text.hide();
    $("div[name='spinner").show();
    $.ajax({
        type: 'POST',
        url: "/translation_async/",
        data: {
            original_text: original_text.val(),
            csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            translated_text.val(response);
            $("div[name='spinner").hide();
            translated_text.show();
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