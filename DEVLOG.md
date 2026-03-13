## Entry 1 Project Outline
*11th March 2026*

Before writing any code, it is important I lay out exactly what I am trying to achieve, how I aim to achieve it and any thoughts I have on the direction I can take this. Also it is important to address I will be using Claude to help me build this project, so I will also be including how and where I have used AI as a tool.

### The Problem
I want to build a website that tests my mental maths abilities and improves them by analysing patterns in my mistakes. To me, being good at mental maths means being able to complete calculations both quickly and accurately, so response time and accuraccy will be vital components this project is built around.

### Core Features
The website will generate questions using the basic operations: addition, subtraction, multiplication and division, as well as percentages and fractions. For each question and answer, data will be stored into a CSV file which I can export and analyse in Python

### What Data I Will Record and Why
I aim to use the data to find patterns in my mathematical ability, to then feed this back into the website to help me improve, so choosing the right data to collect from the beginning is very important.

| Field | Type | Reason |
|---|---|---|
|`date`|DATE|To track improvement over time|
|`session_id`|STRING|To see development over a session, and fatigue|
|`operator`|STRING| To understand what operation I struggle with|
|`number_1`,`number_2`|FLOAT| To see if theres specific numbers that cause issues|
|`correct_answer`|FLOAT|Used with `my_answer` to measure accuracy and error type|
|`my_answer`|FLOAT|Above|
|`is_correct`|BOOL|Accuracy Measure|
|`response_time_ms`|INT|Speed combined with accuracy reflects ability, and allows us to explore nature of wrong answers|
|`difficulty_level`|INT|To track performance changes across levels|

### How the Website Will Work
There will be two game modes involved:

**Test Mode:** A level-based system where the user must answer a set number of random questions in a time limit to beat the level. As levels progress these random questions will increase in difficulty, with larger more complicated numbers or perhaps decimals. 

**Practice Mode:** This mode allows you to choose which type of questions to practice, allowing customisation to number ranges and operations. In this section there will be key data insights that showcase areas I am weaker in, and recommends practice in those specififc areas. This step is key as the website will be helping me to identify my weaknesses and improve on them.

### Level-based System
Whilst it is clear increasing the difficulty of the questions is key, deciding how to approach this is tricky.

**Option 1 - Preset Levels** Questions are grouped into levels of increasing difficulty. To progress past a level, I must correctly answer x questions in y time without getting more than z questions wrong. The data this produces is clean and easy to group, as questions will already be banded into a difficulty level.

**Option 2 - Elo Rating System** Like in chess, an Elo system gives a rating to me that is assosciated to my ability. Whereby, if I calculate a difficult sum correctly, it increases more than if it was a simple sum, and if I were to get a question wrong, it decreases. Then the website will base questions on Elo rating, so that you are constantly being pushed. 

I will choose the Preset Level based system for two reasons. Firstly, the data structure it produces will be simpler and more straighforward to work with in pandas, and analysis of this data is key component of the project. Secondly, the level based system feels like a prerequisite for the Elo system, so makes more sense to approach first.

I think the Elo is a more elegant solution that I look forward to tackling, and can potentially incorporate it as a third function to the website.

### Data Insights
Some questions I might want to explore using my answers data:

Which operator am I weakest/strongest at?
Which operator am I slowest at?
How does my performance change over a session?
How has my performance changed since starting?
Are there specific numbers I struggle with?


### Considerations and Potential Issues
**Operation diffculty:** Addition is easier than multiplication, for example, 16 + 51 is trivial, whereas 16 * 51 proves to be harder. For each operation, a different set of numbers will have to be used on the same levels.

**Deciding difficulty of a question:** Determing what makes a question a medium level compared to hard can be challenging. Perhaps research and test results found online can provide me on insight on how to determine the difficulty brackets. 

**Data Bias:** I am the only data provider, so deciding if I need to improve a skill or whether those questions are too hard for a level is challenging. Lets say on the medium level, I keep scoring badly on division questions, is this due to a weakness in that area, or do I need to reconfigure the questions. 

## Entry 2 Project Planning
*12th March 2026*

Now I have laid out what I want to achieve, I have to plan how I am going to get there. I finished last entry with some initial considerations and issues I have to iron out. Here are my first plans to do so:

**Operation difficulty:** Not all operations are equal in difficulty. Adding two numbers is mostly easier than multiplying them, so a level system that ignores this won't reflect the users ability, rather the difference in operation. To account for this, each operation will have its own number ranges per level, chosen so that each question is similar in difficulty, regardless of the operator.

**Deciding these sets** Deciding exactly which numbers belong at each level is not straightforward, combined with the fact I will be the only user to provide data. If I consistently struggle with level 3 multiplication, does this tell us I need to improve my multiplication or are the questions simply too hard for that level.

