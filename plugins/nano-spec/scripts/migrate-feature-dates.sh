#!/usr/bin/env bash
#
# migrate-feature-dates.sh — renomeia pastas em .specs/features/ para o padrão
# YYYY-MM-DD-[feature], usando a data do primeiro commit que criou o spec.md.
#
# Uso:
#   ./migrate-feature-dates.sh           # interativo (pergunta cada rename)
#   ./migrate-feature-dates.sh --dry-run # só lista, não renomeia
#   ./migrate-feature-dates.sh --yes     # renomeia tudo sem perguntar
#
# Roda da raiz do projeto (onde existe .specs/).

set -euo pipefail

DRY_RUN=0
ASSUME_YES=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --yes|-y)  ASSUME_YES=1 ;;
    -h|--help)
      grep '^# ' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *) echo "Flag desconhecida: $arg" >&2; exit 2 ;;
  esac
done

FEATURES_DIR=".specs/features"

if [[ ! -d "$FEATURES_DIR" ]]; then
  echo "❌ $FEATURES_DIR não existe. Rode na raiz do projeto." >&2
  exit 1
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "⚠️  Não é um repo git. Datas virão do filesystem (menos confiável)." >&2
  USE_GIT=0
else
  USE_GIT=1
fi

DATE_REGEX='^[0-9]{4}-[0-9]{2}-[0-9]{2}-'

# Detectar pastas sem prefixo de data (portável para bash 3.2)
CANDIDATES=()
while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  CANDIDATES+=("$path")
done < <(find "$FEATURES_DIR" -mindepth 1 -maxdepth 1 -type d \
  | sort \
  | while read -r path; do
      name=$(basename "$path")
      if [[ ! "$name" =~ $DATE_REGEX ]]; then
        echo "$path"
      fi
    done)

if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
  echo "✅ Todas as pastas em $FEATURES_DIR já seguem o padrão YYYY-MM-DD-[feature]."
  exit 0
fi

echo "📋 Pastas detectadas sem prefixo de data: ${#CANDIDATES[@]}"
echo

renamed=0
skipped=0

for src in "${CANDIDATES[@]}"; do
  name=$(basename "$src")
  spec_file="$src/spec.md"

  # Resolver data: primeiro commit do spec.md > primeiro commit da pasta > mtime
  date=""
  if [[ $USE_GIT -eq 1 && -f "$spec_file" ]]; then
    date=$(git log --diff-filter=A --follow --format=%ad --date=short -- "$spec_file" 2>/dev/null | tail -1 || true)
  fi
  if [[ -z "$date" && $USE_GIT -eq 1 ]]; then
    date=$(git log --diff-filter=A --format=%ad --date=short -- "$src" 2>/dev/null | tail -1 || true)
  fi
  if [[ -z "$date" ]]; then
    date=$(date -r "$src" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
    src_label="(filesystem)"
  else
    src_label="(git)"
  fi

  dst="$FEATURES_DIR/${date}-${name}"

  if [[ -e "$dst" ]]; then
    echo "⚠️  $src → $dst $src_label · destino já existe, pulando."
    ((skipped++))
    continue
  fi

  echo "→ $src"
  echo "  $dst $src_label"

  if [[ $DRY_RUN -eq 1 ]]; then
    ((skipped++))
    continue
  fi

  if [[ $ASSUME_YES -eq 0 ]]; then
    read -r -p "  renomear? [y/N] " resp
    if [[ ! "$resp" =~ ^[yY]$ ]]; then
      ((skipped++))
      echo "  pulado."
      continue
    fi
  fi

  if [[ $USE_GIT -eq 1 ]]; then
    git mv "$src" "$dst"
  else
    mv "$src" "$dst"
  fi
  ((renamed++))
  echo "  ✓ renomeado"
done

echo
if [[ $DRY_RUN -eq 1 ]]; then
  echo "🔍 Dry-run · ${#CANDIDATES[@]} pasta(s) candidata(s). Rode sem --dry-run para aplicar."
else
  echo "✅ Renomeadas: $renamed · Puladas: $skipped"
  if [[ $renamed -gt 0 && $USE_GIT -eq 1 ]]; then
    echo "💡 Commite as mudanças: git commit -m \"chore: aplica prefixo de data nas features\""
  fi
fi
