#!/usr/bin/env python3
"""Create a read-only inventory of project-owned files for Project Commander."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    "target",
    "__pycache__",
}

SOURCE_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".css", ".dart", ".ex", ".exs", ".go",
    ".gd", ".h", ".hpp", ".html", ".java", ".js", ".jsx", ".kt", ".kts",
    ".lua", ".php", ".py", ".rb", ".rs", ".scala", ".scss", ".sh", ".sql",
    ".swift", ".ts", ".tsx", ".vue", ".xml",
}
DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".txt", ".adoc"}
CONFIG_EXTENSIONS = {".json", ".jsonc", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".conf"}
ASSET_EXTENSIONS = {
    ".aiff", ".avi", ".bmp", ".doc", ".docx", ".flac", ".gif", ".ico", ".jpeg",
    ".jpg", ".m4a", ".mkv", ".mov", ".mp3", ".mp4", ".ogg", ".otf", ".pdf",
    ".png", ".ppt", ".pptx", ".psd", ".svg", ".tif", ".tiff", ".ttf", ".wav",
    ".webm", ".webp", ".woff", ".woff2", ".xls", ".xlsx", ".zip",
}

KEY_NAMES = {
    "readme", "readme.md", "license", "license.md",
    "package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "pyproject.toml",
    "requirements.txt", "poetry.lock", "cargo.toml", "cargo.lock", "go.mod", "go.sum",
    "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts",
    "pubspec.yaml", "project.godot", "dockerfile", "docker-compose.yml", "compose.yaml",
    "makefile", "justfile", "tsconfig.json", "vite.config.ts", "next.config.js",
}

SENSITIVE_EXACT = {
    ".env", ".env.local", ".env.production", ".npmrc", ".pypirc", ".netrc",
    "credentials.json", "secrets.json", "id_rsa", "id_ed25519",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".keystore"}


def iso_time(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def is_sensitive(path: Path) -> bool:
    name = path.name.lower()
    if name in SENSITIVE_EXACT or path.suffix.lower() in SENSITIVE_SUFFIXES:
        return True
    return any(token in name for token in ("credential", "api_key", "apikey", "access_token"))


def classify(path: Path) -> str:
    lower_parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    suffix = path.suffix.lower()
    if is_sensitive(path):
        return "sensitive-metadata-only"
    if "test" in lower_parts or "tests" in lower_parts or name.startswith("test_") or name.endswith("_test.py"):
        return "test"
    if suffix in DOC_EXTENSIONS or "docs" in lower_parts or "documentation" in lower_parts:
        return "documentation"
    if suffix in CONFIG_EXTENSIONS or name in KEY_NAMES or name.startswith("."):
        return "configuration"
    if suffix in SOURCE_EXTENSIONS:
        return "source"
    if suffix in ASSET_EXTENSIONS:
        return "asset-or-binary"
    return "other"


def is_key_file(path: Path) -> bool:
    return path.name.lower() in KEY_NAMES


def collect(root: Path, include_all: bool, limit: int) -> dict:
    files: list[dict] = []
    skipped: list[str] = []
    unreadable: list[str] = []

    for current, dirs, names in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_dirs = []
        for directory in sorted(dirs):
            candidate = current_path / directory
            if directory in SKIP_DIRS:
                skipped.append(candidate.relative_to(root).as_posix())
            else:
                kept_dirs.append(directory)
        dirs[:] = kept_dirs

        for name in sorted(names):
            path = current_path / name
            relative = path.relative_to(root)
            try:
                stat = path.lstat()
            except OSError:
                unreadable.append(relative.as_posix())
                continue
            files.append(
                {
                    "path": relative.as_posix(),
                    "size": stat.st_size,
                    "modified": iso_time(stat.st_mtime),
                    "modified_timestamp": stat.st_mtime,
                    "category": "symlink" if path.is_symlink() else classify(relative),
                    "extension": relative.suffix.lower() or "<none>",
                    "key_file": is_key_file(relative),
                }
            )

    category_counts = Counter(item["category"] for item in files)
    extension_counts = Counter(item["extension"] for item in files)
    newest = sorted(files, key=lambda item: item["modified_timestamp"], reverse=True)[:limit]
    largest = sorted(files, key=lambda item: item["size"], reverse=True)[:limit]
    key_files = [item for item in files if item["key_file"]]

    for item in files:
        item.pop("modified_timestamp", None)
        item.pop("key_file", None)

    report = {
        "schema_version": 1,
        "root": str(root),
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "counts": {
            "project_owned_files": len(files),
            "total_bytes": sum(item["size"] for item in files),
            "skipped_directories": len(skipped),
            "unreadable_files": len(unreadable),
        },
        "category_counts": dict(sorted(category_counts.items())),
        "extension_counts": dict(extension_counts.most_common()),
        "key_files": key_files,
        "newest_files": newest,
        "largest_files": largest,
        "skipped_directories": skipped,
        "unreadable_files": unreadable,
    }
    if include_all:
        report["files"] = files
    return report


def markdown(report: dict) -> str:
    counts = report["counts"]
    lines = [
        "# Project inventory",
        "",
        f"- Root: `{report['root']}`",
        f"- Project-owned files: {counts['project_owned_files']}",
        f"- Total bytes: {counts['total_bytes']}",
        f"- Skipped dependency/generated/VCS directories: {counts['skipped_directories']}",
        f"- Unreadable files: {counts['unreadable_files']}",
        "",
        "## Categories",
        "",
    ]
    for name, count in report["category_counts"].items():
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Key files", ""])
    for item in report["key_files"]:
        lines.append(f"- `{item['path']}` ({item['category']}, {item['size']} bytes)")
    lines.extend(["", "## Newest files", ""])
    for item in report["newest_files"]:
        lines.append(f"- `{item['path']}` — {item['modified']}")
    lines.extend(["", "## Skipped directories", ""])
    for path in report["skipped_directories"]:
        lines.append(f"- `{path}`")
    if "files" in report:
        lines.extend(["", "## All inventoried files", ""])
        for item in report["files"]:
            lines.append(f"- `{item['path']}` ({item['category']}, {item['size']} bytes)")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Project root to inspect")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--all-files", action="store_true", help="Include every inventoried file in output")
    parser.add_argument("--limit", type=int, default=30, help="Number of newest/largest files to include")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    if args.limit < 1:
        parser.error("--limit must be positive")

    report = collect(root, args.all_files, args.limit)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(markdown(report), end="")


if __name__ == "__main__":
    main()
