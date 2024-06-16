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

  def translate_text(self, text, language):
    # returns the translation of bare text into any language.
    prompt = f"The following phrase is an exerpt from a scientific article. Please translate the phrase into {language}: {text}"
    return self.chat_prompt(prompt)

  def translate_xml(self, xml, language):
    # returns the (string of) an xml object after translating its contents into any language.
    prompt = f"The following xml object represents a section of a scientific article. Please translate the contents into {language} but please keep all of the xml tags. The format of the response should be an xml object without any extra words at the beginning or end.{xml}"
    response = self.chat_prompt(prompt)
    i = response.find("<") # start of the xml object
    j = response.rindex(">")+1 # end of the xml object
    return response[i:j]
