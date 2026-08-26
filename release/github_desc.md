# MC Ecosystem Adaptation Engineer

> One-stop Minecraft mod ecosystem intelligent management tool.

---

> ## 🚨 [URGENT NOTICE TO ALL EXISTING USERS]
>
> **Dear V1.0.2 and earlier users:**
>
> Thank you for downloading and using this Skill! To provide you with a more stable experience and richer features, **please make sure to update to the latest version V1.0.3**.
>
> ### ✅ What's New in V1.0.3 (Exclusive Perks for Existing Users)
>
> 1. **🔧 Fixed Network Fluctuation Download Freeze**: Previous versions would hang during mod downloads on unstable networks requiring manual interruption. V1.0.3 adds timeout + auto-retry (3x exponential backoff) + resume-from-breakpoint, greatly improving download reliability
> 2. **📢 New Version Auto-Reminder**: From now on, whenever a new version is released on GitHub, the Skill will display a banner notification at the top of the console — **never miss important updates again**
> 3. **💰 Free Period & Payment System Fully Launched**: V1.0.3 supports Alipay / WeChat Pay / PayPal three-channel payments. **Existing users get 20% OFF your first month** after upgrading
> 4. **🇸🇦 Added Modern Standard Arabic Support**: 10 languages → 12 languages with auto-detection, including Arabic (ar_sa) with full RTL right-to-left layout support
> 5. **🎛️ Admin Dashboard Now Live**: Complete web-based operation console with manual authorization activation, order tracking, email notifications, and automated business reports
> 6. **📋 One-Click Machine ID Viewer**: Built-in "View My Machine ID + Copy to Clipboard" button for easier manual authorization activation
>
> ### 🎁 Exclusive Perks for Upgrading Users
>
> - **20% OFF First Month**: After upgrading, send your machine ID to the developer via contact info on the payment guide page to receive your exclusive 20% discount license key (V1.0.2 upgraders only)
> - **Free Period Fully Preserved**: Your 60-day free period starts from your first use of the original version and is **100% preserved** after upgrading — no reset
> - **Semi-Manual Activation Flow**: V1.0.3 adds semi-manual payment activation guide that works even before cloud server deployment
>
> ### ⚠️ Why You Should Upgrade Today
>
> V1.0.2 and earlier versions **have no version reminder feature**, meaning you could miss critical bug fixes and new features. After upgrading to V1.0.3, you'll be notified immediately every time a new GitHub release is published. Even better: V1.0.3 supports **urgent notices pushed without version bumps** — the developer can broadcast time-sensitive announcements (free period rule changes, limited-time discounts, etc.) via the banner even when the version number doesn't change.
>
> **Click the "Update" button below to upgrade now! If you have any questions, reach the developer via the contact methods on the Skill's payment guide page (email / QQ / Afdian).**
>
> — Liang Jingyu, Developer
>
> ---
>
> ## 🚨【中文紧急公告 · 请所有老用户必读】
>
> **尊敬的 V1.0.2 及更早版本老用户：**
>
> 感谢您下载使用本 Skill！为了给您提供更稳定的体验和更丰富的功能，**请您务必更新到最新版本 V1.0.3**。
>
> ### ✅ V1.0.3 新版本重要更新（老用户专属福利）
>
> 1. **🔧 修复网络波动下载卡死问题**：V1.0.2 版本中模组下载在网络不稳定时会卡住需手动中断，V1.0.3 已新增超时+自动重试（3次指数退避）+断点续传
> 2. **📢 新增版本自动提醒功能**：以后 GitHub 每次发布新版本，Skill 会在控制台顶部自动弹窗提醒，**再也不用担心错过重要更新**
> 3. **💰 免费期与付费体系全面上线**：支持支付宝/微信/PayPal 三渠道支付，老用户升级后**立即享受首月 8 折专属优惠**
> 4. **🇸🇦 新增通用阿拉伯语支持**：10 种语言升级为 12 种，含阿拉伯语 RTL 从右向左书写
> 5. **🎛️ 管理员控制台上线**：完整 Web 运营后台，支持手动开通授权、订单追踪、邮件通知
> 6. **📋 一键查看机器码**：内置「查看我的机器码 + 一键复制」按钮，手动开通授权更便捷
>
> ### 🎁 老用户升级专属福利
>
> - **首月套餐 8 折优惠**：升级后通过付费引导页的联系方式发送机器码领取专属 8 折授权码（仅限 V1.0.2 升级用户）
> - **免费期完整保留**：60 天免费期从首次使用 V1.0.2 那天起算，升级后 100% 保留，不重置
> - **半手动开通流程**：V1.0.3 新增半手动付费开通引导，云服务器未上线也能手动完成授权
>
> ### ⚠️ 为什么强烈建议升级？
>
> V1.0.2 及更早版本**没有版本提醒功能**，您可能会错过重要 Bug 修复和功能更新。升级到 V1.0.3 后，每次 GitHub 发版都会第一时间通知。V1.0.3 还支持**版本不变时的紧急通知推送**——不发版也能推送免费期规则变更、限时优惠等信息。
>
> **立即点击「更新」按钮升级！如有问题，请通过付费引导页的联系方式（邮箱/QQ/爱发电）联系作者。**
>
> —— 开发者 梁靖羽 敬上

