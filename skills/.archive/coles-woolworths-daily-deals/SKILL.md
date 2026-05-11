---
name: coles-woolworths-daily-deals
description: Daily Coles + Woolworths discount monitoring — scrapes official sites, filters ≥30% off, outputs Chinese report to Telegram
category: productivity
---

# Coles + Woolworths Daily Discount Monitor

## Trigger
Daily cron job at 6:00 AM Australia/Sydney via `scheduler_add_interval`.

## Sources
- https://www.coles.com.au
- https://www.woolworths.com.au
- Default region: Sydney NSW

## Filter Rules
- **Minimum discount: 30% off** (NOT 20%)
- No speculative prices — exclude if unconfirmed
- No multi-buy tricks — calculate unit price
- Prefer practical family essentials over impulse items
- Avoid daily repetition unless: better price, ending soon, still outstanding, or essentials (母婴/厕纸/清洁用品/日常食材)

## Priority Order
1. 母婴用品 (尿片、湿巾、婴儿用品)
2. 家庭日用品 (厕纸、纸巾、洗衣液、清洁剂、洗碗用品)
3. 粮油米面 (米、面、意粉、酱料、罐头、食用油)
4. 肉/海鲜/鸡蛋/牛奶/芝士/乳制品
5. 水果蔬菜
6. 冷冻食品
7. 个人护理/药房商品 (洗发水、牙膏、沐浴露、维他命)
8. 零食饮品 — only if genuinely good deal

## Emoji Tags
- 🔥 值得囤货
- 🍼 母婴/家庭实用
- 🧻 家庭日用品
- 🥩 优质蛋白
- 🍎 新鲜食品
- 🧊 冷冻食品
- ⚠️ 只适合本来就会买的人

## Output Format (Chinese, concise, mobile-friendly)

```
早晨好！这是今天 Coles + Woolworths 值得看的折扣，筛选标准：至少 30% off。

## 今日最值得买

### 1. [商品名] — [Coles / Woolworths]
- 折扣：[例如 50% off]
- 价格：[$当前价格]，原价：[$原价]
- 单价：[例如 $/100g、$/L、$/each]
- 标签：[例如 🔥 值得囤货 / 🍼 母婴实用]
- 为什么值得买：[一句话]
- 链接：[商品直接链接]

## 值得囤货
- [商品] — [商店] — [% off] — [$价格] — [一句话理由]

## 可以看看，但不是必买
- [商品] — [商店] — [% off] — [$价格] — [适合什么情况]

## 今天整体判断
2-4句话总结：哪个超市更值得、是否有明显囤货机会、母婴/日用品情况，或直接说"今天没有特别值得为了折扣下单的商品"。
```

## Notes
- Only list if discount ≥30% and genuinely useful
- Must be currently valid and available online or in-store
- Check Flybuys / Everyday Rewards / online-only / member conditions — must note clearly
- Limit to top 10-20 items if too many qualify
- Job ID: ab87beb60f95
