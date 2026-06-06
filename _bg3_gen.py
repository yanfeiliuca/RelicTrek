#!/usr/bin/env python3
"""Generate BG3 Group 2 files: guides 7-12 (EN+ZH)."""
import os

BASE = r"C:\Users\yanfe\OneDrive\Desktop\RelicTrek\GitHub\RelicTrek"

# Read CSS from existing Group 1 file
en_sample = open(BASE + r'\en\games\bg3\house-of-hope.html', 'r', encoding='utf-8').read()
css_start = en_sample.find(':root{')
css_end = en_sample.find('</style>') + 8
EN_CSS = en_sample[css_start:css_end]

# ZH variant
ZH_CSS = EN_CSS.replace("--font-heading:'Cinzel',Georgia,serif", "--font-heading:'Cinzel','Noto Sans SC',Georgia,serif").replace("--font-body:'Inter',-apple-system,sans-serif", "--font-body:'Inter','Noto Sans SC',-apple-system,sans-serif").replace("line-height:1.7","line-height:1.8").replace("text-transform:uppercase;letter-spacing:.04em}.tag","letter-spacing:.04em}.tag")

EN_FONTS = "Cinzel:wght@400;600;700;900&family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700"
ZH_FONTS = EN_FONTS + "&family=Noto+Sans+SC:wght@300;400;500;700"
EN_NAV = '<nav><a href="/en/" class="logo"><span>🧭</span>RelicTrek</a><ul class="nav-links"><li><a href="/en/games/">Games</a></li><li><a href="/en/games/windrose/">Guides</a></li><li><a href="/en/blog/">Blog</a></li><li><a href="/en/about.html">About</a></li></ul>'
ZH_NAV = '<nav><a href="/zh/" class="logo"><span>🧭</span>RelicTrek 圣物寻踪</a><ul class="nav-links"><li><a href="/zh/games/">游戏</a></li><li><a href="/zh/games/windrose/">攻略</a></li><li><a href="/zh/blog/">博客</a></li><li><a href="/zh/about.html">关于</a></li></ul>'
EN_FOOTER = '<footer><div class="footer-grid"><div><h4>RelicTrek</h4><p style="color:var(--text-dim)">Every relic has a trail. We map the trek.</p></div><div><h4>Games</h4><ul><li><a href="/en/games/windrose/">Windrose</a></li><li><a href="/en/games/mhwilds/">Monster Hunter Wilds</a></li><li><a href="/en/games/tw3/">The Witcher 3</a></li></ul></div><div><h4>Company</h4><ul><li><a href="/en/about.html">About Us</a></li><li><a href="/en/contact.html">Contact</a></li><li><a href="/en/blog/">Blog</a></li></ul></div><div><h4>Legal</h4><ul><li><a href="/en/privacy.html">Privacy Policy</a></li><li><a href="/en/terms.html">Terms of Service</a></li></ul></div></div><div class="footer-bottom"><p>© 2026 RelicTrek. This is a fan site and is not affiliated with Larian Studios or any game developer or publisher.</p></div></footer>'
ZH_FOOTER = '<footer><div class="footer-grid"><div><h4>RelicTrek 圣物寻踪</h4><p style="color:var(--text-dim)">每一件圣物都有迹可循。我们绘制寻宝之路。</p></div><div><h4>游戏</h4><ul><li><a href="/zh/games/windrose/">Windrose</a></li><li><a href="/zh/games/mhwilds/">怪物猎人：荒野</a></li><li><a href="/zh/games/tw3/">猎魔人3</a></li></ul></div><div><h4>关于</h4><ul><li><a href="/zh/about.html">关于我们</a></li><li><a href="/zh/contact.html">联系方式</a></li><li><a href="/zh/blog/">博客</a></li></ul></div><div><h4>法律</h4><ul><li><a href="/zh/privacy.html">隐私政策</a></li><li><a href="/zh/terms.html">服务条款</a></li></ul></div></div><div class="footer-bottom"><p>© 2026 RelicTrek。本站为粉丝站点，与 Larian Studios 或任何游戏开发商/发行商无关。</p></div></footer>'