To solve this I will take a 2 stage approach. First, I will define an initial set of numbers for each operation and level, with the help of three sources: patterns I find on other mental maths websites, my own intuition, and siggestions from Claude since an AI model will be drawing from a much larger data set then I could create. 

Then using these initial sets embedded in my website, I will answer questions and begin creating data to explore. Once I have enough, I will analyse it in Python to look for any strong patterns, whether its accuracy or answer time, and from my findings can adjust levels appropriately. After this calibration stage I will finalise the sets and from that point treat the data as a reliable record of performance to explore.

**Development Stage** After initial development of the number sets, I quickly realised this is a feature I will have to continuously tinker in the beginning, so would involve lots of edits and etracting data from the website to python to analyse. So I have decided to change the order of the project. I will build the program in Python first to allow me to easily modify and test my ranges. Once this is finalised, I can then base the website off my local python project. This is exactly why the planning process is key to a successful project, detecting issues before they arise.

## Entry 3 Number Ranges

### Claude usage
After researching and experimenting with number ranges, I settled on a starting point I was happy with, storing in an Excel spreadsheet with one table per operation. I then asked Claude to translate these into a Python dictionary stored in a seperate file, meaning I can adjust ranges without touching the main quiz code. 

Division would require special care since you can't divide two numbers and hope to get a whole number as an answer. I was aware of this constraint and planned to deal with it later, but Claude identified this difficulty and structured division around a result range and divisor range. After reviewing this approach I decided to keep this format as it would ensure only valid division questions are generated.

## Entry 4 Quiz Logic Spec
*12th March 2026**

**Session Structure:** Each session, I have a minute to answer as many questions as I can correctly. When I answer a question, my input is stored and a new question is generated. This process continues until the timer runs out at whioch point the user is shown their score out of total attempted questions.

**Data Storage:** Data will be stored into two seperate CSV files, one that is question specific and another that is a session overview. The files will share `session_id` so can be combined later.

We have discussed the format of the question csv file previously, but for the session csv we will extract the following: 
| Field | Type |
|---|---|
|`date`|DATE|
|`session_id`|STRING|
|`level`|INT|
|`total_questions`|FLOAT|
|`correct`|INT|
|`score_percent`|FLOAT|
|`operator_focus`|STRING|

`session_id` will be a generated from a timestamp at the start of each session, formatted as `YYYY-MM-DD-HHMMSS`

### Considerations

The last question presented just before the timer runs out doesn't provide us with useful data, as I will not be able to give an answer, so this doesn't need to be included when collecting the data.

### Question Generator

With this spec finalised, I asked Claud to write a `generate_question` function taking two inputs: a level integer and an operator string, returning a dictionary containing question and answer.

Claude produced a working first version, but testing revealed two issues. Firstly, division questions were occasionally producing decimal numbers within the question itself which was caused by odd numbers being paired with .5 values. I fixed this with a constraint so only even numbers are paired with .5s. Secondly, level 5 decimal questions were multiplying two decimal numbers together, which I hadn't intended. I corrected this simply so that only one of the numbers could be decimal.

### CSV Writers
Before I create the quiz loop, I need a function that will record my answers and append them to a CSV file for analysis.

I need two functions, a write_question(row) which appends a single question's data to questions.csv, and write_session(summary) which appends a session summary to sessions.csv. Both take a dictionary as input containing the data points I am interested in and have specified.

These functions need an additional attribute, if these functions are being called without the CSV file existing, then they will create this file themselves. This decision means the code can be shared to different users without having to create their own files.

Using this spec as a prompt, combined with the explicit data points, Claud built these functions. The code was simple and also recommend I add the CSV files to .gitignore so that they are generated data rather than project code. The os.path.isfile() handles the case when the files don't exist and created them with the correct headers automattically. In the case when a question is generated just before the timer runs out, I want to exclude this from the CSV file but can handle this in the quiz loop rather than complicating the CSV writers.

## Entry 4 

*March 13th 2026*

### Quiz loop

With all the individual functions coded, I am now going to create the quiz that ties everything together and can then begin generating data. The process will operate in the following order:

**Initiation** The user is asked what level they want to play, then a session ID is generated and a 3 second timer starts before the questions begin.

**During the Quiz** A 120 second timer will begin, and the user must answer as many questions as they can correctlty in that time. A new question is generated each time the last one has been answered, the user will not be told which ones they have answered correctly until the end. I want to ensure each operation is randomly chosen but with the condition that no two consecutive questions can use the same operator. The quiz will format the questions 12 = 7 = ? and only numeric inputs are accepted. Also before the users answer is corrected, the answer and their answer is rounded to 2.dp to avoid float comparison issues. Each answered question is written immediately to questions.csv. If the timer expires mid-answer, that question is discarded and the session ends.

**End** Once the timer runs out, the session data is stored into the csv file and the user is showed their score as well as a list of questions they answered incorrectly with my answer and the correct answer. They are then given the option to play again, which generates a new session ID and restarts, or exit.











