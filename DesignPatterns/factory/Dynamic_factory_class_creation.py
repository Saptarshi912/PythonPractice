import json
import types


class DynamicClassFactory:
    def __init__(self, config_path):
        self.config_path = config_path
        self.classes = {}
        self._load_config()

    def _load_config(self):
        """Load and parse the JSON config file."""
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        for class_config in config['classes']:
            class_name = class_config['name']
            attributes = class_config.get('attributes', {})
            methods = class_config.get('methods', {})

            # Create method dictionary for dynamic class
            method_dict = {}
            for method_name, method_body in methods.items():
                # Create method from string
                method_code = f"def {method_name}(self, *args, **kwargs):\n"
                for line in method_body.split('\n'):
                    method_code += f"    {line}\n"

                # Execute method code in a new namespace
                namespace = {}
                exec(method_code, namespace)
                method_dict[method_name] = namespace[method_name]

            # Create class dynamically
            def init(self, **kwargs):
                for attr_name, attr_value in attributes.items():
                    setattr(self, attr_name, attr_value)
                for attr_name, attr_value in kwargs.items():
                    setattr(self, attr_name, attr_value)

            # Add __init__ to method dictionary
            method_dict['__init__'] = init

            # Create class using type()
            dynamic_class = type(class_name, (), method_dict)
            self.classes[class_name] = dynamic_class

    def create_instance(self, class_name, **kwargs):
        """Create an instance of a dynamic class."""
        if class_name not in self.classes:
            raise ValueError(f"Class {class_name} not found in config")
        return self.classes[class_name](**kwargs)

    def get_available_classes(self):
        """Return list of available class names."""
        return list(self.classes.keys())


# Example usage
if __name__ == "__main__":
    # Create factory with config file
    factory = DynamicClassFactory("ai_chat_config.json")

    # Print available classes
    print("Available AI Chat APIs:", factory.get_available_classes())

    # Create instances and demonstrate usage
    try:
        # Create Grok instance
        grok = factory.create_instance("Grok", api_key="custom_key_123")
        print("\nGrok instance:")
        print("API Key:", grok.api_key)
        print("Endpoint:", grok.endpoint)
        print("Chat Response:", grok.chat("Hello!"))

        # Create ChatGPT instance
        chatgpt = factory.create_instance("ChatGPT")
        print("\nChatGPT instance:")
        print("API Key:", chatgpt.api_key)
        print("Endpoint:", chatgpt.endpoint)
        print("Chat Response:", chatgpt.chat("Hi there!"))

    except ValueError as e:
        print(f"Error: {e}")