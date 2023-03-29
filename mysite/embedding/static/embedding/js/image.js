function async_call() {
    let original_text = $("input[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let generated_img = $("img[name='generated_img']");
    let style = $("select[name='style']");
    let count = $("select[name='count']");
    let image_container = $("div[name='image_container']");
    $("div[name='spinner']").show();
    $.ajax({
        type: 'POST',
        url: "/image_async/",
        data: {
            original_text: original_text.val(),
            style: style.val(),
            csrfmiddlewaretoken: csrf.val(),
            count: count.val(),
        },
        success: function (response) {
            $("div[name='spinner']").hide();
            let data = JSON.parse(response);
            for (let i = 0; i < data.urls.length; i++) {
                let cloned = generated_img.clone();
                cloned.attr('src', data.urls[i].url);
                cloned.attr('name', 'temp');
                image_container.prepend(cloned);
            }

            setTimeout(showImage, 1000);
        },
    })
}

function showImage() {
    $("img[name='temp']").animate({
        opacity: 0.85,
    }, 400);
    $("img[name='temp']").attr('name', '');
}

function init() {
    $('.send-button').click(function () {
        async_call();
        return false;
    });

    $("input[name='text']").keydown(function (e) {
        if (e.keyCode == 13) {
            async_call();
            return false;
        }
    });
}

$(document).ready(function () {
    init();
})