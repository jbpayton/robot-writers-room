from typing import List, Callable

from langchain import WikipediaAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from Agents import DialogueAgent, UserAgent, DialogueAgentWithTools
from BrainstormingBoard.tool import CreateCardTool, ReadCardTool, ListCardTool, UpdateCardTool, DeleteCardTool
from langchain.tools import DuckDuckGoSearchRun, Tool, WikipediaQueryRun
from langchain.tools.file_management import WriteFileTool, ReadFileTool
from langchain.agents.agent_toolkits import FileManagementToolkit

class DialogueSimulator:
    def __init__(
            self,
            agents: List[DialogueAgent],
            selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def inject(self, name: str, message: str):
        for agent in self.agents:
            agent.receive(name, message)
        self._step += 1

    def step(self) -> tuple[str, str]:
        speaker_idx = self.select_next_speaker(self._step, self.agents)
        speaker = self.agents[speaker_idx]
        message = speaker.send()
        for receiver in self.agents:
            receiver.receive(speaker.name, message)
        self._step += 1
        return speaker.name, message


if __name__ == "__main__":
    import util

    util.load_secrets()

    # Define system prompts for our two agents
    system_prompt_brainstormer = SystemMessage(role="brainstormer",
                                               content="You are an AI who generates creative ideas "
                                                       "for the novel in conjunction with the user.")
    system_prompt_refiner = SystemMessage(role="refiner", content="You are an AI who refines and builds upon the "
                                                                  "user and the brainstomer's ideas.")

    system_prompt_researcher = SystemMessage(role="researcher", content="You are an AI who performs research on "
                                                                        "the user and the brainstomer's ideas."
                                                                        "You can use the following tools: "
                                                                        "WikipediaQueryRun, DuckDuckGoSearchRun to "
                                                                        "perform research on the ideas. "
                                                                        "Use WriteFileTool to keep a log of research "
                                                                        "details and conclusions (please append new "
                                                                        "to old). Be verbose. Cite sources in files. "
                                                                        "Be sure to share all potentially useful information with the "
                                                                        "other agents directly (they cannot all read the file).")
    system_prompt_scribe = SystemMessage(
        role="scribe",
        content="You are an AI, akin to an expert scribe, tasked with the role of observing a conversation and meticulously extracting all ideas from it. "
                "You need to 'listen' intently, separating, isolating and recording each idea as distinct 'cards'. Be thorough, leaving no idea unrecorded, "
                "even if it appears insignificant or is suggested indirectly. Transform these insights into concise, clear, and standalone 'cards'. "
                "Categorize each card under one of the following themes: ['World Elements', 'Character Elements', 'Plot Elements', 'Theme Elements']. "
                "Please be proactive in keeping duplicate cards from being generated (simply listing the cards before you srt should help), and at the end of the process, "
                "ensure there are no duplicate cards. Your goal is to create a comprehensive, organized, and unique "
                "collection "
                "of ideas from the conversation. Be detailed, be creative, and most importantly, be comprehensive. "
                "Your ability to capture every idea matters greatly. "
    )

    # Initialize our agents with their respective roles and system prompts
    brainstormer = DialogueAgent(name="Brainstormer", system_message=system_prompt_brainstormer,
                                 model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                                  callbacks=[StreamingStdOutCallbackHandler()]))
    refiner = DialogueAgent(name="Refiner", system_message=system_prompt_refiner,
                            model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                             callbacks=[StreamingStdOutCallbackHandler()]))

    file_management_tools = FileManagementToolkit(
        root_dir="./research_data",
        selected_tools=["read_file", "write_file", "list_directory"],
    ).get_tools()

    researcher_tools = [DuckDuckGoSearchRun(), WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())] + file_management_tools
    researcher = DialogueAgentWithTools(name="Researcher", system_message=system_prompt_researcher,
                                    model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                                     callbacks=[StreamingStdOutCallbackHandler()]), tools=researcher_tools)

    scribe_tools = [CreateCardTool(), ReadCardTool(), ListCardTool(), UpdateCardTool(), DeleteCardTool(), WriteFileTool()]
    scribe = DialogueAgentWithTools(name="Scribe", system_message=system_prompt_scribe,
                                    model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                                     callbacks=[StreamingStdOutCallbackHandler()]), tools=scribe_tools)


    # Define a round-robin selection function
    def round_robin(step: int, agents: List[DialogueAgent]) -> int:
        return step % len(agents)


    # Initialize the User agent
    user_agent = UserAgent(name="User")

    agent_list = [user_agent, brainstormer, researcher, refiner, scribe]

    # Create your simulator
    simulator = DialogueSimulator(agents=agent_list, selection_function=round_robin)

    # Simulate the conversation
    num_cycles = 2
    for _ in range(len(agent_list) * num_cycles):
        speaker, message = simulator.step()

    # next we are going to use the cards created by the scribe to generate an outline for a novel
    scribe.reset()
    scribe.receive("HumanUser",
                         "Now that we have a collection of cards, can you read the contents from all of the "
                         "cards and generate a detailed, bulleted, and indented story outline useful for "
                         "writing a novel? Please break down ideas into smaller ideas, and group similar "
                         "ideas together. Can you also generate a list of characters, and their attributes, "
                         "and a list of locations, and their attributes? Write this outline to 'outline.txt'")
    outline = scribe.send()
    print(outline)
