from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests
import time
import uuid
import urllib.request
import os
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

COMFY_URL = "http://127.0.0.1:8188/prompt"

# ===== 3. 数据模型 =====
class GenerateRequest(BaseModel):
    product_image_path: str = ""   # 瓷韵产品初稿路径
    model_type: str = "realistic"
    glaze: str = "yyms"            # 釉色代码
    purpose: str                   # "personal" 或 "gift"
    category: str                  # "dinnerware" / "tea" / "coffee" / "decor"
    items: Dict[str, int]          # 产品清单 {id: quantity}
    scene_prompt: str              # 场景描述
    mood: str                      # 氛围 ID
    mood_label: str                # 氛围中文名
    style: str                     # 氛围详细描述
    packaging: str = "none"        # 包装类型: "simple", "luxury", "wood"
    custom: str = ""

# ===== 4. 釉色配置（9种） =====
GLAZE_LIBRARY = {
    "yyms": "(Masterpiece:1.2), Yue ware secret color celadon, greenish celadon with slight yellow tint, clear glassy lime glaze, smooth and transparent, bright and vivid appearance, jade-like finish.",
    "rytq": "(Masterpiece:1.2), Ru ware sky blue celadon, soft bluish-gray tone, milky and oily texture, thick lime-alkali glaze, fine subtle crackle, elegant and soft diffusion.",
    "gytq": "(Masterpiece:1.2), Guan ware sky blue celadon, cool bluish tone, thick glossy glaze, pronounced ice crackle pattern, structural and layered appearance.",
    "geyhq": "(Masterpiece:1.2), Ge ware greyish celadon, muted blue-green, semi-matte finish, strong dark crackle lines, iron-rich coarse body, aged and rustic aesthetic.",
    "jytl": "(Masterpiece:1.2), Jun ware sky blue, opalescent glaze with purple-red flambé variations, uneven flowing texture, worm-like streaks, kiln transmutation effect.",
    "dyyb": "(Masterpiece:1.2), Ding ware moon white, warm ivory-white with slight cool tone, thin transparent glaze, soft gloss, clean and elegant.",
    "lqyfq": "(Masterpiece:1.2), Longquan powder green celadon, soft pale green with slight pinkish tone, thick jade-like glaze, smooth and gentle, soft diffusion.",
    "lqymzq": "(Masterpiece:1.2), Longquan plum green celadon, deep bluish-green, rich and dense thick glaze, deep glossy finish, stable mature jade texture.",
    "htyyq": "(Masterpiece:1.2), Hutian yingqing celadon, pale bluish-white, translucent glassy glaze, bright and luminous, fine white porcelain body."
}

