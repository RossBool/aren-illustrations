# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

[IDENTITY-5-CORE — 5 核心元素硬约束，最前以保证 token 权重]
A cute anime teenage boy character named 'Aren' with the following EXACT features (all 5 are non-negotiable identity anchors — all 5 MUST appear visibly, missing any is wrong):

1. KAMEYAMA-STYLE large ROUND glasses: perfect CIRCULAR frame (height equals width, ratio 1:1), the frame DOMINATES the upper face (very large, similar to 'Ninja Hattori' Kanzo's glasses or Mitsuba Sougo's glasses), thin black metal frame
2. FLUFFY black hair: short-to-medium length (ear to shoulder), soft air-textured tousled messy strands with VISIBLE volume (like after running, NOT slicked back, NOT triangle-cut, NOT anime-protagonist spike)
3. OVERSIZED black jacket: simple/clean design (boyfriend-fit, 30% wider than torso, jacket hangs loosely past hips), NO zippers, NO buttons, NO leather motorcycle details, NO rivets, NO buckles
4. SOFT orange-pink blush: oval on both cheeks only, peachy-orange color (salmon-peach like hex #FFA07A, NOT bright red, NOT pink, NOT spreading), the ONLY pink color on the face
5. Q-VERSION chibi body: head-to-body ratio 1:2.5 (big head, small body, like a trading figure or Nendoroid — NOT realistic 1:7, NOT normal 1:5)

[AVOID — 软负向约束]
AVOID: realistic body proportions, bright red cheeks, leather motorcycle jacket, spiky hair, rectangular glasses, chuunibyou or angry expression, sweat drops, exaggerated blush, open mouth, big smile

[Visual DNA]
Pure white background. Minimalist black pencil line art with Shinkai-style colored-pencil coloring on skin and objects. Slight wobbly hand-drawn pen lines. Visible pencil grain/strokes in color fill. Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI, no 3D render, no anime style exaggeration.

[Theme]
{正文配图主题}

[Structure type]
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

[Core idea]
{这张图要表达的核心意思}

[Composition]
{具体画面：阿任在哪里、正在做什么、主要物件是什么、信息如何流动}

[Suggested elements]
{元素1} / {元素2} / {元素3} / {元素4}

[Chinese handwritten labels]
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

[Color use — strict 5-color rule (with 1 exception)]
- Black: main line art, 阿任's hair/jacket/pants/shoes/glasses frame, all text and frame lines.
- Orange-pink: ONLY for 阿任's cheek blush. Do not use this color for any annotation or object.
- Red: only for key warning/problem/result annotations.
- Orange: only for main flow/path/arrows.
- Blue: only for secondary notes or feedback/system state.
- Skin tone (warm beige / peach): **EXCEPTION** — allowed for 阿任's face/hands, not counted in 5-color rule. Skin is implicit, like paper.
- Object warm tones (wood, coffee, paper): limited to desaturated earth tones, don't dominate. Background must stay clean white.
- Maximum 3 annotation colors per image (chosen from red/orange/blue).

[Final constraints]
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. 阿任 is a real person figure, not a mascot or a piece of machinery — do not stuff 阿任 inside a funnel or a black box; 阿任 operates the machine, not becomes it. Do not give 阿任 a blank/deadpan face — always show subtle smile or focused calm. It should be clear but not instructional, interesting but not childish, strange but clean.
```

## Multi-image input（强烈推荐）

> **为什么需要**：MCP `matrix_generate_image` 接收 prompt 时是**一次性、瞬时性**的——没有"持续学习"机制。**单纯文字描述**会让模型关联到通用动漫 IP（银魂新八、路人甲），**IP 跑偏 50-70%**。
>
> **解决办法**：用 `input_files` 传 2-3 张 character-refs 作**视觉锚**——让 MCP 模型**看到**阿任长啥样，再结合 prompt 文字生成。
>
> **实测效果**（2026-07-12 验证）：IP 还原度从 ~30% 提升到 ~65%。

**推荐选 3 张**：
- `assets/character-refs/01-base-front.png`（基线正面，OS 短款黑夹克标准站姿）
- `assets/character-refs/04-walking.png`（动态，验证下身走姿）
- `assets/character-refs/12-jacket-simple.png`（OS 简单夹克 + 微笑基线，覆盖外套变体）

> ⚠️ **不要传 11-trench-coat.png**（长款风衣不是阿任默认款，会污染生成）。校准图（13-aren-curved-path.png 等）也**不要传**——校准图带"豆包AI生成"水印 + 风格不同，污染 MCP 视觉锚。

**调用格式**（PowerShell + `mavis mcp call`）：

```powershell
$body = @{
    requests = @(
        @{
            prompt       = $prompt
            input_files  = @(
                "D:\path\to\aren-illustrations\assets\character-refs\01-base-front.png"
                "D:\path\to\aren-illustrations\assets\character-refs\06-coffee.png"
                "D:\path\to\aren-illustrations\assets\character-refs\11-trench-coat.png"
            )
            aspect_ratio = "16:9"
        }
    )
} | ConvertTo-Json -Depth 5 -Compress

$jsonFile = "D:\path\to\_mcp-req.json"
[System.IO.File]::WriteAllText($jsonFile, $body, [System.Text.UTF8Encoding]::new($false))
mavis mcp call matrix matrix_generate_image --file $jsonFile
```

**注意**：
- `input_files` 是 MCP 本地路径或 URL 数组——MCP 会自动上传到 CDN
- 最多 3 张为佳（再多会稀释权重，AI 抓不到重点）
- 选图原则：覆盖**正/动态/服装变体**三个角度
- **不要传校准图**（校准图带"豆包AI生成"水印 + 风格与目标不同——会污染生成）

## 图像编辑提示

去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

增强怪诞感：

```text
Regenerate this illustration with the same core meaning and simple layout, but make 阿任 more central to the conceptual action. 阿任 should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, in Shinkai-style colored-pencil sketch, and not cute. Preserve 阿任's round glasses, soft orange-pink cheek blush, black leather jacket, and warm closed-mouth smile. Do not give 阿任 a blank/deadpan face.
```

## 已知限制（MCP 天花板）

- **纯 text-to-image 无 input_files**：IP 还原度 ~30%（已知）
- **multi-image input 3 张**：IP 还原度 ~65%（实测）
- **更强方案**：训 LoRA 用 SDXL——可提升到 95%+（待用户决定是否投入）

实际效果以 MCP 模型版本为准——遇到严重跑偏时**重新生成**或**调整 input_files 选图**。
