from typing import Optional, List, Any

from langchain.callbacks.manager import AsyncCallbackManagerForToolRun
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
import json
import os


class CardInput(BaseModel):
    name: str = Field(
        ...,
        description="The name of the idea.",
    )
    category: str = Field(
        ...,
        description="The category of the idea.",
    )
    description: str = Field(
        ...,
        description="A detailed description of the idea.",
    )


class BaseCardTool(BaseTool):
    @staticmethod
    def _load_cards():
        if os.path.exists("cards.json"):
            with open("cards.json", 'r') as file:
                return json.load(file)
        else:
            return {}

    @staticmethod
    def _save_cards(cards):
        with open("cards.json", 'w') as file:
            json.dump(cards, file, indent=4)

    def _run(self, card_data: CardInput):
        raise NotImplementedError("BaseCardTool does not support sync")

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BaseCardTool does not support async")


class CreateCardTool(BaseCardTool):
    name: str = "create_card"
    description: str = "Tool to create a new card. Please provide a name, category, and description."
    args_schema: type = CardInput

    def _run(self, name="", category="", description=""):
        cards = super()._load_cards()
        next_id = len(cards)
        cards[next_id] = {"id": next_id, "name": name, "category": category, "description": description}
        super()._save_cards(cards)
        return f'Card {next_id} created.'

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("CreateCardTool does not support async")


class ReadCardTool(BaseCardTool):
    name: str = "read_card"
    description: str = "Tool to read a card."
    args_schema: type = CardInput

    def _run(self, card_id: str):
        cards = super()._load_cards()
        if card_id not in cards:
            raise ValueError(f"No card with id {card_id} exists.")
        return cards[card_id]

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("ReadCardTool does not support async")


class UpdateCardTool(BaseCardTool):
    name: str = "update_card"
    description: str = "Tool to update a card, provided with an name, category, and description."
    args_schema: type = CardInput

    def _run(self, id="", name="", category="", description=""):
        cards = super()._load_cards()
        if id not in cards.keys():
            raise ValueError(f"No card with id {id} exists.")
        cards[id] = {"id": id, "name": name, "category": category, "description": description}
        super()._save_cards(cards)
        return f'Card {id} updated.'

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("UpdateCardTool does not support async")


class DeleteCardTool(BaseCardTool):
    name: str = "delete_card"
    description: str = "Tool to delete a card."
    args_schema: type = CardInput

    def _run(self, card_id: str):
        cards = super()._load_cards()
        if card_id not in cards.keys():
            raise ValueError(f"No card with id {card_id} exists.")
        del cards[card_id]
        super()._save_cards(cards)
        return f'Card {card_id} deleted.'

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DeleteCardTool does not support async")


class ListCardTool(BaseTool):
    name: str = "list_card"
    description: str = "Tool to list ids and names of all cards."

    @staticmethod
    def _load_cards():
        if os.path.exists("cards.json"):
            with open("cards.json", 'r') as file:
                return json.load(file)
        else:
            return {}

    def _run(self):
        cards = ListCardTool._load_cards()
        return [(card_id, card_data['name']) for card_id, card_data in cards.items()]

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("ListCardTool does not support async")