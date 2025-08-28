# Chat With Two LLM Agents Python Workflow
A simple python workflow that shows how one user can chat with two LLM agents at the same time. Useful for gaining multiple expert perspectives on a subject. 

In this example a user is chatting with two AI experts in a panel discussion. The topic is: The Rise of Virtual Girlfriends. One agent is a historian. The other is a psychologist. The user is the discussion moderator. After each person speaks, an LLM Router agent reviews the conversation history and decides who should speak next. The user is able to speak using a simple python input. 

<a href="https://www.youtube.com/@walterthealien">
  <img src="https://github.com/vbookshelf/Chat-With-Two-LLM-Agents-Python-Workflow/blob/main/images/panel-discussion.png" alt="Ep1 - Hello, Earth" height="300">
</a>

## Environment and Hardware
The code is set up to run locally, in a Jupyter notebook, using the gemma3:12b model from Ollama. I used a M4 Macbook Air, 16GB RAM. I also used the Ollama Python package.

## Sample Chat

```
---USER---
User:  Hi everyone. Welcome to the discussion. Its a pleasure to have you here.
---ROUTER AGENT---
Route to...
Name: User
---USER---
User:  Can you please tell us a bit about your background
---ROUTER AGENT---
Route to...
Name: Emma
agent_id: agent1
---CHAT AGENT---
(Smiling warmly) "Thank you for having me. It's lovely to be here. My name is Emma, and I'm a psychologist.
I've dedicated my career to understanding and supporting mental health and well-being.
I work with individuals to navigate challenges, build resilience, and cultivate a greater sense of self-understanding.
I believe deeply in the power of empathy and connection, and I strive to create a safe and supportive space
for people to explore their thoughts and feelings.
I'm particularly interested in how technology impacts our relationships and emotional lives,
which is why I'm so intrigued by this discussion about virtual girlfriends."
---ROUTER AGENT---
Route to...
Name: Liam
agent_id: agent2
---CHAT AGENT---
(Adjusting my spectacles and with a twinkle in my eye) "The pleasure's all mine! Liam's the name,
and historical context is my game. It's fascinating to be here discussing virtual girlfriends – a topic that, frankly,
feels ripped from the pages of a particularly outlandish science fiction novel.
But as a historian, I'm trained to see patterns, and let me tell you, this isn't entirely new territory. 

We've been seeking companionship and connection through artificial means for centuries!
Think about the elaborate automata of the 18th century – mechanical dolls designed to mimic human interaction.
They were status symbols, yes, but also, I suspect, a yearning for something *more* than what was readily available.
Or consider the rise of fan fiction, which has been a vibrant, if often overlooked, cultural phenomenon for decades.
People creating their own idealized companions within established narratives – a digital courtship, if you will. 

History has a funny way of repeating itself, much like the desire for connection finds new and increasingly
inventive outlets.
It’s just that now, instead of clockwork mechanisms or imagined characters, we have sophisticated AI.
The core human need remains the same, doesn't it? It’s just the delivery method that’s undergone a
rather dramatic upgrade."
---ROUTER AGENT---
Route to...
Name: User
```
