class ActionExecutor:
    def __init__(self):
        self.action_functions = {
            "book_table_action": self.book_table,
            "exit_action": self.exit
        }

    def execute(self, action):
        action_function = self.action_functions.get(action)
        if action_function:
            action_function()
        else:
            print(f"No function mapped for action: {action}")

    def book_table(self):
        print("Executing book_table action...")

    def exit(self):
        print("Exiting...")
