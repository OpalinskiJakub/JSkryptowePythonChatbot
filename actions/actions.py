import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCheckOpeningHours(Action):
    def name(self) -> Text:
        return "action_check_opening_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        day = tracker.get_slot('day')
        with open("data/opening_hours.json") as f:
            opening_hours = json.load(f)["items"]

        hours = opening_hours.get(day.capitalize(), {"open": 0, "close": 0})
        if hours["open"] == 0:
            dispatcher.utter_message(text=f"We are closed on {day}.")
        else:
            dispatcher.utter_message(text=f"We are open on {day} from {hours['open']} to {hours['close']}.")

        return []

class ActionListMenu(Action):
    def name(self) -> Text:
        return "action_list_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open("data/menu.json") as f:
            menu = json.load(f)["items"]

        menu_items = ", ".join([item["name"] for item in menu])
        dispatcher.utter_message(text=f"Our menu includes: {menu_items}")

        return []

class ActionProcessOrder(Action):
    def name(self) -> Text:
        return "action_process_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        items = tracker.get_slot('items')
        dispatcher.utter_message(text=f"You have ordered: {items}. Your order will be ready shortly.")
        return []
