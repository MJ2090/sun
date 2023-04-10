function summary_async_call() {
    let original_text = $("textarea[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let summary_text = $("textarea[name='summary_text']");
    summary_text.val('');
    summary_text.hide();
    $("div[name='spinner").show();
    $.ajax({
        type: 'POST',
        url: "/summary_async/",
        data: {
            original_text: original_text.val(),
            csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            summary_text.val(response);
            $("div[name='spinner").hide();
            summary_text.show();
        },
    })
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