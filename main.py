from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests
import time
import uuid
from typing import Dict, Optional, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# ===== 1. 跨域配置 (CORS) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 2. 模型与配置常量 =====
sessions = {}

MODEL_MAP = {
    "fast": "epiCrealism.safetensors",
    "realistic": "realvisxlV50_v50LightningBakedvae.safetensors",
    "artistic": "dreamshaperXL_lightningDPMSDE.safetensors"
}

# 完整的翻译映射
TRANSLATION_MAP = {
    "dinner_plate": "large dinner plate", "medium_plate": "medium plate", "bowl": "bowl",
    "sauce_dish": "sauce dish", "large_pot": "large serving pot", "teapot": "teapot",
    "gaiwan": "Gaiwan (tea lidded bowl)", "fair_cup": "fairness cup", "tea_cup": "tea cup",
    "tea_sea": "tea sea", "tea_tray": "tea tray", "tea_wash": "tea wash bowl",
    "incense_burner": "incense burner", "coffee_pot": "coffee pot", "coffee_cup": "coffee cup and saucer",
    "mug": "ceramic mug", "vase": "celadon vase", "lamp": "celadon table lamp",
    "plaque": "engraved porcelain plaque", "sculpture": "celadon sculpture"
}

# ===== 3. 数据模型 =====
class GenerateRequest(BaseModel):
    model_type: str = "realistic"
    purpose: str                  # "personal" 或 "gift"
    category: str
    items: Dict[str, int]
    scene_prompt: str             # 来自前端场景选择
    mood: str                     # 氛围 ID
    mood_label: str               # 氛围中文名
    style: str                    # 来自前端氛围映射的详细描述
    packaging: str = "none"
    custom: str = ""

COMFY_URL = "http://127.0.0.1:8188/prompt"

# ===== 4. 核心提示词工厂 (三视角逻辑) =====

def get_item_desc(items):
    parts = [f"{v} {TRANSLATION_MAP.get(k, k)}" for k, v in items.items() if v > 0]
    return ", ".join(parts) if parts else "exquisite celadon porcelain"

# ===== 1. 材质与品牌常量定义 =====

# ===== 材质/釉色库定义 =====

GLAZE_LIBRARY = {
    "fenqing": (
        "exquisite Powder Celadon (Fenqing), solid stoneware body, thick opaque glaze, "
        "color is pale bluish-celadon with a (strong bluish undertone:1.3), "
        "immaculate uniform surface, no crackles, smooth polished finish"
    ),
    "meiziqing": (
        "premium Meiziqing celadon, thick opacified lime-alkali glaze, "
        "color is a lush (fresh bluish-green:1.2), strictly avoiding sky blue, "
        "liquid-like glossy finish with deep luster, viscous and rich texture, no transparency"
    ),
    "yingqing": (
        "premium Hutian Yingqing, pure modern white porcelain substrate, "
        "highly dense body, (thick opacified glaze:1.2), resembling the texture of fine jade, "
        "color is a delicate pale watery-green, viscous and rich glaze, bright lustrous finish"
    )
}

# 品牌标识 (Logo) 的物理呈现
BRANDING_STAMP = (
    "subtle brand logo, (dark taupe and terracotta colors:1.1), "
    "crisp minimalist graphic on the porcelain surface"
)

# ===== 2. 函数实现 =====

def get_pkg_name(p_id):
    pkg_dict = {
        "1": "minimalist eco paper box", 
        "2": "luxury silk-lined gift box", 
        "3": "traditional wooden crate"
    }
    return pkg_dict.get(p_id, "gift packaging")

def build_delivery_prompts(req: GenerateRequest) -> List[str]:
    item_desc = get_item_desc(req.items)
    
    # 动态获取釉色，如果请求中没有指定则默认使用粉青
    # 建议在 GenerateRequest 增加 glaze 字段，如 'fenqing', 'meiziqing', 'yingqing'
    glaze_key = getattr(req, 'glaze', 'fenqing')
    selected_glaze = GLAZE_LIBRARY.get(glaze_key, GLAZE_LIBRARY['fenqing'])
    
    # 基础物理定义组装
    base_material = f"{selected_glaze}, {BRANDING_STAMP}, masterpiece"
    tech_suffix = "photorealistic, 8k, cinematic lighting, elegant aesthetic"
    user_custom = f", {req.custom}" if req.custom.strip() else ""
    
    prompts = []

    # 视角 1: 产品展示 (侧重材质质感)
    prompts.append(
        f"{base_material}, {item_desc}, macro photography, blurred simple background, "
        f"centered composition, studio lighting, {tech_suffix}{user_custom}"
    )

    if req.purpose == "gift":
        # 视角 2: 礼盒效果 (侧重包装与产品的嵌套关系)
        pkg = get_pkg_name(req.packaging)
        prompts.append(
            f"{base_material}, {item_desc} neatly placed inside an open {pkg}, "
            f"presentation view, silk lining details, premium gift set, "
            f"{req.style}, {tech_suffix}{user_custom}"
        )
        # 视角 3: 商务送礼场景 (侧重人机互动与礼仪感)
        prompts.append(
            f"{base_material} in a {pkg}, hands holding the box, {req.scene_prompt}, "
            f"ceremonial gifting moment, business etiquette, professional atmosphere, "
            f"{req.style}, {tech_suffix}{user_custom}"
        )
    else:
        # 视角 2: 居家环境 (侧重生活美学与自然光)
        prompts.append(
            f"{base_material}, {item_desc}, {req.scene_prompt}, "
            f"daily life scene, soft natural window light, home interior design, "
            f"{req.style}, {tech_suffix}{user_custom}"
        )
        # 视角 3: 社交共享 (侧重氛围感与局部景深)
        prompts.append(
            f"{base_material}, {item_desc}, {req.scene_prompt}, people enjoying tea or meal, "
            f"warm social interaction, shared happiness, shallow depth of field, "
            f"{req.style}, {tech_suffix}{user_custom}"
        )
    
    return prompts

