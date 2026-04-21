from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests
import time
import uuid
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

# ===== 数据结构与配置 =====
sessions = {}

# 渲染引擎映射表 (请确保文件名与你本地文件夹一致)
MODEL_MAP = {
    "fast": "epiCrealism.safetensors",              # 2GB 快速生成版 (SD 1.5)
    "realistic": "realvisxlV50_v50LightningBakedvae.safetensors", # 6GB 顶级写实版 (SDXL)
    "artistic": "dreamshaperXL_lightningDPMSDE.safetensors"       # 6GB 艺术质感版 (SDXL)
}

class GenerateRequest(BaseModel):
    model_type: str = "realistic"
    purpose: str
    scene: str
    mood: str
    packaging: str = "none"
    style: str = ""          
    custom: str = ""              
    batch: int = 3

COMFY_URL = "http://127.0.0.1:8188/prompt"

# ===== 核心功能函数 =====

def call_comfy(prompt_text, seed, ckpt_name, model_type):
    # 1. 架构检测
    is_xl = "XL" in ckpt_name or "xl" in ckpt_name
    
    # 2. 动态参数适配 (修正了导致色彩崩坏的根源)
    if is_xl:
        steps = 8           
        cfg = 2.0           # Lightning模型严禁高CFG
        width, height = 1344, 768
        sampler = "dpmpp_sde"
        lora_weight = 0.8 if model_type == "artistic" else 0.6
    else:
        steps = 20          # SD 1.5 步数不宜过高
        cfg = 5.0           # 降低CFG以防止色彩过饱和/烧焦感
        width, height = 768, 512 
        sampler = "dpmpp_2m"
        lora_weight = 0     # SD 1.5 严禁加载 XL LoRA

    # 3. 精简负面词：移除高权重括号，防止画面逻辑走入死角
    negative_content = (
        "(two spouts:1.5), (extra spout:1.5), deformed handle, (multiple teapots:1.3), duplicate items, "
        "lowres, bad quality, blurry, washed out, grey, dark, gloomy, messy background, cluttered table"
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
                "seed": seed,
                "steps": steps,           
                "cfg": cfg,             
                "sampler_name": sampler,
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["2", 0], "positive": ["3", 0], "negative": ["4", 0], "latent_image": ["5", 0]
            }
        },
        "7": { "class_type": "VAEDecode", "inputs": { "samples": ["6", 0], "vae": ["1", 2] } },
        "8": { "class_type": "SaveImage", "inputs": { "filename_prefix": "SceneForge_Vibe", "images": ["7", 0] } }
    }
    
    try:
        res = requests.post(COMFY_URL, json={"prompt": workflow}, timeout=10)
        return res.json()
    except Exception as e:
        print(f"ComfyUI 连接失败: {e}")
        return {"error": "connection failed"}

def build_vibe_prompt(req, is_packaging_focus=False):
    """
    重构 Prompt 逻辑：去除过载权重，采用结构化描述
    """
    scene_map = {
        "tea room": "minimalist Chinese tea room, dark wood tea table",
        "home": "modern living room, white marble tabletop, natural light",
        "office": "executive mahogany desk, intellectual setting",
        "gallery": "minimalist art gallery, museum spotlight"
    }
    
    # 核心主体：去掉了导致崩溃的 ( :1.5) 高权重
    subject = "ONE single celadon teapot, exactly ONE spout and ONE handle, 2-3 small matching teacups beside"
    
    if is_packaging_focus and req.packaging != "none":
        subject = f"an open {req.packaging} gift box, {subject}"

    # 整合客户留言
    user_custom = f", {req.custom}" if req.custom.strip() else ""
    
    # 最终组装：保持词汇中性，靠底模自身素质出图
    full_prompt = (
        f"MASTERPIECE, ultra realistic, {subject}, "
        f"scene: {scene_map.get(req.scene, 'clean background')}, "
        f"mood: {req.mood} atmosphere, soft natural lighting, "
        f"style: high-end product photography, {req.style}{user_custom}, "
        f"depth of field, centered composition, clean layout"
    )
    return full_prompt.strip()

# ===== 路由定义 (保持不变) =====

@app.get("/start")
def start():
    sid = str(uuid.uuid4())
    sessions[sid] = {"confirmed": False, "selected_image": None}
    return {"session_id": sid}

@app.post("/generate")
def generate(req: GenerateRequest):
    ckpt_name = MODEL_MAP.get(req.model_type, MODEL_MAP["realistic"])
    image_urls = []
    prompt_ids = []

    print(f"收到请求: 模型={req.model_type}, 留言={req.custom}")

    for i in range(req.batch):
        focus_on_pkg = (i == 1 and req.packaging != "none")
        view_hint = "close-up shot" if i == 2 else "product photography"
        
        prompt = build_vibe_prompt(req, is_packaging_focus=focus_on_pkg) + f", {view_hint}"
        seed = int(uuid.uuid4().int % 1e9)
        
        comfy_res = call_comfy(prompt, seed, ckpt_name, req.model_type)
        pid = comfy_res.get("prompt_id")
        if pid:
            prompt_ids.append(pid)

    for pid in prompt_ids:
        urls = get_images(pid)
        if urls:
            image_urls.append(urls[0])

    return {"status": "ok", "images": image_urls}

def get_images(prompt_id):
    url = f"http://127.0.0.1:8188/history/{prompt_id}"
    for _ in range(40):
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