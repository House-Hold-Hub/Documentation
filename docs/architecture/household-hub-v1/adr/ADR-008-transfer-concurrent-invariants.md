# ADR-008 — Invarianti concorrenti dei giroconti

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Proposto** (2026-11-05): il testo richiede review prima dell'approvazione formale. La decisione tecnica che formalizza è **approvata dal product owner il 2026-11-05**; l'approvazione del testo la registrerà con una revisione di questo ADR |
| Data | 2026-11-05 |
| Decisore | mdellapa (product owner) |
| Questione | [Q-011](../../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Requisiti | NFR-004, NFR-005; [DR-006](../../../prd/household-hub-v1/domain-rules.md#dr-006--giroconti), [DR-012](../../../prd/household-hub-v1/domain-rules.md#dr-012--invariante-dei-totali); [US-006](../../../prd/household-hub-v1/stories/US-006-transfers.md); RISK-002 |
| Correlati | [ADR-004](ADR-004-space-isolation-and-authorization.md), [ADR-005](ADR-005-persistence-and-monetary-amounts.md) (§3), [ADR-006](ADR-006-testing-and-continuous-integration.md); [TS-006, D-10 e D-17](../M1-technical-preparation.md#ts-006--giroconti-sotto-concorrenza); evidenze: [`docs/ver-012-013.md`](https://github.com/House-Hold-Hub/household-hub/blob/main/docs/ver-012-013.md) di `household-hub` (TASK-099, issue #58) |

## Contesto

[ADR-005](ADR-005-persistence-and-monetary-amounts.md) (§3) approva il
principio delle invarianti concorrenti (una riga padre comune, aggiornata
nella stessa transazione) ma non ne approva i meccanismi, e rinvia l'esito
delle verifiche a un ADR dedicato. Per i giroconti il candidato era VER-012
(vincolo differito sul gruppo del giroconto), con VER-013 per lo strumento
dei trigger. [D-10](../M1-technical-preparation.md#d-10--termine-di-ver-012-e-ver-013)
fissa il termine: l'ADR è prerequisito bloccante di TASK-017 (AC-TS-006-03).

[DR-006](../../../prd/household-hub-v1/domain-rules.md#dr-006--giroconti)
definisce il giroconto: un'uscita su un conto e un'entrata di pari importo su
un altro conto dello stesso spazio. TASK-099 ha provato il candidato su
PostgreSQL reale con connessioni concorrenti e ne ha registrato l'esito in
`docs/ver-012-013.md`. Questo ADR formalizza la decisione che ne deriva; non
introduce requisiti né regole di dominio.

## Decisione

Approvata dal product owner il 2026-11-05.

### 1. Meccanismo

Un **constraint trigger differito** (`DEFERRABLE INITIALLY DEFERRED`) verifica
l'invariante del giroconto a fine transazione. La concorrenza è gestita con la
**serializzazione tramite `UPDATE` della riga padre** (la riga del gruppo del
giroconto): per ogni riga di lato scritta, il controllo aggiorna prima la riga
del gruppo, quindi legge i due lati con una sola query.

- Chi arriva dopo attende il commit di chi è arrivato prima e vede lo stato
  aggiornato, come previsto dal principio di ADR-005 §3.
- **Non basta un lock.** Un `SELECT … FOR NO KEY UPDATE` sulla riga padre
  regge in `READ COMMITTED` ma non in `REPEATABLE READ`: il controllo
  rilegge un'istantanea vecchia e la violazione passa. Serve l'`UPDATE`.
- **Non basta il vincolo differito.** Senza la riga padre, due commit
  incrociati possono eseguire il controllo prima che l'altro sia visibile.
- **L'ordine fisso di scrittura dei lati non protegge l'invariante:** serve
  solo a evitare i deadlock. Una scrittura in ordine inverso viene rifiutata
  dal database (`40P01`) senza danni ai dati.
- Un rifiuto è un errore di integrità (`23000`, `IntegrityError` in Django) con
  nome del vincolo riconoscibile dal servizio senza leggere il testo.

### 2. Invariante garantita dal database

Un giroconto ha **esattamente due lati**, con:

1. **direzioni opposte** (un'uscita e un'entrata);
2. **importi uguali**;
3. **stesso spazio**, anche del gruppo;
4. **conti distinti** (DR-006: «su un altro conto»).

La regola dei conti distinti entra quindi nell'invariante del database. Le
altre garanzie su una riga o su una coppia di righe restano vincoli
ordinari: importo > 0 e direzione nota (`CHECK`), un lato per direzione in un
gruppo (`UNIQUE`), spazio immutabile (VER-014), esistenza del gruppo (chiave
esterna differita). La struttura dei nomi e delle colonne del modello reale è
definita da TASK-017; quella della prova isolata (`testing.transfer_probe`) non
è vincolante.

### 3. Strumento: migrazioni Django `RunSQL` esplicite

Funzione e trigger si dichiarano con migrazioni Django `RunSQL` scritte a
mano, con `reverse_sql`, **senza nuove dipendenze**. È la convenzione già in
uso (VER-014).

- **`django-pgtrigger` escluso.** La sua funzione `ignore` è un parametro di
  sessione (`pgtrigger.ignore`) che il ruolo applicativo può impostare, e i
  trigger lo controllano prima della logica: un lato incoerente è stato
  committato col ruolo applicativo. Il vincolo non sarebbe più indipendente
  dalla disciplina dell'applicazione, come invece richiede ADR-005 §3.
  Inoltre non copre la funzione condivisa tra i trigger, che finirebbe
  comunque in una migrazione.
- **`django-migrate-sql-deux` non adottata.** È sicura e reversibile, ma
  sostituisce `makemigrations` e `migrate` per pochi oggetti SQL
  (i meccanismi candidati in V1 sono tre). Si può riesaminare se gli oggetti
  SQL crescessero molto.
- **Costo accettato:** una modifica alla funzione si scrive a mano, con tutta
  la funzione, e le migrazioni non sono coperte da `makemigrations --check`.
  Lo compensano un test sul catalogo (trigger attivi) e la prova di andata e
  ritorno della migrazione. In produzione le migrazioni restano solo in
  avanti (ADR-005).

### 4. Ripiego

**Nessun ripiego è necessario.** Le alternative di ADR-005 §3 (`SERIALIZABLE`
limitato alle operazioni; lock applicativo sulla riga padre) non sono state
provate e non sono adottate. `select_for_update` nei servizi resta ammesso per
coordinare le operazioni e dare messaggi precisi, non come garanzia.

### 5. Ambito: VER-010 e VER-011

**VER-010 (capienza delle attribuzioni) e VER-011 (almeno un amministratore)
restano rinviate a M4**, con i termini di ADR-005 (prima di US-018 e di
US-015). Questo ADR non ne approva né ne preclude i meccanismi. Ne riusa
l'infrastruttura di concorrenza `testing/concurrency.py`, già generica, ma
non il meccanismo dei giroconti. La parte di VER-013 che riguarda lo strumento
dei trigger vale per i giroconti; per VER-010 e VER-011 lo strumento si
riconferma con la loro verifica.

## Garanzie dimostrate

Dimostrate su prova isolata (`testing.transfer_probe`), PostgreSQL 18.6, ruolo
applicativo, commit reali (`docs/ver-012-013.md`; criterio AC-TS-006-01
registrato in `REQUIRED_ACS`):

- ogni scenario concorrente provato (16 interleaving imposti, osservati nel
  catalogo dei lock e non basati sul tempo) mantiene l'invariante o è rifiutato
  per intero, senza modificare lo stato precedente;
- una prova di carico con 4 connessioni e 20 operazioni casuali ciascuna non
  trova violazioni; l'esito non dipende dal particolare interleaving;
- tutti i percorsi di scrittura provati (SQL diretto, `MERGE`, `ON CONFLICT`,
  CTE con scrittura, ORM con `save`, `bulk_*`, `update_or_create`,
  eliminazioni e cascata) rispettano l'invariante o sono rifiutati;
- il ruolo applicativo non può disattivare o alterare il vincolo
  (`DISABLE TRIGGER`, `DROP TRIGGER`, `DROP FUNCTION`,
  `CREATE OR REPLACE FUNCTION`, `SET session_replication_role`, `TRUNCATE`
  sono rifiutati con `42501`); `SET CONSTRAINTS` può solo anticipare il
  controllo;
- i controlli negativi mostrano che le prove non sono vuote: con solo il
  vincolo differito o con solo il lock sulla riga padre l'invariante viene
  violata; il meccanismo intero la mantiene. Dieci mutazioni della migrazione
  fanno tutte fallire la suite;
- la migrazione è reversibile senza residui sul catalogo.

## Limiti delle verifiche

Fanno parte della decisione e non vanno letti come garanzie:

- **Prova isolata, non il modello reale.** In `ledger` un lato è un movimento
  che può esistere senza gruppo prima dell'abbinamento (FR-025); nella prova
  `group_id` è obbligatorio. Il passaggio da movimento singolo a lato e le
  altre regole di DR-006 sul movimento non sono provati.
- **`account_ref` senza chiave esterna** nella prova: il conto reale arriva
  con TASK-008. L'argomento che spazio, importo e direzione non siano esposti
  a scritture oblique è un ragionamento, non una prova; la regola dei conti
  distinti sì, ed è provata.
- **Interazione con D-14 non provata.** La chiave esterna composta
  `(space_id, <colonna>)` di TASK-102 garantirà lo spazio dei lati anche dal
  database; la sua combinazione con il trigger va verificata.
- **Prestazioni non misurate.** Ogni riga scritta aggiorna il gruppo
  (circa due `UPDATE` in più per giroconto): da misurare sui volumi di
  importazione (NFR-006, DEF-016).
- **Isolamento.** Provati `READ COMMITTED` (standard di ADR-005) e
  `REPEATABLE READ`; `SERIALIZABLE` non è provato.
- **Più giroconti in una transazione.** L'ordine fisso tra gruppi, per
  evitare deadlock, non è provato.
- **Il proprietario può aggirare il vincolo**, per natura: una migrazione di
  dati deve rispettare l'invariante.
- **Ambiente e carico.** Esito su ambiente locale (macOS); l'esito in CI è
  quello della PR di TASK-099. Il seme della prova di carico fissa le
  operazioni, non l'interleaving; il `LockMonitor` vede solo i lock pesanti di
  PostgreSQL; i test con commit non girano in parallelo sullo stesso database.
- **Librerie VER-013** provate sui percorsi descritti, non con
  un'integrazione completa.
- **Solo giroconti.** Nessuna garanzia è dimostrata per VER-010 e VER-011.

## Implicazioni per TASK-017

Non aggiungono requisiti né soluzioni: precisano cosa il servizio deve
tenere presente.

- **Il rifiuto arriva all'uscita dal blocco `atomic` più esterno**, non
  sull'istruzione che ha scritto: il servizio gestisce lì `IntegrityError` e
  l'errore di deadlock (`40P01`). Un deadlock non è un errore di dominio:
  TASK-017 decide se ripetere l'operazione o mostrare un errore.
- **Ordine di scrittura fisso** dei lati (e, se una transazione tocca più
  giroconti, dei gruppi) per limitare i deadlock; non protegge l'invariante.
- **Test di servizio in `TestCase`:** lì non c'è commit e il vincolo non
  scatta; si chiama `connection.check_constraints()` (Django lo chiama anche
  a fine test). Le prove di rifiuto stanno meglio in `ConcurrencyTestCase`.
- **Migrazione `RunSQL` scritta a mano** nel modulo che possiede il modello,
  con test sul catalogo e prova di reversibilità; la funzione condivisa dai
  trigger va riscritta per intero a ogni modifica.
- **Verificare quanto non provato**: passaggio da movimento singolo a lato,
  conto reale, interazione con D-14 e prestazioni (sezione precedente).
- **Registrazione dei criteri (D-17).** AC-TS-006-03 è un criterio di
  processo e si verifica in TASK-105; questo ADR non lo registra come
  verificato.

## Alternative considerate

| Alternativa | Motivo dello scarto |
|---|---|
| Solo vincolo differito, senza `UPDATE` della riga padre | Provato: due commit incrociati lo superano e l'invariante è violata |
| Solo lock (`FOR NO KEY UPDATE`) sulla riga padre | Provato: in `REPEATABLE READ` il controllo rilegge un'istantanea vecchia e passa |
| `django-pgtrigger` | Il ruolo applicativo può spegnere il trigger con un parametro di sessione (provato) |
| `django-migrate-sql-deux` | Sicura, ma sostituisce due comandi di Django per pochi oggetti SQL |
| `SERIALIZABLE` limitato alle operazioni | Protegge solo se tutti gli scrittori lo usano; non copre la scrittura diretta in `READ COMMITTED`. Non provato |
| Lock applicativo sulla riga padre | Garanzia per disciplina, non copre il SQL diretto. Non provato |

## Conseguenze

- TASK-017 può partire (D-10) quando questo ADR è approvato: l'approvazione
  del testo è la condizione di AC-TS-006-03.
- ADR-005 §3 non è modificato nel merito: il meccanismo di VER-012 è ora
  deciso in questo ADR; VER-010 e VER-011 restano meccanismi candidati.
- Una quantità limitata di logica SQL vive nelle migrazioni e richiede test
  dedicati (RA-003).
- Il vincolo dei giroconti non dipende da una libreria né dalla disciplina
  dell'applicazione, ma il costo di una modifica alla funzione è a carico di
  chi scrive la migrazione.

## Revisioni

| Data | Modifiche |
|---|---|
| 2026-11-05 | Prima stesura (TASK-100), in stato Proposto. Decisione tecnica approvata dal product owner; testo in attesa di review |
