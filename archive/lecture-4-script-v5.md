# Lecture 4 — Context and Compaction

Read this out exactly as written. The only extra things are small cues in square brackets:

- [PICTURE 28] = put picture 28 on screen (folder `diagrams-lecture4/`).
- [ASK, wait 3 sec] = ask the viewers this question, wait 3 seconds, then keep reading. The answer is the next lines.
- [PAUSE] = take a breath, a new topic starts.
- [DO: ...] = something you type or run on screen.

# PART 1 — What goes into the context

[PICTURE 01]

Alright everyone, welcome back to the Harness Engineering series. This is lecture number four.

Before we start today, I want you to open your Zill repository once and check where you are. It should look exactly like this picture.

From lecture two, you have provider.py. That's the only file that talks to the model provider. And you have loop.py, which is the heartbeat of the harness, the ReAct loop. From lecture three, you have tools.py, which gives Zill its hands. security.py, which is the conscience, the permission gate. And operations.py, which decides where a tool actually runs, on your local machine, over SSH, or in a sandbox.

If you have these five files, you are on the right track. If you don't, please go back and finish lecture three first, because today we are building directly on top of it.

Today we add one more file, context.py. And I'll be honest with you, I think today is probably the most important lecture of this whole series. Let me tell you why.

[PICTURE 02]

When people learn about context, what they usually learn is the elements of a context. The key components. What goes inside. The system prompt, the tools, the skills, the memory files, the conversation. This is called context engineering. Context engineering is the art and science of filling up the context properly. And that's important, no doubt.

But most courses stop right here.

When you are actually designing a harness, there is something much more important, and it's called context management. Context management is about how the harness keeps this context alive and under control, turn after turn, while the agent is working. When should it compact? What should it keep exactly? Where should it cut? And what happens if compaction itself fails?

And the most important part of context management is context compaction. Now, many of you might think compaction is simple, you just summarize the old messages and you're done. It is not as simple as that. Today we are going to open up how Pi does it, how Hermes does it, and how DeepSeek Harness does it. And you will see, it's extremely detailed. These harnesses have thought of so many things that look obvious once you see them, but nobody tells you about them.

And at the end of the lecture, we will build our own compaction into Zill.

[PAUSE]

[PICTURE 03]

So let's start simple. What exactly is context?

In lecture one, we used the analogy of a car for a harness.

The LLM is the engine. It does the thinking.

The tools are the wheels. They let the engine actually move in the real world.

And the context is the fuel. Now think about fuel. What happens when it gets exhausted? It needs to be refilled. And the tank has a fixed size. You cannot keep pouring fuel forever. It's exactly the same with context. Every model has a fixed context window, say two hundred thousand tokens. You cannot keep adding things to it forever. So context is a budget. It's a very, very precious resource, and the harness has to manage it.

[PICTURE 04]

[ASK, wait 3 sec] Remember the loop we built in lecture two. Can you tell me the main arguments this loop takes? Pause the video and think.

The loop takes the messages array, and max turns. And of course it also gets the tools.

So what happens in the loop? We call the model. We check, does the model want to use a tool on this turn? If not, we stop and return the answer. If yes, we run the tool, the tool touches the outside world, we observe the result, and we append that result back into the messages array. And then we go round again.

Now look at the messages array. Every turn, the assistant's reply is appended. Every tool result is appended. Nothing is ever removed. So this array only grows. We call this array the tape. And the important thing is, on every single call, the whole tape is sent to the model again, because the model itself remembers nothing.

So look what happens. Turn one, maybe three thousand tokens. Turn five, nine thousand. Turn ten, twenty-four thousand. Turn twenty, fifty-one thousand. And by turn thirty of a real task, the tape crosses the ceiling, the context window. And then either the API call fails, or the harness starts silently dropping old messages, and the dropped message might be the original task itself.

And notice, nobody wrote a bug here. The loop is doing exactly what we told it to do. Append everything, forever. That rule is what gives the agent its memory, and that same rule is what kills it on a long task.

[PAUSE]

[PICTURE 05]

[ASK, wait 3 sec] So let's make a proper list. What do you think goes into the context every time we call the model? Pause the video and make your own list.

Number one, the system prompt. This tells the agent how to behave.

Number two, very important, the tools. And tools don't come as just names. They come with their whole contract, the one we learned in lecture three: the name, the label, the description, and the parameters. All of that goes in, for every tool, on every call.

Number three, the skills. But here is something very interesting. For a skill, the entire skill file is not put into the context. Only its name and a short description. So even if a skill file is a thousand lines of markdown, only one or two lines about it go in. The model reads that name and description, and decides whether it needs that skill. The full skill is loaded only when it's selected. This is called progressive disclosure, and we'll come to it in a few minutes.

Then numbers four, five and six. This is the messages array itself, and we can break it into three parts. The user messages, which is what you type. The assistant messages, which is what the model thinks and replies. And the tool calls with their tool results.

Number seven, memory. Now, when we say memory, there is short-term memory and long-term memory. The messages array is the short-term memory. Long-term, persistent memory is files like AGENTS.md or CLAUDE.md. When you work on a project, you might keep a CLAUDE.md file with instructions for that project, and it stays across all your sessions.

Number eight, and I'm writing this one as optional. Hermes and OpenClaw do something extra. After a conversation, they decide by themselves what was important to the user, and they save small memory fragments to disk. It can be your local computer, a VM, a database, anywhere permanent. Pi does not do this. Pi only has its AGENTS.md or CLAUDE.md file.

And number nine, which looks very small but is really important. The current working directory, and today's date. So the agent knows which folder it's in and what day it is.

Now here's the key question. Out of these nine things, which ones get compacted?

The system prompt is never compacted. I'm marking it NC, not compacted. The tools, never compacted. The skills, never. The memory files, never. The working directory and date, never.

Only these three, the messages array, are ever compacted. Nothing else in the context is touched. Keep this in your mind, because everything we discuss today is about how to compact just this part.

[PICTURE 06]

A question people always ask me is: what's the difference between a system prompt and a user message? Let me make that very clear.

The system prompt is something that tells the system how to behave. For example, Pi's system prompt starts like this: "You are an expert coding assistant operating inside pi, a coding agent harness. You help users by reading files, executing commands, editing code, and writing new files." And then it gives the list of available tools. That's it, it's actually a very small system prompt.

And this is fixed. Anyone who starts a new session in Pi gets this exact same text. It's a high-level guideline for the harness itself, written by the harness.

