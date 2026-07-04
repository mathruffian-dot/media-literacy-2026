# 2026 媒體素養 × 短影音教學資源包

> 給教「媒體素養」的老師（教學對象為國中、國小學生）的一套**可被 AI Agent 自動重建**的教學工具包。
> 來源：三師爸（宋睿偉）「媒體素養與短影音創作教學實務研習」。

把這個 repo 交給你的 AI Agent（Claude Code / Codex / OpenCode…），它就能帶你把裡面的功能，一步一步在你自己的電腦上裝好、重建。

---

## 這個 repo 有什麼

| 內容 | 說明 |
|------|------|
| 🎬 自動剪輯生產線 `skills/` | 原始錄影 →（去靜音 → 字幕 → 封面 → 說明欄 → SEO）自動產出，七個技能 |
| 📱 學生短影音腳本入口 | `短影音腳本入口_製作指南.md`：學生填班級座號 → AI 生成符合教材規範的腳本 → 下載 |
| 🧪 HK3R 科普片範例 | `output/HK3R科普影片/`：短影音五要素（Hook·Key·3R）科普片，附可重跑腳本 |
| 📋 研習大綱 | `研習大綱.md`：短影音 5 段式黃金結構（＝HK3R）等硬規範 |

---

## 快速開始

### 你是老師（human）
1. 安裝 [Claude Code](https://claude.com/claude-code) 或其他 AI Agent。
2. 在這個資料夾啟動你的 Agent，跟它說：**「照 AGENTS.md 幫我把這個專案裝起來」**。
3. Agent 會先跑環境清點、回報你缺哪些程式與金鑰，再帶你一步步安裝。

### 你是 AI Agent
1. 讀 [`AGENTS.md`](AGENTS.md) — 你的行動流程入口。
2. 跑 `python check_env.py` — 逐項清點缺少的程式與 API 金鑰。
3. 依 [`handoff.md`](handoff.md) 帶使用者重建功能。

想先手動確認環境：
```bash
python check_env.py
```

---

## 相依資源
- 影片製作規範（社群影片 / 教學影片）：[`mathruffian-dot/claude-video-specs`](https://github.com/mathruffian-dot/claude-video-specs)
- 自動剪輯生產線來源：[`mathruffian-dot/2026-YouTube`](https://github.com/mathruffian-dot/2026-YouTube)

## 🔒 安全須知
- **本 repo 不含任何 API 金鑰**。Groq / OpenAI 金鑰請自行申請，放在本機（`~/.groq_api_key`、`~/.openai.env`）或雲端環境變數。
- 請勿把金鑰、學生個資、個人肖像照提交進 repo（`.gitignore` 已預設排除常見金鑰檔與媒體大檔）。

## 授權與致謝
教學規範參考 SOIL 教學心法（李俊儀教授）、林長揚簡報原則。影片素材請遵守各自授權（CC0 / Unsplash 等）。
