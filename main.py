from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
import uvicorn

app = FastAPI()

# Allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>Recipe AI 🍳</title>
        <style>
            body { font-family: Arial; background-color: #f9f9f9; text-align: center; padding: 50px; }
            textarea { width: 400px; height: 100px; padding: 10px; }
            button { background: #ff6f00; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>AI Recipe Generator</h1>
        <form method="post" action="/generate">
            <textarea name="ingredients" placeholder="Enter ingredients..."></textarea><br><br>
            <button type="submit">Get Recipe</button>
        </form>
    </body>
    </html>
    """

@app.post("/generate", response_class=HTMLResponse)
async def generate_recipe(ingredients: str = Form(...)):
    prompt = f"Create a beginner-friendly recipe using these ingredients: {ingredients}. Include ingredients list, step-by-step instructions, and one cooking tip."

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        recipe = response.text
    except Exception as e:
        recipe = f"Error: {e}"

    return f"""
    <html>
    <body style="font-family:Arial; background:#f9f9f9; text-align:center; padding:40px;">
        <h1>🍲 Your Recipe</h1>
        <div style="width:600px; margin:auto; background:white; padding:20px; border-radius:10px; text-align:left;">
            <pre>{recipe}</pre>
        </div>
        <br>
        <a href="/"><button>Generate Another</button></a>
    </body>
    </html>
    """

# ✅ This part is REQUIRED for Render to detect the running port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
