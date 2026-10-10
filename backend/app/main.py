from fastapi import FastAPI

app = FastAPI(
    title="AI Interviewer API",
    description="Backend API for the AI Interviewer Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "AI Interviewer API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }