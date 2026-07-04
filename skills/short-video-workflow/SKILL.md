---
name: short-video-workflow
description: 從已剪過的長片（cut.mp4 + .srt）擷取亮點片段，組成 ≤2 分鐘的短片。當使用者要『剪 short / 做短片 / 抓亮點 / 剪精華 / 做 YouTube Shorts』時請使用此 Skill。會依字幕亮點偵測產 3 個候選版本（痛點型/好奇型/承諾型），等使用者選；也接受使用者直接給時間碼或描述覆寫。輸出走 `output/<短片標題> [Claude|Codex] (Short)/`，含 mp4/srt/txt/cover/metadata 五個檔。
---

# short-video-workflow：長片亮點 → ≤2 分鐘短片

## 何時觸發
使用者說：
- 「幫我剪一個 short / 短片」
- 「把這支影片的亮點抓出來做精華」
- 「做一個 2 分鐘的版本」
- 「用 X 段時間碼剪一個短片」

## 前置條件
**必須有**已跑完 `claude-youtube-video-workflow` 或 `codex-youtube-video-workflow` 的長片產物：
- `working/<video-id>/<video-id>.cut.mp4`（剪口播完的版本）
- `working/<video-id>/<video-id>.srt`（清字完的字幕，時間碼對齊 cut.mp4）

如果這兩個檔案還沒生，先跑長片總控流程。

---

## 規格（來自使用者拍板）

| 項目 | 設定 |
|------|------|
| 影音格式 | **16:9 維持原片**（不轉直式 9:16） |
| 封面尺寸 | **16:9**（與長片共用樣板） |
| 輸出資料夾 | **`output/<短片標題> [Claude|Codex] (Short)/`** |
| 短片時長上限 | **≤ 120 秒** |
| 開頭 Hook | **≤ 5 秒** |
| 候選版本數 | **3 個**（不同 hook 策略） |
| 內部檔案 | 5 個：`<標題>.mp4 / .srt / .txt / cover.png / metadata.md` |

---

## 流程

### Step 1：讀入並確認
- 讀 `working/<video-id>/<video-id>.srt`，理解全片內容與時間碼
- 確認 `cut.mp4` 存在
- 取得長片總時長（ffprobe）

### Step 2：亮點偵測（自動模式）

依以下「亮點偵測檢核表」掃過全部字幕段，標記候選：

| 亮點類型 | 字幕特徵範例 |
|---------|--------------|
| **痛點宣告** | 「每年都要⋯」「最痛苦的⋯」「沒有人喜歡⋯」 |
| **反問句** | 「你還在⋯嗎？」「為什麼⋯？」 |
| **數字承諾** | 「3 步驟」「5 分鐘」「一鍵⋯」 |
| **強斷言** | 「只要⋯就⋯」「最⋯的⋯」「再也不⋯」 |
| **轉折揭密** | 「但其實⋯」「結果⋯」「沒想到⋯」 |
| **價值結算** | 「省了⋯」「賺到⋯」「換來⋯」 |
| **行動指令** | 「你只要⋯」「你可以⋯」 |

把每段給一個 0–3 的亮點分數，記在工作筆記。

### Step 3：組三個候選版本

每個版本走 **三幕結構**：

```
[幕 1] Hook (≤ 5s)：選一段最強的亮點當開頭，抓住注意力
[幕 2] Body (60–100s)：3–6 段邏輯連貫的內容，串起 hook 的承諾
[幕 3] CTA / 收尾 (5–15s)：呼應 hook，給一個記憶點或行動
```

三個版本走**不同 hook 策略**：

| 版本 | Hook 策略 | 適合情境 |
|------|-----------|---------|
| A | **痛點型** Hook（從「你還在⋯」開頭）| 觀眾對痛點有共鳴 |
| B | **好奇型** Hook（從「沒想到⋯」「其實⋯」開頭）| 想做病毒傳播 |
| C | **承諾型** Hook（從「3 分鐘搞定⋯」開頭）| 工具教學類最強 |

**邏輯連貫性檢核**：每個版本內，相鄰段落必須在語意上能接上（前一段結尾 → 下一段開頭不能斷裂）。如果語意接不上，補一段過場字幕或重選。

### Step 4：寫候選清單，等使用者挑

寫到 `working/<video-id>/shorts-candidates.md`：

