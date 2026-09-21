import aiohttp
from typing import List
from .base import BaseSource, JobItem

class ArbeitnowSource(BaseSource):
    name = "arbeitnow"
    BASE_URL = "https://www.arbeitnow.com/api/job-board-api"

    async def fetch_jobs(self, keywords: List[str]) -> List[JobItem]:
        jobs = []
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL) as resp:
                if resp.status != 200:
                    return jobs
                data = await resp.json()
                
                for item in data.get("data", []):
                    title = item.get("title", "")
                    desc = item.get("description", "")
                    tags = item.get("tags", [])
                    
                    combined_text = f"{title} {desc} {' '.join(tags)}".lower()
                    if any(kw.lower() in combined_text for kw in keywords):
                        jobs.append(
                            JobItem(
                                source_id=self.name,
                                original_id=item.get("slug", item.get("title")),
                                title=title,
                                company=item.get("company_name", "Unknown"),
                                location=item.get("location", "Europe / Remote"),
                                url=item.get("url", ""),
                                description=desc,
                                tags=tags
                            )
                        )
        return jobs