GLAZE_ENGINE_CONFIG = {
    "yyms": {
        "model_type": "realistic",
        "ckpt": "realvisxlV50_v50LightningBakedvae.safetensors",
        "steps": 10,
        "cfg": 1.8,
        "width": 1344,
        "height": 768,
        "sampler": "dpmpp_sde",
        "scheduler": "karras",
        "lora_weight": 0.6,
    },
    "rytq": {
        "model_type": "artistic",
        "ckpt": "dreamshaperXL_lightningDPMSDE.safetensors",
        "steps": 10,
        "cfg": 2.0,
        "width": 1344,
        "height": 768,
        "sampler": "dpmpp_sde",
        "scheduler": "karras",
        "lora_weight": 0.8,
    },
    "gytq": {
        "model_type": "realistic",
        "ckpt": "realvisxlV50_v50LightningBakedvae.safetensors",
        "steps": 10,
        "cfg": 1.8,
        "width": 1344,
        "height": 768,
        "sampler": "dpmpp_sde",
        "scheduler": "karras",
        "lora_weight": 0.6,
    },
    "geyhq": {
        "model_type": "realistic",
        "ckpt": "realvisxlV50_v50LightningBakedvae.safetensors",
        "steps": 10,
        "cfg": 1.8,
        "width": 1344,
        "height": 768,
        "sampler": "dpmpp_sde",
        "scheduler": "karras",
        "lora_weight": 0.6,
    },
    "jytl": {
        "model_type": "artistic",
        "ckpt": "dreamshaperXL_lightningDPMSDE.safetensors",
        "steps": 10,
        "cfg": 2.0,
        "width": 1344,
        "height": 768,
        "sampler": "dpmpp_sde",
        "scheduler": "karras",
        "lora_weight": 0.8,
    },
    "dyyb": {
        "model_type": "fast",
        "ckpt": "epiCrealism.safetensors",
        "steps": 20,
        "cfg": 5.0,
        "width": 768,
        "height": 512,
        "sampler": "dpmpp_2m",
        "scheduler": "karras",
        "lora_weight": 0.6,
    },
    "lqyfq": {
        "model_type": "artistic",
        "ckpt": "dreamshaperXL_lightningDPMSDE.safetensors",
        "steps": 10,
        "cfg": 2.0,
        "width": 1344,
        "height": 768,
        "sampler": "dpmpp_sde",
        "scheduler": "karras",
        "lora_weight": 0.8,
    },
    "lqymzq": {
        "model_type": "artistic",
        "ckpt": "dreamshaperXL_lightningDPMSDE.safetensors",
        "steps": 10,
        "cfg": 2.0,
        "width": 1344,
        "height": 768,
        "sampler": "dpmpp_sde",
        "scheduler": "karras",
        "lora_weight": 0.8,
    },
    "htyyq": {
        "model_type": "fast",
        "ckpt": "epiCrealism.safetensors",
        "steps": 20,
        "cfg": 5.0,
        "width": 768,
        "height": 512,
        "sampler": "dpmpp_2m",
        "scheduler": "karras",
        "lora_weight": 0.6,
    }
}

# 品牌标识
BRANDING_STAMP = "subtle brand logo on the porcelain surface"

# 产品名称翻译
TRANSLATION_MAP = {
    "bowl_1": "celadon bowl", "bowl_l_1": "large celadon bowl", "bowl_m_1": "medium celadon bowl", "bowl_s_1": "small celadon bowl",
    "fruit_bowl_1": "fruit bowl", "plate_l_1": "large plate", "plate_l_2": "large plate", "plate_m_1": "medium plate",
    "salad_bowl_l_1": "salad bowl", "sauce_dish_1": "sauce dish",
    "teapot_1": "teapot", "teapot_2_lefthand": "left-handed teapot", "teapot_2_righthand": "right-handed teapot", "teapot_3": "teapot",
    "teaset_3": "tea set", "gaiwan_1": "gaiwan", "fairness_cup_1": "fairness cup", "fairness_cup_2": "fairness cup",
    "teacup_1": "tea cup", "teacup_2": "tea cup", "teacup_3": "tea cup", "tea_basin_1": "tea basin", "incense_burner_1": "incense burner",
    "coffee_pot_1": "coffee pot", "cup_saucer_1": "coffee cup and saucer", "coffee_set_1": "coffee set", "mug_1": "mug",
    "jar_genenral_1": "jar", "vase_mei_1": "mei vase", "vase_mei_2": "mei vase", "vase_lamp_base_1": "lamp base", "vase_lamp_base_2": "lamp base",
    "plaque_1": "porcelain plaque", "plaque_2": "porcelain plaque", "plaque_3": "porcelain plaque", "plaque_4": "porcelain plaque",
    "plaque_5": "porcelain plaque", "plaque_6": "porcelain plaque", "plaque_7": "porcelain plaque",
    "sculpture_1": "sculpture", "sculpture_2": "sculpture", "sculpture_3": "sculpture", "sculpture_4": "sculpture",
    "sculpture_5": "sculpture", "sculpture_6": "sculpture", "sculpture_7": "sculpture", "sculpture_8": "sculpture"
}

