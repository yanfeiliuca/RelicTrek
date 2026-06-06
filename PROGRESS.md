# RelicTrek — Work Log

## 2026-06-06 — BMW 首页重排 + COE33 14-18 修订版上线

### BMW 首页重排 — Commit `597abd6`
- 按游戏内获取/推进顺序重排 BMW 中英文首页 30 张圣物卡片
- EN/ZH 保持同样顺序
- 仅修改 `en/games/bmw/index.html` 与 `zh/games/bmw/index.html`
- 30 篇 BMW 攻略正文未改动
- 已推送到 GitHub `main`

### COE33 Guides 14-18 修订版上线 — Commit `c6889d7`
| # | Slug | EN 主题 | ZH 主题 |
|---|------|---------|---------|
| 14 | `esquie-all-abilities` | Esquie ability unlock route | 埃斯奇全能力解锁路线 |
| 15 | `manor-complete-route` | The Manor complete route | 庄园完整探索路线 |
| 16 | `all-side-quests` | All side quests checklist | 全支线任务清单 |
| 17 | `character-specific-weapons` | Character-specific weapons | 角色专属武器路线 |
| 18 | `thank-you-update` | Thank You Update content | 感谢更新内容路线 |

### 配套更新与验证
- 新增 10 个 COE33 页面：5 EN + 5 ZH
- `en/games/coe33/index.html` 与 `zh/games/coe33/index.html`：13 → 18 Relics
- `en/games/index.html` 与 `zh/games/index.html`：COE33 计数 13 → 18
- `sitemap.xml` 重新生成，当前为 365 个 URL
- 第17篇从原 `clea-boss` 改为 `character-specific-weapons`，避免与现有 `flying-manor-clea` 语义重复
- `thank-you-update` 聚焦 Root of All Evil、Enhanced Endless Tower、新 Gestral Merchant；Verso's Drafts 继续指向现有独立页
- 移动端检查发现中文详情页长标题横向裁切，已通过短 H1 + 响应式 overflow guard 修复
- 推送后确认 `origin/main` 位于 `c6889d7`

### Agent 交接文档
- 新增根目录 `CODEX_README.md`
- 同步更新根目录 `PROGRESS.md` 与仓库内 `PROGRESS.md`

---

## 2026-06-05 — BMW 专区补全至 30 件攻略（第3批：物品21-30）

### BMW 攻略创建（第3批，补全至30件）
| 批次 | 物品编号 | 创建文件数 |
|------|----------|-----------|
| 第1批 | 1-10 | 先前完成 |
| 第2批 | 11-20 | 先前完成 |
| 第3批 | 21-30 | 本会话 — 10 EN + 10 ZH |

**总计：30 篇攻略 × 2 语言 = 60 篇 BMW guides + 2 个 index = 62 个 BMW 专区文件**

### 本会话创建的 10 篇新攻略 — Commit `4033bd6`

| # | Slug | EN 标题 | ZH 标题 |
|---|------|---------|---------|
| 21 | `hundred-eye-boss-route` | Hundred-Eye Demon Lord Route | 百目魔君任务链→第三破天角 |
| 22 | `plantain-fan` | Plantain Fan | 铁扇公主·芭蕉扇法宝 |
| 23 | `matianba-transformation-route` | Ma Tianba Transformation Chain | 马天霸变身任务链 |
| 24 | `great-sage-armor-set` | Great Sage Armor Set | 齐天大圣套装 |
| 25 | `all-transformations-route` | All 10 Transformations Route | 全10种变身法术路线 |
| 26 | `best-spirits-route` | Best Spirits Route | 全精魄高价值选取路线 |
| 27 | `missable-guide` | Permanently Missable Guide | 章节不归路与永久错过清单 |
| 28 | `ng-plus-route` | NG+ Complete Route | 二周目完整武装路线 |
| 29 | `bodhi-seed-system` | Bodhi Patriarch Seed System | 须菩提植物种子系统完整路线 |
| 30 | `chapter6-hidden-areas` | Chapter 6 Hidden Exploration Route | 第六章隐藏区域完整探索路线 |

### 配套更新
- **EN index** (`en/games/bmw/index.html`): 20 → 30 Relics Mapped，新增 10 张 relic card
- **ZH index** (`zh/games/bmw/index.html`): 已收录 20 → 30 件圣物，新增 10 张 relic card
- **Sitemap**: 新增 20 个 URL（EN+ZH 各 10 个）。Rebase 时与远程 auto-sitemap 冲突，已手动解决
- **现有文件**: 前 20 篇攻略均未被修改

### BMW 专区最终验证
- ✅ 10/10 新 slugs 在 EN 和 ZH 均完整存在
- ✅ EN BMW 文件数：31（30 guides + 1 index）
- ✅ ZH BMW 文件数：31（30 guides + 1 index）
- ✅ 所有 HTML 文件自包含（inline CSS/JS，仅外部依赖 Google Fonts + GA + AdSense）
- ✅ 所有页面包含 6 节结构、侧边栏、面包屑、canonical + hreflang 标签
- ✅ Sitemap 包含全部 20 个新 URL

