# Hearth Studio 釉色物理定义指南 (Glaze Definitions)

本文件定义了 Hearth Studio 核心产品的视觉物理特性，用于指导 AI 生成引擎准确模拟传统青瓷与影青的质感。

## 1. 粉青 (Fenqing - Bluish Celadon)
* **物理属性**：炻器胎（Stoneware），白胎底，厚乳浊釉。
* **视觉特征**：青中泛蓝，无开片，质感细腻如粉，温润如脂。
* **Prompt 锚点**：
    > (Masterpiece:1.2), exquisite Powder Celadon (Fenqing), solid stoneware body, thick opaque glaze, color is a delicate pale bluish-celadon, strong (bluish undertone:1.3), immaculate and uniform surface, no crackles, smooth polished finish, soft diffused studio lighting.

## 2. 梅子青 (Meiziqing - Greenish Celadon)
* **物理属性**：炻器胎（Stoneware），石灰碱釉，高粘度乳浊感。
* **视觉特征**：青中泛绿，似江南青梅，水润感强但不透明，亮光面。
* **Prompt 锚点**：
    > (Masterpiece:1.2), premium Meiziqing celadon, thick opacified lime-alkali glaze, color is a lush (fresh bluish-green:1.2), strictly avoiding sky blue, liquid-like glossy finish with deep luster, viscous and rich texture, no transparency, solid heavy stoneware body.

## 3. 影青 (Yingqing - Shadow Green/Jade Porcelain)
* **物理属性**：现代白瓷胎（White Porcelain），薄胎，高致密性。
* **视觉特征**：近似现代白瓷的纯净感，釉色中隐隐泛出水绿色，具有和田玉般的温润深度，高亮光泽。
* **Prompt 锚点**：
    > (Masterpiece:1.2), premium Hutian Yingqing celadon, pure modern white porcelain substrate, highly dense and smooth body, (thick opacified glaze:1.2), resembling the texture of fine jade, color is a delicate pale watery-green, subtle shadow-green tint, viscous and rich glaze appearance, bright lustrous finish, deep reflections with a soft edge.

## 负面修正 (Negative Constants)
* **禁忌项**：玻璃透明感、磨砂感、现代廉价发色、多余纹理、火石红过度（口沿）、发黄、发灰。
* **Negative Prompt**:
    > (matte, dry, textured, frosted glass, sandblasted:1.4), (transparent, clear, crystal:1.3), ice, bubbles, patterns, crackles, rough surface, uneven color, grass green, yellow-green.