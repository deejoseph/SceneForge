🧾 项目进度记录（AI陶艺定制系统）
📌 项目名称

AI Ceramic Customizer（SceneForge）

🚀 当前阶段：MVP 已跑通 ✅
✅ 已完成模块
1️⃣ 系统架构搭建
✔ ComfyUI 本地部署（独立运行）
✔ Conda 环境（ai_backend）
✔ FastAPI 后端服务
✔ 一键启动脚本（run_all.bat）
2️⃣ AI生成流程打通
✔ prompt 自动生成（基于用户输入）
✔ 调用 ComfyUI API（/prompt）
✔ 生成图片并保存至 output
✔ 使用 /history 获取图片路径
✔ 转换为可访问 URL
3️⃣ 前端交互（简化版）
✔ HTML 表单输入（scene / mood / custom）
✔ 调用后端 /generate
✔ 图片实时显示（image_url）
✔ CORS 跨域处理完成
🎯 当前系统能力

用户可以：

输入场景 + 氛围 → 点击生成 → 自动出陶艺产品图

👉 已具备完整 AI 产品闭环能力

⚠️ 当前存在问题（已识别）
🟡 1. 生成结果不稳定
器皿比例偶尔异常
底托/结构不完整
图案融合不自然

👉 原因：

prompt 还未结构化
未使用专用 workflow（6C / 6D）
🟡 2. 只有单图输出
无法做“方案对比”
用户决策成本高
🟡 3. 需求收集不完整

当前只收集：

scene
mood

缺少：

使用目的
送礼对象
器型偏好
风格偏好
预算 / 时间
🧠 下一阶段目标（明天重点）
🔥 阶段 1：需求收集系统（核心）

构建完整表单：

用户输入结构（目标）
{
  "purpose": "gift / self-use",
  "target": "friend / business / elder",
  "scene": "tea room / office / home",
  "mood": "zen / warm / luxury",
  "vessel": "cup / vase / tea set",
  "pattern": "landscape / abstract / floral",
  "style": "celadon / modern / traditional",
  "budget": "low / mid / high",
  "deadline": "urgent / normal"
}
🔥 阶段 2：三方案生成（产品感提升）
一次生成 3 张：
- 禅意款（Zen）
- 商务款（Premium）
- 艺术款（Artistic）

👉 用户选择 → 再细化

🔥 阶段 3：融合系统（核心竞争力）

接入你已有：

6C / 6D workflow（器皿 + 图案融合）

实现：

用户上传：
- 器皿图
- 图案图

→ 自动融合生成产品图
🔥 阶段 4：Prompt工程升级

从：

自然语言

升级为：

结构化prompt模块（可控）
📦 项目结构（当前）
SceneForge/
│
├── main.py              # FastAPI后端
├── run_all.bat          # 一键启动
├── index.html           # 简易前端
├── ai_backend/          # 虚拟环境
└── SceneForge.json      # workflow（预留）
💡 核心价值（已经验证）

你这个系统本质是：

用户需求 → AI理解 → 自动设计 → 可视化产品

👉 不是“画图工具”，而是：

🔥 定制设计引导系统

🚀 明天的明确行动计划

我们直接做这三件事：

1️⃣ 设计完整表单（结构化）

👉 不再用自由输入

2️⃣ 做三图生成逻辑

👉 提升产品感

3️⃣ 接入你的融合 workflow（关键）

👉 做出差异化能力