// ========== 图片服务器地址 ==========
const IMG_BASE_URL = "http://127.0.0.1:8888";

// ========== 釉色配置（18种） ==========
const glazeTypes = [
  { code: "yyms", name: "越窑秘色釉", desc: "青中带绿 · 玻璃感 · 鲜活", variants: [1] },
  { code: "rytq", name: "汝窑天青釉", desc: "天青微灰 · 奶油感 · 润", variants: [1, 2, 3] },
  { code: "gytq", name: "官窑天青釉", desc: "厚釉开片 · 冰裂纹 · 结构感", variants: [1, 2, 3] },
  { code: "geyhq", name: "哥窑灰青釉", desc: "灰青沧桑 · 铁胎粗粝 · 大开片", variants: [1, 2] },
  { code: "jytl", name: "钧窑天蓝釉", desc: "窑变花釉 · 紫红斑 · 流动感", variants: [1] },
  { code: "dyyb", name: "定窑月白釉", desc: "白中冷青 · 薄釉柔光", variants: [1] },
  { code: "lqyfq", name: "龙泉窑粉青釉", desc: "柔粉青绿 · 厚釉玉质感", variants: [1, 2] },
  { code: "lqymzq", name: "龙泉窑梅子青釉", desc: "深青浓翠 · 稳重玉质", variants: [1, 2] },
  { code: "htyyq", name: "湖田窑影青釉", desc: "白中透青 · 玻璃质感 · 清透", variants: [1, 2, 3] }
];

// 釉色引擎映射
const glazeEngineMap = {
  "yyms_1": { model_type: "realistic", model_label: "越窑秘色 · 写实引擎", glazeFile: "yyms_1.png" },
  "rytq_1": { model_type: "artistic", model_label: "汝窑天青 · 艺术引擎", glazeFile: "rytq_1.png" },
  "rytq_2": { model_type: "artistic", model_label: "汝窑天青 · 艺术引擎", glazeFile: "rytq_2.png" },
  "rytq_3": { model_type: "artistic", model_label: "汝窑天青 · 艺术引擎", glazeFile: "rytq_3.png" },
  "gytq_1": { model_type: "realistic", model_label: "官窑天青 · 写实引擎", glazeFile: "gytq_1.png" },
  "gytq_2": { model_type: "realistic", model_label: "官窑天青 · 写实引擎", glazeFile: "gytq_2.png" },
  "gytq_3": { model_type: "realistic", model_label: "官窑天青 · 写实引擎", glazeFile: "gytq_3.png" },
  "geyhq_1": { model_type: "realistic", model_label: "哥窑灰青 · 写实引擎", glazeFile: "geyhq_1.png" },
  "geyhq_2": { model_type: "realistic", model_label: "哥窑灰青 · 写实引擎", glazeFile: "geyhq_2.png" },
  "jytl_1": { model_type: "artistic", model_label: "钧窑天蓝 · 艺术引擎", glazeFile: "jytl_1.png" },
  "dyyb_1": { model_type: "fast", model_label: "定窑月白 · 快速引擎", glazeFile: "dyyb_1.png" },
  "lqyfq_1": { model_type: "artistic", model_label: "龙泉粉青 · 艺术引擎", glazeFile: "lqyfq_1.png" },
  "lqyfq_2": { model_type: "artistic", model_label: "龙泉粉青 · 艺术引擎", glazeFile: "lqyfq_2.png" },
  "lqymzq_1": { model_type: "artistic", model_label: "龙泉梅子青 · 艺术引擎", glazeFile: "lqymzq_1.png" },
  "lqymzq_2": { model_type: "artistic", model_label: "龙泉梅子青 · 艺术引擎", glazeFile: "lqymzq_2.png" },
  "htyyq_1": { model_type: "fast", model_label: "湖田影青 · 快速引擎", glazeFile: "htyyq_1.png" },
  "htyyq_2": { model_type: "fast", model_label: "湖田影青 · 快速引擎", glazeFile: "htyyq_2.png" },
  "htyyq_3": { model_type: "fast", model_label: "湖田影青 · 快速引擎", glazeFile: "htyyq_3.png" }
};