# ===== 5. 辅助函数 =====
def download_image_to_temp(url):
    """下载图片到临时目录，返回本地路径"""
    temp_dir = "D:/PixelSmile/temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 从 URL 提取文件名
    filename = url.split('/')[-1]
    # 去掉可能存在的查询参数
    if '?' in filename:
        filename = filename.split('?')[0]
    local_path = os.path.join(temp_dir, filename)
    
    # 如果文件已存在，直接返回
    if os.path.exists(local_path):
        print(f"图片已存在: {local_path}")
        return local_path
    
    # 下载
    try:
        urllib.request.urlretrieve(url, local_path)
        print(f"图片已下载: {local_path}")
        return local_path
    except Exception as e:
        print(f"下载图片失败: {e}")
        return url  # 返回原 URL，让 ComfyUI 尝试处理

def get_item_desc(items):
    parts = [f"{v} {TRANSLATION_MAP.get(k, k)}" for k, v in items.items() if v > 0]
    return ", ".join(parts) if parts else "exquisite celadon porcelain"

def get_pkg_name(p_id):
    pkg_dict = {
        "simple": "minimalist eco-friendly paper box",
        "luxury": "premium paper gift box with gold foil",
        "wood": "traditional wooden gift crate with silk lining"
    }
    return pkg_dict.get(p_id, "elegant gift packaging")

# ===== 6. 构建三张图的 Prompt =====
def build_delivery_prompts(req: GenerateRequest) -> List[str]:
    """
    构建三张图的 Prompt
    关键：不描述产品本身，只描述场景和氛围
    产品形状和釉色完全由输入的图片（瓷韵初稿）决定
    """
    tech_suffix = "photorealistic, 8k, cinematic lighting, elegant aesthetic"
    user_custom = f", {req.custom}" if req.custom.strip() else ""
    
    prompts = []
    
    # ========== 第1张：产品展示（两个分支相同）==========
    product_shot = (
        f"product photography, centered composition, "
        f"clean white background, soft diffused studio lighting, "
        f"showcasing ceramic texture and form, high detail, "
        f"{tech_suffix}{user_custom}"
    )
    prompts.append(product_shot)
    
    if req.purpose == "gift":
        # ========== 商务馈赠分支 ==========
        pkg_name = get_pkg_name(req.packaging)
        
        # 第2张：礼盒嵌套展示
        gift_box_shot = (
            f"product placed inside an open {pkg_name}, "
            f"premium gift box presentation, silk lining details, "
            f"studio lighting, luxury product shot, "
            f"{tech_suffix}{user_custom}"
        )
        prompts.append(gift_box_shot)
        
        # 第3张：商务送礼场景
        business_gift_shot = (
            f"{req.scene_prompt}, "
            f"hands holding a gift box, ceremonial gifting moment, "
            f"professional business setting, etiquette atmosphere, "
            f"elegant composition, {req.style}, "
            f"{tech_suffix}{user_custom}"
        )
        prompts.append(business_gift_shot)
        
    else:
        # ========== 个人自用分支 ==========
        # 第2张：居家使用环境
        home_env_shot = (
            f"{req.scene_prompt}, "
            f"daily home environment, soft natural window light, "
            f"warm cozy atmosphere, lifestyle photography, "
            f"{req.style}, {tech_suffix}{user_custom}"
        )
        prompts.append(home_env_shot)
        
        # 第3张：社交共享氛围
        social_shot = (
            f"{req.scene_prompt}, "
            f"people gathering around a table, sharing meal or tea, "
            f"warm social interaction, happy moments, "
            f"shallow depth of field, candid lifestyle shot, "
            f"{req.style}, {tech_suffix}{user_custom}"
        )
        prompts.append(social_shot)
    
    return prompts

