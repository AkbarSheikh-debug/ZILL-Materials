# Lecture 4 — Context and Compaction (Teleprompter Script)

## How to read this script

Every step is numbered. In each step you will see these labels. They tell you **exactly what to do**:

| Label | What you do |
|---|---|
| 🖼 **SHOW** | Put this picture on the screen. |
| 🗣 **SAY** | Speak these lines to the camera. |
| 👉 **POINT** | While speaking, point at this part of the picture. |
| ❓ **ASK** | Ask the viewers this question. Then **stop talking for 3 seconds**. |
| ✅ **ANSWER** | Now give the answer yourself. |
| ⏸ **PAUSE** | Take a breath. A new topic starts. |

Pictures are in the folder `diagrams-lecture4/`. If you get lost, just look for the next step number.

---

# PART 1 — What goes into the context

---

### STEP 1

🖼 **SHOW** diagram-01

🗣 **SAY**
Alright everyone, welcome back to the Harness Engineering series. This is lecture four.

Before we start, open your Zill repo once. It should look like this picture.

👉 **POINT** at the five green boxes.

🗣 **SAY**
From lecture two, you have provider.py and loop.py. From lecture three, you have tools.py, security.py and operations.py. If you have these five files, you are on the right track. If not, please finish lecture three first, because today we build on top of it.

👉 **POINT** at the yellow box, context.py.

🗣 **SAY**
Today we add one new file, context.py. And honestly, I think today is the most important lecture of this whole series. Let me tell you why.

---

### STEP 2

🖼 **SHOW** diagram-02

👉 **POINT** at the left box.

🗣 **SAY**
When people learn about context, they usually learn what goes inside it. The system prompt, the tools, the memory, the conversation. This is called context engineering. It means filling the context properly. And most courses stop here.

👉 **POINT** at the right box.

🗣 **SAY**
But when you build a harness, the more important job is context management. Turn after turn, how does the harness keep this context under control? When does it compact? What does it keep? Where does it cut? And what if compaction fails?

Many people think compaction is just "summarize the old messages". It is not that simple. Today we will see how Pi does it, how Hermes does it, and how DeepSeek Harness does it. It is very detailed, and very beautiful. And at the end, we build our own compaction for Zill.

⏸ **PAUSE**

---

### STEP 3

🖼 **SHOW** diagram-03

🗣 **SAY**
Let's start simple. What is context?

In lecture one, we said a harness is like a car.

👉 **POINT** at the engine, then the wheels, then the fuel tank.

🗣 **SAY**
The LLM is the engine. The tools are the wheels. And the context is the fuel. And fuel has a limit. The tank has a size. You cannot keep pouring forever. So context is a budget. It is very precious.

---

### STEP 4

🖼 **SHOW** diagram-04

❓ **ASK**
"Remember the loop we built in lecture two. What arguments does it take? Pause the video and think."

*(stop for 3 seconds)*

✅ **ANSWER**
It takes the messages, and max turns. And it also gets the tools.

👉 **POINT** at the loop on the left, going round once.

🗣 **SAY**
We call the model. If it wants a tool, we run the tool. Then we append the result to the messages. And go round again. Every turn, something is added. Nothing is ever removed. And every call sends the whole thing again.

👉 **POINT** at the bars on the right, from small to big.

🗣 **SAY**
So turn one is maybe three thousand tokens. Then nine thousand. Then twenty-four thousand. And by turn thirty of a real task, we hit the ceiling. Nobody wrote a bug. The loop is doing exactly what we told it.

⏸ **PAUSE**

---

### STEP 5

🖼 **SHOW** diagram-05

❓ **ASK**
"What do you think goes into the context on every call? Pause and make your own list."

*(stop for 3 seconds)*

✅ **ANSWER** — go down the list, pointing at each row:

🗣 **SAY**
Number one, the system prompt. How the agent should behave.

Number two, the tools. With their full contract: name, label, description and parameters.

Number three, the skills. But only the name and a short description. Not the whole skill file. We'll see why soon.

Four, five and six. The user messages, the assistant messages, and the tool calls with their results. This is the messages array.

Number seven, memory files. Like AGENTS.md or CLAUDE.md, which you write for your project.

Number eight is optional. Hermes and OpenClaw decide by themselves what was important and save small memory notes to disk. Pi does not do this.

And number nine, the current folder and today's date.

👉 **POINT** at the yellow rows 4, 5, 6 and the bracket.

🗣 **SAY**
Now, out of these nine, which ones get compacted? Only these three. The messages array. Everything else is never touched.

---

### STEP 6

🖼 **SHOW** diagram-06

🗣 **SAY**
People often ask me: what's the difference between the system prompt and a user message?

👉 **POINT** at the purple box.

🗣 **SAY**
The system prompt tells the agent how to behave. Pi's system prompt starts with "You are an expert coding assistant operating inside pi". It's the same for every session.

👉 **POINT** at the blue box.

🗣 **SAY**
The user message is what you want right now. Like "migrate this code to Rust". It changes every session.

👉 **POINT** at the green box.

🗣 **SAY**
And the assistant message is what the model thinks and says, plus the tool calls it makes.

⏸ **PAUSE**

---

### STEP 7

🖼 **SHOW** diagram-07

🗣 **SAY**
Okay, that list was fine for a context engineering class. But we are doing harness engineering. So let's see what Pi actually does.

Pi builds its prompt with a function called buildSystemPrompt. It stacks five pieces.

👉 **POINT** at each box, from bottom to top.

🗣 **SAY**
One, the base template. "You are an expert coding assistant", plus the list of tools.

Two, appendSystemPrompt. Extra text you want to add.

Three, the project context. Every AGENTS.md or CLAUDE.md it finds. That's the memory part.

Four, the available skills. Only name, description and location. And this is added only if the read tool exists, because without it the model can't open a skill anyway.

