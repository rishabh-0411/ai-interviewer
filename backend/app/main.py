from fastapi import FastAPI

from app.api.routes.candidates import router as candidates_router
from app.api.routes.interviews import router as interviews_router
from app.api.routes.interview_questions import (
    router as interview_questions_router,
)

app = FastAPI(
    title="AI Interviewer API",
    description="Backend API for the AI Interviewer Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "AI Interviewer API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(candidates_router)
app.include_router(interviews_router)
app.include_router(interview_questions_router)