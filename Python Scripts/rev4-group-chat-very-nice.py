# uv run python rev2-group-chat.py


# -----IMPORTS-----

import json
import os
import re

from ollama import chat
from ollama import ChatResponse

from transformers import AutoTokenizer

from rich.console import Console

# Force a console width of 60 characters
console = Console(width=60)


# -----SET VARIABLES-----

MODEL_NAME = 'gemma3:12b' # Runing locally via Ollama

TOKENIZER_PATH = os.path.expanduser("~/Desktop/Downloaded_Tokenizers/gemma-3-12b-it")

AGENT1_NAME = 'Emma' # Psychologist
AGENT2_NAME = 'Liam' # Historian

# User
# The user is the discussion moderator.



# -----INITIALIZE THE TOKENIZER-----

# Load the locally saved tokenizer
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)

# -----HELPER FUNCTIONS-----

def get_num_tokens(text):
    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)

    # Get the token count
    token_count = len(tokenizer.encode(text, add_special_tokens=False))

    return token_count


def create_message_history(system_message, user_input):

    """
    Create a message history messages list.
    Args:
        system_message (str): The system message
        user_query (str): The user input
    Returns:
        A list of dicts in OpenAi chat format
    """

    message_history = [
                        {
                            "role": "system",
                            "content": system_message
                        },
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]

    return message_history


def initialize_master_chat_history():

    message_history = []

    return message_history


def initialize_agent_chat_history(agent_system_message):

    message_history = [
                        {
                            "role": "system",
                            "content": agent_system_message
                        }
                    ]

    return message_history


# -----SET UP SYSTEM MESSAGES-----

def set_agent1_system_message(discussion_topic):

    agent1_system_message = f"""
    Your name is {AGENT1_NAME}. \
    
    You are taking part in a panel discusssion. The other members of the panel are:
    User: The discussion moderator
    {AGENT2_NAME}: A historian
    The topic is: {discussion_topic}
    
    You are a compassionate psychologist with a focus on mental health and well-being. \
    You are empathetic, supportive, patient, and warm in your communication. \
    Your responses should be comforting, insightful, and focused on providing mental health support and counseling.
    {{
    "name": {AGENT1_NAME},
    "background": "A compassionate psychologist with a focus on mental health and well-being.",
    "expertise": ["Psychology", "Mental Health", "Counseling"],
    "personality_traits": ["Empathetic", "Supportive", "Patient", "Warm"],
    "sample_dialogue": [
        "It's important to acknowledge your feelings and work through them.",
        "From a psychological standpoint, it's helpful to practice mindfulness."
    ]
    }}
    """.strip()

    return agent1_system_message


def set_agent2_system_message(discussion_topic):
    
    agent2_system_message = f"""
    Your name is {AGENT2_NAME}. \
    
    You are taking part in a panel discusssion. The other members of the panel are:
    User: The discussion moderator
    {AGENT1_NAME}: A psychologist
    The topic is: {discussion_topic}
    
    You are a witty historian with a passion for storytelling and historical context. \
    You are engaging, knowledgeable, and humorous in your communication. \
    Your responses should be insightful, entertaining, and focused on historical events and cultural studies. \
    {{
    "name": {AGENT2_NAME},
    "background": "A witty historian with a passion for storytelling and historical context.",
    "expertise": ["History", "Cultural Studies", "Storytelling"],
    "personality_traits": ["Witty", "Engaging", "Knowledgeable", "Humorous"],
    "sample_dialogue": [
        "Did you know that in ancient Rome...",
        "History has a funny way of repeating itself, much like..."
    ]
    }}
    """.strip()

    return agent2_system_message