### BMW 专区文件清单（30 篇完整）
```
en/games/bmw/ (31 files: 30 guides + index)
├── all-transformations-route.html  [NEW]
├── best-spirits-route.html         [NEW]
├── bishui-cave.html
├── bodhi-seed-system.html          [NEW]
├── celestial-pills.html
├── chapter6-hidden-areas.html      [NEW]
├── dark-thunder-transformation.html
├── fireproof-mantle.html
├── five-skandhas-pill.html
├── great-sage-armor-set.html       [NEW]
├── hundred-eye-boss-route.html     [NEW]
├── index.html                      [UPDATED]
├── loong-scales-chain.html
├── man-in-stone.html
├── matianba-transformation-route.html [NEW]
├── mind-core-medicine.html
├── missable-guide.html             [NEW]
├── ng-plus-route.html              [NEW]
├── plantain-fan.html               [NEW]
├── prisoner-questline.html
├── purple-talismans.html
├── sky-piercing-horn.html
├── snow-fox-questline.html
├── stormflash-loong-staff.html
├── supreme-gourd.html
├── triple-tipped-spear.html
├── turtle-island-guide.html
├── weavers-needle.html
├── wind-tamer-vessel.html
├── wukong-armor-jingubang.html
└── zodiac-village.html

zh/games/bmw/ (31 files: 30 guides + index)
└── (same filenames as above)
```

### 跨专区统计
**当前总计：7 款游戏 / 161 篇攻略**

| 游戏专区 | 攻略数 | 状态 |
|----------|--------|------|
| Black Myth: Wukong (BMW) | 30 | ✅ 完成 |
| Baldur's Gate 3 (BG3) | 30 | ✅ 完成 |
| Elden Ring (ER) | 30 | ✅ 完成 |
| The Witcher 3 (TW3) | 30 | ✅ 完成 |
| Clair Obscur: Expedition 33 (COE33) | 18 | 🚧 进行中 |
| Monster Hunter Wilds (MHWilds) | 11 | 🚧 进行中 |
| Windrose | 12 | 🚧 进行中 |

---
## 2026-06-04 — BG3 专区全部 30 件攻略完成 + 全面审计

### BG3 攻略创建（全部 5 组）
| 组别 | 物品编号 | 创建批次 | 文件数 |
|------|----------|----------|--------|
| 组1 | 1-6 | 先前完成 | 6 EN + 6 ZH |
| 组2 | 7-12 | 先前完成 | 6 EN + 6 ZH |
| 组3 | 13-18 | 本会话 | 6 EN + 6 ZH |
| 组4 | 19-24 | 本会话 | 6 EN + 6 ZH |
| 组5 | 25-30 | 本会话 | 6 EN + 6 ZH |

**总计：30 篇攻略 × 2 语言 = 60 篇 guides + 2 个 index = 62 个 BG3 专区文件**

### 本会话创建的批次

#### 组5（25-30）— Commit `57ca5d2`
- Moonlantern Route / 月亮灯笼路线
- Gale Orb Resolution / 伽尔任务链终局
- Wyll Pact Resolution / 威尔任务链+解除契约
- Phalar Aluve / 法拉阿鲁维
- Auntie Ethel Hair / 埃塞尔奶奶的头发
- Devotee Mace / 神圣干预权杖
- Index 更新：6→12

#### 组3（13-18）— Commit `85b8a4e`
- Nightsong Rescue / 夜歌救援
- Astarion Vampire Ascension / 阿斯塔里昂至尊吸血鬼
- Potent Robe / 强效长袍
- STR 23 + CON 23 Gear / 力量23+耐力23装备
- Gauntlets of the Warmaster / 战争大师手套
- Arcane Tower / 地下城秘法塔
- Index 更新：12→18

#### 组4（19-24）— Commit `3986f4c`
- Gontr Mael / 贡特尔麻雀弩
- Viconia Walking Fortress / 维科尼娅行走要塞
- Sussur Weapon / 苏瑟武器
- Last Light Inn Complete / 最后曙光旅馆全收集
- Titanstring Bow / 泰坦弦长弓
- Dark Urge Origin Route / 黑暗冲动专属路线
- Index 更新：18→24

#### 全面审计修复 — Commit `66d7e39`
- 修复：组2的6张卡片从未加入index（Band of Mystic Scoundrel、Helldusk Armor、Karlach Engine、Karsus Vault、Nyrulna、Orin Paired Daggers）
- 修复：两个index的Dark Urge卡片缺少闭合标签
- 修复：Meta description从"6件"更新为"30件"
- 验证：全部canonical URL、hreflang、交叉引用、面包屑正确
- Index更新：24→30 Relics Mapped
- Sitemap：333 URLs

### BG3 专区最终文件清单
```
en/games/bg3/ (31 files: 30 guides + index)
├── adamantine-forge.html
├── arcane-tower.html
├── astarion-vampire.html
├── balduran-giantslayer.html
├── band-of-mystic-scoundrel.html
├── blood-of-lathander.html
├── dark-urge-route.html
├── devotees-mace.html
├── ethel-hair.html
├── gale-orb-resolution.html
├── gauntlets-warmaster.html
├── gontr-mael.html
├── helldusk-armor.html
├── house-of-hope.html
├── index.html
├── karlach-engine.html
├── karsus-vault.html
├── last-light-inn.html
├── moonlantern-route.html
├── nightsong-rescue.html
├── nyrulna.html
├── orin-paired-daggers.html
├── orphic-hammer.html
├── phalar-aluve.html
├── potent-robe.html
├── selunes-spear.html
├── strength-constitution-gear.html
├── sussur-weapon.html
├── titanstring-bow.html
├── viconia-walking-fortress.html
└── wyll-pact-resolution.html

zh/games/bg3/ (31 files: 30 guides + index)
└── (same filenames as above)
```

### 审计结果摘要
- ✅ 30/30 EN+ZH 文件名完全匹配
- ✅ 所有 canonical URL 正确
- ✅ 所有 hreflang 交替链接正确
- ✅ 所有跨页面交叉引用（如 house-of-hope → orphic-hammer）有效
- ✅ 所有面包屑导航正确
- ✅ Index 显示 30 Relics Mapped（EN）/ 已收录 30 件圣物（ZH）
- ✅ Sitemap 覆盖 333 个 HTML 文件
- ⚠️ 无 PROGRESS.md（本文件为首次创建）

