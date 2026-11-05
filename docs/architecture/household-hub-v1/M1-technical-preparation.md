# M1 — Preparazione tecnica

[← Architettura](README.md) · Precedente: [M0.1](M0.1-structural-refactoring.md) · Milestone di prodotto: [M1](../../prd/household-hub-v1/milestones/M1-personal-monthly-analysis.md)

| Campo | Valore |
|---|---|
| Tipo | Preparazione tecnica di una milestone di prodotto: decisioni, storie tecniche, task e dipendenze. Non modifica requisiti, regole di dominio o criteri di accettazione del PRD |
| Stato | **Approvata** (2026-11-03): D-10 – D-18 approvate dal product owner con TASK-098. Per D-14 e D-15 è approvata la soluzione progettuale; le verifiche di TASK-102 e TASK-103 restano obbligatorie. Esito di TASK-102 per D-14: [superate sul commit `b3a5f50`](#d-14--collegamenti-nello-stesso-spazio-garantiti-dal-database), PR non ancora unita a `main` |
| Decisore | mdellapa (product owner) |
| Collocazione | Dopo M0.1 (chiusa il 2026-11-03), prima e durante M1 |
| Repository interessati | `household-hub` (codice e test), `Documentation` (decisioni ed esiti) |
| Issue tracker | Milestone GitHub «M1 — Analisi mensile personale» e issue `[M1]` di `household-hub`: TASK-098 è l'issue #57; le altre si creano dopo l'unione di questa scheda |
| Correlati | [ADR-001](adr/ADR-001-modular-monolith.md), [ADR-004](adr/ADR-004-space-isolation-and-authorization.md), [ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md), [ADR-006](adr/ADR-006-testing-and-continuous-integration.md), [ADR-007](adr/ADR-007-read-time-reports.md), [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md); [consegne di M0.1](M0.1-structural-refactoring.md#consegne-a-m1) |

## Esito

Prima del primo task di codice di M1 sono decisi e registrati: il termine
delle verifiche sui giroconti, la collocazione dei moduli `classification`,
`ledger` e `reporting`, la superficie `core.money`, i punti di estensione tra
moduli, le garanzie del database sui collegamenti tra risorse, l'accesso ai
report, la registrazione dei criteri di accettazione e i dati di test.

**Approvazione e sviluppo sono separati.** Questa scheda e
[ADR-007](adr/ADR-007-read-time-reports.md) registrano le decisioni
(TASK-098); nessuna è applicata da TASK-098. Le applicano i task indicati,
ciascuno con la propria issue e i propri criteri.

## Perimetro

**In perimetro**: decisioni tecniche di M1, storie tecniche TS-004 – TS-008,
task di preparazione e funzionali con le dipendenze, registrazione dei
criteri di accettazione di M1.

**Fuori perimetro**:

- requisiti, regole di dominio e criteri del PRD (i criteri completati dopo
  M1 sono nel [PRD](../../prd/household-hub-v1/milestones/M1-personal-monthly-analysis.md#criteri-completati-nelle-milestone-successive));
- meccanismo delle invarianti dei giroconti: è l'esito di VER-012 e VER-013,
  registrato in [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md)
  (TASK-100), approvato il 2026-11-05;
- hosting, rilascio e livello 1 (DEF-001, DEF-012);
- moduli di M2 – M6.

## Decisioni

| ID | Decisione | Stato |
|---|---|---|
| D-10 | Termine di VER-012 e VER-013 | Approvata (2026-11-03) |
| D-11 | Livelli dei moduli | Approvata (2026-11-03) |
| D-12 | Superficie `core.money` | Approvata (2026-11-03) |
| D-13 | Punti di estensione tra moduli | Approvata (2026-11-03) |
| D-14 | Collegamenti nello stesso spazio garantiti dal database | Approvata (2026-11-03): soluzione progettuale; verifiche in TASK-102, superate sul commit `b3a5f50` (2026-11-05), integrazione in `main` in attesa |
| D-15 | Modelli di sola lettura su viste | Approvata (2026-11-03): soluzione progettuale; verifiche in TASK-103 |
| D-16 | Elenco vivo delle relazioni attraversabili | Approvata (2026-11-03) |
| D-17 | Registrazione dei criteri di accettazione | Approvata (2026-11-03) |
| D-18 | Dati di test | Approvata (2026-11-03) |

### D-10 — Termine di VER-012 e VER-013

VER-012 e VER-013 si completano prima dell'implementazione di US-006
(TASK-017, e quindi TASK-018), non prima dell'avvio di M1. TASK-099
(verifica) e TASK-100 (ADR delle invarianti) sono prerequisiti bloccanti di
TASK-017. È coerente con le «Conseguenze» di ADR-005; il testo è allineato
nel §9 e nel §10 dell'architettura e con una revisione in loco di ADR-005.

### D-11 — Livelli dei moduli

Ordine lineare dei livelli di Import Linter, dall'alto:
`identity > reporting > ledger > classification > spaces > core`.

- `classification` e `ledger` estendono `spaces.scoping`: stanno sopra
  `spaces`.
- `ledger` usa `classification.selectors` (tipo, categorie archiviate,
  albero delle categorie); `classification` non importa `ledger` (D-13).
- `reporting` legge `ledger` e `classification` tramite la propria vista
  SQL e i loro selettori.
- `identity` resta in cima, come oggi.
- L'ordine è lineare perché il test di completezza dei contratti confronta
  l'elenco dei livelli con `root_packages`; ogni modulo ha il proprio
  contratto `superficie-*` (lista di controllo del README di
  `household-hub`).

### D-12 — Superficie `core.money`

Il tipo `Money` di ADR-005 vive in `core.money`, aggiunto all'elenco chiuso
della regola 2 di ADR-001 (revisione in loco del 2026-11-03) e al contratto
`superficie-core` nella stessa modifica che introduce il tipo (TASK-101). La
sede del filtro di formattazione, che richiede un'app installata, si decide
in TASK-101.

### D-13 — Punti di estensione tra moduli

Dipendenze inverse tramite registri espliciti (ADR-001, regola 4), mai con
signals:

| Registro | Chi lo espone | Chi si registra | Uso |
|---|---|---|---|
| Inizializzatori di spazio | `spaces.services`, eseguiti nella transazione di creazione dello spazio | `classification` (M1) | Tassonomia predefinita di ogni nuovo spazio (AC-US-004-01; nuclei in AC-US-014-01) |
| Usi delle categorie | `classification.services` | `ledger` (M1); regole (TASK-035, M2) e budget (TASK-041, M3) | Categoria «in uso» e riassegnazione all'eliminazione (AC-US-004-06) |

**Spazi personali già esistenti.** Il registro vale per gli spazi creati
dopo l'introduzione di `classification`. TASK-011 deve dare la tassonomia
predefinita anche agli spazi personali creati prima. La strategia, scelta in
TASK-011, è idempotente: rieseguita, o applicata a uno spazio che ha già
categorie, non crea duplicati né modifica la tassonomia esistente. I test di
TASK-011 la verificano. Questa decisione non la implementa.

Alternativa scartata: far creare la tassonomia a `identity` dopo lo spazio
personale. Non coprirebbe i nuclei, creati in `spaces` (M4), che non può
importare `classification`.

### D-14 — Collegamenti nello stesso spazio garantiti dal database

Ogni `SpaceResourceForeignKey` ha nel database una chiave esterna composta
`(space_id, <colonna>) → (space_id, id)` della risorsa collegata. Rende
garantito dal database ciò che oggi garantiscono form e servizi (rischio
«Medio fino a M1» in `docs/ver-016.md` di `household-hub`).

- Django 6.1 non crea chiavi esterne composte: il vincolo è un'operazione
  di migrazione dedicata, come `ProtectSpaceId`, con
  `DEFERRABLE INITIALLY DEFERRED`.
- La risorsa di destinazione dichiara `UniqueConstraint(space, id)`,
  compatibile con `check_models` (lo spazio è nel vincolo).
- Una chiave nulla (es. movimento "Da categorizzare") non è verificata
  (`MATCH SIMPLE`); `space_id` è immutabile (VER-014), quindi il vincolo
  non è violato da cambi di spazio.
- Un test in CI verifica che ogni `SpaceResourceForeignKey` abbia il
  vincolo, con una prova negativa sulla risorsa di prova.
- Restano nei servizi, con test: compatibilità tra tipo del movimento e
  tipo della categoria (DR-008), due livelli di categorie, stesso tipo
  della sottocategoria e del padre.

**Approvazione.** È approvata la soluzione progettuale. Le verifiche di
TASK-102 (AC-TS-005-01, AC-TS-005-02) restano obbligatorie: se non sono
superate, la decisione si rivede prima dei task che la usano.

**Esito delle verifiche (TASK-102, 2026-11-05).** Positivo: la soluzione
approvata regge e la decisione non cambia. L'esito vale per il commit
[`b3a5f50`](https://github.com/House-Hold-Hub/household-hub/commit/b3a5f5070950c70d48c25395e663df4e339ae8fc) della PR [household-hub#86](https://github.com/House-Hold-Hub/household-hub/pull/86). **La PR non è ancora unita a `main`:** fino
all'unione il vincolo non è nel codice integrato, TASK-102 non è concluso e
AC-TS-005-01 e AC-TS-005-02 sono registrati in `REQUIRED_ACS` solo sul branch
della PR. Il commit di `main` va riportato qui dopo l'unione.

Verificato su quel commit, con PostgreSQL 18, ruolo applicativo e commit reali:

- **Forma del vincolo (AC-TS-005-01).** Ogni `SpaceResourceForeignKey` ha la
  chiave composta `MATCH SIMPLE`, `NO ACTION`, `DEFERRABLE INITIALLY DEFERRED`,
  creata dall'operazione reversibile `SameSpaceForeignKey`. Ne sono coperti i due
  collegamenti esistenti, entrambi su risorse di prova: `ProbeResource.parent`
  e `TransferSide.group`. Il controllo sul catalogo rileva un vincolo rimosso
  o indebolito (colonne o destinazione scambiate, `MATCH FULL`, azioni diverse,
  non differibile, `NOT VALID`); `check_models` rileva una destinazione senza
  `UniqueConstraint(space, id)`.
- **Rifiuto (AC-TS-005-02).** Il database rifiuta il collegamento a una risorsa
  di un altro spazio scritto con SQL diretto o con l'ORM, senza lasciare
  effetti. Senza il vincolo la stessa scrittura passa: la chiave esterna semplice
  di Django non basta.
- **Reversibilità.** Le migrazioni si annullano e si riapplicano sul database;
  una riga fuori regola ferma la migrazione in avanti.
- **Giroconti.** La chiave composta convive con il trigger di ADR-008:
  [nota successiva](adr/ADR-008-transfer-concurrent-invariants.md#2026-11-05--interazione-con-d-14-task-102).

Evidenze: [`test_same_space_links.py`](https://github.com/House-Hold-Hub/household-hub/blob/b3a5f5070950c70d48c25395e663df4e339ae8fc/spaces/tests/test_same_space_links.py) e controlli in
[`spaces/scoping_lint.py`](https://github.com/House-Hold-Hub/household-hub/blob/b3a5f5070950c70d48c25395e663df4e339ae8fc/spaces/scoping_lint.py) sul commit indicato;
le prove negative e le mutazioni sono riportate nella PR. In CI, i sei job
(`lint`, `typecheck`, `contracts`, `test` con PostgreSQL 18, `audit`,
`gitleaks`) sono verdi: [esecuzione `ci` 42044887334](https://github.com/House-Hold-Hub/household-hub/actions/runs/42044887334).

Limiti: la prova riguarda solo risorse di prova, quindi i modelli di M1
ricevono il vincolo con i loro task, sotto lo stesso controllo in CI. Una
migrazione che tocca la colonna collegata deve ricreare il vincolo, perché
PostgreSQL lo elimina insieme alla colonna; il controllo sul catalogo lo
segnala.

### D-15 — Modelli di sola lettura su viste

Una base di `spaces.scoping` per i modelli non gestiti che leggono una vista
SQL di uno spazio, come previsto da
[ADR-007](adr/ADR-007-read-time-reports.md): `for_context` come unica porta,
nessuna scrittura, riconosciuta da `scoping_lint` (HH001) e da
`check_models`. Al posto del trigger di VER-014 la verifica in CI controlla
che la relazione sia una vista con `security_invoker` e non aggiornabile.

**Approvazione.** È approvata la soluzione progettuale. Le verifiche di
TASK-103 (AC-TS-005-05, VER-024) restano obbligatorie: se non sono
superate, la decisione e ADR-007 si rivedono prima di TASK-019.

### D-16 — Elenco vivo delle relazioni attraversabili

Oggi `test_elenco_documentato_coincide_con_i_modelli` confronta i modelli
con la tabella di `docs/ver-016.md`, un documento di verifica datato che non
si riscrive. Ogni chiave esterna di M1 lo modificherebbe. L'elenco passa in
un documento vivo di `household-hub`, letto dal test; `docs/ver-016.md`
resta l'evidenza della verifica di M0.

### D-17 — Registrazione dei criteri di accettazione

- Un criterio si cita in un test e si registra in `REQUIRED_ACS` solo
  nella PR che ne implementa e verifica l'ultima condizione verificabile.
- Le PR che ne realizzano solo una parte la verificano con test che citano
  il task, non il criterio: il controllo di tracciabilità non distingue i
  criteri parziali e fallirebbe con un criterio citato e non registrato.
- I criteri che si completano dopo M1 sono elencati nel PRD con milestone e
  task di completamento; la verifica di M1 riporta per ciascuno le parti
  verificate in M1.
- Il controllo di tracciabilità non cambia.

### D-18 — Dati di test

Continua D-5 di M0.1: helper come semplici funzioni in `testing/` (condivisi)
e nei `tests/` dei moduli (privati), con creazione in blocco per i dataset
di volume (NFR-006). Nessuna nuova dipendenza: factory_boy non è adottato.
Il dataset di verifica e l'oracolo delle invarianti (ADR-006) stanno in
`testing/`, riusati in M3 e M4.

## Storie tecniche e criteri di accettazione

Legenda: **auto** = richiamato da un test e registrato in `REQUIRED_ACS`;
**processo** = verificato nella verifica di completamento di M1.

### TS-004 — Importi esatti

| ID | Criterio | Tipo | Task |
|---|---|---|---|
| AC-TS-004-01 | `Money` rifiuta `float`, valori non finiti, più di due decimali e valori fuori dall'intervallo di `numeric(12,2)`; aritmetica ammessa e vietata come in ADR-005 | auto | TASK-101 |
| AC-TS-004-02 | Il parser italiano accetta e rifiuta i casi della tabella di ADR-005, con il segno solo nei campi con segno; `parse(format(x)) == x` e associatività delle somme provate con test property-based | auto | TASK-101 |
| AC-TS-004-03 | Il campo del modello accetta e restituisce solo `Money`; un test documenta il comportamento di Django, psycopg e PostgreSQL con più di due decimali (VER-007) | auto | TASK-101 |
| AC-TS-004-04 | Una regola di lint segnala `float` e `Decimal` creati da `float` nei moduli con importi (prova negativa) | auto | TASK-101 |
| AC-TS-004-05 | Esiti di VER-007 e VER-008 documentati; la parte di VER-008 sulla tastiera degli smartphone è chiusa sul primo form con importi (TASK-008) | processo | TASK-101, TASK-008 |

### TS-005 — Contratto delle risorse e delle viste

| ID | Criterio | Tipo | Task |
|---|---|---|---|
| AC-TS-005-01 | Ogni `SpaceResourceForeignKey` ha la chiave esterna composta di D-14; prova negativa sulla risorsa di prova | auto | TASK-102 |
| AC-TS-005-02 | Il database rifiuta un collegamento a una risorsa di un altro spazio anche scritto senza form né servizio | auto | TASK-102 |
| AC-TS-005-03 | Un secondo invio dello stesso form restituisce la risorsa già creata; con l'identificativo di una risorsa di un altro spazio l'esito è quello di una risorsa inesistente (ADR-005) | auto | TASK-102 |
| AC-TS-005-04 | L'elenco vivo delle relazioni coincide con i modelli (D-16) | auto | TASK-102 |
| AC-TS-005-05 | Un modello di sola lettura su vista si legge solo con `for_context`, è riconosciuto da `scoping_lint` e non richiede il trigger di VER-014; la relazione è una vista con `security_invoker`, non aggiornabile anche dopo la riesecuzione di `provision_db` (VER-024) | auto | TASK-103 |

### TS-006 — Giroconti sotto concorrenza

| ID | Criterio | Tipo | Task |
|---|---|---|---|
| AC-TS-006-01 | Con transazioni concorrenti su più connessioni, i due lati di un giroconto restano nello stesso spazio, di pari importo e di direzione opposta, oppure l'operazione è rifiutata | auto | TASK-099 |
| AC-TS-006-02 | Esiti di VER-012 e VER-013 documentati, con lo strumento scelto per i trigger | processo | TASK-099 |
| AC-TS-006-03 | Il meccanismo o il ripiego (ADR-005, §3) è approvato in un ADR prima dell'avvio di TASK-017 ([ADR-008](adr/ADR-008-transfer-concurrent-invariants.md): approvato il 2026-11-05, prerequisito di TASK-017 soddisfatto; il criterio si verifica retrospettivamente in TASK-105) | processo | TASK-100 |

### TS-007 — Interfaccia verificata

| ID | Criterio | Tipo | Task |
|---|---|---|---|
| AC-TS-007-01 | Un job di CI esegue test end-to-end con Playwright e controlli axe, a versioni fissate, anche a 360 px (ADR-006) | auto | TASK-104 |
| AC-TS-007-02 | Dopo una sostituzione htmx il focus è gestito e l'esito è annunciato con `aria-live`, senza script inline (CSP) | auto | TASK-104 |
| AC-TS-007-03 | Esito di VER-020 documentato, con una prova su lettore di schermo | processo | TASK-104 |

### TS-008 — Decisioni ed esiti registrati

| ID | Criterio | Tipo | Task |
|---|---|---|---|
| AC-TS-008-01 | Prima dell'avvio di TASK-101, TASK-102 e TASK-103, `Documentation` registra la chiusura di M0.1, le decisioni D-10 – D-18, ADR-007 e la superficie `core.money` nella regola 2 di ADR-001 | processo | TASK-098 |
| AC-TS-008-02 | Nessun testo dell'architettura lega VER-012 o VER-013 all'avvio di M1; il termine è TASK-017 | processo | TASK-098 |
| AC-TS-008-03 | Il PRD indica, per ogni criterio completato dopo M1, la milestone e il task di completamento; i criteri di completamento di M2, M3 e M4 li comprendono | processo | TASK-098 |
| AC-TS-008-04 | La verifica di US-007 delimita le invarianti di DR-012 verificabili in M1 e quelle completate in M3 e M4, senza cambiare il significato dei criteri | processo | TASK-098 |
| AC-TS-008-05 | Nessuna modifica di merito a requisiti, regole di dominio, criteri di accettazione e ADR approvati, salvo le revisioni in loco dichiarate (ADR-001, ADR-005) | processo | TASK-098 |
| AC-TS-008-06 | Alla conclusione di M1, `Documentation` registra gli esiti, inclusi VER-007, VER-008, VER-012, VER-013, VER-020, VER-023 e VER-024, e collega la verifica | processo | TASK-106 |

## Task e dipendenze

Una issue per task, una PR per issue. I task del PRD (TASK-008 – TASK-023,
escluso TASK-081 di M4) mantengono la propria mappatura sui criteri; la
colonna «Registra» indica i criteri che la PR dichiara soddisfatti (D-17).

### Preparazione tecnica

| Task | Titolo | Storia | Dipende da |
|---|---|---|---|
| TASK-098 | Registrazione di M0.1, decisioni tecniche di M1 e ADR-007 (`Documentation`) | TS-008 | — |
| TASK-099 | Verifica di VER-013 e VER-012: giroconti sotto concorrenza | TS-006 | — |
| TASK-100 | ADR delle invarianti concorrenti dei giroconti (`Documentation`): [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md), approvato il 2026-11-05 | TS-006 | TASK-099 |
| TASK-101 | `Money`, parser italiano e persistenza esatta (VER-007, VER-008) | TS-004 | TASK-098 |
| TASK-102 | Collegamenti nello stesso spazio, doppio invio ed elenco vivo delle relazioni | TS-005 | TASK-098 |
| TASK-103 | Modelli di sola lettura su viste di uno spazio (VER-024) | TS-005 | TASK-098 |
| TASK-104 | Test end-to-end con Playwright e axe; accessibilità delle sostituzioni htmx (VER-020) | TS-007 | TASK-008 |

### Task funzionali

| Task | Storia | Registra | Dipende da |
|---|---|---|---|
| TASK-008 | US-003 | AC-US-003-02 | TASK-101, TASK-102 |
| TASK-011 | US-004 | AC-US-004-01 | TASK-102 |
| TASK-014 | US-005 | AC-US-005-02, 03 | TASK-008, TASK-011 |
| TASK-019 | US-007 | — (calcolo per i criteri registrati da TASK-017, TASK-020, TASK-010 e in M4) | TASK-014, TASK-103 |
| TASK-020 | US-007 | AC-US-007-03, 04, 08 (VER-023) | TASK-019 |
| TASK-009 | US-003 | AC-US-003-01, 03, 04; AC-US-005-01, 07 | TASK-014, TASK-020 |
| TASK-012 | US-004 | AC-US-004-02 – 05 | TASK-011, TASK-014, TASK-020 |
| TASK-013 | US-004 | AC-US-004-06, 07 | TASK-012 |
| TASK-015 | US-005 | AC-US-005-04, 05 | TASK-009, TASK-020 |
| TASK-017 | US-006 | AC-US-006-01, 03, 05; AC-US-007-01 | TASK-009, TASK-015, TASK-020, TASK-100 |
| TASK-016 | US-005 | AC-US-006-04 (AC-US-005-06 in M4) | TASK-017 |
| TASK-018 | US-006 | AC-US-006-07 (AC-US-006-06 in M4) | TASK-017 |
| TASK-010 | US-003 | AC-US-003-06; AC-US-007-07 (AC-US-003-05 in M2) | TASK-017, TASK-020 |
| TASK-023 | US-007 | — (dataset e oracolo; AC-US-007-02 e 09 in M4) | TASK-017, TASK-020 |
| TASK-022 | US-007 | AC-US-004-08; AC-US-007-06 | TASK-012, TASK-015, TASK-020, TASK-023 |
| TASK-021 | US-007 | AC-US-007-05, se non rinviato | TASK-020 |

### Chiusura

| Task | Titolo | Storia | Dipende da |
|---|---|---|---|
| TASK-105 | Verifica di completamento di M1 | — | Tutti i task precedenti (TASK-021 se non rinviato) |
| TASK-106 | Esiti di M1 (`Documentation`) | TS-008 | TASK-105 |

### Ordine

```
TASK-098 ∥ TASK-099 → TASK-100
TASK-098 → TASK-101 ∥ TASK-102 ∥ TASK-103
TASK-101 + TASK-102 → TASK-008 ∥ TASK-011 → TASK-014 → TASK-019 → TASK-020
TASK-020 → TASK-009 ∥ TASK-012 → TASK-015 ∥ TASK-013
TASK-015 + TASK-100 → TASK-017 → TASK-016 ∥ TASK-018 ∥ TASK-010 ∥ TASK-023 → TASK-022
→ TASK-021 (facoltativo) → TASK-105 → TASK-106            TASK-104 dopo TASK-008
```

Percorso critico: TASK-098 → TASK-101 → TASK-008 → TASK-014 → TASK-019 →
TASK-020 → TASK-009 → TASK-015 → TASK-017 → TASK-023 → TASK-022 → TASK-105.
TASK-099 e TASK-100 devono concludersi prima di TASK-017.

## Decisioni di prodotto da prendere prima del task

Non sono decisioni architetturali e non bloccano TASK-098.

| Tema | Entro |
|---|---|
| Contenuto della tassonomia predefinita (FR-017 ne fissa il minimo) | TASK-011 |
| Dove si consulta il saldo a fine mese (FR-009) | TASK-009 |
| Unicità dei nomi rispetto alle categorie archiviate | TASK-012 |
| Modificabilità dei movimenti esistenti di un conto archiviato | TASK-015 |
| Calcolo del «totale dei movimenti filtrati» (AC-US-005-06) | TASK-016 |
| Riattivazione di un conto con il nome di un conto attivo | TASK-010 |
| Perimetro delle «nuove assegnazioni» di AC-US-004-08 | TASK-022 |
| Realizzazione o rinvio di AC-US-007-05 | TASK-021 o TASK-105 |

## Rischi

| Rischio | Impatto | Mitigazione |
|---|---|---|
| Il meccanismo dei giroconti non regge sotto concorrenza (RA-002) | Ritardo di TASK-017 sul percorso critico | TASK-099 avviato subito, in parallelo; ripieghi già previsti da ADR-005. Esito: il meccanismo regge e nessun ripiego serve ([ADR-008](adr/ADR-008-transfer-concurrent-invariants.md)); restano i limiti della prova isolata |
| Totali incoerenti (RISK-002) | Report inaffidabile | Fonte unica (ADR-007), oracolo e dataset di verifica, registrazione dei criteri solo se completi |
| Arrotondamenti silenziosi (RA-008) | Importi errati | `Money` e VER-007 prima del primo campo importo |
| Collegamenti tra spazi diversi | Esposizione di dati (RISK-001) | D-14 e join per `(space_id, id)` nella vista |
| Scritture o letture non filtrate tramite la vista | Esposizione o alterazione di dati | D-15, `security_invoker`, vista non aggiornabile, test negativi |
| Cicli tra `classification` e `ledger` | Confini violati | D-11, D-13, Import Linter |
| Prestazioni del calcolo in lettura | NFR-006 non rispettato | Indice `(space_id, date)`, VER-023 in TASK-020 |

## Revisioni

| Data | Modifiche |
|---|---|
| 2026-11-03 | Prima versione (TASK-098): D-10 approvata; D-11 – D-18 proposte; storie tecniche TS-004 – TS-008, task, dipendenze e registrazione dei criteri di M1 |
| 2026-11-03 | Review della PR Documentation#5: D-13 integrata con gli spazi personali già esistenti (TASK-011); D-11 – D-18 approvate dal product owner, D-14 e D-15 nella soluzione progettuale con le verifiche obbligatorie di TASK-102 e TASK-103; stato della scheda «Approvata» |
| 2026-11-05 | TASK-100: [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md) proposto con l'esito di VER-012 e VER-013 (decisione tecnica approvata dal product owner, testo in review); riferimenti di D-10, TASK-100, AC-TS-006-03 e rischi allineati. Decisioni, criteri e task invariati; AC-TS-006-03 resta un criterio di processo verificato in TASK-105 |
| 2026-11-05 | TASK-100: approvazione formale di [ADR-008](adr/ADR-008-transfer-concurrent-invariants.md) da parte del product owner (versione `b97470a` della PR Documentation#7); prerequisito di TASK-017 (D-10) soddisfatto. Decisioni, criteri e task invariati; AC-TS-006-03 resta un criterio di processo da verificare retrospettivamente in TASK-105 |
| 2026-11-05 | TASK-102: esito positivo delle verifiche di D-14 registrato, con le evidenze, sul commit `b3a5f50` della PR household-hub#86, non ancora unita a `main`; [nota successiva in ADR-008](adr/ADR-008-transfer-concurrent-invariants.md#2026-11-05--interazione-con-d-14-task-102) sull'interazione con la chiave composta. Decisioni, criteri e task invariati |
