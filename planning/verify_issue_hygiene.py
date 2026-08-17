#!/usr/bin/env python3
"""Backlog issue-body hygiene verifier (R1-R7).

Redesigned after the Phase 4b audit, which found four defects the original Phase 4 checker missed.
Read-only. Always audits the LIVE GitHub bodies (R6), never a locally generated projection.

Usage:  python3 verify_issue_hygiene.py [--selftest] [--json OUT]
"""
import argparse, json, re, subprocess, sys

ORG = "House-Hold-Hub"
REPOS = ["Automation", "Backend", "Documentation", "Frontend", "Infrastructure"]
CANON_PREFIX = ("MVP", "IA", "HH", "TASK", "SHOP", "EXP", "INV", "DASH")

# ------------------------------------------------------------------ R1/R2/R3 rules
# R1: quantity patterns tolerate up to 3 intervening words between number and noun.
QTY = r"\b\d+\s*\+(?:\s*[\w/-]+){0,3}?\s*"
RULES = [
    ("H-01-test-quota", re.compile(QTY + r"(?:test cases?|tests|cases|scenarios)\b", re.I),
     "Arbitrary numeric test-count quota",
     "quality/testing-strategy.md §Purpose, §Coverage reporting"),
    ("H-02-coverage-gate",
     re.compile(r"coverage(?:\s*[\w/-]+){0,3}?\s*[:>≥]\s*[>≥]?\s*\d+\s*%?", re.I),
     "Merge-blocking coverage percentage", "quality/testing-strategy.md §Coverage reporting"),
    ("H-03-latency-gate", re.compile(r"<\s*\d+\s*ms\b|\b\d+\s*ms\b|\bwithin \d+ seconds?\b", re.I),
     "Unqualified latency gate", "quality/testing-strategy.md §Performance testing"),
    ("H-04-concurrency-gate", re.compile(r"\b\d+\s*concurrent users\b", re.I),
     "Unqualified concurrency gate", "quality/testing-strategy.md §Performance testing"),
    ("H-05-bundle-gate", re.compile(r"<\s*\d+\s*KB\b|bundle(?:\s*[\w/-]+){0,3}?\s*<\s*\d+", re.I),
     "Fixed bundle-size threshold", "product/roadmap.md §Numeric performance gates"),
    ("H-06-lighthouse-gate", re.compile(r"lighthouse(?:\s*[\w/-]+){0,3}?\s*[>≥]\s*\d+", re.I),
     "Fixed Lighthouse threshold", "product/roadmap.md §Numeric performance gates"),
    ("H-07-index-count", re.compile(QTY + r"indexes\b", re.I),
     "Asserted index count", "quality/testing-strategy.md; roadmap D06"),
    # R3: legacy requirement identifiers, excluding canonical prefixed forms
    ("H-08-legacy-fr", re.compile(r"(?<![A-Z-])\bFR-\d{1,2}\b(?:-\d{1,2})?", re.I),
     "Legacy monolithic-PRD requirement identifier", "product/prds/*.md §Legacy traceability"),
    # R2: archived snapshots, with or without an extension
    ("H-09-archived-doc",
     re.compile(r"\bERD(?:\.md)?\b|\bSYSTEM_DESIGN(?:\.md)?\b|\bDOMAIN_MODEL_[A-Z]+(?:\.md)?\b"
                r"|\bOPENAPI\.md\b|\bIMPLEMENTATION_PLAN[A-Z_]*(?:\.md)?\b"
                r"|\bGITHUB_ISSUES_PROPOSAL[A-Z_]*(?:\.md)?\b|\bFINAL_TECHNOLOGY_CHOICES(?:\.md)?\b", re.I),
     "Normative reference to an archived snapshot", "README.md §Archive policy"),
    ("H-10-amount-cents", re.compile(r"\bamount_cents\b"), "Superseded money field",
     "prd-expense-tracking.md EXP-FR-002/003"),
    ("H-11-google-id", re.compile(r"\bgoogle_id\b"), "Provider-specific identity field",
     "ADR-011; IA-FR-009"),
    ("H-12-password-hash", re.compile(r"\bpassword_hash\b"), "Bespoke password field",
     "ADR-011; architecture/domain-model.md"),
    ("H-13-django6", re.compile(r"\bDjango\s*6(?:\.\w+)?\b", re.I), "Superseded framework baseline",
     "ADR-010; architecture/technology-baseline.md"),
    ("H-14-status-422", re.compile(r"\b422\b"), "Status code the contract never returns",
     "ADR-014 §Error semantics; api/README.md"),
    ("H-15-deferred-vendor", re.compile(r"\bSendGrid\b|\bMailgun\b|\bAWS SES\b|\bSentry\b", re.I),
     "Vendor selected while D02 defers the choice", "roadmap D02; ADR-015"),
    ("H-16-samesite-strict", re.compile(r"SameSite\s*=\s*Strict", re.I),
     "Cookie policy contradicting OAuth redirects", "ADR-011"),
    ("H-17-obsolete-invite-route", re.compile(r"/invitations/\{?token\}?/accept|invitations/\{token\}", re.I),
     "Superseded invitation route", "ADR-013; api/openapi.yaml"),
    ("H-18-protect-payer", re.compile(r"\bPROTECT\b"), "PROTECT as payer-immutability mechanism",
     "prd-expense-tracking.md EXP-FR-013/014"),
    ("H-19-check-constraint", re.compile(r"check constraint(?:[^.\n]{0,60})household", re.I),
     "Cross-table CHECK claimed to guarantee same-household assignment", "ADR-012; TASK-FR-003"),
]

