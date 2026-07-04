# handoff.md — 專案交接文件

> **給接手的 Agent**：這份檔案是本專案的唯一交接入口。開工請先完整讀完本檔，再依「🤖 接手 Agent 執行清單」逐步進行。每完成一個里程碑就回報使用者，不要悶頭做。
>
> 最後更新：**2026-07-04** ｜ 更新者：**Claude Opus 4.8（公開發布 + 環境清點入口）**
>
> **入口變更**：接手請以 **`AGENTS.md`** 為正式行動流程，第一步跑 **`python check_env.py`** 清點缺漏的程式與 API 金鑰。本檔為完整背景交接。

---

## 🎯 專案目的（最重要，先讀）

這個專案是一個**「可被其他老師 Agent 接手、自動重建」的媒體素養教學資源包**。

- **服務對象**：教「媒體素養」的老師。
- **這些老師的教學對象**：**國中、國小學生**。
- **運作模式**：當其他老師把本專案資料夾（或公開的 GitHub Repo）交給他們自己的 Agent，該 Agent 應能**自動重建我們在此專案中完成的所有內容**，並**檢查、協助安裝所有缺漏的元件與程式**。
- **本質**：這不只是一份研習教材，而是一個「**Agent 讀了就能自我 bootstrap**」的教學工具包，設計模型參考 `mathruffian-dot/claude-video-specs` 的 `AGENTS.md` + `install/` 流程。

---

## 📦 專案依賴的三個影片技能

本專案要「一併打包」三個影片製作技能。它們的規範來源是**獨立 repo `mathruffian-dot/claude-video-specs`**（本身即為自動 bootstrap 設計，含 `install/` 一鍵安裝腳本）：

| # | 使用者說法 | 對應規範 / 來源 | 狀態 |
|---|-----------|----------------|------|
| 1 | 製作**社群影片**的技能 | `claude-video-specs/specs/03-社群科普影片.md` | ✅ 來源明確（該 repo） |
| 2 | 製作**教學影片**的技能 | `claude-video-specs/specs/02-教學影片.md` | ✅ 來源明確（該 repo） |
| 3 | **自動剪輯**影片的技能 | 來源 repo `mathruffian-dot/2026-YouTube`（原始位置 `G:\我的雲端硬碟\2026Youtube`）| ✅ **已精簡打包進本專案 `skills/`（見下）** |

### 自動剪輯技能：已打包內容（`skills/`）

本專案 `skills/` 是從 `2026Youtube` 精簡打包的自動剪輯生產線，**已排除影片素材、`__pycache__`、機密 `.env`**（只帶 `.env.example`）。含七個技能：`smart-cut`（去靜音）、`audio-to-srt`（Groq 字幕）、`video-editing-and-subtitles`（字幕收尾）、`short-video-workflow`（短片）、`cover-image`（封面，需 OpenAI）、`claude/codex-youtube-video-workflow`（總控編排）。安裝步驟見 `skills/README.md`。

> 使用者示範時會回到 `G:\我的雲端硬碟\2026Youtube` 原專案跑；本 repo 的 `skills/` 是給其他老師安裝用的副本。兩邊若有更新需注意同步。

> `claude-video-specs` 安裝方式（該 repo README 已載明）：
> ```bash
> git clone https://github.com/mathruffian-dot/claude-video-specs.git
> cd claude-video-specs
> bash install/check_env.sh && bash install/install_all.sh   # 或 install_all.ps1 / setup.py
> # 打包成技能：bash install/pack_skill.sh <name> <02|03> --target=claude
> ```

---

## ✅ 目前做到哪（本次初始化已完成）