# ===== 7. ComfyUI 图生图调用 =====
def call_comfy_img2img(product_image_path, prompt_text, seed, engine_config, denoise=0.65):
    """
    图生图：将产品初稿融入场景
    """
    # 如果是 HTTP URL，先下载到本地
    if product_image_path.startswith('http://') or product_image_path.startswith('https://'):
        product_image_path = download_image_to_temp(product_image_path)
        print(f"转换后本地路径: {product_image_path}")
    
    ckpt_name = engine_config["ckpt"]
    steps = engine_config["steps"]
    cfg = engine_config["cfg"]
    width = engine_config["width"]
    height = engine_config["height"]
    sampler = engine_config["sampler"]
    scheduler = engine_config["scheduler"]
    lora_weight = engine_config["lora_weight"]
    
    workflow = {
        "1": {
            "class_type": "LoadImage",
            "inputs": {"image": product_image_path}
        },
        "2": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": ckpt_name}
        },
        "3": {
            "class_type": "LoraLoader",
            "inputs": {
                "lora_name": "CeramicXL_LoRA.safetensors",
                "strength_model": lora_weight,
                "strength_clip": 1.0,
                "model": ["2", 0],
                "clip": ["2", 1]
            }
        },
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt_text, "clip": ["3", 1]}
        },
        "5": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "low quality, bad anatomy, text, watermark, deformed, blurry, two spouts",
                "clip": ["3", 1]
            }
        },
        "6": {
            "class_type": "VAEEncode",
            "inputs": {"pixels": ["1", 0], "vae": ["2", 2]}
        },
        "7": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler,
                "scheduler": scheduler,
                "denoise": denoise,
                "model": ["3", 0],
                "positive": ["4", 0],
                "negative": ["5", 0],
                "latent_image": ["6", 0]
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["7", 0], "vae": ["2", 2]}
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": "Atmosphere_Custom", "images": ["8", 0]}
        }
    }
    
    try:
        res = requests.post(COMFY_URL, json={"prompt": workflow}, timeout=30)
        return res.json()
    except Exception as e:
        print(f"ComfyUI 调用失败: {e}")
        return {"error": str(e)}

def get_images(prompt_id):
    url = f"http://127.0.0.1:8188/history/{prompt_id}"
    for _ in range(60):
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

# ===== 8. 路由接口 =====
@app.post("/generate")
def generate(req: GenerateRequest):
    print(f"--- 开始生成氛围图 | 釉色: {req.glaze} | 用途: {req.purpose} | 包装: {req.packaging} ---")
    
    # 获取引擎配置
    engine_config = GLAZE_ENGINE_CONFIG.get(req.glaze, GLAZE_ENGINE_CONFIG["yyms"])
    
    # 获取产品初稿路径
    product_image_path = req.product_image_path
    if not product_image_path:
        # 如果没有传入产品图，使用默认占位（测试用）
        product_image_path = "D:/PixelSmile/imgs/placeholder.png"
        print(f"警告: 未传入产品图路径，使用默认: {product_image_path}")
    
    # 构建三张图的 Prompt
    prompts = build_delivery_prompts(req)
    
    image_urls = []
    prompt_ids = []
    
    # 不同视角使用不同的 denoise
    denoise_values = {
        0: 0.45,  # 产品展示：保持原样
        1: 0.55,  # 场景图：融入环境
        2: 0.60   # 社交/送礼图：更多创意
    }
    
    for i, p_text in enumerate(prompts):
        seed = int(uuid.uuid4().int % 1e9)
        denoise = denoise_values.get(i, 0.65)
        
        print(f"生成第 {i+1} 张图，denoise={denoise}")
        print(f"Prompt: {p_text[:100]}...")
        
        res = call_comfy_img2img(product_image_path, p_text, seed, engine_config, denoise)
        if "prompt_id" in res:
            prompt_ids.append(res["prompt_id"])
        else:
            print(f"调用失败: {res}")
    
    for pid in prompt_ids:
        urls = get_images(pid)
        if urls:
            image_urls.append(urls[0])
    
    print(f"生成完成，共 {len(image_urls)} 张图")
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

# ===== 9. 启动主程序 =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)