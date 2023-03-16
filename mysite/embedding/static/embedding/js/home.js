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


function hover1() {
    let desc_dict = {
        feature_chat: 'Chat and have fun with human-like AI',
        feature_embedding: 'Q&A Machine answers questions baesd on your documents',
        feature_image: 'Meet Piccaso and Monet here, generating master pieces based on pure text description',
        feature_translation: 'Have your text translated by AI',
        feature_summary: 'Generate simple summary that is easy to understand',
        feature_grammar: 'Fix any grammar & spelling in seconds'
    };
    let name = this.getAttribute("name");
    let desc = desc_dict[name];
    $("p[name='p_feature_more']").text(desc);
}
function hover2() {
    $("p[name='p_feature_more']").text('More are on the way');
}

function setup_hover() {
    $("div[name='feature_chat']").hover(hover1, hover2);
    $("div[name='feature_embedding']").hover(hover1, hover2);
    $("div[name='feature_image']").hover(hover1, hover2);
    $("div[name='feature_translation']").hover(hover1, hover2);
    $("div[name='feature_summary']").hover(hover1, hover2);
    $("div[name='feature_grammar']").hover(hover1, hover2);
}

function home_init() {
    welcome();
    setup_hover();
}

$(document).ready(function () {
    home_init();
})