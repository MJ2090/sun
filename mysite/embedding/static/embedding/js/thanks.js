function init() {
    let total = 5;
    setInterval(function() {
        total -= 1;
        if (total == 0) {
            window.location.replace('/');
        }
        $("span[name='tick']").text(total);
    }, 1000);
}

$(document).ready(function () {
    init();
})