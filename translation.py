#%%
from openai import OpenAI
import tiktoken

class Translator():
  def __init__(self):
    self.model = "gpt-4o"
    self.encoding = tiktoken.encoding_for_model(self.model)
    self.api_key_location = "../keys/openai_key.txt"
    self.client = OpenAI(api_key=self.api_key())
    self.token_count = 0

  def clear_tokens(self):
    self.token_count = 0

  def count_tokens(self):
    return self.token_count

  def api_key(self):
    # read api_key from local file
    with open(self.api_key_location) as f:
      return f.readline()
  
  def num_tokens(self, text):
    # returns the number of tokens that corresponds to the text
    return len(self.encoding.encode(text))

  def chat_prompt(self, prompt):
    # returns the result of a GPT chat prompt
    response = self.client.chat.completions.create(
      model=self.model,
      temperature=0,
      messages=[{"role": "user", "content": prompt}]
    )
    ret = response.choices[0].message.content
    token_price = self.num_tokens(prompt) + self.num_tokens(ret)
    print(f"Exchange complete. Price: {token_price} tokens.")
    self.token_count += token_price
    return ret
  
  def translate_word(self, word, language):
    prompt = f"The following pertains to a scientific article. Translate '{word}' into {language}. Do not include any kind of Romanization."
    return self.chat_prompt(prompt).replace('"', '')

  def translate_text(self, text, language):
    # returns the translation of bare text into any language.
    prompt = f"The following text is an exerpt from a scientific article. Please translate it into {language}: {text}"
    return self.chat_prompt(prompt)

  def translate_xml(self, xml, language):
    # returns the (string of) an xml object after translating its contents into any language.
    prompt = f"The following xml object represents a section of a scientific article. Please translate the text into {language} but please keep all of the xml tags. The format of the response should be an xml object without any extra words at the beginning or end.{xml}"
    return self.chat_prompt(prompt)

#%%
  
tl = Translator()
annyeong = tl.translate_text("hello!", "Korean")
ab = tl.translate_word("Abstract", "Korean")
disc = tl.translate_word("Discussion", "Korean")
print(tl.count_tokens())
print(ab)
print(disc)
print(annyeong)


# TODO:
# MOVE APIKEY INTO FILE OUTSIDE OF REPOSITORY
# WORK ON WEBSITE

# %%
