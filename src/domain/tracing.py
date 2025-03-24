import asyncio
import random
from agents import Agent, AgentHooks, RunContextWrapper, Runner, Tool, function_tool

# Tracing Hook để theo dõi các sự kiện
class TracingHooks(AgentHooks):
    def __init__(self, name: str):
        self.event_counter = 0
        self.name = name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"[{self.name}] {self.event_counter}: Agent {agent.name} started")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: str) -> None:
        self.event_counter += 1
        print(f"[{self.name}] {self.event_counter}: Agent {agent.name} ended with output: {output}")

    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
        self.event_counter += 1
        print(f"[{self.name}] {self.event_counter}: Handoff from {source.name} to {agent.name}")