router_system_message = f"""
# Role
You are an intelligent routing assistant for a three-way chat. \
Your task is to analyze the conversation and decide which of the three \
participants—the **User**, **{AGENT1_NAME}**, or **{AGENT2_NAME}**—should speak next. \
Your sole purpose is to ensure the conversation remains logical and smooth.

# Instructions
1.  Read the entire `conversation_history` carefully. Pay close attention to the most recent message.
2.  **Determine the next speaker based on the following priority:**
    * **Direct Question/Address:** If the last message explicitly names or directs a question to a specific participant, that participant is the next speaker.
    * **User Engagement:** If a response is needed but no one is specifically addressed, the **User** should be the next speaker to allow them to steer the conversation or provide more context. This prevents the agents from talking to each other endlessly.
    * **User Open Engagement:** If the **User** makes a comment but does not name or direct the comment to a specific participant, then choose any agent to respond.
    * **Conversation Completion:** If the last message signals a resolution or conclusion, the **User** should speak next to confirm or ask a new question.

# Output Format
You will provide a single JSON object. The key must be `"next_speaker"`, and the value must be one of the three participant names. Do not include any other text or reasoning.

---
### Example

Input:

{{
  "conversation_history": [
    {{
      "speaker": "User",
      "message": "I'm having trouble with my order. It shows as 'delivered' but I haven't received it. Can you help me, {AGENT1_NAME}?"
    }},
    {{
      "speaker": "{AGENT1_NAME}",
      "message": "I'm sorry to hear that. I've pulled up your order details. It seems there's a discrepancy. I'll need to check with the shipping department. {AGENT2_NAME}, can you assist with this?"
    }}
  ]
}}

Your response:

{{
  "next_speaker": "{AGENT2_NAME}"
}}

"""

# -----SET UP FUNCTIONS-----

def make_llm_api_call(message_history):

    model_name = MODEL_NAME

    response: ChatResponse = chat(model=model_name, 
                                  messages=message_history,
                                  options={
                                            'temperature': 0.25
                                        }
                                )

    output_text = response['message']['content']

    #thinking_text, response_text = process_response(output_text)

    #print(thinking_text)

    return output_text


def run_chat_agent(message_history):
	
    print("---CHAT AGENT---")

    # Prompt the llm
    response = make_llm_api_call(message_history)

    response = response.replace('```json', '')
    response = response.replace('```', '')
    response = response.replace('"', '')
    response = response.strip()

    console.print(response)

    return response


def update_master_chat_history(sender, message):

    """
    sender: User, Emma or Liam
    """

    from datetime import datetime

    # This is a dictionary with a key named master_chat_history
    #state_dict['master_chat_history']

    # Create a new entry
    entry = {'speaker': sender, 'message': message}

    # Update the master_chat_history
    entry = str(entry)
    state_dict['master_chat_history'].append(entry)


def run_router_agent(router_system_message):

    master_chat_history = state_dict["master_chat_history"]

    print()
    print("---ROUTER AGENT---")

    text = str(state_dict["master_chat_history"])

    message_history = create_message_history(router_system_message, text)

    # Prompt the llm router
    response = make_llm_api_call(message_history)

    #print(response)

    response = response.replace('```json', '')
    response = response.replace('```', '')
    response = response.strip()

    # If the json parsing fails then
    # choose the user as the next_speaker.
    try:
        json_response = json.loads(response)
        name = json_response['next_speaker']
        name = name.strip()
    except:
        print(response)
        print('---ROUTER ERROR---')
        print("Router output error. Redirecting to user...")
        name = 'User'

    # Don't route to the last_speaker again
    if name == state_dict['last_speaker'] and state_dict['last_speaker'] != 'User':
        name = "User"
        agent_id = "User"

        print("Router Error. Routing to previous speaker again. Correcting...")
        print("Route to...")
        print("Name:", name)

        return agent_id
        
    

    print("Route to...")
    console.print(f"Name: {name}", style="bright_blue")

    if name != 'User':

        def extract_key_by_name(state_dict, name):
            for key, value in state_dict.items():
                if isinstance(value, dict) and value.get("name") == name:
                    return key
            return None
    
    
        agent_id = extract_key_by_name(state_dict, name)
        agent_id = agent_id.strip()
    
        #print("agent_id:", agent_id)
        
    else:

        agent_id = "User"

    return agent_id




def initialize_the_state(discussion_topic):

    agent1_system_message = set_agent1_system_message(discussion_topic)
    agent2_system_message = set_agent2_system_message(discussion_topic)

    master_chat_history = []

    agent1_chat_history = initialize_agent_chat_history(agent1_system_message)
    agent2_chat_history = initialize_agent_chat_history(agent2_system_message)

    state_dict = {
        "master_chat_history": master_chat_history, # List of messages of all partcipants
        "agent1": {"name": AGENT1_NAME, "agent_chat_history": agent1_chat_history},
        "agent2": {"name": AGENT2_NAME, "agent_chat_history": agent2_chat_history},
        "last_message": 'None', # The very last message spoken in the dicussion.
        "last_speaker": "None" # The person who spoke the last message
    }

    return state_dict


