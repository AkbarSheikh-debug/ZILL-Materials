# Harness Engineering Series — Lecture 2: The Loop

**Speaking script, spoken-voice version.** Lecture 1 covered prompt, context, harness, loop and graph engineering. This lecture opens the harness and builds its first component.
Read the normal text aloud. Lines in `[brackets]` are cues for you and are not spoken.
Diagrams: `diagram-01.png` … `diagram-17.png` (1920×1080), in two styles — `diagrams/` (hand-drawn) and `diagrams-pro/` (clean). Same numbers in both.

Rough length: 25–30 minutes of speaking, plus the live build.

---

# PART A — Opening the harness

## 1. Welcome — and which loop are we talking about?

Hello everyone, and welcome back to the Harness Engineering series. This is lecture number two.

So in the last lecture, if you remember, we looked at five terms. Prompt engineering, context engineering, harness engineering, loop engineering, and graph engineering. And we saw how each one sits inside the next one, right?

Now in this lecture, we are going to go inside the harness. We are going to open it up, see what components it is made of, and we are going to start building our own harness. From scratch.

And the first component which we are going to look at today is called the loop.

Now wait. Some of you will immediately say, "But you already taught us loops in the last lecture. Loop engineering." So let me clear this up right at the start, because otherwise it is going to create confusion later.

The loop which I talked about in the last lecture, loop engineering, that is the bigger loop. That one sits outside, around the agent.

The loop which we are looking at today is a different thing. It is a very small loop, and it sits inside the harness itself. Every time you type one message into Claude Code or Cursor, this is the loop which is running inside. The model thinks, it takes an action, it looks at the result. Then again it thinks, takes an action, looks at the result. This is called the ReAct loop. Some people also call it the agent loop.

So in this lecture, whenever I say "loop", I am talking about this small loop inside the harness. Okay? Just keep that in mind.

And one more thing. I will be using "agentic harness" and "harness" interchangeably. Both mean the same thing. So from now on I will just say harness.

---

## 2. The five elements of a harness

So before we get into the loop, let me first formally introduce the elements of a harness. There are five of them.

`[SHOW diagram-01 — the pyramid]`

And you can actually arrange them like a pyramid, as you can see here.

At the bottom I have the loop. Then on top of that I have tools. Then I have context and memory. Then durability. And then right at the top, orchestration.

And the way I like to remember these is that each layer is answering one question.

The loop is answering: how does a thought become an action?
Tools: what is the agent allowed to touch?
Context and memory: what does the model actually get to see?
Durability: if something crashes in between, what survives?
And orchestration: how do multiple agents work together?

We are going to build all five of these, step by step, one layer at a time. And at the end we will put all of them together, and we will have our own complete harness.

And I have given a name to our harness. I am calling it **Zill**. So whenever I say Zill, that is the harness which we are building in this series.

So today we are doing only the bottom layer. The loop.

Now why are we starting from the loop? See, take any element. Take gold, or silver, or lead. If you keep on breaking it down, finally you will reach a single atom, right? You cannot go smaller than that.

It is very, very similar for a harness. If you keep breaking a harness down, the smallest thing you will reach is the loop. So the loop is the atom of a harness. You can also call it the heartbeat of the harness. Without this, there is nothing. There is no harness.

So that is what we are going to understand today, and that is what we are going to build today.

---

## 3. My philosophy — small harness, detailed skills

Now before going ahead, I want to share my philosophy behind building this harness. And many of you might choose to follow a different philosophy later on. That is completely fine.

`[SHOW diagram-02 — small harness + skill files = real products]`

If you look at the open-source harnesses which are out there today, you will see that they are huge. Even the ones which people call "minimal" — if you actually open the code, it is still tens of thousands of lines. Sometimes much more than that.

And there is a reason for that. These are production-level systems. They have written gateways for different model providers, they support many platforms, they handle many edge cases. So naturally the code becomes big.

But my thinking is a bit different. My thinking is that your harness can be very, very minimal. Something like a thousand lines of Python. And with that minimal harness, you can still build serious products.