def create(name, content):
    path = os.path.join(BASE, name.replace('/', '\\'))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def build_page(lang, slug, title, desc, kw, tags, h1, meta, stats, content, sidebar_items, related_links=""):
    canon = f"https://relictrek.com/{lang}/games/bg3/{slug}.html"
    zhlang = "zh" if lang == "en" else "en"
    zhurl = canon.replace(f"/{lang}/", f"/{zhlang}/")
    selfurl = canon
    if lang == "en":
        fonts,css,nav,footer = EN_FONTS,EN_CSS,EN_NAV,EN_FOOTER
        lang_nav = f'<div class="nav-right"><div class="lang-switch"><a href="{selfurl}" class="active">EN</a><a href="{zhurl}">中文</a></div></div></nav>'
        bc = f'<a href="/en/">Home</a> &rsaquo; <a href="/en/games/">Games</a> &rsaquo; <a href="/en/games/bg3/">Baldur\'s Gate 3</a> &rsaquo; <span>{slug.replace("-"," ").title()}</span>'
        og_title = title.split("|")[0].strip()
        sidebar_title = "On This Page"; sidebar_home = '<li><a href="/en/games/bg3/">← Baldur\'s Gate 3 home</a></li>'
        sidebar_root = '<li><a href="/en/">← RelicTrek Home</a></li>'
    else:
        fonts,css,nav,footer = ZH_FONTS,ZH_CSS,ZH_NAV,ZH_FOOTER
        lang_nav = f'<div class="nav-right"><div class="lang-switch"><a href="{zhurl}">EN</a><a href="{selfurl}" class="active">中文</a></div></div></nav>'
        bc = f'<a href="/zh/">首页</a> &rsaquo; <a href="/zh/games/">游戏</a> &rsaquo; <a href="/zh/games/bg3/">博德之门3</a> &rsaquo; <span>{slug.replace("-"," ").title()}</span>'
        og_title = (title.split("|")[0].strip() + " | RelicTrek 圣物寻踪")[:120]
        sidebar_title = "本页导航"; sidebar_home = '<li><a href="/zh/games/bg3/">← 博德之门3首页</a></li>'
        sidebar_root = '<li><a href="/zh/">← RelicTrek 首页</a></li>'
    stats_html = "".join([f'<div class="stat-card"><div class="stat-value">{s[0]}</div><div class="stat-label">{s[1]}</div></div>' for s in stats])
    tags_html = "".join([f'<span class="tag tag-{"endgame" if "miss" in t.lower() or "⚠" in t else "armor"}">{t}</span>' for t in tags])
    sb_links = "".join([f'<li><a href="#{s[0]}">{s[1]}</a></li>' for s in sidebar_items])
    sb_rel = related_links if related_links else ""
    html = f'<!DOCTYPE html>\n<html lang="{"en" if lang == "en" else "zh-CN"}">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{title}</title>\n<meta name="description" content="{desc}">\n<meta name="keywords" content="{kw}">\n<link rel="canonical" href="{canon}">\n<link rel="alternate" hreflang="{"en" if lang == "en" else "zh"}" href="{canon}">\n<link rel="alternate" hreflang="{"zh" if lang == "en" else "en"}" href="{zhurl}">\n<link rel="alternate" hreflang="x-default" href="https://relictrek.com/en/games/bg3/{slug}.html">\n<meta property="og:title" content="{og_title}"><meta property="og:description" content="{desc[:150]}">\n<meta property="og:type" content="article"><meta property="og:url" content="{canon}">\n<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family={fonts}&display=swap" rel="stylesheet">\n<script async src="https://www.googletagmanager.com/gtag/js?id=G-5VH076R049"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","G-5VH076R049");</script>\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1971262808837870" crossorigin="anonymous"></script>\n<style>{css}</style>\n</head>\n<body>\n{nav}{lang_nav}\n<div class="page-header"><div class="breadcrumb">{bc}</div><div class="article-header"><div class="tags">{tags_html}</div><h1>{h1}</h1><div class="article-meta">{meta}</div></div><div class="quick-stats">{stats_html}</div></div>\n<div class="main-layout"><div class="main-content">\n{content}\n</div>\n<aside class="sidebar"><div class="sidebar-card"><h4>{sidebar_title}</h4><ul>{sb_links}</ul></div><div class="sidebar-card"><h4>{"Quick Navigation" if lang == "en" else "快捷导航"}</h4><ul>{sidebar_home}{sb_rel}{sidebar_root}</ul></div><div class="ad-placeholder">Google AdSense<br>300×250</div></aside></div>\n{footer}\n</body>\n</html>'
    return html

