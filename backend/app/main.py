from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.modules.creative.router import router as creative_router
from app.modules.campaign.router import router as campaign_router
from app.modules.data.router import router as data_router
from app.modules.rule.router import router as rule_router
from app.modules.architecture.router import router as arch_router
from app.modules.platform.router import router as platform_router
from app.modules.rebate.router import router as rebate_router
from app.modules.platform.manager import seed_demo_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_demo_data()
    yield


app = FastAPI(title="AdFlow - 自动化投放平台", version="1.0.0", lifespan=lifespan)

app.include_router(creative_router)
app.include_router(campaign_router)
app.include_router(data_router)
app.include_router(rule_router)
app.include_router(arch_router)
app.include_router(platform_router)
app.include_router(rebate_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return FileResponse("static/index.html")
