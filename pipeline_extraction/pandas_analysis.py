import json
import math

import pandas as pd

SUBSET = "small"
RESULTS_CSV = f"{SUBSET}_pyref_results_full.csv"   # output della pipeline (una riga per occorrenza di smell)
OUTPUT_MD = f"analisi_valid_refactor_{SUBSET}.md"

# configurazione delle due fasi: colonne della pipeline per introduzione e rimozione
PHASES = {
    "intro": {
        "title": "Introduzione",
        "plural": "introduzioni",
        "status": "pyref_refactor_intro_status",
        "count": "pyref_refactor_intro_count",
        "commit": "commitid_introduced",
        "same_file": "same_file_intro",
        "same_function": "same_function_intro",
        "valid_out": "pyref_out_same_function_intro",
    },
    "removed": {
        "title": "Rimozione",
        "plural": "rimozioni",
        "status": "pyref_ref_removed_status",
        "count": "pyref_ref_removed_count",
        "commit": "commitid_removed",
        "same_file": "same_file_removed",
        "same_function": "same_function_removed",
        "valid_out": "pyref_out_same_function_removed",
    },
}

# unita' di analisi: una riga del CSV = una occorrenza di smell
dedup = pd.read_csv(RESULTS_CSV, dtype=str, keep_default_na=False)
n_raw = n_dedup = len(dedup)


def _betacf(a, b, x):
    """Frazione continua per la beta incompleta (metodo di Lentz)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-16:
            break
    return h


def _betainc(a, b, x):
    """Beta incompleta regolarizzata I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def spearman(x, y):
    """
    rho di Spearman = Pearson sui ranghi (ranghi medi per i pari merito) e p-value a due code
    con la distribuzione t di Student (n-2 gradi di liberta'), come scipy.stats.spearmanr.
    """
    x, y = pd.Series(list(x)), pd.Series(list(y))
    n = len(x)
    rho = x.rank().corr(y.rank())  # Pearson sui ranghi
    if n < 3 or pd.isna(rho):
        return float("nan"), float("nan")
    if abs(rho) >= 1.0:
        return rho, 0.0
    t = rho * math.sqrt((n - 2) / (1.0 - rho * rho))
    df = n - 2
    return rho, _betainc(df / 2.0, 0.5, df / (df + t * t))


def wilson(k, n, z=1.96):
    """Intervallo di confidenza di Wilson al 95% per una proporzione k/n."""
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    metà = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centro - metà, centro + metà


def pct(n, d):
    return f"{100 * n / d:.1f}%" if d else "n/d"


def to_flag(series):
    return pd.to_numeric(series, errors="coerce")


def valid_types(cell):
    """Tipi di refactoring delle entry di PyRef gia' filtrate (stesso file e stessa funzione)."""
    if not cell:
        return []
    out = []
    for entry in json.loads(cell):
        rt = entry.get("Refactoring Type")
        if isinstance(rt, list):
            out.extend(rt)
        elif rt:
            out.append(rt)
    return [t.strip() for t in out if t and t.strip()]


def count_entries(cell):
    """Numero di entry di PyRef nel JSON filtrato."""
    return len(json.loads(cell)) if cell else 0