# R4: clause-level negation, including nominalized forms
NEG = re.compile(r"\b(no|not|never|neither|nor|without|remove[ds]?|removing|removal|drop(?:ped|s)?|"
                 r"forbid(?:den|s)?|exclude[ds]?|excluding|exclusion|superseded|supersedes|"
                 r"instead of|rather than|replaces?|replaced|replacement|must not|cannot|"
                 r"does not|is not|are not|no longer)\b", re.I)
FOOTER = "Reconciled from"


def clauses(line):
    return [c for c in re.split(r"[;.]|\s+—\s+", line) if c.strip()]


def affirmative(line, frag):
    for c in clauses(line):
        if frag in c:
            return not NEG.search(c)
    return not NEG.search(line)


def section(body, name):
    m = re.search(rf"^##+\s*{name}\s*$(.*?)(?=^##+\s|\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


def scan_body(body):
    """Return (findings, contradictions) for one body."""
    scope, ac = section(body, "Scope"), section(body, "Acceptance Criteria")
    found, contra = [], []
    for rid, rx, reason, src in RULES:
        ac_hits, scope_removal = [], bool(rx.search(scope)) and bool(NEG.search(scope))
        for m in rx.finditer(body):
            frag = m.group(0)
            if rid == "H-08-legacy-fr":
                ctx = body[max(0, m.start() - 6):m.start()]
                if any(ctx.upper().endswith(p + "-") or ctx.upper().endswith(p) for p in CANON_PREFIX):
                    continue
            line = next((l for l in body.splitlines() if frag in l), frag)
            if line.strip().startswith(FOOTER) or not affirmative(line, frag):
                continue
            found.append(dict(rule=rid, reason=reason, source=src, text=line.strip()[:160]))
            if frag in ac:
                ac_hits.append(line.strip()[:160])
        # R5: class-level Scope↔AC contradiction
        if scope_removal and ac_hits:
            for h in ac_hits:
                contra.append(dict(rule=rid, reason="Scope states this class was removed; "
                                                    "Acceptance Criteria still asserts it", text=h))
    return found, contra


# ------------------------------------------------------------------ R7 self-test
POSITIVE = [  # must fire — the four real Phase 4b defects plus class representatives
    ("H-01-test-quota", "- [ ] 20+ auth test cases (happy path + errors)"),
    ("H-01-test-quota", "- [ ] 50+ test cases"),
    ("H-08-legacy-fr", "- [ ] Last modified date shown per item (FR-58)"),
    ("H-08-legacy-fr", "- [ ] Optional grouping by category (FR-57)"),
    ("H-09-archived-doc", "- [ ] Model created, matches ERD"),
    ("H-09-archived-doc", "- [ ] Matches DOMAIN_MODEL_CORRECTED.md"),
    ("H-02-coverage-gate", "- [ ] Coverage: >95% of household code"),
    ("H-03-latency-gate", "- [ ] returns <200ms"),
    ("H-04-concurrency-gate", "- [ ] 100 concurrent users"),
    ("H-05-bundle-gate", "- [ ] Main bundle <500KB (gzip)"),
    ("H-06-lighthouse-gate", "- [ ] Lighthouse score >80"),
    ("H-10-amount-cents", "- [ ] Expense stores amount_cents"),
    ("H-11-google-id", "- [ ] User has google_id field"),
    ("H-13-django6", "- [ ] Initialize Django 6.x project"),
    ("H-14-status-422", "- [ ] Errors return 400/422"),
    ("H-15-deferred-vendor", "- [ ] Configure SendGrid for email"),
    ("H-16-samesite-strict", "- [ ] Cookie uses SameSite=Strict"),
    ("H-17-obsolete-invite-route", "- [ ] POST /invitations/{token}/accept"),
]
NEGATIVE = [  # must stay clean — real prohibition/supersession language from live bodies
    "- [ ] amount_minor is a strictly positive integer; no field named amount_cents exists.",
    "- [ ] The User model defines no bespoke password field and no provider-specific `google_id`.",
    "- [ ] Error responses use 400/401/403/404/409 only; no 422 is returned.",
    "- [ ] No operation returns 422.",
    "Remove 422 from the error set; validation failures return 400.",
    "Drop the archived OPENAPI.md reference and the fresh-developer gate.",
    "Replace the archived System Design and ERD references with the architecture overview.",
    "note the explicit exclusion of Jest.",
    "Replace numeric test-count and coverage gates with the behaviour/journey matrix.",
    "Rebuild around the canonical identity model: no bespoke password field, no google_id.",
    "- [ ] Requirements trace to INV-FR-005 and INV-FR-006.",
    "- [ ] Covered by TASK-FR-003 and HH-FR-016.",
]


def selftest():
    fails = []
    for rid, text in POSITIVE:
        f, _ = scan_body(f"## Acceptance Criteria\n{text}\n")
        if not any(x["rule"] == rid for x in f):
            fails.append(f"POSITIVE miss [{rid}]: {text!r}")
    for text in NEGATIVE:
        f, _ = scan_body(f"## Acceptance Criteria\n{text}\n")
        if f:
            fails.append(f"NEGATIVE fired [{f[0]['rule']}]: {text!r}")
    return fails


def fetch_live():
    live = {}
    for r in REPOS:
        out = subprocess.run(
            ["gh", "api", f"repos/{ORG}/{r}/issues?state=all&per_page=100", "--paginate",
             "-q", '.[]|select(.pull_request==null)|@json'],
            capture_output=True, text=True).stdout
        for line in out.strip().splitlines():
            o = json.loads(line)
            live[f"{r}#{o['number']}"] = o
    return live


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()

    st = selftest()
    print(f"R7 self-test: {len(POSITIVE)} positive fixtures, {len(NEGATIVE)} negative fixtures "
          f"-> {'PASS' if not st else 'FAIL'}")
    for s in st:
        print("   ", s)
    if a.selftest:
        sys.exit(1 if st else 0)

    live = fetch_live()
    report = {}
    tf = tc = 0
    for k, o in sorted(live.items()):
        f, c = scan_body(o["body"] or "")
        if f or c:
            report[k] = dict(findings=f, contradictions=c)
            tf += len(f)
            tc += len(c)
    print(f"R6 live audit: {len(live)} issues read from the GitHub API")
    print(f"  genuine findings: {tf} across {len(report)} issues")
    print(f"  Scope/AC contradictions: {tc}")
    for k, v in report.items():
        for x in v["findings"]:
            print(f"   {k:16} [{x['rule']}] {x['text']}")
    if a.json:
        json.dump(report, open(a.json, "w"), indent=1)
    sys.exit(1 if (st or tf or tc) else 0)