Then you will ask me, "If the harness is so small, then where is the quality coming from?"

What I am betting on is the skill files. The human contribution should go into the skill files. So the harness itself stays small and simple, but the skill files have to be a lot more detailed. How exactly you want the front end to be built, which design system to follow, how the testing should be done — all of that, you write down in detail in the skill files.

So, small harness, very detailed skill files. That is the whole idea behind Zill.

And if this works, then it means that all of us, every one of you watching this, can build your own harness. Not just use somebody else's. Actually build your own.

---

## 4. Why build your own at all?

Now there is one question which always comes up here, and it is a good question. "Beyond learning, what is the actual benefit of building my own harness? Claude Code is already there. Codex is there. Cursor is there."

So I have two answers for this.

The first one is this. When you use these tools every day, slowly you start feeling that some kind of magic is happening inside. And once you feel it is magic, you become dependent on it. What I want to show you in this lecture is that this "magic" is basically ten lines of code. And once you see that, you cannot go back. You stop looking at these tools as a user, and you start looking at them as an engineer.

And the second one is independence. If you understand how the harness works, you are not locked into one company, or one model, or one pricing. Suppose tomorrow the tool which you are using becomes very expensive. You are not stuck. You take your own harness, you connect it to some other model, and you continue your work.

So we are not building Zill because the world needs one more harness. We are building it so that you know that you can.

---

# PART B — The loop, in detail

## 5. A model, on its own, cannot do anything

All right. So now let me start explaining the first element. The loop.

And to understand why we even need this loop, I first have to tell you something which may sound a bit strange.

`[SHOW diagram-03 — the model is a function]`

A language model, by itself, cannot do anything.

It cannot open a file. It cannot run a command. It does not remember what you told it yesterday. It cannot even check its own work.

Then what can it do? Only one thing. See, a language model is basically a function. You give it a list of messages as input, and it gives you one message as output. That's it. After that, it stops.

So suppose you tell a bare model, "Please delete this file." What will happen? Nothing will happen. It will write some text saying, "Okay, I will delete the file." But the file is still sitting there on your computer. Nothing has changed. It is just some text.

The way I like to think about it is this. Imagine there is a genius, and this genius is locked inside a room. No windows, no phone. There is only a small gap under the door. So you can slide a note inside, the genius reads it, writes a very good reply, and slides it back to you.

Now this genius can tell you exactly what needs to be done. "Open the test file, I think the problem is on line twelve." But the genius cannot come out of the room and open the file. Somebody who is outside the room has to do that.

That somebody is the harness.

---

## 6. So what is a harness?

So now we can define the harness properly.

`[SHOW diagram-04 — the harness around the model]`

The harness is everything which is around the model. And if you look at this diagram, it is doing three jobs.

The first job is to assemble. It puts together whatever the model is going to see. So it is preparing that note which goes under the door.

The second job is to execute. Whatever the model asks for, the harness actually does it. It opens the file, it runs the command, it calls the API. So the harness is the hands.

And the third job is to repeat. It takes the result, brings it back to the model, and asks, "Okay, what next?"

So the model is giving the judgment. And the harness is giving the hands, the memory, and the persistence.

And if you think about it, "harness" is actually a very good name. Think of the harness which you put on a horse. The harness is not making the horse strong. The horse is already strong. The harness is what makes that strength usable.

One more point here. Many people say, "Models are getting better every month, so very soon we will not need all this." Actually, it is the other way around. A stronger model will ask for more actions, it will work on longer tasks, it will touch more files. So the load on the harness goes up. It does not come down.

And things like your laptop crashing, or the context window getting full, or a dangerous command getting executed — these problems are not inside the model. No better model is going to fix them. They have to be handled by the harness.

---

## 7. The heartbeat: thought, action, observation

Okay. So now let us see how the model and the harness actually talk to each other. And this is the heartbeat which I was talking about.

`[SHOW diagram-05 — the ReAct triangle]`

There are three things happening here.

