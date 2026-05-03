🧾 项目进度记录（AI陶艺定制系统）
📌 项目名称

AI Ceramic Customizer（SceneForge）

🚀 当前阶段：MVP 已跑通 ✅
✅ 已完成模块
1️⃣ 系统架构搭建
✔ ComfyUI 本地部署（独立运行）
✔ Conda 环境（ai\_backend）
✔ FastAPI 后端服务
✔ 一键启动脚本（run\_all.bat）
2️⃣ AI生成流程打通
✔ prompt 自动生成（基于用户输入）
✔ 调用 ComfyUI API（/prompt）
✔ 生成图片并保存至 output
✔ 使用 /history 获取图片路径
✔ 转换为可访问 URL
3️⃣ 前端交互（简化版）
✔ HTML 表单输入（scene / mood / custom）
✔ 调用后端 /generate
✔ 图片实时显示（image\_url）
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

* 禅意款（Zen）
* 商务款（Premium）
* 艺术款（Artistic）

👉 用户选择 → 再细化

🔥 阶段 3：融合系统（核心竞争力）

接入你已有：

6C / 6D workflow（器皿 + 图案融合）

实现：

用户上传：

* 器皿图
* 图案图

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
├── run\_all.bat          # 一键启动
├── index.html           # 简易前端
├── ai\_backend/          # 虚拟环境
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

🚀 项目进度更新报告 (2026-04-22)
✅ 已完成 (Completed)
核心釉色物理建模 (Backend/Prompting)

粉青 (Fenqing)：锁定炻器质感与冷蓝调，去除开片。

梅子青 (Meiziqing)：锁定石灰碱釉乳浊感，强化青绿色泽与水润光泽。

湖田窑影青 (Yingqing)：攻克“假玉器”质感，实现白瓷胎的半透光性与油脂光泽，避开了玻璃感。

前端引导系统 (Frontend/UI)

双准入机制：实现 Step 0 引擎与釉色的双重选择锁定，未完成选择前禁止进入后续环节。

动态氛围预览：完成三维视角（产品、环境、社交）的逻辑分发。

交互闭环：实现了真正的 Blob 图片下载、全屏放大预览以及正式定制环节的入口跳转。

业务逻辑解耦

明确了“场景确认”仅作为美学决策辅助，不与后续器型生成的工程参数强耦合。

🚧 进行中 (In Progress)
商务馈赠逻辑 (Gift Mode)

礼盒包装展示的渲染逻辑已预留接口，需进一步细化不同档次包装（纸盒/丝缎/木盒）的 Prompt 描述。

正式定制模块 (Formal Customization)

需开发具体的器型选择器（基于已有的 categoryDefaults）以及 Logo 最终定位功能。

📅 下一步计划 (Next Steps)
测试商务包装渲染：验证三款包装盒在 AI 生成中的识别度。

集成正式定制页：将“进入正式定制环节”的按钮点击行为从 alert 替换为真实的页面路由或状态切换。

Prompt 自动化整合：将 glaze.md 中的定义通过环境变量或配置文件的形式，更优雅地注入 main.py。

4月24日
应该在【当前定制方案】中加上【类别】来区分（餐具、茶具、咖啡具、家居摆设），因为这会提醒用户。并且，在prompt中如果不加以类别约束，容易造成餐具茶具等类别互相污染。

【氛围图生成测试】

1. 自用方案
当前定制方案：
引擎 高清写实 | 釉色 粉青釉
用途 个人自用
清单 大盘 x6, 中盘 x6, 碗 x6, 味碟 x6, 大盆 x1
场景 中餐大圆桌 | 氛围 家庭聚餐 (温暖)

1.1 产品图（对准确率要求最高）
【prompt】
MASTERPIECE, product photography

a ceramic dinnerware set,
celadon glaze,

6 bowls, 6 plates, 6 soup bowls,
NO teapot,

clean product layout,
neatly arranged tableware,
balanced composition,

studio background,
neutral color,

accurate proportions,
realistic ceramic material,

ONLY dinnerware, no tea set
【测试结果】

* dreamshaperXL：生成类别中有茶壶串入，并且品种和数量不符
* epiCrealism：生成造型接近餐具，但有点怪，且品种和数量不符
* realvisxl50：生成造型最接近餐具，但品种和数量不符

1.2 使用环境图（对准确率要求不高）
【prompt】
MASTERPIECE, lifestyle photography

a celadon ceramic dinnerware set on a dining table,
family meal setting,

plates and bowls with food,
warm and cozy home atmosphere,

wooden dining table,
soft natural lighting,

casual but realistic placement,
NOT too many items,

ONLY dinnerware, no teapot, no tea set
【测试结果】

* dreamshaperXL：生成类别中有茶壶串入，并且品种和数量不符
* epiCrealism：生成造型接近餐具，但有点怪，且品种和数量不符
* realvisxl50：生成造型最接近餐具，但品种和数量不符

