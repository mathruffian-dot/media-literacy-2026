# 2026 媒體素養與短影音創作教學實務研習

## 專案簡介
為「教授媒體素養的教師社群」設計的一場**全天 6 小時線上研習**備課專案。講師為三師爸（宋睿偉），主軸為 **讀懂它 → 拆解它 → 做出它 → 經營它 → 帶回教室**（讀 → 析 → 做 → 行 → 教），亮點在第三節「AI Agent 自動剪片工作流」現場 Demo。本資料夾負責研習大綱、逐節腳本、簡報與教學轉化素材的產出與版本控管。

## 關鍵時程
- 研習日期：2026-07-04（線上研習 · 全天 6 小時，09:00–17:00）
- 大綱版本：v2（2026-06-01 定稿）

## 語言與風格
- 所有回應、文件皆使用**繁體中文**
- 修改前先確認計畫，優先保留原有資料結構

## Obsidian 關聯資料
以下 Obsidian 筆記可作為佐證素材，路徑相對於 vault 根目錄：
- `claude-video-specs/specs/03-社群科普影片.md` — 短影音 5 段式硬規範、版面庫（第二節教材）
- `claude-video-specs/specs/02-教學影片.md` — SOIL 脈絡、視覺/配色系統
- `研習直播/第一堂｜思維升級：建構 AI 決策大腦.md` — 第一性原理／SAMR／個人品牌框架
- `創作庫/使用 AI Agent 自動剪輯教學影片 - Skills 福利大放送直播.md` — 第三節 AI 剪片亮點來源
- `SUPER決選佐證/研習回饋彙整.md` — 口碑佐證

## 目前進度
- [x] 擬定大綱 v2（四塊均衡、AI 剪片當亮點、對象＝媒體素養教師）
- [x] 更新 YT 訂閱數據（6.43 萬訂閱 / 452 部）
- [x] 專案初始化（CLAUDE.md、git、GitHub、Obsidian）
- [x] 打包自動剪輯工作流技能至 `skills/`（來源 2026-YouTube）
- [x] 產出範例科普片 `output/HK3R短影音五要素.mp4`（HK3R 五要素，115s，可重跑 build.py）
- [ ] 回填總觀看次數與觀看時數（YT Studio）
- [ ] 逐節展開詳細腳本（含互動、金句、講師備忘）
- [ ] 製作簡報（SOIL × 視覺規範）

## 最近更動紀錄
| 日期 | 變更摘要 | GDrive | Obsidian | GitHub |
|------|----------|--------|----------|--------|
| 2026-07-04 | 製作完成 HK3R 影片五要素科普影片（三師爸克隆旁白 + HyperFrames 動畫，放置於 hk3r_video/） | ✅ | ✅ | ✅ |
| 2026-07-04 | 專案初始化（CLAUDE.md + git + GitHub + Obsidian） | ✅ | ✅ | ✅ |
| 2026-06-01 | 建立大綱 v2，更新 YT 數據（6.43 萬訂閱 / 452 部） | ✅ | — | — |

## 資料夾結構
```
2026媒體素養_agent/
├── CLAUDE.md        # 本檔：專案設定與同步指引
├── handoff.md       # Agent 交接入口（接手先讀）
├── .gitignore
├── .env.example     # API 金鑰範本（自動剪輯技能用）
├── 研習大綱.md      # 研習大綱 v2（時間軸、五節內容、製作進度）
├── skills/          # 自動剪輯教學影片工作流（打包給老師安裝，來源 2026-YouTube）
│   ├── README.md    # 技能安裝指南
│   ├── smart-cut/、audio-to-srt/、video-editing-and-subtitles/
│   ├── short-video-workflow/、cover-image/
│   └── claude-youtube-video-workflow/、codex-youtube-video-workflow/
└── hk3r_video/      # HK3R 科普影片專案目錄
    ├── output_video.mp4  # 最終渲染成品 (1m 21.0s, 30fps, 三師爸配音)
    ├── index.html   # 由 GSAP 驅動的直式網頁動畫
    ├── DESIGN.md    # 品牌配色與字型規範
    ├── SCRIPT.md    # 5 段旁白腳本
    ├── STORYBOARD.md# 逐 Beat 分鏡規劃
    ├── generate_narration.py # 呼叫三師爸克隆語音生成旁白的 Python 腳本
    └── assets/      # 存放音訊與背景照片
```

## 三處同步指引

| 平台 | 路徑 / 位置 | 用途 |
|------|-------------|------|
| Google Drive | `G:\我的雲端硬碟\2026媒體素養_agent\` | 主要工作目錄，Claude Code 直接讀寫 |
| Obsidian | `2026媒體素養_agent/` | 第二大腦，佐證素材與草稿撰寫 |
| GitHub | `mathruffian-dot/media-literacy-2026` | 版本控制與備份（**公開 repo**，供其他老師 Agent 取用） |

## 工作注意事項
- 此資料夾位於 Google 雲端硬碟
- 跨裝置作業，每次開始前應先瀏覽現有檔案確認最新狀態
- 新增或修改檔案後，更新「資料夾結構」與「最近更動紀錄」
- 每次對話結束前，確認三處同步狀態是否一致
- 本專案名稱含 `_agent`，若有多 Agent 協作，使用 `handoff.md` 交接

## 跨裝置工作流程
1. **開工前**：瀏覽「目前進度」與「最近更動紀錄」
2. **工作中**：優先在 Google Drive 編輯，完成後同步至 Obsidian
3. **收工前**：更新「最近更動紀錄」，標記同步狀態
4. **跨電腦切換**：Google Drive 自動同步、Obsidian 確認 vault 同步、GitHub `git pull`