// ========== 产品原始数据（从表格整理）==========
const productRawData = [
  // 餐具 tableware (1-10)
  { id: "bowl_1", label: "1号碗", category: "tableware", file: "bowl_1.png" },
  { id: "bowl_l_1", label: "1号大碗", category: "tableware", file: "bowl_l_1.png" },
  { id: "bowl_m_1", label: "1号中碗", category: "tableware", file: "bowl_m_1.png" },
  { id: "bowl_s_1", label: "1号小碗", category: "tableware", file: "bowl_s_1.png" },
  { id: "fruit_bowl_1", label: "1号果盘", category: "tableware", file: "fruit_bowl_1.png" },
  { id: "plate_l_1", label: "1号大盘", category: "tableware", file: "plate_l_1.png" },
  { id: "plate_l_2", label: "2号大盘", category: "tableware", file: "plate_l_2.png" },
  { id: "plate_m_1", label: "1号中盘", category: "tableware", file: "plate_m_1.png" },
  { id: "salad_bowl_l_1", label: "1号沙拉碗", category: "tableware", file: "salad_bowl_l_1.png" },
  { id: "sauce_dish_1", label: "1号调料碟", category: "tableware", file: "sauce_dish_1.png" },
  
  // 茶具 teaware (11-24)
  { id: "teapot_1", label: "1号茶壶", category: "teaware", file: "teapot_1.png" },
  { id: "teapot_2_lefthand", label: "2号茶壶（左手）", category: "teaware", file: "teapot_2_lefthand.png" },
  { id: "teapot_2_righthand", label: "2号茶壶（右手）", category: "teaware", file: "teapot_2_righthand.png" },
  { id: "teapot_3", label: "3号茶壶", category: "teaware", file: "teapot_3.png" },
  { id: "teaset_3", label: "3号茶具组", category: "teaware", file: "teaset_3.png" },
  { id: "gaiwan_1", label: "1号盖碗", category: "teaware", file: "gaiwan_1.png" },
  { id: "fairness_cup_1", label: "1号公道杯", category: "teaware", file: "fairness_cup_1.png" },
  { id: "fairness_cup_2", label: "2号公道杯", category: "teaware", file: "fairness_cup_2.png" },
  { id: "teacup_1", label: "1号茶杯", category: "teaware", file: "teacup_1.png" },
  { id: "teacup_2", label: "2号茶杯", category: "teaware", file: "teacup_2.png" },
  { id: "teacup_3", label: "3号茶杯", category: "teaware", file: "teacup_3.png" },
  { id: "tea_basin_1", label: "1号茶洗", category: "teaware", file: "tea_basin_1.png" },
  { id: "incense_burner_1", label: "1号薰香炉", category: "teaware", file: "incense_burner_1.png" },
  
  // 咖啡具 coffeeware (25-28)
  { id: "coffee_pot_1", label: "1号咖啡壶", category: "coffeeware", file: "coffee_pot_1.png" },
  { id: "cup_saucer_1", label: "1号咖啡杯碟", category: "coffeeware", file: "cup_saucer_1.png" },
  { id: "coffee_set_1", label: "1号咖啡组", category: "coffeeware", file: "coffee_set_1.png" },
  { id: "mug_1", label: "1号马克杯", category: "coffeeware", file: "mug_1.png" },
  
  // 家居摆设 homedecor (29-46)
  { id: "jar_genenral_1", label: "1号将军罐", category: "homedecor", file: "jar_genenral_1.png" },
  { id: "vase_mei_1", label: "1号梅瓶", category: "homedecor", file: "vase_mei_1.png" },
  { id: "vase_mei_2", label: "2号梅瓶", category: "homedecor", file: "vase_mei_2.png" },
  { id: "vase_lamp_base_1", label: "1号台灯座", category: "homedecor", file: "vase_lamp_base_1.png" },
  { id: "vase_lamp_base_2", label: "2号台灯座", category: "homedecor", file: "vase_lamp_base_2.png" },
  { id: "plaque_1", label: "1号瓷版画", category: "homedecor", file: "plaque_1.png" },
  { id: "plaque_2", label: "2号瓷版画", category: "homedecor", file: "plaque_2.png" },
  { id: "plaque_3", label: "3号瓷版画", category: "homedecor", file: "plaque_3.png" },
  { id: "plaque_4", label: "4号瓷版画", category: "homedecor", file: "plaque_4.png" },
  { id: "plaque_5", label: "5号瓷版画", category: "homedecor", file: "plaque_5.png" },
  { id: "plaque_6", label: "6号瓷版画", category: "homedecor", file: "plaque_6.png" },
  { id: "plaque_7", label: "7号瓷版画", category: "homedecor", file: "plaque_7.png" },
  { id: "sculpture_1", label: "1号雕塑", category: "homedecor", file: "sculpture_1.png" },
  { id: "sculpture_2", label: "2号雕塑", category: "homedecor", file: "sculpture_2.png" },
  { id: "sculpture_3", label: "3号雕塑", category: "homedecor", file: "sculpture_3.png" },
  { id: "sculpture_4", label: "4号雕塑", category: "homedecor", file: "sculpture_4.png" },
  { id: "sculpture_5", label: "5号雕塑", category: "homedecor", file: "sculpture_5.png" },
  { id: "sculpture_6", label: "6号雕塑", category: "homedecor", file: "sculpture_6.png" },
  { id: "sculpture_7", label: "7号雕塑", category: "homedecor", file: "sculpture_7.png" },
  { id: "sculpture_8", label: "8号雕塑", category: "homedecor", file: "sculpture_8.png" }
];

// ========== 从原始数据自动生成分类目录 ==========
function buildProductCatalog() {
  const catalog = {
    tableware: [],
    teaware: [],
    coffeeware: [],
    homedecor: []
  };
  
  productRawData.forEach(product => {
    if (catalog[product.category]) {
      catalog[product.category].push({
        id: product.id,
        label: product.label,
        file: product.file
      });
    }
  });
  
  return catalog;
}

// 产品目录（按大类分组，自动生成）
const productCatalogByCategory = buildProductCatalog();

// 产品大类配置（从原始数据动态生成）
const productCategories = [
  { code: "tableware", name: "餐具", desc: `共 ${productCatalogByCategory.tableware.length} 款`, previewFile: productCatalogByCategory.tableware[0]?.file || "bowl_1.png" },
  { code: "teaware", name: "茶具", desc: `共 ${productCatalogByCategory.teaware.length} 款`, previewFile: productCatalogByCategory.teaware[0]?.file || "teapot_1.png" },
  { code: "coffeeware", name: "咖啡具", desc: `共 ${productCatalogByCategory.coffeeware.length} 款`, previewFile: productCatalogByCategory.coffeeware[0]?.file || "coffee_pot_1.png" },
  { code: "homedecor", name: "家居摆设", desc: `共 ${productCatalogByCategory.homedecor.length} 款`, previewFile: productCatalogByCategory.homedecor[0]?.file || "vase_mei_1.png" }
];

