function setFocus(el) {
    el.focus();
    el.click();
}

function fadeIn(element) {
    element.classList.add('fade-in');
}

function fadeOut(element) {
    element.classList.add('fade-out');
}

function hide(element) {
    element.classList.add('hidden');
}

function show(element) {
    element.classList.remove('hidden');
}

function isShown(element) {
    return !element.classList.contains('hidden');
}

function toggle_spinner(show) {
    if (show) {
        document.querySelector("div[name='spinner']").classList.remove("invisible");
    } else {
        document.querySelector("div[name='spinner']").classList.add("invisible");
    }
}