import requests
import urllib
import string
import re
import json

class Blackbox:
  def __init__(self):
      self.url = 'https://www.blackbox.ai/api/chat'
      self.headers = self._get_headers()

  def _get_headers(self) -> dict:
      return {
          'Content-Type': 'application/json',
          'Cookie': 'sessionId=f77a91e1-cbe1-47d0-b138-c2e23eeb5dcf; intercom-id-jlmqxicb=4cf07dd8-742e-4e3f-81de-38669816d300; intercom-device-id-jlmqxicb=1eafaacb-f18d-402a-8255-b763cf390df6; intercom-session-jlmqxicb=',
          'Origin': 'https://www.blackbox.ai',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
      }

  def _format_response(self, response: str) -> str:
      response = re.sub(r"\$~~~\$\[{.*}\]\$~~~\$", "", response)
      response = re.sub(r'\$@\$v=.*?\n.*?\n.*?\n.*?\n', '', response)
      response = re.sub(r'\$@\$.+?\$', '', response)
      response = re.sub(r'\@\$|@\$', '', response)
      if response:
          return response

  def request(self, content: str, user_system_prompt: str = None) -> dict:
      if not content:
          raise ValueError("Content is required")

      payload = {
          "agentMode": {},
          "codeModelMode": True,
          "id": "XM7KpOE",
          "isMicMode": False,
          "maxTokens": None,
          "messages": [
              {
                  "id": "XM7KpOE",
                  "content": urllib.parse.unquote(content),
                  "role": "user"
              }
          ],
          "previewToken": None,
          "trendingAgentMode": {},
          "userId": "87cdaa48-cdad-4dda-bef5-6087d6fc72f6",
          "userSystemPrompt": user_system_prompt
      }
      try:
          response = requests.post(self.url, json=payload, headers=self.headers)
          response.raise_for_status()  # Raise an exception for bad status codes
          results = self._format_response(response.text)
          return {"success": True, "answer": results, "join": "@Lectures_For_JEE"}
      except requests.exceptions.RequestException as e:
          return {"error": str(e)}
      except Exception as e:
          return {"error": str(e)}

  def details(self) -> dict:
      return {"url": self.url, "headers": self.headers}
