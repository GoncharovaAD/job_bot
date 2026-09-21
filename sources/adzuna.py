import aiohttp
from typing import List
from .base import BaseSource, JobItem

class AdzunaSource(BaseSource):
    name = "adzuna"
    # Поддерживаемые страны Европы в Adzuna API
    EU_COUNTRIES = ["gb", "de", "nl", "fr", "at", "ch", "pl", "es", "it"]

    def __init__(self, app_id: str, app_key: str):
        self.app_id = app_id
        self.app_key = app_key

    async def fetch_jobs(self, keywords: List[str]) -> List[JobItem]:
        if not self.app_id or not self.app_key:
            return []

        jobs = []
        query = " ".join(keywords[:3])

        async with aiohttp.ClientSession() as session:
            for country_code in self.EU_COUNTRIES:
                url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
                params = {
                    "app_id": self.app_id,
                    "app_key": self.app_key,
                    "what": query,
                    "results_per_page": 10
                }
                try:
                    async with session.get(url, params=params) as resp:
                        if resp.status != 200:
                            continue
                        data = await resp.json()

                        for item in data.get("results", []):
                            loc_display = item.get("location", {}).get("display_name", country_code.upper())
                            jobs.append(
                                JobItem(
                                    source_id=self.name,
                                    original_id=str(item.get("id")),
                                    title=item.get("title", ""),
                                    company=item.get("company", {}).get("display_name", "Unknown"),
                                    location=loc_display,
                                    url=item.get("redirect_url", ""),
                                    description=item.get("description", ""),
                                    tags=[item.get("category", {}).get("label", "")]
                                )
                            )
                except Exception as e:
                    print(f"Adzuna error for country {country_code}: {e}")
        return jobs