from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
