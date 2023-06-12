function process_side_channel(side_channel) {
    if (side_channel.therapy_assessment == true) {
        let therapy_assessment_label = document.querySelector("span[name='badge_therapy_assessment']");
        therapy_assessment_label.innerHTML = side_channel.therapy_assessment_label;
        show(therapy_assessment_label);
    }
}