---

## Overview

MC Ecosystem Adaptation Engineer is an AI-powered assistant tool for Minecraft mod players and modpack authors. It covers 15 core capabilities including mod search, environment setup, Mixin conflict scanning, crash analysis, multi-language translation, migration feasibility assessment, online payment system, admin dashboard, and automated business reports. Supports Forge, NeoForge, Fabric, and Quilt loaders across MC versions 1.16.5 to 1.21.x. 12-language auto-detection with Arabic RTL support.

---

### 📝 Version Additions / Optimizations by Release (GitHub release numbering, against actual GitHub_V1.0.2 README)

> **GitHub V1.0.2 README actual overview**: "10+ core capabilities" — only F1–F9 + F8.1 in the feature table (10 items), 10 languages (ZH/EN/JA/KO/RU/ES/IT/EL/TH/HI), no commercial modules, no Arabic.

**GitHub V1.0.3 added/optimized (upcoming release, from GitHub V1.0.2 → V1.0.3):**
- 🏗️ **10+ → 15 core capabilities** — overview module adds F12 Online Payment System, F13 Admin Dashboard, F14 Automated Business Reports (full commercial stack)
- 🇸🇦 **Arabic MSA added to overview** — GitHub V1.0.2 had zero mention of Arabic; V1.0.3 updates the overview to "12-language auto-detection with Arabic RTL support"
- 💰 **Progressive 3-level payment guidance now in overview context** — GitHub V1.0.2 overview had no payment-related narrative at all; V1.0.3 overview carries it as part of the 15-capability commercial system
- 📦 **Dataset expansions** — recommendation DB 50+ → 65+ mods; Java version mapping table fully expanded

**GitHub V1.0.2 (current online release — what users actually see in the README today):**
- Overview only promises 10+ capabilities and 10 built-in languages (nothing else)

---

## Key Features

| # | Feature | Description |
|---|---------|-------------|
| F1 | JAR Structure Parser | Parse mod JAR metadata (mcmod.info, fabric.mod.json, mods.toml) and generate Chinese feature documentation |
| F2 | Mod Search & Download | Modrinth API integration with version/loader/category filtering, batch search, category search, related recommendations, dynamic categories, and auto-update |
| F3 | Environment Setup Guide | Intelligently recommend MC version and loader combinations, auto-detect Java version and launcher paths |
| F4 | Mixin Conflict Scanner | Detect Mixin injection conflicts between multiple mods and identify compatibility risks |
| F5 | Resource Repacker + Mod Packaging Output | Repack and optimize mod resource files (textures, sounds, language files in batch), plus resource-level migration bundles and distributable mod package generation |
| F6 | Save Sync | Backup and restore game saves with multi-device sync support |
| F7 | Multi-language Translation | Translate mod language files between 12 supported languages (ZH/EN/JA/KO/RU/ES/IT/EL/TH/HI/AR with RTL) |
| F8 | Crash Fix | Intelligently analyze crash logs, identify 25+ error patterns, and provide fix suggestions |
| F8.1 | Auto Fix | One-click mod version upgrade, automatic backup and replacement with fix report generation |
| F9 | Migration Feasibility Assessment | Cross-version/cross-loader migration feasibility report with API/dependency/Mixin analysis |
| F10 | Authorization & Usage Management | Local machine ID generation, daily usage counting, 60-day free period management, membership tiers (Free/Normal/Premium-Coming-Soon), license activation, with server-side verification via F13 Admin Dashboard |
| F11 | Payment Guide | Three-level progressive payment guidance (friendly reminder → subscription plans → support options) |
| F12 | Online Payment System | Alipay, WeChat Pay, and PayPal integration with 3 subscription plans (monthly/quarterly/yearly) |
| F13 | Admin Dashboard | Web-based admin console for user management, order tracking, permission control, email configuration, and notification settings |
| F14 | Automated Business Reports | Inactive user lists, subscription expiry reminders, and monthly business summary reports |

