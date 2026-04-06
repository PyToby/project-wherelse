import google.genai as genai
import os, json
from tavily import TavilyClient, UsageLimitExceededError
from dotenv import load_dotenv

load_dotenv()

class ProcessData:
    '''
    A class to compare two services, package the result and return it formatted.
    Uses GEMINI API (AI processing data) and TAVILY API (AI web and webpage scraping)

    :param service_a: The first of two services being compared.
    :param service_b: The second of two services being compared.
    :return: A dictionary iterable.
    '''

    def __init__(self, service_a: str, service_b: str):
        self.service_a = service_a
        self.service_b = service_b
        self.tv = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.gemini = genai.Client(api_key=os.getenv("API_KEY"))

    def __str__(self) -> str:
        return f"Comparing {self.service_a.upper()} against {self.service_b.upper()}."
    
    def generate_response(self, reddit_data: str, content: str) -> str:
        prompt = """
        You are an expert product analyst. Your job is to produce a structured, honest, and opinionated comparison between two software services based on the source material provided to you.

        You will be given:
        - SERVICE_A: the name of the first service
        - SERVICE_B: the name of the second service
        - SCRAPED_CONTENT: web-scraped articles, feature pages, and review site content
        - REDDIT_DATA: posts and comments from Reddit discussions

        Your task is to synthesise all of this into a single JSON object. Use the source material as your primary evidence. You may supplement with your own knowledge only to fill genuine gaps — never to contradict what the sources say.

        ---

        SERVICES:
        - Service A: {service_a}
        - Service B: {service_b}

        SCRAPED CONTENT:
        {content}

        REDDIT DATA:
        {reddit_data}

        ---

        Return ONLY a valid JSON object. No preamble, no explanation, no markdown fences. The JSON must follow this exact schema:

        {{
        "service_a": "<name>",
        "service_b": "<name>",
        "tldr": "<2-3 sentence honest summary of which tool wins in what context>",
        "verdict": {{
            "winner_overall": "<service name or 'Tie'>",
            "winner_reasoning": "<1-2 sentences explaining the overall winner>",
            "best_for": {{
            "service_a": "<one-line description of ideal user for service A>",
            "service_b": "<one-line description of ideal user for service B>"
            }}
        }},
        "scores": {{
            "service_a": {{
            "ease_of_use": "<integer 1-10>",
            "features": "<integer 1-10>",
            "value_for_money": "<integer 1-10>",
            "performance": "<integer 1-10>",
            "community_support": "<integer 1-10>"
            }},
            "service_b": {{
            "ease_of_use": "<integer 1-10>",
            "features": "<integer 1-10>",
            "value_for_money": "<integer 1-10>",
            "performance": "<integer 1-10>",
            "community_support": "<integer 1-10>"
            }}
        }},
        "pros": {{
            "service_a": ["<pro>", "<pro>", "<pro>"],
            "service_b": ["<pro>", "<pro>", "<pro>"]
        }},
        "cons": {{
            "service_a": ["<con>", "<con>", "<con>"],
            "service_b": ["<con>", "<con>", "<con>"]
        }},
        "community_sentiment": {{
            "service_a": "<short summary of what Reddit and reviewers say about this service>",
            "service_b": "<short summary of what Reddit and reviewers say about this service>",
            "notable_quotes": [
            {{
                "text": "<paraphrased or direct quote>",
                "sentiment": "<positive|negative|neutral>",
                "about": "<service name>"
            }}
            ]
        }},
        "use_case_fit": [
            {{
            "use_case": "<e.g. Solo note-taking>",
            "winner": "<service name or 'Tie'>",
            "reasoning": "<one sentence>"
            }}
        ],
        "sources_used": {{
            "scraped_content_used": "<true|false>",
            "reddit_data_used": "<true|false>",
            "own_knowledge_used": "<true|false>"
        }}
        }}

        Rules:
        - Every string value must be concise. No value should exceed 2 sentences.
        - notable_quotes should contain 2-4 entries.
        - use_case_fit should contain 3-5 entries covering the most relevant use cases for these two services specifically.
        - pros and cons should each contain exactly 3 items per service.
        - Scores must reflect evidence from the sources, not generic assumptions.
        - If the source material is insufficient to score a category confidently, score it 5 and note nothing — do not hallucinate specifics.
        - Do not include any text outside the JSON object.
        """.format(
            service_a=self.service_a,
            service_b=self.service_b,
            content=content,
            reddit_data=reddit_data
        )

        response = self.gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    
    def scrape(self) -> tuple[str, str]:
        '''
        Internet scraping algorithm. Scrapes Reddit and online reviews.
        '''
        reddit_prompt = f"{self.service_a} vs {self.service_b} site:reddit.com"
        prompt = f"{self.service_a} vs {self.service_b} reviews pros cons"
        try:
            reddit_result = self.tv.search(reddit_prompt, max_results=5)
            web_result = self.tv.search(prompt, max_results=10)
        except UsageLimitExceededError:
            return "The application is currently overloaded. Please try again later."

        context = ""
        reddit_context = ""
        for response in web_result["results"]:
            context += f"Source: {response["title"]}\nContent: {response["content"]}\n\n"
        for response in reddit_result["results"]:
            reddit_context += f"Content: {response["content"]}\n\n"        
        
        return context, reddit_context

    def parse_response(self, response:str) -> json:
        '''
        Formats AI response

        :param response: The AI raw response
        :return: Formated JSON string
        '''
        formatted_text = response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(formatted_text)
