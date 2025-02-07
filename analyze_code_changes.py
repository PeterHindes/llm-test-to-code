# Copyright 2023 Sagi Shnaidman (sshnaidm at gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import openai
import sys

# Set up OpenAI credentials
if not os.environ.get("OPENAI_API_KEY"):
    print("No OpenAI API key found")
    sys.exit(1)

global client
if not os.environ.get("OPENAI_API_BASEURL"):
    client = openai.OpenAI(api_key= os.getenv("OPENAI_API_KEY"))
else:
    client = openai.OpenAI(api_key= os.getenv("OPENAI_API_KEY"), base_url= os.getenv("OPENAI_API_ROUTE"))

model_engine = os.environ["MODEL"]

prompt = os.getenv("PROMPT")
with open(os.getenv("FILE"), "r") as f:
    prompt+= f"\n{f.read()}"
print(f"Prompt: {prompt}")
kwargs = {
    'model': model_engine,
    'messages': [
        {"role": "system", "content": "You are a helpful assistant and code reviewer. Explain the changes in the code and suggest improvements."},
        {"role": "user", "content": prompt},
    ]
}
try:
    response = client.chat.completions.create(**kwargs)
    if response.choices:
        review_text = response.choices[0].message.content.strip()
    else:
        review_text = f"No correct answer from OpenAI!\n{response.text}"
except Exception as e:
    review_text = f"OpenAI failed to generate a review: {e}"

print(f"Response>\n{review_text}")
with open("review.txt", "w") as f:
    f.write(review_text)
