from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from datalar.scrapers.schemas import PropertySchema

class ScraperInterface:
    def scrape(self, url: str) -> PropertySchema:
        """
        Scrape property data from the given URL and return a PropertySchema instance.
        
        :param url: The URL of the property listing to scrape.
        :return: An instance of PropertySchema containing the scraped data.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_source_info(self) -> Dict[str, Any]:
        """
        Get information about the source of the scraped data.
        
        :return: A dictionary containing source information such as name, URL, and ID.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")