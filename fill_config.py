import json
import boto3
from botocore.exceptions import ClientError


def get_ssm_parameter(param_name: str) -> str:
    """Fetches a parameter value from AWS Systems Manager Parameter Store."""
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return response['Parameter']['Value']

def load_template(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)

def resolve_env_vars(config: dict) -> dict:
    env_vars = config["ImageRepository"]["ImageConfiguration"]["RuntimeEnvironmentVariables"]
    resolved_env = {}

    for key, param_path in env_vars.items():
        print(f"Fetching parameter: {param_path}")
        try:
            resolved_value = get_ssm_parameter(param_path)
        except:
            message=f'Failed to get parameter: {param_path}'
            print(message)
            resolved_value = param_path
        resolved_env[key] = resolved_value

    config["ImageRepository"]["ImageConfiguration"]["RuntimeEnvironmentVariables"] = resolved_env
    return config

def save_config(config: dict, output_path: str):
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Resolved config written to {output_path}")

if __name__ == "__main__":
    template_path = 'source-config.template.json'
    output_path = 'source-config.json'

    config = load_template(template_path)
    resolved_config = resolve_env_vars(config)
    save_config(resolved_config, output_path)