A user message is what the user asks in that particular session. For example, "migrate this code base to Rust". That's a user prompt, because I asked it in this session. Tomorrow I'll ask something else. But no matter what I ask, the system prompt is loaded as it is.

And the assistant message is what the LLM thinks and replies. Its thinking tokens, its answer, and the tool calls it decides to make. And this grows every turn.

[PAUSE]

[PICTURE 07]

Okay. Now this list of nine components is fine for a context engineering class. But we are doing harness engineering. So the real question is, how does an actual harness like Pi assemble its context? Let's see what Pi does in practice.

The terminology here is a bit confusing, so listen carefully. When Pi says "system prompt", it doesn't mean one fixed paragraph. It means everything it assembles and sends to the model before the conversation. And it builds this with a function called buildSystemPrompt. This function stacks five pieces, in a fixed order.

Piece one is the base template. "You are an expert coding assistant operating inside pi", plus the available tools list. So what we called "system prompt" and "tools" in our list of nine, Pi merges these two together into this first piece.

Piece two is appendSystemPrompt. This is any extra text you want to glue on at the end of the base template.

Piece three is the project context. This is every AGENTS.md or CLAUDE.md file Pi finds. Can you tell me where this maps on our list of nine? Yes, this is the memory part. We'll look at how it finds these files in a minute.

Piece four is the available skills. Only the name, the description, and the location of each skill file. And look at this small note. This block is added only if the read tool is present. Why? Because to use a skill, the model has to read the skill file. If it can't read files, there's no point telling it about skills.

And piece five, stamped last, the current date and the current working directory.

All five pieces become one single string. And this string is rebuilt on every call. Also, if you give Pi a customPrompt, it replaces the base template completely. So the model's identity is not hard-coded anywhere. It's built fresh, every single time.

[PICTURE 08]

Why does rebuilding every time matter? Look at these three examples.

Example A. Monday, in a repo called app. The date says the fourteenth. One AGENTS.md is found. Three skills are available.

Example B. Tuesday, same repo. What changed? Only the date. That's called date injection. Everything else is the same.

Example C. Same day, but now the read tool is switched off. And the skills block is simply gone, because the model can't open a skill anyway.

So the template stays constant. But the assembled prompt keeps moving with the date, the files and the skills.

[PAUSE]

[PICTURE 09]

Now let's zoom into piece three, the project context. Because there's a really nice detail here that people miss.

Think about how people actually work. At a higher level, you might have one AGENTS.md file which says how you generally like to do all your projects. Then inside one specific project, you have a CLAUDE.md with the instructions for that project. In another project, maybe you're using a different harness, so there's a different file. So these files are spread across different folders.

What Pi does is that it gathers files from two sources. First, the global file, from Pi's own agent folder in your home directory. That's your personal, cross-project standing instructions, and it goes in first.

Then it walks up. It starts at your current working directory. Here, that's the src folder. Nothing there. Then it checks the parent, the repo folder. It finds CLAUDE.md and grabs it. Then the parent of that, work. Nothing. Then the parent, your user folder. It finds AGENTS.md and grabs it. And it keeps going, all the way up to the root of the file system.

And in every folder it checks four file names, in this order: AGENTS.md, AGENTS.MD in capitals, CLAUDE.md, and CLAUDE.MD. This is actually written in Pi's code.

Now look at the final order these files go in. Global first. Then the furthest ancestor folder. And the closest file, last.

Why last? Because the file closest to your project is the most specific one, so it should have the final word. If two files contradict each other, the one closest to your local repo wins.

And one more detail. Pi dedups by path. So a file that's already loaded is never counted twice.

[PICTURE 10]

[ASK, wait 3 sec] Here's a question. Why do you think Pi does this walk again every time it rebuilds the prompt? Why not just once at the start?

Because you can edit these files in the middle of a session.

Look at this timeline. On turn four, the agent is using npm. Now you open CLAUDE.md, in the middle of the session, and add one line: "use pnpm, never npm". On turn five, the prompt is rebuilt, the walk runs again, it finds your edit, and now the agent uses pnpm.

In fact, if there's an important memory you want the agent to keep, you can just write it into your CLAUDE.md mid-session. So the walk has to happen every time, so that whatever you change is captured immediately.

Someone might ask, is there a limit on how many markdown files Pi takes? No, there's no limit. So be careful. If you keep too many markdown files in one project, Pi will collect all of them, and you'll confuse the model.

And if two files disagree, the one closest to your repo is read last, and it wins. But ideally, don't have contradictions in the first place.

And one honest point about Pi here. These files are Pi's only memory. Pi has no separate system for memory. It relies on you, every single time, to update this CLAUDE.md with the things you think are important. That's a design choice. Pi wants to stay minimal.

[PAUSE]

[PICTURE 11]

Next, we come to a very, very important thing, which is skills. A lot of people are really confused about skills. So let me make it very simple.

A skill is one markdown file, called SKILL.md. At the top, it has a small labelled section called the frontmatter. It has two things. A name, here "processing-pdfs". And a description, here "Extracts text and tables from PDF files".

Below that is the body. The real instructions. This can be long, hundreds of lines.

Now here is the key idea. When the context is built, the body is never added. Only the name and the description go into the context. Every turn, for every skill. The body is loaded only when the model selects that skill.

So it's your job to write the name and the description really well. Because the model has to choose which skill to use based only on these two things.

Think of it like a movie trailer. The trailer is short. It tells you what the movie is about. You watch the full movie only if the trailer makes you want to. The name and description are the trailer. The body is the full movie.

This idea is called progressive disclosure. You disclose the skill progressively, little by little, only when it's needed.

[PICTURE 12]

And actually, it's not just two levels. There are three.

Level one, the name and description. Loaded at startup, for every single skill.

Level two, the body of SKILL.md. Read only when the skill is triggered.

Level three. A skill can also point to other files, like a reference file, an examples file, or a scripts folder. These are read only if that specific thing is needed for this task.

So you can bundle as many files as you like with a skill. A bundled file costs nothing until it's actually opened. The model pays for a skill in three instalments, and most of the time it stops at the first one.

[PICTURE 13]

[ASK, wait 3 sec] Let me check if this is clear. What's the difference between a tool and a skill?

A tool is how to do one action. Read a file. Run a bash command. Search with grep. And its full contract is in the context every turn. Tools are the hands.

A skill is what to do, and when to do it. It's a procedure, a set of steps, like a recipe. And only its name and description are in the context until it's picked.

So a skill is the what and the when. A tool is the how. A recipe can call for many hands, but a hand never tells you the recipe.