```markdown
# 短片候選 — <video-id>

## 版本 A：痛點型
- **時長**：1:42
- **時間碼**：00:00:08.500-00:00:13.200, 00:00:45.100-00:01:30.800, 00:01:55.000-00:02:05.000
- **三幕劇本**：
  - Hook：「你還在手動填課程計畫嗎？」（4.7s）
  - Body：示範 3 個步驟讓 Claude 自動填表（45.7s）
  - CTA：「再也不用熬夜寫課程計畫」（10.0s）
- **預估亮點命中率**：8/10

## 版本 B：好奇型
（同上格式）

## 版本 C：承諾型
（同上格式）
```

回報三版給使用者，**停下等使用者選編號 A/B/C**，或：
- 「我自己給你時間碼」→ 跳到 step 5 用使用者給的時間碼
- 「再生 3 版」→ 重跑 step 3，調整 hook 策略

### Step 5：使用者拍板後 — 切片+組片

呼叫包裝腳本：

```bash
python skills/short-video-workflow/scripts/clip_cut.py \
  --input-mp4 "working/<video-id>/<video-id>.cut.mp4" \
  --input-srt "working/<video-id>/<video-id>.srt" \
  --segments "00:00:08.500-00:00:13.200,00:00:45.100-00:01:30.800,00:01:55.000-00:02:05.000" \
  --out-dir "working/<video-id>/short-tmp/"
```

腳本會產出：
- `short-tmp/short.mp4`（ffmpeg trim+concat，重新編碼確保乾淨切點）
- `short-tmp/short.srt`（依新時間軸重編字幕）
- `short-tmp/short.txt`（純文字稿）

跑完後**確認時長 ≤ 120 秒**（ffprobe），超過就回 step 4 重組。

### Step 6：新增結尾字卡與燒錄字幕

1. **添加結尾字卡**：
在影片的最尾端放置一個 3 秒的「詳細影片請看留言」字卡。
呼叫包裝腳本：
```bash
python skills/short-video-workflow/scripts/add_end_card.py \
  --input-mp4 "working/<video-id>/short-tmp/short.mp4" \
  --output-mp4 "working/<video-id>/short-tmp/short_with_card.mp4"
```
這會生成 `short-tmp/short_with_card.mp4`（總長度增加 3 秒，顯示深海軍藍 `#0A192F` 背景、霓虹亮藍字白色描邊的字卡，包含無聲音軌）。

2. **燒錄字幕**：
使用 `burn_subtitles.py` 將 `.srt` 字幕燒錄到影片中：
```bash
python skills/short-video-workflow/scripts/burn_subtitles.py \
  "working/<video-id>/short-tmp/short_with_card.mp4" \
  "working/<video-id>/short-tmp/short.srt" \
  "working/<video-id>/short-tmp/short_subtitled.mp4"
```
這會產出燒錄好字幕並帶有結尾字卡的影片 `short-tmp/short_subtitled.mp4`。

### Step 7：給短片定 3 個標題，等使用者挑

短片標題不一定等於長片標題；通常更聳動、更短。
依前述內容生 3 個候選寫到 `working/<video-id>/short-titles.md`，停下等使用者挑（不要 10 個，短片不需要那麼多）。

### Step 8：使用者選定短片標題後 — 建資料夾

- 標題清洗（去除 `？！：／＼?!:/\\<>|"*`）
- 建 `output/<短片標題> [Claude] (Short)/`（Claude）或 `output/<短片標題> [Codex] (Short)/`（Codex）
- 搬移並重新命名檔案到輸出資料夾：
  - 把 `short_with_card.mp4` 改名為 `<短片標題>.mp4`（乾淨版）
  - 把 `short_subtitled.mp4` 改名為 `<短片標題>_字幕版.mp4`（燒錄字幕版）
  - 把 `short.srt` 改名為 `<短片標題>.srt`
  - 把 `short.txt` 改名為 `<短片標題>.txt`

### Step 9：產封面（沿用長片封面 SOP）

**生封面前 SOP（缺一不可）**：
1. `Read assets/style/reference-thumbnails.png`
2. `Read assets/style/cover-style.md`
3. `Read assets/persona/三師爸人物形象照.png`
4. 依影片主角決定主色：Claude=橘 / Codex=藍 / 兩者並用=橘+藍

