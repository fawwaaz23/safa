from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Allow cross-origin if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Serve static files (optional if you add CSS later)

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <html>
        <head>
            <title>Recipe AI 🍳</title>
            <style>
                body { 
                    font-family: Arial; 
                    background-color: #f9f9f9; 
                    color: #333; 
                    display: flex; 
                    flex-direction: column; 
                    align-items: center; 
                    padding: 50px;
                }
                h1 { color: #ff6f00; }
                textarea {
                    width: 400px;
                    height: 100px;
                    padding: 10px;
                    font-size: 16px;
                }
                button {
                    margin-top: 10px;
                    background-color: #ff6f00;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #e65c00;
                }
                .recipe-box {
                    margin-top: 30px;
                    width: 500px;
                    background-color: #fff;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                pre {
                    white-space: pre-wrap;
                    font-size: 16px;
                }
            </style>
        </head>
        <body>
            <h1>AI Recipe Generator 🍲</h1>
            <form method="post" action="/generate">
                <textarea name="ingredients" placeholder="Enter your ingredients..."></textarea><br>
                <button type="submit">Get Recipe</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/generate", response_class=HTMLResponse)
async def generate_recipe(ingredients: str = Form(...)):
    prompt = f"Create a detailed, step-by-step recipe using these ingredients: {ingredients}. Include ingredients list, instructions, and a short tip for beginners."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        recipe = response.choices[0].message.content.strip()
    except Exception as e:
        recipe = f"Error: {e}"

    html_content = f"""
    <html>
        <head>
            <title>Recipe AI 🍳</title>
            <style>
                body {{ 
                    font-family: Arial; 
                    background-color: #f9f9f9; 
                    color: #333; 
                    display: flex; 
                    flex-direction: column; 
                    align-items: center; 
                    padding: 50px;
                }}
                .recipe-box {{
                    margin-top: 30px;
                    width: 600px;
                    background-color: #fff;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                button {{
                    margin-top: 20px;
                    background-color: #ff6f00;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                }}
            </style>
        </head>
        <body>
            <h1>🍳 Your AI-Generated Recipe</h1>
            <div class="recipe-box">
                <pre>{recipe}</pre>
            </div>
            <form method="get" action="/">
                <button type="submit">Generate Another Recipe</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
