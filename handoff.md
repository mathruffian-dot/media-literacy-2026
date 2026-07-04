# handoff.md — 專案交接文件

> **給接手的 Agent**：這份檔案是本專案的唯一交接入口。開工請先完整讀完本檔，再依「🤖 接手 Agent 執行清單」逐步進行。每完成一個里程碑就回報使用者，不要悶頭做。
>
> 最後更新：**2026-07-04** ｜ 更新者：**Claude Opus 4.8（初始化 Agent）**

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
| 3 | **自動剪輯**影片的技能 | 研習第三節亮點「使用 AI Agent 自動剪輯教學影片」工作流；Obsidian 佐證：`創作庫/使用 AI Agent 自動剪輯教學影片 - Skills 福利大放送直播.md` | ⚠️ **本機未找到獨立技能資料夾，需定位或建立** |

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
| GitHub Repo | ⚠️ **目前為私有** | `mathruffian-dot/media-literacy-2026` — 但專案目的需要**公開**（見下方待決策）|
| Obsidian 筆記 | ✅ | `2026媒體素養_agent/專案工作流程.md` |
| 研習大綱 v2 | ✅（既有）| `研習大綱.md`，全天 6 小時線上研習，講師三師爸 |

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
8. 「自動剪輯」技能來源尚未定位 → 向使用者確認來源 repo/路徑後再安裝。

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

- [ ] **【需使用者拍板】repo 改為公開**：目前是私有，但專案目的是「公開分享給其他老師 Agent」。改公開前務必先跑一次敏感資訊掃描（見下一點）。
- [ ] **【安全】公開前掃描敏感資訊**：確認 repo 內無 API key、無個資、無肖像權素材。目前 `.gitignore` 已排除 `.env`/`*.key`/credentials；打包技能時**勿**把 `~/.groq_api_key`、`~/.openai.env` 等寫入 repo。
- [ ] **定位「自動剪輯影片」技能來源**：本機未找到獨立技能夾，需向使用者確認是哪個 repo / skill。
- [ ] 回填 YT 總觀看次數與累積觀看時數（YT Studio 後台）。
- [ ] 逐節展開詳細腳本（含互動、金句、講師備忘）。
- [ ] 製作研習簡報（SOIL × 視覺規範）。
- [ ] （可選）建立 `AGENTS.md`，把「接手 Agent 執行清單」做成正式的 5 階段 bootstrap 入口，模仿 `claude-video-specs/AGENTS.md`。

---

## 🗂️ 目前檔案結構

```
2026媒體素養_agent/
├── handoff.md       # 本檔：Agent 交接入口
├── CLAUDE.md        # 專案設定與三處同步指引
├── .gitignore
└── 研習大綱.md      # 研習大綱 v2（時間軸、五節內容、製作進度）
```

## 🔗 三處同步位置

| 平台 | 位置 |
|------|------|
| Google Drive | `G:\我的雲端硬碟\2026媒體素養_agent\` |
| Obsidian | `2026媒體素養_agent/` |
| GitHub | `mathruffian-dot/media-literacy-2026`（私有，待改公開） |

## 📝 交接更新規則（全域多 Agent 協作）

- **開工**：先讀本 `handoff.md`。
- **有進度或收工**：更新本檔「目前做到哪」「下一步」「最後更新時間與更新者」。
- **改共用檔前**：先讀最新內容，避免覆蓋其他 Agent 的變更。