First there is a thought. The model looks at the situation and decides what to do next.

Then there is an action. The model asks for a tool, and the harness runs that tool.

And then there is an observation. Whatever came out of that tool goes back to the model, and the model sees it.

And then again it goes around. Thought, action, observation. Thought, action, observation.

This is called the ReAct loop. Now some of you might be thinking of React, the web framework. No, no, it has nothing to do with that. Here, ReAct stands for reasoning and acting. Re-Act. The name comes from a very nice research paper which came out in 2022. I will put the link to that paper in the description.

`[SHOW diagram-06 — one task, six laps]`

Let me take an example, so that this becomes very clear. Suppose I tell my agent, "There is an issue in my GitHub repository. Please fix it."

Now see what happens.

The first thought is, "I have to look at this issue." So the action is that it uses the GitHub tool to fetch the issue. And the observation is, "Okay, I have got the issue."

The next thought is, "Now I need to read the code." So the tool it uses is the read tool. And the observation is the contents of that file.

Then the thought is, "Okay, I have found the bug, let me fix it." The action is the edit tool. The observation is, "The file has been edited."

Then the thought is, "I need to verify this. Did my fix actually work?" So the action is to run the tests. And the observation is, "All the tests are passing."

Then the thought is, "Now I will create a pull request." Again it uses the GitHub tool. The observation is, "Pull request created successfully."

And then finally the thought is, "There is nothing left for me to do." So this time it does not call any tool. It simply gives the final answer, and it comes out of the loop.

So did you see what happened here? It went through this thought-action-observation loop multiple times.

And notice, I never told it that this task has six steps. I did not write step one, step two, step three anywhere. At every step, the model itself decided what to do next, based on what it had just seen. And the model itself decided when it is done.

By the way, this action part is also where a lot of agent mistakes come from. If you give the model five hundred tools which it does not need, it gets confused, and it does not know which tool to pick. Just keep that in mind. We will come back to it in the next lecture, when we build the tools.

So next time when you open Claude Code, or Cursor, or Codex, and you see it saying "reading this file… editing… running tests…", now you know what is going on inside. It is this same loop. Thought, action, observation. Running again and again.

---

## 8. The model has no memory — the messages array

Now here I have to break one misconception. And honestly, if you take only one thing from this lecture, take this one.

`[SHOW diagram-07 — the growing array]`

The model does not have any memory.

When I talk to people, most of them think that the language model remembers the whole conversation. That is not true. Every single time we call the model, it starts completely fresh. It does not remember your previous question. It does not remember the file which it read ten seconds back. It does not remember its own plan.

Then you will say, "But when I am chatting with it, it clearly remembers everything I said!"

It doesn't. Somebody else is doing the remembering for it.

Think of it like this. Suppose you have a very brilliant colleague, but this colleague forgets everything every few seconds. How will you work with such a person? There is only one way. You keep a diary. And before asking any question, you read out the entire diary to them, right from the first page. Then they answer. And then you write that answer also into the diary.

In our case, that diary is called the messages array. It is just a list. Nothing more than that.

Now look at this diagram. In the first call, the list has the system prompt and the user's question. This goes to the model.

The model replies, "Let me read the test file." The harness runs that tool and gets the file contents. And both of these things get appended to the list.

In the second call, we send the whole thing again. The system prompt, the user's question, what the model said, the tool result. Everything.

In the third call, the list has grown further, and again we send the whole thing.

So the memory is not inside the model. The memory is this list, and it is the harness which is sending this list again and again, on every call.

And once you see it like this, things become very simple. If you append something to the list, the agent remembers it. If you delete something from the list, the agent forgets it. That's all. And later in this series, when we do memory, compaction, resuming a session — all of those are nothing but careful editing of this one list.

And there is a very practical use of this also. Suppose your agent is on turn number forty, and you want to know what all it knows at that point. You don't need any special tool for that. Just print the list. Whatever is in that list, that is everything the agent knows at that moment.

---

## 9. Three roles in the array

Now let us open this list and look at one single entry.

