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
            show_diagnose_msg(label);
        }
        if (label == 'Suicide') {
            let green_badge = document.querySelector("span[name='badge_green_assessment']");
            hide(green_badge)
            let red_badge = document.querySelector("span[name='badge_red_assessment']");
            red_badge.innerHTML = side_channel.therapy_assessment_label;
            show(red_badge);
        }
    }
}

function show_diagnose_msg(label) {
    if (label == 'Depression') {
        display_msg('And, it looks like you may be suffering from Depression, should we start a session about that?');
        display_msg('We can get started by filling the PHQ-9 Questionnaire.');
        let buttons = document.querySelector("div[name='depression_buttons']");
        display_element(buttons);
        document.querySelector("textarea").setAttribute('disabled', true);
    }
}

function provide_assessment(disorder_name) {
    if (disorder_name == 'Depression') {
    }
}