// 包装配置
const packageList = [
  { id: "1", name: "简易环保纸盒", desc: "简约自然 / 环保降解", file: "pkg_simple.jpg" },
  { id: "2", name: "精美丝绒礼盒", desc: "雅致礼遇 / 烫金工艺", file: "pkg_luxury.jpg" },
  { id: "3", name: "高档珍藏木盒", desc: "榫卯结构 / 传世收藏", file: "pkg_wood.jpg" }
];

// 场景配置
const sceneConfig = {
  dinnerware: [
    { id: "grand_round", label: "中餐大圆桌", p: "on a large traditional Chinese round dining table, luxury setting" },
    { id: "long_table", label: "西餐长桌", p: "on a minimalist modern long dining table" },
    { id: "square_table", label: "温馨方桌", p: "on a cozy family square wooden table" }
  ],
  tea: [
    { id: "tatami", label: "禅茶室 (榻榻米)", p: "on a low Japanese tatami tea table, garden background" },
    { id: "master_desk", label: "专业茶台", p: "on a professional stone or wood tea ceremony table" },
    { id: "desk_corner", label: "单人书室", p: "on a scholar's wooden desk corner" }
  ],
  coffee: [
    { id: "cafe_corner", label: "现代咖啡角", p: "in a bright minimalist cafe corner" },
    { id: "office_desk", label: "办公位", p: "on a clean professional office desk" }
  ],
  decor: [
    { id: "vase_scene", label: "条案/几页 (屏风前)", p: "on a traditional Chinese console table, silk screen background" },
    { id: "lamp_scene", label: "卧室床头", p: "on a minimalist bedside table, soft interior lighting" },
    { id: "plaque_scene", label: "博古架/挂墙", p: "displayed on a luxury wooden gallery shelf" },
    { id: "sculpture_scene", label: "玄关展示", p: "placed in a high-end foyer entrance cabinet" }
  ]
};

// 氛围配置
const moodConfig = {
  dinnerware: [
    { id: "m1", label: "家庭聚餐 (温暖)", s: "warm family gathering atmosphere, soft yellow lighting, reunion feel" },
    { id: "m2", label: "宴请宾客 (高雅)", s: "elegant banquet lighting, high-end hotel restaurant vibe, luxury" },
    { id: "m3", label: "家居日常 (轻松)", s: "casual daily life atmosphere, bright natural daylight, simple lifestyle" }
  ],
  tea: [
    { id: "m4", label: "禅意静思 (静谧)", s: "zen silence, wabi-sabi style, shadows of bamboo, morning mist" },
    { id: "m5", label: "茶艺表演 (高雅)", s: "formal tea ceremony style, theatrical lighting, sophisticated" },
    { id: "m6", label: "亲友茶会 (温暖)", s: "friendly gathering, relaxed tea time, warm and cozy social vibe" }
  ],
  coffee: [
    { id: "m7", label: "家庭温馨", s: "homey morning coffee vibe, soft focus background, comfortable" },
    { id: "m8", label: "办公高级", s: "modern executive office style, sharp professional lighting" },
    { id: "m9", label: "单人随意", s: "solitary relaxing moment, cinematic moody light, personal time" }
  ],
  decor: [
    { id: "m10", label: "中式装饰", s: "traditional Chinese aesthetic, ink wash style, classic heritage" },
    { id: "m11", label: "西式装饰", s: "modern western interior design, minimalist, clean lines" },
    { id: "m12", label: "日韩装饰", s: "Muji style, natural wood, zen minimalist, soft tones" },
    { id: "m13", label: "美式装饰", s: "American classic interior, retro luxury, heavy wood textures" }
  ]
};

// ========== 全局状态 ==========
let historyStack = ["step0"];
let formData = {
  customer_name: "", customer_contact: "",
  glaze: "", glaze_code: "", glaze_variant: "", glaze_label: "",
  model_type: "", model_label: "",
  purpose: "", purpose_label: "",
  category: "dinnerware", category_label: "",
  items: {},
  selected_product_id: "", selected_product_label: "", selected_product_file: "", selected_product_category: "",
  fused_product_path: "", fusion_linked: false,
  scene: "", scene_label: "", scene_prompt: "",
  mood: "", mood_label: "",
  packaging: "none", packaging_label: "系统默认",
  style: "",
  custom: ""
};

// 产品清单管理
let productList = [];  // 存储选中的产品 { product, quantity }

let selectedGlazeType = null;
let selectedGlazeVariant = null;
let selectedGlazeFullCode = null;

let selectedProductCategory = null;
let selectedProduct = null;

// ========== 初始化 ==========
document.addEventListener("DOMContentLoaded", () => {
  renderGlazeTypeGrid();
  renderProductCategories();
  renderPackageCards();
  
  fetch(`${IMG_BASE_URL}/glaze/yyms_1.png`)
    .then(res => { if (!res.ok) console.warn("图片服务器未启动"); })
    .catch(err => console.warn("图片服务器连接失败:", err));
});