`[SHOW diagram-08 — three voices]`

Every message is a very small thing. It has a role, which tells you who is speaking. And it has content, which is what was said.

And there are only three roles.

The first one is system. This has the standing instructions — who the agent is, which tools it has, how it should behave. It is written once, and it sits right at the top.

The second one is user. This is anything which is coming from outside.

And the third one is assistant. This is the model's own voice. Whatever text it writes, and whatever tools it asks for.

Now here is the part where most people get confused.

When a tool runs and gives back a result — let's say the contents of a file — that result also goes to the model as an input from outside. Just like a user message. No human has typed it. A program has produced it. But for the model, it is coming in through the same door.

So think of it like this. The model has one mouth and one ear. The mouth is the assistant role. And everything else comes in through the ear. And the ear cannot make out whether it is a human speaking or a program. A person typing something, the contents of a file, the output of a command — for the model, all of it is just input.

Later, when we write our own code for Zill, we will tag these messages as "tool", just so that our code is easier to read. But the idea stays the same. It is the outside world talking to the model.

---

## 10. What a turn is, and the tax you pay

Now let me define one word properly, because people use it very loosely. The word is "turn".

One turn is one call to the model, plus whatever tool work comes out of that call. So call, act, append. That is one turn. One thought-action-observation.

A simple question may finish in one turn. Something like "fix the failing test" may take six.

Now let us think about the cost of this.

`[SHOW diagram-09 — the bars climbing]`

Let's start at time equal to zero, before anything has happened. Even at that point, the messages array is not empty. It already has the system prompt. It has the list of tools. It has your skill files. It has your CLAUDE.md or AGENTS.md file. Then the user's question gets added. And all of this is sent to the model.

In turn two, all of that is sent once again, plus whatever happened in turn one.

And by the time you reach turn forty, you are paying to re-read everything from turn one to turn thirty-nine.

Look at the bars here. The yellow portion on top is the new work which happens in that turn. It is the same size every time. The grey portion below is everything which is being read again. And you can see, it just keeps on growing.

So this is the tax which you have to pay, every single time. In practice, an agent reads a lot more than it writes.

That is why you have to build your context very carefully. People put five hundred tools into a project "just in case", and that only confuses the model. Or they paste a forty-thousand-line log, when the last two hundred lines would have been enough. Whatever you leave in that list, you keep paying for it again and again.

We have one full lecture on this later in the series. For now, just keep this idea at the back of your mind.

---

## 11. How a tool call finds its result

One small thing more, and then we will go to the actual loop.

`[SHOW diagram-10 — the ticket]`

When the model asks for a tool, it does not simply say "read the file". It sends a small structured request. That request has a name, which is which tool it wants. It has the arguments, like which file. And it has an id.

Now what is this id for? Think of a busy restaurant counter. You place your order and they give you a token, say token number seventeen. When your food is ready, they call out "seventeen", and that is how you get your food and not somebody else's.

The id is exactly that token. The model is saying, "Here is a job, token A-seventeen." And when our harness sends the result back, it puts the same token on it. A-seventeen.

So two rules come out of this.

Rule number one. Every request should get exactly one result. If the model has asked for three tools, it should get back three results. Not two. If even one request is left without an answer, the list is broken, and the next call to the model will simply fail with an error.

Rule number two. In one turn, there can be more than one request. The models today very often ask for three files at the same time. So our loop has to go through each request and answer every one of them.

Remember rule number one. Later in the series, when we come to durability, you will see that some of the worst bugs come from exactly this — the program crashes after the request got saved, but before the result got saved.

---

## 12. The loop, derived

Okay. So now we have everything we need. Let us put the whole loop in one picture.

`[SHOW diagram-11 — the loop, derived]`

And as we go through this, I want you to notice one thing. We are not really designing this loop. We are getting forced into it, one step at a time.

First look at the left side. This stack is our messages array. System, user, and whatever gets added after that. It grows in every lap. And as we just saw, this list is the memory.

Now just follow the numbers.

