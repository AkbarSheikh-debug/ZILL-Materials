# Lecture 4 — Context and Compaction

*How to use this: just read it out, the way you talk. Lines starting with **▶** mean "put this picture on screen". A line with **— — —** means a small pause or change of topic. That's all. Pictures are in `diagrams-lecture4/`.*

---

## PART 1 — What goes into the context

▶ diagram-01

Alright everyone, welcome back to the Harness Engineering series. This is lecture four.

Before we get started, just open your Zill repo once. At this point it should look like this picture. From lecture two you have provider.py and loop.py. From lecture three you have tools.py, security.py and operations.py. If you have these five files, you are on the right track. If not, please go back and finish lecture three first, because today we are building on top of it.

And honestly, I think today is probably the most important lecture of this whole series. Let me tell you why.

▶ diagram-02

Today we are going to talk about context. Now, when people learn about context, they usually learn the elements of a context, the key components, and then they stop there. That part is called context engineering. Context engineering is basically the art of filling up the context properly. That's fine, it's important.

But when you are designing a harness, what is much more important is something called context management. How does the harness keep this context under control, turn after turn? And one of the most important parts of context management is context compaction.

Many of you might think compaction is just summarizing the context. It is not as simple as that. Today we are going to look at how Pi does it, how Hermes does it, and how DeepSeek Harness does it. And it is actually extremely detailed. It's very beautiful how these harnesses do it. After this lecture, I think you'll say, "I never thought compaction would be this detailed."

And at the end, we will build our own compaction for Zill.

— — —

▶ diagram-03

So let's start simply. What is context?

When we looked at the analogy of a harness in the first lecture, we said the LLM is the engine, the tools are the wheels, and the context is the fuel. And what happens with fuel? Once it gets exhausted, it needs to be refilled. There is a budget to it. You cannot just keep on adding things to the context. It's a very precious resource.

▶ diagram-04

Now remember our loop. Let me ask you a question, and you can pause the video and think. The loop which we built in lecture two, what are the arguments it takes?

It takes the messages, and it takes max turns. And it also gets the tools. So we call the model, we check if a tool is needed. If not, we end. If yes, we run the tool, we observe the result, and we append it back to the messages array.

So this messages array is something which keeps on growing. Every turn, something gets appended. Nothing is ever removed. And every single time we call the model, the whole thing is sent again. So if you look at this chart, turn one is maybe three thousand tokens, then nine thousand, then twenty-four thousand, and by turn thirty of a real task, you hit the ceiling. Nobody wrote a bug here. The loop is doing exactly what we told it to do.

— — —

▶ diagram-05

So let's make a systematic list of everything that comes into the context. You can pause and make your own list first.

Okay. The first thing is the system prompt. Second, very importantly, the tools. And tools come with their full contract, the name, the label, the description and the parameters.

Third, the skills. But for skills, the entire skill file is not passed. Only its name and a short description. So if a skill file is a thousand lines of markdown, only the name and one or two lines of description go in. We'll see why in a few minutes.

Then the messages array itself, which we can break into three parts: the user messages, the assistant messages, and the tool calls with their results.

Then memory. Pi uses files like AGENTS.md or CLAUDE.md, which you write for your project and which stay across all your sessions. Hermes and OpenClaw do something extra. After a conversation, they decide by themselves what was important, and they save small memory fragments to disk. Pi doesn't do this. So I'm writing that one as optional.

And the last one, which is small but very important, the current working directory and today's date.

So these nine things go into every call. Now look at the right side. Out of these nine, which ones are compacted? The system prompt is never compacted. Tools, never. Skills, never. Memory files, never. Working directory and date, never. Only the messages array is compacted. Nothing else in the context is touched.

▶ diagram-06

People often ask me, what's the difference between a system prompt and a user message? So a system prompt tells the agent how to behave. For example, Pi's system prompt starts with "You are an expert coding assistant operating inside pi, a coding agent harness", and then it lists the available tools. This is the same for every session. Anyone who starts Pi gets this.

A user message is what you ask in that particular session. Like "migrate this code base to Rust". That changes every session. And the assistant message is what the LLM thinks and replies, plus the tool calls it makes.

— — —

▶ diagram-07

Okay, now this list of nine things is fine for a context engineering class. But we are doing harness engineering. So let's see what Pi actually does in practice.

