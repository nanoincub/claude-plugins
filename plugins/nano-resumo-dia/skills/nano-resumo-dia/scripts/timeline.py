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
                        "all_timestamps": sorted(all_timestamps),
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

    # Sugestão de Time Track — baseada em clusters de atividade por projeto
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

    def cluster_timestamps(timestamps, gap_minutes=15):
        """Agrupa timestamps em clusters onde o gap entre msgs consecutivas < gap_minutes."""
        if not timestamps:
            return []
        sorted_ts = sorted(timestamps)
        clusters = []
        current = [sorted_ts[0]]
        for ts in sorted_ts[1:]:
            if (ts - current[-1]).total_seconds() < gap_minutes * 60:
                current.append(ts)
            else:
                clusters.append(current)
                current = [ts]
        clusters.append(current)
        return clusters

    def build_timetrack_from_clusters(session_list):
        """Junta todos os timestamps por projeto, clusteriza e gera entries de time track."""
        # Agregar timestamps por projeto
        project_timestamps = defaultdict(list)
        for s in session_list:
            project_timestamps[s["project"]].extend(s["all_timestamps"])

        entries = []
        ignored = []
        for project, timestamps in project_timestamps.items():
            clusters = cluster_timestamps(timestamps, gap_minutes=15)
            for cluster in clusters:
                cluster_start = cluster[0]
                cluster_end = cluster[-1]
                duration_min = (cluster_end - cluster_start).total_seconds() / 60
                if duration_min < 3:
                    ignored.append({"project": project, "duration_min": round(duration_min, 1)})
                    continue
                # Arredondar para blocos de 15 min
                entry_start = round_time_15(cluster_start, "down")
                entry_end = round_time_15(cluster_end, "up")
                # Garantir mínimo de 15 min
                if (entry_end - entry_start).total_seconds() < 900:
                    entry_end = entry_start + timedelta(minutes=15)
                block_min = round((entry_end - entry_start).total_seconds() / 60)
                entries.append({
                    "project": project,
                    "start": entry_start.strftime("%H:%M"),
                    "end": entry_end.strftime("%H:%M"),
                    "start_dt": entry_start,
                    "end_dt": entry_end,
                    "duration": f"{block_min // 60:02d}:{block_min % 60:02d}",
                    "block_min": block_min,
                    "raw_min": round(duration_min),
                })
        # Merge clusters do mesmo projeto com gap <= 30 min entre eles
        # Agrupa por projeto, merge dentro de cada, depois reordena
        MERGE_GAP = 30 * 60  # 30 minutos em segundos

        by_project = defaultdict(list)
        for e in entries:
            by_project[e["project"]].append(e)

        merged = []
        for project, proj_entries in by_project.items():
            proj_entries.sort(key=lambda x: x["start_dt"])
            current = proj_entries[0]
            for e in proj_entries[1:]:
                if (e["start_dt"] - current["end_dt"]).total_seconds() <= MERGE_GAP:
                    current["end_dt"] = e["end_dt"]
                    current["end"] = e["end"]
                    current["raw_min"] += e["raw_min"]
                    block_min = round((current["end_dt"] - current["start_dt"]).total_seconds() / 60)
                    current["block_min"] = block_min
                    current["duration"] = f"{block_min // 60:02d}:{block_min % 60:02d}"
                else:
                    merged.append(current)
                    current = e
            merged.append(current)

        merged.sort(key=lambda x: x["start_dt"])
        return merged, ignored

    tt_entries, tt_ignored = build_timetrack_from_clusters(sessions)

    # Separar por período
    tt_manha = [e for e in tt_entries if e["start_dt"].hour < cutoff]
    tt_tarde = [e for e in tt_entries if e["start_dt"].hour >= cutoff]

    lines.append("")
    lines.append("## Sugestão para Time Track")
    lines.append("")
    lines.append("> Timestamps de todas as sessões agrupados **por projeto**.")
    lines.append("> Mensagens com gap < 15 min formam um **cluster de atividade**.")
    lines.append("> Início e fim arredondados para blocos de 15 min (mínimo 15 min).")
    lines.append("> Clusters com < 3 min de atividade são descartados.")

    def render_tt_table(entries, lines):
        lines.append("")
        lines.append("| Horário | Duração | Projeto | Resumo |")
        lines.append("|---------|---------|---------|--------|")
        for e in entries:
            lines.append(f"| {e['start']} - {e['end']} | {e['duration']} | `{e['project']}` | {{RESUMO}} |")
        total_block = sum(e["block_min"] for e in entries)
        total_raw = sum(e["raw_min"] for e in entries)
        lines.append(f"\n*Atividade real: {total_raw} min | Arredondado (blocos 15 min): {total_block} min*")

    if tt_manha:
        lines.append("")
        lines.append("### Manhã")
        render_tt_table(tt_manha, lines)

    if tt_tarde:
        lines.append("")
        lines.append("### Tarde")
        render_tt_table(tt_tarde, lines)

    if not tt_manha and not tt_tarde:
        lines.append("\nNenhum cluster de atividade com ≥ 3 min.")

    if tt_ignored:
        lines.append("")
        lines.append("**Ignorados (< 3 min):**")
        for ig in tt_ignored:
            lines.append(f"- `{ig['project']}` — {ig['duration_min']} min")

    lines.append("")
    lines.append("<!-- DADOS PARA GERAR RESUMO -->")
    all_summary = build_project_summary(sessions)
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