Number one. We call the model, and we pass the messages to it. That is this box, call model.

Number two. The model gives a reply, and we ask only one question: did it ask for a tool?

If the answer is no, that means the model has just given us normal text. And that is the only way the model has of telling us, "I don't need anything more. Here is my answer." So we go down this red arrow, we return the answer, and we are out of the loop.

If the answer is yes, then we cannot return yet, because there is some work to be done.

So number three. Our code runs each tool. And look at what is written in this box — *our* code. Not the model. The model cannot run anything. It can only ask. It is the harness which actually runs it.

Now at this point, we have something in our hand which the model has not seen yet — the result of that tool.

So number four. We append that result to the messages. So this stack on the left becomes one block taller.

And number five. We go back to number one. We call the model again, and this time the model can see the result. And it decides again what to do.

That is the complete loop. Call, check, run, append, and repeat.

Now look at this note in the corner, because this is really the main point. Nobody designed this loop. It is forced by what the model cannot do. The model cannot act, so we have to act for it. Once we act, we know something which the model does not know, so we have to show it to the model. And the moment we show it, we are back where we started. So every step is coming out of the step before it.

And one last thing in this picture, at the bottom left. Max turns. This is our safety brake. If the model gets stuck and keeps going round and round, we stop it at a fixed number, we ask it for a short summary, and we exit. I will come back to this in a few minutes.

---

## 13. The loop, in about ten lines

And now here is the same thing in code.

`[SHOW diagram-12 — the code]`

Let us read it together.

We have a function called run loop. It takes the messages, the tools, and the maximum number of turns.

In every turn, first we call the model. That is the thought.

Then we append the reply to the messages, so that it is remembered.

Then we check. If there are no tool calls in the reply, we return the text, and we are done.

Otherwise, for every tool call which is there in the reply, we run the tool — that is the action — and we append the result — that is the observation.

And if we run out of turns, we ask for a wrap-up and come out safely.

Now count the lines. It is about ten lines.

`[PAUSE — let it sit on screen for two seconds]`

That's it. This is the heartbeat of every coding agent. It is as small as this. Claude Code, Cursor, Codex — at the core, all of them have this. The tools, the permissions, the memory, the sub-agents, all of that is built around these ten lines.

Most people think that agents work because of some deep magic which is inside the model. It is not that. It is a loop which is around the model. A loop which keeps calling a function that has no memory, and keeps telling it what happened.

And once you understand this, the whole subject looks different. We are not studying something mysterious. We are studying a loop.

---

## 14. Who decides when it is done?

Now let me show you why this small loop is so powerful. And it really comes down to one question: who decides when the work is done?

`[SHOW diagram-13 — workflow vs agent]`

See, there are two ways in which you can make a model do a multi-step task.

Look at the left side first. This is called a workflow. Plan, step one, step two, step three, done. Now who wrote these steps? You wrote them. The plan is fixed, and it was written beforehand. You are the one who decided that there will be three steps.

And that works fine, as long as you already know what the task looks like. But the moment the task is unpredictable, it breaks. What if two steps were enough? What if this particular bug needed five steps? A workflow cannot change its path. It does not take any decisions in between. It just follows whatever you have drawn.

Now look at the right side. This is an agent. Here there are no numbered steps at all. There is only a loop, going round and round. And see what is there in the middle — a steering wheel. Because in an agent, it is the model which is sitting in the driver's seat.

In every lap, the model decides: should I act again, or should I stop? And the number of laps is not written anywhere. It depends on the task. A small fix may take two laps. A messy one may take fifteen.

And this red arrow in the middle is the main idea. This is called inversion of control. The exit condition has moved. It has moved out of your code, and it has gone into the model.

So in a workflow, you decide when it is done. In an agent, the model decides when it is done. That is the whole difference between the two. And that is exactly why an agent can handle open-ended tasks — the kind of tasks which you could never write a script for in advance.

Now, if you are handing the steering wheel to a model, you should be a little bit nervous. And that is correct. Sometimes the model gets stuck. It keeps reading the same file again and again, and it never says, "I am done."

