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

    const request_data = new FormData();
    request_data.append('original_text', original_text.val());
    request_data.append('target', target.val());
    request_data.append('csrfmiddlewaretoken', csrf.val());
    fetch("/translation_async/", {
        method: "POST",
        body: request_data,
    }).then(response => response.json()).then((response) => {
        translated_text.val(response.result);
        $("div[name='spinner").hide();
        translated_text.show();
    });
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