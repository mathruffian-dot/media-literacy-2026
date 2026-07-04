# skills — 自動剪輯教學影片工作流（打包給老師安裝）

> 這是「**原始錄影 → AI 接力 → 剪好的影片 + 字幕 + 封面 + 說明欄 + SEO**」自動化生產線。
> 來源 repo：[`mathruffian-dot/2026-YouTube`](https://github.com/mathruffian-dot/2026-YouTube)（本資料夾為精簡打包版，不含影片素材與金鑰）。
> **接手的 Agent：先讀本檔，再依「安裝步驟」逐條驗證，缺什麼主動幫使用者裝。**

---

## 管線總覽

```
raw/<影片代號>/原始.mp4
   ├─ smart-cut                    → auto-editor 去靜音、剪口播
   ├─ audio-to-srt                 → Groq Whisper 轉乾淨 SRT + 純文字
   ├─ video-editing-and-subtitles  → 字幕校潤、燒錄收尾
   ├─（可選）short-video-workflow  → 切 ≤2 分鐘短片、加字幕與結尾字卡
   ├─ cover-image                  → gpt-image-2 生封面
   └─ 由 workflow 技能編排 →       output/<標題>/（影片+字幕+txt+封面+metadata）
```

## 七個技能

| 技能 | 作用 | 相依 | 需金鑰 |
|------|------|------|--------|
| `smart-cut` | 智能剪口播（去靜音） | auto-editor, ffmpeg | — |
| `audio-to-srt` | 語音轉 SRT 字幕 | groq (Python SDK) | `~/.groq_api_key` ✅ |
| `video-editing-and-subtitles` | 字幕校潤 + 燒錄 | ffmpeg | — |
| `short-video-workflow` | 短片切段 + 字卡 | ffmpeg | — |
| `cover-image` | 生封面圖 | openai (Python SDK) | `~/.openai.env`（僅 Claude Code 需要） |
| `claude-youtube-video-workflow` | Claude Code 總控編排 | 以上技能 | — |
| `codex-youtube-video-workflow` | Codex 總控編排（內建生圖） | 以上技能 | — |

## 安裝步驟（接手 Agent 照做）

**1. 系統前置**
```bash
pip install auto-editor groq openai
ffmpeg -version                  # Win: winget install Gyan.FFmpeg / Mac: brew install ffmpeg
python -m auto_editor --version  # exit code 255 屬正常，看到版本號即可
```

**2. API 金鑰（不在本 repo，需自行建立）**
- Groq（audio-to-srt 必填）：到 console.groq.com 取 key，存到 `~/.groq_api_key`（整檔就是 key 字串）。
- OpenAI（cover-image，僅 Claude Code 需要）：需 Individual 驗證才能用 gpt-image-2，存到 `~/.openai.env`（格式 `OPENAI_API_KEY=sk-...`）。Codex 用內建生圖，免此 key。

**3. 個人化（每位老師必改）**
- `audio-to-srt/references/vocabulary.md`、`audio-to-srt/scripts/apply_vocab.py` — 換成你自己的專有名詞與常聽錯字。
- `cover-image` / workflow 內引用的人物照與頻道風格 — 換成你自己的（人物照請勿放進公開 repo）。
- workflow SKILL.md 內的頻道/學校名稱、repo 連結 — 全文取代成你的。

**4. 驗證跑通**
- 把一支短影片放進 `raw/測試/原始.mp4`，對 Agent 說：「使用 claude-youtube-video-workflow 處理 raw/測試」。

## 使用注意
- **先剪後轉**：一定先 smart-cut 再 audio-to-srt，否則字幕時間碼會錯位。
- smart-cut `--threshold`（預設 0.06）與 `--margin` 可依講話停頓多寡微調（見 `smart-cut/SKILL.md`）。
- 螢幕錄影常是 VFR，`smart_cut.py` 已內建自動轉 CFR 防黑幀。
- 影片/音訊大檔與 `.env` 已由本專案 `.gitignore` 排除，不會進 git。

## 完整文件
更詳盡的設定、參數、常見問題見來源 repo 的 `SETUP.md`：[mathruffian-dot/2026-YouTube](https://github.com/mathruffian-dot/2026-YouTube)。
