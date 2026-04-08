#!/usr/bin/env python3
"""
Extrai timeline de trabalho dos históricos de sessão do Claude Code.
Uso: python3 timeline.py [YYYY-MM-DD] [--json]
  - Sem argumento: usa a data de ontem
  - Com data: usa a data informada
  - --json: saída em JSON ao invés de Markdown
"""

import json
import os
import glob
import re
import sys
from datetime import datetime, timedelta
from collections import defaultdict

UTC_OFFSET_HOURS = -3  # BRT


def find_projects_dir():
    """Detecta o diretório de projetos do Claude Code.
    Busca em ordem: --base-dir arg, path padrão, sandbox Cowork (mnt/.claude)."""
    for arg in sys.argv[1:]:
        if arg.startswith("--base-dir="):
            custom = os.path.join(arg.split("=", 1)[1], "projects")
            if os.path.isdir(custom):
                return custom

    # Path padrão (CLI local)
    default = os.path.expanduser("~/.claude/projects")
    if os.path.isdir(default):
        return default

    # Sandbox Cowork: $HOME/mnt/.claude/projects
    cowork = os.path.join(os.environ.get("HOME", ""), "mnt", ".claude", "projects")
    if os.path.isdir(cowork):
        return cowork

    # Fallback: tenta achar .claude/projects em qualquer subpasta do HOME
    home = os.environ.get("HOME", "")
    for root, dirs, _ in os.walk(home, topdown=True):
        if ".claude" in dirs:
            candidate = os.path.join(root, ".claude", "projects")
            if os.path.isdir(candidate):
                return candidate
        # Não descer mais que 3 níveis
        if root.count(os.sep) - home.count(os.sep) >= 3:
            dirs.clear()

    return default  # fallback mesmo se não existir


PROJECTS_DIR = find_projects_dir()


def parse_ts(ts):
    if isinstance(ts, (int, float)):
        return datetime.utcfromtimestamp(ts / 1000)
    if isinstance(ts, str):
        try:
            ts = ts.replace("Z", "+00:00")
            dt = datetime.fromisoformat(ts)
            return dt.replace(tzinfo=None)
        except Exception:
            pass
    return None


def to_brt(dt):
    return dt + timedelta(hours=UTC_OFFSET_HOURS)


def readable_project(dirname):
    # Formato: -Users-<username>-<path> onde path começa com pasta conhecida (www, claude, Downloads, etc)
    # Detecta onde o username termina encontrando o primeiro segmento de path comum
    known_roots = ["www", "claude", "Downloads", "Documents", "Desktop", "tmp", "opt", "var", "home", "projects"]
    for root in known_roots:
        marker = f"-{root}"
        idx = dirname.find(marker)
        if idx > 0:
            name = dirname[idx + 1:]  # remove tudo antes incluindo o hífen
            return name.replace("-", "/") if name else "root"
    # Fallback: remove -Users-xxx- com regex genérico (2 segmentos após Users)
    name = re.sub(r"^-Users-[^-]+-[^-]+-", "", dirname)
    if name == dirname:
        name = re.sub(r"^-Users-[^-]+-", "", dirname)
    return name.replace("-", "/") if name else "root"


def clean_content(content):
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block["text"])
            elif isinstance(block, str):
                texts.append(block)
        content = " ".join(texts)

    if "<local-command-caveat>" in content:
        return ""

    content = re.sub(r"<system-reminder>.*?</system-reminder>", "", content, flags=re.DOTALL)
    content = re.sub(r"<command-\w+>.*?</command-\w+>", "", content, flags=re.DOTALL)
    content = re.sub(r"<IMPORTANT>.*?</IMPORTANT>", "", content, flags=re.DOTALL)
    content = re.sub(r"<EXTREMELY_IMPORTANT>.*?</EXTREMELY_IMPORTANT>", "", content, flags=re.DOTALL)
    content = re.sub(r"Base directory for this skill:.*?\n", "", content)
    content = content.strip()
    return content


