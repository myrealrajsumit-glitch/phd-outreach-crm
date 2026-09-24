import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5555))
    print(f"Starting backend on port {port}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
