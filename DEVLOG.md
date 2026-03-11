## Entry 1 Project Planning
*11th March 2026*

Before writing any code, it is important I lay out exactly what I am trying to achieve, how I aim to achieve it and any thoughts I have on the direction I can take this. 

### The Problem
I want to build a website that tests my mental maths abilities and improve them by analysing patterns in my mistakes. To me, being good at mental maths means being able to complete calculations both quickly and accurately, so response time and accuraccy will be vital components this project is built around.

### Core Features
The website will generate questions using the basic operations: addition, subtraction, multiplication and division, as well as percentages and fractions. For each question and answer, data will be stored into a CSV file which I can export and analyse in Python

### What Data I Will Record and Why
I aim to use the data to find patterns in my mathematical ability, to then feed this back into the website to help me improve, so choosing the right data to collect from the beginning is very important.

| Field | Type | Reason |
|---|---|---|
|`date`|DATE|To track improvement over time|
|`session_id`|STRING|To see development over a session, and fatigue|
|`operator`|STRING| To understand what operation I struggle with|
|`number_1`,`number_2`|INT| To see if theres specific numbers that cause issues|
|`correct_answer`|FLOAT|Used with `my_answer` to measure accuracy and error type|
|`my_answer`|FLOAT|Above|
|`is_correct`|BOOL|Accuracy Measure|
|`response_time_ms`|INT|Speed combined with accuracy reflects ability, and allows us to explore nature of wrong answers|
|difficulty_level|INT|To track performance changes across levels|