Five, at the very end, the date and the working folder.

👉 **POINT** at the red bracket on the right.

🗣 **SAY**
All five become one string. And this string is rebuilt on every single call.

---

### STEP 8

🖼 **SHOW** diagram-08

👉 **POINT** at A, then B, then C.

🗣 **SAY**
So on Monday, you get one prompt. On Tuesday, same repo, only the date changes. And if you remove the read tool, the skills block disappears. The template stays the same, but the final prompt keeps changing.

⏸ **PAUSE**

---

### STEP 9

🖼 **SHOW** diagram-09

🗣 **SAY**
Now let's look closer at the project context. How does Pi find these memory files?

You might have one AGENTS.md for how you like to do all your projects. And inside one project, a CLAUDE.md just for that project.

👉 **POINT** at the purple box at the top left.

🗣 **SAY**
First, Pi loads the global file from its own folder. That goes in first.

👉 **POINT** at the blue arrows on the right, going up one by one.

🗣 **SAY**
Then it walks up. It starts at the folder you're working in. Then the parent. Then the parent of that. All the way to the top. In each folder, it looks for AGENTS.md or CLAUDE.md.

👉 **POINT** at the final order list on the right.

🗣 **SAY**
And the final order is: global first, then the furthest folder, and the closest file last. The closest file speaks last, so if two files disagree, the closest one wins. And Pi never loads the same file twice.

---

### STEP 10

🖼 **SHOW** diagram-10

❓ **ASK**
"Why do you think Pi does this walk again on every call, instead of just once?"

*(stop for 3 seconds)*

✅ **ANSWER**
Because you can edit the file in the middle of a session.

👉 **POINT** at the four boxes, left to right.

🗣 **SAY**
On turn four, the agent uses npm. You open CLAUDE.md and write "use pnpm". On turn five, the prompt is rebuilt, the walk finds your change, and now the agent uses pnpm.

👉 **POINT** at the two dashed boxes below.

🗣 **SAY**
Is there a limit on how many files? No. So don't keep too many in one project, or you'll confuse the model.

And remember, these files are Pi's only memory. You have to keep them updated yourself.

⏸ **PAUSE**

---

### STEP 11

🖼 **SHOW** diagram-11

🗣 **SAY**
Now, a very important topic. Skills. Many people are confused about skills, so let me make it simple.

👉 **POINT** at the yellow top part of the file.

🗣 **SAY**
A skill is one markdown file, SKILL.md. At the top it has a name and a description.

👉 **POINT** at the lines below the dashed line.

🗣 **SAY**
Below that is the body, the real instructions. It can be hundreds of lines.

Only the top part is in the context. The body loads only when the model picks this skill.

👉 **POINT** at the TRAILER box.

🗣 **SAY**
It's like a movie trailer. You see the trailer first. You watch the full movie only if you want. This is called progressive disclosure.

---

### STEP 12

🖼 **SHOW** diagram-12

👉 **POINT** at the three boxes, top to bottom.

🗣 **SAY**
Actually there are three levels. At the start, only the name and description, for every skill. When the skill is picked, the body. And extra files, like references or scripts, only if they are needed. So an extra file costs nothing until it is opened.

---

### STEP 13

🖼 **SHOW** diagram-13

❓ **ASK**
"So what's the difference between a tool and a skill?"

*(stop for 3 seconds)*

✅ **ANSWER**

👉 **POINT** at TOOL, then SKILL.

🗣 **SAY**
A tool is how to do one action. Read a file. Run bash. A skill is what to do, and when to do it. Like a recipe. A recipe can use many hands, but a hand never tells you the recipe.

---

### STEP 14

🖼 **SHOW** diagram-14

🗣 **SAY**
Let me show you a skill I made myself.

I had a writing agent, and everything it wrote looked AI-generated. Double dashes everywhere. Words like "delve" and "honestly".

👉 **POINT** at the books on the left, then the agent, then the file.

🗣 **SAY**
So I gave my agent a few chapters of my own book and asked it to make a skill. It made writing-style.md. A name, a description, and a long list of rules.

👉 **POINT** at the arrows on the right.

🗣 **SAY**
Now for any new book, blog post or page, I never explain my style again. The skill carries it.

And this is my philosophy. Keep the harness small. Put your effort into skills.

⏸ **PAUSE**

---

### STEP 15

🖼 **SHOW** diagram-15

🗣 **SAY**
So how do you write a good skill? These rules come from Anthropic's own guide.

Rule one. Say less.

👉 **POINT** at the short box on the left, then the long box on the right.

🗣 **SAY**
The model already knows what a PDF is. It knows React. It knows why Rust is fast. So don't explain these things. The good version is fifty tokens. The bad one is a hundred and fifty. Only write what the model does not already know.

---

### STEP 16

🖼 **SHOW** diagram-16

👉 **POINT** at the name box, then the description box.

🗣 **SAY**
Every skill has two required fields. The name: max sixty-four characters, only small letters, numbers and hyphens, and no "claude" or "anthropic". The description: max one thousand twenty-four characters, never empty, and it must say what the skill does and when to use it.

---

### STEP 17

🖼 **SHOW** diagram-17

🗣 **SAY**
The description is how the model finds your skill. So it's the most important line you write.

👉 **POINT** at the green good example.

🗣 **SAY**
Good: "Extract text and tables from PDF files. Use when working with PDF files." What it does, and when to use it.

👉 **POINT** at the two red examples.

🗣 **SAY**
Bad: "I can help you process Excel files." Never write "I" or "you". And bad: "Helps with documents." Too vague. Out of a hundred skills, the model will never pick this one.

---

### STEP 18

🖼 **SHOW** diagram-18

👉 **POINT** at the green names, then the crossed-out names.