[PICTURE 14]

Let me give you a real example of a skill I made myself.

I was building a product with a writing agent. And the problem was, whatever it wrote, it looked AI-generated. You know the classic mistakes. Double dashes everywhere. Words like "delve", or "honestly". I did not want any of this. I wanted it to write the way I write.

So what I did is, I gave my agent a few chapters from my own book, and I asked it to create a skill file from them.

And the agent came back with a markdown file called writing-style.md. It had a name, a description, and then a big list of rules. No double dashes. Never "delve". Short paragraphs, real numbers. Explain with one analogy first. And so on.

Now every time this agent runs, this skill is loaded. So next time I want to write a new book, I don't have to explain my style again. A blog post, a landing page, anything. You write one skill once, and you can use it for any number of tasks.

And this is my own philosophy about harnesses. The core of the harness should be very small. And the real power should come from the skill files you write, and the way you write them. Hermes takes a different approach. It ships with a big core and a lot of skill files already built in. Both approaches are valid. But for your own product, the best skills come from your own experience. That's how your product becomes yours.

[PAUSE]

[PICTURE 15]

So now the real question. How do you write a good skill file? What does "good" even mean?

The rules I'm going to show you come from Anthropic's own guide on authoring skills. It's a very densely written document, so I've distilled the key points into pictures.

Rule number one. Say less.

The model already knows a lot. It knows what a PDF is. It knows how libraries work. It knows what React is, what Rust is, why Rust is fast. So you don't need to explain any of that in your skill.

Look at these two. The good one says what's needed in about fifty tokens. The verbose one says the same thing in a hundred and fifty tokens, because it also explains what a PDF is and why libraries exist. That's wasted budget.

Remember, the context window is shared. Your skill sits next to the system prompt, the conversation, and every other skill. So writing a skill is really a budgeting exercise. For every paragraph, ask: does this justify its token cost? If something is common knowledge, cut it.

[PICTURE 16]

Next, the two required fields at the top. First, the name. Maximum sixty-four characters. Only lowercase letters, numbers and hyphens. And you're not allowed to use the words "claude" or "anthropic" in it.

Second, the description. Maximum one thousand twenty-four characters. It must not be empty. And it must say what the skill does, and also when to use it.

And no XML tags in either one. Both fields are actually validated, so if you break these rules, the skill won't load properly.

[PICTURE 17]

Now, the description is probably the most important line you'll write in the whole skill. Here's why. There are only two ways a skill gets found: the name and the description. That's all the model sees. If the description is bad, your skill will never be picked, no matter how good the body is.

Look at the good one. "Extract text and tables from PDF files, fill forms, merge documents." That's what the skill does. Then: "Use when working with PDF files or when the user mentions PDFs." That's when to use it. You need both halves. Most people only write the first half.

Now the bad ones. "I can help you process Excel files." Always write the description in third person. Never "I", never "you".

And "Helps with documents". This is far too vague. Imagine you have a hundred skills. How will the model pick this one? The model chooses between skills on this one sentence alone.

[PICTURE 18]

And the same goes for the name. Name the skill after the activity it does. Processing PDFs. Analyzing spreadsheets. Managing databases. Writing documentation.

Never use vague names like helper, utils, documents, or tools. A name should say what the skill does, not just that it helps.

[PAUSE]

[PICTURE 19]

Now this next rule is a bit non-intuitive. When you write the body of the skill, how detailed should you be? How much freedom should you give the model?

Anthropic uses a really nice picture for this.

Some tasks are like a narrow bridge, with a cliff on both sides. Only one path is safe, and everything else fails. A database migration is like this. Or something very specific to your company or your organization. For these tasks, give low freedom. Write the exact steps, or even give an exact script, and say "do not change it". So it happens in a deterministic way, every time.

Other tasks are like an open field. There are many safe paths, and the right one depends on what the model finds. A code review is like this. For these tasks, give high freedom. Just give the goal, like "review the code for bugs and readability", and let the model choose how.

And here's the non-intuitive part. If you over-specify an open-field task, the skill actually becomes worse. You're taking away the model's judgment where it's actually useful.

[PICTURE 20]

Next, how long should a skill be?

Generally, keep the body of SKILL.md under about five hundred lines. If it becomes bigger than that, split it into separate markdown files in the same folder. The main idea is, don't make huge skill files unnecessarily.

Look at this pdf skill folder. SKILL.md is always read first. FORMS.md, reference.md and examples.md are read only when they're needed. And the scripts folder is special. Scripts are run, not read. So the model doesn't spend tokens reading the script code. Only the output of the script costs tokens.

So SKILL.md works like a table of contents for everything in the folder. Bundle as much as you like, because nothing costs anything until it's opened.

[PICTURE 21]

But be careful with how you link these files. On the left, SKILL.md points to advanced.md, and advanced.md points to details.md. That's two levels deep. This is difficult for the model to follow. It may only skim that last file and miss what's inside.

On the right, SKILL.md points directly to every file. One level deep. That's what you want. Every reference file should be linked straight from SKILL.md, and nothing should link further down.

[PICTURE 22]

Now this one, I personally find the most useful of all, and honestly not many people know about it.

If your skill has many steps, give it a checklist. Step one, analyze the form. Step two, create the field mapping. Step three, validate the mapping. Step four, fill the form. Step five, verify the output. And you tell the model: copy this checklist, and mark each step as done as you go. The model copies it into its reply and ticks things off. A written checklist stops steps from being skipped. This is a vertical pattern, a straight line.

The second pattern is a circle. A feedback loop. Make the change. Then run a validator. If the validator reports errors, fix them, and run the validator again. And only continue when it passes.

So the skill checks its own work. It never just runs and hopes. Most people write a skill as one instruction and move on. But if you put a feedback loop inside your skill, the skill will never move forward without reading its own output. And the more feedback loops you have in your skills, the more robust your whole product becomes.

[PICTURE 23]

[ASK, wait 3 sec] Okay, you wrote a skill. How do you know it's actually working?

You have to test it. And Anthropic's advice actually reorders the whole process: write the tests before you write the skill.

Step one, run the task with no skill at all. Step two, write down exactly what failed. Step three, build a few test scenarios from those failures, say three. Step four, write the smallest skill that fixes them. Smallest, not fullest. And step five, run the tests again.

Let me tell you what I did for my writing-style skill. I used that skill to write about a hundred articles. Then I passed every single article through an AI-detection API. And I gave one clear rule: this skill is not done until every article scores under five percent AI. Only once that happened for all hundred articles did I know my skill was working. And only then did I put it into production.