So to prevent this kind of infinite loop, we keep one brake. That is max turns. It is just a counter. If the loop reaches that number, we stop it, whatever is happening. But we don't just crash. We make one last call, without any tools, and we tell the model, "You have run out of turns. Summarise where things are." So the person sitting there gets a status report, and not an error.

So remember this one rule: never end a run without a report.

And one more thing. Suppose a tool fails in the middle. We don't crash the loop for that also. We simply put the error message into the result and give it back to the model. And many times, the model reads the error and fixes the problem on its own.

---

## 15. A skill is not a tool

Before we move on, there is one confusion which I want to clear, because a lot of people mix this up. Skills and tools.

`[SHOW diagram-14 — skill vs tool]`

A tool is code. It is a function which the harness can run. It does one specific thing — read a file, run a command. It has a name, and it has arguments.

A skill is a document. It is written in plain language, and it explains how to do some job, step by step. Something like, "This is how we build the front end in this project. Use this design system. Follow these steps in this order."

So think of a kitchen. The tool is the knife. The skill is the recipe. The recipe may tell you which knife to use, but the recipe is not the knife.

So a skill may mention some tools inside it. For example, your front-end skill file may say, "Use the Figma tool for this." But a skill is not a tool. Don't confuse the two.

Now here is a small question for you. Suppose you have a template for your front end, and you want your agent to always follow that template. Where will that go inside the messages array? Just think about it for a second.

`[PAUSE]`

It will go into a skill file. And that skill file gets added to the messages array, as part of what the model sees. That is why this whole system is so modular. You don't touch the harness. You just change the instructions.

---

# PART C — Now we build it

## 16. The three pieces of a bare harness

So I hope the loop is now clear to all of you at a fundamental level. If you had any confusion or any misconception about it, I hope all of that is cleared now.

Now we are going to start building. But before that, let me put everything which we discussed today into one single picture.

`[SHOW diagram-15 — three pieces of a bare harness]`

The simplest harness you can make — what I call a bare harness — has only three pieces.

Number one, at the top, is the model client. Its job is just one line: send the messages, and get a reply. And this is the only piece which talks to the model company.

Number two, at the bottom left, is the message array. System, user, assistant, tool, and so on. Every new message gets appended here, and this is what keeps the history across turns. And look at the red note. This list *is* the agent's state. There is no other state hidden anywhere else.

Number three, at the bottom right, are the tools. Each tool is just a name, a schema which describes its arguments, and a function. For example, a read-file tool is just two or three lines of normal Python.

And in the middle, connecting all three, is the loop. Send, check for a tool, run, append, repeat.

Now read this box at the bottom along with me. Client, plus message array, plus tools, spun in a loop, is equal to an agent.

That's all an agent is. And this is exactly what we are going to build now.

---

## 17. The provider — one doorway to the model

Let us take the first piece, the model client. Somebody has to actually send our list to a model, right? In Zill, that is one file, and we call it the provider.

`[SHOW diagram-16 — provider.py]`

The provider does four things.

One, it authenticates. It holds the API key.

Two, it translates. Inside Zill we keep our own simple message format. The provider converts that into whatever format the model company wants, and it converts the reply back into our format.

Three, it retries. Networks fail, rate limits get hit. So the provider waits for a bit and tries again.

Four, it normalises. Whatever comes back from the model, it turns that into one clean shape: some text, maybe some tool calls, and the token count.

Now why are we putting all of this in one file? There is one big benefit. Suppose tomorrow you want to move from Gemini to Claude, or to OpenRouter. You change only this one file. The loop does not even come to know. Nothing else in the harness has to change.

So think of it as the one door of the house. Every model company has its own small peculiar requirements. All of those stay at the door. They don't spread into the rest of the house.

---

## 18. Let us build it

Okay. So now let us build.

`[SHOW diagram-17 — what we build today]`

