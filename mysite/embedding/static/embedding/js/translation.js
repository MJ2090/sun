function translation_async_call() {
    let original_text = $("textarea[name='text']");
    if (original_text.val().trim() == "") {
        return;
    }
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let translated_text = $("textarea[name='translated_text']");
    let target = $("select[name='target']");
    translated_text.val('');
    translated_text.hide();
    $("div[name='spinner").show();
    $.ajax({
        type: 'POST',
        url: "/translation_async/",
        data: {
            original_text: original_text.val(),
            csrfmiddlewaretoken: csrf.val(),
            target: target.val(),
        },
        success: function (response) {
            translated_text.val(response);
            $("div[name='spinner").hide();
            translated_text.show();
        },
    })
}

function translation_init() {
    let timer;
    $("textarea[name='text']").keyup(function () {
        clearTimeout(timer);
        timer = setTimeout(() => { translation_async_call(); }, 800);
    });
    $("select[name='target']").change(function () {
        clearTimeout(timer);
        timer = setTimeout(() => { translation_async_call(); }, 800);
    });
}

$(document).ready(function () {
    translation_init();
})