function summary_async_call() {
    let original_text = $("textarea[name='text']");
    let prompt = $("textarea[name='prompt']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let result_text = $("textarea[name='result_text']");
    result_text.val('');
    result_text.hide();
    $("div[name='spinner").show();

    const request_data = new FormData();
    request_data.append('original_text', original_text.val());
    request_data.append('prompt', prompt.val());
    request_data.append('csrfmiddlewaretoken', csrf.val());
    fetch("/demo_async/", {
        method: "POST",
        body: request_data,
    }).then(response => response.json()).then((response) => {
        result_text.val(response.result);
        $("div[name='spinner").hide();
        result_text.show();
    });
}

function summary_init() {
    let timer;
    $("textarea[name='text']").keyup(function () {
        clearTimeout(timer);
        timer = setTimeout(() => { summary_async_call(); }, 800);
    });
}

$(document).ready(function () {
    summary_init();
})