// ========== 釉色种类选择 ==========
function renderGlazeTypeGrid() {
  const grid = document.getElementById("glazeTypeGrid");
  if (!grid) return;
  grid.innerHTML = "";
  
  glazeTypes.forEach(glaze => {
    const card = document.createElement("div");
    card.className = "glaze-card";
    card.dataset.glazeCode = glaze.code;
    card.onclick = () => selectGlazeType(glaze);
    
    const previewVariant = glaze.variants[0];
    const imgPath = `${IMG_BASE_URL}/glaze/${glaze.code}_${previewVariant}.png`;
    
    card.innerHTML = `
      <img src="${imgPath}" alt="${glaze.name}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%25%22 height=%22160%22%3E%3Crect width=%22100%25%22 height=%22160%22 fill=%22%23eee%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23999%22%3E${glaze.name}%3C/text%3E%3C/svg%3E'">
      <div class="glaze-name">${glaze.name}</div>
      <div class="glaze-desc">${glaze.desc}</div>
      <div class="glaze-code">${glaze.variants.length}种编号可选</div>
    `;
    grid.appendChild(card);
  });
}

function selectGlazeType(glaze) {
  selectedGlazeType = glaze;
  selectedGlazeVariant = null;
  selectedGlazeFullCode = null;
  
  document.querySelectorAll("#glazeTypeGrid .glaze-card").forEach(card => {
    card.classList.remove("selected");
    if (card.dataset.glazeCode === glaze.code) card.classList.add("selected");
  });
  
  document.getElementById("nextToVariantBtn").disabled = false;
}

function goToVariantStep() {
  if (!selectedGlazeType) {
    alert("请先选择釉色种类");
    return;
  }
  
  document.getElementById("selectedGlazeName").innerText = selectedGlazeType.name;
  
  const variantGrid = document.getElementById("glazeVariantGrid");
  variantGrid.innerHTML = "";
  
  selectedGlazeType.variants.forEach(variant => {
    const card = document.createElement("div");
    card.className = "glaze-card";
    card.dataset.variant = variant;
    card.onclick = () => selectGlazeVariant(variant);
    
    const imgPath = `${IMG_BASE_URL}/glaze/${selectedGlazeType.code}_${variant}.png`;
    card.innerHTML = `
      <img src="${imgPath}" alt="${selectedGlazeType.name} ${variant}号" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%25%22 height=%22160%22%3E%3Crect width=%22100%25%22 height=%22160%22 fill=%22%23eee%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23999%22%3E${selectedGlazeType.name} ${variant}号%3C/text%3E%3C/svg%3E'">
      <div class="glaze-name">${selectedGlazeType.name}</div>
      <div class="glaze-desc">${variant}号 · ${selectedGlazeType.desc}</div>
    `;
    variantGrid.appendChild(card);
  });
  
  pushStep("step0_variant");
}

function selectGlazeVariant(variant) {
  selectedGlazeVariant = variant;
  selectedGlazeFullCode = `${selectedGlazeType.code}_${variant}`;
  
  document.querySelectorAll("#glazeVariantGrid .glaze-card").forEach(card => {
    card.classList.remove("selected");
    if (parseInt(card.dataset.variant) === variant) card.classList.add("selected");
  });
  
  document.getElementById("confirmGlazeBtn").disabled = false;
}

function confirmGlazeSelection() {
  if (!selectedGlazeFullCode) {
    alert("请选择具体的釉色编号");
    return;
  }
  
  const engine = glazeEngineMap[selectedGlazeFullCode];
  if (!engine) {
    alert(`未找到釉色配置: ${selectedGlazeFullCode}`);
    return;
  }
  
  formData.glaze = selectedGlazeFullCode;
  formData.glaze_code = selectedGlazeType.code;
  formData.glaze_variant = selectedGlazeVariant;
  formData.glaze_label = `${selectedGlazeType.name} ${selectedGlazeVariant}号`;
  formData.model_type = engine.model_type;
  formData.model_label = engine.model_label;
  
  updateSummary();
  pushStep("step1");
}

function popToGlazeType() {
  pushStep("step0");
}

// ========== 客户信息 ==========
function syncCustomerInfo() {
  formData.customer_name = document.getElementById("customerName").value.trim();
  formData.customer_contact = document.getElementById("customerContact").value.trim();
  updateSummary();
}

// ========== 产品大类 ==========
function renderProductCategories() {
  const grid = document.getElementById("productCategoryGrid");
  if (!grid) return;
  grid.innerHTML = "";
  
  productCategories.forEach(cat => {
    const card = document.createElement("div");
    card.className = "product-category-card";
    card.dataset.categoryCode = cat.code;
    card.onclick = () => selectProductCategory(cat);
    
    const imgPath = `${IMG_BASE_URL}/${cat.code}/${cat.previewFile}`;
    
    card.innerHTML = `
      <img src="${imgPath}" alt="${cat.name}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%25%22 height=%22160%22%3E%3Crect width=%22100%25%22 height=%22160%22 fill=%22%23eee%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23999%22%3E${cat.name}%3C/text%3E%3C/svg%3E'">
      <div class="category-name">${cat.name}</div>
      <div class="category-desc">${cat.desc}</div>
    `;
    grid.appendChild(card);
  });
}

function selectProductCategory(category) {
  selectedProductCategory = category;
  selectedProduct = null;
  
  document.querySelectorAll("#productCategoryGrid .product-category-card").forEach(card => {
    card.classList.remove("selected");
    if (card.dataset.categoryCode === category.code) card.classList.add("selected");
  });
  
  // 启用下一步按钮
  const nextBtn = document.getElementById("nextToProductStepBtn");
  if (nextBtn) nextBtn.disabled = false;
}