1.3 社交分享图（对准确率要求最低）
【prompt】
MASTERPIECE, social lifestyle photography

a beautifully arranged dining table,
celadon ceramic dinnerware set,

top view composition,
plates and bowls with food,

aesthetic plating,
clean layout,

modern home dining scene,
sharing meal atmosphere,

ONLY dinnerware, no teapot, no tea set
【测试结果】

* dreamshaperXL：生成类别中有茶壶串入，并且品种和数量不符
* epiCrealism：生成了白瓷
* realvisxl50：生成造型最接近餐具，品种和数量基本符合



【对于产品器形和数量不符的解决计划】

* 重新架构

在 1.1 产品图测试中遇到的品种污染（茶壶串入）和数量不对，本质上是因为 Stable Diffusion XL 模型在处理复杂的“碗、盘、盆组合”提示词时，它的注意力机制（Attention）会产生“语义漂移”和“计数幻觉”。把复杂任务拆解为\*\*“单件生成” $\\rightarrow$ “背景生成” $\\rightarrow$ “最终组合渲染”\*\*，是完全成熟且可行的 ComfyUI API 工作流。

（阅读【ComfyUI组合式产品图架构.docx】）

* 单独增加单件器皿的生成步骤，逐一确认后组合为整体
* 在模型中增加上传釉色参考图片功能，选择釉色后，自动切换到该釉色的参考图，前端让客户选择釉色时也展示同一张图片
* 允许客户修改设置，而非每一次都要从头开始







## 2026-04-30 架构同步：造境 / 瓷韵工作流分工

当前判断：

* 造境流程中继续开放“选择引擎”会增加用户理解成本，并放大釉色与器形还原不稳定的问题。
* 造境当前产品图生成仍存在釉色还原不准确、器形不稳定的问题，因此产品初稿不应继续完全依赖造境工作流直接生成。
* 新增独立项目目录 `D:\PixelSmile\CeramicFusion`，用于推进“瓷韵”工作流。

新的流程分工：

* 造境阶段取消用户侧“选择引擎和釉色”的组合入口，改为只选择釉色。
* 釉色选择负责决定后端引擎、提示词锚点和后续生成策略。
* 用户选择釉色后进入产品器形选择。
* 器形选择后转入 CeramicFusion / 瓷韵工作流，将 `D:\PixelSmile\imgs` 中的釉色图片与无背景器形图片融合，生成产品初稿。
* `D:\PixelSmile\imgs\Origin` 为备份目录，不参与业务读取；其他目录分别作为釉色图和不同类别产品器形图来源。
* 产品初稿完成后，再回到造境工作流，继续生成产品氛围图、商务馈赠图或自用生活场景图。

架构图理解：

* Hearth Studio 入口进入导购流程。
* 第一段由造境负责：选择釉色，釉色决定引擎和提示词。
* 第二段由瓷韵负责：选择器形，融合釉色与器形，生成产品初稿。
* 第三段回到造境：选择产品用途、包装、场景等，生成产品氛围图。
* 后续正式定制设计阶段再进入青瓷图生图与 PolyView 等工作流，分别生成整形工艺融合图和多角度图。



## 2026-04-30 补充：CeramicFusion 回流造境后的数量一致性

瓷韵生成产品初稿之后，需要回到造境。造境后续重点不再是重新生成产品，而是使用瓷韵输出的产品初稿作为固定素材，完成产品进入氛围图的组合与场景化表达。

这一阶段的核心问题是数量不符：产品本体已经由瓷韵确认，造境只需要把已确认的器形、数量和组合关系放入环境、社交或商务馈赠氛围图中，避免再次由文生图模型自行解释产品数量和器形。

## 2026-04-30 衔接 CeramicFusion：釉色驱动与产品融合入口

本次调整目标：

* SceneForge 第一阶段不再让客户选择“引擎 + 釉色”，改为只选择釉色。
* 釉色在后台决定引擎、checkpoint、采样参数和提示词锚点，降低客户决策成本。
* 产品选择阶段为每个产品行增加“打开瓷韵融合”按钮。
* 按钮会把当前釉色和产品素材映射为 CeramicFusion URL 参数，并在新标签页打开 `http://127.0.0.1:8765`。
* CeramicFusion 已支持读取 URL 参数自动预选釉色、产品类别和产品图。

当前映射策略：

* 粉青釉：写实优先，默认对应 `glaze_fq_1_new.png`。
* 梅子青：质感与高光优先，默认对应 `glaze_mzq_1_new.png`。
* 影青釉：快速预览优先，默认对应 `glaze_yq_1_new.png`。

后续需要把测试矩阵中的最佳组合回写到 `GLAZE_ENGINE_CONFIG` 和前端 `glazeRuntime`，让每个釉色走经过验证的引擎与参数。
