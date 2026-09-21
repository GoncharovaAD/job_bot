import aiohttp
from typing import List
from sources.base import BaseSource, JobItem

class JobicySource(BaseSource):
    name = "Jobicy"

    async def fetch_jobs(self, keywords: List[str]) -> List[JobItem]:
        url = "https://jobicy.com/api/v2/remote-jobs"
        results: List[JobItem] = []

        async with aiohttp.ClientSession() as session:
            for kw in keywords:
                # Jobicy API v2 лучше всего принимает таги dev, writing, tech, support
                params = {
                    "count": 50,
                    "tag": kw
                }
                try:
                    async with session.get(url, params=params, timeout=10) as response:
                        if response.status != 200:
                            continue
                        
                        data = await response.json()
                        jobs = data.get("jobs", [])

                        for job in jobs:
                            job_id = str(job.get("id", ""))
                            title = job.get("jobTitle", "")
                            company = job.get("companyName", "")
                            job_url = job.get("url", "")
                            
                            geo = job.get("jobGeo", "Remote")
                            job_type = job.get("jobType", "")
                            location = f"{geo} ({job_type})" if job_type else geo
                            
                            description = job.get("jobExcerpt", "") or job.get("jobDescription", "")
                            
                            tags = []
                            if job.get("jobCategory"):
                                tags.append(job.get("jobCategory"))
                            if job.get("jobLevel"):
                                tags.append(job.get("jobLevel"))

                            results.append(
                                JobItem(
                                    source_id="jobicy",
                                    original_id=job_id,
                                    title=title,
                                    company=company,
                                    location=location,
                                    url=job_url,
                                    description=description,
                                    tags=tags
                                )
                            )
                except Exception as e:
                    print(f"[Jobicy] Ошибка запроса '{kw}': {e}")

        return results