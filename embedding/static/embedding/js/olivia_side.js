function process_side_channel(side_channel) {
    if (side_channel.suicide == true) {
        let suicide_label = document.querySelector("span[name='badge_suicide']");
        show(suicide_label);
    }
}