🗣 **SAY**
Same for the name. Name it after the activity. Processing PDFs. Analyzing spreadsheets. Never vague names like helper, utils or tools.

⏸ **PAUSE**

---

### STEP 19

🖼 **SHOW** diagram-19

🗣 **SAY**
Now, how detailed should the body be?

👉 **POINT** at the bridge on the left.

🗣 **SAY**
Some tasks are a narrow bridge. Only one safe path. Like a database migration. For these, give the exact steps and say "don't change them".

👉 **POINT** at the field on the right.

🗣 **SAY**
Other tasks are an open field. Many paths work. Like a code review. For these, just give the goal and let the model choose. Too many rules here make the skill worse.

---

### STEP 20

🖼 **SHOW** diagram-20

👉 **POINT** at the folder, top to bottom.

🗣 **SAY**
Keep SKILL.md under about five hundred lines. If it grows, split it into other files in the same folder. SKILL.md is read first. The others only when needed. And scripts are run, not read, so only their output costs tokens.

---

### STEP 21

🖼 **SHOW** diagram-21

👉 **POINT** at the red side, then the green side.

🗣 **SAY**
But keep links one level deep. If one file points to another file, which points to another, the model may miss the last one. So link every file directly from SKILL.md.

---

### STEP 22

🖼 **SHOW** diagram-22

🗣 **SAY**
This one I find the most useful, and few people know it.

👉 **POINT** at the checklist on the left.

🗣 **SAY**
If a skill has many steps, give it a checklist. The model copies it and ticks each step. So no step gets skipped.

👉 **POINT** at the circle on the right.

🗣 **SAY**
Or make a loop. Make the change. Run a check. If it fails, fix it, and check again. Only move on when it passes. So the skill checks its own work.

---

### STEP 23

🖼 **SHOW** diagram-23

❓ **ASK**
"You wrote a skill. How do you know it actually works?"

*(stop for 3 seconds)*

✅ **ANSWER**
You test it. And Anthropic says: write the tests before the skill.

👉 **POINT** at the five boxes, left to right.

🗣 **SAY**
Run the task with no skill. Write down what failed. Make three test cases. Write the smallest skill that fixes them. Run the tests again.

👉 **POINT** at the blue box.

🗣 **SAY**
For my writing skill, I wrote a hundred articles and checked each one with an AI-detection tool. The skill was not done until every article scored under five percent AI. And I set that bar myself. That's the human's job.

---

### STEP 24

🖼 **SHOW** diagram-24

👉 **POINT** at Claude A, then Claude B, then the arrows.

🗣 **SAY**
One last trick. Use one Claude session to write the skill. Then open a fresh session that knows nothing, and let it use the skill. Tell it to be harsh and report every mistake. Then fix the skill based on what really happened. Not on guesswork.

⏸ **PAUSE**

---

### STEP 25

🖼 **SHOW** diagram-25

🗣 **SAY**
And the last piece of Pi's prompt, the date and the folder.

👉 **POINT** at the two example boxes.

🗣 **SAY**
If you say "send this tomorrow", the model doesn't know what today is. If you say "run the tests here", it doesn't know which folder. So the harness must tell it. Many people forget this.

🗣 **SAY** — *quick recap, slowly:*
So, part one in three lines. Nine things go into every call, but only the conversation is compacted. Pi builds its prompt fresh on every call from five pieces. And skills load slowly, only when needed, and a good skill is short, easy to find, and tested.

⏸ **PAUSE** — *If you want two videos, you can end video 1 here.*

---

# PART 2 — Compaction: Pi vs Hermes

---

### STEP 26

🖼 **SHOW** diagram-26

❓ **ASK**
"If you were building your own harness, how would you do compaction? Pause and think."

*(stop for 3 seconds)*

✅ **ANSWER**

🗣 **SAY**
Most people say: "When the context is almost full, I'll ask another LLM to summarize the old messages."

👉 **POINT** at LEVEL 1 at the bottom.

🗣 **SAY**
That's not wrong. But it's only level one. If someone says only this in an interview, it means they've never built a real harness.

👉 **POINT** at each level going up.

🗣 **SAY**
Level two: when do you start? Not at the very end. Some time before. But when exactly?

Level three: what do you keep word for word, and what do you summarize?

Level four: where does the cut fall? What if it falls between a tool call and its result?

Level five: what if compaction itself fails?

Real harnesses answer all five. Let's see how.

---

### STEP 27

🖼 **SHOW** diagram-27

🗣 **SAY**
But first, one important fact.

👉 **POINT** at the small parts of the bar, then the big yellow part.

🗣 **SAY**
The system prompt is small. The user messages are tiny. The biggest part is the tool results. File contents. Logs. Test output.

👉 **POINT** at the two boxes below.

🗣 **SAY**
A user asks a ten-word question. The agent runs a command and gets a five-thousand-line error log. And that log is sent again on every later turn. So remember this: tool results eat most of the context.

⏸ **PAUSE**

---

### STEP 28

🖼 **SHOW** diagram-28

🗣 **SAY**
Let's start with Pi. When does Pi compact?

👉 **POINT** at the blue arrow, then the red part at the end.

🗣 **SAY**
The blue arrow is how many tokens we're carrying. At the end, Pi keeps a reserve of sixteen thousand three hundred eighty-four tokens. When we cross the window minus this reserve, Pi compacts.

Why keep a reserve? Because the model still has to write its reply on that turn. So we leave room for the answer.

---

### STEP 29

🖼 **SHOW** diagram-29

❓ **ASK**
"How does a harness even count the tokens in the context?"

*(stop for 3 seconds)*

✅ **ANSWER**
The API tells us. Every reply from the model comes with a usage block, with the exact token count.

👉 **POINT** at the green box, then the left bracket, then the right bracket.

