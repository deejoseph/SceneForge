# ===== 1️⃣ 基础导入 =====
from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests
import time
import uuid

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

@app.get("/download")
def download(url: str):
    r = requests.get(url)
    return StreamingResponse(
        iter([r.content]),
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=scene.png"}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 2️⃣ Session存储 =====
sessions = {}

# ===== 3️⃣ 数据结构 =====
class Request(BaseModel):
    purpose: str
    scene: str
    mood: str
    packaging: str = "none"
    style: str = ""          # ✅ 不写死
    custom: str = ""
    batch: int = 3

# ===== 4️⃣ ComfyUI =====
COMFY_URL = "http://127.0.0.1:8188/prompt"

def call_comfy(prompt_text, seed):
    workflow = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "dreamshaper_8.safetensors"
            }
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt_text,
                "clip": ["1", 1]
            }
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": """
multiple objects, clutter, messy, crowded,
duplicate items, too many cups,
non-celadon, colorful ceramics,
bad composition, off-center,
blurry, low quality
"""
,
                "clip": ["1", 1]
            }
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": 1344,
                "height": 768,
                "batch_size": 1
            }
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": 20,
                "cfg": 7,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 1,
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0]
            }
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["5", 0],
                "vae": ["1", 2]
            }
        },
        "7": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "scene",
                "images": ["6", 0]
            }
        }
    }

    res = requests.post(COMFY_URL, json={"prompt": workflow})
    return res.json()

def get_images(prompt_id):
    url = f"http://127.0.0.1:8188/history/{prompt_id}"

    for _ in range(30):
        res = requests.get(url)
        data = res.json()

        if prompt_id in data:
            outputs = data[prompt_id]["outputs"]

            for node_id in outputs:
                images = outputs[node_id].get("images", [])
                if images:
                    urls = []
                    for img in images:
                        image_url = f"http://127.0.0.1:8188/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"
                        urls.append(image_url)
                    return urls

        time.sleep(1)

    return []

# ===== 5️⃣ Prompt =====
def build_prompt(scene, mood, style, custom, packaging):

    if packaging in ["simple", "premium"]:
        packaging_prompt = """
Include a refined Chinese gift box.
One version can show open box with tea set inside.
"""
    else:
        packaging_prompt = "No packaging box."

    return f"""
MASTERPIECE, photorealistic,

celadon (qingci) ceramic tea set,
jade-like glaze, soft green tone,

scene: {scene},
mood: {mood},
style: {style},

clean composition,
wide horizontal layout,

minimalist Chinese interior,
wood table, soft natural light,

{packaging_prompt}

{custom},

high detail
"""

# ===== 6️⃣ API =====

@app.get("/start")
def start():
    sid = str(uuid.uuid4())
    sessions[sid] = {
        "confirmed": False,
        "selected_image": None
    }
    return {"session_id": sid}

@app.post("/generate")
def generate(req: Request):

    image_urls = []

    for i in range(req.batch):

        # ✅ 第2张强制礼盒
        if i == 1 and req.packaging in ["simple", "premium"]:
            custom_packaging = "focus on packaging box, open box display"
        else:
            custom_packaging = ""

        prompt = build_prompt(
            req.scene,
            req.mood,
            req.style,         # ✅ 用用户style
            custom_packaging,
            req.packaging
        )

        seed = int(uuid.uuid4().int % 1e9)

        comfy_res = call_comfy(prompt, seed)
        prompt_id = comfy_res.get("prompt_id")

        urls = get_images(prompt_id)

        if urls:
            image_urls.append(urls[0])

    return {
        "status": "ok",
        "images": image_urls
    }

@app.post("/confirm")
def confirm(session_id: str = Body(...), image_url: str = Body(...)):
    if session_id not in sessions:
        return {"status": "error"}

    sessions[session_id]["confirmed"] = True
    sessions[session_id]["selected_image"] = image_url

    return {"status": "ok"}

@app.post("/reset")
def reset(session_id: str = Body(...)):
    if session_id in sessions:
        sessions[session_id] = {}
    return {"status": "ok"}

@app.post("/save")
def save(image_url: str = Body(...)):
    return {
        "status": "ok",
        "download_url": image_url
    }