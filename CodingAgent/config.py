"""Configuration handling for the coding agent."""
import yaml
import os
import importlib.resources


def write_config():
    """Write configuration to a YAML file."""
    log_dir = os.path.join(os.getcwd(), "log")
    print("log dir: ", log_dir)

    # Write into yaml file
    config_data = {
        "log_dir_home": log_dir,
    }

    # Write to YAML file
    with open("./CodingAgent/config.yaml", "w") as yaml_file:
        yaml.dump(config_data, yaml_file, default_flow_style=False)

    print("Configuration written to config.yaml")


def load_config():
    """Load configuration from the YAML file.
    
    Returns:
        dict: Configuration data.
    """
    with importlib.resources.files("CodingAgent").joinpath("config.yaml").open("r") as f:
        config = yaml.safe_load(f)
    return config


if __name__ == "__main__":
    write_config()