🗣 **SAY**
So Pi finds the last assistant reply. Everything up to there is exact. Pi calls it usageTokens. The few messages after it, Pi estimates. Those are trailingTokens. And the total is just the two added.

---

### STEP 30

🖼 **SHOW** diagram-30

🗣 **SAY**
But even counting has a catch. Look at this example.

👉 **POINT** at box 28 on the right, then move left.

🗣 **SAY**
Pi starts at the newest message, number twenty-eight, and walks backwards. Twenty-eight is a user message, no usage.

👉 **POINT** at the red box 27.

🗣 **SAY**
Twenty-seven is an assistant message, but this call broke halfway. So it has no usage either.

❓ **ASK**
"So which message gives Pi the exact count?"

*(stop for 3 seconds)*

✅ **ANSWER**

👉 **POINT** at the green box 24.

🗣 **SAY**
Number twenty-four. Exact up to there. Everything after it is estimated. So even counting tokens has edge cases.

---

### STEP 31

🖼 **SHOW** diagram-31

👉 **POINT** at the three boxes, left to right.

🗣 **SAY**
And how does Pi estimate? Simple rules. Text: count characters, divide by four. Tool call: count the name and the arguments. Image: always four thousand eight hundred characters. And it guesses a bit high on purpose, so it compacts a bit early, never too late.

⏸ **PAUSE**

---

### STEP 32

🖼 **SHOW** diagram-32

🗣 **SAY**
Pi knows it must compact. Now, what does it keep?

👉 **POINT** at the blue arrow going left, then the orange line.

🗣 **SAY**
Pi walks backwards from the newest message, adding up tokens, until it reaches twenty thousand. That's the cut.

👉 **POINT** at the green boxes on the right.

🗣 **SAY**
These recent twenty thousand tokens stay word for word, because that's what you're working on right now.

👉 **POINT** at the grey boxes on the left.

🗣 **SAY**
Everything before the cut gets summarized.

---

### STEP 33

🖼 **SHOW** diagram-33

🗣 **SAY**
Now, pay careful attention. This is where the real depth is.

❓ **ASK**
"What if the cut lands right on a tool result?"

*(stop for 3 seconds)*

✅ **ANSWER**

🗣 **SAY**
Then the new context starts with an answer, but the question was summarized away. It's like a coat with no ticket. And the API will reject it.

👉 **POINT** at the green list, then the red crossed box.

🗣 **SAY**
So Pi only cuts at legal places. At a user message, fine. At an assistant message, fine. But never at a tool result. A tool result must always stay with its tool call.

---

### STEP 34

🖼 **SHOW** diagram-34

👉 **POINT** at the two column headings.

🗣 **SAY**
Pi asks two questions about each message. Can we cut here? And does this start a turn?

👉 **POINT** at each row.

🗣 **SAY**
User: yes and yes. Tool result: no and no.

👉 **POINT** at the assistant row and the yellow note.

🗣 **SAY**
But assistant: yes we can cut, but no, it doesn't start a turn. That's why the cut can land in the middle of a turn.

---

### STEP 35

🖼 **SHOW** diagram-35

🗣 **SAY**
So what does Pi do when the cut is in the middle of a turn?

👉 **POINT** at the two boxes on the left, then the big box.

🗣 **SAY**
It makes two summaries. One of the old history. And one of the start of this turn, so the question is not lost. Then it joins them into one message. Two LLM calls, one summary.

---

### STEP 36

🖼 **SHOW** diagram-36

👉 **POINT** at each heading, top to bottom.

🗣 **SAY**
And Pi's summary always has the same six sections. Goal. Constraints. Progress: done, in progress, blocked. Key decisions, and why. Next steps. Critical context.

👉 **POINT** at the green strip at the bottom.

🗣 **SAY**
And the list of files read and changed is added by code, not by the model. So it's always correct.

---

### STEP 37

🖼 **SHOW** diagram-37

👉 **POINT** at the five boxes, left to right.

🗣 **SAY**
So Pi, end to end. Take the messages. Count the tokens. Find a safe cut. Summarize with one or two LLM calls. Get a new, shorter context. One clean cut, one big drop.

⏸ **PAUSE**

---

### STEP 38

🖼 **SHOW** diagram-38

🗣 **SAY**
If you think Pi was detailed, wait for Hermes. It does almost everything differently.

👉 **POINT** at the green arrow at the bottom.

🗣 **SAY**
First, Hermes works out the effective window. That's the full window minus the space for the reply.

👉 **POINT** at the red dashed line in the middle.

🗣 **SAY**
And Hermes compacts at fifty percent of that. Half! Pi waits till the edge. Hermes starts at half.

---

### STEP 39

🖼 **SHOW** diagram-39

👉 **POINT** at each box, left to right.

🗣 **SAY**
And Hermes fixes three edge cases. One: never compact below sixty-four thousand tokens. Two: if the window is under five hundred twelve thousand, use seventy-five percent instead of fifty. Three: if the window is even smaller than sixty-four thousand, use eighty-five percent. These edge cases are what make a harness production ready.

---

### STEP 40

🖼 **SHOW** diagram-40

🗣 **SAY**
Second big difference. What does Hermes keep?

👉 **POINT** at HEAD, then TAIL, then MIDDLE.

🗣 **SAY**
It keeps the start, the system prompt and the first three messages. It keeps the end, the recent messages. And it only summarizes the middle.

❓ **ASK**
"Why would you keep the first three messages?"

*(stop for 3 seconds)*

✅ **ANSWER**
Because at the start, the user says what they really want. In the middle, people wander off and get distracted. So the start holds the true goal. Pi keeps only the end. Hermes keeps the start and the end.

---

### STEP 41

🖼 **SHOW** diagram-41

❓ **ASK**
"Remember, tool results are the biggest part of the context. So what do you think Hermes does with old tool results?"

*(stop for 3 seconds)*

✅ **ANSWER**

