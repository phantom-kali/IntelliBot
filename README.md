# Lemme know you were here, click the ★

# IntelliBot

IntelliBot is a customizable chatbot framework designed to handle natural language understanding (NLU) and dialogue management tasks efficiently. This project leverages libraries such as spaCy, scikit-learn, and Word2Vec to create a robust conversational agent capable of handling various intents and providing relevant responses.

## Features

- **Natural Language Understanding (NLU)**: Identifies user intents and extracts entities using spaCy and scikit-learn.
- **Dialogue Management**: Generates contextually appropriate responses based on user intents.
- **Action Execution**: Executes predefined actions based on user inputs.
- **Configurable Responses**: Easily modify responses through a YAML configuration file.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/phantom-kali/IntelliBot.git
    cd IntelliBot
    ```

2. Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have your virtual environment activated:
    ```bash
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Run the bot:
    ```bash
    python main.py
    ```

3. Interact with the bot by typing in user inputs.

## Configuration

### intents.yml

Define your intents and their associated training examples. Example:

```yaml
intents:
  greet:
    - text: "Hi, my name is [name]."
      entities:
        - name
    - text: "Hello, I'm [username]."
      entities:
        - username
    - text: "Good morning!"
    - text: "Hey there!"
  book_table:
    - text: "I'd like to book a table for [number] people."
      entities:
        - number
    - text: "Can I reserve a table for [number]?"
      entities:
        - number
    - text: "Table for [number], please."
      entities:
        - number
```

### responses.yml

Define your responses for each intent. Example:

```yaml
intents:
  greet:
    entities:
      - PERSON
    responses:
      - text: "Hello[PERSON]! How can I assist you today?"
      - text: "Hi there[PERSON]! What can I do for you?"
      - text: "Hey[PERSON]! How may I help you?"
  book_table:
    responses:
      - text: "Sure! How many people would you like to book the table for?"
      - text: "Certainly! For how many guests should I book the table?"
    action: book_table_action
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
