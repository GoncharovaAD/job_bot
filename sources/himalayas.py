import httpx
from typing import List
from .base import BaseSource, JobItem

class HimalayasSource(BaseSource):
    def __init__(self):
        super().__init__("himalayas")
        self.api_url = "https://himalayas.app/api/search"

    async def fetch_jobs(self, search_keywords: List[str]) -> List[JobItem]:
        jobs: List[JobItem] = []
        headers = {"User-Agent": "JobStormBot/2.2"}

        async with httpx.AsyncClient(timeout=15.0) as client:
            for kw in search_keywords:
                try:
                    params = {"q": kw, "limit": 20}
                    response = await client.get(self.api_url, params=params, headers=headers)
                    
                    if response.status_code != 200:
                        continue

                    data = response.json()
                    # Himalayas возвращает список или словарь с ключом 'jobs'
                    job_list = data.get("jobs", []) if isinstance(data, dict) else data

                    if not isinstance(job_list, list):
                        continue

                    for item in job_list:
                        title = item.get("title", "")
                        company = item.get("company_name", item.get("company", {}).get("name", "Unknown"))
                        url = item.get("url", item.get("application_link", ""))
                        location = item.get("location", item.get("location_restriction", "Remote"))
                        categories = item.get("categories", [])
                        skills = item.get("skills", [])

                        if not title or not url:
                            continue

                        tags = [str(c) for c in categories] + [str(s) for s in skills]

                        jobs.append(
                            JobItem(
                                title=title,
                                company=company,
                                location=location if location else "Remote",
                                url=url,
                                source_id=self.name,
                                tags=tags
                            )
                        )
                except Exception as e:
                    print(f"Error fetching Himalayas for keyword '{kw}': {e}")

        return jobs