**短片封面額外要求**：
- 標題用**最短最聳動**的版本（封面標題可以比 YouTube 標題更精煉）
- 加「SHORT」或「精華」字樣小貼紙作識別（選擇性）
- 16:9 尺寸與長片同樣板

呼叫方式：
- **Claude Code**：`python skills/cover-image/draw.py "<prompt>" --edit "assets/persona/三師爸人物形象照.png" --size 1536x1024 --quality low --name cover --outdir "output/<標題> [Claude] (Short)/"`
- **Codex**：用內建 Image2，不呼叫 draw.py

### Step 10：寫 metadata（短片版本）

`metadata.md` 結構**與長片不同**（短片有自己的玩法）：

1. **YouTube 短描述**（≤ 150 字，前 50 字最關鍵）
2. **Hashtag 帶**：開頭 3 個 → `#Shorts #<頻道主題>` 一定要有
3. **社群貼文**（IG Reels、TikTok 各一版本，比長片更短更挑釁）
4. **SEO 關鍵字**：
   - 主關鍵字（3–5 個）
   - 長尾（3–5 個）
   - **YouTube 標籤欄位（直接複製）**：半形逗號分隔，**最後加 `Shorts,短影片` 兩個必備標籤**
5. **上架前 checklist**：標題 ≤ 40 字、封面、字幕、`#Shorts` 在標題或描述、發布時段建議

### Step 11：自我檢查清單

跑完後逐項確認：
- [ ] 資料夾名結尾有 ` [Claude] (Short)` 或 ` [Codex] (Short)` 後綴
- [ ] 影片時長 ≤ 120 秒（ffprobe 確認）
- [ ] 開頭 5 秒內出現 hook 字幕
- [ ] 5 個檔案齊全
- [ ] cover.png 主色對應 AI 主角（橘 / 藍）
- [ ] metadata.md 含 `#Shorts` 標籤
- [ ] HANDOFF.md 已更新本支短片狀態

### Step 12：更新 HANDOFF.md

紀錄：
- 短片標題
- 來源長片 video-id
- 時間碼組合
- 選用的 hook 策略（A/B/C 或 user-defined）
- 輸出路徑

---

## Override 模式：使用者直接給時間碼或描述

使用者可以在 step 2 之前直接指定，例如：
- 「用 00:00:05–00:00:15、00:01:20–00:02:00 這兩段組」→ 跳到 step 5
- 「我要剪『Claude 怎麼操作 + 結果展示』那兩段」→ 你 AI 從 SRT 找出對應時間碼，給使用者確認後跳 step 5

## 踩坑

- **時間碼必須對齊 `cut.mp4` 不是 `raw/`**：對原始檔的時間碼跟字幕對不上。
- **重新編碼 vs stream copy**：短片切點通常不在 keyframe，用 stream copy（`-c copy`）會出現黑畫面；本 Skill 一律走重新編碼。
- **音訊 fade in/out**：`clip_cut.py` 預設不加 fade；想要 0.05s 軟切點可在 step 5 加 `--audio-fade 0.05`。
- **段落數別超過 8 段**：太多碎片會讓觀感不連貫；2 分鐘 3–6 段最舒服。
- **不要切到一句話中間**：選時間碼時對齊字幕段落邊界，否則會「切到一半」。
- **YouTube Shorts 規則**：影片 ≤ 60 秒會自動進 Shorts feed，60–180 秒則是「短片」但不一定進 Shorts feed。本 Skill 預設 ≤ 120 秒比較通用。
- **垂直版本若需要**：本 Skill 規格固定 16:9；要 9:16 走另開 task，加 `--aspect 9:16` 並在 ffmpeg 後加 crop filter。

---

## 檔案結構

```
skills/short-video-workflow/
├── SKILL.md
└── scripts/
    ├── clip_cut.py        # ffmpeg 切片+組片+SRT 重編
    ├── add_end_card.py    # 結尾添加 3 秒「詳細影片請看留言」字卡
    └── burn_subtitles.py  # 將 srt 字幕燒錄進 mp4 影片
```

## 與其他 Skill 的關係
- **依賴**：`smart-cut` + `audio-to-srt`（已產 cut.mp4 + srt）
- **共用**：`cover-image` SOP、`assets/style/cover-style.md`、`assets/persona/`
- **平行**：與 `claude-youtube-video-workflow` / `codex-youtube-video-workflow` 是兄弟關係
