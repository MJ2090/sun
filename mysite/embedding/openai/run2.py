import df
import robot


################################################################################
### Step 13
################################################################################
def run_it_2():
    my_text = """
        ADHD: A four-letter acronym that stands for attention-deficit/hyperactivity disorder. Across our society and throughout modern history, it has also come to represent harmful stereotypes, debilitating assumptions, and unconscious bias.

    Our mission is to empower everyone living with ADHD to reach their fullest potential. We meet that mission by providing a patient-first, technology-powered ADHD treatment platform that keeps costs down and reduces patient wait times.

    Unchecked and untreated, ADHD can hamper brain development and impede everything from a person’s social skills to their productivity in a professional environment. While the condition itself is considered very common, with more than 3 million cases now diagnosed annually in the U.S. alone, the treatment opportunities for ADHD are anything but common. Most people suffer in silence.

    We are facing a challenge when it comes to providing psychiatric care, physician burnout, an aging workforce, bureaucratic and insurance demands, and poor compensation. In fact, it’s a simple math equation. In total, more than 20 million people in the U.S. have received a diagnosis of ADHD. But there are fewer than 30,000 psychiatrists to treat them. That means there are roughly 667 patients per psychiatrist. Clearly, unsustainable.

    Beyond addressing the emotional and mental wellness of patients we also see an opportunity to address the financial impact of $150-200 million in lost productivity every year due to ADHD. In addition, no one should lose their job over ADHD, and no one should lose their opportunity to find a meaningful path forward in their professional life as well as their personal one.

    Clearly, the time is now to change the course of this treatable condition. The solution?

    At Done., first we want to eliminate the stigma and confusion or isolation around ADHD and empower anyone to receive the help they need to live up to their fullest potential. We provide awareness and education for people to learn more, confidential and accurate medical diagnosis through telehealth, and actionable ways to receive immediate treatment.

    We’ve also hired some of the most esteemed and board-certified experts in the industry to collaborate and tackle ADHD together. Their wisdom and experience has allowed us to build a robust online platform that infuses efficiency with effectiveness. We put the patient’s needs first and seek to provide a stable scaffolding during their entire journey with us.

    Done. is dedicated to serving individuals who otherwise may not be comfortable seeking care for ADHD in person due to stigma around ADHD treatment or may not be able to access care due to cost or availability.   By providing a platform that deals directly with patients and manages the logistics and administrative work around their care, Done. allows providers to spend more time focusing on what they do best – evaluating and treating patients.

    Indeed, we believe that technology is a vital part of the solution to connect anyone to the right psychiatric care at the right time - even through their mobile device. This “always-on” strategy allows for seamless accessibility, convenient interactions like video calls, and 24/7 support. Our patients are the lifeblood of Done. and we know that the overwhelming nature of ADHD can strike at any moment.

    There is also a shared responsibility between the patient, the medical practitioner, and Done. to ensure everyone receives responsible and quality treatment in such a timely manner. That treatment can include therapy, medication, or a combination of options depending on the circumstances.

    Done. does not generate the diagnosis. Rather Done. serves as the ultimate conduit between ailment and treatment; Done.’s clinical operations are managed by an independent professional corporation (PC) headed by board-certified psychiatrists and psychiatric mental health nurse practitioners.

    Our approach is simple:

    1. Visit donefirst.com to take a medically approved assessment test and learn where a patient falls in the spectrum of ADHD (80% of adults with ADHD are not even aware).

    2. Schedule an appointment directly with a medical practitioner and for a patient to discuss their wellness in private.

    3. Once treatment is determined, a patient has the option to join Done. as a valued member of our services and access a broad network of clinicians.

    Of course we do not suggest that our approach is perfect. No medical system in the world functions without difficulties and hurdles along the way. But we know it’s working.
        """

    my_texts = [("ss", my_text)]

    my_df = df.get_df(my_texts)
    qs = ["What day is it?",
          "What is Done?",
          "What is ADHD?",
          "How to treat ADHD?",
          "How many people have ADHD?",
          "Where are you",
          "How do patients like Done.?"]
    for q in qs:
        print("Question:")
        print(q)
        print("Answer:")
        print(robot.answer_question(my_df, question=q))
        print("=======================\n\n\n")

run_it_2()