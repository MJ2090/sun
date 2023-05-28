async function stream_async_call() {
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

    const response = await fetch("/stream_async/", {
        method: "POST",
        body: request_data,
    });

    if (!response.body) return;
    const reader = response.body
        .pipeThrough(new TextDecoderStream())
        .getReader();
    while (true) {
        var { value, done } = await reader.read();
        $("div[name='spinner").hide();
        translated_text.show();
        if (!value) {
            break;
        }
        translated_text.val(translated_text.val() + value);
    }

    // Play with GET:
    // var source = new EventSource("/stream_async");
    // source.onmessage = function (event) {
    //     translated_text.show();
    //     $("div[name='spinner").hide();
    //     console.log(event.data);
    //     if (event.data == 'DONE') {
    //         source.close();
    //     } else {
    //         translated_text.val(translated_text.val() + event.data);
    //     }
    // };
}

function stream_init() {
    let timer;
    $("textarea[name='text']").keyup(function () {
        clearTimeout(timer);
        timer = setTimeout(() => { stream_async_call(); }, 800);
    });
    $("select[name='target']").change(function () {
        clearTimeout(timer);
        timer = setTimeout(() => { stream_async_call(); }, 800);
    });
}

$(document).ready(function () {
    stream_init();
})