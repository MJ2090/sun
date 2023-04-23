function summary_async_call() {
    let original_text = $("textarea[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let summary_text = $("textarea[name='summary_text']");
    summary_text.val('');
    summary_text.hide();
    $("div[name='spinner").show();

    const request_data = new FormData();
    request_data.append('original_text', original_text.val());
    request_data.append('csrfmiddlewaretoken', csrf.val());
    fetch("/summary_async/", {
        method: "POST",
        body: request_data,
    }).then(response => response.json()).then((response) => {
        summary_text.val(response.result);
        $("div[name='spinner").hide();
        summary_text.show();
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