# AGENTS.md — 其他老師的 Agent 入口

> 你是一位老師的 AI Agent，剛拿到這個公開 repo。
> 這是一個**媒體素養 × 短影音**教學資源包，目標是讓你**帶著使用者，一步一步把本專案的功能在他的電腦上重建起來**。
> 服務對象：教媒體素養的老師；他們的教學對象是國中、國小學生。
>
> **請照下面 5 階段進行。每一步都先問過使用者、每完成一個里程碑就回報，不要悶頭做。**

---

## 階段 0 — 讀懂專案（先讀這三份）
1. `AGENTS.md`（本檔）— 你的行動流程。
2. `handoff.md` — 完整交接：專案目的、已完成內容、待辦。
3. `CLAUDE.md` + `研習大綱.md` — 研習內容與短影音 5 段式（HK3R）硬規範。

## 階段 1 — 環境清點（最重要）
跑一次清點腳本，它會逐項回報缺哪些**程式**與**API 金鑰**：
```bash
python check_env.py
```
把 ❌ 的項目整理給使用者，**主動帶他一項一項安裝**（腳本已附每項的安裝指令）。全部 ✅ 才進下一階段。

## 階段 2 — 安裝三個影片技能
本 repo 內含的自動剪輯工作流在 `skills/`，安裝步驟見 `skills/README.md`：
```bash
pip install auto-editor groq openai        # + ffmpeg + ~/.groq_api_key
```
另外兩個影片技能（社群影片 / 教學影片）來自獨立 repo，依 `handoff.md` 指示安裝：
```bash
git clone https://github.com/mathruffian-dot/claude-video-specs.git
bash install/check_env.sh && bash install/install_all.sh
```

## 階段 3 — 重建可交付的功能
本專案已示範三種產出，帶使用者挑要重建哪些：
| 功能 | 位置 / 做法 | 需要 |
|------|------------|------|
| HK3R 科普影片（範例） | `output/HK3R科普影片/build.py`，`python build.py` 重生 | playwright, edge-tts, ffmpeg |
| 自動剪輯 YouTube 生產線 | `skills/`（原始錄影 → 剪輯 → 字幕 → 封面 → 文案） | 見階段 2 |
| 學生短影音腳本入口 | `短影音腳本入口_製作指南.md`（Netlify + Groq Function 完整做法） | node, netlify-cli, Groq 金鑰, Netlify PAT |

## 階段 4 — 回報與交接
- 每完成一項就回報使用者。
- 更新 `handoff.md` 的「目前做到哪」與「最後更新（時間 + 你是誰）」。

---

## 🔒 安全鐵則（公開 repo）
- **絕不把任何 API 金鑰寫進 repo**。金鑰一律放本機（`~/.groq_api_key`、`~/.openai.env`）或雲端環境變數（Netlify `--secret`）。
- `.gitignore` 已排除 `groq_api_key.txt`、`*api_key*`、`.env`、`*.key` 等；提交前務必再確認沒有金鑰被 staged。
- 個人肖像照、學生個資不進 repo。