function goToProductStep() {
  if (!selectedProductCategory) {
    alert("请先选择产品大类");
    return;
  }
  
  // 提示跨类别警告
  if (productList.length > 0 && productList[0].product.category !== selectedProductCategory.code) {
    alert("⚠️ 您已选择其他大类的产品，当前类别不同。\n请先完成当前清单或重新开始。");
    return;
  }
  
  document.getElementById("selectedCategoryName").innerText = selectedProductCategory.name;
  
  const productGrid = document.getElementById("productGrid");
  productGrid.innerHTML = "";
  
  const products = productCatalogByCategory[selectedProductCategory.code];
  products.forEach(product => {
    // 检查是否已在清单中
    const isSelected = productList.some(item => item.product.id === product.id);
    
    const card = document.createElement("div");
    card.className = "product-card";
    if (isSelected) card.classList.add("selected");
    card.dataset.productId = product.id;
    card.onclick = () => selectSpecificProduct(product);
    
    const imgPath = `${IMG_BASE_URL}/${selectedProductCategory.code}/${product.file}`;
    card.innerHTML = `
      <img src="${imgPath}" alt="${product.label}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%25%22 height=%22130%22%3E%3Crect width=%22100%25%22 height=%22130%22 fill=%22%23eee%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23999%22%3E${product.label}%3C/text%3E%3C/svg%3E'">
      <b>${product.label}</b>
      ${isSelected ? '<span style="color:var(--primary-color);font-size:11px;"> ✓ 已添加</span>' : ''}
    `;
    productGrid.appendChild(card);
  });
  
  pushStep("step_product_select");
}

// 渲染产品清单
function renderProductList() {
  const container = document.getElementById("productListContainer");
  if (!container) return;
  
  if (productList.length === 0) {
    container.innerHTML = '<div style="padding:20px;text-align:center;color:#999;">暂无产品，请点击"继续添加产品"选择</div>';
    return;
  }
  
  let html = '<table style="width:100%; border-collapse: collapse;">';
  html += '<thead><tr style="background:#f0f4f2;"><th style="padding:12px; text-align:left;">产品名称</th><th style="padding:12px;">数量</th><th style="padding:12px;">操作</th></tr></thead><tbody>';
  
  productList.forEach((item, index) => {
    html += `
      <tr style="border-bottom:1px solid #eee;">
        <td style="padding:12px;">${item.product.label}</td>
        <td style="padding:12px; text-align:center;">
          <button onclick="updateQuantity(${index}, -1)" style="padding:4px 10px;">-</button>
          <span style="margin:0 12px; min-width:40px; display:inline-block;">${item.quantity}</span>
          <button onclick="updateQuantity(${index}, 1)" style="padding:4px 10px;">+</button>
        </td>
        <td style="padding:12px; text-align:center;">
          <button onclick="removeProduct(${index})" style="background:#dc3545; color:white; border:none; padding:4px 12px; border-radius:4px; cursor:pointer;">删除</button>
        </td>
      </tr>
    `;
  });
  
  html += '</tbody></table>';
  container.innerHTML = html;
}

function updateQuantity(index, delta) {
  const newQty = productList[index].quantity + delta;
  if (newQty < 1) {
    removeProduct(index);
  } else {
    productList[index].quantity = newQty;
    renderProductList();
  }
}

function removeProduct(index) {
  const removed = productList[index];
  if (confirm(`确定删除 ${removed.product.label} 吗？`)) {
    productList.splice(index, 1);
    renderProductList();
    
    // 同步更新产品选择页的勾选状态
    if (document.getElementById("step_product_select")?.classList.contains("active")) {
      goToProductStep();  // 刷新产品页，移除勾选标记
    }
    
    if (productList.length === 0) {
      // 清单为空，提示用户
      alert("产品清单已清空，请继续添加产品");
    }
  }
}

function backToProductSelect() {
  pushStep("step_product_select");
}

function confirmFinishList() {
  if (productList.length === 0) {
    alert("请至少添加一个产品");
    return;
  }
  
  // 显示清单确认对话框
  let itemsText = "请确认您的产品清单：\n\n";
  productList.forEach(item => {
    itemsText += `  ${item.product.label} x ${item.quantity}\n`;
  });
  itemsText += "\n确认无误后点击确定继续。";
  
  if (!confirm(itemsText)) {
    return;
  }
  
  // 保存到 formData
  formData.items = {};
  productList.forEach(item => {
    formData.items[item.product.id] = item.quantity;
  });
  formData.selected_product_id = productList[0].product.id;
  formData.selected_product_label = productList[0].product.label;
  formData.selected_product_file = productList[0].product.file;
  formData.selected_product_category = selectedProductCategory.code;
  
  updateSummary();
  
  // 根据用途跳转
  if (formData.purpose === 'gift') {
    // 确保包装区域显示
    const pkgSection = document.getElementById("packagingSection");
    if (pkgSection) {
      pkgSection.style.display = "block";
    }
    // 渲染包装卡片
    renderPackageCards();
    pushStep("step_quantity");
  } else {
    pushStep("step_fusion_return");
  }
}

function selectSpecificProduct(product) {
  selectedProduct = product;
  
  // 弹出数量输入框
  const quantity = prompt(`请输入 ${product.label} 的数量：`, "1");
  if (quantity === null) return;
  
  const qty = parseInt(quantity);
  if (isNaN(qty) || qty < 1) {
    alert("请输入有效的数量（大于0）");
    return;
  }
  
  // 检查是否已有相同产品
  const existingIndex = productList.findIndex(item => item.product.id === product.id);
  if (existingIndex >= 0) {
    productList[existingIndex].quantity = qty;
  } else {
    productList.push({ product: product, quantity: qty });
  }
  
  // 更新UI高亮
  document.querySelectorAll("#productGrid .product-card").forEach(card => {
    card.classList.remove("selected");
    if (card.dataset.productId === product.id) card.classList.add("selected");
  });
  
  // 刷新清单显示
  renderProductList();
  
  // 提示用户
  alert(`已添加 ${product.label} x ${qty}\n\n点击"确认清单"完成，或点击"继续添加产品"添加更多。`);
}
  
