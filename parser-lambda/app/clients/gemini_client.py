import json
import google.generativeai as genai

from config import settings


class GeminiClient:
    def __init__(self):
        """
        Initialize the GeminiClient with API credentials.
        """
        genai.configure(api_key=settings.gemini.api_key)

    def call_gemini(self, extracted_text, extracted_links, prompt):
        """
        Call Google's Generative AI with a prompt based on the extracted text and links.
        :param extracted_text: The text extracted from the resume.
        :param extracted_links: The links extracted from the resume.
        :param prompt: The prompt to be used for the Generative AI.
        :return: A JSON string containing the structured response.
        """

        self.prompt = prompt.format(text=extracted_text)

        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(self.prompt)

        if not response:
            raise Exception("Failed to get a response from Google's Generative AI.")

        return self.__parse_gemini_content(response.text)

    def __parse_gemini_content(self, response_text):
        """
        Parse the response from Google's Generative AI in order to get a structured json.
        :param response_text: The text response from the AI.
        :return: A structured JSON object containing the parsed content.
        """
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        clean_json = response_text[start:end]

        parsed_data = json.loads(clean_json)

        return parsed_data