| 項目 | 狀態 | 位置 / 說明 |
|------|------|------------|
| CLAUDE.md | ✅ | 專案設定、時程、三處同步指引 |
| .gitignore | ✅ | 排除 desktop.ini、`.env`、`*.key`、credentials 等 |
| Git 本地庫 | ✅ | 已 init + 初始 commit（`c2a8b42`），user = mathruffian-dot |
| GitHub Repo | ✅ **已公開** | `mathruffian-dot/media-literacy-2026`（已 commit + push + public）|
| Obsidian 筆記 | ✅ | `2026媒體素養_agent/專案工作流程.md` |
| 研習大綱 v2 | ✅（既有）| `研習大綱.md`，全天 6 小時線上研習，講師三師爸 |
| AGENTS.md + check_env.py | ✅ | Agent 入口 + 環境清點腳本（缺程式/金鑰逐項回報） |
| 學生短影音腳本入口 | ✅（指南）| `短影音腳本入口_製作指南.md`（Netlify+Groq，原始碼在另一資料夾未同步進本 repo）|
| HK3R 科普片（Claude 版）| ✅ | `output/HK3R科普影片/`（edge-tts 曉臻，115s，build.py 可重跑）|
| 🔒 金鑰安全 | ✅ | `groq_api_key.txt`（含兩把真實 Groq 金鑰）已被 `.gitignore` 排除，未進 repo |
| HK3R 科普影片 | ✅ | [hk3r_video/output_video.mp4](file:///G:/%E6%88%91%E7%9A%84%E9%9B%B2%E7%AB%AF%E7%A1%AC%E7%A2%9F/2026%E5%AA%92%E9%AB%94%E7%B4%A0%E9%A4%8A_agent/hk3r_video/output_video.mp4) (三師爸配音+HyperFrames 網頁動畫影片已產出) |

---

## 🤖 接手 Agent 執行清單（其他老師的 Agent 拿到本 repo 後照做）

**階段 0 — 相容性確認**
- 確認自己有 shell 執行能力（純 Web Agent 無法跑 install，只能參考文件）。
- 確認執行平台：Claude Code → 技能路徑 `~/.claude/skills/`；Codex → `~/.agents/skills/`；OpenCode → `~/.config/opencode/skills/`。

**階段 1 — 讀懂專案**
1. 讀本 `handoff.md`（你正在讀）。
2. 讀 `CLAUDE.md`（專案設定與同步規則）。
3. 讀 `研習大綱.md`（研習五節內容與製作進度）。

**階段 2 — 安裝三個影片技能**
4. Clone 依賴 repo：`git clone https://github.com/mathruffian-dot/claude-video-specs.git`
5. 跑環境檢查：`bash install/check_env.sh`（回報缺漏：字體 / playwright / edge-tts / python 套件等）。
6. 主動詢問使用者是否安裝缺漏元件，同意後 `bash install/install_all.sh`。
7. 依需求打包技能：`pack_skill.sh <name> 02 --target=<agent>`（教學影片）、`... 03 ...`（社群影片）。
8. 自動剪輯技能已內附於本 repo `skills/` → 依 `skills/README.md` 安裝相依（`pip install auto-editor groq openai`、ffmpeg、`~/.groq_api_key`）。

**階段 3 — 缺漏元件總檢查**
9. 檢查並回報缺漏：`gh`（GitHub CLI）是否登入、`ffmpeg`、`python`、字體、API key（如 `~/.groq_api_key`）。
10. **API key 類敏感檔不在 repo 內**，需提醒使用者自行於本機建立。

**階段 4 — 重建與產出**
11. 依 `研習大綱.md` 的「製作進度」續作：回填 YT 數據 → 逐節腳本 → 簡報。
12. 產出教材時可用平台既有技能：`soil-teaching-deck`、`html-slide-builder`、`teaching-cockpit`、`teaching-minigames`。

**階段 5 — 回報**
13. 每完成一個里程碑回報使用者，並更新本 `handoff.md` 的「目前做到哪」與「最後更新」。

---

## ⚠️ 待決策 / 待辦（交接重點）

- [x] ~~repo 改為公開~~ → 已 commit + push + 設為公開（2026-07-04）。
- [x] ~~公開前掃描敏感資訊~~ → 已掃描；發現根目錄 `groq_api_key.txt`（兩把真實金鑰），已加入 `.gitignore` 未提交。**提醒使用者**：該檔請移出 repo 資料夾（改放 `~/.groq_api_key`），並考慮到 console.groq.com 輪替金鑰以策安全。
- [x] ~~定位「自動剪輯影片」技能來源~~ → 已完成，來源 `2026Youtube`，已打包進 `skills/`（2026-07-04）。
- [ ] 回填 YT 總觀看次數與累積觀看時數（YT Studio 後台）。
- [ ] 逐節展開詳細腳本（含互動、金句、講師備忘）。
- [ ] 製作研習簡報（SOIL × 視覺規範）。
- [ ] （可選）建立 `AGENTS.md`，把「接手 Agent 執行清單」做成正式的 5 階段 bootstrap 入口，模仿 `claude-video-specs/AGENTS.md`。

---

## 🗂️ 目前檔案結構

```
2026媒體素養_agent/
├── AGENTS.md        # ★ Agent 正式入口（先讀）
├── check_env.py     # ★ 環境清點腳本（缺程式/金鑰逐項回報）
├── handoff.md       # 本檔：完整背景交接
├── CLAUDE.md        # 專案設定與三處同步指引
├── 研習大綱.md      # 研習大綱 v2（短影音 5 段式 = HK3R）
├── 短影音腳本入口_製作指南.md   # 學生腳本生成入口做法（Netlify+Groq）
├── .gitignore / .env.example
├── skills/          # 自動剪輯 YouTube 生產線（七技能，來源 2026-YouTube）
└── output/HK3R科普影片/          # HK3R 科普片成品 + build.py（可重跑）
（未進 git：groq_api_key.txt〔金鑰〕、*.mp4/*.mp3〔大檔〕）
```

## 🔗 三處同步位置

| 平台 | 位置 |
|------|------|
| Google Drive | `G:\我的雲端硬碟\2026媒體素養_agent\` |
| Obsidian | `2026媒體素養_agent/` |
| GitHub | `mathruffian-dot/media-literacy-2026`（**公開**） |

## 📝 交接更新規則（全域多 Agent 協作）

- **開工**：先讀本 `handoff.md`。
- **有進度或收工**：更新本檔「目前做到哪」「下一步」「最後更新時間與更新者」。
- **改共用檔前**：先讀最新內容，避免覆蓋其他 Agent 的變更。
