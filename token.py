class Token:
  def __init__(self):
    self.content = []

  def add_content(self, content):
    self.content.append(content)

  def close(self):
    if len(self.content) == 0:
      raise Exception("Content for token '" + self.token_name() + "' is missing")