# ===== GROUP 2 DATA =====
guides = {
    "band-of-mystic-scoundrel": {
        "en": {
            "title": "Band of the Mystic Scoundrel — The Most Powerful Ring in BG3, in a Backpack Next to a Dinosaur | RelicTrek",
            "desc": "After hitting with an attack, cast enchantment/illusion spells as a bonus action. Attack then Hold Monster as bonus = paralyzed enemy + auto-crits. Same jungle as Nyrulna. Most players walk past it.",
            "kw": "BG3 Band of Mystic Scoundrel, Akabi jungle ring, bonus action enchantment spells, best ring BG3, Circus of Last Days, Hold Monster bonus action",
            "tags": ["Ring", "Act 3", "Bonus Action Spells"],
            "h1": "Band of the Mystic Scoundrel — Cast Control Spells as a Bonus Action",
            "meta": '<span>🕐 30 min (with Nyrulna)</span><span>⚔ No boss</span><span>📍 Akabi Jungle</span><span>💍 Bonus Action Spells</span><span>📅 Updated 2026-06-04</span>',
            "stats": [("Bonus Action","Cast Spells"),("~30 min","With Nyrulna"),("No Lockpick","Backpack"),("Act 3","Circus"),("Hidden","Western Jungle")],
            "content": '''<section id="why"><h2>1. Why You Need This</h2><p>Screen Rant called it the most recommended item in all of Baldur's Gate 3. Effect: After hitting a target with an attack, you can cast any enchantment or illusion spell as a <strong>bonus action</strong>. In practice: attack → bonus action Hold Person/Monster → target paralyzed → next round all attacks have advantage and auto-crit. This works for the entire party. Any character who can attack and cast spells benefits. It transforms action economy in every fight it appears in.</p></section>
<section id="location"><h2>2. Location — Same Jungle as <a href="nyrulna.html">Nyrulna</a></h2><p>Access via Akabi at the Circus of the Last Days. Once in the jungle: do NOT go straight to the exit portal. Navigate to the <strong>WESTERN SECTION</strong> first. Find a skeleton near a backpack. Inside: Band of the Mystic Scoundrel. The skeleton is humanoid — a previous unlucky visitor, clearly not a dinosaur.</p></section>
<section id="route"><h2>3. Getting Both Items in One Trip</h2><p>This ring and <a href="nyrulna.html">Nyrulna</a> are in the same jungle instance, accessible in a single trip. Recommended route: enter the jungle → hug northern edge to avoid dinosaurs → go WEST first for the ring (backpack, no lockpick) → then southeast to the exit portal for Nyrulna (chest, DC 20 lockpick). Get both before leaving. Only ONE character gets sent per Akabi interaction.</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #1</div>
<section id="hazard"><h2>4. Hazard Guide</h2><div class="danger-box"><div class="box-label">⚠ Get Both in One Trip</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">The ring and Nyrulna are in the same jungle. You cannot return easily — redo the entire Akabi pickpocket process to come back.</p></div><div class="danger-box"><div class="box-label">⚠ Dinosaurs Can Be Avoided</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Hug the northern jungle edge, jumping between platforms. Zero dinosaur encounters needed.</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #2</div>
<section id="verdict"><h2>5. The Ring That Breaks Action Economy</h2><p>Turn 1: attack → Hold Monster as bonus action → enemy paralyzed. Turn 2: all melee attacks have advantage and auto-crit. Repeat. No other single item in BG3 provides this level of action economy transformation for spellcasting martial characters.</p></section>''',
            "sidebar": [("why","1. Why You Need This"),("location","2. Location"),("route","3. Both Items Route"),("hazard","4. Hazard Guide"),("verdict","5. Action Economy")],
            "related": '<li><a href="/en/games/bg3/nyrulna.html">Nyrulna →</a></li>'
        },
        "zh": {
            "title": "神秘骗徒之戒——全游戏最受推荐的戒指，放在一个骷髅旁边的背包里，紧挨着一群恐龙 | RelicTrek 圣物寻踪",
            "desc": "攻击命中后可将魅惑/幻术系法术作为奖励行动施放。实战：攻击→奖励行动定身怪物→目标瘫痪→下一轮全员自动暴击。与尼鲁纳在同一片丛林。大多数玩家径直走过从未发现。",
            "kw": "博德之门3 神秘骗徒之戒, BG3 阿卡比丛林, 奖励行动施法, 最强戒指, 末日马戏团",
            "tags": ["戒指", "第三幕", "奖励行动"],
            "h1": "神秘骗徒之戒——攻击后奖励行动施放控制法术",
            "meta": '<span>🕐 约30分钟（与尼鲁纳一起）</span><span>⚔ 无Boss</span><span>📍 阿卡比恐龙丛林</span><span>💍 奖励行动施法</span><span>📅 更新 2026-06-04</span>',
            "stats": [("奖励行动","施放法术"),("~30min","与尼鲁纳同行"),("无需开锁","背包"),("第三幕","马戏团"),("隐藏","丛林西侧")],
            "content": '''<section id="why"><h2>一、为什么你需要它</h2><p>Screen Rant 称其为全博德之门3最受推荐的物品。效果：攻击命中后可将任何魅惑系或幻术系法术作为<strong>奖励行动</strong>施放。实战：攻击→奖励行动定身怪物→目标瘫痪→下一轮全员攻击优势和自动暴击。全队任何能攻击和施法的角色都受益。彻底改变每场战斗的行动经济。</p></section>
<section id="location"><h2>二、位置——与<a href="nyrulna.html">尼鲁纳</a>在同一片丛林</h2><p>通过末日马戏团的阿卡比进入。进入丛林后不要直接走向出口传送门。先导航到<strong>西侧区域</strong>。找到一具骷髅旁的背包。背包内：神秘骗徒之戒。骷髅是人形的——某个之前不走运的访客，明显不是恐龙。</p></section>
<section id="route"><h2>三、一次取得两件物品</h2><p>这枚戒指和<a href="nyrulna.html">尼鲁纳</a>在同一片丛林，可以在一次行动中取得。推荐路线：进入丛林→贴北侧边缘跳跃前进绕开恐龙→先去西侧拿戒指（背包，无需开锁）→再去东南出口传送门旁的宝箱拿尼鲁纳（DC 20开锁）。离开前两件都拿到。每次阿卡比互动只能传送一名角色。</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #1</div>
<section id="hazard"><h2>四、避坑指南</h2><div class="danger-box"><div class="box-label">⚠ 一次拿两件</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">戒指和尼鲁纳在同一片丛林。很难返回——需要重做整个阿卡比扒窃流程才能再来。</p></div><div class="danger-box"><div class="box-label">⚠ 可完全避开恐龙</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">贴丛林北侧边缘，在平台间跳跃。完全不需要遭遇恐龙。</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #2</div>
<section id="verdict"><h2>五、打破行动经济的戒指</h2><p>第一回合：攻击→奖励行动定身怪物→敌人瘫痪。第二回合：所有近战攻击优势和自动暴击。重复。BG3中没有任何其他单个物品能为施法型武斗角色提供这种程度的行动经济转换。</p></section>''',
            "sidebar": [("why","一、为什么你需要它"),("location","二、位置"),("route","三、两件同行"),("hazard","四、避坑指南"),("verdict","五、行动经济")],
            "related": '<li><a href="/zh/games/bg3/nyrulna.html">尼鲁纳 →</a></li>'
        }
    },
    "orin-paired-daggers": {
        "en": {
            "title": "Orin Paired Daggers — The Murder Tribunal, Bhaal Temple, and a Two-Dagger Critical Hit System | RelicTrek",
            "desc": "Bloodthirst makes enemies vulnerable to piercing. Crimson Mischief deals bonus critical damage. Together: vulnerability + auto-crit piercing = highest single-turn damage for Rogue/Fighter builds. From Orin the Red in the Temple of Bhaal.",
            "kw": "BG3 Orin daggers, Bloodthirst, Crimson Mischief, Murder Tribunal, Temple of Bhaal, Orin the Red, piercing vulnerability",
            "tags": ["Legendary Weapons", "Act 3", "Boss 4/5"],
            "h1": "Orin Paired Daggers — A Two-Dagger System Built for Critical Hits",
            "meta": '<span>🕐 ~2 hrs</span><span>⚔ Orin 4/5</span><span>📍 Undercity · Bhaal Temple</span><span>🗡 Piercing Vulnerability</span><span>📅 Updated 2026-06-04</span>',
            "stats": [("Piercing Vuln","Bloodthirst"),("+7 Crit Dice","Crimson Mischief"),("~2 hrs","Full Route"),("4/5","Orin Difficulty"),("Act 3","Undercity")],
            "content": '''<section id="why"><h2>1. What You Get</h2><p>Both daggers drop from Orin the Red in the Temple of Bhaal: <strong>Bloodthirst</strong> — target becomes Vulnerable to piercing (double damage), +2 attack/damage, offhand applies Weak Point (no reactions). <strong>Crimson Mischief</strong> — +1 attack/damage vs targets below 50% HP, +7 damage dice on critical hits. Together: Bloodthirst makes enemies vulnerable to piercing → Crimson Mischief crits deal piercing → double piercing damage. One of the highest single-turn damage combinations for Rogue/Fighter.</p></section>
<section id="route"><h2>2. The Route (4 Steps)</h2><p><strong>Step 1:</strong> Act 3 Lower City — investigate Open Hand Temple murders. <strong>Step 2:</strong> Enter Murder Tribunal in Undercity Ruins (sewers). Bhaal worshipper path: present a kill. Non-Bhaal: fight through cultists. <strong>Step 3:</strong> Find Temple of Bhaal entrance past Tribunal. Orin holds a companion hostage. <strong>Step 4:</strong> Defeat Orin — she shapeshifts during combat, has ~200 HP. Key: burst damage on first phase to prevent Slayer transformation escalation. Both daggers on her body.</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #1</div>
<section id="hazard"><h2>3. Hazard Guide</h2><div class="danger-box"><div class="box-label">⚠ Companion Hostage</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Orin takes one party member hostage. They survive the fight but must be rescued after.</p></div><div class="danger-box"><div class="box-label">⚠ Three Layers Deep</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Temple is below Undercity Ruins, below Lower City sewers. Three layers of descent.</p></div><div class="danger-box"><div class="box-label">⚠ Tribunal Keys</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Specific items from the Open Hand Temple investigation allow Tribunal entry without full combat.</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #2</div>
<section id="verdict"><h2>4. Best Rogue/Fighter Combo in the Game</h2><p>The vulnerability-piercing-crit chain makes this the highest burst damage weapon pairing for any dual-wielding build. For Astarion or a dual-wield Tav, this is the definitive endgame weapon loadout.</p></section>''',
            "sidebar": [("why","1. What You Get"),("route","2. The Route"),("hazard","3. Hazard Guide"),("verdict","4. Best Rogue Combo")],
            "related": ""
        },
        "zh": {
            "title": "谋杀法庭→奥林双匕首——三层地下室之下，专为暴击构筑打造的双匕首系统 | RelicTrek 圣物寻踪",
            "desc": "嗜血使目标对穿刺伤害变弱。猩红错误暴击+7伤害骰。组合：穿刺变弱+自动暴击=盗贼/战士最高单回合伤害。从巴尔神殿的红发奥林身上获取。",
            "kw": "博德之门3 奥林双匕首, BG3 嗜血, 猩红错误, 谋杀法庭, 巴尔神殿, 穿刺变弱",
            "tags": ["传奇武器", "第三幕", "Boss 4/5"],
            "h1": "奥林双匕首——专为暴击构筑打造的双匕首系统",
            "meta": '<span>🕐 ~2小时</span><span>⚔ 奥林 4/5</span><span>📍 下城废墟·巴尔神殿</span><span>🗡 穿刺变弱</span><span>📅 更新 2026-06-04</span>',
            "stats": [("穿刺变弱","嗜血"),("+7暴击骰","猩红错误"),("~2h","完整路线"),("4/5","奥林难度"),("第三幕","下城废墟")],
            "content": '''<section id="why"><h2>一、你获得什么</h2><p>两把匕首均从巴尔神殿的红发奥林身上掉落：<strong>嗜血</strong>——命中时目标对穿刺伤害变弱（双倍伤害），+2攻击/伤害，副手命中施加弱点（无法使用反应）。<strong>猩红错误</strong>——对50%血量以下目标+1攻击/伤害，暴击时+7伤害骰。组合：嗜血让敌人穿刺变弱→猩红错误暴击穿刺伤害翻倍→盗贼/战士最高单回合伤害之一。</p></section>
<section id="route"><h2>二、路线（4步）</h2><p><strong>第1步：</strong>第三幕下城——调查开放之手神殿谋杀案。<strong>第2步：</strong>在下城废墟（下水道）进入谋杀法庭。巴尔信徒路线：展示某次击杀。非信徒：杀出一条路。<strong>第3步：</strong>法庭之后找到巴尔神殿入口。奥林劫持了一名同伴。<strong>第4步：</strong>击败奥林——她战斗中变形，约200HP。关键：第一阶段爆发输出防止她升级为Slayer形态。两把匕首均从她遗骸拾取。</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #1</div>
<section id="hazard"><h2>三、避坑指南</h2><div class="danger-box"><div class="box-label">⚠ 同伴人质</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">奥林劫持一名队员。战斗中不会死但之后必须营救。</p></div><div class="danger-box"><div class="box-label">⚠ 三层深度</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">神殿在下城废墟之下，废墟在下水道之下。三层下降。</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #2</div>
<section id="verdict"><h2>四、全游戏最佳盗贼/战士组合</h2><p>变弱-穿刺-暴击链条使这对匕首成为任何双持构筑的最高爆发伤害配对。对阿斯塔里昂或双持主角，这是最理想的终局武器配置。</p></section>''',
            "sidebar": [("why","一、你获得什么"),("route","二、路线"),("hazard","三、避坑指南"),("verdict","四、最佳组合")],
            "related": ""
        }
    },
    "nyrulna": {
        "en": {
            "title": "Nyrulna — Steal a Ring From a Djinn, Win His Rigged Game, Survive a Dinosaur Jungle Alone | RelicTrek",
            "desc": "Legendary trident that returns when thrown, creates thunder explosion on impact, grants permanent +3m movement and fall immunity. Steal Akabi's ring, win his jackpot, navigate the jungle alone. DC 20 lockpick for the chest.",
            "kw": "BG3 Nyrulna, legendary trident, Akabi djinn, Circus of Last Days, thrown weapon returns, thunder explosion",
            "tags": ["Legendary Weapon", "Act 3", "Thrown"],
            "h1": "Nyrulna — The Legendary Returning Trident Hidden in a Dinosaur Jungle",
            "meta": '<span>🕐 ~30 min</span><span>⚔ DC 15 pickpocket + 20 lockpick</span><span>📍 Rivington Circus</span><span>🔱 Returns + Explosion</span><span>📅 Updated 2026-06-04</span>',
            "stats": [("Returns","When Thrown"),("3d4 Thunder","Explosion AoE"),("+3m Move","Permanent"),("Fall Immune","Permanent"),("DC 20","Lockpick")],
            "content": '''<section id="why"><h2>1. What It Does</h2><p>Thrown weapon returns to hand automatically. On throw: 3d4 Thunder explosion in 6m radius (hits enemies AND allies — aim carefully). Permanent +3m movement speed and jump distance. Permanent immunity to falling damage. Best use: Barbarian Throw build — every throw deals melee hit + thunder explosion + returns for next throw.</p></section>
<section id="route"><h2>2. Complete Route (5 Steps)</h2><p><strong>1.</strong> Circus of the Last Days in Rivington. Find Akabi at his Wheel of Wonders. <strong>2.</strong> Pickpocket Akabi (DC 15 Sleight of Hand, Astarion recommended). Take Djinni Ring. <strong>3.</strong> Equip ring. Spin wheel. Win jackpot. Akabi accuses you of cheating and teleports you to a jungle. Only the speaking character is sent. <strong>4.</strong> Navigate jungle: hug NORTHERN edge, jumping between platforms. Before reaching portal — go WEST to get <a href="band-of-mystic-scoundrel.html">Band of the Mystic Scoundrel</a> from the skeleton backpack. <strong>5.</strong> At southeastern exit portal, a DC 20 locked chest. Inside: Nyrulna. Alternative: carry the entire chest through the portal and open it outside.</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #1</div>
<section id="hazard"><h2>3. Hazard Guide</h2><div class="danger-box"><div class="box-label">⚠ One Character Only</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Send a character with high Dex and access to invisibility if possible.</p></div><div class="danger-box"><div class="box-label">⚠ Thunder Friendly Fire</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Nyrulna throws explode in 6m radius. Friendly fire is real — position carefully.</p></div><div class="danger-box"><div class="box-label">⚠ Get the Ring Too</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Band of the Mystic Scoundrel is in the same jungle. Do not leave without it.</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #2</div>
<section id="verdict"><h2>4. Best Thrown Weapon in the Game</h2><p>For Barbarian Throw builds, Nyrulna + Ring of Flinging + Tavern Brawler feat creates the highest sustained ranged DPS in BG3. The thunder AoE and permanent movement buffs make it valuable for any melee character even without a throw-focused build.</p></section>''',
            "sidebar": [("why","1. What It Does"),("route","2. Complete Route"),("hazard","3. Hazard Guide"),("verdict","4. Best Thrown")],
            "related": '<li><a href="/en/games/bg3/band-of-mystic-scoundrel.html">← Band of Mystic Scoundrel</a></li>'
        },
        "zh": {
            "title": "尼鲁纳——从精灵那里偷一枚戒指，赢得他的作弊游戏，独自在恐龙丛林中生存 | RelicTrek 圣物寻踪",
            "desc": "传奇三叉戟：投掷自动返回，命中产生3d4雷电爆炸。永久+3米移动和跳跃距离，永久免疫坠落伤害。扒窃阿卡比的戒指，赢得大奖，独自穿越丛林。宝箱DC 20开锁。",
            "kw": "博德之门3 尼鲁纳, BG3 传奇三叉戟, 阿卡比精灵, 末日马戏团, 投掷武器返回",
            "tags": ["传奇武器", "第三幕", "投掷"],
            "h1": "尼鲁纳——藏在恐龙丛林里的传奇回归三叉戟",
            "meta": '<span>🕐 ~30分钟</span><span>⚔ DC 15扒窃+20开锁</span><span>📍 里文顿马戏团</span><span>🔱 返回+爆炸</span><span>📅 更新 2026-06-04</span>',
            "stats": [("返回","投掷自动"),("3d4雷电","AoE爆炸"),("+3m移动","永久"),("免疫坠落","永久"),("DC 20","开锁")],
            "content": '''<section id="why"><h2>一、武器属性</h2><p>投掷后自动返回手中。投掷时：6米半径3d4雷电爆炸（注意友方伤害）。永久+3米移动速度和跳跃距离。永久免疫坠落伤害。最佳用途：野蛮人投掷构筑——每次投掷造成近战命中+雷电爆炸+自动返回准备下一次投掷。</p></section>
<section id="route"><h2>二、完整路线（5步）</h2><p><strong>1.</strong> 里文顿末日马戏团。找到阿卡比精灵的幸运轮摊位。<strong>2.</strong> 扒窃阿卡比（DC 15手法，推荐阿斯塔里昂）。拿走精灵戒指。<strong>3.</strong> 装备戒指。转动轮盘。赢得头奖。阿卡比指控你作弊，将你传送到恐龙丛林。只有对话角色被传送。<strong>4.</strong> 穿越丛林：贴北侧边缘跳跃前进。到达出口前——先去西侧拿<a href="band-of-mystic-scoundrel.html">神秘骗徒之戒</a>（骷髅背包）。<strong>5.</strong> 东南出口传送门旁的DC 20宝箱内有尼鲁纳。替代方案：抱走整个宝箱穿过传送门再开锁。</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #1</div>
<section id="hazard"><h2>三、避坑指南</h2><div class="danger-box"><div class="box-label">⚠ 仅限一名角色</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">尽量派出高灵巧且有隐身能力的角色。</p></div><div class="danger-box"><div class="box-label">⚠ 雷电友方伤害</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">尼鲁纳投掷爆炸半径6米。友方伤害真实存在——注意站位。</p></div><div class="danger-box"><div class="box-label">⚠ 别忘了戒指</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">神秘骗徒之戒在同一片丛林。不要空手离开。</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #2</div>
<section id="verdict"><h2>四、全游戏最佳投掷武器</h2><p>对野蛮人投掷构筑，尼鲁纳+投掷戒指+酒馆斗殴者专长创造了BG3最高的持续远程DPS。雷电AoE和永久移动增益即使对非投掷构筑的近战角色也极具价值。</p></section>''',
            "sidebar": [("why","一、武器属性"),("route","二、完整路线"),("hazard","三、避坑指南"),("verdict","四、最佳投掷")],
            "related": '<li><a href="/zh/games/bg3/band-of-mystic-scoundrel.html">← 神秘骗徒之戒</a></li>'
        }
    },
    "karsus-vault": {
        "en": {
            "title": "Karsus Vault — Four Locked Doors in a Wizard Tower and Three Legendary Items Behind Them | RelicTrek",
            "desc": "Inside Ramazith Tower: Markoheshkir staff (+1 spell DC, free spell per rest), Annals of Karsus (learn high-level spells), Red Knight's Final Strategem. Navigate 4 sequential doors in the Upper City wizard tower.",
            "kw": "BG3 Karsus Vault, Markoheshkir staff, Ramazith Tower, Annals of Karsus, Red Knight Strategem, legendary spell books",
            "tags": ["Legendary Items", "Act 3", "Wizard Tower"],
            "h1": "Karsus Vault — Three Legendary Items Behind Four Locked Doors",
            "meta": '<span>🕐 ~1.5 hrs</span><span>⚔ No boss (puzzle locks)</span><span>📍 Upper City Ramazith Tower</span><span>📚 Staff + 2 Tomes</span><span>📅 Updated 2026-06-04</span>',
            "stats": [("+1 Spell DC","Markoheshkir"),("Free Spell","Per Long Rest"),("~1.5 hrs","Puzzle Route"),("No Boss","Puzzle Only"),("Act 3","Upper City")],
            "content": '''<section id="why"><h2>1. What You Get</h2><p>All three items are in the Karsus Vault inside Ramazith Tower (Upper City, Act 3): <strong>Markoheshkir</strong> — legendary staff, +1 spell DC/attack, Arcane Battery (free spell per long rest), Kereska's Favour (imbue with element for resistance). <strong>The Annals of Karsus</strong> — legendary spell book, teaches high-level wizard spells permanently. <strong>The Red Knight's Final Strategem</strong> — legendary spell book, unique tactical spells.</p></section>
<section id="route"><h2>2. Complete Route</h2><p><strong>1.</strong> Reach Upper City (Act 3 late progression). Find Ramazith Tower in northeastern section. <strong>2.</strong> Inside the tower, lower level — vault over to a side room with locked bookcase and vault route. <strong>3.</strong> Navigate four doors in sequence: Ramazith Door (specific key or lockpick) → Silverhand Door (Silverhand item or high Arcana) → Evocation Door (cast Evocation spell in front of it) → Silver Door (final door). <strong>4.</strong> Vault chamber contains all three legendary items.</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #1</div>
<section id="hazard"><h2>3. Hazard Guide</h2><div class="danger-box"><div class="box-label">⚠ Door Order Matters</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">The four doors must be opened in sequence. Wrong approach wastes resources but doesn't lock progress.</p></div><div class="danger-box"><div class="box-label">⚠ Clear Tower First</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Ramazith Tower has guardian enemies on various floors. Clear before vault route to avoid interruption.</p></div><div class="danger-box"><div class="box-label">⚠ Bring Lockpicks</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Several doors have lockpick options as backup to skill checks.</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #2</div>
<section id="verdict"><h2>4. Essential for Any Wizard</h2><p>Markoheshkir alone makes this vault worth the trip for any spellcaster. The free spell per long rest and +1 DC combine to make it the best wizard staff in the game. Combined with two legendary spell tomes, this is the single most valuable non-combat destination for magic users in Act 3.</p></section>''',
            "sidebar": [("why","1. What You Get"),("route","2. Complete Route"),("hazard","3. Hazard Guide"),("verdict","4. Essential Wizard")],
            "related": ""
        },
        "zh": {
            "title": "卡苏斯金库路线——上城法师塔里的四道锁门，以及门后的三件传奇物品 | RelicTrek 圣物寻踪",
            "desc": "拉马兹斯塔楼内有：马克霍赫什基尔法杖（+1法术DC，每次长休免费施法），卡苏斯编年史（永久学习高阶法术），红骑士最终战略。穿越上城法师塔内四道依次排列的门。",
            "kw": "博德之门3 卡苏斯金库, BG3 马克霍赫什基尔法杖, 拉马兹斯塔楼, 传奇法术书",
            "tags": ["传奇物品", "第三幕", "法师塔"],
            "h1": "卡苏斯金库——四道锁门后的三件传奇",
            "meta": '<span>🕐 ~1.5小时</span><span>⚔ 无Boss（解谜）</span><span>📍 上城拉马兹斯塔楼</span><span>📚 法杖+2本法典</span><span>📅 更新 2026-06-04</span>',
            "stats": [("+1法术DC","法杖"),("免费施法","每次长休"),("~1.5h","解谜路线"),("无Boss","纯解谜"),("第三幕","上城")],
            "content": '''<section id="why"><h2>一、你获得什么</h2><p>三件物品均在拉马兹斯塔楼（上城第三幕）的卡苏斯金库内：<strong>马克霍赫什基尔法杖</strong>——传奇法杖，+1法术DC/攻击，奥术电池（每次长休免费施法一次），元素赋予（六选一获抗性）。<strong>卡苏斯编年史</strong>——传奇法术书，永久学习高阶法师法术。<strong>红骑士最终战略</strong>——传奇法术书，独特战术法术。</p></section>
<section id="route"><h2>二、完整路线</h2><p><strong>1.</strong> 到达上城（第三幕后期）。在东北区域找到拉马兹斯塔楼。<strong>2.</strong> 塔内下层——翻越隔间到有锁书柜和通往金库路线的侧室。<strong>3.</strong> 依次穿越四道门：拉马兹门（特定钥匙或开锁）→银手门（银手相关物品或高奥术检定）→唤术门（在门前施放唤术系法术）→银门（最后一道）。<strong>4.</strong> 金库室内三件传奇物品全部可取。</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #1</div>
<section id="hazard"><h2>三、避坑指南</h2><div class="danger-box"><div class="box-label">⚠ 顺序重要</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">四道门必须依次打开。错误的方法浪费资源但不锁定进度。</p></div><div class="danger-box"><div class="box-label">⚠ 先清塔</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">拉马兹斯塔楼各层有守护者。金库路线前先清理避免中断。</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #2</div>
<section id="verdict"><h2>四、任何法师的必备之地</h2><p>仅马克霍赫什基尔法杖就值得任何施法者跑一趟。每次长休免费施法+ +1DC使之成为全游戏最佳法师法杖。加上两本传奇法术书，这是第三幕魔法使用者最有价值的非战斗目的地。</p></section>''',
            "sidebar": [("why","一、你获得什么"),("route","二、完整路线"),("hazard","三、避坑指南"),("verdict","四、法师必备")],
            "related": ""
        }
    },
    "helldusk-armor": {
        "en": {
            "title": "Helldusk Armor — The Best Heavy Armor in BG3 Without Fighting Raphael | RelicTrek",
            "desc": "Legendary heavy armor (21 AC, no STR requirement) with fire immunity and Spell Resistance. Located in the House of Hope Archive — take the armor, skip the Orphic Hammer, and leave without triggering the Raphael boss fight.",
            "kw": "BG3 Helldusk Armor, Raphael armor no fight, House of Hope Archive, fire immunity armor, Spell Resistance heavy armor, 21 AC no strength",
            "tags": ["Legendary Armor", "Act 3", "No Boss Required"],
            "h1": "Helldusk Armor — The Best Heavy Armor Without Fighting Raphael",
            "meta": '<span>🕐 ~30 min (partial run)</span><span>⚔ No boss for armor only</span><span>📍 House of Hope Archive</span><span>🛡 Fire Immune + Spell Resist</span><span>📅 Updated 2026-06-04</span>',
            "stats": [("21 AC","No STR Req"),("Fire Immune","Cannot Burn"),("Spell Resist","Save Advantage"),("~30 min","Partial Run"),("Act 3","House of Hope")],
            "content": '''<section id="why"><h2>1. What It Does</h2><p>Legendary Heavy Armor: 21 AC (no Strength requirement — any class wears it). Prime Aegis of Fire: immunity to fire damage, cannot be Burned. Spell Resistance: advantage on all saving throws against spells. Hellfire: once per long rest, 3d6 fire + 3d6 necrotic on a target. This is the strongest heavy armor in the game.</p></section>
<section id="route"><h2>2. Getting Helldusk Without Fighting Raphael</h2><p>The Helldusk Armor is in the Archive of the House of Hope — the SAME room as the Orphic Hammer. You can take the armor WITHOUT picking up the hammer, which does NOT trigger the alarm. Route: enter House of Hope via Helsik portal → get disguise from Hope → navigate to Archive → take Helldusk Armor → do NOT touch Orphic Hammer → exit. No Raphael fight required. If you also want all other items: follow the full <a href="house-of-hope.html">House of Hope heist</a>, taking everything before the hammer last.</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #1</div>
<section id="hazard"><h2>3. Hazard Guide</h2><div class="danger-box"><div class="box-label">⚠ Don't Touch the Hammer</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">The alarm triggers ONLY when the Orphic Hammer is taken. Helldusk Armor is safe to take.</p></div><div class="danger-box"><div class="box-label">⚠ Haarlep Still Required</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Getting the Archive password from Raphael's Safe (via Haarlep key) is still needed to navigate safely.</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #2</div>
<section id="verdict"><h2>4. Best Defense in the Game</h2><p>The combination of fire immunity, Spell Resistance, and no Strength requirement makes this the most universally useful heavy armor in BG3. Any class can wear it, and the defensive passives make the wearer one of the most durable frontliners possible in Act 3 without any build investment.</p></section>''',
            "sidebar": [("why","1. What It Does"),("route","2. No-Fight Route"),("hazard","3. Hazard Guide"),("verdict","4. Best Defense")],
            "related": '<li><a href="/en/games/bg3/house-of-hope.html">House of Hope (Full) →</a></li>'
        },
        "zh": {
            "title": "地狱黑暗盔甲——全游戏最强重甲，不需要击败拉斐尔也能拿到 | RelicTrek 圣物寻踪",
            "desc": "传奇重甲21AC无力量要求，火焰免疫+法术抗性。在希望之屋档案馆——只取盔甲，不碰奥菲克锤，不触发警报，不打拉斐尔。",
            "kw": "博德之门3 地狱黑暗盔甲, BG3 拉斐尔不打, 希望之屋档案馆, 火焰免疫重甲, 法术抗性",
            "tags": ["传奇盔甲", "第三幕", "无需Boss"],
            "h1": "地狱黑暗盔甲——不需要击败拉斐尔的最强重甲",
            "meta": '<span>🕐 ~30分钟（部分路线）</span><span>⚔ 仅取盔甲无需Boss</span><span>📍 希望之屋档案馆</span><span>🛡 火焰免疫+法术抗性</span><span>📅 更新 2026-06-04</span>',
            "stats": [("21AC","无力量要求"),("火焰免疫","不能燃烧"),("法术抗性","豁免优势"),("~30min","部分路线"),("第三幕","希望之屋")],
            "content": '''<section id="why"><h2>一、装备属性</h2><p>传奇重甲：21AC（无力量要求——任何职业都可穿戴）。火焰护盾：免疫火焰伤害，不能被燃烧。法术抗性：所有法术豁免掷骰优势。地狱火：每次长休一次对目标造成3d6火焰+3d6死灵伤害。这是全游戏最强重甲。</p></section>
<section id="route"><h2>二、不触发拉斐尔战的获取路线</h2><p>地狱黑暗盔甲在希望之屋档案馆——和奥菲克锤在同一个房间。可以只取盔甲不碰锤子——不会触发警报。路线：通过赫尔西克传送门进入希望之屋→从希望处获得伪装→导航至档案馆→取地狱黑暗盔甲→不要碰奥菲克锤→离开。无需与拉斐尔战斗。若想同时获得全部物品：遵循完整<a href="house-of-hope.html">希望之屋攻略</a>，最后拿锤子之前先拿齐所有物品。</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #1</div>
<section id="hazard"><h2>三、避坑指南</h2><div class="danger-box"><div class="box-label">⚠ 不要碰锤子</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">警报仅在取走奥菲克锤时触发。地狱黑暗盔甲安全可取。</p></div><div class="danger-box"><div class="box-label">⚠ 仍需哈尔勒普</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">从拉斐尔保险箱（通过哈尔勒普钥匙）获取档案馆密码仍是安全导航所必需的。</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #2</div>
<section id="verdict"><h2>四、全游戏最佳防御</h2><p>火焰免疫+法术抗性+无力量要求的组合使这件盔甲成为BG3中普适性最强的重甲。任何职业都能穿，防御被动使穿戴者成为第三幕最耐打的前排之一，无需任何构筑投入。</p></section>''',
            "sidebar": [("why","一、装备属性"),("route","二、无战斗路线"),("hazard","三、避坑指南"),("verdict","四、最佳防御")],
            "related": '<li><a href="/zh/games/bg3/house-of-hope.html">希望之屋（完整）→</a></li>'
        }
    },
    "karlach-engine": {
        "en": {
            "title": "Karlach Engine — The Three-Act Upgrade Chain That Keeps Her Alive | RelicTrek",
            "desc": "Find Dammon the infernal smith three times across Acts 1-3 to upgrade Karlach's Infernal Engine. Each upgrade unlocks new combat abilities. Miss Dammon in Act 1 (Grove destruction) or Act 2 (Last Light siege) = upgrade permanently lost.",
            "kw": "BG3 Karlach engine, Dammon locations, Karlach upgrade chain, Infernal Engine, Karlach companion quest, Act 1-3",
            "tags": ["Companion Quest", "⚠ MISSABLE", "Acts 1-3"],
            "h1": "Karlach Engine — Three Upgrades Across Three Acts",
            "meta": '<span>🕐 Across full game</span><span>⚠ Missable in Act 1 or 2</span><span>📍 Druid Grove → Last Light → Lower City</span><span>❤ Dammon x3</span><span>📅 Updated 2026-06-04</span>',
            "stats": [("3 Upgrades","Across 3 Acts"),("⚠ Missable","Act 1 or 2"),("Dammon","Infernal Smith"),("Combat","Ability Unlocks"),("Story","Karlach Survival")],
            "content": '''<section id="why"><h2>1. Why It Matters</h2><p>Karlach joins with a malfunctioning Infernal Engine. Three times across the game, the infernal smith Dammon can upgrade it. Each upgrade changes her combat abilities and extends her survival. Most players complete her quest partially — all three Dammon meetings is rarer because he moves between acts and can die permanently.</p></section>
<section id="dammon"><h2>2. Three Dammon Locations</h2><p><strong>Act 1 — Druid Grove:</strong> Dammon at the Emerald Grove. Prerequisite: Grove must survive (do NOT side with goblins). If Grove falls, Dammon dies, all upgrades lost. <strong>Act 2 — Last Light Inn:</strong> Find Dammon BEFORE Moonrise Towers falls. If you advance past the Inn siege without speaking to him, he may die. <strong>Act 3 — Forge of the Nine (Lower City):</strong> Fixed workshop. Cannot be missed once Act 3 begins.</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #1</div>
<section id="hazard"><h2>3. Hazard Guide</h2><div class="danger-box"><div class="box-label">⚠ Grove Survival (Act 1)</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Do not massacre the Grove or side with Minthara's goblin route. This is the most commonly missed prerequisite.</p></div><div class="danger-box"><div class="box-label">⚠ Last Light Timing (Act 2)</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Speak to Dammon at the Inn BEFORE engaging the main Act 2 climax. After the Inn is attacked, Dammon may die.</p></div><div class="danger-box"><div class="box-label">⚠ Act 3 Is Safe</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">Dammon has a permanent workshop in the Lower City. He does not move and cannot be missed in Act 3.</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — In-Content Ad #2</div>
<section id="verdict"><h2>4. The Most Commonly Missed Companion Quest</h2><p>Karlach's engine upgrades are easy to miss because Dammon is not flagged as essential, can die in two separate acts, and has no quest marker directing the player to find him each time. A fully upgraded Karlach is one of the strongest melee companions in the game — a partially upgraded one is notably weaker. The difference is three conversations most players never have.</p></section>''',
            "sidebar": [("why","1. Why It Matters"),("dammon","2. Dammon Locations"),("hazard","3. Hazard Guide"),("verdict","4. Most Missed")],
            "related": ""
        },
        "zh": {
            "title": "卡拉赫引擎心脏升级链——贯穿三幕的升级任务，让她活着 | RelicTrek 圣物寻踪",
            "desc": "在三幕中三次找到炼狱铁匠达蒙，升级卡拉赫的炼狱引擎。每次升级解锁新的战斗能力。第一幕（圣林被毁）或第二幕（最后曙光围攻）错过达蒙=永久失去升级。",
            "kw": "博德之门3 卡拉赫引擎, BG3 达蒙位置, 卡拉赫升级链, 炼狱引擎, 卡拉赫同伴任务",
            "tags": ["同伴任务", "⚠ 可错过", "第一至三幕"],
            "h1": "卡拉赫引擎——贯穿三幕的三次升级",
            "meta": '<span>🕐 贯穿全游戏</span><span>⚠ 第一或二幕可错过</span><span>📍 圣林→最后曙光→下城</span><span>❤ 达蒙×3</span><span>📅 更新 2026-06-04</span>',
            "stats": [("3次升级","贯穿3幕"),("⚠ 可错过","第一或二幕"),("达蒙","炼狱铁匠"),("战斗","能力解锁"),("剧情","卡拉赫存活")],
            "content": '''<section id="why"><h2>一、为什么重要</h2><p>卡拉赫加入时胸腔里有一个过热的炼狱引擎。贯穿游戏三幕，炼狱铁匠达蒙可以对引擎进行三次升级。每次升级改变她的战斗能力并延续她的生存。大多数玩家只完成部分——三次全部找到达蒙更为罕见，因为他在幕间移动且可能永久死亡。</p></section>
<section id="dammon"><h2>二、三处达蒙位置</h2><p><strong>第一幕——翡翠圣林：</strong>达蒙在圣林做铁匠。前置条件：圣林必须存活（不要协助哥布林路线）。若圣林被毁，达蒙死亡，全部升级失效。<strong>第二幕——最后曙光旅馆：</strong>在月升要塞沦陷前找到达蒙。若在旅馆被围攻后才去找他，他可能已死亡。<strong>第三幕——下城九神铸造坊：</strong>固定工坊。进入第三幕后不会错过。</p></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #1</div>
<section id="hazard"><h2>三、避坑指南</h2><div class="danger-box"><div class="box-label">⚠ 圣林存活（第一幕）</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">不要屠杀圣林或协助明萨拉的哥布林路线。这是最常见被错过的前置条件。</p></div><div class="danger-box"><div class="box-label">⚠ 最后曙光时机（第二幕）</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">在第二幕主线高潮前与旅馆的达蒙对话。旅馆被攻击后他可能死亡。</p></div><div class="danger-box"><div class="box-label">⚠ 第三幕安全</div><p style="margin:0;font-size:.85rem;color:var(--text-dim)">达蒙在下城有永久工坊。第三幕不会错过。</p></div></section>
<div class="ad-placeholder" style="margin:2rem 0;">Google AdSense — 文中广告 #2</div>
<section id="verdict"><h2>四、最常被错过的同伴任务</h2><p>卡拉赫的引擎升级容易被错过，因为达蒙没有被标记为重要NPC，会在两幕中分别可能死亡，且没有任何任务标记引导玩家每次去找他。完全升级的卡拉赫是游戏中最强的近战同伴之一——部分升级的明显更弱。区别在于大多数玩家从未进行的三次对话。</p></section>''',
            "sidebar": [("why","一、为什么重要"),("dammon","二、达蒙位置"),("hazard","三、避坑指南"),("verdict","四、最常错过")],
            "related": ""
        }
    }
}

print("Generating BG3 Group 2 files...")
for slug, data in guides.items():
    for lang in ["en", "zh"]:
        d = data[lang]
        html = build_page(lang, slug, d["title"], d["desc"], d["kw"], d["tags"], d["h1"], d["meta"], d["stats"], d["content"], d["sidebar"], d.get("related",""))
        create(f"{lang}/games/bg3/{slug}.html", html)
print("Done! Generated 12 guide files (6 EN + 6 ZH).")
