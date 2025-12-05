from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.auth_router import router as auth_router
from routers.learning_history_router import router as learning_history_router
from routers.learning_hours_router import router as learning_hours_router
from routers.login_issue_router import router as login_issue_router
from routers.content_completion_router import router as content_completion_router
from routers.work_profile_router import router as work_profile_router
from routers.analytics_table_router import router as analytics_table_router

app = FastAPI(title="Learning Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth
app.include_router(auth_router, prefix="/auth")

# Features
app.include_router(learning_history_router)
app.include_router(learning_hours_router)
app.include_router(login_issue_router)
app.include_router(content_completion_router)
app.include_router(work_profile_router)
app.include_router(analytics_table_router)