The terminology here is a bit confusing. When Pi says "system prompt", it doesn't mean one fixed paragraph. It means everything that it assembles before the conversation. And it builds this with a function called buildSystemPrompt, from five pieces, stacked in order.

First, the base template. "You are an expert coding assistant operating inside pi", plus the list of available tools. So Pi merges the tools into this first piece itself.

Second, appendSystemPrompt. Any extra text you want to glue on.

Third, the project context. Every AGENTS.md or CLAUDE.md file it finds. Can you guess where this maps on our list of nine? Yes, that's the memory part.

Fourth, the available skills. Only the name, the description and where the file is. And notice, this block is added only if the read tool is present. Because if the model cannot read files, it cannot open a skill anyway.

And fifth, stamped last, the current date and working directory.

All five pieces become one string, and that string is rebuilt on every call.

▶ diagram-08

So look at what that means. Monday, in a repo, the date is the fourteenth, one AGENTS.md, three skills. Tuesday, same repo, only the date changed. And if you switch off the read tool, the skills block is simply gone. So the template stays the same, but the assembled prompt keeps moving.

— — —

▶ diagram-09

Now let's zoom into the project context, because there is a nice detail here.

Think about how people actually work. At a higher level, you might have one AGENTS.md file which says how you generally like to do your projects. And inside one specific project, you have a CLAUDE.md with the instructions for that project. In another project, maybe you're using a different harness, so you have a different file.

What Pi does is that it grabs all of these markdown files. First it loads the global one, from its own folder in your home directory. That's your personal, cross-project instructions. Then it walks up. It starts at your current working directory, then checks its parent, then its parent, all the way to the root of the file system. In every folder, it checks for AGENTS.md or CLAUDE.md.

And look at the final order. Global first, then the furthest folder, and the closest file comes last. Why last? Because the file closest to your project should have the final word. So if two files contradict each other, the one closest to your local repo wins. And Pi also dedups by path, so the same file is never loaded twice.

▶ diagram-10

Now why does Pi do this walk every single time it rebuilds the prompt? Because you can edit your CLAUDE.md in the middle of a session. Say on turn four the agent is using npm, and you open CLAUDE.md and write "use pnpm, never npm". On turn five, the prompt is rebuilt, the walk finds your edit, and now the agent uses pnpm. So no matter when you change the file, it's captured immediately.

Someone might ask, is there a limit on how many files it takes? No, there's no limit. So be careful. In one project, don't keep too many markdown files, otherwise you'll confuse the model.

And one honest point here. These files are Pi's only memory. Pi has nothing else. It relies on you, every single time, to keep these files up to date.

— — —

▶ diagram-11

Next we come to a very important thing, which is skills. Many people are really confused about skills, so let me make it simple.

A skill is one markdown file, SKILL.md. At the top it has a name and a description. That top part is called the frontmatter. Below that is the body, the actual instructions, which can be hundreds of lines.

Now, when you load the context, the body is never added. Only the name and the description go into the context. So it's your job to write the name and description well, because the LLM has to pick which skill to use based only on these two things. The full body is loaded only when that skill is selected.

Think of it like a trailer. The trailer is short, it tells you what the movie is about. You watch the full movie only if you want to. This is called progressive disclosure. You disclose the skill progressively, only when it's needed.

▶ diagram-12

Actually there are three levels. At startup, only the name and description, for every skill. When the skill is triggered, the body of SKILL.md. And if the skill refers to other files, like a reference file or a scripts folder, those are read only if that specific thing is needed. So a bundled file costs nothing until it is opened.

▶ diagram-13

Let me ask you this. What's the difference between a tool and a skill? A tool is how to do something. Read a file, run bash. A skill is more like what to do and when to do it. It's a procedure, a recipe. A recipe can call for many hands, but a hand never tells you the recipe.

▶ diagram-14

Let me give you an example of a skill I made myself. I was building a product with a writing agent. And whatever it wrote, it looked AI-generated. You know the classic signs, double dashes everywhere, words like "delve" and "honestly". I did not want any of this.

So what I did is, I gave my agent a few chapters from my own book, and I asked it to create a skill file. It came back with a file called writing-style.md. A name, a description, and a big list of rules. And now every time this agent runs, this skill is loaded. Next time I write a new book, a blog post, anything, I don't have to explain my style again. You write the skill once, and you use it for any number of tasks.

