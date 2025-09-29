import json
from pathlib import Path
from diffusers import StableDiffusionPipeline
import torch
from transformers import pipeline


def print_model_info(func):
    """
    Decorator to print model information based on the model type.
    """

    def wrapper(self, *args, **kwargs):
        if isinstance(self, TextToImage):
            print("Text to Image Model Info:")
            info = func(self, *args, **kwargs)
            print([f"{k}: {v}\n" for k, v in info.items()])
        elif isinstance(self, TextGeneration):
            print("Text Generation Model Info:")
            info = func(self, *args, **kwargs)
            print([f"{k}: {v}\n" for k, v in info.items()])
        else:
            print("Unknown model type")
        return func(self, *args, **kwargs)
    return wrapper

class ModelConfigs():
    """
    Class to handle model configurations from a JSON file.

    The model configs should be statically defined outside of the program and not require user input.

    Setting configs to private to prevent modification after initialization. [ENCAPSULATION]
    """
    def __init__(self, config_path: str):

        if not Path(config_path).is_file():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        else:
            with open(Path(config_path), mode='r') as f:
                model_configs = json.loads(f.read())

        self.__configs = model_configs

    def show_configs(self) -> dict:
        return self.__configs
    

class AIModelFactory():
    """
    Factory class to create AI model instances based on configurations.

    The factory does not own the instances it creates.
    """
    def get_text_to_image_model(self, model_configs: ModelConfigs):

        model_configurations = model_configs.show_configs()

        if model_configurations.get("Text-To-Image") is not None:
            return TextToImage(model_configurations["Text-To-Image"])

    def get_text_generation_model(self, model_configs: ModelConfigs):

        model_configurations = model_configs.show_configs()

        if model_configurations.get("Text-Generation") is not None:
            return TextGeneration(model_configurations["Text-Generation"])

class TextToImage():
    """
    Class to handle text-to-image generation using a specified model.

    """
    def __init__(self, model_configs: dict):
        # Model information
        self.name = model_configs.get("name")
        self.version = model_configs.get("version")
        self.type = model_configs.get("type") 
        self.author = model_configs.get("author")
        self.description = model_configs.get("description")

        # Model configuration
        self.__pipe = StableDiffusionPipeline.from_pretrained(self.name, dtype=torch.float16)

    def generate_image(self, prompt, num_inference_steps=50, guidance_scale=7.5):
        assert isinstance(prompt, str), "Prompt should be a string"

        return self.__pipe(prompt).images[0]  

    def save_image(self, image, file_path: str):
        """ 
        Save the generated image to a file.

        Only file format supported is PNG for now.
        """
        image.save("astronaut_rides_horse.png")

    def display_image(self, image):
        """
        Display the generated image.
        """
        return image.show()

    @print_model_info
    def get_info(self) -> str:
        """
        Print the model information.
        """
        return {"name": self.name, "version": self.version, "type": self.type, "author": self.author, "description": self.description}
    
class TextGeneration():
    """
    Class to handle text generation using a specified model.

    This is a high-level implementation so the token output will be relatively slow compared to optimized implementations.
    """
    def __init__(self, model_configs: dict):
        # Model information
        self.name = model_configs.get("name")
        self.version = model_configs.get("version")
        self.type = model_configs.get("type") 
        self.author = model_configs.get("author")
        self.description = model_configs.get("description")

        # Model configuration
        self.__pipe = pipeline("text-generation", model=self.name, model_kwargs={"dtype": torch.bfloat16})
        self.messages = []

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response based on the user input, and append the user prompt and model response to self.messages.
        """
        self.messages.append(f"User: {prompt}")
        model_response = self.__pipe(str(prompt))
        print(model_response[0]['generated_text'])
        self.messages.append(f"Model: {model_response[0]['generated_text']}")
        
        return model_response

    def save_conversation(self, image, file_path: str):
        """
        Save the conversation history to a text file.
        """
        message_history = ("\n").join([msg for msg in self.messages])

        with open(Path(file_path), "w") as f:
            f.write(message_history)

    def display_message_history(self):
        """ 
        Display the conversation history.
        """
        return ("\n").join([msg for msg in self.messages])

    @print_model_info
    def get_info(self) -> str:
        """
        Print the model information.
        """
        return {"name": self.name, "version": self.version, "type": self.type, "author": self.author, "description": self.description}
