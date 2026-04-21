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

# ===== 数据结构 =====
sessions = {}

class GenerateRequest(BaseModel):
    purpose: str
    scene: str
    mood: str
    packaging: str = "none"
    style: str = ""          
    custom: str = ""
    batch: int = 3

# ===== ComfyUI API 配置 =====
COMFY_URL = "http://127.0.0.1:8188/prompt"

def call_comfy(prompt_text, seed):
    # 强化负面权重，严控“双嘴”和“堆砌”错误
    negative_content = (
        "(two spouts:1.6), (extra spout:1.6), (multiple teapots:1.5), (too many cups:1.4), "
        "deformed handle, duplicate items, invalid design, "
        "blurry, low quality, messy background, cluttered table"
    )
    
    workflow = {
        "1": { "class_type": "CheckpointLoaderSimple", "inputs": { "ckpt_name": "realisticVisionV60B1_v51HyperVAE.safetensors" } },
        "2": { "class_type": "LoraLoader", "inputs": { "lora_name": "CeramicXL_LoRA.safetensors", "strength_model": 0.6, "strength_clip": 1.0, "model": ["1", 0], "clip": ["1", 1] } },
        "3": { "class_type": "CLIPTextEncode", "inputs": { "text": prompt_text, "clip": ["2", 1] } },
        "4": { "class_type": "CLIPTextEncode", "inputs": { "text": negative_content, "clip": ["2", 1] } },
        "5": { "class_type": "EmptyLatentImage", "inputs": { "width": 1344, "height": 768, "batch_size": 1 } },
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": 10,           
                "cfg": 3.0,             
                "sampler_name": "dpmpp_sde",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["2", 0], "positive": ["3", 0], "negative": ["4", 0], "latent_image": ["5", 0]
            }
        },
        "7": { "class_type": "VAEDecode", "inputs": { "samples": ["6", 0], "vae": ["1", 2] } },
        "8": { "class_type": "SaveImage", "inputs": { "filename_prefix": "SceneForge_Vibe", "images": ["7", 0] } }
    }
    res = requests.post(COMFY_URL, json={"prompt": workflow})
    return res.json()

def get_images(prompt_id):
    url = f"http://127.0.0.1:8188/history/{prompt_id}"
    # 针对 3070 显存写盘较慢，维持 40 次尝试，每次间隔 1.2 秒
    for _ in range(40):
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if prompt_id in data:
                outputs = data[prompt_id].get("outputs", {})
                all_images = []
                for node_id, node_output in outputs.items():
                    if "images" in node_output:
                        for img in node_output["images"]:
                            # 转换为可访问的 view URL
                            all_images.append(f"http://127.0.0.1:8188/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}")
                if all_images:
                    print(f"成功抓取到任务 {prompt_id} 的图片")
                    return all_images
        time.sleep(1.2)
    return []

def build_vibe_prompt(req, is_packaging_focus=False):
    # 1. 场景环境精确映射
    scene_elements = {
        "tea room": "on a traditional chinese dark wood tea table, bamboo shadows, zen calligraphy hanging in background, tatami mat texture",
        "home": "modern minimalist living room, clean white marble tabletop, soft sunlight through linen curtains, cozy domestic atmosphere",
        "office": "executive mahogany desk, neatly stacked books, soft lamp light, professional and intellectual setting",
        "gallery": "on a minimalist white pedestal, soft professional spotlight, clean grey museum wall background, artistic exhibition style"
    }
    
    # 2. 氛围灯光映射
    mood_lighting = {
        "zen": "cinematic fog, soft diffused top light, tea smoke lingering, wabi-sabi aesthetics",
        "warm": "golden hour sunset glow, long soft shadows, warm orange hue, inviting and cozy",
        "luxury": "dramatic rim lighting, deep contrast, elegant reflections on surface, premium studio photography"
    }

    selected_scene = scene_elements.get(req.scene, "clean minimalist background")
    selected_light = mood_lighting.get(req.mood, "natural lighting")
    
    # 3. 核心主体：强制单壶双杯（防止 AI 乱画）
    subject = "(ONLY one single celadon teapot:1.5), (two small matching teacups:1.2)"
    
    # 4. 包装逻辑：仅在第二张图且选择了包装时触发
    if is_packaging_focus and req.packaging != "none":
        pkg_desc = f"an open {req.packaging} premium gift box, luxury fabric lining, elegant presentation"
        subject = f"{pkg_desc}, {subject}"
    
    # 5. 组合最终 Prompt
    full_prompt = f"MASTERPIECE, 8k, professional product photography, {req.style}, {selected_light}, {selected_scene}, {subject}, elegant composition, depth of field, (flower vase with one branch in distance:0.8)"
    return full_prompt.strip()

# ===== 路由部分 =====

@app.get("/start")
def start():
    sid = str(uuid.uuid4())
    sessions[sid] = {"confirmed": False, "selected_image": None}
    return {"session_id": sid}

@app.post("/generate")
def generate(req: GenerateRequest):
    image_urls = []
    prompt_ids = []

    # 1. 第一步：快速连续发送 3 个任务到 ComfyUI 队列
    for i in range(req.batch):
        focus_on_pkg = (i == 1 and req.packaging != "none")
        
        # 视角微调：第一张标准，第二张看包装/全景，第三张特写
        view_custom = ""
        if not focus_on_pkg:
            view_custom = "close-up shot" if i == 2 else "centered composition"
        
        prompt = build_vibe_prompt(req, is_packaging_focus=focus_on_pkg) + f", {view_custom}"
        
        seed = int(uuid.uuid4().int % 1e9)
        comfy_res = call_comfy(prompt, seed)
        pid = comfy_res.get("prompt_id")
        if pid:
            prompt_ids.append(pid)
            print(f"任务 {i+1} 已入队: {pid}")

    # 2. 第二步：按 ID 顺序逐个抓取结果
    for pid in prompt_ids:
        urls = get_images(pid)
        if urls:
            image_urls.append(urls[0])
            print(f"获取图片成功: {urls[0]}")
        else:
            print(f"警告：任务 {pid} 读取超时")

    return {"status": "ok", "images": image_urls}

@app.get("/download")
def download(url: str):
    r = requests.get(url)
    return StreamingResponse(
        iter([r.content]), 
        media_type="image/png"
    )

@app.post("/confirm")
def confirm(session_id: str = Body(...), image_url: str = Body(...)):
    if session_id in sessions:
        sessions[session_id].update({"confirmed": True, "selected_image": image_url})
    return {"status": "ok"}