function selectSpecificProduct(product) {
  selectedProduct = product;
  
  // 弹出数量输入框
  const quantity = prompt(`请输入 ${product.label} 的数量：`, "1");
  if (quantity === null) return;
  
  const qty = parseInt(quantity);
  if (isNaN(qty) || qty < 1) {
    alert("请输入有效的数量（大于0）");
    return;
  }
  
  // 检查是否已有相同产品
  const existingIndex = productList.findIndex(item => item.product.id === product.id);
  if (existingIndex >= 0) {
    productList[existingIndex].quantity = qty;
  } else {
    productList.push({ product: product, quantity: qty });
  }
  
  // 更新UI高亮
  document.querySelectorAll("#productGrid .product-card").forEach(card => {
    card.classList.remove("selected");
    if (card.dataset.productId === product.id) card.classList.add("selected");
  });
  
  // 跳转到清单确认页
  renderProductList();
  pushStep("step_product_list");
}

// ✅ 添加 confirmProductSelection 函数
function confirmProductSelection() {
  if (!selectedProduct) {
    alert("请选择具体产品");
    return;
  }
  
  // 检查是否跨类别
  if (productList.length > 0) {
    const firstCategory = productList[0].product.category;
    if (firstCategory !== selectedProductCategory.code) {
      alert("⚠️ 不同大类的产品需要分别生成氛围图（因为场景和氛围不同）。\n请先完成当前大类的产品清单，再重新开始选择其他大类。");
      return;
    }
  }
  
  const sceneCategory = { 
    tableware: "dinnerware", 
    teaware: "tea", 
    coffeeware: "coffee", 
    homedecor: "decor" 
  }[selectedProductCategory.code] || "dinnerware";
  
  formData.category = sceneCategory;
  formData.category_label = selectedProductCategory.name;
  
  selectSpecificProduct(selectedProduct);
}

function popToCategoryStep() {
  pushStep("step_category");
}

function popToCategoryStep() {
  pushStep("step_category");
}

// ========== 包装 ==========
function renderPackageCards() {
  const grid = document.getElementById("packageGrid");
  if (!grid) return;
  grid.innerHTML = "";
  
  const packageList = [
    { id: "simple", name: "简易环保包装", file: "pkg_simple.jpg", desc: "简约自然 / 环保降解" },
    { id: "luxury", name: "高档纸质包装", file: "pkg_luxury.jpg", desc: "雅致礼遇 / 烫金工艺" },
    { id: "wood", name: "豪华木质包装", file: "pkg_wood.jpg", desc: "榫卯结构 / 传世收藏" }
  ];
  
  packageList.forEach(pkg => {
    const card = document.createElement("div");
    card.className = "pkg-card";
    card.id = `pkg_${pkg.id}`;
    card.onclick = () => setPackaging(pkg.id, pkg.name);
    const imgPath = `${IMG_BASE_URL}/package/${pkg.file}`;
    card.innerHTML = `
      <img src="${imgPath}" alt="${pkg.name}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%25%22 height=%22150%22%3E%3Crect width=%22100%25%22 height=%22150%22 fill=%22%23eee%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23999%22%3E${pkg.name}%3C/text%3E%3C/svg%3E'">
      <div style="padding:10px;">
        <b>${pkg.name}</b><br>
        <small>${pkg.desc}</small>
      </div>
    `;
    grid.appendChild(card);
  });
}

function setPackaging(id, label) {
  formData.packaging = id;
  formData.packaging_label = label;
  
  // UI 高亮
  document.querySelectorAll("#packageGrid .pkg-card").forEach(card => {
    card.classList.remove("selected");
  });
  const selectedCard = document.getElementById(`pkg_${id}`);
  if (selectedCard) selectedCard.classList.add("selected");
  
  updateSummary();
}

function linkCustomerProduct() {
  // 使用真实存在的测试图片
  formData.fused_product_path = "D:/PixelSmile/imgs/tableware/bowl_1.png";
  formData.fusion_linked = true;
  
  const cont = document.getElementById("quantityContainer");
  if (cont) {
    cont.innerHTML = `
      <div class="quantity-row row-selected">
        <span><b>测试产品初稿</b><br><small>${formData.fused_product_path}</small></span>
        <span class="badge">✅ 已关联（测试）</span>
      </div>
    `;
  }
  
  updateSummary();
  pushStep("step_quantity");
}

function goToSceneStep() {
  if (!formData.selected_product_id) { 
    alert("请选择产品器形"); 
    return; 
  }
  if (!formData.fusion_linked) { 
    alert("请先关联瓷韵生成的产品初稿"); 
    return; 
  }
  if (formData.purpose === 'gift' && formData.packaging === 'none') { 
    alert("请选择商务馈赠包装"); 
    return; 
  }
  pushStep('step4');
}

