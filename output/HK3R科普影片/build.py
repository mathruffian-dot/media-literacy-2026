# -*- coding: utf-8 -*-
"""HK3R 短影音五要素 科普影片建置腳本
流程：HTML 投影片 → Playwright 截圖 PNG → edge-tts 旁白 → ffmpeg 合成 MP4
依 specs/03 社群科普影片視覺規範（teal/coral/paper/ink）。可重跑。
"""
import asyncio, subprocess, json, pathlib, sys
import edge_tts
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
ASSETS = HERE / "assets"
ASSETS.mkdir(exist_ok=True)

W, H = 1920, 1080
VOICE = "zh-TW-HsiaoChenNeural"   # 曉臻 女聲
RATE = "-5%"

# 配色（specs/03）
TEAL, CORAL, PAPER, INK, NEON = "#0E7C7B", "#E36414", "#FAF7EE", "#1A1A1A", "#FFD23F"
FONT = "'Microsoft JhengHei','微軟正黑體','PingFang TC',sans-serif"

SLIDES = [
    dict(kind="hook",
         narr="為什麼有些短影音，你手指一滑就忍不住停下來，有些卻三秒就被劃過去？差別不在運氣，而在骨架。而這個骨架，只有五個字母：H、K、3、R。",
         cap="一滑就停下來的短影音，都藏著這五個要素"),
    dict(kind="elem", letter="H", en="Hook", zh="鉤子", desc="前 3 秒抓住滑手", color=TEAL, idx=1,
         narr="第一個 H，Hook 鉤子。前三秒決定生死。用一個問句、一個反常識、或是不是A而是B的句型，先把觀眾牢牢釘在螢幕前。沒有鉤子，再好的內容也沒人看到。",
         cap="Hook｜前 3 秒用問句或反常識釘住觀眾"),
    dict(kind="elem", letter="K", en="Key", zh="關鍵比喻", desc="抽象概念變生活比喻", color=CORAL, idx=2,
         narr="第二個 K，Key 關鍵比喻。抽象的知識，大腦是拒絕的。把它比喻成生活裡熟悉的東西，像是把演算法比喻成餐廳點餐，觀眾一秒就懂，也才記得住。",
         cap="Key｜用生活比喻，讓抽象變好記"),
    dict(kind="elem", letter="R", en="Rationale", zh="機制", desc="講清楚為什麼會這樣", color=TEAL, idx=3,
         narr="接下來是三個 R。第一個，Rationale 機制。光說結論不夠，要說清楚它為什麼會這樣運作。講出背後的原理，觀眾才會信服，而不只是看個熱鬧。",
         cap="Rationale｜講清楚原理，觀眾才信服"),
    dict(kind="elem", letter="R", en="Reversal", zh="反轉", desc="打破預期，製造記憶點", color=CORAL, idx=4,
         narr="第二個 R，Reversal 反轉。在觀眾以為自己懂了的那一刻，丟一個意料之外的轉折。這一秒的驚訝，往往就是他們願意按下分享的理由。",
         cap="Reversal｜一個意外，就是被分享的理由"),
    dict(kind="elem", letter="R", en="Round-up", zh="結語", desc="收束成一句帶得走的話", color=TEAL, idx=5,
         narr="第三個 R，Round-up 結語。把整支影片收束成一句能帶得走的話，再留下一個下集預告，或一個明確的行動呼籲，讓觀眾知道下一步該做什麼。",
         cap="Round-up｜一句帶得走的話 + 行動呼籲"),
    dict(kind="outro",
         narr="H、K，再加上三個 R，合起來就是 HK3R。下次拍影片，照著這五步走。更重要的是，把它帶回教室，讓學生從只會看影片，變成會拆影片。",
         cap="H·K·R·R·R｜讓學生從「看影片」到「拆影片」"),
]


def dots(active):
    out = []
    for i in range(1, 6):
        c = CORAL if i == active else "transparent"
        b = CORAL if i == active else "#00000030"
        out.append(f'<span style="width:26px;height:26px;border-radius:50%;background:{c};border:3px solid {b};display:inline-block"></span>')
    return '<div style="display:flex;gap:20px">' + "".join(out) + "</div>"


