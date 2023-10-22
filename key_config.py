import json

def get_openai_key():
    with open('OAI_CONFIG_LIST.json', 'r') as f:
        config_list = json.load(f)
        valid_models = ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"]
        filtered_configs = [conf for conf in config_list if conf["model"] in valid_models]
        if filtered_configs:
            return filtered_configs[0]['api_key']
        else:
            raise ValueError("No valid API key found in the configuration file.")
