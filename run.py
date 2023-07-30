from typing import List, Callable

from langchain import WikipediaAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from Agents import DialogueAgent, UserAgent, DialogueAgentWithTools
from BrainstormingBoard.tool import CreateCardTool, ReadCardTool, ListCardTool, UpdateCardTool, DeleteCardTool
from langchain.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain.tools.file_management import WriteFileTool, ReadFileTool

from prompts import CHARACTER_DESIGNER_HUMAN_PROMPT, CHARACTER_DESIGNER_SYSTEM_PROMPT, WORLDBUILDER_HUMAN_PROMPT, \
    WORLDBUILDER_SYSTEM_PROMPT, OUTLINER_HUMAN_PROMPT, OUTLINER_SYSTEM_PROMPT, BRAINSTORMER_SYSTEM_PROMPT, \
    REFINER_SYSTEM_PROMPT, RESEARCHER_SYSTEM_PROMPT, SCRIBE_SYSTEM_PROMPT


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
                                               content=BRAINSTORMER_SYSTEM_PROMPT)
    system_prompt_refiner = SystemMessage(role="refiner", content=REFINER_SYSTEM_PROMPT)

    system_prompt_researcher = SystemMessage(role="researcher", content=RESEARCHER_SYSTEM_PROMPT)
    system_prompt_scribe = SystemMessage(
        role="scribe",
        content=SCRIBE_SYSTEM_PROMPT
    )

    # Initialize our agents with their respective roles and system prompts
    brainstormer = DialogueAgent(name="Brainstormer",
                                 system_message=system_prompt_brainstormer,
                                 model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                                  callbacks=[StreamingStdOutCallbackHandler()]))

    refiner = DialogueAgent(name="Refiner",
                            system_message=system_prompt_refiner,
                            model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                             callbacks=[StreamingStdOutCallbackHandler()]))

    # Define the tools for the researcher
    researcher_tools = [DuckDuckGoSearchRun(),
                        WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),WriteFileTool()]
    researcher = DialogueAgentWithTools(name="Researcher",
                                        system_message=system_prompt_researcher,
                                        model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                                         callbacks=[StreamingStdOutCallbackHandler()]),
                                        tools=researcher_tools)

    scribe_tools = [CreateCardTool(), ReadCardTool(), ListCardTool(), UpdateCardTool(), DeleteCardTool(),
                    WriteFileTool()]

    scribe = DialogueAgentWithTools(name="Scribe",
                                    system_message=system_prompt_scribe,
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
    print("Starting brainstorming session, please provide an idea for a novel.")
    num_cycles = 2

    for _ in range(num_cycles):
        for _ in range(len(agent_list)):
            speaker, message = simulator.step()

        # reset the researcher after each cycle
        researcher.reset()

    # next we are going to use the cards created by the scribe to generate an outline for a novel
    system_prompt_outliner = SystemMessage(
        role="outliner",
        content=OUTLINER_SYSTEM_PROMPT
    )
    scribe_tools = [ReadCardTool(), ListCardTool(), WriteFileTool()]
    outliner = DialogueAgentWithTools(name="Outliner", system_message=system_prompt_outliner,
                                      model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                                       callbacks=[StreamingStdOutCallbackHandler()]),
                                      tools=scribe_tools)
    outliner.receive("HumanUser",
                     OUTLINER_HUMAN_PROMPT)

    outline = outliner.send()
    print(outline)

    # next we are going to have the worldbuilder use the outline created by the outliner to flesh out the outline
    system_prompt_world_builder = SystemMessage(
        role="world_builder",
        content=WORLDBUILDER_SYSTEM_PROMPT
    )
    world_builder_tools = [ReadFileTool(),
                           WriteFileTool(),
                           WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
                           DuckDuckGoSearchRun()]

    world_builder = DialogueAgentWithTools(name="WorldBuilder", system_message=system_prompt_world_builder,
                                           model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                                            callbacks=[StreamingStdOutCallbackHandler()]),
                                           tools=world_builder_tools)
    world_builder.receive("HumanUser",
                          WORLDBUILDER_HUMAN_PROMPT)

    outline = world_builder.send()
    print(outline)

    # next we are going to have the character designer use the outline created by the outliner to flesh out the
    # character portion of the outline
    system_prompt_character_designer = SystemMessage(
        role="character_designer",
        content=CHARACTER_DESIGNER_SYSTEM_PROMPT
    )
    character_designer_tools = [ReadFileTool(), WriteFileTool()]
    character_designer = DialogueAgentWithTools(name="CharacterDesigner",
                                                system_message=system_prompt_character_designer,
                                                model=ChatOpenAI(model_name='gpt-4', streaming=True,
                                                                 callbacks=[StreamingStdOutCallbackHandler()]),
                                                tools=character_designer_tools)
    character_designer.receive("HumanUser",
                               CHARACTER_DESIGNER_HUMAN_PROMPT)

    outline = character_designer.send()
    print(outline)
