import json
from pathlib import Path
from diffusers import StableDiffusionPipeline
import torch
from transformers import pipeline


class ModelConfigs():
    """
    Class to handle model configurations from a JSON file.

    The model configs should be statically defined outside of the program and not require user input.
    """
    def __init__(self, config_path: str):

        if not Path(config_path).is_file():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        else:
            with open(Path(config_path), mode='r') as f:
                model_configs = json.loads(f.read())

        self.configs = model_configs

    def show_configs(self) -> dict:
        return self.configs
    

class AIModelFactory():
    """
    Factory class to create AI model instances based on configurations.

    The factory does not own the instances it creates.
    """
    def get_text_to_image_model(self, model_configs: ModelConfigs):

        if model_configs.configs.get("Text-To-Image") is not None:
            return TextToImage(model_configs.configs["Text-To-Image"])

    def get_text_generation_model(self, model_configs: ModelConfigs):

        if model_configs.configs.get("Text-Generation") is not None:
            return TextGeneration(model_configs.configs["Text-Generation"])


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
        self.pipe = StableDiffusionPipeline.from_pretrained(self.name, dtype=torch.float16)

    def generate_image(self, prompt, num_inference_steps=50, guidance_scale=7.5):
        assert isinstance(prompt, str), "Prompt should be a string"

        return self.pipe(prompt).images[0]  

    
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

    def print_info(self) -> str:
        """
        Print the model information.
        """
        return f"Model Name: {self.name}\nVersion: {self.version}\nType: {self.type}\nAuthor: {self.author}\nDescription: {self.description}"
    

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
        self.pipe = pipeline("text-generation", model=self.name, model_kwargs={"dtype": torch.bfloat16})
        self.messages = []

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response based on the user input, and append the user prompt and model response to self.messages.
        """
        self.messages.append(f"User: {prompt}")
        model_response = self.pipe(prompt)
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

    def print_info(self) -> str:
        """
        Print the model information.
        """
        return f"Model Name: {self.name}\nVersion: {self.version}\nType: {self.type}\nAuthor: {self.author}\nDescription: {self.description}"