def spearman_section(d, ok, cfg):
    """
    Spearman nella singola fase, una osservazione per occorrenza di smell nei soli commit con refactoring
    (status=ok e count > 0):
      A = refactoring valido (same_function 0/1)
      B = numero di smell (tutte le istanze, di qualsiasi tipo) del commit di questa fase
          (commit di introduzione per 'intro', di rimozione per 'removed')
    """
    # B si calcola su tutte le righe del commit, stesso repo
    d = d.assign(n_smell_commit=d.groupby(["repo", cfg["commit"]])[cfg["commit"]].transform("size"))
    # solo commit in cui PyRef ha trovato refactoring (status=ok e count > 0)
    ok = d[(d[cfg["status"]] == "ok") & (d["count_num"] > 0)]
    x = ok["f_func"].astype(int)
    y = ok["n_smell_commit"]
    n = len(ok)
    lines = ["### Correlazione di Spearman: refactoring valido vs numero di smell nel commit\n"]
    lines.append(f"Occorrenze in commit con `status=ok` e almeno un refactoring (`{cfg['count']}` > 0): **{n}** "
                 f"(commit distinti: {ok.groupby(['repo', cfg['commit']]).ngroups})\n")
    if n < 3 or x.nunique() < 2 or y.nunique() < 2:
        lines.append("Correlazione non calcolabile: una delle due variabili e' costante.\n")
        return lines

    rho, p = spearman(x, y)
    lines.append(f"- rho di Spearman: **{rho:.3f}** (p-value = {p:.3g}, n = {n})\n")
    lines.append("| Refactoring valido (A) | # occorrenze | smell nel commit (B): mediana | media |")
    lines.append("|---|---:|---:|---:|")
    for v in (0, 1):
        g = y[x == v]
        lines.append(f"| {v} | {len(g)} | {g.median():.1f} | {g.mean():.2f} |")
    lines.append("")
    lines.append("Nota: le occorrenze dello stesso commit hanno lo stesso B, quindi non sono osservazioni indipendenti "
                 "e il p-value tende a essere troppo ottimistico.\n")
    return lines


