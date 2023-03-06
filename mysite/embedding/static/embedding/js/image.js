function async_call() {
    let original_text = $("textarea[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let generated_img = $("img[name='generated_img']");
    let style = $("select[name='style']");
    generated_img.hide();
    generated_img.attr('src', '');
    $("div[name='spinner").show();
    $.ajax({
        type: 'POST',
        url: "/image_async/",
        data: {
            original_text: original_text.val(),
            style: style.val(),
            csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            $("div[name='spinner").hide();
            generated_img.attr('src', response);
            generated_img.show();
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