def caption_bar(text):
    return (f'<div style="position:absolute;left:0;bottom:0;width:100%;height:150px;background:{INK};'
            f'display:flex;align-items:center;justify-content:center">'
            f'<div style="color:{PAPER};font-size:56px;font-weight:700;letter-spacing:1px">{text}</div></div>')


def frame(inner, bg):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>*{{margin:0;box-sizing:border-box}}'
            f'html,body{{width:{W}px;height:{H}px;overflow:hidden;font-family:{FONT};background:{bg}}}</style></head>'
            f'<body>{inner}</body></html>')


def html_for(s):
    if s["kind"] == "hook":
        inner = (f'<div style="position:absolute;top:130px;left:130px;color:{CORAL};font-size:52px;font-weight:700;letter-spacing:6px">短影音 · 五要素</div>'
                 f'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center">'
                 f'<div style="font-size:380px;font-weight:900;color:{NEON};letter-spacing:10px;line-height:1">HK3R</div>'
                 f'<div style="margin-top:30px;font-size:74px;font-weight:700;color:{PAPER}">拆解一支短影音的骨架</div></div>'
                 + caption_bar(s["cap"]))
        return frame(inner, INK)
    if s["kind"] == "outro":
        inner = (f'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{PAPER}">'
                 f'<div style="font-size:200px;font-weight:900;letter-spacing:8px">H · K · R · R · R</div>'
                 f'<div style="margin-top:40px;font-size:80px;font-weight:700">讓學生從「看影片」到「拆影片」</div>'
                 f'<div style="margin-top:50px;font-size:48px;color:{NEON};font-weight:700">媒體素養 × 短影音創作</div></div>'
                 + caption_bar(s["cap"]))
        return frame(inner, TEAL)
    # elem
    col = s["color"]
    left = (f'<div style="width:44%;height:100%;background:{col};display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;color:{PAPER}">'
            f'<div style="font-size:520px;font-weight:900;line-height:1">{s["letter"]}</div>'
            f'<div style="font-size:76px;font-weight:700;letter-spacing:4px">{s["en"]}</div></div>')
    right = (f'<div style="width:56%;height:100%;padding:0 120px;display:flex;flex-direction:column;justify-content:center">'
             f'<div style="font-size:52px;color:{col};font-weight:700">要素 {s["idx"]} / 5</div>'
             f'<div style="font-size:190px;font-weight:900;color:{INK};margin:10px 0 30px">{s["zh"]}</div>'
             f'<div style="font-size:72px;color:#4a4a4a;font-weight:500;line-height:1.4">{s["desc"]}</div>'
             f'<div style="margin-top:70px">{dots(s["idx"])}</div></div>')
    inner = f'<div style="display:flex;height:100%">{left}{right}</div>' + caption_bar(s["cap"])
    return frame(inner, PAPER)


async def tts_all():
    for i, s in enumerate(SLIDES):
        out = ASSETS / f"a{i}.mp3"
        c = edge_tts.Communicate(s["narr"], VOICE, rate=RATE)
        await c.save(str(out))
        print(f"[tts] a{i}.mp3")


def render_all():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(SLIDES):
            pg.set_content(html_for(s), wait_until="networkidle")
            pg.screenshot(path=str(ASSETS / f"s{i}.png"))
            print(f"[png] s{i}.png")
        b.close()


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return float(json.loads(r.stdout)["format"]["duration"])


def assemble():
    clips = []
    for i, s in enumerate(SLIDES):
        d = dur(ASSETS / f"a{i}.mp3") + 0.6
        clip = ASSETS / f"c{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", str(ASSETS / f"s{i}.png"),
                        "-i", str(ASSETS / f"a{i}.mp3"),
                        "-vf", f"scale={W}:{H},fps=30,format=yuv420p",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                        "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-t", f"{d:.2f}",
                        str(clip)], check=True)
        clips.append(clip)
        print(f"[clip] c{i}.mp4  {d:.1f}s")
    lst = ASSETS / "concat.txt"
    lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    out = HERE / "HK3R短影音五要素.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out)], check=True)
    print(f"[done] {out}  總長 {dur(out):.1f}s")


if __name__ == "__main__":
    print("== 1/3 TTS ==");    asyncio.run(tts_all())
    print("== 2/3 Render =="); render_all()
    print("== 3/3 Assemble =="); assemble()
