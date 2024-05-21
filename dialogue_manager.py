import yaml
import random

class DialogueManager:
    def __init__(self, responses_file="yams/responses.yml"):
        self.responses = self.load_responses(responses_file)

    def load_responses(self, responses_file):
        with open(responses_file, "r") as file:
            responses_data = yaml.safe_load(file)
        return responses_data.get("intents", {})

    def respond(self, intent, entities):
        if intent in self.responses:
            intent_data = self.responses[intent]
            responses = intent_data.get("responses", [])
            response_template = random.choice(responses)["text"] if responses else "I'm not sure how to respond to that."
            response_text = self.fill_placeholders(response_template, entities, intent_data.get("entities", []))
            action = intent_data.get("action")
            
            response = {"text": response_text, "action": action}
        else:
            response = {"text": "I'm not sure how to respond to that."}
        
        return response

    def fill_placeholders(self, template, entities, expected_entities):
        filled_response = template
        for entity_name in expected_entities:
            entity_value = next((ent[0] for ent in entities if ent[1] == entity_name.upper()), None)
            placeholder = f"[{entity_name}]"
            if entity_value:
                filled_response = filled_response.replace(placeholder, f" {entity_value}")
            else:
                filled_response = filled_response.replace(placeholder, "")
        return filled_response


if __name__ == "__main__":
    dialogue_manager = DialogueManager("yams/responses.yml")
    test_intent = "greet"
    test_entities = [("John", "PERSON")]
    response = dialogue_manager.respond(test_intent, test_entities)
    print(response["text"])
