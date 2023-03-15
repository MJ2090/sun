function welcome() {
    let labels = ['Enjoy', '欢迎使用', 'Bonne lecture', '楽しむ', '즐기기', '歡迎使用', 'насолоджуватися', 'disfrute de', 'genießen Sie']
    let index = 1;
    let total = labels.length;

    var check1 = function () {
        $("p[name='enjoy_label']").animate({ opacity: 0 }, 1000);
        setTimeout(check2, 1000);
    }

    var check2 = function () {
        $("p[name='enjoy_label']").text(labels[index]);
        index += 1;
        if (index == total) {
            index = 0;
        }
        $("p[name='enjoy_label']").animate({ opacity: 1 }, 1000);
        setTimeout(check1, 3000);
    }

    setTimeout(check1, 2000);
}

function setup_hover() {
    let wait_time = 400;
    $("div[name='feature_chat']").hover(function () { $("p[name='p_feature_chat']").fadeIn(wait_time) }, function () { $("p[name='p_feature_chat']").hide() });
    $("div[name='feature_embedding']").hover(function () { $("p[name='p_feature_embedding']").fadeIn(wait_time) }, function () { $("p[name='p_feature_embedding']").hide() });
    $("div[name='feature_image']").hover(function () { $("p[name='p_feature_image']").fadeIn(wait_time) }, function () { $("p[name='p_feature_image']").hide() });
    $("div[name='feature_translation']").hover(function () { $("p[name='p_feature_translation']").fadeIn(wait_time) }, function () { $("p[name='p_feature_translation']").hide() });
    $("div[name='feature_summary']").hover(function () { $("p[name='p_feature_summary']").fadeIn(wait_time) }, function () { $("p[name='p_feature_summary']").hide() });
    $("div[name='feature_grammar']").hover(function () { $("p[name='p_feature_grammar']").fadeIn(wait_time) }, function () { $("p[name='p_feature_grammar']").hide() });
}

function init() {
    welcome();
    setup_hover();
}

$(document).ready(function () {
    init();
})