from CodingAgent.utils.logging_info import setup_logging_config

logger = setup_logging_config()

def main():
    logger.info("[MAIN]: This is a hello from main.py!")
    print("Hello world")

if __name__ == "__main__":
    main()