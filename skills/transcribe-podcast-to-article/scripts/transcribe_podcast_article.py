#!/usr/bin/env python3
"""Transcribe or format podcast audio into article-style Markdown.

The script is intentionally conservative: it creates a strong first-pass draft
and leaves final editorial judgment to the agent using the skill.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
DEFAULT_PROMPT = (
    "这是一段中文播客转写。请使用简体中文，保留原话，省略无意义的语气词和重复口头禅。"
    "遇到口头解释拼写或字形时，只写最终词语。不要转写背景音乐或歌曲歌词。"
    "请尽量添加自然的中文标点。"
)


def parse_time(value: str) -> float:
    parts = value.strip().split(":")
    if not parts or any(not p for p in parts):
        raise ValueError(f"Invalid time: {value}")
    nums = [float(p) for p in parts]
    if len(nums) == 1:
        return nums[0]
    if len(nums) == 2:
        return nums[0] * 60 + nums[1]
    if len(nums) == 3:
        return nums[0] * 3600 + nums[1] * 60 + nums[2]
    raise ValueError(f"Invalid time: {value}")


def parse_chapters(path: Path | None) -> list[tuple[float, str]]:
    if path is None:
        return [(0.0, "正文")]
    chapters: list[tuple[float, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$", line)
        if not match:
            raise ValueError(f"Chapter line must be '<time> <title>': {line}")
        chapters.append((parse_time(match.group(1)), match.group(2).strip()))
    return chapters or [(0.0, "正文")]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ensure_command(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"Missing required command: {name}")


def original_audio_path(args: argparse.Namespace) -> Path:
    input_audio = Path(args.input_audio).expanduser().resolve()
    if not input_audio.exists():
        raise SystemExit(f"Audio file not found: {input_audio}")
    return input_audio


def prepare_audio(args: argparse.Namespace, temp_dir: Path) -> Path:
    ensure_command(args.ffmpeg)
    input_audio = original_audio_path(args)

    if args.max_minutes is None and args.skip_initial_seconds == 0:
        return input_audio

    out = temp_dir / "transcription_input.wav"
    cmd = [
        args.ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
    ]
    if args.skip_initial_seconds:
        cmd += ["-ss", str(args.skip_initial_seconds)]
    cmd += ["-i", str(input_audio)]
    if args.max_minutes is not None:
        cmd += ["-t", str(args.max_minutes * 60)]
    cmd += ["-ac", "1", "-ar", "16000", str(out)]
    run(cmd)
    return out


def transcribe_audio(audio: Path, args: argparse.Namespace) -> dict[str, Any]:
    try:
        import mlx_whisper  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "Missing Python package mlx-whisper. Install in a local venv with: "
            "python3 -m pip install mlx-whisper"
        ) from exc

    return mlx_whisper.transcribe(
        str(audio),
        path_or_hf_repo=args.model,
        language=args.language,
        task="transcribe",
        verbose=False,
        temperature=(0.0, 0.2, 0.4),
        condition_on_previous_text=False,
        hallucination_silence_threshold=1.0,
        initial_prompt=args.prompt,
    )


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
    return slug or "value"


def compact_float(value: float | None) -> str:
    if value is None:
        return "full"
    return f"{value:g}"


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12]


def cache_paths(input_audio: Path, args: argparse.Namespace) -> tuple[Path, Path]:
    cache_dir = Path(args.asr_cache_dir).expanduser().resolve()
    model = slugify(args.model)
    language = slugify(args.language)
    skip = compact_float(args.skip_initial_seconds)
    max_minutes = compact_float(args.max_minutes)
    stem = slugify(input_audio.stem)
    name = f"{stem}.{model}.{language}.skip{skip}.max{max_minutes}.{prompt_hash(args.prompt)}"
    return cache_dir / f"{name}.asr.json", cache_dir / f"{name}.meta.json"


def audio_fingerprint(input_audio: Path) -> dict[str, Any]:
    stat = input_audio.stat()
    return {
        "path": str(input_audio),
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def expected_cache_metadata(input_audio: Path, args: argparse.Namespace) -> dict[str, Any]:
    return {
        "source_audio": audio_fingerprint(input_audio),
        "asr_backend": "mlx-whisper",
        "model": args.model,
        "language": args.language,
        "skip_initial_seconds": args.skip_initial_seconds,
        "max_minutes": args.max_minutes,
        "prompt_sha256": hashlib.sha256(args.prompt.encode("utf-8")).hexdigest(),
    }


def cache_metadata_matches(metadata: dict[str, Any], expected: dict[str, Any]) -> bool:
    return all(metadata.get(key) == value for key, value in expected.items())


def normalize_segment_times(result: dict[str, Any], offset: float) -> dict[str, Any]:
    if offset == 0:
        result.setdefault("_podcast_transcript", {})["timeline"] = "absolute"
        return result

    for seg in result.get("segments") or []:
        for key in ("start", "end"):
            if key in seg:
                seg[key] = float(seg[key]) + offset
    result.setdefault("_podcast_transcript", {})["timeline"] = "absolute"
    result["_podcast_transcript"]["skip_initial_seconds"] = offset
    return result


def load_asr_cache(input_audio: Path, args: argparse.Namespace) -> dict[str, Any] | None:
    if not args.asr_cache_dir:
        return None

    asr_path, meta_path = cache_paths(input_audio, args)
    if not asr_path.exists() or not meta_path.exists():
        return None

    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    expected = expected_cache_metadata(input_audio, args)
    if not cache_metadata_matches(metadata, expected):
        return None

    print(f"asr_cache_hit={asr_path}", file=sys.stderr)
    return json.loads(asr_path.read_text(encoding="utf-8"))


def save_asr_cache(input_audio: Path, args: argparse.Namespace, result: dict[str, Any]) -> None:
    if not args.asr_cache_dir:
        return

    asr_path, meta_path = cache_paths(input_audio, args)
    asr_path.parent.mkdir(parents=True, exist_ok=True)
    asr_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    metadata = expected_cache_metadata(input_audio, args)
    metadata.update(
        {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "asr_json": str(asr_path),
        }
    )
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"asr_cache_saved={asr_path}", file=sys.stderr)


def load_result(args: argparse.Namespace, temp_dir: Path) -> dict[str, Any]:
    if args.from_json:
        return json.loads(Path(args.from_json).read_text(encoding="utf-8"))

    input_audio = original_audio_path(args)
    cached = load_asr_cache(input_audio, args)
    if cached is not None:
        return cached

    audio = prepare_audio(args, temp_dir)
    result = transcribe_audio(audio, args)
    result = normalize_segment_times(result, args.skip_initial_seconds)
    save_asr_cache(input_audio, args, result)
    return result


def cjk_count(text: str) -> int:
    return len(re.findall(r"[\u3400-\u9fff]", text))


def looks_like_music(text: str, start: float, language: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if re.fullmatch(r"[啦 laLA。,.，\s]+", stripped):
        return True
    latin_words = re.findall(r"[A-Za-z]{2,}", stripped)
    if language.lower().startswith("zh") and start < 90 and cjk_count(stripped) == 0 and len(latin_words) >= 5:
        return True
    return False


TERM_PATTERNS = [
    (re.compile(r"P\s*[，,、]?\s*A\s*[，,、]?\s*R\s*[，,、]?\s*A", re.I), "PARA"),
    (re.compile(r"C\s*[，,、]?\s*O\s*[，,、]?\s*D\s*[，,、]?\s*E", re.I), "CODE"),
    (re.compile(r"B\s*[，,、]?\s*G\s*[，,、]?\s*M", re.I), "BGM"),
    (re.compile(r"X\s*[，,、]?\s*Y", re.I), "XY"),
]

DEFAULT_REPLACEMENTS = {
    "写影Melody": "携隐 Melody",
    "携影Melody": "携隐 Melody",
    "谐影Melody": "携隐 Melody",
    "卡曼卡片盒": "卢曼卡片盒",
    "鲁曼卡片盒": "卢曼卡片盒",
}


def parse_replacements(values: list[str]) -> dict[str, str]:
    replacements = dict(DEFAULT_REPLACEMENTS)
    for value in values:
        if "=" not in value:
            raise SystemExit(f"--replace must be OLD=NEW, got: {value}")
        old, new = value.split("=", 1)
        replacements[old] = new
    return replacements


def clean_text(text: str, replacements: dict[str, str]) -> str:
    text = text.strip()
    for pattern, replacement in TERM_PATTERNS:
        text = pattern.sub(replacement, text)
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"(?<![A-Za-z])(?:uh+|um+|erm+|well)(?![A-Za-z])[,，。.\s]*", "", text, flags=re.I)
    text = re.sub(r"^[嗯呃啊]+[，,。.\s]*", "", text)
    text = re.sub(r"(?:那个){2,}[，,。.\s]*", "", text)
    text = re.sub(r"(?:这个){2,}[，,。.\s]*", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ,", ",").replace(" 。", "。").strip()
    return text


def collect_segments(result: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    replacements = parse_replacements(args.replace)
    segments: list[dict[str, Any]] = []
    raw_segments = result.get("segments") or []
    if not raw_segments and result.get("text"):
        raw_segments = [{"start": 0, "end": 0, "text": result["text"]}]

    metadata = result.get("_podcast_transcript") or {}
    offset = 0 if args.from_json or metadata.get("timeline") == "absolute" else args.skip_initial_seconds
    for seg in raw_segments:
        start = float(seg.get("start", 0)) + offset
        text = clean_text(str(seg.get("text", "")), replacements)
        if looks_like_music(text, start, args.language):
            continue
        if not text:
            continue
        segments.append({"start": start, "text": text})
    return segments


def heading(title: str) -> str:
    title = re.sub(r"^\d{1,2}:\d{2}(?::\d{2})?\s*", "", title).strip()
    return f"## {title}"


def join_text(parts: list[str]) -> str:
    text = "".join(parts)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def render_markdown(title: str, chapters: list[tuple[float, str]], segments: list[dict[str, Any]]) -> str:
    lines: list[str] = [f"# {title}", ""]
    chapter_idx = -1
    paragraph: list[str] = []
    paragraph_len = 0

    def flush() -> None:
        nonlocal paragraph, paragraph_len
        if paragraph:
            text = join_text(paragraph)
            if text:
                lines.append(text)
                lines.append("")
        paragraph = []
        paragraph_len = 0

    for seg in segments:
        while chapter_idx + 1 < len(chapters) and seg["start"] >= chapters[chapter_idx + 1][0]:
            flush()
            chapter_idx += 1
            lines.append(heading(chapters[chapter_idx][1]))
            lines.append("")
        if chapter_idx < 0:
            chapter_idx = 0
            lines.append(heading(chapters[0][1]))
            lines.append("")

        text = seg["text"]
        if paragraph and paragraph_len + len(text) > 260:
            flush()
        paragraph.append(text)
        paragraph_len += len(text)
    flush()
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_audio", nargs="?", help="Audio file to transcribe")
    parser.add_argument("--from-json", help="Format an existing Whisper JSON result instead of running ASR")
    parser.add_argument("--output", required=True, help="Markdown output path")
    parser.add_argument("--title", default="Podcast Transcript", help="Markdown H1 title")
    parser.add_argument("--chapters", type=Path, help="Optional chapter file: '<time> <title>' per line")
    parser.add_argument("--max-minutes", type=float, help="Only transcribe the first N minutes after skipped intro")
    parser.add_argument("--skip-initial-seconds", type=float, default=0, help="Skip intro music or ads before ASR")
    parser.add_argument("--language", default="zh", help="Whisper language code")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="mlx-whisper model repo")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Initial prompt for Whisper")
    parser.add_argument("--replace", action="append", default=[], help="Safe ASR correction OLD=NEW; repeatable")
    parser.add_argument("--asr-cache-dir", type=Path, help="Durable ASR JSON cache directory")
    parser.add_argument("--ffmpeg", default="ffmpeg", help="ffmpeg command path")
    parser.add_argument("--keep-work", action="store_true", help="Keep temporary work directory")
    args = parser.parse_args()

    if not args.from_json and not args.input_audio:
        parser.error("input_audio is required unless --from-json is provided")

    temp = Path(tempfile.mkdtemp(prefix="podcast-transcript-"))
    try:
        result = load_result(args, temp)
        chapters = parse_chapters(args.chapters)
        segments = collect_segments(result, args)
        markdown = render_markdown(args.title, chapters, segments)
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
        print(output)
    finally:
        if args.keep_work:
            print(f"work_dir={temp}", file=sys.stderr)
        else:
            shutil.rmtree(temp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
