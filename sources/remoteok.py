import httpx
from typing import List
from .base import BaseSource, JobItem

class RemoteOKSource(BaseSource):
    def __init__(self):
        super().__init__("remoteok")
        self.api_url = "https://remoteok.com/api"

    async def fetch_jobs(self, search_keywords: List[str]) -> List[JobItem]:
        jobs: List[JobItem] = []
        headers = {"User-Agent": "JobStormBot/2.2 (Technical Detective Bot)"}

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(self.api_url, headers=headers)
                if response.status_code != 200:
                    return jobs
                
                data = response.json()
                # Первый элемент в массиве RemoteOK — это системная строка с описанием API
                if isinstance(data, list) and len(data) > 0:
                    job_entries = data[1:]
                else:
                    job_entries = []

                for item in job_entries:
                    # Проверяем, что это действительно словарь с данными вакансии
                    if not isinstance(item, dict):
                        continue

                    title = item.get("position", "")
                    company = item.get("company", "Unknown")
                    url = item.get("url", item.get("apply_url", ""))
                    location = item.get("location", "Remote")
                    tags = item.get("tags", [])
                    description = item.get("description", "")

                    if not title or not url:
                        continue

                    # Проверяем, подходит ли вакансия под хотя бы одно ключевое слово
                    searchable_text = f"{title} {' '.join(tags)} {description}".lower()
                    matched = any(kw.lower() in searchable_text for kw in search_keywords)

                    if matched:
                        # Корректируем ссылку, если она относительная
                        if url.startswith("/"):
                            url = f"https://remoteok.com{url}"

                        jobs.append(
                            JobItem(
                                title=title,
                                company=company,
                                location=location if location else "Remote",
                                url=url,
                                source_id=self.name,
                                tags=tags if isinstance(tags, list) else [str(tags)]
                            )
                        )
        except Exception as e:
            print(f"Error fetching from RemoteOK: {e}")

        return jobs