👉 **POINT** at the messy "before" box, then the small "after" box.

🗣 **SAY**
Before any summary, Hermes shrinks old tool results into one short line. A huge test log becomes "ran npm test, exit zero, forty-seven lines".

👉 **POINT** at the two blue notes on the right.

🗣 **SAY**
If a file was read five times, it keeps only the last copy. And old images are dropped. And this needs no LLM. It's free. So most of the space is saved before any model is called.

---

### STEP 42

🖼 **SHOW** diagram-42

👉 **POINT** down the list.

🗣 **SAY**
And Hermes's summary is bigger. Eleven sections instead of six. It also keeps the active state and the relevant files, so it knows exactly where the work is.

👉 **POINT** at the red note.

🗣 **SAY**
And a nice safety rule: never write an API key in the summary. Write "redacted".

---

### STEP 43

🖼 **SHOW** diagram-43

👉 **POINT** at the five boxes, left to right.

🗣 **SAY**
So Hermes, end to end. Shrink old tool results, free. Keep the start. Keep the end. Summarize only the middle, the one costly step. And next time, update the same summary instead of starting again.

⏸ **PAUSE**

---

### STEP 44

🖼 **SHOW** diagram-44

🗣 **SAY**
Hermes has one more trick. It's called micro-compaction, and I really like it.

👉 **POINT** at the rolling summary, then the red cursor, then E3 to E7.

🗣 **SAY**
Pi compacts everything at once when the context is full. Hermes can do it bit by bit. After every turn, it folds one more exchange into a rolling summary. So when the limit comes, the summary is already ready.

👉 **POINT** at "OFF by default".

🗣 **SAY**
One note. In Hermes, this is off by default. You have to switch it on.

---

### STEP 45

🖼 **SHOW** diagram-45

👉 **POINT** at the left chart, then the right chart.

🗣 **SAY**
If you draw the context size over time: Pi goes up, drops suddenly, goes up again. Like a saw. Hermes with micro-compaction stays almost flat. Same work, just spread out differently.

---

### STEP 46

🖼 **SHOW** diagram-46

🗣 **SAY**
And level five. What if compaction itself fails? Pi just retries. Hermes has four guards.

👉 **POINT** at each box, left to right.

🗣 **SAY**
One, the floor. The system prompt and tools can never be summarized. If they're huge, they alone may fill the window. Hermes knows this.

Two, two strikes. If two tries barely help, stop trying.

Three, cooldown. If the summary model is rate-limited, wait ten minutes and try again.

Four, fallback. Try another model. And if no model works at all, make a simple summary without any model. Compaction must always produce something.

⏸ **PAUSE**

---

### STEP 47

🖼 **SHOW** diagram-47

🗣 **SAY**
Let's put them side by side.

👉 **POINT** at PI, then HERMES.

🗣 **SAY**
When to compact: Pi keeps a fixed reserve. Hermes uses a percentage. Pi reserves a constant, Hermes reserves a proportion.

---

### STEP 48

🖼 **SHOW** diagram-48

👉 **POINT** at PI, then HERMES.

🗣 **SAY**
Where to cut: Pi picks a safe place first. Hermes cuts by size and then fixes the cut. Pi chooses a safe boundary. Hermes repairs the one it took.

---

### STEP 49

🖼 **SHOW** diagram-49

👉 **POINT** at both lists.

🗣 **SAY**
The summary: Pi has six sections, Hermes has eleven. Every harness picks its own shape. Claude Code has its own too.

---

### STEP 50

🖼 **SHOW** diagram-50

👉 **POINT** at each row of the table.

🗣 **SAY**
Here's the full scorecard. When, what is kept, the summary, the free step, and what happens on failure. Same problem, two very different designs. And I think this care for edge cases is a big reason why Hermes became so popular.

⏸ **PAUSE**

---

# PART 3 — DeepSeek Harness, and the cache

---

### STEP 51

🖼 **SHOW** diagram-51

🗣 **SAY**
Now a third harness. DeepSeek has an open-source harness too, called DeepSeek Harness. And it does something different: it puts compaction outside the loop.

👉 **POINT** at the purple circle, then the dashed socket box.

🗣 **SAY**
The core loop is small. It just has a socket for compaction.

👉 **POINT** at the three boxes on the left.

🗣 **SAY**
And you plug in packages. One that does the compaction. One that shrinks tool results first, like Hermes. And one that adds a /compact command. Want a different summarizer? Swap the plugin. Don't touch the loop.

---

### STEP 52

🖼 **SHOW** diagram-52

🗣 **SAY**
And the second idea: DeepSeek Harness never deletes anything.

👉 **POINT** at the top row of boxes.

🗣 **SAY**
Every session is a log. Things are only added, never removed.

👉 **POINT** at the bottom row.

🗣 **SAY**
What the model sees is made from that log. When it compacts, one summary replaces the old messages in what the model sees. But the log still has everything. So if you need the exact old text, you can always read it back.

---

### STEP 53

🖼 **SHOW** diagram-53

👉 **POINT** at the yellow formula.

🗣 **SAY**
When does it compact? It has two limits, and whichever comes first wins. Eighty percent of the window. Or the window minus the reply space minus about sixty-five thousand tokens.

👉 **POINT** at the green formula.

🗣 **SAY**
And it keeps the newest sixteen percent word for word.

👉 **POINT** at the two rows of the table.

🗣 **SAY**
With a small model, the second limit fires first. With a huge model, the eighty percent fires first. So it's like Pi's fixed reserve and Hermes's percentage, both together.

---

### STEP 54

🖼 **SHOW** diagram-54

👉 **POINT** at PRESSURE, then OVERFLOW.

🗣 **SAY**
There are two triggers. Pressure, checked before every call. And overflow, when the provider says "too long" after a call fails.

👉 **POINT** at the boxes, left to right.

