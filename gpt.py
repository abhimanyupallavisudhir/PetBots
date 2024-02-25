from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
import openai
import prefaces

#load_dotenv(override=True)

cliento = openai.OpenAI()

def text_input(prompt_text = "Input text here: "):
    session = PromptSession()

    # Initialize text storage
    text_storage = []

    # Customize key bindings for multiline input
    bindings = KeyBindings()

    @bindings.add('c-d')
    def _(event):
        # When Ctrl+D is pressed, capture the current input buffer and exit
        text_storage.append(event.app.current_buffer.text)
        event.app.exit()

    try:
        session.prompt(prompt_text, multiline=True, key_bindings=bindings)
    except EOFError:
        # Handle the EOFError to gracefully return the input when Ctrl+D is pressed
        pass

    # Return the captured text or join multiple inputs if necessary
    return '\n'.join(text_storage) if text_storage else ''

class Agent:
    public_history = []  # Shared conversation history among all Agent instances
    _registry = {}
    quit_word = 'quit'
    
    def __init__(self, name, model_type, private_preface):
        if name == Agent.quit_word:
            name = name + '_1995'
            print(f"Taking the name '{Agent.quit_word}' would bring on the Apocalypse. I have instead named him {Agent.quit_word}_1995.\n\n")
        if name in Agent._registry: # important: don't make this an elif
            print(f"Overrwrote an existing agent with the name '{name}'. Hope you weren't too attached to the old {name}.\n\n")
        self.name = name
        self.model_type = model_type
        self.private_history = [{"role" : "system", "content" : private_preface}]
        Agent._registry[name] = self            
    
    # def run(self):
    #     if self.model_type == "user":
    #         output = text_input(f"{self.name}, enter your message: ")
    #         Agent.public_history.append({"role": "user", "content": output})
    #     elif self.model_type.startswith("gpt"):
    #         completion = cliento.chat.completions.create(
    #             model = self.model_type, 
    #             messages = self.private_history + Agent.public_history)
    #         output = completion.choices[0].message.content
    #         Agent.public_history.append({"role": "assistant", "content": output})
    #         print(f"{self.name}: {output}") 
    #     else:
    #         print("Unsupported model type.")

    def run(self):
        if self.model_type == "user":
            output = text_input(f"\n\n{self.name}, input your message (Ctrl-D to submit):\n")
            Agent.public_history.append({"role": "user", "content": output})
        elif self.model_type.startswith("gpt"):
            try:
                print(f"\n\n{self.name} says:")
                stream = cliento.chat.completions.create(
                    model=self.model_type,
                    messages=self.private_history + Agent.public_history,
                    stream=True
                )
                
                for chunk in stream:
                    completion = ""
                    if chunk.choices[0].delta.content is not None:
                        completion_chunk = chunk.choices[0].delta.content
                        print(completion_chunk, end='', flush=True)
                    completion += completion_chunk
                Agent.public_history.append({"role": "assistant", "content": completion})
            except Exception as e:
                print(f"Error during API call: {e}")
        else:
            print("Unsupported model type.")

    @classmethod
    def print_history(cls):
        for entry in cls.public_history:
            print(f"{entry['role']}: {entry['content']}")

def conversation(order_of_speaking=Agent._registry):
    if order_of_speaking is None:
        # Interactive mode, similar to the original implementation
        while True:
            agent_name = input("\n\nEnter the name of the Agent to run (or '{Agent.quit_word}' to exit): ")
            if agent_name == Agent.quit_word:
                break
            agent = Agent._registry.get(agent_name)
            if agent:
                agent.run()
            else:
                print("Agent not found.")
    else:
        # Follow the predefined order of speaking
        while True:
            for agent_name in order_of_speaking:
                agent = Agent._registry.get(agent_name)
                if agent:
                    agent.run()
                else:
                    print(f"Agent named '{agent_name}' not found.")

User = Agent(name = "Your Name", model_type = "user", private_preface = "You're a human, you don't need a preface.")
Assistant = Agent(name = "Assistant", model_type = "gpt-4", private_preface = prefaces.default)