And this is my own philosophy. The core of a harness should be very small. The power comes from the skill files you write. Hermes takes a different approach, it ships with a lot of skill files already built in. Both are fine. But for your own product, the best skills will come from your own experience.

— — —

▶ diagram-15

So now the real question. How do you write a good skill file? This part is based on Anthropic's own guide on authoring skills. It's a very dense document, so I've made it visual.

First rule. Say less. The model already knows a lot. It knows what a PDF is, it knows what React is, it knows why Rust is fast. So don't write all that in your skill. Look here, the good one is about fifty tokens. The verbose one is a hundred and fifty, because it explains what a PDF is and why libraries exist. Cut that. If something is common knowledge, don't include it.

▶ diagram-16

Then the two required fields. The name, maximum sixty-four characters, only lowercase letters, numbers and hyphens, and you cannot use the words "claude" or "anthropic". And the description, maximum one thousand twenty-four characters, it must not be empty, and it must say what the skill does and when to use it.

▶ diagram-17

And the description is really how a skill gets found. There are only two ways the model finds a skill, the name and the description. So look at the good example. "Extract text and tables from PDF files, fill forms, merge documents." That's what it does. Then, "Use when working with PDF files or when the user mentions PDFs." That's when to use it. Most people only write the first half.

And the bad ones. "I can help you process Excel files." Always write in third person, never "I" or "you". And "helps with documents". Way too vague. If you have a hundred skills, how will the model pick this one?

▶ diagram-18

Same thing with the name. Name the skill after the activity. Processing PDFs, analyzing spreadsheets, managing databases. Never something vague like helper, utils, documents or tools.

— — —

▶ diagram-19

Now this next one is a bit non-intuitive. How much freedom should you give in the body?

Anthropic uses this nice picture. Some tasks are a narrow bridge, with a cliff on both sides. Only one path is safe. Like a database migration, or something very specific to your company. For these, give the exact script, and say "don't change it". Low freedom.

But some tasks are an open field. Many paths reach the goal. Like a code review. For these, just give the goal and let the model choose. And if you over-specify an open field, the skill actually becomes worse.

▶ diagram-20

Then, how long should a skill be? Generally keep the SKILL.md body under five hundred lines. If it becomes bigger, split it into other files in the same folder. Look at this pdf folder. SKILL.md is always read first. The other markdown files are read only when needed. And scripts are run, not read, so only their output costs tokens.

▶ diagram-21

But don't keep references two levels deep. If SKILL.md points to advanced.md, which points to details.md, that's difficult for the model to unearth, it may only skim the last one. Just keep everything one level deep, linked straight from SKILL.md.

▶ diagram-22

And this one, I found it to be the most useful, and not many people know about it. If your skill has many steps, give it a checklist. Step one, step two, step three. The model copies the checklist and ticks things off as it goes. A written checklist stops steps from being skipped. That's a vertical pattern.

The second pattern is a circle, a feedback loop. Make the change, run a validator, fix whatever it reports, and only continue when it passes. So the skill checks its own work. Not many people do this. The more feedback loops you have in your skills, the more robust your whole product becomes.

▶ diagram-23

And then, how do you even know your skill is working? Anthropic recommends writing the tests before the skill. Run the task without any skill, write down what failed, build a few test scenarios, write the smallest skill that fixes it, and run the tests again.

Let me tell you what I did. For my writing-style skill, I wrote about a hundred articles using that skill, and I passed all of them through an AI detection API. And I gave the instruction that the skill is not done until every article scores under five percent AI. Once that happened, I knew the skill was working. And notice, I defined that bar. That's the human's job. Don't just tell the model "design your own criteria".

▶ diagram-24

And one more simple idea. Use one Claude session to write the skill, and a completely fresh Claude session to test it. Claude B is not biased, it knows nothing about how the skill was written. Tell it to be very critical, and report everything that went wrong. Then improve the skill based on what actually happened. It's like a small competition, one writes and one judges, the same idea as GANs. Not many people do this, but it's so simple.

— — —

▶ diagram-25

And the last piece of the prompt, which looks very small. The current date and the working directory. If you say "schedule this email for tomorrow at the same time", the agent needs to know what today is. The model doesn't know what day it is. So the harness has to tell it. Many people forget this, but it's really important.

So that's part one. Nine things go into every call, only the conversation is compacted. Pi assembles its prompt fresh every call from five pieces. And skills use progressive disclosure, and a good skill is short, easy to find, and tested.

Now comes the part which I think very few people actually know, because not many people have opened the code of Pi and Hermes and compared them. Let's go.

---

## PART 2 — Compaction: Pi vs Hermes

▶ diagram-26

So let me ask you. If you were making your own harness, how would you do compaction? Pause the video and think about it.

Most people say something like, "when the context gets close to the limit, I'll use another LLM to summarize the past." Some people say sliding window, or throw away old tool results. These are good thoughts.

But if you go to an interview and someone asks you how compaction is done, and you only say "use another LLM to summarize", it tells them you have no idea how production harnesses are built. That is just level one. There are many more levels of depth.

Level two, when do you start compacting? If the context window is two hundred thousand tokens, you cannot start at two hundred thousand. You have to start some time before. But when exactly?

Level three, what about past messages and new messages? Do you treat everything the same way? How many new messages do you keep? How do you summarize the past?

Level four, where does the cut fall? The messages are user, assistant, tool call, tool result. What if the cut falls right between a tool call and its result? Then the fresh part starts with a tool result, and you have no idea what question was asked to get that result.

And level five, what if compaction itself fails?

So let's see how deep modern harnesses actually go.

▶ diagram-27

But first, one thing you should keep in mind. When you look at what takes up the context, the user message is usually very small. But the user might ask a ten-word question, the agent calls a tool, and the tool result is huge. Maybe a five-thousand-line error log. And that stays on the tape and is sent again on every later turn. This is a very common pattern in agent systems. Tool results take up most of the context. Remember this, because it explains one of the smartest things Hermes does.

— — —

▶ diagram-28

So let's first see how Pi does it. When does Pi compact?

Pi has a reserve, called reserveTokens, which is sixteen thousand three hundred eighty-four by default. So if the context window is two hundred thousand, Pi does not wait until you reach two hundred thousand. When the tokens you're carrying cross the context window minus this reserve, Pi decides it's time to compact.

Why keep the reserve? Because compaction itself needs some room. The model still has to write a reply on that turn. So you leave space for the answer.

▶ diagram-29

But let me ask you, how do you even measure the number of tokens in the context? How would a harness do this?

The way harnesses do it is through the API itself. Whenever the LLM provider answers, it comes back with something called a usage block. That tells you exactly how many tokens were used. So Pi finds the last assistant reply with a usage block. Everything up to that point is exact, that's called usageTokens. And anything that came after it, Pi estimates. Those are called trailingTokens. And the total is just these two added together.

▶ diagram-30

But even this has a small intricacy. Look at this example. These are the last few entries of a session, number twenty-one to twenty-eight. Pi walks backwards from the newest one, looking for the last assistant message with a usable usage block.

Twenty-eight is a user message, no usage. Twenty-seven is an assistant message, but this call was aborted halfway, it dropped for some reason. So it has no usage block. Can you tell me which message gives us the usable usage? Yes, number twenty-four. Up to that point the provider told us exactly, one lakh seventy-eight thousand nine hundred. And everything after it is estimated.

▶ diagram-31

And how does Pi estimate the trailing tokens? Some simple rules. For text, count the characters and divide by four. For a tool call, count the name plus the JSON arguments. And an image is always counted as four thousand eight hundred characters. And these estimates deliberately run a little high, so Pi compacts a little early rather than a little late.

So my point is, even estimating tokens is not easy. You have to think about cases like what if the provider returned an error.

— — —

▶ diagram-32

Now Pi knows it wants to compact. But what does it compact?

Pi has another setting, keepRecentTokens, which is twenty thousand. So it walks backwards from the newest message, adding up tokens, until it collects twenty thousand recent tokens. Those are never compacted, because recent messages carry what the user cares about right now. And everything before that, Pi summarizes.

▶ diagram-33

Up to here, it's easy to understand. But now pay very careful attention, because this is where you see the level of depth.

How do you know where to draw this line? What if the cut lands on a tool result? Then the past gets summarized, and the fresh part starts randomly with a tool result, and we have no clue what question was asked to get it. The API will actually reject this.

