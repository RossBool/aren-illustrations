# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist black pencil line art with Shinkai-style colored-pencil coloring on skin and objects. Slight wobbly hand-drawn pen lines. Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI, no 3D render, no anime style exaggeration.

Recurring IP character required:
阿任, a teen-age boy drawn in Shinkai-style colored-pencil sketch: round oval face with soft chin, fluffy short-to-medium black hair (length between ear and shoulder, colored-pencil texture, not solid black), round black-framed glasses with slight lens reflection, soft white skin with colored-pencil texture (not flat fill), prominent orange-pink blush on both cheeks (this blush color is IP-exclusive, do not reuse for other elements), a slight warm closed-mouth smile (never blank/deadpan/expressionless — always either soft smile or focused calm), white T-shirt under an oversized black leather jacket (long sleeves covering hands, with slight shine/texture, visible collar fold), solid black track pants (simple, no decorative stripes), black-white sneakers, Q-version body proportion (head-to-body ratio around 1:2.5 to 1:3). Always wears the round glasses. 阿任 must perform the core conceptual action, not decorate the scene. 阿任 is calm, studious, slightly whimsical, and bookish, not cute or kawaii, not a mascot. Do not give 阿任 a big smile, an open mouth, surprise, or any exaggerated expression. Keep the face serene and the action focused.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：阿任在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use (strict 5-color rule):
- Black: main line art, 阿任's hair/jacket/pants/shoes/glasses frame, all text and frame lines.
- Orange-pink: ONLY for 阿任's cheek blush. Do not use this color for any annotation or object.
- Red: only for key warning/problem/result annotations.
- Orange: only for main flow/path/arrows.
- Blue: only for secondary notes or feedback/system state.
- Subtle warm tones: allowed for 阿任's skin and a few objects (coffee cup, desk) but the background must stay clean white.
- Maximum 3 annotation colors per image (chosen from red/orange/blue).

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. 阿任 is a real person figure, not a mascot or a piece of machinery — do not stuff 阿任 inside a funnel or a black box; 阿任 operates the machine, not becomes it. Do not give 阿任 a blank/deadpan face — always show subtle smile or focused calm. It should be clear but not instructional, interesting but not childish, strange but clean.
```

## 图像编辑提示

去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

增强怪诞感：

```text
Regenerate this illustration with the same core meaning and simple layout, but make 阿任 more central to the conceptual action. 阿任 should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, in Shinkai-style colored-pencil sketch, and not cute. Preserve 阿任's round glasses, soft orange-pink cheek blush, black leather jacket, and warm closed-mouth smile. Do not give 阿任 a blank/deadpan face.
```
