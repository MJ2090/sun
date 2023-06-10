function process_side_channel(side_channel) {
    if (side_channel.suicidal == true) {
        let suicidal_label = document.querySelector("span[name='badge_suicide']");
        suicidal_label.innerHTML = side_channel.suicidal_label;
        show(suicidal_label);
    }
}