So what Pi does, very intelligently, is that it has a list of legal places to cut. You can cut at a user message, because a new chain starts there. You can cut at an assistant message too. But you never cut at a tool result. A tool result must always stay attached to the tool call that asked for it.

▶ diagram-34

And there is one more subtle thing. Pi asks two different questions about each message. Can we cut here? And does this message start a turn? A user message, yes and yes. A tool result, no and no. But an assistant message, we can cut there, but it does not start a turn. So that's exactly why a cut can land in the middle of a turn.

▶ diagram-35

So what happens if the cut lands in the middle of a turn? Pi makes two summaries. One is the normal history summary of everything before. And the second is the turn prefix summary, which captures what was asked at the start of this turn. Then both are joined into one summary message. Two LLM calls, one stored summary. So the model never loses the question it was in the middle of answering.

▶ diagram-36

And when you compact, what should the summary contain? Pi's summary always has the same shape. The goal, the constraints and preferences, the progress, done, in progress and blocked, the key decisions with why they were made, the next steps, and the critical context. And at the end, the list of files read and modified, which is added by code, not written by the model. A fixed shape, so the next model always knows where to look.

▶ diagram-37

So that's Pi end to end. It prepares the compaction, finds the cut point, summarizes with one or two LLM calls, and you get a new, shorter context. All of this is in Pi's compaction file, it's public. It's just very difficult to pull it out and teach it, which is why I made these pictures.

— — —

▶ diagram-38

Now if you think that was detailed, you'll be even more surprised by Hermes. It's really very different.

First, when does Hermes compact? Hermes has something called the effective window, which is the context length minus the maximum output tokens. And Hermes triggers compaction at fifty percent of this effective window. Fifty percent! Pi waits until it's near the edge. Hermes starts at half.

▶ diagram-39

And Hermes has even more edge cases here. First, there's a floor of sixty-four thousand tokens. It never triggers below that, so a small model doesn't compact while half its window is still empty. Second, if the window is under five hundred twelve K, it raises the trigger to seventy-five percent. And third, if the floor itself is bigger than the context window, like a thirty-two thousand model with a sixty-four thousand floor, that makes no sense, so then it uses eighty-five percent. I'm telling you all these details because this is how harnesses are actually built.

▶ diagram-40

Now the second major difference. What does Hermes keep? Hermes keeps the beginning as it is, the system prompt and the first three messages. It keeps the end as it is, about twenty percent of the trigger. And it only summarizes the middle.

Why keep the first three messages? Think about it. When a user starts a session, they're fresh. The first few messages usually tell you what they really wanted. In the middle, they might wander off, get distracted. So the first messages hold the actual intent. Pi does not retain the beginning. Hermes keeps the head and the tail.

▶ diagram-41

And now remember what I said, tool results take most of the space. Let me ask you, why do you think Hermes prunes old tool results, and Pi doesn't?

So before Hermes summarizes anything, it first prunes the old tool results. It rewrites them as short, descriptive lines. A tool result might have a thousand-line error message, but you maybe just need one line, like "ran npm test, exit zero, forty-seven lines". If the same file was read five times, it keeps only the newest copy. And old images are dropped.

And this is fully deterministic. No LLM involved. It costs nothing. So most of the space is won back before any model is even called.

▶ diagram-42

And the summary of Hermes is a lot more detailed than Pi. It has eleven sections. Historical task snapshot, goal, constraints, completed actions, active state, blocked, key decisions, resolved questions, relevant files, critical context, and pruned skills. And there's a nice safety rule, never write an API key into the summary, write "redacted" instead.

▶ diagram-43

So Hermes end to end. Prune the old tool results, free. Protect the head. Protect the tail. Summarize only the middle, that's the only expensive step. And next time, it doesn't start from zero, it updates the summary it already has.

— — —

▶ diagram-44

But Hermes does not even stop here. It has something called micro compaction, and I think it's a beautiful technique.

What Pi does is batch compaction. When you cross the line, everything is compacted at once. Micro compaction spreads the same work out. After every completed turn, the user, the assistant and the tool result, Hermes folds that one exchange into a rolling summary. So the summary keeps updating itself after every turn. And when you hit the limit, you don't have to summarize everything again, because it's already summarized. One note, in Hermes this is off by default. You have to turn it on.

