h_system_prompt = """
Your task is to extend a short opinion into a well-organized key factor for ethical dilemmas.
Input:
    - An ethical dilemma description
    - A human's opinion on the dilemma
Output:
Organize and extend the human's opinion.
Here is an example.

Ethical dilemma description:
I joined a lab during graduate school and was assigned to a post-doc, who immediately had me working
with him to synthesize a key compound for his project. We worked on the compound for a number of
months with him directing the effort. However, I was pleased with my own contributions and was
delighted to get positive feedback from him. Indeed, the overall experience I was having was very
positive, making me work even harder on the project.
That’s when things got interesting. Early one evening, when we felt we were very close to
success, I decided to stay a bit longer in the lab and try out some hunches. As I systematically tried out
each one and tested it to see if it was correct, I FINALLY GOT IT. I verified it over and over to make sure.
And I was overjoyed. I wrote it up, and left the lab in the wee hours of the morning elated but
exhausted.
So I didn’t get to the lab until late the next morning, but I wasn’t concerned because I knew my
senior partner would be gratified. What do I see, however, but him talking to the PI of the project and
taking credit for my discovery of the previous evening. I walked over and was astonished to hear him
saying to the PI, “I verified the compound this morning, so we’re on our way.” Apparently, he saw my
lab notes of the evening before, duplicated my test that morning, and now was taking credit for it as his
own!
When I got him in private, I was very upset and told him that the last, crucial step in the
experiment—the one I did the previous evening—was my idea and my work. He laughed in my face and
said that I was only tinkering around with some obvious strategies and that sooner or later one of us
would finalize it. In other words, he was entirely dismissing the importance of my work the night before
and arguing that the outcome was inevitable no matter which one of us did it. So, he was claiming the
work as largely his own because the project was his and he did most of the intellectual work.
How should a lab resolve this problem? In a situation like this, who should get credit and what
should the decisional process be?

Human answer:
I think we need to document the discovery in notes and clearly distinguish project oversight from the student’s experimental breakthrough. We should also fairly acknowledge the postdoc’s prior intellectual contributions.

Expected output:
The primary factors include the documentation of the discovery through lab notes, the hierarchical relationship between student and postdoc, the collaborative nature of the work, and the distinction between project oversight and actual discovery. The postdoc's prior intellectual contribution versus the student's crucial experimental breakthrough must also be weighed.
"""
h_user_prompt = """
Ethical dilemma description:
{}

Human answer:
{}

The output should be a paragraph. Make sure the output is in utf-8 format. Make sure the size of the output does not exceed three times the human answer.
"""