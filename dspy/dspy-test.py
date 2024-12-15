import os
import dspy
from dotenv import load_dotenv
from pathlib import Path

root_dir = Path(__file__).parent.parent
dotenv_path = os.path.join(root_dir, '.env')
result = load_dotenv(dotenv_path=dotenv_path)
oai_api_key = os.environ.get('OPENAI_API_KEY')

lm = dspy.LM('openai/gpt-4o-mini', api_key=oai_api_key)
dspy.configure(lm=lm)

# math = dspy.ChainOfThought("question -> answer: float")
# math(question="Two dice are tossed. What is the probability that the sum equals two?")
# print(math)

res1 = lm("Say this is a test!", temperature=0.7)  # => ['This is a test!']
res2 = lm(messages=[{"role": "user", "content": "Say this is a test!"}])  # => ['This is a test!']
print(res1)
print(res2)