▶ diagram-45

So if you plot the context size over time, for Pi it goes up, then a big drop, then up again. Like a sawtooth. And for Hermes with micro compaction, it stays almost flat. Same work, just spread differently.

Someone may ask, won't this cause issues with the KV cache, because the conversation keeps changing? That's a good question. Yes, every fold changes the conversation after the fixed part, so that part has to be computed again. We'll talk about the cache in a few minutes. I haven't seen this documented as a problem in Hermes, so I'd check before relying on it.

▶ diagram-46

And Hermes does one more thing. It also thinks about where compaction itself would fail.

First, the floor. What if your system prompt is huge, and you have a thousand tools? These parts are never compacted, so they alone might fill the window. Hermes knows this can happen.

Second, two strikes. If two compaction passes barely help, Hermes stops trying. It doesn't loop forever.

Third, cooldown. To summarize, you need an LLM. What if that LLM is rate limited? Hermes waits six hundred seconds, ten minutes, and tries again.

And fourth, fallback. If the summary model is not available, it tries an auxiliary model, then the main model. And if no model is available at all, say your API bill is not paid, it builds a summary with no model at all, just using character budgets. Because compaction has to produce something.

— — —

▶ diagram-47

So let's put Pi and Hermes side by side. When do you compact? Pi keeps a fixed sixteen thousand three hundred eighty-four tokens. Hermes uses a percentage of what's left. Pi reserves a constant, Hermes reserves a proportion.

▶ diagram-48

Where do you cut? Pi picks a legal cut point and summarizes a split turn separately. Hermes cuts by token budget, and then moves the cut until the tail is valid. Pi chooses a safe boundary, Hermes repairs the boundary it took.

▶ diagram-49

The shape of the summary. Pi has six sections, Hermes has eleven. Both keep the decisions, Hermes also keeps the working state. And Claude Code has its own shape too.

▶ diagram-50

And the attitude to failure. Pi just retries. Hermes has four separate guards. Remember, we are talking about production harnesses. If a user never sees compaction, it simply has to work. And I think this is one of the reasons Hermes has become so popular. They have thought about these edge cases very well.

---

## PART 3 — DeepSeek Harness, and the cache

▶ diagram-51

Now there's a third harness I want to show you. DeepSeek also has an open source harness, called DeepSeek Harness. And its big idea is about where compaction even lives.

In Pi and Hermes, compaction is built inside the harness. In DeepSeek Harness, the core loop is kept small, and compaction is a plugin. The loop just has a socket called ctx.compaction, and you plug an engine into it. The basic engine is a package called dsh-compaction-basic. There's an optional tool result pruner, which trims big tool outputs first, which is the same idea as Hermes' free step. And there's a command package that gives you a slash compact command. So if you want a different summarizer, you swap the plugin. You don't touch the loop.

▶ diagram-52

The second idea is even more interesting. In DeepSeek Harness, compaction never deletes anything. Every session is an append-only log of events. Things are only added, never removed. What the model actually sees is derived from that log. When compaction happens, it does not delete old events. It only changes what the model sees. One summary replaces a range of old messages, and the recent messages stay as they are.

So compaction is lossy for the model, but not for you. If you ever need the exact old text, you can read it back from the log.

▶ diagram-53

When does DeepSeek Harness compact? It uses two limits, and whichever comes first wins. One is eighty percent of the window. The other is the window, minus the output cap, minus an extra headroom of sixty-five thousand five hundred thirty-six tokens. And after compacting, it keeps the newest sixteen percent word for word.

Look at this table. For a two hundred thousand token model, the headroom rule fires first. For a one million token model, the eighty percent rule fires first. So you could say it's Pi's fixed reserve and Hermes' percentage, both at the same time.

▶ diagram-54

And the pipeline. There are two triggers. One is pressure, checked before the request is built. The other is overflow, when the provider actually comes back with an error saying the context window is exceeded. Both go into the same pipeline. First, prune tool results, which is free. Then measure again. If it fits now, skip the summary completely, that saves a whole LLM call. If not, make one summary call.

And there's a clever detail here. That summary call replays the same system prompt and tools, so that the provider's cache stays warm. We'll see why that matters in a minute. For an overflow, it retries only once. And if the summary fails, it just logs a warning and carries on with the full history. It doesn't crash.

