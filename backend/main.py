from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
# from mcp.router import router as mcp_router
from backend.mcp.router import router as mcp_router


app = FastAPI(title="AgentDock MCP Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #for dev, allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mcp_router, prefix="/mcp")

@app.get("/")
def root():
    return {"message": "AgentDock is live"}