---

### 📝 Version Additions / Optimizations by Release (GitHub release numbering, against actual GitHub_V1.0.2 README feature table)

> **GitHub V1.0.2 README actual feature table**: only F1–F9 + F8.1 (10 rows). **F10/F11/F12/F13/F14 are all missing** from the feature table. F7 row explicitly states "10 supported languages (ZH/EN/JA/KO/RU/ES/IT/EL/TH/HI)" (not 11).

**GitHub V1.0.3 added/optimized (Key Features module, true delta vs. V1.0.2 package):**
- 🆕 **F10 Authorization & Usage Management (first public feature-table listing)** — GitHub V1.0.2 README feature table had no F10 row (although an internal declaration existed in SKILL.json); V1.0.3 publicly lists it for the first time: machine ID generation, 60-day free period, daily usage counting, membership tiers, license activation, with F13 server-side auth linkage
- 🆕 **F11 Payment Guide (3-level)** — GitHub V1.0.2 feature table had no F11 row; V1.0.3 adds friendly reminder → subscription plans → support & appreciation (non-mandatory, daily free quota preserved)
- 🆕 **F12 Online Payment System** — GitHub V1.0.2 had no payment module at all; V1.0.3 adds Alipay/WeChat/PayPal with 3 subscription tiers (monthly/quarterly/yearly) and mandatory "I paid" verification button
- 🆕 **F13 Admin Dashboard** — GitHub V1.0.2 had zero admin console; V1.0.3 adds Web-based console with random admin key, 1h token, user/order/permission/email/notification management
- 🆕 **F14 Automated Business Reports** — GitHub V1.0.2 had no reporting system; V1.0.3 adds inactive-user lists, expiry reminders (configurable weekday), monthly summary, and a manual test-email trigger
- ⬆️ **F7 Multi-language Translation (10 → 12 languages)** — GitHub V1.0.2 explicitly listed only 10 languages (no Arabic); V1.0.3 adds ar_sa MSA, Arabic MC terms dictionary (Tool→أداة, Armor→درع, etc.), multi-language dictionary lookup engine, and RTL layout on payment pages
- ⬆️ **F2 Mod Search description expanded** — GitHub V1.0.2 only said "version and loader filtering"; V1.0.3 now aligns with actual shipped capability: batch search, category search, related recommendations, dynamic categories, auto-update
- 📦 **Dataset expansion note** — mod recommendation index 50+ → 65+; Java version mapping table expanded comprehensively

---

## Technical Highlights

- **All-Loader Support**: Native support for Forge, NeoForge, Fabric, and Quilt
- **12 Languages**: Built-in language packs for Chinese, English, Japanese, Korean, Russian, Spanish, Italian, Greek, Thai, Hindi, and Arabic (with RTL support)
- **25+ Crash Patterns**: Comprehensive crash pattern database covering OOM, shader conflicts, Mixin conflicts, class loading failures, and more
- **Modrinth API Integration**: Real-time mod version queries via Modrinth API
- **Smart Caching**: Avoid redundant API calls for improved response speed
- **Safety Backups**: Forced backup before auto-fix operations with one-click rollback support
- **Mixin Injection Analysis**: Deep scan of Mixin injection points with target class compatibility assessment
- **Cross-Platform**: Windows, macOS, and Linux support
- **Commercialization Ready**: Integrated payment system (Alipay/WeChat/PayPal), admin dashboard, and automated business reports

---

### 📝 Version Additions / Optimizations by Release (GitHub release numbering, against actual GitHub_V1.0.2 README Technical Highlights)

> **GitHub V1.0.2 README actual Technical Highlights (8 bullets, exact):** All-Loader Support, **10 Languages**, 25+ Crash Patterns, Modrinth API Integration, **Smart Caching**, Safety Backups, Mixin Injection Analysis, Cross-Platform.
> **Note**: "Offline Mode" and "Commercialization Ready" are **NOT present in the actual V1.0.2 README highlights** at all. Smart Caching, however, already exists in V1.0.2.

**GitHub V1.0.3 added/optimized (Technical Highlights module, true delta vs. V1.0.2 package):**
- 🇸🇦 **10 Languages → 12 Languages with explicit Arabic RTL note** — GitHub V1.0.2 only wrote "Built-in language packs for [10 languages]"; V1.0.3 updates to "12 Languages...and Arabic (with RTL support)"
- 🪙 **"Commercialization Ready" — brand new 9th highlight bullet** — GitHub V1.0.2 had zero commercial highlights; V1.0.3 adds the 9th bullet covering full Alipay/WeChat/PayPal + admin dashboard + automated reports stack
- 🛡️ **Commercial security posture implicitly covered** — random admin key, 1h in-memory token, server-side F10+F13 auth checks are all now implied by the new Commercialization Ready bullet
- 📚 **Crash pattern content expanded** — GitHub V1.0.2 already listed the "25+ Crash Patterns" bullet count; V1.0.3 expands the actual pattern entries and fix suggestions behind that number (not the headline count)