▶ diagram-55

And DeepSeek's summary also has a fixed shape, eight sections. Primary request and intent, key technical concepts, files and code, errors and fixes, pending jobs, current work, next step, and critical context. And the model is told, this is a checkpoint, continue, and don't acknowledge it. So the model doesn't stop and say "thanks for the summary".

▶ diagram-56

So here are all three side by side. Same five questions, three different answers. There's no single right design. There are only trade-offs.

▶ diagram-57

And one small thing about the DeepSeek model itself, because context management doesn't only live in the harness. In the DeepSeek V3.2 paper, they describe how the model treats its own thinking during tool use. While tool results keep coming, the thinking is kept. But when a new user message arrives, the old thinking is dropped, and the tool calls and results stay. And for their search agents, they also tried a very simple strategy when the context is nearly full, just throw away all the tool history and keep the original question. And simple things like that worked really well.

— — —

▶ diagram-58

Now since we're talking about the cache, let me talk about something which doesn't get talked about often. Prompt caching.

If you think about it, what we're doing is pretty wasteful. Every single turn, we re-send the entire conversation, the system prompt, every tool schema, every earlier turn, just to add one new tool result at the end and ask "what's next?" The model is stateless, so yes, it needs the whole thing. But the beginning is the same every time.

So the provider can keep the work it already did. On the server side, the cache is stored. And you mark where caching starts with something called cache control.

How does this save cost? People who know inference will understand this. There are two phases, prefill and decode. In prefill, the model computes the key and value vectors for every input token. For the cached part, those are already computed. So you don't pay to compute them again, and the first token comes much faster. That metric is called TTFT, time to first token.

And one more term, TTL, time to live. That's how long the cache is kept. For example five minutes, or one hour. Different harnesses support different TTLs, Pi for example supports the one hour TTL. So even if the provider caches automatically, your harness should say where the breakpoints are and how long to keep them.

▶ diagram-59

Now connect this to compaction. When you compact, the system prompt and tools stay cached, because they didn't change. But the summary is new, and the recent messages have to be computed again. So every fold costs you one cache miss.

So two simple rules. Keep the system prompt and tools stable, and at the front. That's exactly why DeepSeek Harness replays them in its summary call. And if you fold every single turn, like micro compaction, you get a cache miss every turn. That's the price of a flat line.

---

## PART 4 — Building compaction into Zill

▶ diagram-60

Okay, so we've seen how the best harnesses do it. Now let's build our own.

Pi and Hermes have thousands of lines for this. But the idea of Zill is to build a minimal harness, so we are going to keep it very simple and keep only the core idea.

So here's what we do. When the tape goes over budget, we cut it into two halves. The last six messages, we keep them exactly as they are. We call this number KEEP_RECENT. And everything older than that, we send to the language model in one call, and it writes a summary. So the new tape is just one summary message, and then the last six messages.

To estimate tokens, we use the same simple rule Pi uses, four characters per token.

And we also borrow three cheap ideas from what we saw today. From Hermes, we copy the user's original request word for word into the summary, so it never gets lost, no matter how many times we compact. Also from Hermes, we clip the big tool results before sending them to the summarizer, because they are the bulk. And from Pi and Hermes, our summary has fixed sections, goal, constraints, progress, decisions, files, errors and next steps.

▶ diagram-61

But our simple cut has exactly the same problem we saw in Pi. Look here. "Keep the last six" doesn't know anything about tool calls and results. So the cut can fall right between "write four.txt", the call, and "Wrote four.txt", the result.

And after the fold, the kept part starts with a tool result whose call was summarized away. An orphan. And the API will reject it.

The fix is just one line. While the kept part starts with a tool message, drop it. And notice, we don't invent a fake call to match it, because that would be lying to the agent about its own past. Dropping it is safe, because its meaning is already inside the summary. It's the same rule as Pi's "never cut on a tool result", just done the cheap way.

▶ diagram-63

So this is what we're building today. One new file, context.py. It has the two constants, and a few small functions. estimate_tokens, which is our meter. render, which turns the old messages into a plain transcript. compact, which does the fold. mend, which fixes that orphan problem. And a fallback summary that needs no model at all, Hermes' last resort, in case the summarizer is down.

