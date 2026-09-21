import aiohttp
from typing import List
from .base import BaseSource, JobItem

class RemotiveSource(BaseSource):
    name = "remotive"
    BASE_URL = "https://remotive.com/api/remote-jobs"

    async def fetch_jobs(self, keywords: List[str]) -> List[JobItem]:
        jobs = []
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL) as resp:
                if resp.status != 200:
                    return jobs
                data = await resp.json()
                
                for item in data.get("jobs", []):
                    title = item.get("title", "")
                    desc = item.get("description", "")
                    category = item.get("category", "")
                    
                    combined_text = f"{title} {desc} {category}".lower()
                    if any(kw.lower() in combined_text for kw in keywords):
                        jobs.append(
                            JobItem(
                                source_id=self.name,
                                original_id=str(item.get("id")),
                                title=title,
                                company=item.get("company_name", "Unknown"),
                                location=item.get("candidate_required_location", "Remote"),
                                url=item.get("url", ""),
                                description=desc,
                                tags=[category] + item.get("tags", [])
                            )
                        )
        return jobs