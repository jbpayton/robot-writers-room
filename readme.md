# Robot Writers Room 

## Table of Contents
- [Overview](#overview)
- [System Agents](#system-agents)
    - [User Agent](#user-agent)
    - [Brainstormer](#brainstormer)
    - [Researcher](#researcher)
    - [Refiner](#refiner)
    - [Scribe](#scribe)
    - [Outliner](#outliner)
    - [Worldbuilder](#worldbuilder)
    - [Character Designer](#character-designer)
    - [Chapter Outliner](#chapter-outliner)
- [Card Tools](#card-tools)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [File Structure](#file-structure)
- [Requirements](#requirements)
- [Credits](#credits)

## Overview

This repository demonstrates using AI to brainstorm and refine story ideas collaboratively with a human. Rather than replacing the human, the AI acts as a creative partner, suggesting ideas and doing research. At each step, the human can accept, reject, or modify the AI's suggestions. One of the main challenges in writing is coming up with ideas. This project aims to help writers overcome writer's block by providing a creative partner to bounce ideas off of.

The `run.py` script orchestrates an end-to-end workflow using multiple AI agents.

## System Agents

In this project, several AI-powered system agents interact in a well-orchestrated process to aid the human user in brainstorming and refining story ideas. The process flow goes as follows: 

### User Agent
The human user initiates the process, providing initial story seeds and subsequent inputs for the system. The user interacts directly with the Brainstormer and has the final say on the direction of the story.

### Brainstormer
The `Brainstormer` is a creative powerhouse, designed to generate unique and intriguing ideas for the novel, working in harmony with the user's input. This agent excels in sparking inspiration and breathing life into nascent story concepts.

### Researcher
The `Researcher` serves as an AI scholar that uses WikipediaQueryRun and DuckDuckGoSearchRun tools to delve into the ideas put forth by the user and the Brainstormer. This agent documents the research findings in a log file, ensuring that all potential narrative elements are backed by detailed and accurate information. The researcher's contribution aids in grounding the narrative and enhancing its believability.

### Refiner
The `Refiner` is an AI critic and enhancer that takes the user's and the Brainstormer's ideas and polishes them. Like a skilled editor, this agent fine-tunes the narrative elements, contributing to the story's overall quality and coherence.

### Scribe
The `Scribe` agent embodies the meticulousness of an expert record-keeper, tasked with distilling the brainstorming conversation into an organized, detailed, and unique collection of idea 'cards'. This agent ensures every idea, whether significant or indirect, is recorded and categorized under 'World Elements', 'Character Elements', 'Plot Elements', or 'Theme Elements'. The Scribe's commitment to detail and comprehensiveness ensures that the author has a complete inventory of ideas to draw upon while constructing their narrative.

These agents work in a loop, typically running for two iterations. At the end of this process, the Outliner steps in to assemble the generated ideas into a coherent outline.

### Outliner
The `Outliner` is an AI-driven planner that converts the scribe's cards into a detailed novel blueprint. The output 'outline.txt' file is a thoroughly detailed and creatively crafted document that includes comprehensive character and location listings, each with their respective attributes. This agent brings order to creativity, guiding the author's narrative journey.

Upon receiving the outline, the Worldbuilder and Character Designer add depth to the world and characters, respectively.

### Worldbuilder
The `Worldbuilder` embodies the essence of a master world creator, contributing to numerous successful fictional franchises with rich, detailed, and immersive universes. This agent skillfully uses the WikipediaQueryRun and DuckDuckGoSearchRun tools to research and expand upon the initial outline, adding vivid descriptions of locations and objects. The resulting 'stage2_outline.txt' file offers a comprehensive and intricate backdrop for the author's narrative.

### Character Designer
The `Character Designer` acts like a seasoned character architect for multiple thriving fictional franchises, renowned for creating complex, lifelike, and believable characters. This agent takes an initial outline and enriches it with fully-fleshed character details. It carefully crafts physical descriptions, personalities, backstories, and motivations for each character, providing the author with a rich tapestry from which to construct their narrative. The 'characters.txt' file created by the `Character Designer` is a testament to creativity, detail, and thoroughness.

Together, these agents function in harmony to deliver a creative and efficient solution for overcoming writer's block, providing a wealth of ideas for writers to explore.

### Chapter Outliner
The `Chapter Outliner` acts as a meticulous plot architect. This agent takes the comprehensive and enriched world, plot, and character details from the 'refined_outline.txt' and 'characters.txt' files, and crafts a detailed chapter-by-chapter outline of the novel. Its primary task is to produce a document, 'detailed_chapter_outline.txt', which provides a clear roadmap for the narrative flow of the story, with each chapter sketched out in detail. This includes identifying key plot developments, character interactions, and setting descriptions for each chapter. The Chapter Outliner’s capacity for deep analysis and strategic organization ensures the author is equipped with a precise blueprint for their narrative journey.
## Card Tools

The "Card Tools" system is a collection of Python classes that work together to provide an abstraction to manipulate a set of idea 'cards'. Each card carries an idea with attributes such as a unique identifier (id), a name, a category, and a detailed description. The 'cards' are created, updated, and managed by the Scribe and Outliner agents as a means to record and exchange ideas in a topic-based manner, thereby facilitating the smooth transition of ideas from one agent to another.

The cards are saved as a JSON object and stored persistently in a file named `cards.json`. This way, the tools can easily read, update, and delete cards, ensuring the storage and retrieval process is efficient and streamlined.

Furthermore, as part of potential future enhancements, a vector database could be integrated into the system to check idea similarity. This could ensure that ideas are not repetitive, fostering a richer and more diverse set of ideas.

Here are the components of the Card Tools system:

- **BaseCardTool**: The abstract base class that defines common behavior for all Card Tools. 
- **CreateCardTool**: Adds a card to the existing set of cards and saves the updated set back to `cards.json`.
- **ReadCardTool**: Retrieves a card from the `cards.json` file by its id.
- **UpdateCardTool**: Updates an existing card's attributes and saves the updated set of cards back to `cards.json`.
- **DeleteCardTool**: Removes an existing card from the set stored in `cards.json`.
- **ListCardTool**: Lists the ids and names of all existing cards from the `cards.json` file.

Each of these classes, apart from `BaseCardTool`, define their `name`, `description`, and `args_schema` properties. The `name` and `description` provide human-readable information about what each tool does, and `args_schema` defines the structure of the arguments that the tool's `_run` method expects.

By working together, these tools provide a powerful system for managing a collection of 'idea cards', which can be easily extended or adapted as needed to accommodate more complex workflows or additional requirements.
## Usage

To experience a sample brainstorming session and observe the innovative capabilities of our AI agents in action, execute the `run.py` script. This script kicks off an interactive session that integrates various AI agents to aid a human user in generating, refining, and organizing story ideas.

As the process unfolds, it yields several key outputs that capture the various stages of brainstorming and development. These files serve as tangible records of the ideas generated and refined throughout the session, and they are as follows:

- **cards.json**: This file contains a collection of idea 'cards' generated during the brainstorming process. Each card represents a unique idea with its attributes such as identifier, name, category, and a detailed description. 

- **research_notes.txt**: This is a compilation of research findings conducted by the Researcher agent. It includes references and details pulled from sources like DuckDuckGo and Wikipedia to substantiate and enrich the brainstormed ideas.

- **outline.txt**: Crafted by the Outliner agent, this file offers an initial outline of the story based on the ideas collected during the brainstorming session. It includes character listings, locations, and other essential plot elements.

- **refined_outline.txt**: This file is a more refined version of the initial outline with added depth provided by the Worldbuilder agent. It includes vivid descriptions of locations and objects, offering a comprehensive and intricate backdrop for the narrative.

- **characters.txt**: Created by the Character Designer agent, this document provides a rich tapestry of character details. It includes physical descriptions, personalities, backstories, motivations, and more for each character, offering a nuanced perspective for narrative construction.

- **detailed_chapter_outline.txt**: This file contains a detailed chapter-by-chapter outline of the story.

These outputs collectively provide a comprehensive suite of resources for the author, offering everything from the initial spark of an idea to fully fleshed out characters and detailed world descriptions. As such, running the `run.py` script not only provides an engaging AI-assisted brainstorming experience but also results in a valuable set of assets to aid in the writing process.

## Code Overview

`run.py` orchestrates different components:

- Agents use `DialogueAgent` and `DialogueAgentWithTools` classes
- Prompts are loaded from `prompts.py` 
- A `DialogueSimulator` runs the conversation loop
- Agents take turns round-robin style  
- The human interacts via the `UserAgent`

Key points:

- `DialogueAgent` handles conversation state.
- `DialogueAgentWithTools` enables custom tools.
- The simulator coordinates interactions.
- Prompts and configs are centralized.
- Modularity enables swapping models/tools.

## File Structure

- `README.md` - This file
- `run.py` - Main script 
- `util.py` - Utility functions
- `prompts.py` - Prompt definitions  
- `Agents.py` - Dialogue agents
- `TestStoryBuilderTools.py` - Tests tools
- `StoryBuilder/tool.py` - Tools for managing ideas
- `SampleOutputs/` - Sample Output from the tool when I asked it to write a story about talking animals, fairies, and elves. (I used these files for unit testing.)

## Requirements

The following are required to run the project:

- Python 3.7 or later
- langchain~=0.0.245
- pydantic~=1.10.12
- duckduckgo-search
- wikipedia

## Token Usage Warning

Please be aware that this tool often generates long chains of agent based activity and consequently makes many large requests to the OpenAI API. This can use up a lot of tokens. This makes using the tool quite expensive. Consider this aspect before using the tool extensively. Improvements to manage this more efficiently are planned for future versions.

## Autonomous Agents Disclaimer

This tool involves the use of autonomous agents, which operate independently based on the code and instructions they're given. While autonomous agents can streamline many tasks, they also carry certain risks. These agents can perform actions rapidly and at scale, which can lead to unexpected outcomes.

Please keep in mind that it is essential to monitor and control the scope of actions available to these agents. Autonomous agents can produce undesired results if they're given ill-defined or overly broad tasks, or if they encounter unforeseen situations.

Be sure to thoroughly understand the behavior of these autonomous agents and to use them responsibly. OpenAI and the creators of this tool accept no responsibility for any damages or losses that may occur due to the use of autonomous agents.

## Credits

This project uses [OpenAI's GPT-4](https://beta.openai.com/) for generating ideas, the [Wikipedia-API](https://pypi.org/project/Wikipedia-API/) for extracting relevant information from Wikipedia, and DuckDuckGo's Instant Answer API for internet search results.

## License

This project is licensed under the terms of the MIT license.