def extract_sessions(target_date):
    sessions = []

    for project_dir in glob.glob(os.path.join(PROJECTS_DIR, "*")):
        if not os.path.isdir(project_dir):
            continue
        project_name = readable_project(os.path.basename(project_dir))

        for jsonl_file in glob.glob(os.path.join(project_dir, "*.jsonl")):
            try:
                first_user_msg = None
                first_ts = None
                last_ts = None
                branches = set()
                user_msgs = 0
                assistant_msgs = 0
                all_timestamps = []
                session_id = os.path.basename(jsonl_file).replace(".jsonl", "")
                has_target_date = False

                with open(jsonl_file, "r") as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        dt = parse_ts(entry.get("timestamp"))
                        if not dt:
                            continue

                        dt_brt = to_brt(dt)

                        if entry.get("gitBranch"):
                            branches.add(entry["gitBranch"])

                        entry_type = entry.get("type")

                        if entry_type == "user" and isinstance(entry.get("message"), dict):
                            if entry["message"].get("role") == "user":
                                if dt_brt.strftime("%Y-%m-%d") == target_date:
                                    has_target_date = True
                                    user_msgs += 1
                                    all_timestamps.append(dt_brt)

                                    content = clean_content(entry["message"].get("content", ""))
                                    if not first_user_msg and content and len(content) > 3:
                                        first_user_msg = content[:150].replace("\n", " ").strip()
                                        first_ts = dt_brt

                        if entry_type == "assistant":
                            if dt_brt.strftime("%Y-%m-%d") == target_date:
                                assistant_msgs += 1
                                all_timestamps.append(dt_brt)

                        if dt_brt.strftime("%Y-%m-%d") == target_date:
                            if not first_ts or dt_brt < first_ts:
                                pass
                            if not last_ts or dt_brt > last_ts:
                                last_ts = dt_brt

                if has_target_date and first_user_msg and first_ts:
                    # Tempo ativo: soma intervalos entre msgs consecutivas onde gap < 5 min
                    active_seconds = 0
                    all_timestamps.sort()
                    for i in range(1, len(all_timestamps)):
                        gap = (all_timestamps[i] - all_timestamps[i - 1]).total_seconds()
                        if gap < 900:  # 15 minutos
                            active_seconds += gap
                    duration_min = int(active_seconds / 60)

                    branch = ", ".join(sorted(branches)) if branches else "-"

                    end_time = last_ts.strftime("%H:%M") if last_ts else first_ts.strftime("%H:%M")
                    span_min = int((last_ts - first_ts).total_seconds() / 60) if last_ts and first_ts else 0
                    span_h = span_min // 60
                    span_m = span_min % 60
                    dur_h = duration_min // 60
                    dur_m = duration_min % 60
                    sessions.append({
                        "time": f"{first_ts.strftime('%H:%M')} - {end_time}",
                        "time_sort": first_ts,
                        "project": project_name,
                        "branch": branch,
                        "description": first_user_msg,
                        "span": f"{span_h:02d}:{span_m:02d}",
                        "span_min": span_min,
                        "active": f"{dur_h:02d}:{dur_m:02d}",
                        "duration_min": duration_min,
                        "msgs": user_msgs + assistant_msgs,
                        "user_msgs": user_msgs,
                        "assistant_msgs": assistant_msgs,
                        "session_id": session_id,
                    })
            except Exception:
                continue

    sessions.sort(key=lambda x: x["time_sort"])
    return sessions