And notice one thing. I defined that bar. Not the model. That's where the human comes in. Don't just tell the model "design your own criteria". You have to take the effort to define what "good" means.

[PICTURE 24]

And one more simple trick, which almost nobody uses.

Use one Claude session, Claude A, to help you write the skill.

Then open a completely fresh session, Claude B. It knows nothing about how the skill was written, so it's not biased. Give it the skill, let it use it on real tasks, and tell it to be highly critical. Report everything that went wrong.

Then go back and improve the skill based on what Claude B actually did. Not from guesswork.

It's like a small competition. One writes, one judges, and the writer is never "done" until the judge passes it. It's the same idea as GANs, generative adversarial networks. It's such a simple idea, but it makes your skills much better.

[PAUSE]

[PICTURE 25]

We covered four of Pi's five pieces. Now the last one, which looks very small. The current date and the working directory.

Say you tell your agent, "schedule this email for tomorrow at the same time". Which tomorrow? The model doesn't know what today is. It was trained months ago.

Or you say, "run the tests in this project". Which project? It needs to know the folder.

So all of this has to come from the harness. The harness must bake the current date into the prompt. Many people forget this, but it's really important.

So let's quickly lock in part one. One: nine things go into every call, but only the conversation, the messages array, is ever compacted. Two: Pi assembles its prompt fresh on every call, from five pieces: base template, appended text, project context, skills, and the date with the folder. Three: skills use progressive disclosure. Only the name and description are always loaded. And a good skill is short, easy to find, has feedback loops, and is tested.

[PAUSE] (If you want two videos, end video 1 here.)

# PART 2 — Compaction: Pi vs Hermes

Now comes the part which I really think very few people know. Because not many people have actually gone into the code of Pi and Hermes and compared them side by side. We're going to do that now.

[PICTURE 26]

[ASK, wait 3 sec] If you were building your own harness, how would you do compaction? Pause the video and really think about it.

Most people say something like this. "If my model has a context window of two hundred thousand tokens, when it gets close to that, I'll just use another LLM to summarize the past context." Some people say a sliding window. Some people say, throw away the old tool results. These are good thoughts.

But here's the truth. If you go for an interview for an AI engineer role, and someone asks you how context compaction is done, and you only say "use another LLM to summarize the past", it tells them you have no idea how harnesses are built. Especially production harnesses. That answer is not wrong. It's just level one. And there are many more levels of depth.

Level two. When do you start compacting? If the context window is two hundred thousand tokens, you clearly cannot start when your messages reach two hundred thousand. You have to begin some time before. But exactly when?

Level three. What about past messages and new messages? Are you going to compact everything in the same way? Some people will say, keep the new messages and summarize the past. Okay, but how many new messages do you keep? And how do you summarize the past?

Level four. Even if you decide to summarize the past, where does the summarization boundary fall? Remember, the messages array is user, assistant, tool call, tool result, user, assistant, tool call. What if the boundary falls right between a tool call and its result? Then the fresh part starts with a tool result, and you have no idea what question was asked to get that result, because the question got summarized. So the boundary of splitting is very important.

And level five. What if compaction itself fails?

Production harnesses answer all five levels. So now let's uncover how deep modern harnesses actually go.

[PICTURE 27]

Okay, before we jump into Pi, I want to show you one small thing. Because once you see this, a lot of what Hermes does later will just make sense.

[ASK, wait 3 sec] Tell me honestly, what do you think takes up the most space in the context? Is it the system prompt? Is it what you type? Or is it what the model says?

Most people guess the system prompt, or the conversation. But look at this bar.

See this tiny purple bit at the start? That's the system prompt. This thin blue line next to it, that's everything you typed. And this small green part is what the model replied. And then look at this huge yellow block. That's the tool results. All the files the agent read, the folder listings, the build logs, the test output.

Let me give you a real example. Look at the boxes below. You type something very small, like "why is my build red?" That's maybe ten tokens. Now the agent goes and runs a bash command to check, and what comes back? A five-thousand-line error log. That can easily be sixty thousand tokens.

And here's the painful part, right? That log doesn't go away. It sits on the tape. And on every next turn, the whole tape is sent again. So you're paying for that same giant log again, and again, and again.

I see this in almost every agent I build. The context doesn't get full because of what we say. It gets full because of what the agent sees.

So just keep one line in your head: if you control the tool results, you control most of your budget. Remember this, because Hermes uses exactly this idea, and we'll come back to it.

[PAUSE]

[PICTURE 28]

So let's first understand how Pi does compaction. Question one: when does Pi compact?

This long bar is the context window. The blue arrow is contextTokens, how many tokens we're carrying right now.

At the end, Pi keeps a reserve, called reserveTokens. By default it's sixteen thousand three hundred eighty-four tokens. So if the context window is two hundred thousand, Pi won't wait until the tokens reach two hundred thousand.

The rule is: when contextTokens becomes bigger than the context window minus sixteen thousand three hundred eighty-four, Pi decides it's time to compact.

Why keep this reserve? Because compaction itself needs room to run. On the turn that triggers it, the model still has to produce a reply. So you leave space for the answer.

[PICTURE 29]

[ASK, wait 3 sec] But wait. To know when we cross that line, we need to measure the tokens. How would a harness measure how many tokens are in the context?

The harness measures it through the API itself. No matter which LLM provider you use, when the model answers, it comes back with something called a usage block. And that tells you exactly how many tokens that call used.

So Pi finds the last assistant reply that has a usage block. The provider told us the exact usage up to there.

Everything up to that point is exact. Pi calls it usageTokens.

But after that reply, a few more messages may have come in. A tool result, maybe a new user message. The provider hasn't counted those yet. So Pi estimates them. It calls these trailingTokens.

And the total is simply usageTokens plus trailingTokens. Exact where the provider told us, and estimated only for the newest few messages.

[PICTURE 30]

Now even this has a small intricacy. Let me show you a practical example of one session.

These are the last entries of a session, numbers twenty-one to twenty-eight. The newest one is number twenty-eight. And Pi walks backwards from the newest one, looking for the most recent assistant message with a usable usage block.

Twenty-eight is a user message. Users don't have usage blocks.

Twenty-seven is an assistant message. But look, it's red. This call was aborted halfway. The connection dropped, there was an error. So it never got a usage block.

[ASK, wait 3 sec] So looking at this picture, which message gives Pi a usable usage block?

Number twenty-four. The provider told us exactly: one lakh seventy-eight thousand nine hundred tokens up to that point.

