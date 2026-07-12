# 阿任形象参考库

> **主文档**：[`assets/examples/README.md`](../examples/README.md) 第 2 节。这里只是本目录的精简索引。

## 12 张 · 角度 × 动作 × 场景

### ✅ 正面参考（推荐作 input_files）

| # | 文件名 | 角度 | 表情 | 动作 / 场景 | 用途 |
|---|---|---|---|---|---|
| 01 | `01-base-front.png` | 正面 | 微笑 | 双手插兜立绘 | **基线（强烈推荐）** |
| 04 | `04-walking.png` | 正面 | 微笑 | 走姿 | 动态下身（推荐） |
| 12 | `12-jacket-simple.png` | 正面 | 微笑 | 简单夹克 | OS 短款基线（强烈推荐） |

> **这 3 张是 input_files 的核心组合**——覆盖基线 / 动态 / 服装变体三个角度。

### ⚠️ 完整场景参考（**不建议作 input_files**）

| # | 文件名 | 角度 | 表情 | 动作 / 场景 | 不建议的原因 |
|---|---|---|---|---|---|
| 05 | `05-reading.png` | 正面 | 专注 | 坐书桌前看书 + 台灯 | 背景太复杂（书桌+台灯+笔记本+笔），会污染 MCP 风格判断 |
| 06 | `06-coffee.png` | 正面 | 微笑 | 持咖啡杯 | 咖啡杯会被 MCP 复制到生成图（v2 测试已验证） |

> 这 2 张**作为"完整场景"参考很有价值**——让 AI 知道阿任可以在复杂场景里。但**不要传给 MCP** 作 input_files。

### 🪞 侧面 / 背面参考（**不可作 input_files**）

| # | 文件名 | 角度 | 用途 / 备注 |
|---|---|---|---|
| 02 | `02-side-static.png` | 左侧 | 侧面立绘——5 元素只可见部分（1 只眼镜） |
| 03 | `03-back.png` | 背面 | **仅供后脑勺发型参考**——看不到脸/眼镜/夹克 |
| 07 | `07-side-calm.png` | 左侧 | 侧面立绘（不同发型细节） |
| 09 | `09-hoodie-pocket.png` | 正面 | hoodie 拉起——**OS 夹克的变体**，不是默认款 |

> 侧面 / 背面图作为 AI 的"形象完整性"参考有用（让 AI 知道侧面/背面长啥样），但**不能作 input_files**——AI 看不到完整 5 元素。

### ❌ 反面参考（**绝对不要作 input_files**）

| # | 文件名 | 角度 | 表情 | 为什么是反面 |
|---|---|---|---|---|
| 08 | `08-side-serious.png` | 左侧 | 严肃 | 严肃无表情——IP 表情下界 |
| 10 | `10-side-furrowed.png` | 左侧 | 皱眉 | 皱眉——IP 表情下界 |
| 11 | `11-trench-coat.png` | 正面 | 微笑 | **长款风衣不是阿任默认款**——会污染 MCP |

> 11 之前标"服装变体"——**实际上是反面参考**（和阿任 OS 短款不符）。误传给 MCP 会让 AI 学到"长款是常态"。

## 表情硬约束

- ✅ 微笑 / 平静专注 / 轻严肃有神
- ❌ 皱眉 / 严肃无表情（08 / 10 反面）
- ❌ 大笑 / 卖萌 / 惊讶 / 哭泣 / 呆滞（已写入 `references/qa-checklist.md`）

## Multi-image input（`input_files`）用图指引

> **核心问题**：MCP image generation 接收 prompt 时是"一次性、瞬时性"的——单纯文字描述会关联到通用动漫 IP，IP 跑偏 50-70%。
>
> **解决办法**：用 `input_files` 传 2-3 张 character-refs 作**视觉锚**——让 MCP 模型"看到"阿任长啥样。
>
> **实测效果**（2026-07-12 验证）：IP 还原度从 ~30% 提升到 ~75%。

### 推荐 3 张（覆盖正 / 动态 / 服装变体）

- `01-base-front.png`（基线正面，OS 短款黑夹克标准站姿）
- `04-walking.png`（动态，验证下身走姿）
- `12-jacket-simple.png`（OS 简单夹克 + 微笑基线）

### 严格不要传

- ❌ **校准图**（13-aren-curved-path.png 等）——带"豆包AI生成"水印 + 风格不同
- ❌ **11-trench-coat.png**（长款风衣不是阿任默认款）
- ❌ **08/10 严肃脸**（反面参考）
- ❌ **03-back.png**（背面看不到任何 IP 元素）
- ❌ **05-reading.png / 06-coffee.png**（背景/道具干扰）
- ❌ **02/07 侧面**（5 元素只可见部分）

### 为什么 ≤ 3 张？

3 张以上会**稀释权重**——MCP 模型尝试学习所有 input 的共同特征，反而抓不到重点。**3 张**足够覆盖"基线 / 动态 / 服装变体"三个维度。

## 已知 IP 偏差（character-refs 本身）

> ⚠️ character-refs 自身的**发型偏"软尖"**——不是"真正蓬松带体积"。MCP 学到这特征后，生成图也偏尖。
>
> **修复路径**：
> - 短期：在 prompt 里强调 "FLUFFY with MAX VOLUME, tousled like after running"——让 MCP 往"更蓬松"走
> - 长期：让用户重画 12 张"真正蓬松"的 character-refs——根本解决
> - 终极：训 LoRA——25 张图训 SDXL LoRA，IP 一致性 95%+

## 调用格式（PowerShell）

```powershell
$body = @{
    requests = @(
        @{
            prompt       = $prompt
            input_files  = @(
                "D:\path\to\aren-illustrations\assets\character-refs\01-base-front.png"
                "D:\path\to\aren-illustrations\assets\character-refs\04-walking.png"
                "D:\path\to\aren-illustrations\assets\character-refs\12-jacket-simple.png"
            )
            aspect_ratio = "16:9"
        }
    )
} | ConvertTo-Json -Depth 5 -Compress

$jsonFile = "D:\path\to\_mcp-req.json"
[System.IO.File]::WriteAllText($jsonFile, $body, [System.Text.UTF8Encoding]::new($false))
mavis mcp call matrix matrix_generate_image --file $jsonFile
```

> 全部图片由豆包 AI 生成，保留原图水印"豆包AI生成"作为来源标识。
