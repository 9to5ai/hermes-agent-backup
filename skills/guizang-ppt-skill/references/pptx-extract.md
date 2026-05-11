# 从 PPTX 提取内容

用 `python-pptx` 将 `.pptx` 文件的文字内容提取为纯文本，供生成参考。

## 快速命令

```bash
# 检查依赖
python3 -c "from pptx import Presentation; print('ok')" 2>/dev/null || pip install python-pptx

# 提取（将输出保存到 .md 文件）
python3 << 'PYEOF'
from pptx import Presentation
import sys
prs = Presentation(sys.argv[1])
for i, slide in enumerate(prs.slides):
    print(f"--- SLIDE {i+1} ---")
    for shape in slide.shapes:
        if hasattr(shape, 'text') and shape.text.strip():
            print(shape.text[:300])
    print()
PYEOF /path/to/deck.pptx > deck_text.md
```

## 注意事项

- **总是用最新版**：PPTX 文件常有多个版本（如 `v2.pptx`, `v6_title_options_expanded.pptx`），选版本号最高、文件名最长的那个。
- `shape.text[:300]` 截断超长文本，防止某张幻灯片有超多文字时刷屏。
- 此提取仅含文字，不含图片、颜色、动画 — 这些由 skill 模板重新设计。
- 输出 `.md` 文件仅作为**参考草稿**，不是最终幻灯片内容。
