# House-Hold-Hub V1 — Product Requirements Document

| Campo | Valore |
|---|---|
| Prodotto | House-Hold-Hub |
| Versione del PRD | 0.2.3 (bozza per revisione) |
| Data | 2026-10-30 |
| Product owner | mdellapa |
| Ambito | V1, di cui MVP = milestone M0–M5 |

## Navigazione

| Documento | Contenuto |
|---|---|
| [requirements.md](requirements.md) | Requisiti funzionali (FR) e non funzionali (NFR) — fonte canonica |
| [domain-rules.md](domain-rules.md) | Glossario, regole di dominio (DR), matrice dei permessi |
| [roadmap.md](roadmap.md) | MVP, completamento V1 ed evoluzione successiva |
| [open-questions-and-risks.md](open-questions-and-risks.md) | Questioni aperte (Q), assunzioni (A), rischi (RISK) |
| [milestones/](milestones/) | Una scheda per milestone (M0–M6) |
| [stories/](stories/) | Una scheda per user story con criteri di accettazione e task |

## Convenzioni

**Origine di ogni requisito o regola**

- **C — Confermato**: richiesto esplicitamente dal product owner.
- **P — Proposta**: decisione di prodotto proposta in questo PRD. Vale come
  default per V1 finché non viene respinta in revisione.
- **A — Assunzione**: ipotesi di contesto non verificata; se si rivela falsa
  impatta i requisiti indicati.

**Identificatori stabili**: `FR-001`, `NFR-001`, `DR-001`, `M0`, `US-001`,
`AC-US-001-01`, `TASK-001`, `UC-01`, `Q-001`, `A-001`, `RISK-001`, `SM-01`.
Gli identificatori non vengono riutilizzati: un elemento eliminato resta
indicato come *ritirato*.

**Definition of Ready**: una storia è **READY** quando obiettivo, requisiti,
criteri di accettazione e dipendenze sono chiari e nessuna questione aperta
*bloccante* la riguarda. Le proposte (P) sono considerate risolte. Altrimenti
è **BLOCKED** e la scheda indica cosa manca.