def format_markdown(sessions, target_date):
    lines = []
    lines.append(f"# Timeline de trabalho — {target_date}")
    lines.append(f"Sessões: {len(sessions)}")

    if not sessions:
        lines.append("\nNenhuma sessão encontrada para esta data.")
        return "\n".join(lines)

    total_msgs = sum(s["msgs"] for s in sessions)
    total_duration = sum(s["duration_min"] for s in sessions)
    first_time = sessions[0]["time"]
    last_time = sessions[-1]["time"]

    lines.append(f"Período: {first_time} → {last_time} BRT | Total: ~{total_duration} min | {total_msgs} mensagens")

    cutoff = 14  # 14h divide manhã/tarde
    manha = [s for s in sessions if s["time_sort"].hour < cutoff]
    tarde = [s for s in sessions if s["time_sort"].hour >= cutoff]

    def render_table(session_list, lines):
        lines.append("")
        lines.append("| Horário | Sessão Aberta | Interação Real | Projeto | Descrição | msg User | msg Claude | Session ID |")
        lines.append("|---------|---------|-------|---------|-----------|----------|-----------|------------|")
        for s in session_list:
            desc = s["description"][:80]
            lines.append(f"| {s['time']} | {s['span']} | {s['active']} | `{s['project']}` | {desc} | {s['user_msgs']} | {s['assistant_msgs']} | `{s['session_id']}` |")

    if manha:
        manha_msgs = sum(s["msgs"] for s in manha)
        manha_dur = sum(s["duration_min"] for s in manha)
        lines.append("")
        lines.append(f"### Manhã ({len(manha)} sessões | ~{manha_dur} min | {manha_msgs} msgs)")
        render_table(manha, lines)

    if tarde:
        tarde_msgs = sum(s["msgs"] for s in tarde)
        tarde_dur = sum(s["duration_min"] for s in tarde)
        lines.append("")
        lines.append(f"### Tarde ({len(tarde)} sessões | ~{tarde_dur} min | {tarde_msgs} msgs)")
        render_table(tarde, lines)

    # Resumo por projeto com divisão manhã/tarde
    from collections import OrderedDict

    def build_project_summary(session_list):
        summary = OrderedDict()
        for s in session_list:
            p = s["project"]
            if p not in summary:
                summary[p] = {
                    "start": s["time_sort"],
                    "end": s["time_sort"] + timedelta(minutes=s["span_min"]),
                    "descriptions": [],
                    "total_user_msgs": 0,
                    "total_assistant_msgs": 0,
                    "total_duration": 0,
                    "total_span": 0,
                }
            ps = summary[p]
            if s["time_sort"] < ps["start"]:
                ps["start"] = s["time_sort"]
            end_candidate = s["time_sort"] + timedelta(minutes=s["span_min"])
            if end_candidate > ps["end"]:
                ps["end"] = end_candidate
            ps["descriptions"].append(s["description"][:80])
            ps["total_user_msgs"] += s["user_msgs"]
            ps["total_assistant_msgs"] += s["assistant_msgs"]
            ps["total_duration"] += s["duration_min"]
            ps["total_span"] += s["span_min"]
        return summary

    def render_summary_table(summary, lines):
        lines.append("")
        lines.append("| Horário | Sessão Aberta | Interação Real | Projeto | Resumo | msg User | msg Claude |")
        lines.append("|---------|---------|-------|---------|--------|----------|-----------|")
        for p, ps in summary.items():
            start = ps["start"].strftime("%H:%M")
            end = ps["end"].strftime("%H:%M")
            span_min = int((ps["end"] - ps["start"]).total_seconds() / 60)
            span_h = span_min // 60
            span_m = span_min % 60
            dur_h = ps["total_duration"] // 60
            dur_m = ps["total_duration"] % 60
            lines.append(f"| {start} - {end} | {span_h:02d}:{span_m:02d} | {dur_h:02d}:{dur_m:02d} | `{p}` | {{RESUMO}} | {ps['total_user_msgs']} | {ps['total_assistant_msgs']} |")

    lines.append("")
    lines.append("## Resumo por projeto")

    manha_summary = build_project_summary(manha)
    tarde_summary = build_project_summary(tarde)

    if manha_summary:
        lines.append("")
        lines.append("### Manhã")
        render_summary_table(manha_summary, lines)

    if tarde_summary:
        lines.append("")
        lines.append("### Tarde")
        render_summary_table(tarde_summary, lines)

    # Sugestão de Time Track
    import math

    def round_up_15(minutes):
        """Arredonda para cima em blocos de 15 min (mínimo 15)."""
        if minutes <= 0:
            return 15
        return int(math.ceil(minutes / 15) * 15)

    def round_time_15(dt, direction="down"):
        """Arredonda datetime para o bloco de 15 min mais próximo."""
        minute = dt.minute
        if direction == "down":
            rounded = minute - (minute % 15)
        else:
            rounded = minute + (15 - minute % 15) if minute % 15 != 0 else minute
        return dt.replace(minute=0, second=0) + timedelta(minutes=rounded)

    all_summary = build_project_summary(sessions)

    # Filtrar projetos com menos de 15 min de interação real e ordenar por início
    sorted_projects = sorted(
        [(p, ps) for p, ps in all_summary.items() if ps["total_duration"] >= 15],
        key=lambda x: x[1]["start"],
    )

    timetrack_entries = []
    cursor = None  # onde o próximo entry começa

    for p, ps in sorted_projects:
        active_min = ps["total_duration"]
        block_min = round_up_15(active_min)

        if cursor is None:
            entry_start = round_time_15(ps["start"], "down")
        else:
            # Se o início real é depois do cursor, usa o início real arredondado
            if ps["start"] > cursor:
                entry_start = round_time_15(ps["start"], "down")
            else:
                entry_start = cursor

        entry_end = entry_start + timedelta(minutes=block_min)
        cursor = entry_end

        timetrack_entries.append({
            "project": p,
            "start": entry_start.strftime("%H:%M"),
            "end": entry_end.strftime("%H:%M"),
            "duration": f"{block_min // 60:02d}:{block_min % 60:02d}",
            "active_min": active_min,
        })

    lines.append("")
    lines.append("## Sugestão para Time Track")
    lines.append("")
    lines.append("> Horários calculados com base no tempo de **interação real** (mensagens com gap < 15 min),")
    lines.append("> arredondados para cima em blocos de **15 minutos** (mínimo 15 min por projeto),")
    lines.append("> organizados **sequencialmente** sem sobreposição.")
    lines.append("> Sessões com menos de 15 min de interação real são descartadas.")
    lines.append("")
    lines.append("| Horário | Duração | Projeto | Resumo |")
    lines.append("|---------|---------|---------|--------|")
    for e in timetrack_entries:
        lines.append(f"| {e['start']} - {e['end']} | {e['duration']} | `{e['project']}` | {{RESUMO}} |")

    total_tt = sum(e["active_min"] for e in timetrack_entries)
    total_block = sum(round_up_15(e["active_min"]) for e in timetrack_entries)
    lines.append(f"\n*Interação real: {total_tt} min | Arredondado (blocos 15 min): {total_block} min*")

    # Itens ignorados (< 15 min de interação real)
    ignored = [(p, ps) for p, ps in all_summary.items() if ps["total_duration"] < 15]
    if ignored:
        lines.append("")
        lines.append("**Ignorados (< 15 min):**")
        for p, ps in ignored:
            lines.append(f"- `{p}` — {ps['total_duration']} min de interação real")

    lines.append("")
    lines.append("<!-- DADOS PARA GERAR RESUMO -->")
    for p, ps in all_summary.items():
        lines.append(f"<!-- PROJETO: {p} -->")
        for d in ps["descriptions"]:
            lines.append(f"<!--   - {d} -->")

    return "\n".join(lines)


def format_json(sessions, target_date):
    output = {
        "date": target_date,
        "timezone": "BRT (UTC-3)",
        "total_sessions": len(sessions),
        "sessions": [],
    }
    for s in sessions:
        output["sessions"].append({
            "time": s["time"],
            "project": s["project"],
            "branch": s["branch"],
            "description": s["description"],
            "duration": s["duration"],
            "messages": {"total": s["msgs"], "user": s["user_msgs"], "assistant": s["assistant_msgs"]},
            "session_id": s["session_id"],
        })
    return json.dumps(output, indent=2, ensure_ascii=False)


def main():
    output_json = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]

    if args:
        target_date = args[0]
    else:
        yesterday = datetime.now() + timedelta(hours=UTC_OFFSET_HOURS) - timedelta(days=1)
        target_date = yesterday.strftime("%Y-%m-%d")

    sessions = extract_sessions(target_date)

    if output_json:
        print(format_json(sessions, target_date))
    else:
        print(format_markdown(sessions, target_date))


if __name__ == "__main__":
    main()