🗣 **SAY**
Both go the same way. First, shrink the tool results, free. Check again. If it fits now, skip the summary. If not, make one summary call. And that call sends the same system prompt and tools, so the cache stays warm. We'll see why in a minute.

👉 **POINT** at the bottom box.

🗣 **SAY**
And if the summary fails, it doesn't crash. It just warns and carries on.

---

### STEP 55

🖼 **SHOW** diagram-55

👉 **POINT** at the list, then the blue box.

🗣 **SAY**
Its summary has eight sections. And the model is told: "This is a checkpoint. Just continue." So it doesn't stop and say "thanks for the summary".

So: Pi six, Hermes eleven, DeepSeek eight.

---

### STEP 56

🖼 **SHOW** diagram-56

👉 **POINT** at each column.

🗣 **SAY**
Here are all three together. Same five questions, three different answers. There is no single right design. Only trade-offs.

---

### STEP 57 *(optional, skip if the video is long)*

🖼 **SHOW** diagram-57

👉 **POINT** at the row of boxes, then the red line.

🗣 **SAY**
One small thing about the DeepSeek model itself. During tool use, it keeps its thinking. But when a new user message comes, the old thinking is dropped. The tool calls stay. So context management also lives inside how the model was trained.

⏸ **PAUSE**

---

### STEP 58

🖼 **SHOW** diagram-58

🗣 **SAY**
Now let's talk about something not many people discuss. Prompt caching.

👉 **POINT** at call 1, call 2, call 3.

🗣 **SAY**
Every turn, we send everything again. The system prompt, the tools, all old messages, just to add one new message. But the start is the same every time. So the provider can save that part. That's caching. You mark where it starts with something called cache control.

👉 **POINT** at the three boxes at the bottom.

🗣 **SAY**
Why does it help? The cached part doesn't need to be processed again. So it's cheaper, and the first word of the answer comes faster. And TTL means time to live, how long the cache is kept. For example five minutes or one hour.

---

### STEP 59

🖼 **SHOW** diagram-59

❓ **ASK**
"What do you think happens to the cache when we compact?"

*(stop for 3 seconds)*

✅ **ANSWER**

👉 **POINT** at "before", then "after".

🗣 **SAY**
The system prompt and tools are still cached. But the summary is new, so everything after it has to be processed again. So every compaction costs one cache miss.

👉 **POINT** at the two rule boxes.

🗣 **SAY**
So two rules. Keep the system prompt and tools the same, at the front. And if you compact every turn, you lose the cache every turn. That's the price of the flat line.

⏸ **PAUSE**

---

# PART 4 — Build it for Zill

---

### STEP 60

🖼 **SHOW** diagram-60

🗣 **SAY**
Now it's our turn. Pi and Hermes have thousands of lines for this. Zill is a small harness, so we keep only the main idea.

👉 **POINT** at the green boxes on the right.

🗣 **SAY**
We keep the last six messages exactly as they are.

👉 **POINT** at the grey boxes, then the LLM call, then the yellow summary.

🗣 **SAY**
Everything older goes to the model in one call, and it writes one summary. So the new tape is: one summary, plus the last six messages.

And we borrow three small ideas from today. From Hermes: we copy the user's first request word for word into the summary, so it's never lost. Also from Hermes: we cut big tool results short before summarizing. And from both: our summary has fixed sections.

And to count tokens, we use Pi's simple rule: characters divided by four.

---

### STEP 61

🖼 **SHOW** diagram-61

❓ **ASK**
"Our simple cut has the same problem we saw in Pi. Can you spot it?"

*(stop for 3 seconds)*

✅ **ANSWER**

👉 **POINT** at the cut line on the left.

🗣 **SAY**
The cut can land between "write four.txt" and its result.

👉 **POINT** at the red ORPHAN row on the right.

🗣 **SAY**
So after the fold, the kept part starts with a result with no question. An orphan. And the API rejects it.

👉 **POINT** at the green code box.

🗣 **SAY**
The fix is one line. If the kept part starts with a tool result, drop it. We never invent a fake call. The meaning is already in the summary anyway.

---

### STEP 62

🖼 **SHOW** diagram-63

👉 **POINT** at the yellow box, then the three boxes on the right.

🗣 **SAY**
So this is what we build today. One new file, context.py, with a few small functions. One small socket in the loop, called before_turn, so compaction can plug in. A test file that needs no internet. And a demo with a tiny budget of fifteen hundred tokens, so we can watch it compact live.

⏸ **PAUSE**

---

### STEP 63 — The build

🗣 **SAY**
Okay, let's build it. Open Claude Code in your Zill repo and paste this prompt.

