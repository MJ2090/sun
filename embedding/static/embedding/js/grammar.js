function grammar_fetch() {
    let original_text = $("textarea[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let fixed_text = $("textarea[name='fixed_text']");
    fixed_text.val('');
    fixed_text.hide();
    $("div[name='spinner']").show();

    const request_data = new FormData();
    request_data.append('original_text', original_text.val());
    request_data.append('csrfmiddlewaretoken', csrf.val());
    fetch("/grammar_async/", {
        method: "POST",
        body: request_data,
    }).then(response => response.json()).then((response) => {
        let data = response;
        fixed_text.val(data.plain_result);
        $("div[name='spinner']").hide();
        fixed_text.show();
    });
}

function grammar_init() {
    let timer;
    $("textarea[name='text']").keyup(function () {
        clearTimeout(timer);
        timer = setTimeout(() => { grammar_fetch(); }, 800);
    });
}

$(document).ready(function () {
    grammar_init();
})