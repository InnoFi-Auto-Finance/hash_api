import yaml

with open("apprunner.yaml", "r") as f:
    data = yaml.safe_load(f)

print(data)
