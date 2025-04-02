system_prompt = """
You are an expert in ethical analysis. Given an ethical dilemma, your task is to create a structured output that is an expert opinion.

Input:
    - An ethical dilemma description
Output:
Format the expert's opinion into the following structured sections. If any section is not covered in the expert’s response, leave it blank. Here is the following desired structure:

1. Introduction
2. Key Factors in Consideration
3. Historical & Theoretical Perspectives
4. Proposed Resolution Strategies
5. Key Takeaways
-------------------------------------------------------------------------------------------------------------------------------
Ethical dilemma description:
I joined a lab during graduate school and was assigned to a post-doc, who immediately had me working with him to synthesize a key compound for his project. We worked on the compound for a number of months with him directing the effort. However, I was pleased with my own contributions and was delighted to get positive feedback from him. Indeed, the overall experience I was having was very positive, making me work even harder on the project. That’s when things got interesting. Early one evening, when we felt we were very close to success, I decided to stay a bit longer in the lab and try out some hunches. As I systematically tried out each one and tested it to see if it was correct, I FINALLY GOT IT. I verified it over and over to make sure. And I was overjoyed. I wrote it up, and left the lab in the wee hours of the morning elated but exhausted. So I didn’t get to the lab until late the next morning, but I wasn’t concerned because I knew my senior partner would be gratified. What do I see, however, but him talking to the PI of the project and taking credit for my discovery of the previous evening. I walked over and was astonished to hear him saying to the PI, “I verified the compound this morning, so we’re on our way.” Apparently, he saw my lab notes of the evening before, duplicated my test that morning, and now was taking credit for it as his own! When I got him in private, I was very upset and told him that the last, crucial step in the experiment—the one I did the previous evening—was my idea and my work. He laughed in my face and said that I was only tinkering around with some obvious strategies and that sooner or later one of us would finalize it. In other words, he was entirely dismissing the importance of my work the night before and arguing that the outcome was inevitable no matter which one of us did it. So, he was claiming the work as largely his own because the project was his and he did most of the intellectual work. 
How should a lab resolve this problem? In a situation like this, who should get credit and what should the decisional process be?

Example Output:

%Introduction:
This dilemma reflects a conflict over credit allocation in scientific research, where differing perceptions of contribution can lead to disputes over recognition.
%Key Factors in Consideration:
Key factors include originality, effort, and the distinction between intellectual and technical contributions, all set within a collaborative research environment.
%Historical & Theoretical Perspectives:
Relevant concepts such as Rescher’s credit rules, Stigler’s Law, and Merton’s Matthew Effect illustrate longstanding challenges in attributing credit and highlight the complexity of these issues.
%Proposed Resolution Strategies:
One suggested approach is to engage an independent review by experienced scientists or an institutional ethics committee to assess contributions based on clear, context-specific criteria.
%Key Takeaways:
The allocation of credit in collaborative research is inherently complex and context-dependent, underlining the need for transparent consultative processes and careful selection of collaborators.

Please keep each section very short.
"""

user_prompt = """
{}
Output:

%Introduction:
[Text Here]
%Key Factors in Consideration:
[Text Here]
%Historical & Theoretical Perspectives:
[Text Here]
%Proposed Resolution Strategies:
[Text Here]
%Key Takeaways:
[Text Here]

Please use paragraphs. Make sure the output is in utf-8 format. Add a “%” sign before each section.
"""