And everything after that is estimated. Six hundred, fifteen, thirty, and twelve hundred twenty-three. Add them up, and we get about one lakh eighty thousand seven hundred sixty-eight tokens.

So my point is, even estimating the number of tokens is not easy when you design a harness. You can't just say "I'll look at the usage from the provider". You have to handle cases like: what if the provider returned an error? What if there are trailing messages?

[PICTURE 31]

And how does Pi estimate those trailing tokens, without the API? It uses some simple rules, some heuristics.

For text, count the characters, and divide by four. Roughly four characters make one token.

For a tool call, count the tool name plus the JSON arguments.

And an image is always counted as four thousand eight hundred characters. These are default values Pi uses.

And these estimates deliberately run a little high. Why? Because if you compact a little too early, it costs you a bit. But if you compact too late, the call crashes. So it's safer to guess high.

[PAUSE]

[PICTURE 32]

Okay. Pi now knows it has to compact. But pay very careful attention here. You know when to compact. But what do you compact?

Pi has another setting called keepRecentTokens, which is twenty thousand. So Pi takes all the messages and walks backwards from the newest one, adding up the estimated tokens as it goes.

As soon as the running total reaches twenty thousand, it stops. That's the cut.

These most recent twenty thousand tokens are never compacted. They stay word for word. Because recent messages carry the most important information, what the user cares about right now.

And everything before the cut, Pi will summarize.

[PICTURE 33]

Up to this point, it's easy to understand. Keep twenty thousand recent tokens, summarize the rest. But this is where you need to understand the details. This is where harnesses are so much more important than we think.

[ASK, wait 3 sec] How do you know where exactly to draw this line? What if the cut happens right on a tool result?

Think about what comes into the context then. The past gets summarized. And the fresh part starts randomly with a tool result. An answer, but we have no clue what question was asked to get that answer, because the question was summarized away. It's like walking into a cloakroom with a coat but no ticket. And the API will actually reject this whole message array.

So what Pi does, very intelligently, is it defines legal places to cut. You can cut at a user message, because a new chain starts there. You can also cut at an assistant message, because the assistant message kind of summarizes what the user asked. You can also cut at a bash execution, a custom entry, a branch summary, or an earlier compaction summary.

But you can never cut at a tool result. A tool result must always stay attached to the tool call that asked for it. Cutting between a tool call and its result leaves the history broken.

[PICTURE 34]

And there's one more subtle thing. Pi actually asks two different questions about each message.

Question one: can we cut here? Question two: does this message start a turn? A turn means the user's question plus everything that answers it.

A user message: yes we can cut, and yes it starts a turn. A tool result: no we can't cut, and no it doesn't start a turn.

But look at the assistant row. Yes, we can cut there. But no, it does not start a turn. And this row is exactly why a cut can land in the middle of a turn. Pi keeps the assistant's recent work, but the user's question that started this turn is now on the old side.

[PICTURE 35]

So what does Pi do when the cut lands in the middle of a turn?

It makes two summaries. The first is the normal history summary, of everything before this turn. It gets a budget of eighty percent of reserveTokens.

The second is called the turn prefix summary. It summarizes the start of this turn, what the user asked, which is now on the old side. It gets a budget of fifty percent of reserveTokens.

Then both are joined into one single summary message. The history summary first, then a section called "Turn Context, split turn". So that's two LLM calls, but one stored summary. And the model never loses the question it's in the middle of answering.

[PICTURE 36]

And when you compact, what should the summary always contain? This is important for any harness.

Pi's summary always has the same shape. The goal. The constraints and preferences. The progress, split into done, in progress, and blocked. The key decisions. The next steps. And the critical context.

And for each key decision, it also writes why that decision was made. Because the next model needs to know the reason, not just the decision.

And at the end, the list of files read and files modified. And notice, this list is appended automatically by code, not written by the model. So it's always accurate.

Why a fixed shape? So that the next model always knows exactly where to look.

[PICTURE 37]

So let's put Pi together. We start with the session entries. prepareCompaction counts the tokens and checks the sixteen thousand rule. findCutPoint walks back twenty thousand tokens and makes sure it never stops on a tool result. Then one or two LLM calls write the summary, two if the turn was split. And you get a new, shorter context.

So Pi decides where to cut first, and then summarizes everything before the cut. One clean cut, one summary, one big drop.

And all of this is publicly available in Pi's code, in one file called compaction.ts. It's just very difficult to pull out and teach to someone, which is why I made these pictures.

[PAUSE]

[PICTURE 38]

Now, if you think Pi was detailed, you'll be even more surprised by Hermes. It does almost everything differently. And honestly, Hermes is a lot more detailed than Pi when it comes to context management.

Same first question. When does Hermes compact?

Hermes first works out something called the effective window. That's the context length minus max_tokens, the maximum output tokens reserved for the reply.

And then it triggers compaction at fifty percent of that effective window. Fifty percent! Think about how different that is. Pi waits until it's almost at the edge. Hermes starts compacting at the halfway point.

[PICTURE 39]

But that fifty percent is not the whole story. Hermes has three more rules for edge cases.

Rule one is a floor. Never trigger below sixty-four thousand tokens. Otherwise a small model would start compacting while half its window is still empty.

Rule two. If the model's window is under five hundred twelve thousand tokens, raise the trigger from fifty percent to at least seventy-five percent. Because we don't want a small window to compact too early.

Rule three. What if the floor itself is bigger than the context window? For example, a model with a thirty-two thousand window, and our floor is sixty-four thousand. That makes no sense. So in that case, Hermes uses eighty-five percent of the window instead.

The reason I'm going into all these technical details is that this is how harnesses are actually built. These rules stop a small model from compacting too early, or never compacting at all.

[PICTURE 40]

Now the second big difference. What does Hermes keep?

Hermes keeps the beginning as it is. The head. That's the system prompt plus the first three messages.

It keeps the end as it is. The tail. About twenty percent of the trigger, measured in tokens.

And it summarizes only the middle. The beginning and the end are protected.

[ASK, wait 3 sec] Why would Hermes keep the first three messages? Pi doesn't do that.

Think about it. When a user starts a session, they're fresh. The first few messages usually tell you what they actually wanted to do in that session. The true intent. In the middle, the user might wander off, might get distracted, might try other things. So the first three messages are very valuable. That's why Hermes keeps them.

Pi does not retain the beginning. Pi only keeps the tail. Hermes keeps both the head and the tail.

[PICTURE 41]

