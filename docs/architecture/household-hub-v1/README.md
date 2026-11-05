# Architettura software — House-Hold-Hub V1

| Campo | Valore |
|---|---|
| Documento | Architettura software, risposta a [Q-011](../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Versione | 0.2.6 (ADR indispensabili per M0 approvati; esiti delle verifiche di M0 registrati; M0.1 chiusa; decisioni tecniche di M1 e ADR-007 approvati; M3.1 approvata; ADR-008 proposto, in review) |
| Data | 2026-11-05 |
| Responsabile | mdellapa |
| Fonte dei requisiti | [PRD House-Hold-Hub V1](../../prd/household-hub-v1/README.md), versione 0.2.5 |
| Ambito | V1 (M0–M6), con il dettaglio delle decisioni necessarie prima di M0 |

## Navigazione

| Documento | Contenuto | Stato |
|---|---|---|
| [ADR-001](adr/ADR-001-modular-monolith.md) | Monolite modulare con app Django | Approvato; regola 2 revisionata il 2026-11-01 (superfici tecniche pubbliche, D-9 di M0.1) e il 2026-11-03 (superficie `core.money`, D-12 di M1) |
| [ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md) | Stack, versioni e interfaccia renderizzata dal server | Approvato |
| [ADR-003](adr/ADR-003-authentication-and-sessions.md) | Autenticazione e sessioni | Approvato |
| [ADR-004](adr/ADR-004-space-isolation-and-authorization.md) | Isolamento degli spazi e autorizzazione applicativa, senza RLS | Approvato; meccanismo di accesso filtrato scelto durante M0 (VER-016) |
| [ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md) | Convenzioni di persistenza, importi e invarianti | Approvato nei principi; meccanismi di trigger e contatori da verificare; termine di VER-012 precisato il 2026-11-03 (prima di TASK-017, D-10 di M1) |
| [ADR-006](adr/ADR-006-testing-and-continuous-integration.md) | Test e integrazione continua | Approvato; esiti di M0 registrati (limite accettato verificato) |
| [ADR-007](adr/ADR-007-read-time-reports.md) | Report calcolati in lettura e vista delle righe di report | Approvato (2026-11-03); VER-023 e VER-024 da completare nei task |
| [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md) | Invarianti concorrenti dei giroconti: esito di VER-012 e VER-013 | **Proposto** (2026-11-05): decisione tecnica approvata dal product owner, testo in review; approvazione prima di TASK-017 (AC-TS-006-03) |
| [M0.1](M0.1-structural-refactoring.md) | Milestone tecnica di refactoring strutturale tra M0 e M1: decisioni D-1 – D-9, storie tecniche, task e dipendenze | Approvata (2026-11-01); esiti registrati; **chiusa il 2026-11-03** |
| [M1 — preparazione tecnica](M1-technical-preparation.md) | Decisioni tecniche D-10 – D-18, storie tecniche TS-004 – TS-008, task, dipendenze e registrazione dei criteri di M1 | Approvata (2026-11-03); applicata dai task di M1 |
| [M3.1](M3.1-level-1-readiness.md) | Milestone tecnica di preparazione al livello 1: decisioni D-19 – D-22, condizioni vincolanti, eccezioni ammissibili, accesso esclusivo, storie tecniche TS-009 – TS-012 e task | Approvata (2026-11-03); non avviata |

## Convenzioni

**Stato delle decisioni**

- **Approvata**: decisa dal product owner. Si cambia solo con un nuovo ADR che la sostituisce.
- **Proposta**: principio raccomandato ma non ancora formalizzato in un ADR
  approvato; orienta la progettazione ma non va reso irreversibile prima
  dell'approvazione.
- **Da verificare** (`VER-nnn`): dettaglio che richiede una verifica tecnica
  (documentazione, prova, test di concorrenza) prima di essere adottato.
  Ogni voce indica quando va chiusa.
- **Rinviata** (`DEF-nnn`): scelta posticipata, con il momento o la
  condizione in cui va presa.

**Ciclo di vita di un ADR**: Proposto → Approvato → eventualmente Sostituito
da ADR-nnn. Un ADR approvato non si modifica nel merito: si sostituisce.

**Identificatori stabili**: `ADR-nnn`, `VER-nnn`, `DEF-nnn`, `RA-nnn`; per le
milestone tecniche `SR-nnn` (requisiti strutturali), `TS-nnn` (storie
tecniche) e `AC-TS-nnn-nn` (loro criteri di accettazione), con i task nella
numerazione globale `TASK-nnn` del PRD. Come nel PRD, gli identificatori non
vengono riutilizzati.

**Rapporto con il PRD**: il PRD resta la fonte dei requisiti e delle regole di
dominio; questo documento non li modifica. Le policy subordinate a
[Q-012](../../prd/household-hub-v1/open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione),
[Q-014](../../prd/household-hub-v1/open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro)
e [Q-015](../../prd/household-hub-v1/open-questions-and-risks.md#q-015--comportamento-alleliminazione-in-attesa-di-q-012)
non sono considerate definitive ([§7](#7-policy-subordinate-a-q-012-q-014-e-q-015)).

## 1. Decisioni approvate

Decisioni del product owner del 2026-10-30: prima stack e stile, poi, dopo la
Decision Review, gli ADR indispensabili per M0. Con la loro approvazione
[Q-011](../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico)
è chiusa.

| Decisione | Riferimento |
|---|---|
| Stack di riferimento della V1: Python, Django, PostgreSQL, HTMX | [ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md) |
| Monolite modulare: una sola applicazione, un solo database, un solo deploy | [ADR-001](adr/ADR-001-modular-monolith.md) |
| Pagine renderizzate dal server; nessuna SPA | [ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md) |
| Nessuna API pubblica nella V1 | [ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md) |
| ADR indispensabili prima di M0 | [ADR-001](adr/ADR-001-modular-monolith.md) – [ADR-006](adr/ADR-006-testing-and-continuous-integration.md) |
| Struttura del repository, organizzazione dei test e superfici tecniche pubbliche (2026-11-01) | [M0.1, D-1 – D-9](M0.1-structural-refactoring.md#decisioni); [§4.1](#41-struttura-del-repository); [ADR-001, regola 2](adr/ADR-001-modular-monolith.md) |
| Preparazione tecnica di M1: termine di VER-012 e VER-013, livelli dei moduli, superficie `core.money`, punti di estensione, collegamenti nello stesso spazio, modelli di sola lettura su viste, elenco delle relazioni, registrazione dei criteri, dati di test (2026-11-03) | [M1, D-10 – D-18](M1-technical-preparation.md#decisioni); [ADR-001, regola 2](adr/ADR-001-modular-monolith.md) |
| Report calcolati in lettura da una vista delle righe di report (2026-11-03) | [ADR-007](adr/ADR-007-read-time-reports.md) |
| Invarianti concorrenti dei giroconti: constraint trigger differito con serializzazione tramite `UPDATE` della riga padre, trigger in migrazioni `RunSQL` esplicite, nessun ripiego (decisione tecnica del 2026-11-05; il testo dell'ADR è in review) | [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md) |
| Preparazione al livello 1: autorizzazione, perimetro di M3.1, Compose locale facoltativo, artefatti di runtime subordinati all'ADR di hosting (2026-11-03) | [M3.1, D-19 – D-22](M3.1-level-1-readiness.md#decisioni) |

**Condizioni dell'approvazione**

- ADR-004: l'isolamento degli spazi è garantito come risultato; il meccanismo
  di accesso filtrato si sceglie durante M0 con VER-016. Nessuna garanzia sui
  tempi di risposta del 404.
- ADR-005: approvato nei principi (convenzioni di persistenza, importi,
  principio delle invarianti). I meccanismi di trigger e contatori del §3 non
  sono approvati e restano da verificare (VER-010 – VER-013).
- Le verifiche architetturali di M0 si completano durante M0
  ([§9](#9-dettagli-da-verificare)); le parti che dipendono dall'hosting
  seguono DEF-001.

## 2. Requisiti che guidano l'architettura

| Requisito | Fonte nel PRD | Conseguenza architetturale |
|---|---|---|
| Nessun accesso fuori perimetro, con esito uguale a una risorsa inesistente | NFR-001, DR-003, SM-03, RISK-001 | Autorizzazione in un solo punto, accesso ai dati filtrato per spazio, test negativi generati ([ADR-004](adr/ADR-004-space-isolation-and-authorization.md)) |
| Importi esatti al centesimo; capienza delle attribuzioni anche con operazioni concorrenti | NFR-004, DR-009, FR-028 | Tipo `Money` con validazione rigorosa; invarianti garantite nel database ([ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md)) |
| Operazioni indivisibili (rettifica con riconciliazione, preavvisi, giroconti, annullamento dei lotti) | DR-023 p.6, DR-026 p.5, DR-006, DR-017 | Transazioni ACID locali in un solo database: esclude architetture distribuite ([ADR-001](adr/ADR-001-modular-monolith.md)) |
| Report coerenti e aggiornati subito | NFR-005, DR-012 | Calcolo al momento della lettura da una fonte unica, senza aggregati salvati ([§5.4](#54-report-calcolati-in-lettura)) |
| File importati non conservati, contenuti mai eseguiti | NFR-011 | File effimero, anteprima non salvata ([§5.6](#56-importazione)) |
| Identità dell'ex membro nascosta subito | DR-023 p.2, NFR-005 | Visibilità calcolata in lettura, viste diverse per destinatario ([§5.5](#55-visibilità-per-destinatario)) |
| Cancellazione entro i tempi, backup ≤ 35 giorni, eliminazioni riapplicate dopo un ripristino | DR-024, NFR-012 | Cancellazione per modulo e registro delle eliminazioni fuori dai backup ([§5.7](#57-privacy-e-cancellazione)) |
| Operatori senza accesso ai dati tramite il prodotto | NFR-013, DR-002 | Nessun admin Django esposto; back-office del referente dedicato in M5 ([ADR-003](adr/ADR-003-authentication-and-sessions.md), DEF-010) |
| Requisiti di sicurezza completi già al livello 1 | [Livelli di rilascio](../../prd/household-hub-v1/roadmap.md#livelli-di-rilascio) | Hosting, backup e prova di ripristino decisi prima dell'uso reale (DEF-001) |
| Progetto personale con un solo sviluppatore | Contesto | Pochi componenti, nessun componente infrastrutturale prima che serva ([§8](#8-infrastruttura-minima-e-componenti-rinviati)) |

## 3. Vista d'insieme

```
 Browser (HTML + HTMX, it-IT)
      │ HTTPS · cookie di sessione · token CSRF
 ┌────▼──────────────────────────────────────────────────────┐
 │ Applicazione Django: un processo web, un deploy           │
 │                                                           │
 │  viste e template, per modulo                             │
 │  moduli: identity · spaces · classification · ledger ·    │
 │          imports · planning · reporting · privacy · audit │
 │  core:   Money · orologio · identificativi ·              │
 │          contesto d'accesso                               │
 └────┬───────────────────────────────────────┬──────────────┘
      │                                       │
 PostgreSQL                             Email transazionale
 (un database, uno schema)              (in sviluppo: console)
```

In M0 servono solo il processo web, PostgreSQL e l'invio delle email. Ogni
altro componente è rinviato al momento in cui un requisito lo richiede
([§8](#8-infrastruttura-minima-e-componenti-rinviati)).

## 4. Moduli

Ogni modulo è un'app Django con un'API pubblica di comandi e query; le regole
di dipendenza sono in [ADR-001](adr/ADR-001-modular-monolith.md). Un modulo
viene creato quando la prima milestone che lo usa inizia: M0 non contiene
moduli vuoti.

| Modulo | Responsabilità | Storie | Introdotto in |
|---|---|---|---|
| `core` | Tipo `Money`, orologio iniettabile, identificativi, contesto d'accesso | — | M0 |
| `identity` | Utenti, credenziali, sessioni, verifica email, recupero, verifica in due passaggi, ri-verifica dell'identità | US-001 | M0 |
| `spaces` | Spazi personali e nuclei, appartenenze per periodo, ruoli, inviti, preavvisi; matrice dei permessi; condivisioni in sola lettura | US-002, US-014, US-015, US-017 | M0 (spazio personale); M4 (nuclei) |
| `classification` | Tassonomie, categorie, regole di categorizzazione, eliminazione e unione con riassegnazione | US-004, US-011 | M1 |
| `ledger` | Conti, saldi, movimenti, giroconti, trasferimenti tra spazi; attribuzioni e quote storiche; rettifica contabile | US-003, US-005, US-006, US-016, US-018 | M1 (attribuzioni in M4) |
| `imports` | Sessioni di importazione, lettura dei file, mappatura, profili, duplicati, lotti, annullamento, abbinamento dei giroconti | US-008 – US-012 | M2 |
| `planning` | Budget; abbonamenti e posizioni d'investimento | US-013, US-019, US-023, US-024 | M3 (abbonamenti e posizioni in M6) |
| `reporting` | Sole letture: report mensile, consuntivi, patrimonio | US-007, US-019, US-024 | M1 |
| `audit` | Audit minimo del nucleo, poi registro completo; registro degli accessi del referente | US-022 | M4 |
| `privacy` | Esportazioni, eliminazione dell'account, opposizioni, registro delle eliminazioni | US-020, US-021 | M5 (progettazione in M4) |

Oltre ai moduli di dominio, `household-hub` contiene pacchetti non di dominio,
fuori dall'elenco di ADR-001:

| Pacchetto | Ruolo | Contratti tra moduli |
|---|---|---|
| `config` | Impostazioni, URL principali, WSGI, middleware HTTP, backend e ruoli del database, provisioning | Non è un modulo |
| `legal` | Informative (bozza provvisoria dell'informativa generale, US-001) | Esclusa per scelta esplicita (`LOCAL_APPS_NOT_COVERED`) |
| `testing` | Helper e infrastruttura condivisi dei test; app di prova `testing.probe`, installata solo nelle impostazioni dei test | Non è un modulo; vincolata da HH007 ([M0.1](M0.1-structural-refactoring.md)) |
| `tests` | Verifiche trasversali (dalla M0.1) | Non è un modulo |

### 4.1 Struttura del repository

Regole decise con [M0.1](M0.1-structural-refactoring.md#decisioni) il
2026-11-01. Si applicano con i task indicati. Applicazione verificata il
2026-11-03 con la [verifica di M0.1](https://github.com/House-Hold-Hub/household-hub/blob/main/docs/m0.1-verifica.md); esiti nella
[scheda](M0.1-structural-refactoring.md#esiti). Le ultime tre righe sono
decise per M1 il 2026-11-03 con la [scheda di preparazione tecnica](M1-technical-preparation.md#decisioni).

| Regola | Decisione | Applicata da |
|---|---|---|
| Ogni modulo è un pacchetto di primo livello del repository; nessuna directory `apps/` né `src/`. Si riesamina all'avvio di ogni milestone che introduce moduli | D-1 | Già in vigore |
| Le impostazioni restano i moduli `config/settings*.py`; il pacchetto `config/settings/` si riesamina con l'ADR di hosting (DEF-001, DEF-007) | D-2 | Già in vigore |
| Test di modulo in `<modulo>/tests/`; verifiche trasversali in `tests/`; helper condivisi in `testing/`. Ogni directory di test è un pacchetto con `__init__.py`; la radice del progetto si ricava da `settings.BASE_DIR` | D-3 | TASK-090 – TASK-092 (applicata) |
| Gli helper usati da più moduli stanno in `testing/`; quelli privati di un modulo nel suo `tests/`, non importabile dagli altri moduli | D-3 (C5) | TASK-090, TASK-092 (applicata) |
| Il codice di produzione non importa `testing.*` né pacchetti `tests`; `scoping_lint` esclude solo migrazioni e file e directory di test | D-3 (C2) | TASK-089 (applicata) |
| Template privati di un modulo in `<modulo>/templates/<modulo>/`; in `templates/` del progetto solo base, pagine di errore, override di allauth, layout e frammenti pubblici | D-4 | TASK-094 (applicata) |
| Helper dei test come semplici funzioni, senza nuove dipendenze; factory_boy si decide in M1 | D-5 | TASK-093 (applicata; era facoltativo, non rinviato) |
| Un modulo usa un altro modulo solo tramite `services`, `selectors` e le superfici tecniche pubbliche elencate in ADR-001, regola 2 | D-9 | Già in vigore in CI (VER-021) |
| I criteri automatizzabili delle storie tecniche (`AC-TS`) sono richiamati dai test come quelli del PRD; ogni PR registra solo quelli che soddisfa | D-8 | TASK-088 (applicata) |
| Livelli dei moduli in un ordine lineare: `identity > reporting > ledger > classification > spaces > core` | D-11 di M1 | Primo task di ogni modulo (TASK-008, TASK-011, TASK-019) |
| L'elenco delle relazioni attraversabili è un documento vivo di `household-hub`, non la verifica datata `docs/ver-016.md` | D-16 di M1 | TASK-102 |
| Un criterio di accettazione si cita e si registra in `REQUIRED_ACS` solo nella PR che ne verifica l'ultima condizione; i test intermedi citano il task | D-17 di M1 | Ogni PR di M1 |

## 5. Principi trasversali

Questi principi valgono con qualsiasi stack. Quelli necessari a M0 sono
dettagliati negli ADR; gli altri saranno formalizzati negli ADR del
[§10](#10-piano-degli-adr), prima della milestone che li usa.

### 5.1 Isolamento applicativo

Ogni risorsa appartiene a uno spazio; lo spazio è esplicito nell'URL; ogni
accesso ai dati passa da query filtrate per spazio. L'esito di una
risorsa fuori perimetro è identico a quello di una risorsa inesistente. La RLS
di PostgreSQL non è adottata in M0: garanzie, limiti e criterio di riesame
sono in [ADR-004](adr/ADR-004-space-isolation-and-authorization.md).
Stato: approvata; meccanismo di accesso filtrato scelto con VER-016.

### 5.2 Importi e date

Importi in `Decimal`, con tipo `Money` e validazione rigorosa: nessun
arrotondamento implicito, nessun `float`, un solo punto di arrotondamento
documentato ([DR-020](../../prd/household-hub-v1/domain-rules.md#dr-020--abbonamenti)).
Date contabili senza orario, fuso Europe/Rome per "oggi" e per i confini del
mese. Dettagli in [ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md).
Stato: approvata.

### 5.3 Invarianti nel database

Le invarianti finanziarie e di governance sono garantite dal database dove
possibile. Quelle che riguardano più righe sono verificate su una riga
"padre" che serializza le scritture concorrenti. Il principio è approvato in
[ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md); i meccanismi
concreti (trigger, vincoli differiti) restano da verificare con test di
concorrenza prima della milestone che li usa (VER-010 – VER-013). Per i
giroconti VER-012 e VER-013 sono **verificate sul piano tecnico** con
TASK-099 (2026-11-04); l'esito è formalizzato in
[ADR-008](adr/ADR-008-transfer-concurrent-invariants.md), che resta
**Proposto** fino all'approvazione formale del product owner. VER-010 e
VER-011 (capienza delle attribuzioni, almeno un amministratore) sono
**ancora pendenti** e restano da verificare prima di M4.

### 5.4 Report calcolati in lettura

Report, consuntivi di budget e "spese non pianificate" sono calcolati al
momento della lettura da un'unica vista delle righe di report: movimenti
ordinari, quote attribuite e quote storiche non limitate. Così il punto 6 di
[DR-012](../../prd/household-hub-v1/domain-rules.md#dr-012--invariante-dei-totali)
è garantito dalla fonte condivisa, perché consuntivi e report leggono le
stesse righe; il punto 7 (quadratura dei saldi) non deriva dalla vista e si
verifica esplicitamente confrontando i saldi di `ledger` con le righe della
vista, tramite l'oracolo delle invarianti
([ADR-006](adr/ADR-006-testing-and-continuous-integration.md),
[ADR-007](adr/ADR-007-read-time-reports.md)). NFR-005 non richiede
invalidazioni e il ricalcolo del ripiego di DR-024 non richiede elaborazioni.
Con i volumi di A-005 il limite di NFR-006 non richiede cache. Stato:
approvata con [ADR-007](adr/ADR-007-read-time-reports.md) il 2026-11-03.

### 5.5 Visibilità per destinatario

Ogni vista che mostra dati a un destinatario diverso dal titolare (membri del
nucleo, ex membro, referente) riceve oggetti dedicati con i soli campi
ammessi, mai istanze di modello. L'identità dell'autore di un'attribuzione è
calcolata in lettura dal periodo di appartenenza; uscita, rientro ed
eliminazione la nascondono subito senza riscrivere dati. Stato: la regola sugli
oggetti dedicati è approvata in
[ADR-004](adr/ADR-004-space-isolation-and-authorization.md); il resto va
formalizzato prima di M4.

### 5.6 Importazione

Il file caricato è effimero ed escluso dai backup. L'anteprima è calcolata,
non salvata. Alla conferma, sotto lock del conto, il controllo dei duplicati si
ripete e, se l'esito è cambiato, si torna all'anteprima. L'idempotenza è su due
livelli: la stessa richiesta (stato della sessione) e gli stessi dati
([DR-016](../../prd/household-hub-v1/domain-rules.md#dr-016--possibili-duplicati)).
L'abbinamento dei duplicati è deterministico. Stato: proposta, da formalizzare
prima di M2.

### 5.7 Privacy e cancellazione

Ogni modulo con dati personali implementa la propria esportazione e
cancellazione; `privacy` le coordina. Le eliminazioni sono annotate in un
registro conservato fuori dalla linea di backup del database, per
riapplicarle dopo un ripristino (NFR-012). Stato: proposta, da formalizzare
prima di M4 (progettazione) e M5 (realizzazione).

### 5.8 Audit

Le voci di audit si scrivono nella stessa transazione dell'azione. I registri
sono di sola aggiunta: il ruolo applicativo del database non ha permessi di
modifica; le cancellazioni previste da DR-024 passano da una procedura
dedicata. Stato: proposta, da formalizzare prima di M4.

## 6. Interfaccia

Pagine renderizzate dal server; HTMX aggiorna parti della pagina. Regole in
[ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md):

- htmx servito come file statico versionato, senza CDN e senza richieste a terzi;
- nessuna valutazione di codice nelle richieste HTMX (`allowEval` disattivato) e
  nessuna cache delle pagine nel browser;
- stessa autorizzazione per pagine intere e frammenti;
- nessun polling, che terrebbe aperte le sessioni oltre il timeout di
  inattività (NFR-003);
- HTML semantico, gestione del focus e annunci `aria-live` dopo le
  sostituzioni (NFR-008).

## 7. Policy subordinate a Q-012, Q-014 e Q-015

L'architettura non anticipa queste decisioni: le isola in punti di
configurazione o strategie sostituibili, così che l'esito cambi un
componente e non la struttura.

| Questione | Cosa resta aperto | Come l'architettura lo isola | Quando serve |
|---|---|---|---|
| Q-012 | Base giuridica e trattamenti del [gate di utilizzo](../../prd/household-hub-v1/open-questions-and-risks.md#gate-di-utilizzo) | Funzioni dei nuclei disattivabili per ambiente fino al superamento del gate; strategia di eliminazione configurabile (quote storiche o cancellazione con ricalcolo); inclusione delle quote limitate nei report come singolo predicato della vista di report; testi degli avvisi configurabili | Progettazione in M4; uso reale al livello 2 |
| Q-014 | Chi autorizza la riconciliazione nei nuclei lasciati; ritiro senza errore | Politica di riconciliazione sostituibile, con default "nega"; il modello conserva periodo di appartenenza e collegamento tecnico, quindi le alternative A e B sarebbero aggiunte | M4 (US-015, US-018) |
| Q-015 | Ordine di realizzazione tra quote storiche e ripiego | Le due strategie condividono la stessa interfaccia; il ripiego serve comunque per le opposizioni accolte | Prima di TASK-066 (M5) |

Nessuna di queste policy è realizzata in M0. Le fondazioni di M0 non
contengono assunzioni sul loro esito.

## 8. Infrastruttura minima e componenti rinviati

**Presenti in M0**: processo web Django, PostgreSQL, invio email (console in
sviluppo), integrazione continua su GitHub Actions
([ADR-006](adr/ADR-006-testing-and-continuous-integration.md)). La cache
condivisa per i limiti di tentativi usa PostgreSQL
([ADR-003](adr/ADR-003-authentication-and-sessions.md)).

| ID | Scelta rinviata | Quando o a quale condizione | Default fino ad allora |
|---|---|---|---|
| DEF-001 | Fornitore di hosting e database gestito. Criteri: dati in UE, PostgreSQL gestito con ripristino a un istante e conservazione dei backup configurabile ≤ 35 giorni, cifratura a riposo, rete privata, accordo sul trattamento dei dati. Comprende la parte di VER-004 sul rilevamento dell'IP dietro proxy e la conferma di VER-015 presso il fornitore, e la parte infrastrutturale di NFR-002 (cifratura in transito terminata dal proxy, cifratura a riposo, backup ed esportazioni temporanee; la parte applicativa è verificata in M0, [§9](#registrazioni-alla-chiusura-di-m0)) | Prima del livello 1 | Sviluppo locale e CI |
| DEF-002 | Provider email transazionale in UE | Prima del livello 1 | Backend email su console |
| DEF-003 | Esecuzione di attività periodiche (pulizie, scadenze) | M2, con la pulizia dei file di importazione | Nessuna; comandi di gestione eseguibili a mano |
| DEF-004 | Coda di lavori asincroni | Solo se un requisito richiede lavoro fuori dalla richiesta che non sia periodico | Non prevista nella V1 |
| DEF-005 | Archiviazione temporanea dei file di importazione | M2 (ADR di importazione) | — |
| DEF-006 | Object storage per esportazioni e registro delle eliminazioni | M5 | — |
| DEF-007 | Ambiente di staging separato | Prima del livello 1 | Nessun ambiente ospitato con dati reali |
| DEF-008 | Error tracking esterno | Dopo la valutazione rispetto a NFR-010 | Log strutturati senza importi né descrizioni |
| DEF-009 | Row-Level Security di PostgreSQL | Revisione di sicurezza di fine M4, prima del livello 2 ([ADR-004](adr/ADR-004-space-isolation-and-authorization.md)) | Isolamento applicativo |
| DEF-010 | Back-office del referente e account del personale | M5 | Nessun accesso del personale tramite il prodotto |
| DEF-011 | API per client esterni (es. app nativa) | Dopo la V1, su necessità, con un ADR dedicato | Nessuna API pubblica (approvato) |
| DEF-012 | Pipeline di rilascio continuo | Con DEF-001 | Solo integrazione continua |
| DEF-013 | Migrazione a htmx 4 | Quando htmx 4 diventa la versione "latest" (prevista a inizio 2027) | htmx 2.x |
| DEF-014 | Verifica in due passaggi per gli utenti (AC-US-001-08, rinviabile nel PRD) e passkey. **Rinviata dopo l'MVP** con la verifica di completamento di M0 (issue #15 di `household-hub`); la MFA va **rivalutata prima del livello 1** (uso reale), perché fino ad allora l'accesso degli utenti poggia sulla sola password con i limiti di ADR-003. Resta obbligatoria per il referente (NFR-013, DEF-010) | Dopo l'MVP; rivalutazione prima del livello 1 | TOTP disponibile nella libreria (`allauth.mfa`), non installato né esposto in M0 |
| DEF-015 | Strumenti di build per CSS e JavaScript | Solo se il CSS scritto a mano non basta | Nessuna toolchain Node |
| DEF-016 | Test di prestazioni periodici sui volumi di NFR-006 | M1–M2 | Nessuno |
| DEF-017 | Scansione dinamica di sicurezza su un ambiente ospitato | Prima del livello 1, con DEF-007 | Nessuna |
| DEF-018 | Container: Compose locale e artefatti di runtime ([D-21 e D-22 di M3.1](M3.1-level-1-readiness.md#decisioni)) | Compose locale solo per una necessità concreta; Dockerfile e Compose di runtime solo se richiesti dall'ADR di hosting | PostgreSQL installato in locale; in CI il servizio `postgres:18` |

Le scelte da fare «prima del livello 1» si chiudono in
[M3.1](M3.1-level-1-readiness.md), che distingue le condizioni vincolanti
dalle eccezioni ammissibili.

**Esclusi dalla V1 salvo necessità dimostrata**: Redis, broker di messaggi,
CDN, Kubernetes, microservizi, servizi di feature flag, cache dei report.

## 9. Dettagli da verificare

Nessuna verifica condiziona le decisioni approvate: la Decision Review del
2026-10-30 ha accertato che il loro esito può cambiare il meccanismo con cui
una decisione si realizza, non la decisione. Le verifiche sono di due classi:

- **Da completare durante M0**: il loro completamento fa parte del criterio
  di completamento di [M0](../../prd/household-hub-v1/milestones/M0-foundation.md).
  Le parti che dipendono dall'hosting seguono DEF-001, prima del livello 1.
- **Rinviabili**: si chiudono entro il momento indicato. Se una verifica
  fallisce, la decisione interessata si rivede con un nuovo ADR prima della
  milestone che la usa.

### Da completare durante M0

| ID | Verifica | ADR | Momento e dipendenze |
|---|---|---|---|
| VER-001 | Versioni effettive e compatibilità reciproca delle dipendenze, con l'ultima patch disponibile | ADR-002 | Avvio di M0 |
| VER-022 | Strumento di gestione delle dipendenze con lockfile e hash | ADR-006 | Avvio di M0 |
| VER-004 | Configurazione di django-allauth rispetto ai criteri di US-001, incluso il rilevamento dell'IP del client dietro proxy per i limiti di tentativi | ADR-003 | Durante M0, con i test di US-001; la parte sul proxy segue DEF-001 |
| VER-005 | Durata massima assoluta della sessione e comportamento alla scadenza nelle richieste HTMX | ADR-003 | Durante M0 |
| VER-006 | Chiusura delle altre sessioni al cambio e al recupero della password (AC-US-001-06) | ADR-003 | Durante M0, con i test di accettazione di US-001 |
| VER-014 | Meccanismo di immutabilità dello spazio di una risorsa | ADR-004 | Durante M0 |
| VER-015 | Ruoli distinti per applicazione e migrazioni | ADR-004 | Durante M0 in locale e in CI; conferma presso il fornitore con DEF-001 |
| VER-016 | Scelta del meccanismo di accesso filtrato per spazio e comportamento delle relazioni tra modelli | ADR-004 | Durante M0 (TASK-005) |
| VER-017 | Generazione della matrice di test negativi dall'elenco degli URL | ADR-006 | Durante M0 (TASK-007) |
| VER-018 | Formato degli identificativi (UUIDv7 di Python 3.14 o UUIDv4) | ADR-005 | Durante M0, prima del primo modello |
| VER-019 | Configurazione CSP compatibile con htmx e assenza di cache delle pagine nel browser | ADR-002 | Durante M0, con il template di base |
| VER-021 | Contratti di dipendenza tra moduli verificabili in CI | ADR-001 | Durante M0 |

### Esiti in M0

Esiti registrati con la verifica di completamento di M0 (2026-11-01, issue #15 di `household-hub`). I documenti di dettaglio sono nella cartella `docs/` di `household-hub` (repository privato); la sintesi di verifica è `docs/m0-verifica.md`. **Nessuna verifica ha avuto esito negativo e nessuna ha richiesto un nuovo ADR**: le decisioni approvate non cambiano.

| ID | Esito | Scelta o scostamento | Parte che resta su DEF-001 |
|---|---|---|---|
| VER-001 | Chiusa | Python 3.14.6, Django 6.1.2, PostgreSQL 18, django-allauth 65.21.1, django-htmx 1.29.0; compatibilità provata con controlli, migrazioni, test e avvio di gunicorn. Il supporto di Django 6.1 in django-htmx non è stato confrontato con il changelog ufficiale | — |
| VER-022 | Chiusa | uv con `uv.lock` e hash; un hash alterato fa fallire `uv sync --locked`; Dependabot configurato per `uv` e `github-actions` | — |
| VER-004 | Chiusa, tranne il proxy | allauth soddisfa AC-US-001-01..07 (AC-08 rinviato); tre comportamenti predefiniti corretti nel progetto (avviso che distingue un indirizzo appena usato, errore di lunghezza della password in inglese, email inviata prima del commit); limiti dei tentativi su cache condivisa in PostgreSQL; finestra di ri-autenticazione di 300 s (allauth ≥ 65.20: serve la password reinserita) | Rilevamento dell'IP dietro proxy (`TRUSTED_PROXY_COUNT`): senza configurazione i limiti per IP diventano globali |
| VER-005 | Chiusa | Scadenza scorrevole di 1.800 s e durata massima di 12 ore; le richieste htmx non autenticate ricevono `HX-Redirect` | — |
| VER-006 | Chiusa | Il cambio password conserva la sessione corrente e chiude le altre; il recupero le chiude tutte e non effettua l'accesso; collegamento monouso di 3.600 s misurato in UTC (scostamento dal predefinito di Django) | — |
| VER-014 | Chiusa | Immutabilità di `space_id` con trigger nel database, su ogni percorso di scrittura | — |
| VER-015 | Chiusa in locale e in CI | Due ruoli distinti, applicazione senza DDL; confermata dal job reale della CI | Conferma presso il fornitore di hosting |
| VER-016 | Chiusa | Selettori e servizi con contesto obbligatorio (`for_context`), verificati in CI con regole HH001–HH006; non un manager che filtra da sé | — |
| VER-017 | Chiusa | Matrice generata dall'URLconf: ogni vista è classificata o la suite fallisce; 23 URL e 608 casi in M0 | — |
| VER-018 | Chiusa | UUIDv4 (`core.ids.new_id`), non UUIDv7: l'istante di creazione non si deve dedurre dall'identificativo; la località degli indici è trascurabile ai volumi di NFR-006 | — |
| VER-019 | Chiusa | CSP senza `'unsafe-inline'` né `'unsafe-eval'`, htmx 2.0.11 in modalità sicura, nessuna cache delle pagine nel browser; storico di htmx in `sessionStorage` (non `localStorage` come in ADR-002), stessa contromisura | Proxy, HSTS, intestazioni sul percorso reale, controllo dinamico (DEF-017); prova della CSP su un solo motore di browser (il flusso di US-001 è stato poi provato dal product owner anche su Firefox e Safari) |
| VER-021 | Chiusa, con due strumenti | Import Linter per le regole 2 e 7 di ADR-001 (job `contracts`); la regola 3 sulle chiavi esterne è un test su registro dei modelli e migrazioni | — |

### Registrazioni alla chiusura di M0

- **Perimetro di NFR-002 in M0.** Verificata la **parte applicativa**: HTTPS forzato, HSTS, cookie `Secure` e `HttpOnly`, CSP, rifiuto dell'avvio con configurazione insicura (`check --deploy` con le impostazioni di produzione), nessun dato finanziario in sessione, log ed email (in M0 non esistono dati finanziari). **Non verificata** la parte infrastrutturale: cifratura in transito terminata dal proxy, cifratura a riposo, backup ed esportazioni temporanee, che dipendono dall'hosting e restano su DEF-001, prima del livello 1. Il criterio di completamento di M0 «NFR-002 verificato sulle funzioni della milestone» va letto in questo senso.
- **Verifica in due passaggi.** AC-US-001-08 e DEF-014 sono rinviati dopo l'MVP, con gli stessi identificativi ([perimetro dell'MVP](../../prd/household-hub-v1/roadmap.md#perimetro-dellmvp)); `allauth.mfa` non è installato. La MFA va rivalutata prima del livello 1. Per NFR-003, M0 verifica password robuste, limiti dei tentativi e scadenza delle sessioni, non l'autenticazione a due fattori.
- **Informativa.** L'informativa generale di M0 (AC-US-001-09, parte generale) è una **bozza provvisoria, dichiarata non approvata per l'uso con dati reali**: l'avviso compare sulla pagina dedicata e nella registrazione, i dati del titolare, le finalità ulteriori, l'hosting (DEF-001) e il provider email (DEF-002) sono segnaposto `[DA COMPLETARE]`, non si chiede alcun consenso. Resta da verificare con la revisione privacy di NFR-010 prima dell'uso con dati reali; la sezione sullo storico dei nuclei (FR-044) non esiste in M0 e dipende da Q-012.
- **Limite accettato di ADR-006 (decisione B1).** Verificato il 2026-11-01: repository privato su GitHub Free, branch protection non disponibile (risposta 403 dell'API), merge solo con squash, branch eliminati dopo il merge, Gitleaks sull'intera storia. Dalla PR #17, che introduce il workflow, la CI è **obbligatoria per procedura**: le tredici PR #17 e #21–#32 sono state unite con tutti i job verdi sull'ultimo commit (GitHub non prova che la verifica manuale sia avvenuta, solo che i controlli erano verdi). **Eccezione storica:** la PR #16 (bootstrap) è stata unita prima dell'esistenza della CI e resta documentata. Dependabot è attivo per `uv` e `github-actions` (aggiornamenti eseguiti il 2026-10-30, nessun alert aperto).
- **Stato di M0 — decisione del product owner (2026-11-01).** Autorizzata la chiusura della milestone al livello **«Implementato»**, solo con dati di prova, dopo il merge delle PR `household-hub#34` e `Documentation#2` e la chiusura dell'issue #15. Il product owner accetta per M0 l'eccezione storica della PR #16 senza CI e la verifica browser non esaustiva: prove positive dell'agente su Chromium 152 e del product owner su Firefox 159.0 (aarch64) e Safari 27.0.1 (build 22625.1.29.11.28), senza evidenza completa delle ultime due versioni dei principali browser richieste da NFR-007 né dettaglio dei singoli passi del product owner. Il viewport emulato a 360 px è accettato per M0; la matrice browser va rivalutata prima dell'uso reale. Restano aperti DEF-001, la revisione privacy dell'informativa e gli altri requisiti del livello 1. Nessun dato reale è autorizzato.

### Rinviabili

| ID | Verifica | ADR | Entro |
|---|---|---|---|
| VER-012 | Coerenza dei due lati dei giroconti | ADR-005 | Prima dell'implementazione di US-006 (TASK-017); non condiziona l'avvio di M1 ([D-10](M1-technical-preparation.md#d-10--termine-di-ver-012-e-ver-013)). **Verifica tecnica completata con TASK-099 (2026-11-04):** il meccanismo regge e non serve alcun ripiego; decisione tecnica approvata il 2026-11-05. **Prima di TASK-017** serve l'approvazione formale di [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md), oggi Proposto. AC-TS-006-03 è un criterio di processo verificato retrospettivamente in TASK-105 e non blocca l'avvio di TASK-017 dopo l'approvazione dell'ADR |
| VER-013 | Strumento con cui dichiarare e migrare i trigger | ADR-005 | Con la prima tra VER-010 – VER-012; per i giroconti prima di TASK-017. **Verifica tecnica completata con TASK-099 per i giroconti:** migrazioni Django `RunSQL` esplicite, senza nuove dipendenze ([ADR-008](adr/ADR-008-transfer-concurrent-invariants.md), Proposto fino all'approvazione formale); da riconfermare con VER-010 e VER-011, ancora pendenti |
| VER-007 | Comportamento di Django e psycopg con importi a più di due decimali: errore o arrotondamento silenzioso | ADR-005 | Prima dei primi importi (M1) |
| VER-008 | Parser degli importi in formato italiano, anche da tastiera di smartphone | ADR-005 | M1 |
| VER-020 | Accessibilità delle sostituzioni HTMX (focus, annunci) | ADR-002 | Primi flussi di M1 |
| VER-023 | Prestazioni del report calcolato in lettura sui volumi di NFR-006 | ADR-007 | TASK-020 |
| VER-024 | Modello di sola lettura su vista: ruoli, `security_invoker`, scritture rifiutate, filtro per spazio | ADR-007 | TASK-103 |
| VER-009 | Conversione dei numeri delle celle Excel in importi esatti | ADR-005 | M2, con i file di esempio di Q-008 |
| VER-010 | Capienza delle attribuzioni garantita nel database sotto concorrenza | ADR-005 | Prima di M4 (US-018) |
| VER-011 | Invariante "almeno un amministratore" garantita nel database sotto concorrenza | ADR-005 | Prima di M4 (US-015) |
| VER-002 | Piano di aggiornamento a Django 6.2 (uscita prevista il 2027-04-06) | ADR-002 | Entro il 2027-04; obbligatorio prima della fine del supporto esteso di 6.1 (2027-12) |
| VER-003 | Supporto di Python 3.15 nelle dipendenze; base attuale Python 3.14 | ADR-002 | Riesame a ogni aggiornamento di Django |

## 10. Piano degli ADR

**Prima di M0**: ADR-001 – ADR-006, approvati il 2026-10-30. La loro
approvazione ha chiuso
[Q-011](../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico);
gli ADR successivi non la riaprono.

**Successivi**, redatti appena prima della milestone che li richiede
(numerazione assegnata alla redazione):

| Tema | Entro |
|---|---|
| Report calcolati in lettura e vista delle righe di report | Prima di M1: [ADR-007](adr/ADR-007-read-time-reports.md), approvato il 2026-11-03 |
| Invarianti concorrenti: esito di VER-010 – VER-013 | Giroconti (VER-012, VER-013): [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md), redatto con TASK-100 e proposto il 2026-11-05 (decisione tecnica approvata, testo in review); da approvare prima di TASK-017. VER-010 e VER-011: aggiornamento prima di M4 |
| Hosting, ambienti, backup e ripristino, cifratura, accessi tecnici (NFR-002, NFR-012, NFR-013), accesso esclusivo degli utenti autorizzati e artefatti di runtime ([M3.1](M3.1-level-1-readiness.md)) | Prima del livello 1, dopo l'ADR di importazione (TASK-108) |
| Importazione: file, anteprima, duplicati, lotti, attività periodiche | Prima di M2 |
| Visibilità per destinatario, appartenenze, attribuzioni e quote | Prima di M4 |
| Audit e registri immutabili | Prima di M4 |
| Row-Level Security: decisione definitiva (DEF-009) | Revisione di sicurezza di fine M4 |
| Esportazione, cancellazione, opposizioni, registro delle eliminazioni | Progettazione in M4, prima di M5 |
| Back-office del referente (DEF-010) | M5 |

## 11. Rischi architetturali

| ID | Rischio | Mitigazione |
|---|---|---|
| RA-001 | L'isolamento è solo applicativo: una query non filtrata o una relazione attraversata in un template espone dati di altri spazi (RISK-001) | Accesso filtrato per spazio (meccanismo scelto con VER-016), oggetti dedicati per destinatario, matrice di test negativi, riesame della RLS (ADR-004, DEF-009) |
| RA-002 | I meccanismi previsti per le invarianti concorrenti non reggono sotto concorrenza | Verifiche VER-010 – VER-013 con test di concorrenza prima della milestone; alternative documentate in ADR-005 |
| RA-003 | La logica nel database (trigger) è poco visibile e difficile da manutenere | Ammessa solo per invarianti, dichiarata nel codice, testata esplicitamente |
| RA-004 | Il supporto di Django 6.1 termina a dicembre 2027 | Aggiornamento pianificato a 6.2 (VER-002) |
| RA-005 | I confini tra moduli dipendono da strumenti e disciplina, non dal linguaggio | Contratti di dipendenza in CI (VER-021) |
| RA-006 | La migrazione da htmx 2 a htmx 4 richiede modifiche agli attributi | Rinvio fino al rilascio "latest" (DEF-013), uso prudente dell'ereditarietà degli attributi |
| RA-007 | In un progetto personale sviluppatore e operatore coincidono (NFR-013) | Controllo procedurale e registrato degli accessi tecnici, da definire nell'ADR di hosting |
| RA-008 | Arrotondamenti silenziosi tra applicazione e database | Validazione rigorosa in `Money`, verifica VER-007 |

## Revisioni

| Versione | Data | Modifiche |
|---|---|---|
| 0.1 | 2026-10-30 | Prima bozza: stack e stile approvati dal product owner; ADR-001 – ADR-006 proposti; verifiche e rinvii elencati |
| 0.1.1 | 2026-10-30 | Verifiche divise tra bloccanti prima di M0 e rinviabili (§9, tabelle degli ADR); criterio di chiusura di Q-011 (§10); Q-011 aggiornata nel PRD come parzialmente risolta. Stato degli ADR invariato: Proposto |
| 0.2 | 2026-10-30 | Decision Review: ADR-001 – ADR-006 approvati (ADR-005 nei principi, non nei meccanismi di trigger e contatori); ADR-004 garantisce l'isolamento come risultato, con meccanismo scelto in VER-016, e non promette tempi indistinguibili per il 404; rimosso da ADR-002 il riferimento al framework Tasks; verifiche bloccanti riclassificate come da completare durante M0 (con VER-006, già prevista in M0), con le parti dipendenti dall'hosting assegnate a DEF-001; Q-011 chiusa. Nessun identificativo modificato |
| 0.2.1 | 2026-11-01 | Verifica di completamento di M0 (issue #15 di `household-hub`): fonte dei requisiti aggiornata al PRD 0.2.3; esiti delle 12 verifiche di M0 nel §9, con le parti rinviate a DEF-001; DEF-014 rinviata dopo l'MVP con la MFA da rivalutare prima del livello 1; perimetro di NFR-002 in M0 (parte applicativa verificata, parte infrastrutturale su DEF-001); informativa di M0 registrata come bozza provvisoria non approvata; limite accettato di ADR-006 verificato. Nessuna decisione approvata e nessun identificativo modificato |
| 0.2.2 | 2026-11-01 | Milestone tecnica [M0.1](M0.1-structural-refactoring.md) (TASK-095): decisioni D-1 – D-9 approvate dal product owner; nuovo §4.1 sulla struttura del repository e tabella dei pacchetti non di dominio (`config`, `legal`, `testing`, `tests`) nel §4; famiglie di identificativi `SR`, `TS` e `AC-TS`; regola 2 di ADR-001 revisionata in loco con l'elenco chiuso delle superfici tecniche pubbliche (D-9), senza cambiare il merito della decisione. Nessun requisito, VER, DEF o RA modificato |
| 0.2.3 | 2026-11-03 | Esiti di [M0.1](M0.1-structural-refactoring.md#esiti) (TASK-097): registrati nella scheda i risultati della [verifica di completamento](https://github.com/House-Hold-Hub/household-hub/blob/main/docs/m0.1-verifica.md) (TASK-096, PR #56 di `household-hub`) con riserve, anomalie e limiti dichiarati e le modifiche estranee (#47, #54); colonna «Applicata da» del §4.1 aggiornata con lo stato di applicazione; TASK-093 svolto e non rinviato. Nessuna decisione (D-1 – D-9), ADR, requisito, VER, DEF o RA modificato; la chiusura formale di M0.1 non è registrata |
| 0.2.4 | 2026-11-03 | Preparazione di M1 (TASK-098, issue #57 di `household-hub`): chiusura di M0.1 registrata (decisione del product owner del 2026-11-03); termine di VER-012 e VER-013 precisato in «prima dell'implementazione di US-006 (TASK-017)», senza condizionare l'avvio di M1 (§9, §10; revisione in loco di ADR-005); superficie `core.money` aggiunta alla regola 2 di ADR-001 (revisione in loco, D-12); [scheda di preparazione tecnica di M1](M1-technical-preparation.md) con le decisioni D-10 – D-18 approvate dal product owner (D-14 e D-15 nella soluzione progettuale, con le verifiche obbligatorie di TASK-102 e TASK-103); [ADR-007](adr/ADR-007-read-time-reports.md) approvato (§1, §5.4, §10), con VER-023 e VER-024 (§9); §5.4 allineato ad ADR-007 (punto 6 di DR-012 garantito dalla fonte condivisa, punto 7 verificato con l'oracolo); fonte dei requisiti aggiornata al PRD 0.2.4. Nessun requisito, VER, DEF o RA ritirato o riutilizzato |
| 0.2.5 | 2026-11-03 | Preparazione al livello 1 (TASK-107, issue #82 di `household-hub`): nuova scheda [M3.1](M3.1-level-1-readiness.md) con D-19 – D-22, condizioni vincolanti, inclusa la verifica di NFR-007, eccezioni ammissibili e accesso esclusivo; DEF-018 nel §8; ADR di hosting esteso nel §10 ad accesso esclusivo e artefatti di runtime; fonte dei requisiti aggiornata al PRD 0.2.5. Nessun ADR approvato cambia |
| 0.2.6 | 2026-11-05 | Invarianti concorrenti dei giroconti (TASK-100, issue #59 di `household-hub`): nuovo [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md) in stato Proposto, che formalizza la decisione tecnica approvata dal product owner il 2026-11-05 (constraint trigger differito con `UPDATE` della riga padre, trigger in migrazioni `RunSQL`, nessun ripiego) sulla base di ADR-005 §3, DR-006 e `docs/ver-012-013.md`; navigazione, §1, §5.3, §9 e §10 allineati (verifiche tecniche di VER-012 e VER-013 completate con TASK-099, distinte dall'approvazione formale di ADR-008, necessaria prima di TASK-017); VER-010 e VER-011 restano rinviate a M4. ADR-005 e il PRD non sono modificati; AC-TS-006-03 resta un criterio di processo, verificato retrospettivamente in TASK-105, che non blocca l'avvio di TASK-017 dopo l'approvazione dell'ADR. Nessun requisito, VER, DEF o RA ritirato o riutilizzato |
