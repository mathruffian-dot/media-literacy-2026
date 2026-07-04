# -*- coding: utf-8 -*-
"""check_env.py — 環境清點腳本（給接手的 Agent / 老師用）

用途：一跑就清點本專案所有功能需要的「程式」與「API 金鑰」，
逐項回報 ✅ 已具備 / ❌ 缺少，並附上安裝指令。
接手的 Agent 應先跑這支，再帶使用者把 ❌ 的項目一步步裝好。

用法：  python check_env.py
"""
import shutil, importlib, os, pathlib, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OK, NO = "✅", "❌"
missing = []


def has_cmd(name):
    return shutil.which(name) is not None


def has_pkg(mod):
    try:
        importlib.import_module(mod)
        return True
    except Exception:
        return False


def line(ok, label, hint=""):
    print(f"  {OK if ok else NO} {label}" + ("" if ok else f"   →  {hint}"))
    if not ok:
        missing.append(label)


def key_present(env, *files):
    if os.getenv(env):
        return True
    for f in files:
        if pathlib.Path(f).expanduser().exists():
            return True
    return False


print("=" * 60)
print(" 2026 媒體素養 × 短影音 — 環境清點 check_env.py")
print("=" * 60)

print("\n[1] 系統程式")
line(sys.version_info >= (3, 10), f"Python ≥ 3.10（目前 {sys.version.split()[0]}）", "安裝 python.org 3.10 以上")
line(has_cmd("ffmpeg"), "ffmpeg", "Win: winget install Gyan.FFmpeg ｜ Mac: brew install ffmpeg")
line(has_cmd("ffprobe"), "ffprobe（隨 ffmpeg 附帶）", "同 ffmpeg")
line(has_cmd("git"), "git", "git-scm.com")
line(has_cmd("gh"), "GitHub CLI (gh) 並已登入", "cli.github.com，裝好後 gh auth login")
line(has_cmd("node"), "Node.js（學生腳本入口部署用）", "nodejs.org（≥ v18）")
line(has_cmd("netlify"), "netlify-cli（學生腳本入口部署用）", "npm i -g netlify-cli")

print("\n[2] Python 套件")
line(has_pkg("edge_tts"), "edge-tts（免費中文旁白 TTS）", "pip install edge-tts")
line(has_pkg("playwright"), "playwright（HTML→圖片渲染）", "pip install playwright && python -m playwright install chromium")
line(has_pkg("auto_editor"), "auto-editor（smart-cut 去靜音）", "pip install auto-editor")
line(has_pkg("groq"), "groq（audio-to-srt 字幕）", "pip install groq")
line(has_pkg("openai"), "openai（cover-image 封面，Claude Code 才需要）", "pip install openai")

print("\n[3] API 金鑰")
line(key_present("GROQ_API_KEY", "~/.groq_api_key"),
     "Groq 金鑰（字幕 audio-to-srt / 學生腳本入口）",
     "console.groq.com 取 key，存到 ~/.groq_api_key，或設環境變數 GROQ_API_KEY")
line(key_present("OPENAI_API_KEY", "~/.openai.env"),
     "OpenAI 金鑰（cover-image 封面，選用）",
     "platform.openai.com（需 Individual 驗證），存到 ~/.openai.env")
line(bool(os.getenv("NETLIFY_AUTH_TOKEN")),
     "Netlify PAT（僅部署學生腳本入口時需要，選用）",
     "app.netlify.com/user/applications 產生 nfp_ token，export NETLIFY_AUTH_TOKEN")

print("\n" + "=" * 60)
if missing:
    print(f" 尚缺 {len(missing)} 項，請 Agent 帶使用者依上方指令安裝：")
    for m in missing:
        print(f"   - {m}")
    print("\n 註：API 金鑰類請使用者自行申請並存放於本機，切勿寫進 repo。")
else:
    print(" 全部具備，可以開始重建本專案功能。")
print("=" * 60)