---

## Pricing

### Free Period

All features are free for 60 days from first use (except migration assessment: 1/day after first free use).

### Subscription Plans (V1.0.4)

- **Free**: 20 auto/day, 8 semi/day
- **Normal Member**: 100 auto/day, 50 semi/day ($9.99/month, $24.99/quarter, $69.99/year)
- **Premium**: Coming Soon

Payment channels: Alipay, WeChat Pay, PayPal

---

### 📝 Version Additions / Optimizations by Release (GitHub release numbering, against actual GitHub_V1.0.2 README Pricing)

> **GitHub V1.0.2 README actual Pricing (exact 3 lines)**:
> "### Free Access — All features are currently free during the beta period. Premium subscription options will be available in the future. Stay tuned for updates."
> — NO 60-day free-period rule, NO tiered quotas, NO pricing, NO payment channels, NO F11/F12 content of any kind.

**GitHub V1.0.3 added/optimized (Pricing module, true delta vs. V1.0.2 package):**
- ✅ **Commercial features officially launched** — GitHub V1.0.2 had zero real pricing (only "coming soon" placeholder); V1.0.3 ships live Alipay/WeChat/PayPal 3-channel integration
- 💬 **Explicit $ pricing tiers added** — $9.99/month, $24.99/quarter, $69.99/year for Normal Member (Free + Premium tiers documented)
- 📊 **Tiered usage quotas documented** — Free 28/day (20 auto + 8 semi) vs Normal 150/day (100 auto + 50 semi) vs Premium Coming Soon
- 🔒 **60-day free period rule codified** — migration assessment stays 1/day after first free use; all other features unlimited for 60 days from first use
- 📣 **3-level progressive payment guide introduced** — friendly reminder at approaching limit → plan display → support & appreciation (non-mandatory flow)
- 🎯 **Daily free quota numbers stated explicitly** — users now see concrete figures for the first time
- 🌐 **10 → 12 languages payment copy** — all pricing and payment-guide UI copy translated into Arabic as well, with RTL layout and CNY/USD currency auto-switch

---

## Installation

### Prerequisites

- Python 3.10+
- Windows / macOS / Linux
- Network connection (required for mod search and version queries)

### Quick Start

```bash
# 1. Clone or download the project
cd mc-skill-v1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run interactively
python main.py

# Or use the startup script
# Windows: mc-skill-start.bat
```

### Command Line Usage

```bash
# Parse mod JAR structure
python main.py --feature jar_parser --jar-path "create.jar"

# Search and download mods
python main.py --feature mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"

# Analyze crash log
python main.py --feature crash_analyzer --crash-log "crash-report.txt"

# Auto-fix crash issues
python main.py --feature auto_fix --crash-log "crash.txt" --fix-mods-dir "~/.minecraft/mods"

# Assess migration feasibility
python main.py --feature migration_assess --jar-path "mod.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"

# Translate mod language files (Arabic — V1.0.4)
python main.py --feature translator --mods-dir "~/.minecraft/mods" --lang ar_sa

# Sync game saves
python main.py --feature save_sync --action sync --save-dir "~/.minecraft/saves"
```

---

### 📝 Version Additions / Optimizations by Release (GitHub release numbering, against actual GitHub_V1.0.2 README Installation)

> **GitHub V1.0.2 README actual Installation (true facts)**:
> - Already split into **Prerequisites / Quick Start / Command Line Usage** 3 sections (so NOT new in V1.0.3).
> - Command Line Usage already had 7 examples: jar_parser, mod_searcher, crash_analyzer, **auto_fix**, **migration_assess**, **translator**, **save_sync** (included auto_fix/F9/save_sync samples).
> - Translator example used `--lang zh_cn`; there was **no `--lang ar_sa`** anywhere.

