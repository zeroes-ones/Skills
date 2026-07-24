# CrewAI, AutoGen & OpenAI Swarm Patterns

## CrewAI Pattern
```python
from crewai import Agent, Task, Crew, Process

architect = Agent(role="System Architect", goal="Design system", ...)
developer = Agent(role="Backend Developer", goal="Implement API", ...)
tester = Agent(role="QA Engineer", goal="Test system", ...)

task1 = Task(description="Design architecture", agent=architect)
task2 = Task(description="Implement API", agent=developer)
task3 = Task(description="Write tests", agent=tester)

crew = Crew(agents=[architect, developer, tester],
            tasks=[task1, task2, task3],
            process=Process.sequential)
result = crew.kickoff()
```

## AutoGen Pattern
```python
from autogen import AssistantAgent, GroupChat, GroupChatManager

alice = AssistantAgent("Alice", system_message="You are a system architect")
bob = AssistantAgent("Bob", system_message="You are a backend developer")
charlie = AssistantAgent("Charlie", system_message="You review code for security")

groupchat = GroupChat(agents=[alice, bob, charlie], messages=[], max_round=10)
manager = GroupChatManager(groupchat=groupchat)
alice.initiate_chat(manager, message="Design and implement a REST API")
```

## OpenAI Swarm Pattern
```python
from swarm import Swarm, Agent

def transfer_to_developer(): return developer
def transfer_to_architect(): return architect

architect = Agent(name="Architect", instructions="...", functions=[transfer_to_developer])
developer = Agent(name="Developer", instructions="...", functions=[transfer_to_architect])

client = Swarm()
response = client.run(agent=architect, messages=[{"role": "user", "content": "..."}])
```