[ASK, wait 3 sec] Now remember what I told you about tool results taking most of the space. Hermes does something with old tool results that Pi doesn't. What do you think it is, and why is it so smart?

Before Hermes summarizes anything, it first prunes the old tool results. It rewrites each old tool result as one short, descriptive line. A tool result might contain a whole error message, a thousand or five thousand lines. But you may only need one line from it. So a huge test output becomes just: "terminal, ran npm test, exit zero, forty-seven lines".

Two more rules. If the same file was read five times, Hermes keeps only the newest copy. And old images are dropped.

And here's the best part. This step is fully deterministic. There's no LLM involved. It costs nothing. So one big advantage of Hermes is that most of the space is won back before any model is even called. And then only the middle is summarized.

[PICTURE 42]

And the summary itself. Pi had six sections. The summary of Hermes is a lot more detailed.

It has eleven sections. Historical task snapshot. Goal. Constraints and preferences. Completed actions. Active state. Blocked. Key decisions. Resolved questions. Relevant files. Critical context. And pruned skills.

So Hermes also records the exact working state. What's active right now, and which files matter.

And one nice safety rule in the critical context section: never write an API key into the summary. Write "REDACTED" instead.

[PICTURE 43]

So Hermes end to end. Step one, prune the old tool results. Free, no LLM call. Step two, protect the head. Step three, protect the tail. Also free. Step four, summarize the middle. That's the only expensive step. And step five, the next time it compacts, it doesn't start from zero. It updates the summary it already has.

So four cheap steps, around one expensive one.

[PAUSE]

[PICTURE 44]

But Hermes does not even stop here. It has a technique called micro-compaction. And I think it's really beautiful.

What Pi does is batch compaction. When the context reaches the limit, it summarizes all the past messages at once, and the context drops. Then it grows again, reaches the limit, summarizes again, drops again.

Micro-compaction spreads that same work out over time. After every completed turn, meaning the user message, the assistant reply and the tool result, Hermes folds that one exchange into a rolling summary. E1 and E2 are already folded into the rolling summary.

This red line is the cursor. E3 to E7 are not folded yet, so they're kept as they are. After the next turn, the cursor moves one step to the right.

So when the limit finally comes, you don't have to summarize everything in the past again. It's already summarized, because Hermes kept that rolling summary updated after every turn.

One honest note. In Hermes, micro-compaction is off by default. You have to turn it on.

[PICTURE 45]

And you can actually see the difference if you plot the context size over time.

For Pi, the context climbs, then one long pause and a big drop, then it climbs again. An up-and-down, like a sawtooth.

For Hermes with micro-compaction, many tiny pauses, and the line stays almost flat. It's the same total work, just spread differently across the session.

Now someone might ask: won't micro-compaction cause problems with the KV cache, since the conversation keeps changing every turn? That's a good question. Yes, every fold changes the conversation after the fixed part, so that part has to be computed again. We'll talk about caching in part three. I haven't seen this documented as a problem in Hermes, so I'd check before relying on it.

[PICTURE 46]

And now level five of our ladder. What if compaction itself fails? Pi just retries. But Hermes actually thinks about where compaction can fail, and it has four separate guards.

Guard one, the floor. Remember, some parts of the context are never compacted: the system prompt and the tool schemas. Now what if a user has a huge system prompt and a thousand tools? Even before any message, these fixed parts might already be close to the window. Hermes knows these can't be summarized, and accounts for it.

Guard two, two strikes. Sometimes Hermes compacts once, and it's still above the limit. It compacts again, and it's still above. If two passes barely help, Hermes stops trying. It never loops forever.

Guard three, cooldown. To summarize, you need an LLM. What if that summary model is rate-limited? Then Hermes waits six hundred seconds, ten minutes, and tries again.

And guard four, fallback. If the summary model isn't available, it tries an auxiliary model. If that fails, the main model. And if no model is available at all, maybe your API bill isn't paid, it builds a summary with no model at all. Fully deterministic, using character budgets. Because compaction has to produce something.

So compaction is allowed to fail. But it's never allowed to loop.

[PAUSE]

[PICTURE 47]

So let's put Pi and Hermes side by side, because it's very interesting how different they are.

When to compact. Pi keeps a fixed amount of room at the end. Sixteen thousand three hundred eighty-four, always.

Hermes uses a percentage of what's left. Fifty percent, or seventy-five, or eighty-five, depending on the model.

So Pi reserves a constant. Hermes reserves a proportion.

[PICTURE 48]

Where to cut. Pi picks a legal cut point first, never on a tool result, and if the turn is split, it summarizes the split part separately.

Hermes cuts by token budget first, and then moves the cut until the tail is valid.

So Pi chooses a safe boundary. Hermes repairs the boundary it took.

[PICTURE 49]

The summary. Pi has six sections, plus the files read and modified. Hermes has eleven sections. Both keep the key decisions. Hermes also keeps the working state.

And every harness has its own shape. Claude Code follows its own structure for the compacted information too.

[PICTURE 50]

So here's the full scorecard. When: window minus sixteen thousand, versus fifty percent of the effective window. What's kept: the last twenty thousand tokens, versus head and tail. Summary: six sections versus eleven. Free step: Pi has none, Hermes prunes tool results first. And if it fails: Pi retries, Hermes has the floor, two strikes, cooldown and fallback. Plus Hermes can micro-compact every turn.

Remember, this series is about production-level harnesses. When you ship to production, users never see compaction. So it simply has to work. And I really feel that one of the reasons Hermes has become so popular is that they've thought about these edge cases so well.

[PAUSE]

# PART 3 — DeepSeek Harness, and the cache

[PICTURE 51]

Now there's a third harness I want to show you. DeepSeek also has an open-source harness, called DeepSeek Harness. And its big idea is about where compaction even lives.

In Pi and in Hermes, compaction is built into the harness itself. It's part of the core.

In DeepSeek Harness, the core agent loop is kept small, and compaction is a plugin. The loop only has a socket. They call it a seam, named ctx.compaction. And you plug a compaction engine into it from outside.

The basic engine is a package called dsh-compaction-basic. That's the one that actually does the folding.

Then there's an optional package, the tool-result pruner. It trims big tool outputs before summarizing. Does that sound familiar? It's the same idea as Hermes' free step.

And there's a command package that gives you a /compact command, so you can trigger compaction by hand whenever you want.

So if you want a different summarizer, you just swap the plugin. You never touch the loop. Pi and Hermes build compaction in. DeepSeek Harness plugs it in.

[PICTURE 52]

