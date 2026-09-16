#!/bin/sh
# install.sh — instala os hooks de gitflow da Nano Incub no repositório alvo.
#
#   ./install.sh [caminho-do-repo] [diretório-de-hooks]
#
# Default: instala em <repo>/.githooks (versionável) e aponta
# `gitflow.path.hooks` para lá. Se o repo já tiver `gitflow.path.hooks` ou
# `core.hooksPath`, usa o diretório que já está configurado.

set -eu

SRC="$(cd "$(dirname "$0")" && pwd)"
REPO="${1:-$(pwd)}"

cd "$REPO"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "erro: '$REPO' não é um repositório git" >&2
  exit 1
}
cd "$ROOT"

if [ -n "${2:-}" ]; then
  DEST="$2"
else
  DEST="$(git config gitflow.path.hooks 2>/dev/null || git config core.hooksPath 2>/dev/null || echo '.githooks')"
fi

case "$DEST" in
  /*) DEST_ABS="$DEST" ;;
  *)  DEST_ABS="$ROOT/$DEST" ;;
esac

mkdir -p "$DEST_ABS"
for f in nano-pr-create nano-finish-check post-flow-feature-publish post-flow-bugfix-publish \
         post-flow-release-publish post-flow-hotfix-publish post-flow-feature-finish \
         post-flow-bugfix-finish post-flow-release-finish post-flow-hotfix-finish; do
  cp "$SRC/$f" "$DEST_ABS/$f"
  chmod +x "$DEST_ABS/$f"
done

git config gitflow.path.hooks "$DEST"
echo "hooks instalados em $DEST_ABS"
echo "gitflow.path.hooks = $DEST"

git flow version 2>/dev/null | grep -q git-flow-next \
  || echo "aviso: git-flow-next não detectado — os hooks só rodam com ele." >&2
command -v gh >/dev/null 2>&1 \
  || echo "aviso: gh não instalado — o hook de publish não conseguirá abrir o PR." >&2

case "$(git remote get-url origin 2>/dev/null || echo '')" in
  *github.com*) ;;
  *) echo "nota: remote não é GitHub — o hook de publish sai sem fazer nada." ;;
esac
