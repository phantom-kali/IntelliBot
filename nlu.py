import spacy
import yaml
import numpy as np
from gensim.models import Word2Vec
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from joblib import dump, load

class NLU:
    def __init__(self, intents_file=None, w2v_model_path=None, svm_model_path=None, label_encoder_path=None):
        self.nlp = spacy.load("en_core_web_sm")

        if intents_file:
            with open(intents_file, "r") as file:
                self.intents = yaml.safe_load(file)
        elif w2v_model_path and svm_model_path and label_encoder_path:
            self.word2vec_model = Word2Vec.load(w2v_model_path)
            self.svm_model = load(svm_model_path)
            self.label_encoder = load(label_encoder_path)
        else:
            raise ValueError("Either intents_file or model paths must be provided")

        if intents_file:
            self.word2vec_model = self.train_word2vec()
            self.svm_model, self.label_encoder = self.train_svm()
        elif w2v_model_path and svm_model_path and label_encoder_path:
            self.word2vec_model = Word2Vec.load(w2v_model_path)
            self.svm_model = load(svm_model_path)
            self.label_encoder = load(label_encoder_path)
        else:
            raise ValueError("Either intents_file or model paths must be provided")

    def train_word2vec(self):
        sentences = []
        for intent, examples in self.intents["intents"].items():
            for example in examples:
                sentences.append(example["text"].split())

        # Train Word2Vec model
        word2vec_model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
        return word2vec_model

    def get_word2vec_features(self, text):
        words = text.split()
        word_vectors = [self.word2vec_model.wv[word] for word in words if word in self.word2vec_model.wv]
        if not word_vectors:
            return np.zeros(self.word2vec_model.vector_size)
        return np.mean(word_vectors, axis=0)

    def train_svm(self):
        texts = []
        labels = []
        for intent, examples in self.intents["intents"].items():
            for example in examples:
                texts.append(example["text"])
                labels.append(intent)

        # Convert texts to Word2Vec features
        X = np.array([self.get_word2vec_features(text) for text in texts])
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(labels)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        svm_model = SVC(kernel='linear')
        svm_model.fit(X_train, y_train)

        return svm_model, label_encoder

    def parse(self, message):
        doc = self.nlp(message)
        lower_doc = self.nlp(message.lower())

        tokens = [token.text for token in doc]
        pos_tags = [(token.text, token.pos_) for token in doc]

        # Combine entities from original and lowercased text
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        lower_entities = [(ent.text, ent.label_) for ent in lower_doc.ents]
        combined_entities = self.combine_entities(entities, lower_entities)

        # Override entities with YAML-specified entities
        yaml_entities = self.extract_yaml_entities(message)

        intent = self.classify_intent(message)

        return intent, yaml_entities if yaml_entities else combined_entities, tokens, pos_tags

    def combine_entities(self, entities, lower_entities):
        entity_dict = {text.lower(): label for text, label in entities}
        for text, label in lower_entities:
            if text.lower() not in entity_dict:
                entity_dict[text.lower()] = label
        return [(text, label) for text, label in entity_dict.items()]

    def extract_yaml_entities(self, message):
        for intent, examples in self.intents["intents"].items():
            for example in examples:
                if example["text"].lower() in message.lower():
                    entities = example.get("entities", [])
                    entity_list = [(word, entity) for word in message.split() for entity in entities if word in example["text"]]
                    return entity_list
        return None

    def classify_intent(self, message):
        features = self.get_word2vec_features(message)
        intent_idx = self.svm_model.predict([features])[0]
        intent = self.label_encoder.inverse_transform([intent_idx])[0]

        return intent

    def save_models(self, w2v_model_path, svm_model_path, label_encoder_path):
        self.word2vec_model.save(w2v_model_path)
        dump(self.svm_model, svm_model_path)
        dump(self.label_encoder, label_encoder_path)

if __name__ == '__main__':
    nlu = NLU(intents_file="yams/intents.yml")
    nlu.save_models("models/word2vec.model", "models/svm_model.joblib", "models/label_encoder.joblib")


# nlu_loaded = NLU(intents_file="intents.yml", w2v_model_path="word2vec.model", svm_model_path="svm_model.joblib", label_encoder_path="label_encoder.joblib")

