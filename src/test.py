import os

from dotenv import load_dotenv


def main():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is configured.")
    else:
        print("OPENAI_API_KEY is missing.")


if __name__ == "__main__":
    main()
