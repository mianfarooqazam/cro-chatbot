from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

CRO_LIST = [
    {"name": "CRO Alpha", "keywords": ["oncology", "clinical trial", "pharma"]},
    {"name": "Beta CRO", "keywords": ["medical device", "regulatory", "device"]},
    {"name": "Gamma Research", "keywords": ["biotech", "preclinical", "toxicology"]},
    {"name": "Delta CRO", "keywords": ["vaccine", "immunology", "infectious"]},
]

class ActionMatchCROs(Action):
    def name(self) -> Text:
        return "action_match_cros"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        industry = tracker.get_slot("industry")
        service = tracker.get_slot("service")
        matched = []
        for cro in CRO_LIST:
            if (industry and industry.lower() in cro["keywords"]) or (service and service.lower() in cro["keywords"]):
                matched.append(cro["name"])
        if not matched:
            matched = [cro["name"] for cro in CRO_LIST]  
        msg = "Here are some CROs that match your project:\n"
        for name in matched:
            msg += f"- {name}\n"
        msg += "\nPlease type the name of the CRO you'd like to select."
        dispatcher.utter_message(text=msg)
        return []

class ActionSendProject(Action):
    def name(self) -> Text:
        return "action_send_project"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cro_name = tracker.get_slot("cro_name")
        industry = tracker.get_slot("industry")
        service = tracker.get_slot("service")
        budget = tracker.get_slot("budget")
        timeline = tracker.get_slot("timeline")
        msg = (
            f"Your project details have been sent to {cro_name}!\n"
            f"Industry: {industry}\nService: {service}\nBudget: {budget}\nTimeline: {timeline}\n"
            "The CRO will contact you soon."
        )
        dispatcher.utter_message(text=msg)
        return []
