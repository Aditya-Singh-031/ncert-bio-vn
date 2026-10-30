"""Generate looping teaching videos from approved diagram frames with Veo 3.1 (Gemini API).

Usage (from pipeline_source/, with GEMINI_API_KEY set in the environment):
  python src/video_gen.py --dry-run               # show cost, no API call
  python src/video_gen.py --scenes s04            # one scene first
  python src/video_gen.py                         # all scenes in specs/ch8_motion.json
"""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = os.getenv("VEO_MODEL", "veo-3.1-generate-preview")
RATE = float(os.getenv("VEO_USD_PER_SEC", "0.40"))   # check ai.google.dev/gemini-api/docs/pricing
SECS = 8
ATTEMPTS = 2
DRIFT_MAX = 14.0   # heuristic: mean abs pixel diff (0-255) allowed between source frame and clip end frame
NEG = ("text, letters, words, labels, captions, subtitles, watermark, logo, new objects, "
       "extra organelles, camera movement, zoom, scene cut, morphing shapes")
STYLE = ("Flat 2D educational vector animation in the exact palette and layout of the first frame. "
         "Static camera, no zoom. ")


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


def build_prompt(motion):
    return (STYLE + motion + " Everything ends exactly where it started so the clip loops. "
            "No text appears or changes. No sound.")


def run(cmd):
    subprocess.run(cmd, check=True)


def transcode(raw, out):
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-an",
         "-vf", "scale=1920:1080:flags=lanczos,fps=25",
         "-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0", "-pix_fmt", "yuv420p", str(out)])


def probe(path, entries):
    r = subprocess.run(["ffprobe", "-v", "error", *entries, "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    return r.stdout.strip()


def check(out, png):
    """Automated gate. 'ok' False means send to human review / regenerate."""
    from PIL import Image, ImageChops, ImageStat
    res = {"audio_stream": bool(probe(out, ["-select_streams", "a", "-show_entries", "stream=codec_name"])),
           "size": probe(out, ["-select_streams", "v:0", "-show_entries", "stream=width,height"]),
           "duration": probe(out, ["-show_entries", "format=duration"])}
    tmp = Path(out).with_suffix(".end.png")
    run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1", "-i", str(out), "-frames:v", "1", str(tmp)])
    a = Image.open(png).convert("RGB").resize((960, 540))
    b = Image.open(tmp).convert("RGB").resize((960, 540))
    res["end_frame_drift"] = round(sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3, 2)
    tmp.unlink(missing_ok=True)
    res["ok"] = (not res["audio_stream"] and res["size"] == "1920,1080" and res["end_frame_drift"] <= DRIFT_MAX)
    return res


def generate_raw(client, types, png_bytes, prompt, raw_path):
    img = types.Image(image_bytes=png_bytes, mime_type="image/png")
    cfg = types.GenerateVideosConfig(aspect_ratio="16:9", resolution="1080p", duration_seconds=SECS,
                                     last_frame=img, negative_prompt=NEG)
    op = client.models.generate_videos(model=MODEL, prompt=prompt, image=img, config=cfg)
    while not op.done:
        time.sleep(10)
        op = client.operations.get(op)
    vids = getattr(op.response, "generated_videos", None) if op.response else None
    if not vids:
        raise RuntimeError(f"no video returned (filtered or failed): {getattr(op, 'error', None)}")
    client.files.download(file=vids[0].video)
    vids[0].video.save(str(raw_path))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenes", nargs="*")
    ap.add_argument("--motion", default=str(ROOT / "specs" / "ch8_motion.json"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    motion = json.load(open(a.motion))
    sids = a.scenes or sorted(motion)
    vdir = ROOT / "assets" / "video"
    (vdir / "raw").mkdir(parents=True, exist_ok=True)
    (ROOT / "build").mkdir(exist_ok=True)

    todo = []
    for sid in sids:
        png = ROOT / "assets" / f"{sid}.png"
        prompt = build_prompt(motion[sid])
        key = sha((MODEL + prompt + sha(png.read_bytes())).encode())
        meta = vdir / f"{sid}.json"
        cached = meta.exists() and (vdir / f"{sid}.webm").exists() and json.load(open(meta)).get("key") == key
        if cached and not a.force:
            print(f"{sid}: cached, skipped")
            continue
        todo.append((sid, png, prompt, key))

    print(f"{len(todo)} clip(s) x {SECS}s x ${RATE}/s = ${len(todo) * SECS * RATE:.2f} per attempt (model {MODEL})")
    if a.dry_run or not todo:
        return

    from google import genai
    from google.genai import types
    client = genai.Client()   # reads GEMINI_API_KEY from the environment

    for sid, png, prompt, key in todo:
        for attempt in range(1, ATTEMPTS + 1):
            try:
                raw = vdir / "raw" / f"{sid}.mp4"
                out = vdir / f"{sid}.webm"
                print(f"{sid}: generating (attempt {attempt}) ...")
                generate_raw(client, types, png.read_bytes(), prompt, raw)
                transcode(raw, out)
                qa = check(out, png)
                cost = SECS * RATE
                with open(ROOT / "build" / "cost_log.jsonl", "a") as f:
                    f.write(json.dumps({"scene": sid, "model": MODEL, "usd": cost, "attempt": attempt, "qa": qa}) + chr(10))
                json.dump({"key": key, "model": MODEL, "prompt": prompt, "qa": qa, "review": "pending"},
                          open(vdir / f"{sid}.json", "w"), indent=1)
                print(f"{sid}: {'OK' if qa['ok'] else 'NEEDS REVIEW'} {qa}")
                if qa["ok"]:
                    break
            except Exception as e:
                print(f"{sid}: attempt {attempt} failed: {e}", file=sys.stderr)
                time.sleep(5)


if __name__ == "__main__":
    main()
