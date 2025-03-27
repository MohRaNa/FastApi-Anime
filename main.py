from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List 

app = FastAPI()

# In-memory storage for our data
anime_db = []
creator_db = []

class Creator(BaseModel):
    name: str
    role: str

class Anime(BaseModel):
    name: str
    genre: List[str]
    creator: Creator
    episodes: int

## ANIME POST GET METHODS
@app.post('/anime')
def post_anime(anime: Anime):
    try:
        # Check if anime already exists
        if any(a.name == anime.name for a in anime_db):
            raise HTTPException(status_code=400, detail=f"{anime.name} is already in the library")
        
        anime_db.append(anime)
        return {"message": f"{anime.name} successfully added to the library"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get('/anime/{anime_name}', response_model=Anime)
def get_anime_name(anime_name: str):
    try:
        target = next((a for a in anime_db if a.name == anime_name), None)
        if target is None:
            raise HTTPException(status_code=404, detail=f"{anime_name} is not found in the library")
        return target
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

## CREATOR POST GET 
@app.post('/creator')
def post_creator(creator: Creator):
    try:
        # Check if creator already exists
        if any(c.name == creator.name for c in creator_db):
            raise HTTPException(status_code=400, detail=f"{creator.name} is already in the library")
        
        creator_db.append(creator)
        return {"message": f"{creator.name} successfully added to the library"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get('/creator/{creator_name}', response_model=Creator)
def get_creator(creator_name: str):
    try:
        target = next((c for c in creator_db if c.name == creator_name), None)
        if target is None:
            raise HTTPException(status_code=404, detail=f"{creator_name} is not found in the library")
        return target
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# INIT
@app.get('/')
def root():
    return {"Api": "Anime"}