from fastapi import FastAPI
#from app.api.summarization_service import router as summarization_router  
from app.api.transcription_service import router as transcription_router

app = FastAPI()

#app.include_router(summarization_router, prefix="/summarization")
app.include_router(transcription_router, prefix="/transcription")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)