Today we are going to write only two files. One is provider.py, which is the door. And the other is loop.py, which is the heartbeat. And along with that, one very small demo with a deliberately silly tool — a dice roller — so that we can see the whole cycle running without touching any real files.

And we are not going to type this code by hand. That time is gone. What we are going to do is write a good prompt, give that prompt to a coding agent, and the coding agent will build the harness for us. You can use Claude Code, you can use Codex, you can use any open-source agent. Anything is fine.

You need to keep two things ready.

First, an API key for some good model. If you don't have one, a free Gemini API key is fine to begin with. And please, don't paste your key directly into the prompt. That is not good practice. Put it in a small .env file, and just mention in the prompt where that file is.

Second — and this is the fun part — you need a name for your harness. I am calling mine Zill. You can also use Zill and follow along, or you can give your own name. It is your harness, so call it whatever you want.

`[SCREEN: switch to the terminal, open the coding agent]`

So this is the prompt which I am giving.

`[SCREEN: paste the prompt below — read it out section by section as it appears]`

```text
You are building the first part of Zill (lecture 2 of the series), a minimal agentic harness in Python.
Standard library only, no third-party packages, Python 3.10+.

Setup
- Create a project folder named zill-harness and run git init.
- Add a .gitignore covering __pycache__/, *.pyc, .env and .DS_Store.
- All harness code lives in a package folder named zill/ (create an empty
  zill/__init__.py). Demos live in demos/.
- Commit after each working milestone.

Style
- Keep it minimal and readable. This is teaching code.
- Every file starts with a docstring saying what concept it teaches.
- Every public function has a short docstring.
- Target sizes: provider.py about 100 lines, loop.py about 65 lines.

API key
- Read the key from the environment variable ZILL_API_KEY. A .env file at
  <PATH TO YOUR .env FILE> contains it; load it from there if the variable is
  not set. Never print the key and never commit it.
- Use the <YOUR PROVIDER> API with the model <YOUR MODEL ID> as DEFAULT_MODEL.

zill/provider.py — the only file that knows which vendor we use
- complete(model, system, messages, tools) sends one request and returns
  {"text": str, "tool_calls": [...], "usage": {"input": int, "output": int}}.
- Internally Zill uses one neutral message format:
    {"role": "user", "text": ...}
    {"role": "assistant", "text": ..., "tool_calls": [...]}
    {"role": "tool", "name": ..., "text": ...}
  Translate to and from the vendor's wire format inside this file only. If the
  vendor requires any extra field to be echoed back with a tool call, store it
  on the tool call and send it back.
- Retry with exponential backoff on HTTP 429, 500, 502, 503 and on timeouts.
  On any other HTTP error raise RuntimeError with the status and the start of
  the error body.

zill/loop.py — the heartbeat
- run_loop(model, system, messages, tools, on_event, max_turns=80) -> str.
  tools is a dict of name -> tool; each tool has .spec (its schema) and .run.
- Each turn: call provider.complete, append the assistant message, fire
  on_event. If there are no tool calls, return the text. Otherwise run every
  tool call in order and append one tool message per call.
- An unknown tool returns the text "ERROR: unknown tool <name>". A tool that
  raises returns "ERROR: <ExceptionType>: <message>". The loop must never
  crash because a tool did.
- When max_turns runs out: append a user message asking the model to wrap up,
  make one final call with no tools, and return that text.

demos/day1_dice.py
- A hand-written roll_dice tool, an on_event that prints every message, and
  the task: "Roll 3 dice and tell me whether the total beats 10".

Verify before finishing
1. The dice demo prints four messages in order: user, assistant tool call,
   tool result, assistant answer.
2. The prompt "Build a landing page for a coffee shop" returns text only, with
   no tool calls.
3. git log shows today's commits.
```

`[While it runs, keep talking:]`

While this is running, just look at what I have asked for in this prompt. I have given size targets, because we want the harness to be minimal. I have said no third-party packages. And at the end, I have asked it to verify its own work. A good prompt should always say what "done" looks like.

`[When the dice demo runs:]`

