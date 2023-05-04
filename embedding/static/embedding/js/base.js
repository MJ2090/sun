function base_init() {
    if ($(".mobile-only").css("display") == 'none') {
        $(".mobile-only").remove();
    }
    if ($(".desktop-only").css("display") == 'none') {
        $(".desktop-only").remove();
    }
}

$(document).ready(function () {
    base_init();
})