**DO:** paste the prompt below into Claude Code. *(It's also in `zill-lecture4-build-prompt.md`.)*

```text
You are building the next part of Zill (lecture 4 of the series): context
management, meaning the compaction fold that keeps the message array under a
token budget. The parts are cumulative. Your repo already contains the package
zill/ with provider.py (complete(model, system, messages, tools) returns
{"text", "tool_calls", "usage": {"input", "output"}} and uses the neutral
message format {"role": "user"|"assistant"|"tool", "text", ...}), loop.py
(run_loop with the on_event and before_tool sockets), tools.py, operations.py,
security.py, plus demos/ and tests/ from lectures 2 and 3.

Today adds ONE new file, zill/context.py, and ONE small socket in loop.py.
Build exactly what this spec describes and nothing else.

GROUND RULES
- Python 3.10+, standard library only, no third-party packages.
- Must run on Windows, macOS and Linux.
- Same code standard as before: a module docstring on every file naming the
  concept it teaches and the design rules it embodies; a docstring on every
  public function; a short comment wherever behaviour is subtle (the seam,
  the fallback, the "never loop" rule).
- Size targets including documentation, within about 15%: context.py 120
  lines, the loop.py change 10 lines or fewer, tests 140, demo 70.
- Commit after each milestone: loop socket, context.py, tests, demo.
- Do not add features beyond this spec. Where the spec is ambiguous, pick the
  simpler option and note it in a one-line comment at the top of the file.
- Read provider.py and loop.py before you start, and match their names and
  message shapes exactly. If anything below contradicts them, stop and report
  it instead of guessing.

THE ONE IDEA TO PRESERVE
One fold, two halves. When the tape (the message array) is over budget, the
OLD half is folded into one model-written summary message, and the RECENT half
(the last KEEP_RECENT messages) is kept word for word. Summarize the past,
keep the present sharp. The system prompt and the tool definitions are never
part of the fold. They are not in the messages list at all.

------------------------------------------------------------------------------
1) zill/loop.py: the only change allowed to an existing file
------------------------------------------------------------------------------
- Add a keyword parameter before_turn=None to run_loop.
- At the start of every turn, BEFORE provider.complete is called:
    if before_turn is set: messages[:] = before_turn(messages)
  Replace the list IN PLACE, so the caller's list shows the fold too.
- If before_turn raises, report it through on_event (or print one line) and
  continue the turn with the unchanged messages. A broken compactor must never
  kill the run.
- Nothing else in loop.py changes. All existing tests must still pass.

------------------------------------------------------------------------------
2) zill/context.py: the fold
------------------------------------------------------------------------------
Constants
  CHARS_PER_TOKEN = 4       # a budget meter, not a tokenizer
  KEEP_RECENT     = 6       # never summarize the freshest messages
  CLIP_CHARS      = 600     # per message, in the transcript we summarize
  CLIP_TOOL_CHARS = 300     # tool results are clipped harder: they are the bulk
  MARKER          = "[Conversation so far, compacted]"
  SUMMARY_INSTRUCTION = a system prompt for the summarizer that says:
    You compress agent transcripts into a handover note. Use exactly these
    headings: Goal; Constraints and preferences; Progress (done / in progress /
    blocked); Key decisions and why; Files created or edited and their purpose;
    Unresolved errors; Next steps. Be dense and factual, and stay under 250
    words, because the summary itself rides on every later call. Never copy
    secrets such as API keys or passwords: write [REDACTED].

estimate_tokens(messages) -> int
  Sum of len(str(m)) over the list, integer-divided by CHARS_PER_TOKEN.
  The docstring says plainly that this is a rough estimate, which is enough
  because we fold long before the hard ceiling.

render(messages) -> str
  A plain-text transcript, one block per message:
    [role]                   for user and assistant messages
    [tool: <name>]           for tool messages
  followed by the text clipped to CLIP_CHARS (CLIP_TOOL_CHARS for tool
  messages), with " …[clipped N chars]" when something was cut. For an
  assistant message, add one line per tool call: "-> called <name>(<args>)"
  with the arguments clipped to 120 chars. A message whose text starts with
  MARKER (an earlier summary) is kept up to 4,000 chars, because an earlier
  summary must survive into the next one.

original_request(messages) -> str | None
  The text of the first user message that does not start with MARKER. If the
  first message IS an earlier summary, return the text after its
  "Original request (verbatim):" line instead, so the original request
  survives any number of folds.

compact(model, messages, budget_tokens, complete=None, on_compact=None) -> list
  - complete defaults to provider.complete. It is injectable so that the tests
    need no network.
  - If estimate_tokens(messages) <= budget_tokens, or len(messages) <=
    KEEP_RECENT + 1: return messages unchanged (the same object).
  - old, kept = messages[:-KEEP_RECENT], messages[-KEEP_RECENT:]
  - kept = _mend(kept)                     # see THE SEAM below
  - summary = ONE call to complete(model, SUMMARY_INSTRUCTION,
      [{"role": "user", "text": "Summarize this transcript:\n\n" + render(old)}],
      <no tools: pass the empty value that provider.complete accepts>)["text"]
  - If that call raises or returns empty text, do not crash. Use
    _fallback_summary(old) instead, and start it with
    "(fallback summary: the summarizer was unavailable)".
  - head = MARKER + "\nOriginal request (verbatim): " + original_request(messages)
    (clipped to 2,000 chars, omitted if None) + "\n\n" + summary
  - Roles must still alternate correctly. If kept[0] is a user message, merge
    head into it: {"role": "user", "text": head + "\n\n---\n\n" + kept[0]["text"]}.
    If kept is empty after mending, return [{"role": "user", "text": head}].
    Otherwise return [{"role": "user", "text": head}] + kept.
  - Return a NEW list. Never mutate the input list or its message dicts.
  - If the result is STILL over budget, return it anyway. One fold per call,
    never a retry loop. (Hermes' lesson: compaction may fail, it may never
    loop.) The next turn can fold again.
  - If on_compact is given, call on_compact(tokens_before, tokens_after, head)
    after a fold, so a demo can show it.

THE SEAM: _mend(kept) -> list
  The cut before the last KEEP_RECENT messages does not know about call and
  result pairs. If it lands between a tool call and its result, the kept slice
  starts with an ORPHAN tool result whose call was summarized away, and the
  API rejects the whole array. Drop leading messages whose role is "tool"
  until the slice starts on a legal message. Never invent a fake call to match
  an orphan: its meaning is already in the summary. If provider.py pairs
  results with calls by an id, also drop any tool message in kept whose id has
  no matching call in kept.

_fallback_summary(old) -> str
  A deterministic summary with no model at all (Hermes' last resort): the
  tool names used with counts, the paths passed to write_file / edit_file, the
  last three tool results that contain "ERROR" (each clipped to 200 chars),
  and the last assistant text (clipped to 500 chars). Clip the whole thing to
  3,000 chars.

Wiring: the caller passes
  before_turn=lambda msgs: compact(model, msgs, budget_tokens)
to run_loop. Nothing else needs to know that compaction exists.

------------------------------------------------------------------------------
3) demos/context_demo.py: watch the fold happen
------------------------------------------------------------------------------
- Budget from argv, default 1500 tokens (absurdly small on purpose). If that
  default produces no fold with this provider, lower it until it does, and
  report the value you chose.
- Reuse the tools and permission setup from demos/build_demo.py (lecture 3),
  in a fresh temporary folder, so that the demo runs unattended.
- before_turn wraps compact: before each model call it prints
  "turn N: sending X tokens". When a fold happens, it prints
  "*** compacted: X -> Y tokens ***" and the first 600 chars of the head.
- Task: "Create five files one.txt through five.txt, each with 20 lines of the
  word ping, one write_file at a time with a read_file check after each; then
  write MANIFEST.md listing each file and its line count, verified by counting
  the lines (wc -l, or a Python one-liner on Windows)."
- After the run, check from Python that all five files have 20 lines and that
  MANIFEST.md names all five. Print PASS or FAIL, and the number of folds.
  With the default budget, zero folds also means FAIL.

------------------------------------------------------------------------------
4) tests/test_zill_context.py: stdlib unittest, fake complete, no network
------------------------------------------------------------------------------
a) estimate_tokens: a message of about 400 chars gives about 100 tokens.
b) Under budget: compact returns the very same object.
c) KEEP_RECENT + 1 messages, over budget: returned unchanged.
d) Over budget: the result starts with MARKER, ends with the last kept
   messages unchanged, has at most 1 + KEEP_RECENT messages, and the input
   list is not mutated.
e) The seam: when the kept slice would start with a tool message, that message
   is dropped; when every kept message is a tool message, the result is the
   head message alone.
f) Original request: after TWO folds (fold, append more messages, fold again)
   the first user request is still present word for word.
g) A summarizer that raises: the fallback is used, no exception escapes, and
   the result is shorter than the input.
h) A 50,000-char tool result appears clipped in the transcript sent to the
   summarizer (the fake complete records what it receives).
i) Alternation: when the kept slice starts with a user message, the head is
   merged into it and no two user messages are adjacent.
j) The loop socket: run_loop with a fake provider calls before_turn once per
   turn, replaces the list in place, and survives a before_turn that raises.

------------------------------------------------------------------------------
VERIFY BEFORE FINISHING: report each one honestly, with the output
------------------------------------------------------------------------------
(a) All tests pass, including the lecture 2 and 3 tests.
(b) demos/context_demo.py with the default budget of 1500 folds at least once
    and prints PASS.
(c) The same demo with budget 100000 never folds and also prints PASS.
(d) Paste one real summary head that the demo produced.
(e) git log shows today's commits.
If something cannot be verified (for example, no API key), say so plainly
instead of claiming success.
```

🗣 **SAY** — *while it runs:*
While this runs, look at three things in the prompt.

One, it says: add one file and one socket, nothing else. A good prompt keeps the change small.

Two, look at this rule: "If it's still over budget, return it anyway. Never loop." That's Hermes's lesson. Compaction can fail, but it must never loop.

Three, look at the end. It tells Claude Code what "done" means. Tests pass, and the demo actually compacts and prints PASS.

---

### STEP 64 — The demo

🖼 **SHOW** diagram-62

**DO:** run this in the terminal.

```bash
python demos/context_demo.py
```

🗣 **SAY** — *while it runs:*
Look at the counter. A few hundred tokens. Then it grows. Nine hundred. Thirteen hundred. Sixteen hundred. And there. "Compacted." The number drops. That's Zill writing its own summary.

And the task keeps going. Four.txt, five.txt, the manifest. And PASS. The task never noticed.

**DO:** scroll up to the summary it printed.

🗣 **SAY**
Look at the summary. The original request, word for word. The files made so far. What's left to do. Exactly like a handover note.

**DO:** run it again with a big budget.

```bash
python demos/context_demo.py 100000
```

🗣 **SAY**
Now it never compacts, and still passes. So compaction doesn't change what the agent does. It just lets the agent keep going past its own limit.

⏸ **PAUSE**

---

### STEP 65 — Closing

🖼 **SHOW** diagram-64

🗣 **SAY**
Let me leave you with one thing. If you build your own harness, compaction comes down to three questions.

👉 **POINT** at WHEN, then HOW, then WHAT.

🗣 **SAY**
When do I compact? How do I compact: what to keep, where to cut, what to shrink for free? And what does my summary look like?

👉 **POINT** at the red box.

🗣 **SAY**
And for production, one more: what happens when compaction fails?

---

### STEP 66 — Homework and goodbye

🗣 **SAY**
Homework, three small things.

One. Run the demo with a small budget. Read the summary Zill wrote. Find one thing it forgot, and change the summary instruction so it keeps it.

Two. Change KEEP_RECENT from six to two, then to twelve. See how often it compacts, and if the task still passes.

Three. Codex does compaction in yet another way, and it's public. Look at it, and ask the same questions: when, how, what, and what if it fails.

Thank you so much for watching. See you in the next lecture.

---
---

## Notes for you (not spoken)

- **Before recording, run the build prompt once**, so the demo on camera is real.
- **Too long?** Skip Step 57, and Steps 20–21. Or split into two videos after Step 25.
- **Check these numbers against the current code before recording:** Pi (16,384 reserve, 20,000 kept, 4,800 image estimate), Hermes (50% / 64k / 75% / 85%, first 3 messages, 10-minute cooldown, 11 sections, micro-compaction off by default), DeepSeek Harness (80%, 65,536, 16%, 8 sections) from the `dsh-compaction-basic` README.
- Previous versions are saved as `zill-lecture4-script-old.md` and `zill-lecture4-script-v2.md`.