The second big idea is even more interesting. In DeepSeek Harness, compaction never deletes anything.

Every session is an append-only log of events. Things are only ever added to it. Never removed.

Even compaction itself is written into the log as events. Compaction start, compaction summary, compaction end. These are log-only events. The model never sees them.

What the model actually sees is derived from that log. They call it the surface. When compaction happens, it doesn't delete the old events. It just changes the surface. One summary, wrapped in a tag called compacted-summary, replaces a range of old messages. They call that range the shadowed range. And the recent tail stays exactly as it is.

So compaction is lossy for the model, but not for you. If you ever need the exact old text, you can always read it back from the log.

[PICTURE 53]

Same first question again. When does DeepSeek Harness compact?

It uses two limits, and whichever comes first wins. Limit one: eighty percent of the window. Limit two: the window, minus the output cap, minus an extra headroom of sixty-five thousand five hundred thirty-six tokens. The trigger is the smaller of the two.

And after compacting, it keeps the newest sixteen percent of the window minus the output cap, word for word.

Let me show you why two limits matter. Take a two-hundred-thousand-token model with a thirty-two-thousand output cap. Eighty percent is one lakh sixty thousand. But the headroom rule gives about one lakh two thousand. That's smaller, so the headroom rule fires first.

Now take a one-million-token model, same output cap. Eighty percent is eight lakh. The headroom rule gives about nine lakh. Now the eighty percent rule fires first.

So for a small window, the headroom rule bites. For a huge window, the eighty percent rule bites. You could say it's Pi's fixed reserve and Hermes' percentage, both at the same time.

[PICTURE 54]

Now let's walk through the whole pipeline.

There are two triggers. Trigger one is pressure. It's checked before the request is built, on every step. That's the normal one. Trigger two is overflow. That's when the provider actually comes back with an error saying "context window exceeded". That happens after a failed call. Both go into the same pipeline.

First, if the pruner plugin is installed, it prunes the tool results. Free, no model call.

Then it measures again. If it fits now, it skips the summary completely. That saves a whole LLM call.

If it still doesn't fit, it makes one summary call. And here's a clever detail. That summary call replays the same system prompt and the same tools, so that the provider's prefix cache stays warm. We'll understand why that matters in a few minutes. Then the summary replaces the oldest span.

For an overflow, it shrinks harder in one pass, and retries only once. That setting is called maxOverflowRetries, and the default is one.

And if the summary itself fails, it doesn't crash. It logs a warning and carries on with the full history.

[PICTURE 55]

And DeepSeek's summary also has a fixed shape. Eight sections. Primary request and intent. Key technical concepts. Files and code. Errors and fixes. Pending jobs. Current work. Next step. And critical context.

It's wrapped in that compacted-summary tag, and the model is told: this is a checkpoint, continue, and don't acknowledge it. So the model doesn't stop and say "thank you for the summary".

Only the summary text is kept. No reasoning, no tool calls. And it's honest about its limits. It cannot shrink the system prompt, the tools, or one single giant tool call.

So: Pi six sections, Hermes eleven, DeepSeek Harness eight.

[PICTURE 56]

So let's put all three on one page. When: Pi, window minus sixteen thousand. Hermes, fifty percent of effective. DeepSeek, the smaller of eighty percent or window minus output minus sixty-five thousand. Keep: Pi, the last twenty thousand tokens. Hermes, head and tail. DeepSeek, the newest sixteen percent. Free step: Pi none, Hermes prunes tool results, DeepSeek has an optional pruner. Summary: six, eleven, eight sections. On failure: Pi retries, Hermes has four guards, DeepSeek warns and carries on, and retries an overflow once.

Same five questions. Three different answers. There's no single right design. There are only trade-offs.

[PICTURE 57]

One last thing about DeepSeek. Context management doesn't only live in the harness. It also lives in how the model was trained.

In the DeepSeek V3.2 paper, they describe a rule for the model's own thinking during tool use. While tool results keep arriving, the thinking is kept. The model can keep reasoning across many tool calls.

But when a new user message arrives, the old thinking is dropped. The tool calls and their results stay. Only the old reasoning goes.

And for their search agents, they also tested what to do when the context is nearly full. One strategy, called "discard all", just wipes the tool history and keeps the original question. And surprisingly, simple strategies like that worked really well.

[PAUSE]

[PICTURE 58]

Now, since we keep mentioning the cache, let me talk about something that's not discussed very often, but matters a lot for cost. Prompt caching.

If you think about it, what our loop does is pretty wasteful. Every single turn, we re-send the entire conversation. The system prompt, every tool schema, every earlier turn. Just to add one new tool result at the end and ask, "what's next?"

The model is stateless, so yes, it needs the whole thing. But the beginning is exactly the same every time. So the provider can keep the work it already did. Call one, everything is new. Call two, the same prefix is cached, and only the new part is computed. Call three, the cached part is even longer.

This cache is stored on the provider's server side. We never see it. And the point where caching starts is marked with something called cache_control, a breakpoint.

Now, how does this save cost? People who've studied inference will understand this. Inference has two phases, prefill and decode. During prefill, the model computes the key and value vectors for every input token. That's where all the time goes. But for the cached part, those K and V vectors are already computed and stored. So you don't need to compute them again.

That means a lower bill. And it's faster. There's a metric called TTFT, time to first token, and caching reduces it a lot.

And one more term, TTL, time to live. That's how long the cache is kept. For example five minutes, or one hour. Different harnesses support different TTLs. Pi, for example, supports the one-hour TTL and tracks it separately. So even if the provider caches automatically, your harness should say where the breakpoints go and how long to keep them.

[PICTURE 59]

[ASK, wait 3 sec] So now connect this to compaction. What do you think happens to the cache when we compact?

Before the fold, the system prompt and tools are cached. The long history is cached. Only the new message is new.

After the fold, the system prompt and tools are still cached, because they didn't change. But the summary is new. And the recent messages are now in a different position, so they have to be computed again. So every fold costs you one cache miss.

So two rules come out of this. Rule one: keep the system prompt and tools stable, and at the front. Then they stay cached across every fold. That's exactly why DeepSeek Harness replays them in its summary call.

Rule two: if you fold every turn, like micro-compaction, you get a cache miss every turn. That's the price you pay for the flat line.

So fold rarely, fold cleanly, and keep the front of the prompt still.

[PAUSE]

# PART 4 — Build compaction into Zill

[PICTURE 60]

So now we've seen how the best harnesses do it. Now it's our turn.