READY riguarda l'implementazione. Una questione con
[gate di utilizzo](open-questions-and-risks.md#gate-di-utilizzo) non
impedisce READY: la scheda indica "uso con dati reali dopo il gate" e i
criteri interessati si implementano e si verificano con dati di prova.
L'uso con dati reali segue i [livelli di rilascio](roadmap.md#livelli-di-rilascio).

Il PRD è volutamente neutro rispetto a tecnologie, architettura, database e
interfacce tecniche: queste scelte appartengono a documenti di architettura
separati (vedi [Q-011](open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico)).

## Visione

House-Hold-Hub è una piattaforma web per gestire e pianificare le finanze
personali e familiari. Ogni persona tiene le proprie finanze private e decide
in modo selettivo cosa condividere con uno o più nuclei familiari, così che
la famiglia possa capire dove vanno i soldi e pianificare insieme senza
rinunciare alla riservatezza individuale.

## Problema

- Le spese mensili sono disperse su più conti, carte e persone: capire
  "quanto spendiamo in cene o carburante questo mese" richiede fogli di
  calcolo manuali.
- Gli strumenti esistenti sono o strettamente personali (nessuna
  dimensione familiare) o completamente condivisi (nessuna privacy).
- Le spese familiari pagate da conti personali, i giroconti e i doppi
  inserimenti rendono i totali aggregati inaffidabili.
- Senza un confronto tra budget e consuntivo la pianificazione resta
  un'intenzione.

## Obiettivi

| ID | Obiettivo | Origine |
|---|---|---|
| G-1 | Analisi mensile delle spese per categorie e sottocategorie personalizzabili, affidabile e senza doppi conteggi | C |
| G-2 | Pianificazione tramite budget personali e familiari con confronto previsto/consuntivo | C |
| G-3 | Privacy per default, condivisione e attribuzione selettive verso uno o più nuclei | C |
| G-4 | Caricamento dei dati a basso sforzo: inserimento manuale e importazione di estratti conto CSV/Excel | C |
| G-5 | Vista d'insieme di conti, abbonamenti e investimenti | C |

### Non-obiettivi per V1

- Sincronizzazione automatica con le banche (prevista nella
  [roadmap](roadmap.md#evoluzione-successiva-post-v1)).
- Esecuzione di pagamenti, bonifici o operazioni di investimento.
- Consulenza finanziaria o raccomandazioni d'investimento.
- Contabilità aziendale, fatturazione, dichiarazioni fiscali.
- Divisione delle spese e calcolo dei saldi tra membri ("chi deve a chi").

## Utenti e personas

| Persona | Descrizione | Bisogni principali |
|---|---|---|
| **Individuo** | Gestisce le sole finanze personali | Report mensile per categoria, budget, import rapido |
| **Partner in coppia** | Ha conti personali e partecipa a un nucleo con conto comune | Privacy sui conti personali, attribuzione delle spese familiari pagate dal proprio conto |
| **Amministratore del nucleo** | Organizza le finanze di famiglia | Inviti, categorie e budget familiari, conti del nucleo |
| **Membro di più nuclei** | Es. famiglia propria e casa condivisa con coinquilini, o supporto ai genitori | Isolamento netto tra nuclei, attribuzioni distinte per nucleo |

## Casi d'uso principali

| ID | Caso d'uso | Storie |
|---|---|---|
| UC-01 | Registrarsi e avere subito uno spazio personale privato | [US-001](stories/US-001-registration-and-personal-space.md), [US-002](stories/US-002-space-isolation.md) |
| UC-02 | Configurare i propri conti e la propria tassonomia di categorie | [US-003](stories/US-003-personal-accounts.md), [US-004](stories/US-004-categories.md) |
| UC-03 | Registrare spese, entrate e giroconti a mano | [US-005](stories/US-005-manual-transactions.md), [US-006](stories/US-006-transfers.md) |
| UC-04 | Importare l'estratto conto mensile senza duplicati e con categorizzazione automatica | [US-008](stories/US-008-file-import.md) – [US-012](stories/US-012-imported-transfer-matching.md) |
| UC-05 | Analizzare le spese del mese per categoria e sottocategoria | [US-007](stories/US-007-monthly-report.md) |
| UC-06 | Pianificare un budget mensile e verificarne il rispetto | [US-013](stories/US-013-budgets.md) |
| UC-07 | Creare un nucleo, invitare i membri, gestire ruoli | [US-014](stories/US-014-household-creation-and-invitations.md), [US-015](stories/US-015-household-roles-and-members.md) |
| UC-08 | Gestire un conto comune del nucleo | [US-016](stories/US-016-household-accounts-and-categories.md) |
| UC-09 | Mostrare un proprio conto al nucleo in sola lettura | [US-017](stories/US-017-read-only-sharing.md) |
| UC-10 | Attribuire al nucleo una spesa (anche parziale) pagata da un conto personale | [US-018](stories/US-018-transaction-attribution.md) |
| UC-11 | Analizzare spese e budget del nucleo | [US-019](stories/US-019-household-reports-and-budgets.md) |
| UC-12 | Esportare i propri dati o eliminare l'account | [US-020](stories/US-020-data-export.md), [US-021](stories/US-021-account-deletion.md) |
| UC-13 | Tenere traccia degli abbonamenti e dei rinnovi | [US-023](stories/US-023-subscriptions.md) |
| UC-14 | Seguire investimenti e patrimonio | [US-024](stories/US-024-investments-and-net-worth.md) |

## Ambito

- **MVP (M0–M5)**: spazi personali e nuclei, conti, movimenti, giroconti e
  trasferimenti tra spazi, categorie a due livelli, importazione con
  controllo duplicati, regole di categorizzazione, report mensile, budget,
  condivisione in lettura, attribuzione, esportazione dei dati personali e
  del nucleo, eliminazione dei dati. Il perimetro distingue elementi
  indispensabili, rinviabili e dipendenti da decisioni aperte
  ([roadmap](roadmap.md#perimetro-dellmvp)).
- **Completamento V1 (M6)**: abbonamenti, investimenti, patrimonio.
- **Fuori V1**: vedi [roadmap](roadmap.md) e i non-obiettivi sopra.

## Metriche di successo

Valori obiettivo proposti (P), da confermare dopo il primo periodo d'uso.
La misurazione deve usare solo dati aggregati e mai importi o descrizioni
dei movimenti ([NFR-010](requirements.md#requisiti-non-funzionali)).

| ID | Metrica | Obiettivo |
|---|---|---|
| SM-01 | Tempo per passare da un estratto conto mensile (≤ 300 righe) al report mensile categorizzato, misurato in test di usabilità | ≤ 10 minuti dal secondo mese d'uso |
| SM-02 | Quota di movimenti importati categorizzati automaticamente dalle regole, dal secondo mese | ≥ 70% |
| SM-03 | Accessi a dati fuori dal perimetro autorizzato (test di sicurezza e segnalazioni) | 0 |
| SM-04 | Report e budget conformi alle invarianti [DR-012](domain-rules.md#dr-012--invariante-dei-totali) sui dataset di verifica | 100% |
| SM-05 | Utenti attivi con almeno un budget definito entro 30 giorni dalla registrazione | ≥ 50% |
| SM-06 | Quota mediana di movimenti "Da categorizzare" a fine mese tra gli utenti attivi | ≤ 5% |

## Milestone e ordine di implementazione

| Milestone | Esito | Dipende da | Storie |
|---|---|---|---|
| [M0 — Fondamenta](milestones/M0-foundation.md) | Utenti, spazio personale, isolamento | — | US-001, US-002 |
| [M1 — Analisi mensile personale](milestones/M1-personal-monthly-analysis.md) | Conti, categorie, movimenti, giroconti, report mensile | M0 | US-003 – US-007 |
| [M2 — Importazione](milestones/M2-import.md) | Import CSV/Excel, duplicati, lotti, regole, abbinamento giroconti | M1 | US-008 – US-012 |
| [M3 — Budget](milestones/M3-budgets.md) | Budget mensili e confronto con il consuntivo | M1 | US-013 |
| [M4 — Nuclei familiari](milestones/M4-households.md) | Nuclei, ruoli, conti comuni, condivisione, attribuzione, report e budget del nucleo | M1, M2 (per US-016), M3 (per US-019) | US-014 – US-019 |
| [M5 — Privacy e controllo dei dati](milestones/M5-privacy-and-data-control.md) | Esportazione, eliminazione account, registro attività | M4 | US-020 – US-022 |
| [M6 — Abbonamenti e investimenti](milestones/M6-subscriptions-and-investments.md) | Abbonamenti, investimenti, patrimonio | M1 | US-023, US-024 |

Ordine consigliato: M0 → M1 → (M2 ∥ M3) → M4 → M5 → M6.
M2 e M3 sono indipendenti tra loro; M6 dipende da M1 (da M4 per
abbonamenti e posizioni del nucleo) e può essere anticipata se le priorità
cambiano. M4 e M5 sono autorizzate all'uso reale solo insieme e dopo il
[gate di utilizzo](open-questions-and-risks.md#gate-di-utilizzo) di Q-012
([livelli di rilascio](roadmap.md#livelli-di-rilascio)). Le storie di M4 vanno in ordine
US-014 → US-015 → (US-016 ∥ US-017) → US-018 → US-019.

## Stato delle storie

La colonna "Perimetro MVP" segue la classificazione della
[roadmap](roadmap.md#perimetro-dellmvp).

| Storia | Titolo | Milestone | Requisiti | DoR | Perimetro MVP |
|---|---|---|---|---|---|
| [US-001](stories/US-001-registration-and-personal-space.md) | Registrazione, accesso e spazio personale | M0 | FR-001, FR-002, FR-044 | READY | Indispensabile; AC-08 rinviabile; sezione sullo storico dei nuclei di AC-09 dipendente (Q-012) |
| [US-002](stories/US-002-space-isolation.md) | Isolamento degli spazi | M0 | FR-002, FR-005 | READY | Indispensabile |
| [US-003](stories/US-003-personal-accounts.md) | Gestione dei conti personali | M1 | FR-008, FR-009, FR-010 | READY | Indispensabile |
| [US-004](stories/US-004-categories.md) | Categorie e sottocategorie personalizzabili | M1 | FR-016, FR-017, FR-018 | READY | Indispensabile |
| [US-005](stories/US-005-manual-transactions.md) | Movimenti manuali | M1 | FR-012, FR-013, FR-015 | READY | Indispensabile |
| [US-006](stories/US-006-transfers.md) | Giroconti tra conti | M1 | FR-012, FR-014 | READY | Indispensabile; AC-08 verificato in M4 |
| [US-007](stories/US-007-monthly-report.md) | Report mensile per categoria | M1 | FR-030, FR-031, FR-032 | READY | Indispensabile; AC-05 rinviabile |
| [US-008](stories/US-008-file-import.md) | Importazione CSV/Excel | M2 | FR-020, FR-021, FR-022 | READY | Indispensabile; formato .xls rinviabile |
| [US-009](stories/US-009-duplicate-detection.md) | Rilevamento duplicati | M2 | FR-023 | READY | Indispensabile |
| [US-010](stories/US-010-import-batches.md) | Lotti di importazione annullabili | M2 | FR-024, FR-028 | READY | Indispensabile; AC-08 dipendente (Q-014) |
| [US-011](stories/US-011-categorization-rules.md) | Regole di categorizzazione | M2 | FR-019 | READY | Indispensabile |
| [US-012](stories/US-012-imported-transfer-matching.md) | Abbinamento dei giroconti importati | M2 | FR-025 | READY | Rinviabile |
| [US-013](stories/US-013-budgets.md) | Budget mensili | M3 | FR-034, FR-035, FR-036 | READY | Indispensabile |
| [US-014](stories/US-014-household-creation-and-invitations.md) | Creazione del nucleo e inviti | M4 | FR-003, FR-004, FR-005, FR-044 | READY | Indispensabile; AC-09 dipendente (Q-012) |
| [US-015](stories/US-015-household-roles-and-members.md) | Ruoli e gestione dei membri | M4 | FR-006, FR-007, FR-028, FR-045, FR-046 | READY per la progettazione; uso con dati reali dopo il gate di Q-012 | Indispensabile; AC-03, AC-04, AC-09 – AC-12 e AC-14 dipendenti (Q-012, Q-014) |
| [US-016](stories/US-016-household-accounts-and-categories.md) | Conti, movimenti e categorie del nucleo | M4 | FR-011, FR-014, FR-016 | READY | Indispensabile |
| [US-017](stories/US-017-read-only-sharing.md) | Condivisione in sola lettura | M4 | FR-026 | READY | Indispensabile (C) |
| [US-018](stories/US-018-transaction-attribution.md) | Attribuzione dei movimenti al nucleo | M4 | FR-027, FR-028, FR-029, FR-044 | READY; AC-11 dopo il gate di Q-012 | Indispensabile; AC-11 dipendente (Q-012) |
| [US-019](stories/US-019-household-reports-and-budgets.md) | Report e budget del nucleo | M4 | FR-030, FR-033, FR-034 | READY | Indispensabile |
| [US-020](stories/US-020-data-export.md) | Esportazione dei dati | M5 | FR-041, FR-046 | READY | Indispensabile; quote di ex membri e storiche in AC-06 dipendenti (Q-012) |
| [US-021](stories/US-021-account-deletion.md) | Eliminazione dell'account | M5 | FR-042, FR-044, FR-045 | READY per la progettazione; implementazione definitiva e uso con dati reali dopo il gate di Q-012 | Indispensabile per AC-01, AC-03 – AC-05, AC-09 – AC-11, AC-16, AC-19; gli altri dipendenti (Q-012, Q-015) |
| [US-022](stories/US-022-activity-log.md) | Registro attività di condivisione | M5 | FR-043 | READY | Indispensabile per l'audit minimo (AC-01, AC-04 – AC-06); registro completo (AC-02, AC-03, AC-07) rinviabile |
| [US-023](stories/US-023-subscriptions.md) | Abbonamenti | M6 | FR-037, FR-038 | READY | Fuori MVP (M6) |
| [US-024](stories/US-024-investments-and-net-worth.md) | Investimenti e patrimonio | M6 | FR-039, FR-040 | READY | Fuori MVP (M6) |

**Prerequisiti globali di implementazione e di apertura**: le storie sono
pronte dal punto di vista di prodotto, ma l'implementazione richiede prima
le decisioni di architettura e stack ([Q-011](open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico)),
che questo PRD non anticipa e che sono documentate nel
[documento di architettura](../../architecture/household-hub-v1/README.md)
(Q-011 chiusa: ADR-001 – ADR-006 approvati il 2026-10-30). I trattamenti elencati nel [gate di utilizzo](open-questions-and-risks.md#gate-di-utilizzo) di
[Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione)
possono essere implementati e verificati con dati di prova, ma non usati con
dati di utenti reali prima della chiusura di Q-012: per questo M4 e M5 sono
autorizzate all'uso reale solo insieme e dopo il gate ([livelli di rilascio](roadmap.md#livelli-di-rilascio)).

## Contesto del repository

Fatti verificati al 2026-10-27:

- Il repository `House-Hold-Hub/Documentation` contiene solo il `README.md`
  iniziale: non esistono PRD, ADR, specifiche API o convenzioni precedenti.
- L'organizzazione GitHub `House-Hold-Hub` non ha altri repository né issue
  aperte o chiuse su `Documentation`: non ci sono riferimenti da preservare.
- Non esiste codice applicativo: l'impatto è interamente greenfield e non
  ci sono comportamenti esistenti con cui entrare in conflitto.

Nessuna issue è stata creata: la copertura su issue tracker è da definire
quando il product owner lo richiederà.

## Revisioni

| Versione | Data | Modifiche |
|---|---|---|
| 0.1 | 2026-10-27 | Prima bozza per revisione |
| 0.2 | 2026-10-28 | Recepimento della Product Review: collegamento tecnico e capienza delle attribuzioni dopo uscita e rientro (DR-009, DR-010, DR-017, DR-023); trasferimenti tra spazi, rimborsi e quadratura dei saldi (DR-005, DR-007, DR-012, DR-014, DR-018); quote storiche senza accorpamenti distruttivi e opposizioni parziali o ripetute (DR-024, DR-025); proprietà e accessi delle attribuzioni (DR-001); duplicati uno a uno (DR-016); budget senza sovrapposizioni (DR-019); arrotondamento degli abbonamenti (DR-020); tutela dei dati condivisi (DR-026, FR-046); accesso del personale (NFR-013); informativa alla registrazione e all'ingresso (FR-044); gate di utilizzo di Q-012; nuove questioni Q-014 e Q-015; dipendenze e perimetro dell'MVP. Nessun identificativo esistente è stato riutilizzato o ritirato. |
| 0.2.1 | 2026-10-28 | Consolidamento: trasferimenti tra spazi registrabili da qualsiasi membro senza accesso ai conti personali altrui (DR-007, I-1); rivalidazione indivisibile dei preavvisi alla scadenza (DR-026, I-2); audit minimo indispensabile e registro completo rinviabile (FR-043, US-022, I-3); criteri di completamento e NFR al netto dei rinviabili (I-4); informativa generale alla registrazione distinta dalla sezione soggetta al gate (FR-044, I-5); trasferimenti tra spazi verificati in M4 (I-6); rettifica contabile dei movimenti vincolati distinta dall'opposizione (DR-023, I-7); Definition of Ready e livelli di rilascio, con MVP implementato distinto da MVP autorizzato all'uso reale (I-8, I-10); inaccessibilità immediata e cancellazione nei tempi di DR-024 (I-9); tracciabilità tra requisiti, questioni e storie (I-11); accesso degli operatori allineato a NFR-013 (I-12); nessuna correlazione visibile tra quote storiche o tra ex membri (I-13); arrotondamento degli abbonamenti con totali uguali alla somma delle righe (DR-020, I-14). Finalizzazione con le decisioni del product owner: rettifica contabile bloccata se viola la capienza, con riconciliazione esplicita e senza riduzione automatica, e autorizzazioni nei nuclei lasciati aperte in Q-014 (DR-023); conferma di audit minimo indispensabile e registro completo rinviabile (FR-043), con dipendenze e criteri di completamento allineati (US-022, M4, M5); conferma dei livelli di rilascio, con requisiti di sicurezza per dati reali già al livello 1, e del perimetro MVP; costo annuale effettivo distinto dall'equivalente mensile (DR-020, FR-038, US-023). Nessun identificativo esistente è stato riutilizzato o ritirato. |
| 0.2.2 | 2026-10-30 | Q-011 parzialmente risolta: approvati dal product owner stack di riferimento (Python con Django, PostgreSQL, HTMX), monolite modulare, pagine renderizzate dal server senza SPA e assenza di API pubbliche nella V1; collegamenti al documento di architettura e agli ADR-001 – ADR-006, nello stato Proposto; distinzione tra verifiche bloccanti prima di M0 e rinviabili; criterio di chiusura di Q-011 (aggiornati Q-011, prerequisiti globali e prerequisito di M0). Nessun requisito, regola o identificativo modificato. |
| 0.2.3 | 2026-10-30 | Q-011 chiusa con l'approvazione di ADR-001 – ADR-006 (ADR-005 nei principi): aggiornati Q-011, prerequisiti globali e scheda M0; aggiunto al criterio di completamento di M0 il completamento delle verifiche architetturali di M0, escluse le parti che dipendono dall'hosting. Nessun requisito, regola o identificativo modificato. |