// ========== 场景和氛围选择 ==========
function setChoice(key, id, label, nextId) {
  console.log("setChoice 调用:", key, id, label, nextId);  // 添加日志
  
  formData[key] = id;
  formData[key + "_label"] = label;
  
  if (key === 'scene') {
    formData.scene_prompt = label;
  }
  if (key === 'mood') {
    formData.style = label;
    // 启用生成按钮
    const genBtn = document.getElementById("genBtn");
    if (genBtn) {
      genBtn.disabled = false;
      genBtn.style.background = "var(--primary-color)";
      genBtn.innerText = "开始 AI 渲染生成 (共3张)";
    }
  }
  
  if (key === 'purpose') {
    // 包装相关逻辑...
  }
  
  updateSummary();
  if (nextId) pushStep(nextId);
}

// ========== 步骤导航 ==========
function pushStep(nextId) {
  if (!nextId) return;
  if (!document.getElementById(nextId)) {
    console.error("Step not found:", nextId);
    return;
  }
  
  // ========== 进入产品大类选择页时，确保网格已渲染 ==========
  if (nextId === 'step_category') {
    const grid = document.getElementById("productCategoryGrid");
    if (grid && grid.children.length === 0) {
      renderProductCategories();  // 确保大类网格已渲染
    }
  }
  
  // ========== 进入具体产品选择页时，根据选中大类渲染产品 ==========
  if (nextId === 'step_product_select') {
    if (!selectedProductCategory) {
      alert("请先选择产品大类");
      popStep();  // 返回上一步
      return;
    }
    
    document.getElementById("selectedCategoryName").innerText = selectedProductCategory.name;
    
    const productGrid = document.getElementById("productGrid");
    if (productGrid) {
      productGrid.innerHTML = "";
      
      const products = productCatalogByCategory[selectedProductCategory.code];
      if (products && products.length > 0) {
        products.forEach(product => {
          const card = document.createElement("div");
          card.className = "product-card";
          card.dataset.productId = product.id;
          card.onclick = () => selectSpecificProduct(product);
          
          const imgPath = `${IMG_BASE_URL}/${selectedProductCategory.code}/${product.file}`;
          card.innerHTML = `
            <img src="${imgPath}" alt="${product.label}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%25%22 height=%22130%22%3E%3Crect width=%22100%25%22 height=%22130%22 fill=%22%23eee%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23999%22%3E${product.label}%3C/text%3E%3C/svg%3E'">
            <b>${product.label}</b>
          `;
          productGrid.appendChild(card);
        });
      } else {
        productGrid.innerHTML = '<div style="padding:20px;text-align:center;color:#999;">暂无产品</div>';
      }
    }
  }
  
  // ========== 进入场景选择页 ==========
    if (nextId === 'step4') {
      const grid = document.getElementById("sceneOptions");
      if (grid) {
        grid.innerHTML = "";
        let scenes = sceneConfig[formData.category] || sceneConfig.dinnerware;
        scenes.forEach(s => {
          const btn = document.createElement("button");
          btn.innerText = s.label;
          // 确保这里调用 setChoice
          btn.onclick = () => setChoice('scene', s.id, s.p, 'step5');
          grid.appendChild(btn);
        });
      }
    }
  
  // ========== 进入氛围选择页 ==========
    if (nextId === 'step5') {
      const grid = document.getElementById("moodOptions");
      if (grid) {
        grid.innerHTML = "";
        let moods = moodConfig[formData.category] || moodConfig.dinnerware;
        moods.forEach(m => {
          const btn = document.createElement("button");
          btn.innerText = m.label;
          // 确保这里调用 setChoice，nextId 为 null
          btn.onclick = () => setChoice('mood', m.id, m.s, null);
          grid.appendChild(btn);
        });
      }
    }
  
  // 更新历史栈
  if (historyStack[historyStack.length - 1] !== nextId) {
    historyStack.push(nextId);
  }
  
  // 激活步骤
  document.querySelectorAll(".step").forEach(s => s.classList.remove("active"));
  document.getElementById(nextId).classList.add("active");
  
  updateUI();
}

function popStep() {
  if (historyStack.length <= 1) return;
  historyStack.pop();
  const prevStep = historyStack[historyStack.length - 1];
  document.querySelectorAll(".step").forEach(s => s.classList.remove("active"));
  document.getElementById(prevStep)?.classList.add("active");
  updateUI();
}

function updateUI() {
  document.getElementById("prevBtn").disabled = historyStack.length <= 1;
  const stepCount = Math.min(historyStack.length, 7);
  document.getElementById("bar").style.width = (stepCount / 7) * 100 + "%";
  
  const hint = document.getElementById("deliveryHint");
  hint.innerText = formData.purpose === 'gift' 
    ? "1. 产品展示视角 | 2. 礼盒嵌套展示 | 3. 商务送礼氛围图"
    : "1. 产品展示视角 | 2. 居家使用环境 | 3. 亲友共享/社交氛围图";
  
  updateSummary();
}

function updateSummary() {
  const summary = document.getElementById("summaryDetail");
  const productLine = formData.selected_product_label
    ? `${formData.selected_product_label} (${formData.selected_product_category})`
    : "未选择";
  const fusionLine = formData.fusion_linked ? formData.fused_product_path : "待瓷韵回流";
  const packagingLine = formData.purpose === 'gift' ? ` | 🎁 ${formData.packaging_label}` : "";
  
  summary.innerHTML = `
    <span class="badge">👤 ${formData.customer_name || "未填"}</span>
    <span class="badge">🏺 ${formData.glaze_label || "未选"}</span>
    <span class="badge">🎯 ${formData.purpose_label || "未选"}</span><br>
    <span class="badge">📦 器形</span> ${productLine}${packagingLine}<br>
    <span class="badge">🖼️ 瓷韵初稿</span> ${fusionLine}<br>
    <span class="badge">🏠 场景</span> ${formData.scene_label || "未选"} 
    <span class="badge">✨ 氛围</span> ${formData.mood_label || "未选"}
  `;
}