In loop.py we add one small socket called before_turn. Before every model call, the loop hands the messages to this function and uses whatever comes back. That's how compaction plugs in. A bit like DeepSeek Harness, the loop doesn't even need to know that compaction exists.

Then a test file with a fake model, so the tests don't need the internet. And a demo with a budget of only fifteen hundred tokens. That's absurdly small on purpose, so we can actually watch compaction happen in front of us.

— — —

So let's build it. Open Claude Code inside your Zill repo, and paste this prompt.

*[Paste the prompt below. It's also saved as `zill-lecture4-build-prompt.md`.]*

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

While this is running, let me show you a few things in the prompt.

See, the first thing it says is that today we add one file and one socket, and nothing else. A good prompt keeps the change small, so you can actually review every line of it.

Second, look at the rules inside compact. "Return a new list, never change the input." And, "if the result is still over budget, return it anyway, one fold per call, never a retry loop." That's exactly Hermes' lesson. Compaction is allowed to fail, but it's never allowed to loop.

And third, look at the end. It tells Claude Code what "done" looks like. The tests pass, the demo compacts at least once and prints PASS, and with a huge budget it never compacts and still passes. And if something can't be verified, it has to say so honestly.

▶ diagram-62

Okay, so it's done. Now let's run the demo with the small budget.

```bash
python demos/context_demo.py
```

So look at the counter. Turn one, a few hundred tokens. Then it climbs. Nine hundred, thirteen hundred, sixteen hundred... and there. "Compacted." The number drops. That dip is Zill writing its own recap. It just replaced the whole history with one paragraph.

And look, the task keeps going. It writes four.txt, five.txt, then MANIFEST.md. And at the end, PASS. The task never even noticed that its history was folded. This is exactly the sawtooth from the picture. Climb, fold, climb, fold.

Let me scroll up and show you the summary it wrote. "Original request, verbatim." The whole task, word for word. Then the files created, one, two, three. The decisions. And what's left to do. Exactly what a colleague would want in a handover note.

Now let's run it once more with a huge budget.

```bash
python demos/context_demo.py 100000
```

Now it never compacts, and it still passes. So compaction doesn't change what the agent does. It just lets the agent keep working past its own window.

— — —

▶ diagram-64

So let me leave you with the one thing I want you to take away from today.

It's not enough to know the components of a context. That's only the start. If you're designing your own harness, compaction really comes down to three decisions.

When do I compact? A fixed reserve like Pi, a percentage like Hermes, or both like DeepSeek.

How do I compact? What do I keep exactly, where does the cut fall, and what can I prune for free.

And what does my summary look like? Which sections must always survive.

And if you're going to production, one more. What happens when compaction itself fails?

For homework, three things. One, run the demo with a small budget and actually read the summary Zill wrote about itself. Find one thing it dropped that you think was important, and change the summary instruction so it keeps it. Two, play with the numbers. Change KEEP_RECENT from six to two, and then to twelve. Change the budget. See how often it compacts and whether the task still passes. And three, Pi and Hermes are not the only ones. Codex does compaction in yet another way, and it's public. Go through it, and ask the same questions. When, how, what, and what if it fails.

Thank you so much for watching, and I'll see you in the next lecture.

---
---

## Notes for you (not spoken)

**Picture order:** 01 → 59 in order. Then 60, 61, **63**, the build, then **62** while the demo runs, then 64. All pictures are in `diagrams-lecture4/`.

**If the video is too long:** cut the DeepSeek model paragraph (diagram 57), the KV cache question under diagram 45, and diagrams 20–21. Or split into two videos at the end of Part 1.

**Check before recording:**
- Pi numbers (16,384 reserve, 20,000 recent, the 4,800 image estimate, split-turn budgets) and Hermes numbers (50% / 64k floor / 512K → 75% / 85%, first 3 messages, 20% tail, 600 s cooldown, 11 sections, micro compaction off by default) come from your book. Check them against the current code.
- DeepSeek Harness numbers (80%, 65,536 headroom, 16% kept, retry once, 8 sections) come from the `dsh-compaction-basic` README in `deepseek-ai/deepseek-harness`. Re-read it once, since defaults change.
- "Pi supports the one hour TTL" is from your transcript. Check it in Pi's code.
- **Run the build prompt once before recording**, so the demo you show on camera is real.
