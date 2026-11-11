---
name: ambitious-prompt
description: Rewrite a prompt so it asks for altitude, depth, range and an outside judge.
disable-model-invocation: true
---

# Ambitious prompt

Rewrite a prompt (for you, another agent or another model) so it asks for more ambitious work and stays honest about the result.

The prompt is the text after `/ambitious-prompt`. If there is none, use the user's last request.

## 1. Answer four questions for this prompt

- **Altitude**: what is the prompt's output for? What happens after it?
- **Depth**: who is the best practitioner, what raw material would they start from, which instruments would they use?
- **Range**: which other fields would see something here, and what would they do?
- **Outside judge**: what, other than the model itself, will show the result is right?

Also list what the receiving model is actually equipped with (tools, data, a computer, internet). Ask the user if you cannot tell.

## 2. Rewrite

Build the new prompt from those answers, using these levers:

- **Name actions and instruments, not identities.** "Load the data into a database and fit a survival model", not "you are a world-class statistician".
- **State the purpose.** One sentence on what the result is for gives the model reason and permission to question the task.
- **Pair every hard target with a check and an exit.** The target, the measurement that tests it, and permission to report a partial result honestly. A hard target with no check pushes a model toward claiming success.
- **State only real capabilities.** A model told it has tools it lacks stalls or pretends.
- **Give the real reason the result matters** instead of pressure, threats or capital letters.
- **Say what to do.** Phrase every instruction as the target behaviour.

Keep it as short as the task allows.

## 3. Return

1. The rewritten prompt in one code block, ready to paste.
2. Three bullets on what changed and why.
3. A shorter variant when the rewrite runs past about 200 words.
