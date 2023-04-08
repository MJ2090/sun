function grammar_async_call() {
    let original_text = $("textarea[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let fixed_text = $("textarea[name='fixed_text']");
    fixed_text.val('');
    fixed_text.hide();
    $("div[name='spinner").show();
    $.ajax({
        type: 'POST',
        url: "/grammar_async/",
        data: {
            original_text: original_text.val(),
            csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            let data = JSON.parse(response);
            fixed_text.val(data.plain_result);
            $("div[name='spinner").hide();
            fixed_text.show();
        },
    })
}

function grammar_init() {
    let timer;
    $("textarea[name='text']").keyup(function () {
        clearTimeout(timer);
        timer = setTimeout(() => { grammar_async_call(); }, 800);
    });
}

$(document).ready(function () {
    grammar_init();
})