Pi and Hermes have thousands of lines for this. A lot of that code is for supporting many model providers and switching between them. But Zill is a minimal harness. The principle is: keep only what's most important. So we keep only the core idea.

When the tape goes over budget, we cut it in two. The recent half is the last six messages. We keep them word for word. Six is a constant called KEEP_RECENT.

The old half, everything older than that, goes to the language model in one call, and it writes one summary. So the new tape is just one summary message, starting with "Conversation so far, compacted", followed by the six kept messages.

And to estimate tokens, we use the simplest rule, exactly Pi's: characters divided by four.

And we borrow three cheap ideas from what we saw today.

From Hermes, we protect the head in a small way. The user's original request is copied into the summary word for word, so it survives any number of folds, no matter how many times we compact.

Also from Hermes, tool results are clipped hard before we send them to the summarizer, because they are the bulk.

And from Pi and Hermes, our summary has fixed sections: goal, constraints, progress, decisions, files touched, errors, and next steps.

[PICTURE 61]

[ASK, wait 3 sec] Our simple fold has exactly the same problem we saw in Pi. Can you spot it?

The place where the summary meets the kept messages is called the seam. Our rule "keep the last six" doesn't know anything about tool calls and results. So look here. The cut falls between "write four.txt", which is the call, and "Wrote four.txt", which is its result.

So after the fold, the kept part starts with a tool result whose call was summarized away. An orphan. The coat with no ticket. And the API rejects it.

The fix is one line. While the kept part starts with a tool message, drop it.

And notice what we do not do. We don't invent a fake call to match the orphan. That would be writing a lie into the agent's history. Dropping the orphan is safe, because its meaning is already inside the summary.

It's the same rule as Pi's "never cut on a tool result", just done the cheap way.

[PICTURE 63]

So here's exactly what we build today. One new file, zill/context.py. Two constants: four characters per token, and keep the six most recent messages. And a few small functions. estimate_tokens, our meter. render, which turns the old messages into a plain transcript. compact, which does the fold. mend, which fixes the seam. And a fallback summary that needs no model at all, Hermes' last resort, in case the summarizer is down.

One small change in loop.py: a new socket called before_turn. Before every model call, the loop hands the tape to this function and uses whatever comes back. That's how compaction plugs in. A bit like DeepSeek Harness, the loop doesn't even need to know compaction exists.

A test file, with a fake model, so the tests don't need the internet. And a demo with a budget of only fifteen hundred tokens. That's absurdly small on purpose, so we can watch compaction happen right in front of us.

[PAUSE]

Okay, let's build it. Open Claude Code inside your Zill repo, and paste this prompt.

[DO: paste the prompt below into Claude Code. *(It's also saved as `zill-lecture4-build-prompt.md`.)*]

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

While this is running, let me show you a few things in this prompt.

First, look at the top. It says today we add one file and one socket, and nothing else. A good prompt keeps the change small, so you can actually review every line.

Second, look at the rules inside compact. "Return a new list, never change the input." And: "If the result is still over budget, return it anyway. One fold per call, never a retry loop." That's exactly Hermes' lesson. Compaction may fail, but it must never loop.

Third, look at the summary instruction. "Stay under two hundred fifty words." Why? Because the summary itself rides on every later call. A long summary would eat the very budget we're trying to save.

And fourth, look at the end. It tells Claude Code what "done" means. All tests pass. The demo compacts at least once and prints PASS. With a huge budget it never compacts and still passes. And if something can't be verified, it has to say so honestly.

[PICTURE 62]

[DO: run the demo in the terminal.]

```bash
python demos/context_demo.py
```

Look at the counter. Turn one, a few hundred tokens. Then it climbs. Nine hundred. Thirteen hundred. Sixteen hundred.

And there. "Compacted." The number drops. That dip is Zill writing its own recap. It just replaced the whole history with one paragraph.

And look, the task keeps going. It writes four.txt, five.txt, and then MANIFEST.md. And at the end, PASS. The task never even noticed that its history was folded. This is exactly the sawtooth from the picture. Climb, fold, climb, fold.

[DO: scroll up to the summary it printed.]

Let's read the summary Zill wrote about itself. "Original request, verbatim." The whole task, word for word. Then the files created: one, two, three. The key decisions. And what's left to do. Exactly what a colleague would want in a handover note.

[DO: run it again with a big budget.]

```bash
python demos/context_demo.py 100000
```

Now it never compacts, and it still passes. So compaction doesn't change what the agent does. It just lets the agent keep working past its own window.

[PAUSE]

[PICTURE 64]

So let me leave you with the one thing I really want you to take away from today.

It's not enough to just know the components of a context. That's only the first part. If you're designing your own harness, compaction comes down to three decisions.

When do I compact? A fixed reserve like Pi, a percentage like Hermes, or both like DeepSeek.

How do I compact? What do I keep exactly, where does the cut fall, and what can I prune for free?

What does my summary look like? Which sections must always survive?

And if you're going to production, one more. What happens when compaction itself fails?

For homework, I want you to do three things.

One. Run the demo with a small budget, and actually read the summary Zill wrote about itself. Find one thing it dropped that you think was important. Then change the summary instruction so it keeps that.

Two. Play with the numbers. Change KEEP_RECENT from six to two, and then to twelve. Change the budget. Watch how often Zill compacts, and whether the task still passes. You'll feel all the trade-offs we talked about today.

Three. Pi and Hermes are not the only ones. Codex does compaction in yet another way, and its techniques are public. Go through it, and compare it with Pi, Hermes and DeepSeek Harness. Ask the same questions: when, how, what, and what if it fails.

Thank you so much for watching, and I'll see you in the next lecture.

---

## Notes for you (not spoken)

- **Before recording, run the build prompt once in Claude Code**, so the demo you show on camera is real.
- **If the video is too long:** skip Step 57, the cache question in Step 45, and Steps 20–21. Or split into two videos after Step 25.
- **Check these numbers against the current code before recording:** Pi (16,384 reserve, 20,000 kept, 4,800 image estimate, split-turn budgets 80% / 50%), Hermes (50%, 64k floor, 512K → 75%, 85%, first 3 messages, 20% tail, 600-second cooldown, 11 sections, micro-compaction off by default), DeepSeek Harness (80%, 65,536 headroom, 16% kept, retry once, 8 sections) from the `dsh-compaction-basic` README. "Pi supports the one-hour TTL" is from your transcript.
- Older versions are saved as `zill-lecture4-script-old.md`, `zill-lecture4-script-v2.md` and `zill-lecture4-script-v3-short.md`.
