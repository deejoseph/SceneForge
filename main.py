from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests
import time
import uuid
from typing import Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# ===== 跨域配置 =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 配置与模型映射 =====
sessions = {}

MODEL_MAP = {
    "fast": "epiCrealism.safetensors",
    "realistic": "realvisxlV50_v50LightningBakedvae.safetensors",
    "artistic": "dreamshaperXL_lightningDPMSDE.safetensors"
}

# 扩展翻译映射，涵盖所有新增器皿
TRANSLATION_MAP = {
    # 餐具
    "dinner_plate": "large dinner plate",
    "medium_plate": "medium plate",
    "bowl": "bowl",
    "sauce_dish": "sauce dish",
    "large_pot": "large serving pot",
    # 茶具
    "teapot": "teapot",
    "gaiwan": "Gaiwan (tea lidded bowl)",
    "fair_cup": "fairness cup (Gongdao Bei)",
    "tea_cup": "tea cup",
    "tea_sea": "tea sea (Cha Hai)",
    "tea_tray": "tea tray",
    "tea_wash": "tea wash bowl",
    "incense_burner": "incense burner",
    # 咖啡具
    "coffee_pot": "coffee pot",
    "coffee_cup": "coffee cup and saucer",
    "mug": "ceramic mug",
    # 摆设
    "vase": "celadon vase",
    "lamp": "celadon table lamp",
    "plaque": "engraved porcelain plaque",
    "sculpture": "celadon sculpture"
}

class GenerateRequest(BaseModel):
    model_type: str = "realistic"
    purpose: str                  # "personal" 或 "gift"
    category: str = "tea"         # "dinnerware", "coffee", "tea", "decor"
    items: Dict[str, int] = {}    
    scene: str                    # 场景 ID
    scene_prompt: str             # 前端传来的详细英文场景描述
    mood: str
    mood_label: str
    packaging: str = "none"
    style: str = ""               # 氛围触发词
    custom: str = ""              
    batch: int = 3

COMFY_URL = "http://127.0.0.1:8188/prompt"

# ===== 核心功能函数 =====

def call_comfy(prompt_text, seed, ckpt_name, model_type):
    is_xl = "XL" in ckpt_name or "xl" in ckpt_name
    
    # 动态参数调整
    if is_xl:
        steps, cfg = 8, 2.0           
        width, height = 1344, 768
        sampler = "dpmpp_sde"
        lora_weight = 0.8 if model_type == "artistic" else 0.6
    else:
        steps, cfg = 20, 5.0           
        width, height = 768, 512  
        sampler = "dpmpp_2m"
        lora_weight = 0     

    negative_content = (
        "bad hands, (two spouts:1.5), deformed handle, multiple teapots, "
        "lowres, bad quality, blurry, cluttered, text, watermark"
    )
    
    workflow = {
        "1": { "class_type": "CheckpointLoaderSimple", "inputs": { "ckpt_name": ckpt_name } },
        "2": { 
            "class_type": "LoraLoader", 
            "inputs": { 
                "lora_name": "CeramicXL_LoRA.safetensors", 
                "strength_model": lora_weight, 
                "strength_clip": 1.0, 
                "model": ["1", 0], "clip": ["1", 1] 
            } 
        },
        "3": { "class_type": "CLIPTextEncode", "inputs": { "text": prompt_text, "clip": ["2", 1] } },
        "4": { "class_type": "CLIPTextEncode", "inputs": { "text": negative_content, "clip": ["2", 1] } },
        "5": { "class_type": "EmptyLatentImage", "inputs": { "width": width, "height": height, "batch_size": 1 } },
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed, "steps": steps, "cfg": cfg, "sampler_name": sampler,
                "scheduler": "karras", "denoise": 1.0,
                "model": ["2", 0], "positive": ["3", 0], "negative": ["4", 0], "latent_image": ["5", 0]
            }
        },
        "7": { "class_type": "VAEDecode", "inputs": { "samples": ["6", 0], "vae": ["1", 2] } },
        "8": { "class_type": "SaveImage", "inputs": { "filename_prefix": "CeramicCustom", "images": ["7", 0] } }
    }
    
    try:
        res = requests.post(COMFY_URL, json={"prompt": workflow}, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def build_vibe_prompt(req: GenerateRequest, is_packaging_focus=False):
    # 1. 生成器皿清单描述
    item_parts = []
    for key, count in req.items.items():
        if count > 0:
            name = TRANSLATION_MAP.get(key, key.replace("_", " "))
            # 如果是摆设类且单选，不加数字以提高权重
            if req.category == "decor":
                item_parts.append(f"a masterpiece of {name}")
            else:
                item_parts.append(f"{count} {name}")
    
    subject_desc = ", ".join(item_parts) if item_parts else "exquisite celadon porcelain"
    
    # 2. 包装逻辑
    if req.purpose == "gift" and req.packaging != "none":
        pkg_map = {"1": "cardboard box", "2": "luxury gift box", "3": "wooden crate"}
        pkg_name = pkg_map.get(req.packaging, "gift packaging")
        if is_packaging_focus:
            subject = f"an open {pkg_name}, {subject_desc} placed neatly inside"
        else:
            subject = f"{subject_desc}, standing next to its {pkg_name}"
    else:
        subject = subject_desc

    # 3. 组合最终 Prompt (核心：使用 req.scene_prompt)
    user_custom = f", {req.custom}" if req.custom.strip() else ""
    
    full_prompt = (
        f"Longquan celadon porcelain, {subject}, {req.scene_prompt}, "
        f"{req.mood_label} atmosphere, {req.style}, "
        f"soft natural lighting, photorealistic, 8k, highly detailed glaze texture{user_custom}"
    )
    return full_prompt

# ===== 路由定义 =====

@app.post("/generate")
def generate(req: GenerateRequest):
    ckpt_name = MODEL_MAP.get(req.model_type, MODEL_MAP["realistic"])
    image_urls = []
    prompt_ids = []

    print(f"--- 任务启动: {req.category} | 场景: {req.scene_prompt} ---")

    for i in range(req.batch):
        # 批次 2 针对礼品模式生成包装特写
        focus_on_pkg = (i == 1 and req.purpose == "gift")
        view_hint = "macro shot" if i == 2 else "professional photography"
        
        prompt = build_vibe_prompt(req, focus_on_pkg) + f", {view_hint}"
        seed = int(uuid.uuid4().int % 1e9)
        
        comfy_res = call_comfy(prompt, seed, ckpt_name, req.model_type)
        if "prompt_id" in comfy_res:
            prompt_ids.append(comfy_res["prompt_id"])

    # 轮询获取结果
    for pid in prompt_ids:
        urls = get_images(pid)
        if urls:
            image_urls.append(urls[0])

    return {"status": "ok", "images": image_urls}

def get_images(prompt_id):
    url = f"http://127.0.0.1:8188/history/{prompt_id}"
    for _ in range(50): # 增加等待时间至 60 秒左右
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if prompt_id in data:
                outputs = data[prompt_id].get("outputs", {})
                for node_id, node_output in outputs.items():
                    if "images" in node_output:
                        img = node_output["images"][0]
                        return [f"http://127.0.0.1:8188/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"]
        time.sleep(1.2)
    return []

@app.get("/download")
def download(url: str):
    r = requests.get(url)
    return StreamingResponse(iter([r.content]), media_type="image/png")

@app.post("/confirm")
def confirm(session_id: str = Body(...), image_url: str = Body(...)):
    if session_id in sessions:
        sessions[session_id].update({"confirmed": True, "selected_image": image_url})
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)