// ========== 生成氛围图 ==========
async function generate() {
  // 检查必要条件
  if (!formData.glaze) {
    alert("请先选择釉色");
    return;
  }
  if (productList.length === 0) {
    alert("请先选择产品");
    return;
  }
  // 临时注释掉，用于测试
  // if (!formData.fusion_linked) {
  //   alert("请先关联瓷韵生成的产品初稿");
  //   return;
  // }
  if (formData.purpose === 'gift' && formData.packaging === 'none') {
    alert("请选择商务馈赠包装");
    return;
  }
  if (!formData.scene_prompt) {
    alert("请选择场景");
    return;
  }
  if (!formData.style) {
    alert("请选择氛围");
    return;
  }
  
  const btn = document.getElementById("genBtn");
  btn.disabled = true;
  btn.innerText = "生成中...";
  document.getElementById("loading").style.display = "block";
  
  try {
    // 构建产品清单
    const items = {};
    productList.forEach(item => {
      items[item.product.id] = item.quantity;
    });
    
    // 测试用：如果 fused_product_path 为空，使用默认测试图片
    let testImagePath = formData.fused_product_path;
    if (!testImagePath || testImagePath === "") {
      // 根据产品类别选择测试图片
      const testImages = {
        tableware: "http://127.0.0.1:8888/tableware/bowl_1.png",
        teaware: "http://127.0.0.1:8888/teaware/teapot_2_lefthand.png",
        coffeeware: "http://127.0.0.1:8888/coffeeware/coffee_pot_1.png",
        homedecor: "http://127.0.0.1:8888/homedecor/vase_mei_1.png"
      };
      testImagePath = testImages[selectedProductCategory?.code] || "http://127.0.0.1:8888/teaware/teapot_2_lefthand.png";
      console.log("使用测试图片:", testImagePath);
    }
    
    // 构建请求数据
    const requestData = {
      product_image_path: testImagePath,                // 瓷韵产品初稿路径
      glaze: formData.glaze,                            // 釉色代码
      purpose: formData.purpose,                        // personal 或 gift
      category: formData.category,                      // dinnerware/tea/coffee/decor
      items: items,                                     // 产品清单
      scene_prompt: formData.scene_prompt,              // 场景描述
      mood: formData.mood,                              // 氛围ID
      mood_label: formData.mood_label,                  // 氛围中文名
      style: formData.style,                            // 氛围详细描述
      packaging: formData.packaging,                    // 包装类型: simple/luxury/wood
      custom: document.getElementById("customInput").value.trim()
    };
    
    console.log("发送生成请求:", requestData);
    
    const res = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestData)
    });
    
    const data = await res.json();
    
    if (data.status === "ok" && data.images && data.images.length > 0) {
      displayResults(data.images);
      // 显示正式定制按钮
      document.getElementById("formalOrderBtn").style.display = "inline-block";
    } else {
      alert("生成失败，请检查后端服务");
    }
    
  } catch (error) {
    console.error("生成请求失败:", error);
    alert("生成失败，请检查后端服务是否正常运行");
  } finally {
    btn.disabled = false;
    btn.innerText = "开始 AI 渲染生成 (共3张)";
    document.getElementById("loading").style.display = "none";
  }
}

// 显示生成结果
function displayResults(images) {
  const resDiv = document.getElementById("results");
  if (!resDiv) {
    console.error("results 元素不存在");
    return;
  }
  
  resDiv.innerHTML = "";
  
  const titles = formData.purpose === 'gift' 
    ? ['产品展示视角', '礼盒效果展示', '送礼氛围场景']
    : ['产品展示视角', '生活环境氛围', '社交共享氛围'];
  
  images.forEach((url, index) => {
    console.log(`图片 ${index+1}: ${url}`);
    
    const card = document.createElement("div");
    card.className = "image-card";
    const fullUrl = `http://127.0.0.1:8000/download?url=${encodeURIComponent(url)}`;
    
    card.innerHTML = `
      <div style="font-weight:bold; margin-bottom:5px; color:var(--primary-color);">
        视角 ${index+1}: ${titles[index]}
      </div>
      <img src="${fullUrl}" style="cursor: zoom-in; width:100%; border-radius:8px;" 
           onerror="this.onerror=null; this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%25%22 height=%22100%25%22%3E%3Crect width=%22100%25%22 height=%22100%25%22 fill=%22%23eee%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23999%22%3E%E5%9B%BE%E7%89%87%E5%8A%A0%E8%BD%BD%E5%A4%B1%E8%B4%A5%3C/text%3E%3C/svg%3E'"
           onclick="showZoom('${fullUrl}')">
      <button class="btn-main" style="width:100%; margin-top:10px;" 
              onclick="downloadImage('${fullUrl}', 'Hearth_Studio_${titles[index]}.jpg')">
        📥 下载此氛围图
      </button>
    `;
    resDiv.appendChild(card);
  });
}

// ========== 工具函数 ==========
function resetAll() { 
  if(confirm("重置所有选择？")) {
    productList = [];
    location.reload(); 
  } 
}

function showZoom(url) { 
  const overlay = document.getElementById("overlay"); 
  document.getElementById("overlayImg").src = url; 
  overlay.style.display = "flex"; 
}

async function downloadImage(url, filename) { 
  window.open(url, '_blank'); 
}

function goToFormalOrder() { 
  alert("正式定制环节待开发"); 
}