def analyze(phase):
    cfg = PHASES[phase]
    d = dedup.copy()
    d["count_num"] = to_flag(d[cfg["count"]])
    d["has_any"] = d["count_num"] > 0                      # PyRef ha trovato refactoring nel commit (qualsiasi file)
    d["f_file"] = to_flag(d[cfg["same_file"]]) == 1        # almeno un refactoring nello stesso file
    d["f_func"] = to_flag(d[cfg["same_function"]]) == 1    # ... e sulla stessa funzione = refactoring VALIDO
    d["types"] = d[cfg["valid_out"]].apply(valid_types)
    d["n_entries"] = d[cfg["valid_out"]].apply(count_entries)

    status_counts = d[cfg["status"]].value_counts()
    ok = d[d[cfg["status"]] == "ok"]
    n_ok = len(ok)
    n_any, n_file, n_func = int(ok["has_any"].sum()), int(ok["f_file"].sum()), int(ok["f_func"].sum())

    lines = [f"## {cfg['title']}\n"]

    lines.append("### Copertura (status PyRef)\n")
    lines.append("| Status | # occorrenze | % |")
    lines.append("|---|---:|---:|")
    for status, count in status_counts.items():
        lines.append(f"| `{status}` | {count} | {pct(count, n_dedup)} |")
    lines.append("")

    lines.append("### Dal refactoring generico a quello valido\n")
    lines.append(f"Occorrenze con `status=ok`: **{n_ok}**\n")
    lines.append("| Passo | # occorrenze | % su ok |")
    lines.append("|---|---:|---:|")
    lines.append(f"| PyRef trova refactoring nel commit (qualsiasi file) | {n_any} | {pct(n_any, n_ok)} |")
    lines.append(f"| ... di cui nello stesso file (`same_file`) | {n_file} | {pct(n_file, n_ok)} |")
    lines.append(f"| ... di cui sulla stessa funzione (`same_function`) = **valido** | {n_func} | {pct(n_func, n_ok)} |")
    lines.append("")

    lines.append("### Quota con refactoring valido\n")
    lines.append(f"Domanda: in quante {cfg['plural']} di smell c'e' un refactoring valido (stesso file e stessa funzione)?\n")
    lines.append("| Unita' | Con refactoring valido | Analizzabili (`ok`) | Quota | IC 95% (Wilson) |")
    lines.append("|---|---:|---:|---:|---|")
    lo, hi = wilson(n_func, n_ok)
    lines.append(f"| Occorrenze di smell | {n_func} | {n_ok} | {pct(n_func, n_ok)} | {100 * lo:.1f}% - {100 * hi:.1f}% |")
    per_commit = ok.groupby(["repo", cfg["commit"]])["f_func"].any()
    n_c, k_c = len(per_commit), int(per_commit.sum())
    lo, hi = wilson(k_c, n_c)
    lines.append(f"| Commit (almeno una occorrenza valida) | {k_c} | {n_c} | {pct(k_c, n_c)} | {100 * lo:.1f}% - {100 * hi:.1f}% |")
    lines.append("")
    lines.append("L'intervallo sulle occorrenze e' ottimistico: le occorrenze dello stesso commit non sono indipendenti "
                 "(l'intervallo per commit e' piu' prudente).\n")

    lines.append("### Ratio di refactoring valido per tipologia di smell\n")
    per_smell = (
        ok.groupby("smell_name")["f_func"]
        .agg(analizzabili="count", validi="sum")
        .assign(ratio=lambda x: x["validi"] / x["analizzabili"])
        .join(d.groupby("smell_name").size().rename("istanze_totali"))
        .sort_values("ratio", ascending=False)
    )
    lines.append("| Smell | Istanze totali | Analizzabili | Con refactoring valido | Ratio |")
    lines.append("|---|---:|---:|---:|---:|")
    for smell, row in per_smell.iterrows():
        lines.append(
            f"| `{smell}` | {int(row['istanze_totali'])} | {int(row['analizzabili'])} | "
            f"{int(row['validi'])} | {pct(row['validi'], row['analizzabili'])} |"
        )
    lines.append("")

    valid_rows = ok[ok["f_func"]]
    exploded = valid_rows[["smell_name", "types"]].explode("types").dropna(subset=["types"])
    type_counts = exploded["types"].value_counts()
    total_ops = int(type_counts.sum())

    n_entries = int(valid_rows["n_entries"].sum())
    lines.append("### Tipologie di refactoring valide\n")
    lines.append(f"- Occorrenze con refactoring valido: **{n_func}**")
    lines.append(f"- Entry di PyRef valide (stesso file e stessa funzione): **{n_entries}**")
    lines.append(f"- Tipi di refactoring contati: **{total_ops}** (una entry puo' avere piu' tipi)")
    lines.append(f"- Media: {n_entries / n_func:.2f} entry valide per occorrenza\n" if n_func else "")
    dist = valid_rows["n_entries"].clip(upper=4).value_counts().sort_index()
    lines.append("| Entry valide per occorrenza | # occorrenze |")
    lines.append("|---|---:|")
    for k, v in dist.items():
        lines.append(f"| {'4 o piu' if k >= 4 else k} | {v} |")
    lines.append("")
    lines.append("| Tipo di refactoring | Occorrenze | % |")
    lines.append("|---|---:|---:|")
    for rtype, count in type_counts.items():
        lines.append(f"| {rtype} | {count} | {pct(count, total_ops)} |")
    lines.append("")

    lines.append("### Tipologie di refactoring valide per smell\n")
    by_smell = exploded.groupby(["smell_name", "types"]).size().rename("occorrenze")
    for smell in per_smell.index:
        if smell not in by_smell.index.get_level_values(0):
            continue
        sub = by_smell.loc[smell].sort_values(ascending=False)
        lines.append(f"**`{smell}`** (totale: {int(sub.sum())})\n")
        lines.append("| Tipo di refactoring | Occorrenze |")
        lines.append("|---|---:|")
        for rtype, count in sub.items():
            lines.append(f"| {rtype} | {count} |")
        lines.append("")

    lines.extend(spearman_section(d, ok, cfg))
    return lines


# ---------------------------------------------------------------------------
# Report markdown
# ---------------------------------------------------------------------------
lines = [f"# Analisi dei refactoring validi (stesso file e stessa funzione) — subset `{SUBSET}`\n"]
lines.append(f"- Occorrenze di smell (una riga del CSV ciascuna): **{n_raw}**")
lines.append("- Refactoring **valido** = entry di PyRef nello stesso file (`same_file`) e sulla stessa funzione (`same_function`) dello smell")
lines.append("- Tipologie ricavate dalle entry gia' filtrate (`pyref_out_same_function_*`), non dall'elenco generico del commit\n")

for phase in PHASES:
    lines.extend(analyze(phase))

report = "\n".join(lines)
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(report)

print(report)