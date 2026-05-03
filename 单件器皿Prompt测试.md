# 单件器皿Prompt测试



使用新的工作流：SceneForge\_new.json

提供瓷片参考图片

暂时正面prompt：

MASTERPIECE, high-end gallery photography, a single large (Longquan celadon:1.2) dinner plate, (flawless smooth surface:1.3), (unctuous jade-like texture:1.2), solid uniform color, thick milky glaze, refined porcelain body, museum quality, soft studio lighting.

暂时负面prompt：

(dots, spots, impurities:1.4), (pottery texture:1.3), grainy, rough surface, sand particles, rustic style, crackles, bubbles, earthy tones, blurry, low quality.

【测试结果】

epiCrealism.safetensors表现不行，只能生成色块（但是在旧的工作流中表现还可以，而且生成速度快）

dreamshaperXL\_lightningDPMSDE.safetensors和realvisxlV50\_v50LightningBakedvae.safetensors表现还可以，能够结合瓷片釉色和器形prompt生成比较接近的图片，但是器形和釉色、开片纹发挥还不稳定

【建议】

场景氛围图中并不要求器形和釉色绝对真实，但是产品图中数量和造型要基本符合，氛围图要能够激发购物欲，生成速度不要太慢
