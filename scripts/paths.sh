#!/usr/bin/env bash
# Resolve this plugin's user data directory (the private overlay) and find files
# in it. Overlay first, then the built-in copy, by the same relative path.
#
#   scripts/paths.sh               -> data dir and the rule that picked it
#   scripts/paths.sh dir           -> data dir only
#   scripts/paths.sh file REL      -> winning path for REL, exit 1 if none
#                                     REL: templates/<f>, typst/<f>
#   scripts/paths.sh list SUBDIR   -> <file>\t<user|builtin>\t<path>, overlay first
#                                     SUBDIR: templates, typst, brands
#   scripts/paths.sh stage-typst D -> copy built-in .typ files into D, then the
#                                     overlay's on top, so a user sender.typ wins
#
# Data dir resolution (first match wins):
#   1. $RTL_SKILLS_HOME                    explicit override
#   2. $CLAUDE_USER_DATA/rtl-skills        shared user-data root, if set
#   3. ~/.claude-user-data/rtl-skills      if ~/.claude-user-data exists
#   4. ${XDG_DATA_HOME:-~/.local/share}/claude-plugins/rtl-skills
#                                          if that claude-plugins root exists
#   5. ~/.claude-user-data/rtl-skills      default
set -euo pipefail

NAME=rtl-skills
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
XDG_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins"

if [[ -n "${RTL_SKILLS_HOME:-}" ]]; then
  DIR="$RTL_SKILLS_HOME"; RULE="RTL_SKILLS_HOME"
elif [[ -n "${CLAUDE_USER_DATA:-}" ]]; then
  DIR="$CLAUDE_USER_DATA/$NAME"; RULE="CLAUDE_USER_DATA"
elif [[ -d "$HOME/.claude-user-data" ]]; then
  DIR="$HOME/.claude-user-data/$NAME"; RULE="existing ~/.claude-user-data"
elif [[ -d "$XDG_ROOT" ]]; then
  DIR="$XDG_ROOT/$NAME"; RULE="existing $XDG_ROOT"
else
  DIR="$HOME/.claude-user-data/$NAME"; RULE="default"
fi

case "${1:-}" in
  dir) echo "$DIR" ;;
  file)
    rel="${2:?relative path, e.g. templates/newsletter.html}"
    for c in "$DIR/$rel" "$PLUGIN_ROOT/assets/$rel"; do
      [[ -e "$c" ]] && { echo "$c"; exit 0; }
    done
    echo "not found: $rel" >&2; exit 1 ;;
  list)
    sub="${2:?subdir: templates, typst or brands}"
    declare -A seen=()
    if [[ -d "$DIR/$sub" ]]; then
      for f in "$DIR/$sub"/*; do
        [[ -e "$f" ]] || continue
        b=$(basename "$f"); seen[$b]=1
        printf '%s\tuser\t%s\n' "$b" "$f"
      done
    fi
    if [[ -d "$PLUGIN_ROOT/assets/$sub" ]]; then
      for f in "$PLUGIN_ROOT/assets/$sub"/*; do
        [[ -e "$f" ]] || continue
        b=$(basename "$f")
        [[ -n "${seen[$b]:-}" ]] && continue
        printf '%s\tbuiltin\t%s\n' "$b" "$f"
      done
    fi ;;
  stage-typst)
    dest="${2:?destination directory}"
    mkdir -p "$dest"
    cp "$PLUGIN_ROOT"/assets/typst/*.typ "$dest"/
    if compgen -G "$DIR/typst/*.typ" >/dev/null; then cp "$DIR"/typst/*.typ "$dest"/; fi
    echo "$dest" ;;
  "") printf '%s\t(%s)\n' "$DIR" "$RULE" ;;
  *) echo "unknown command: $1" >&2; exit 2 ;;
esac