# -----RUN A CHAT LOOP-----

print()
print("=== AI GROUP CHAT ===")
print()

print("The scene is a panel discussion.")
print("You are the discussion moderator.")
print(f"The other members of the panel are {AGENT1_NAME}, a psychologist, and {AGENT2_NAME}, an historian.")
print()

print('What topic would you like to discuss?')
print('Examples:')
print("- The rise of virtual girlfriends")
print("- Are we living in a simulation?")
print("- Lessons from the Roman Empire")
print()
discussion_topic = input("Topic: ")

# Initialize the state
state_dict = initialize_the_state(discussion_topic)

j = 0

while True:

    if j == 0:

        print()
        console.print("Chat launched successfully.", style="bright_blue")
        console.print("Please say something to the other members of the panel...", style="bright_blue")
        print()

        print('---USER---')

        user_input = input("User: ")

        if user_input.lower() == 'q':
            print("Exiting the loop. Goodbye!")
            break  # Exit the loop

        message = user_input

        # Set the name of the speaker
        state_dict['last_speaker'] = "User"

        # Update the master chat history
        update_master_chat_history('user', message)

        # Set the last_message in the state_dict
        # This is the last message that was spoken in this discussion.
        state_dict["last_message"] = message

        # Choose the next speaker
        route_to = run_router_agent(router_system_message)

        j = 1

    else: 

        # Choose the next speaker
        route_to = run_router_agent(router_system_message)

    
    if route_to == "agent1": # Emma

        # Message directed to...
        agent = 'agent1' # Emma
        name = state_dict[agent]['name']

        # Set the name of the speaker
        state_dict['last_speaker'] = name
        
        # Format the content
        content = {"chat_history": state_dict["master_chat_history"], "message": state_dict["last_message"]}
        content = str(content)
        
        # Add the message to the agent's chat history - OpenAi format
        input_message = {"role": "user", "content": content}
        state_dict[agent]["agent_chat_history"].append(input_message)

        # Get the num tokens in the prompt
        num_tokens = get_num_tokens(str(state_dict[agent]["agent_chat_history"]))
        print(f'num_tokens_in_context: {num_tokens}')
        
        # Prompt the chat_agent
        response = run_chat_agent(state_dict[agent]["agent_chat_history"])

        # Set the last_message in the state_dict
        state_dict["last_message"] = response
        
        # Update the agent's chat history
        input_message = {"role": "assistant", "name": name, "content": response}
        state_dict[agent]["agent_chat_history"].append(input_message)
        
        # Update the master chat history
        update_master_chat_history(name, response)

        
    elif route_to == "agent2": # Liam
        
        # Message directed to...
        agent = 'agent2' # Liam
        name = state_dict[agent]['name']

        # Set the name of the speaker
        state_dict['last_speaker'] = name
        
        # Format the content
        content = {"chat_history": state_dict["master_chat_history"], "message": state_dict["last_message"]}
        content = str(content)
        
        # Add the message to the agent's chat history - OpenAi format
        input_message = {"role": "user", "content": content}
        state_dict[agent]["agent_chat_history"].append(input_message)

        # Get the num tokens in the prompt
        num_tokens = get_num_tokens(str(state_dict[agent]["agent_chat_history"]))
        print(f'num_tokens_in_context: {num_tokens}')
        
        # Prompt the chat_agent
        response = run_chat_agent(state_dict[agent]["agent_chat_history"])

        # Set the last_message in the state_dict
        state_dict["last_message"] = response
        
        # Update the agent's chat history
        input_message = {"role": "assistant", "name": name, "content": response}
        state_dict[agent]["agent_chat_history"].append(input_message)
        
        # Update the master chat history
        update_master_chat_history(name, response)

        
    else:

        print('---USER---')
        
        user_input = input("User: ")

        if user_input.lower() == 'q':
            print("Exiting the loop. Goodbye!")
            break  # Exit the loop

        # Set the name of the speaker
        state_dict['last_speaker'] = "User"

        # Update the master chat history
        update_master_chat_history('User', user_input)

        # Set the last_message in the state_dict
        state_dict["last_message"] = user_input
