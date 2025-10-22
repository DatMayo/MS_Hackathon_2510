"""
Module for generating fake news articles using OpenAI's API.

This module provides functionality to generate plausible-sounding but entirely
fictional articles that fit within specified categories, designed to be used
in a trivia game setting.
"""

import json
from typing import Optional
from colorama import init, Fore, Style

from src.game.models.category import CategoryModel

# Initialize colorama for colorful console output
init(autoreset=True)

from openai import OpenAI

from src.config.settings import OPENAI_API_KEY, WIKI_MAX_SENTENCE_LENGTH, GAME_DEFAULT_ROUNDS
from src.game.models.article import ArticleModel


class FakeNewsGenerator:
    """
    A class to generate fake news articles using OpenAI's API.

    This class provides methods to generate fake news articles that are
    plausible-sounding but entirely fictional, designed to be used as
    distractors in a trivia game.
    """

    @staticmethod
    def _generate_from_api(client: OpenAI, category: str) -> Optional[ArticleModel]:
        """
        Generate a fake news article using the OpenAI API.

        Args:
            client: An instance of the OpenAI client.
            category: The category for which to generate a fake article.

        Returns:
            ArticleModel: A dictionary containing the generated article's title,
                        summary, category, and truth status, or None if an error occurs.

        Note:
            This is an internal method and should not be called directly.
            Use the `generate()` method instead.
        """
        system_prompt = f"""
        You are an AI assistant for a trivia game. You will create a plausible-sounding
        but entirely fictional subject that fits a given category.
        Generate a fake Wikipedia article "title" and a one-paragraph "summary".
        The summary must be about {WIKI_MAX_SENTENCE_LENGTH} sentences long and sound encyclopedic.
        Respond ONLY with a valid JSON object with "title" and "summary" keys. Respond only in English.
        """
        user_prompt = f"Category: {category}"

        try:
            response = client.chat.completions.create(
                model="gpt-5-nano",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=1,
                timeout=30,  # Add timeout for API calls
            )

            if not response.choices or not response.choices[0].message.content:
                print(f"{Fore.YELLOW}Warning: Empty response from OpenAI API")
                return None

            data = json.loads(response.choices[0].message.content)

            # Validate required fields
            if not data.get("title") or not data.get("summary"):
                print(
                    f"{Fore.YELLOW}Warning: Incomplete response from OpenAI API - missing title or summary"
                )
                return None

            article: ArticleModel = {
                "title": data.get("title"),
                "summary": data.get("summary"),
                "category": category,
                "is_truth": False,
            }
            return article

        except json.JSONDecodeError as e:
            print(f"{Fore.RED}Error: Failed to parse JSON response from OpenAI API: {e}")
            return None
        except Exception as e:
            print(f"{Fore.RED}API Error: {e}")
            return None

    @staticmethod
    def generate(category: str) -> Optional[ArticleModel]:
        """
        Generate a fake news article for the specified category.

        Args:
            category: The category for which to generate a fake article.

        Returns:
            Optional[ArticleModel]: A dictionary containing the generated article's
                                 details, or None if generation fails or if the
                                 API key is not configured.

        Example:
            >>> article = FakeNewsGenerator.generate("Science")
            >>> if article:
            ...     print(article['title'])
            ...     print(article['summary'])
        """
        # Input validation
        if not category or not isinstance(category, str):
            print(
                f"{Fore.RED}Error: Invalid category provided. Category must be a non-empty string."
            )
            return None

        if not OPENAI_API_KEY:
            print(
                f"{Fore.RED}Error: OPENAI_API_KEY not found. Please configure your OpenAI API key."
            )
            return None

        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            return FakeNewsGenerator._generate_from_api(client, category)
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to initialize OpenAI client: {e}")
            return None

    @staticmethod
    def generate_all(categories: list[CategoryModel], rounds: int = GAME_DEFAULT_ROUNDS) -> list[ArticleModel]:
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            articles = []
            for category in categories:
                system_prompt = f"""
                        You are an AI assistant for a trivia game. You will create a plausible-sounding
                        but entirely fictional subject that fits a given category.
                        Generate a fake Wikipedia article "title" and a one-paragraph "summary".
                        The summary must be about {WIKI_MAX_SENTENCE_LENGTH} sentences long and sound encyclopedic.
                        Give me the answer in JSON array format only.
                        The array should contain
                        [{{'title': 'Generated Title', 'summary': 'Generated Summary'}}, {{'title': 'Generated Title', 'summary': 'Generated Summary'}}]
                        """
                user_prompt = f"Category: {category.name}"

                response = client.chat.completions.create(
                    model="gpt-5-nano",
                    response_format={"type": "json"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=1,
                    timeout=30,  # Add timeout for API calls
                )

                if not response.choices or not response.choices[0].message.content:
                    print(f"{Fore.YELLOW}Warning: Empty response from OpenAI API")
                    return None

                data = json.loads(response.choices[0].message.content)

                # Validate required fields
                if len(data) != rounds or data != type(dict):
                    print(
                        f"{Fore.YELLOW}Warning: Incomplete response from OpenAI API - missing title or summary"
                    )
                    return None

                for entry in data:
                    articles.append({
                        "title": entry.get("title"),
                        "summary": entry.get("summary"),
                        "category": category.name,
                        "is_truth": False,
                    })


            return articles
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to initialize OpenAI client: {e}")
            return None

        # default: list[ArticleModel] = [{'category': 'UFO_sightings', 'is_truth': False, 'summary': 'The Lumen Vale Synthesis Incident references a series of unidentified aerial phenomena observed over the Lumen Vale region in the spring of 1964. Eyewitnesses reported a luminous, morphing object that appeared to oscillate between solid and radiant states. Concurrent radar readings showed anomalous returns that fluctuated in size and velocity, resisting straightforward classification. Geochemical and atmospheric analyses of nearby samples indicated trace anomalies later interpreted as atmospheric artifacts rather than material from a craft. A government inquiry was initiated and a confidential report circulated among researchers, with portions later released to the public in the 1980s. Today the incident is cited in ufology as a canonical example of how ambiguous sightings, inconsistent instrumentation, and limited data can fuel ongoing speculation about unidentified aerial phenomena.', 'title': 'The Lumen Vale Synthesis Incident'}, {'category': 'UFO_sightings', 'is_truth': False, 'summary': 'The Lumenfall Ridge Encounter is a widely cited but contested UFO sighting reported near the Lumenfall Ridge area in northern Nevada during the late 1980s. Witnesses described a hovering, pearlescent or metallic disk that emitted a diffuse glow and remained in view for several minutes before accelerating vertically out of sight. Local authorities and a small group of amateur astronomers conducted interviews and collected meteorological and radar data in the days following the event. In the ensuing years, researchers attempted to explain the observation with a range of hypotheses, including atmospheric plasma phenomena, misidentified aircraft, and covert drone activity. Despite multiple field reports and media coverage, no unambiguous physical evidence has been published, and the incident remains unresolved. The case continues to be cited in ufology texts as a benchmark for eyewitness testimony and the challenges of corroborating aerial phenomena.', 'title': 'Lumenfall Ridge Encounter'}, {'category': 'Paranormal', 'is_truth': False, 'summary': 'The Dusk Harbor Phantasm is a paranormal phenomenon reported in the harbor town of Duskport, first documented in late 19th-century municipal records. It is described as an ethereal figure appearing on foggy evenings near the old quay, projecting a faint bioluminescent glow. Eyewitness accounts vary, but common elements include a translucent sailor, a receding tide, and a muffled chorus of distant bells. Scientific examination by local researchers in the early 20th century suggested environmental factors such as sea fog, static electricity, and trace phosphorescent minerals, though no physical evidence was produced. The phenomenon has inspired local folklore, including songs and legends about lost crewmen who haunt the harbor until a ceremonial bell is rung at dusk. Modern documentation relies on a combination of archival newspaper reports and contemporary citizen science observations, though skeptics have argued that the sightings correlate with tidal cycles and expectancy effects.', 'title': 'The Dusk Harbor Phantasm'}, {'category': 'Paranormal', 'is_truth': False, 'summary': 'The Cassiopeia Whisper is a purported paranormal phenomenon described as faint, patterned auditory signals detected in the vicinity of the Cassiopeia constellation. First documented by a network of amateur radio operators in 2012, the signals were reported as repeating phrases that seemed to correspond to nautical calls and weather lore. Proponents argue that the patterns show linguistic structure and cross-receiver consistency, while skeptics attribute the reports to radio interference, pareidolia, or misinterpretation of natural sounds. Investigations conducted by the fictional Institute for Anomalous Phenomena found no reproducible physical mechanism, but noted transient correlations with geomagnetic activity during some observation windows. The phenomenon has influenced local folklore in several towns near observatories, where residents exchange anecdotal accounts and organize annual symposia on anomalous sound phenomena. As of the most recent assessments, there is no consensus on the causal explanation, and the Cassiopeia Whisper remains a controversial subject within paranormal research, cited more for its methodological debates than for any verifiable effects.', 'title': 'The Cassiopeia Whisper'}, {'category': 'Fringe_theories', 'is_truth': False, 'summary': 'The Urban Leyline Theory posits that lines of energetic resonance, analogous to traditional ley lines, traverse major urban centers and influence cultural, psychological, and perceptual phenomena. Proponents claim that alignments of monuments, street grids, and historical sites correspond to a network of invisible vectors that shape collective memory and decision-making. They argue for modest but detectable anomalies in environmental measurements—such as electromagnetic activity and atmospheric readings—when conducted near these urban corridors. Critics maintain that the theory rests on correlation rather than causation and suffers from selection bias and a lack of replicable experiments. Despite skepticism, the concept has permeated fringe literature, speculative architecture, and certain countercultural movements, where it is presented as a speculative framework rather than established science. The Urban Leyline Theory remains a subject of interest primarily within sociology of science and paranormal studies, used more as a thought experiment than as a predictive model.', 'title': 'Urban Leyline Theory'}, {'category': 'Fringe_theories', 'is_truth': False, 'summary': 'The Aetheric Trace Theory is a fringe hypothesis proposing that remnants of past events imprint a subtle, non-material field in the environment, detectable under specialized resonance conditions. Proponents claim that long-standing anomalies in radio, acoustic, and electromagnetic data correspond to historical events, suggesting information is preserved in this aetheric trace layer. The theory posits a two-tier reality in which a physical substrate coexists with an information-carrying field that interacts with human perception and sensor arrays at low frequencies. Experimental reports are controversial, with supporters citing occasional signal alignments while critics point to insufficient controls, data dredging, and lack of reproducibility. Mainstream physics remains highly skeptical, arguing that observed effects can be explained by known environmental factors and that predictive tests have not consistently supported the theory. Nevertheless, the Aetheric Trace Theory has generated a small but persistent community of researchers who pursue exploratory measurements for archival science and artifact authentication, while urging rigorous methodological standards.', 'title': 'Aetheric Trace Theory'}]
        return ai_articles