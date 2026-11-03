# ADR-007 — Report calcolati in lettura e vista delle righe di report

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Approvato** (2026-11-03), con TASK-098. Le verifiche VER-023 (TASK-020) e VER-024 (TASK-103) restano obbligatorie |
| Data | 2026-11-03 |
| Decisore | mdellapa (product owner) |
| Requisiti | FR-030, FR-031, FR-032, NFR-001, NFR-004, NFR-005, NFR-006; [DR-007](../../../prd/household-hub-v1/domain-rules.md#dr-007--movimenti-tra-spazi-diversi), [DR-011](../../../prd/household-hub-v1/domain-rules.md#dr-011--perimetro-dei-report) – [DR-014](../../../prd/household-hub-v1/domain-rules.md#dr-014--rimborsi), [DR-018](../../../prd/household-hub-v1/domain-rules.md#dr-018--saldo-del-conto); [US-007](../../../prd/household-hub-v1/stories/US-007-monthly-report.md); RISK-002 |
| Correlati | [ADR-001](ADR-001-modular-monolith.md) (regole 2 e 6), [ADR-004](ADR-004-space-isolation-and-authorization.md), [ADR-005](ADR-005-persistence-and-monetary-amounts.md), [ADR-006](ADR-006-testing-and-continuous-integration.md); [§5.4 dell'architettura](../README.md#54-report-calcolati-in-lettura); [preparazione tecnica di M1](../M1-technical-preparation.md) |

## Contesto

Il report mensile deve essere coerente con i movimenti e aggiornato subito
dopo ogni modifica confermata (NFR-005), con le invarianti di DR-012 su ogni
mese; i rischi principali sono i doppi conteggi e i totali incoerenti
(RISK-002). Lo stesso calcolo servirà ai consuntivi dei budget (M3, DR-012
punto 6) e ai report del nucleo (M4), con quote attribuite e quote storiche.

ADR-005 rinvia a un ADR dedicato, prima di M1, la scelta dei report
calcolati in lettura e della vista delle righe di report; il §5.4
dell'architettura la propone. ADR-001 (regola 6) stabilisce che le letture
aggregate di `reporting` su tabelle di altri moduli passano solo da viste
SQL di cui `reporting` è proprietario. ADR-004 richiede che nessuna query su
dati di uno spazio sia eseguita senza il filtro del contesto d'accesso.

Vincoli del codice su `main` (verificati con la preparazione di M1):

- l'accesso filtrato passa da `for_context` dei modelli che estendono
  `SpaceOwnedModel`; `scoping_lint` (HH001) lo impone solo a quei modelli;
- ogni tabella di un `SpaceOwnedModel` deve avere il trigger di `space_id`
  immutabile (VER-014), che una vista non può avere;
- `config.provision_db` concede al ruolo applicativo `SELECT, INSERT,
  UPDATE, DELETE` su tutte le relazioni dello schema, viste comprese, e lo
  riapplica a ogni esecuzione.

## Decisione

### 1. Fonte unica

Report, dettaglio dei movimenti di ogni importo, voce "Da categorizzare",
confronto con i mesi precedenti (FR-031) e, da M3, consuntivi dei budget si
calcolano al momento della lettura da **una vista SQL delle righe di
report**. Nessun aggregato salvato, nessun contatore, nessuna cache dei
report (§8 dell'architettura).

### 2. Proprietà e collocazione

- La vista è di `reporting` ed è definita nelle sue migrazioni, eseguite
  dal ruolo proprietario (ADR-001, regola 6; ADR-004, «Database»). Le
  migrazioni dichiarano la dipendenza da quelle di `ledger` e
  `classification`.
- `reporting` non scrive: un comando avviato dalla pagina del report (es.
  categorizzare un movimento, FR-032) è un servizio di `ledger`; la pagina
  del report si aggiorna dopo il comando.
- Il saldo dei conti (DR-018) resta in `ledger`: non è un report. La
  quadratura (DR-012 punto 7) confronta i saldi di `ledger` con le righe
  della vista.

### 3. Righe della vista

Una riga per movimento dei conti dello spazio, di **ogni natura**: i
movimenti non ordinari servono alla quadratura e ai trasferimenti mostrati
fuori dai totali (FR-030). Colonne di M1:

| Colonna | Contenuto |
|---|---|
| `space_id` | Spazio del movimento |
| identificativi | Movimento, conto, categoria di primo livello e sottocategoria (nulle se "Da categorizzare" o non ordinario) |
| `date` | Data contabile del movimento (DR-013); il mese si seleziona per intervallo di date |
| tipo e natura | Entrata o uscita; ordinaria o giroconto. La natura «trasferimento tra spazi» si aggiunge in M4 (TASK-081) |
| `section` | `entrate`, `uscite` o `fuori_totali`: le uscite ordinarie e le entrate con categoria di spesa (rimborsi, DR-014) sono `uscite`; le altre entrate ordinarie sono `entrate`; i movimenti non ordinari sono `fuori_totali` (DR-005, DR-012 punto 5) |
| importo nel totale | Importo con segno nella propria sezione: positivo, negativo per i rimborsi; zero fuori dai totali |
| effetto sul saldo | Importo con segno sul saldo del conto: entrate in aumento, uscite in diminuzione, per ogni natura (DR-018) |

Le etichette di categorie e conti non stanno nella vista: le risolvono i
selettori dei moduli proprietari, così una rinomina vale subito per tutti i
mesi (AC-US-004-04). Le colonne sono ricavate in un solo punto (la
definizione della vista), così le invarianti 3 e 4 di DR-012 valgono per
costruzione del raggruppamento e il dettaglio di un importo somma
esattamente quell'importo (AC-US-007-03).

### 4. Isolamento

1. **Filtro per spazio nel contratto.** La vista si legge in Python solo
   tramite un modello di sola lettura che estende una base di
   `spaces.scoping` dedicata alle viste (D-15 della preparazione di M1): non
   gestito dalle migrazioni di Django, senza trigger, con `for_context` come
   unica porta d'ingresso e riconosciuto da `scoping_lint` (HH001) e da
   `check_models`. Nessun SQL scritto a mano nei selettori: l'eccezione di
   HH006 per `reporting` resta disponibile, ma non è usata dalla vista.
2. **Collegamenti nello stesso spazio.** I join della vista con conti e
   categorie usano la coppia `(space_id, id)`, garantita anche nel database
   dal vincolo composito di D-14: un collegamento errato non porterebbe
   righe o etichette di un altro spazio.
3. **Permessi del chiamante.** La vista è creata con
   `security_invoker = true`: le tabelle sottostanti si leggono con i
   permessi del ruolo applicativo e un'eventuale RLS futura (DEF-009) non è
   aggirata dal proprietario della vista.
4. **Sola lettura per costruzione.** La vista non è aggiornabile in modo
   automatico da PostgreSQL (join tra più tabelle): un tentativo di
   scrittura fallisce anche se `provision_db` concede i privilegi di
   scrittura su tutte le relazioni. Un test lo verifica sul catalogo
   (`is_insertable_into`, `is_updatable`), insieme a `security_invoker` e
   alla natura di vista della relazione.
5. **Test negativi.** Le pagine del report entrano nella matrice di
   accesso; i filtri manipolati con identificativi di altri spazi non
   restituiscono dati (AC-US-002-04).

### 5. Importi

Le somme sono calcolate dal database su `numeric` e convertite in `Money`
con la stessa validazione di ADR-005: nessun `float`, nessun arrotondamento.

### 6. Prestazioni

Con i volumi di A-005 il calcolo in lettura non richiede cache. Il filtro
per spazio e intervallo di date si appoggia a un indice dei movimenti su
`(space_id, date)`. NFR-006 si misura sulla pagina del report con 10.000
movimenti annui (AC-US-007-08, TASK-020). Se il limite non fosse rispettato,
una soluzione con dati precalcolati richiederebbe un nuovo ADR.

### 7. Estensioni previste

Le estensioni aggiungono righe o colonne alla stessa vista, senza un
secondo calcolo:

- **M3**: i consuntivi dei budget leggono le stesse righe (DR-012 punto 6
  per costruzione).
- **M4**: natura «trasferimento tra spazi» (fuori dai totali, mostrata a
  parte); nel nucleo, quote attribuite e quote storiche con le categorie
  del nucleo (DR-011); quote limitate durante un'opposizione escluse con un
  solo predicato (§7 dell'architettura, Q-012). Le regole di visibilità per
  destinatario sono dell'ADR previsto prima di M4.

## Da verificare

| ID | Verifica | Entro |
|---|---|---|
| VER-023 | Prestazioni del report calcolato in lettura sui volumi di NFR-006 (10.000 movimenti annui per spazio) | TASK-020 |
| VER-024 | Modello di sola lettura su vista: migrazioni con il ruolo proprietario, `security_invoker`, scritture rifiutate anche dopo la riesecuzione di `provision_db`, filtro di `for_context` e regole di `scoping_lint` | TASK-103 |

## Rinviato

- Quote attribuite, quote storiche e report del nucleo: M4, con l'ADR sulla
  visibilità per destinatario.
- Consuntivi dei budget: M3, sulle stesse righe.
- Confronto con i mesi precedenti (FR-031, AC-US-007-05): rinviabile nel
  perimetro dell'MVP; se realizzato, legge la stessa vista.

## Alternative considerate

| Alternativa | Motivo dello scarto |
|---|---|
| Aggregati salvati o contatori aggiornati a ogni scrittura | Invalidazioni su ogni modifica, rinomina, spostamento ed eliminazione di categorie: rischio diretto per NFR-005 e RISK-002 |
| Vista materializzata | Richiede aggiornamenti espliciti; i dati possono essere vecchi subito dopo una modifica (NFR-005) |
| SQL scritto a mano nei selettori, con lo spazio come parametro | Il filtro dipende dalla disciplina di ogni query e non dal contratto `for_context`; nessun controllo statico |
| Query di `reporting` sui modelli di `ledger` | Vietato da ADR-001 (regole 2 e 6) |
| Calcolo in Python dai movimenti | Duplica le regole di DR-011 – DR-014 fuori dal database e peggiora le prestazioni |

## Conseguenze

- Una sola definizione dei totali per report, dettaglio e, da M3,
  consuntivi; nessuna invalidazione.
- La vista dipende dallo schema di `ledger` e `classification`: una loro
  migrazione che cambia colonne usate dalla vista richiede una migrazione di
  `reporting`; i test del report lo rilevano.
- Il contratto di `spaces.scoping` si estende ai modelli di sola lettura
  su viste (D-15), con controlli propri al posto del trigger di VER-014.
- La correttezza resta verificata dall'oracolo delle invarianti e dal
  dataset di verifica (ADR-006, TASK-023), non presunta dalla struttura.