**GitHub V1.0.3 added/optimized (Installation module, true delta vs. V1.0.2 package):**
- 🇸🇦 **Arabic translation CLI example added** — first ever `--lang ar_sa` sample invocation in the Command Line Usage section (GitHub V1.0.2 had only `--lang zh_cn` + no Arabic docs)
- 📘 **`--lang` value range documented as 12 languages** — GitHub V1.0.2 never enumerated the full 11-language list; V1.0.3 updates this to 12 languages (includes `ar_sa`)
- 🌐 **All CLI examples kept in sync with the latest feature parameters** — continued alignment with new F10–F14 module availability (even though those aren't separately documented as CLI samples)

---

## Changelog (GitHub release numbering: GitHub V1.0.2 → GitHub V1.0.3)

> **Note**: The **actual GitHub_V1.0.2 README in dist/release-packages does NOT contain any Changelog / Change-log section at all**. For GitHub users, this standalone Changelog section is therefore **a brand-new addition that first ships in GitHub V1.0.3**. The entries below are written strictly by comparing the two README files (V1.0.2 package vs. upcoming V1.0.3 package).

---

### GitHub V1.0.3 (2026-08-25) — Major Release (upcoming)

#### Brand-new modules (absent from GitHub V1.0.2 feature table)

| Module | Description (why new) |
|--------|----------------------|
| F10 Authorization & Usage Management | GitHub V1.0.2 README feature table had no F10 row (internal declaration existed only in SKILL.json); V1.0.3 first public listing: machine ID, free-period, usage counting, membership tiers, license activation |
| F12 Online Payment System | GitHub V1.0.2 Pricing only said "future subscriptions"; V1.0.3 ships Alipay / WeChat Pay / PayPal with 3 subscription plans (monthly/quarterly/yearly) |
| F13 Admin Dashboard | GitHub V1.0.2 had zero admin console or Web UI; V1.0.3 adds a Web-based console with random admin key, 1h tokens, user/order/permission/email/notification management |
| F14 Automated Business Reports | GitHub V1.0.2 had no reporting features; V1.0.3 adds inactive-user lists, configurable expiry reminders, monthly business summary, and a manual test-email trigger |

#### Existing modules with major upgrades (compared to V1.0.2 README)

1. **F11 Payment Guide — from missing to feature-table listed**
   - GitHub V1.0.2 had no F11 row in its README feature table (F11 was only an internal disabled placeholder);
   - GitHub V1.0.3 ships F11 as a documented feature with 3-level progressive guidance (friendly reminder → plan display → support & appreciation, non-mandatory).

2. **F7 Multi-Language Translation — 10 languages → 12 languages, + Arabic MSA + RTL**
   - GitHub V1.0.2 README explicitly listed 10 languages only (no Arabic);
   - GitHub V1.0.3 adds ar_sa Modern Standard Arabic, an Arabic MC terms dictionary (Tool→أداة, Armor→درع, etc.), multi-language dictionary lookup, and RTL rendering on payment pages.

3. **F2 Mod Search & Download — description expanded**
   - GitHub V1.0.2 only advertised "version and loader filtering";
   - GitHub V1.0.3 adds batch search, category search, related mod recommendations, dynamic categories, and auto-update.

#### Dataset & infrastructure improvements

- Mod recommendation index expanded from 50+ to 65+ entries;
- Crash pattern 25+ headline count retained, but actual scenarios and fix suggestions expanded behind that number;
- Java version mapping table completed;
- API cache (TTL + disk persistence), offline-database module, and report-rendering performance improvements continue to ship (already implemented for V1.0.2 but now carried forward);
- Security/compliance flow for F11 (from disabled placeholder → progressive guidance) is part of the F11 upgrade above.

### GitHub V1.0.2 (Current Online Release)

- No standalone Changelog section was present in the V1.0.2 README. For users who read only the README, the headline delta between V1.0.2 and V1.0.0 is what V1.0.2 delivered on release (API caching, offline DB, rendering speedups, 10-language i18n, and the compliance pass).

---

## Author

- **Author**: Liang030214
- **Version**: v1.0.3  *(GitHub release tag; internal dev build corresponds to V1.0.4)*
- **License**: MIT License
- **Homepage**: https://github.com/Liang030214/mc-skill-v1
- **Tags**: minecraft, mod, forge, fabric, neoforge, quilt, mixin, translation, crash-fix, migration, i18n, arabic, rtl, payment, admin, reports

---

### 📝 Version Additions / Optimizations by Release (GitHub platform numbering)

**GitHub V1.0.3 added/optimized (upcoming):**
- 🏷️ **Tags extended** — added `arabic, rtl, payment, admin, reports` tags matching new commercial stack
- 📌 **Version set to GitHub V1.0.3** — independent from internal dev version (which is V1.0.4)

---

## Supported MC Versions

- 1.16.5 ~ 1.21.x

## Supported Loaders

- Forge (47.x+)
- NeoForge (21.1+)
- Fabric (0.15+)
- Quilt (0.23+)
