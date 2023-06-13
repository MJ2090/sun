function process_side_channel(side_channel) {
    if (side_channel.therapy_assessment == true) {
        let label = side_channel.therapy_assessment_label
        if (label == 'None') {
            let green_badge = document.querySelector("span[name='badge_green_assessment']");
            green_badge.innerHTML = 'Good so far';
            show(green_badge);
        }
        if (label == 'Depression' || label == 'Anxiety' || label == 'Insomnia' || label == 'Angry') {
            let green_badge = document.querySelector("span[name='badge_green_assessment']");
            hide(green_badge)
            let yellow_badge = document.querySelector("span[name='badge_yellow_assessment']");
            yellow_badge.innerHTML = side_channel.therapy_assessment_label;
            show(yellow_badge);
        }
        if (label == 'Suicide') {
            let green_badge = document.querySelector("span[name='badge_green_assessment']");
            hide(green_badge)
            let red_badge = document.querySelector("span[name='badge_red_assessment']");
            red_badge.innerHTML = side_channel.therapy_assessment_label;
            show(red_badge);
        }
    }

    if (side_channel.action == 'PHQ-9') {
        provide_assessment('PHQ-9');
    }
}

function provide_assessment(disorder_name) {
    if (disorder_name == 'Depression') {
    }
}