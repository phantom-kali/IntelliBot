from nlu import NLU
from dialogue_manager import DialogueManager
from action_executor import ActionExecutor

nlu = NLU(intents_file="yams/intents.yml", w2v_model_path="models/word2vec.model", svm_model_path="models/svm_model.joblib", label_encoder_path="models/label_encoder.joblib")
dialogue_manager = DialogueManager()
action_executor = ActionExecutor()

def main():
    while True:
        user_input = input("User: ")
        if user_input == '!q':
            break
        intent, entities, _, _ = nlu.parse(user_input)
        response = dialogue_manager.respond(intent, entities)
        action = response.get("action")
        if action:
            action_executor.execute(action)
        else:
            print("Bot:", response["text"])

if __name__ == "__main__":
    main()