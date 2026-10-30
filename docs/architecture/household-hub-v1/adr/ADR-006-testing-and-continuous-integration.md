# ADR-006 — Test e integrazione continua

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Approvato** (2026-10-30) |
| Data | 2026-10-30 |
| Revisione | 2026-10-30 — decisione B1: scansione dei segreti con Gitleaks e limite accettato dell'assenza di protezioni del repository (vedi [Limite accettato](#limite-accettato-decisione-b1)) |
| Decisore | mdellapa (product owner) |
| Questione | [Q-011](../../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Requisiti | NFR-001, NFR-004, NFR-005, NFR-007, NFR-008; SM-03, SM-04; TASK-007, TASK-023 |
| Correlati | [ADR-001](ADR-001-modular-monolith.md), [ADR-004](ADR-004-space-isolation-and-authorization.md), [ADR-005](ADR-005-persistence-and-monetary-amounts.md) |

## Contesto

Il PRD chiede, per ogni storia, test di accettazione automatizzati, una suite
di test negativi di accesso riusabile ed estesa a ogni milestone (US-002,
TASK-007) e un dataset di verifica condiviso per le invarianti dei report
(TASK-023, SM-04). Vincoli, lock e trigger del database
([ADR-005](ADR-005-persistence-and-monetary-amounts.md)) sono verificabili
solo sul database reale.

## Decisione

### Strumenti

| Ambito | Strumento |
|---|---|
| Esecuzione dei test | pytest con pytest-django |
| Database dei test | PostgreSQL, stessa versione principale della produzione, in locale e in CI. **Mai SQLite** |
| Dati di test | Fabbriche di oggetti (es. factory_boy); solo dati sintetici. **Mai dati reali** |
| Test property-based | Hypothesis |
| Interfaccia | Test client di Django, con verifica dell'HTML e delle intestazioni HTMX |
| End-to-end e accessibilità | Playwright con controlli automatici di accessibilità (axe), anche a 360 px |
| Analisi statica | ruff (lint e formattazione); mypy con gli stub di Django, rigoroso su `core` e sui servizi; contratti di dipendenza tra moduli ([ADR-001](ADR-001-modular-monolith.md)) |
| Dipendenze | Lockfile con hash (uv, VER-022); audit delle vulnerabilità delle dipendenze in CI; aggiornamenti automatici proposti come PR (Dependabot per `uv` e `github-actions`, cadenza settimanale) |
| Segreti | Gitleaks in CI, a versione fissata e con checksum verificato, sull'intera storia (decisione B1); sostituisce la scansione dei segreti di GitHub |

### Livelli di test

| Livello | Contenuto | Da |
|---|---|---|
| Unitari | Funzioni pure: `Money` e parser, regole di dominio, normalizzazione delle descrizioni, abbinamento dei duplicati | M0 per `core`; poi per milestone |
| Integrazione | Servizi con il database: vincoli, transazioni, effetti tra moduli | M0 |
| Viste | Pagine e frammenti tramite test client: permessi, esiti 404/403, contenuto, intestazioni HTMX | M0 |
| Matrice di accesso | Generata dall'elenco degli URL: per ogni vista e profilo (non autenticato, utente esterno; da M4 ex membro, membro di altro nucleo, ruolo insufficiente) l'esito atteso. Una vista senza permesso dichiarato o senza casi negativi fa fallire la suite | M0, estesa a ogni milestone |
| Concorrenza | Test con transazioni reali e più connessioni simultanee sulle invarianti di [ADR-005](ADR-005-persistence-and-monetary-amounts.md) §3 | Con le verifiche VER-010 – VER-012 |
| Oracolo delle invarianti | Funzione riusabile che verifica le invarianti di DR-012 sul database, eseguita sul dataset di verifica e dopo sequenze casuali di operazioni | M1 (TASK-023); estesa in M2–M5 |
| End-to-end | Pochi flussi critici: registrazione e accesso; poi inserimento, importazione, report, attribuzione | M1 |
| Prestazioni | Report e anteprima di importazione sui volumi di NFR-006 | M1–M2 (DEF-016) |

### Integrazione continua

- GitHub Actions su ogni pull request e su `main`.
- Passaggi: lint e formattazione, tipi, contratti tra moduli, test su
  PostgreSQL, audit delle dipendenze, scansione dei segreti (Gitleaks).
- Una modifica si integra solo con la CI superata. Senza branch protection
  la regola è procedurale: vedi [Limite accettato](#limite-accettato-decisione-b1).
- **Nessuna pipeline di rilascio** fino alla scelta dell'hosting (DEF-001, DEF-012).
- **Tracciabilità**: ogni criterio di accettazione del PRD è richiamato dal
  nome o dal marcatore di almeno un test (es. `AC-US-002-01`). Non si fissa
  una soglia numerica di copertura.

### Limite accettato (decisione B1)

Il repository è privato su GitHub Free: **branch protection, ruleset e push
protection dei segreti non sono disponibili**. Non si passa a un piano a
pagamento. Ne derivano:

- **La regola della CI è procedurale**: nessun push diretto su `main`; merge
  solo da pull request, con squash, dopo la verifica manuale che la CI sia
  verde; branch eliminati dopo il merge. Nulla lo impone tecnicamente.
- **Gitleaks sostituisce la scansione dei segreti di GitHub**: gira in CI su
  ogni pull request e su `main`, scansiona l'intera storia, con eccezioni
  minime e motivate in `.gitleaks.toml`. Rileva il segreto *dopo* il push, non
  lo impedisce.
- **Mitigazioni**: hook Gitleaks locale facoltativo (pre-commit); procedura di
  revoca e rotazione: un segreto finito su GitHub, anche in una PR chiusa o in
  un branch, si considera compromesso, si revoca e si ruota subito, senza
  affidarsi alla riscrittura della storia.
- **Condizioni di riesame**: prima del livello 1; con più contributori; se il
  repository diventa pubblico; se cambia il piano GitHub.

## Da verificare

| ID | Verifica | Entro |
|---|---|---|
| VER-017 | Generazione della matrice di accesso dall'elenco degli URL di Django, inclusi i frammenti HTMX e i parametri di spazio | Durante M0 (TASK-007) |
| VER-022 | Strumento per lockfile con hash, compatibile con la CI e con il fornitore di hosting | Avvio di M0 |

## Rinviato

| ID | Scelta | Quando |
|---|---|---|
| DEF-012 | Pipeline di rilascio | Con DEF-001 |
| DEF-016 | Test di prestazioni periodici sui volumi di NFR-006 | M1–M2 |
| DEF-017 | Scansione dinamica di sicurezza su un ambiente ospitato | Prima del livello 1, con DEF-007 |

## Alternative considerate

| Alternativa | Motivo dello scarto |
|---|---|
| SQLite per velocità | Non verifica vincoli, lock, trigger e tipi di PostgreSQL |
| Test end-to-end come base principale | Lenti e fragili; il test client copre gran parte dell'interfaccia renderizzata dal server |
| Soglia di copertura obbligatoria | Incentiva test poco significativi; la tracciabilità sui criteri di accettazione è più utile |

## Conseguenze

- La sicurezza dell'isolamento ([ADR-004](ADR-004-space-isolation-and-authorization.md))
  poggia in gran parte sulla matrice di accesso, che va mantenuta completa.
- La CI richiede un servizio PostgreSQL, unico componente esterno dei test.