# ===== 5. ComfyUI 交互逻辑 =====

def call_comfy(prompt_text, seed, ckpt_name, model_type):
    is_xl = "XL" in ckpt_name or "xl" in ckpt_name
    steps, cfg = (8, 2.0) if is_xl else (20, 5.0)
    width, height = (1344, 768) if is_xl else (768, 512)
    sampler = "dpmpp_sde" if is_xl else "dpmpp_2m"
    lora_weight = 0.8 if model_type == "artistic" else 0.6
    
    workflow = {
        "1": { "class_type": "CheckpointLoaderSimple", "inputs": { "ckpt_name": ckpt_name } },
        "2": { "class_type": "LoraLoader", "inputs": { "lora_name": "CeramicXL_LoRA.safetensors", "strength_model": lora_weight, "strength_clip": 1.0, "model": ["1", 0], "clip": ["1", 1] } },
        "3": { "class_type": "CLIPTextEncode", "inputs": { "text": prompt_text, "clip": ["2", 1] } },
        "4": { "class_type": "CLIPTextEncode", "inputs": { "text": "low quality, bad anatomy, text, watermark, (two spouts:1.5), deformed", "clip": ["2", 1] } },
        "5": { "class_type": "EmptyLatentImage", "inputs": { "width": width, "height": height, "batch_size": 1 } },
        "6": { "class_type": "KSampler", "inputs": { "seed": seed, "steps": steps, "cfg": cfg, "sampler_name": sampler, "scheduler": "karras", "denoise": 1.0, "model": ["2", 0], "positive": ["3", 0], "negative": ["4", 0], "latent_image": ["5", 0] } },
        "7": { "class_type": "VAEDecode", "inputs": { "samples": ["6", 0], "vae": ["1", 2] } },
        "8": { "class_type": "SaveImage", "inputs": { "filename_prefix": "Ceramic_Custom", "images": ["7", 0] } }
    }
    
    try:
        res = requests.post(COMFY_URL, json={"prompt": workflow}, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def get_images(prompt_id):
    url = f"http://127.0.0.1:8188/history/{prompt_id}"
    for _ in range(60): # 轮询约 72 秒
        try:
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                if prompt_id in data:
                    outputs = data[prompt_id].get("outputs", {})
                    for node_id, node_output in outputs.items():
                        if "images" in node_output:
                            img = node_output["images"][0]
                            return [f"http://127.0.0.1:8188/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"]
        except:
            pass
        time.sleep(1.2)
    return []

# ===== 6. 路由接口 =====

@app.post("/generate")
def generate(req: GenerateRequest):
    ckpt_name = MODEL_MAP.get(req.model_type, MODEL_MAP["realistic"])
    prompts = build_delivery_prompts(req)
    image_urls = []
    prompt_ids = []

    print(f"--- 启动交付级渲染 | 类别: {req.category} | 用途: {req.purpose} ---")

    for p_text in prompts:
        seed = int(uuid.uuid4().int % 1e9)
        res = call_comfy(p_text, seed, ckpt_name, req.model_type)
        if "prompt_id" in res:
            prompt_ids.append(res["prompt_id"])

    for pid in prompt_ids:
        urls = get_images(pid)
        if urls: image_urls.append(urls[0])

    return {"status": "ok", "images": image_urls}

@app.get("/download")
def download(url: str):
    try:
        r = requests.get(url, stream=True)
        return StreamingResponse(r.iter_content(chunk_size=1024), media_type="image/png")
    except:
        return {"error": "Download failed"}

@app.post("/confirm")
def confirm(session_id: str = Body(...), image_url: str = Body(...)):
    sessions[session_id] = {"confirmed": True, "selected_image": image_url, "timestamp": time.time()}
    return {"status": "ok"}

# ===== 7. 启动主程序 =====
if __name__ == "__main__":
    import uvicorn
    # 使用 0.0.0.0 方便局域网测试
    uvicorn.run(app, host="0.0.0.0", port=8000)