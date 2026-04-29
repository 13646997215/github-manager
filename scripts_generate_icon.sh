#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT_DIR/assets"
python3 - <<'PY' "$ROOT_DIR/assets/github-manager.svg"
import sys
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
  <rect width="256" height="256" rx="48" fill="#111827"/>
  <rect x="28" y="28" width="200" height="200" rx="32" fill="#1f2937" stroke="#374151" stroke-width="4"/>
  <circle cx="78" cy="78" r="18" fill="#60a5fa"/>
  <circle cx="128" cy="78" r="18" fill="#34d399"/>
  <circle cx="178" cy="78" r="18" fill="#f472b6"/>
  <path d="M78 96v62c0 11 9 20 20 20h60" fill="none" stroke="#93c5fd" stroke-width="12" stroke-linecap="round"/>
  <path d="M128 96v42c0 11 9 20 20 20h30" fill="none" stroke="#6ee7b7" stroke-width="12" stroke-linecap="round"/>
  <path d="M178 96v24" fill="none" stroke="#f9a8d4" stroke-width="12" stroke-linecap="round"/>
  <rect x="56" y="176" width="144" height="24" rx="12" fill="#111827" stroke="#4b5563" stroke-width="3"/>
  <text x="128" y="194" font-size="20" text-anchor="middle" font-family="DejaVu Sans, sans-serif" fill="#f9fafb">GHM PRO</text>
</svg>'''
open(sys.argv[1], 'w', encoding='utf-8').write(svg)
PY
