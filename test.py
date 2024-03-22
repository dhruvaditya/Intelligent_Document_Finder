from dotenv import load_dotenv
import os

load_dotenv()

s_key=os.environ["secret"]
print(s_key)
algo=os.getenv('OPENAI_KEY')
print(algo)