Okay, see this. Four messages. First the user's request. Then the model asking for the dice tool. Then the result from the tool. And then the model's final answer. That is one complete heartbeat, running on our own code.

`[Then run the landing page prompt:]`

Now watch this one. I am asking it to build a landing page for a coffee shop. And what is it doing? It is only describing a landing page. It is not able to create even a single file.

Why? Because it has the judgment, but it does not have hands. A dice roller is not a toolbox.

And that is exactly the gap which we are going to close in the next lecture.

---

## 19. Homework

Before the next lecture, I want you to do three small things.

One. Print the messages array after every turn, and just watch how it grows. And then try one experiment. Comment out the line which appends the tool result, run it again, and see what error you get. When you break it with your own hands, you will really understand that the array is the state.

Two. After every turn, print the turn number, the input tokens, and the output tokens. Your provider is already returning these numbers. Then run three tasks — one very small, one medium, and one which you think will struggle — and note down the numbers in a small table. And see how much bigger the input number is compared to the output number.

Three. Set max turns to one, for a task which needs a tool, and see how the run ends.

Keep that table safely. We will start our lecture on context with it.

---

## 20. Closing

So let me quickly summarise what we did today.

We saw that a model, by itself, cannot do anything. It is a genius locked inside a room.

We saw that the harness is everything around it — the hands, the memory, and the persistence.

We saw that the model has no memory of its own, and the whole memory is just one list which we send again, every single time.

And we saw that the heartbeat of every agent out there is a loop of about ten lines. Thought, action, observation.

In the last lecture, the harness was just a word on a slide. Now it is running on your machine, and you can read every line of it.

And that is really what I want from this series. I don't want you to be someone who only uses these tools. I want you to be someone who can build them.

So today, Zill got its heartbeat. In the next lecture, we will give it hands.

Thank you so much, and I will see you in the next lecture.

---

## Notes for you (not spoken)

**Diagram cue list** (same numbers in `diagrams/` and `diagrams-pro/`)

| # | File | Use it in section |
|---|------|-------------------|
| 01 | diagram-01.png | 2 — five elements pyramid |
| 02 | diagram-02.png | 3 — small harness + skills |
| 03 | diagram-03.png | 5 — model is a function |
| 04 | diagram-04.png | 6 — what a harness is |
| 05 | diagram-05.png | 7 — ReAct triangle |
| 06 | diagram-06.png | 7 — six laps example |
| 07 | diagram-07.png | 8 — growing messages array |
| 08 | diagram-08.png | 9 — three roles |
| 09 | diagram-09.png | 10 — the per-turn tax |
| 10 | diagram-10.png | 11 — tool call id / ticket |
| 11 | diagram-11.png | 12 — the loop, derived |
| 12 | diagram-12.png | 13 — loop code |
| 13 | diagram-13.png | 14 — who decides (workflow vs agent) |
| 14 | diagram-14.png | 15 — skill vs tool |
| 15 | diagram-15.png | 16 — three pieces of a bare harness |
| 16 | diagram-16.png | 17 — provider |
| 17 | diagram-17.png | 18 — today's build |

**Things to check before recording**

- Section 1 describes loop engineering as "the bigger loop, which sits outside, around the agent". Change that one sentence so it matches how you defined loop engineering in Lecture 1.
- Lecture numbering assumed: Lecture 1 = prompt → graph engineering, Lecture 2 = this one (the loop), next lecture = tools.
- Fill the three `<…>` placeholders in the build prompt: the `.env` path, the provider, and the exact model id (copy it from your provider's dashboard).
- Numbers about other harnesses are kept vague on purpose ("tens of thousands of lines"). If you want to name specific projects and line counts, verify them first.
- The script never claims Zill has already built a product or passed a benchmark. Add such claims only after you have done it.
- The ReAct paper for the description: *ReAct: Synergizing Reasoning and Acting in Language Models* (Yao et al., 2022).
- This lesson follows the structure of the Odysseus bootcamp's Day 1. A credit line in the description is the right thing to do.
