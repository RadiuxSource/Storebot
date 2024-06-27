import requests
import asyncio
from functools import lru_cache

@lru_cache(maxsize=None) 
async def get_teachers(subject):
    response = requests.get(f"https://zenova-lec-api.vercel.app/teachers?subject={subject}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

@lru_cache(maxsize=None)  
async def get_chapters(subject, teacher_name):
    response = requests.get(f"https://zenova-lec-api.vercel.app/chapters?subject={subject}&teacher={teacher_name}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# @lru_cache(maxsize=None)  
async def get_lecture_link(subject, teacher_name, chapter_name):
    response = requests.get(f"https://zenova-lec-api.vercel.app/lecture?subject={subject}&teacher={teacher_name}&ch={chapter_name}")
    if response.status_code == 200:
        return response.json()["link"]
    else:
        return None