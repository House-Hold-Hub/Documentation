# Requisiti — House-Hold-Hub V1

Fonte canonica dei requisiti funzionali (FR) e non funzionali (NFR).
Origine: **C** confermato, **P** proposta, **A** assunzione (vedi
[convenzioni](README.md#convenzioni)). Le regole di calcolo e di
visibilità sono definite in [domain-rules.md](domain-rules.md) e qui solo
richiamate.

## Requisiti funzionali

### Accesso, spazi e nuclei

#### FR-001 — Registrazione e accesso

Una persona può registrarsi con un indirizzo email verificato, accedere,
uscire e recuperare l'accesso. Ogni account corrisponde a una sola persona.
Origine: C (multiutente); P (registrazione aperta, vedi [Q-002](open-questions-and-risks.md#q-002--registrazione-aperta-o-su-invito)).
Storie: [US-001](stories/US-001-registration-and-personal-space.md).

#### FR-002 — Spazio personale privato

Alla registrazione ogni utente riceve uno spazio personale. Le risorse dello
spazio personale sono visibili e modificabili solo dal titolare, salvo
condivisione o attribuzione esplicita ([DR-002](domain-rules.md#dr-002--privacy-per-default)).
Origine: C.
Storie: [US-001](stories/US-001-registration-and-personal-space.md), [US-002](stories/US-002-space-isolation.md).

#### FR-003 — Creazione di un nucleo familiare

Un utente può creare un nucleo familiare con un nome; il creatore ne diventa
amministratore. Ogni nucleo è uno spazio separato con risorse proprie.
Origine: C.
Storie: [US-014](stories/US-014-household-creation-and-invitations.md).

#### FR-004 — Inviti al nucleo

Un amministratore può invitare una persona tramite email. L'invito scade
dopo 7 giorni, è revocabile finché non accettato e richiede un'accettazione
esplicita da parte di un utente registrato con quell'indirizzo.
Origine: P.
Storie: [US-014](stories/US-014-household-creation-and-invitations.md).

#### FR-005 — Appartenenza a più nuclei

Un utente può appartenere a più nuclei contemporaneamente e passare da uno
spazio all'altro. Dati e permessi di ciascun nucleo sono isolati
([DR-003](domain-rules.md#dr-003--isolamento-degli-spazi)).
Origine: C.
Storie: [US-002](stories/US-002-space-isolation.md), [US-014](stories/US-014-household-creation-and-invitations.md).

#### FR-006 — Ruoli nel nucleo

Ogni membro ha il ruolo di Amministratore o Membro, con i permessi della
[matrice dei permessi](domain-rules.md#matrice-dei-permessi-del-nucleo).
Origine: C (autorizzazioni per nucleo); P (ruoli e matrice).
Storie: [US-015](stories/US-015-household-roles-and-members.md).

#### FR-007 — Gestione dei membri

Un amministratore può cambiare il ruolo dei membri e rimuoverli; la
rimozione o il declassamento di un altro amministratore e l'eliminazione di
un nucleo con altri membri hanno effetto dopo il preavviso di
[DR-026](domain-rules.md#dr-026--tutela-dei-dati-condivisi-del-nucleo) e solo
se, alla scadenza, la rivalidazione di permessi e amministratori ha esito
positivo. Ogni membro può lasciare il nucleo. Un nucleo con altri membri ha sempre almeno
un amministratore ([DR-022](domain-rules.md#dr-022--almeno-un-amministratore)).
Uscita e rimozione revocano subito gli accessi e nascondono al nucleo
l'identità dell'ex membro nelle sue attribuzioni storiche, che restano
conservate e collegate ai movimenti di origine in modo non visibile al
nucleo, così da preservarne la capienza; l'uscita non equivale
all'eliminazione dell'account ([DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo)).
Origine: P; C per l'uscita volontaria (decisione su
[Q-004](open-questions-and-risks.md#q-004--attribuzioni-di-un-membro-uscito)),
per il collegamento tecnico e per la tutela dei dati condivisi (decisioni
del 2026-10-28); uso con dati reali subordinato al gate di [Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione).
Storie: [US-015](stories/US-015-household-roles-and-members.md).

#### FR-008 — Conti e tipologie

Un utente può creare conti con nome, tipologia, istituto (facoltativo),
saldo iniziale e data del saldo iniziale. Tipologie: conto corrente (C),
conto deposito (C), conto investimento (C), contanti (P).
Origine: C/P.
Storie: [US-003](stories/US-003-personal-accounts.md).

#### FR-009 — Saldo del conto

Il saldo di un conto è calcolato secondo [DR-018](domain-rules.md#dr-018--saldo-del-conto)
ed è consultabile alla data odierna e a fine di ogni mese.
Origine: P.
Storie: [US-003](stories/US-003-personal-accounts.md).

#### FR-010 — Archiviazione dei conti

Un conto può essere archiviato: non accetta nuovi movimenti, resta nei
report dei periodi passati e può essere riattivato.
Origine: P.
Storie: [US-003](stories/US-003-personal-accounts.md).

#### FR-011 — Conti del nucleo

Un nucleo può possedere conti propri (es. conto cointestato). I loro
movimenti appartengono allo spazio del nucleo e usano le sue categorie.
Origine: P.
Storie: [US-016](stories/US-016-household-accounts-and-categories.md).

### Movimenti

#### FR-012 — Inserimento manuale dei movimenti

Un utente può registrare entrate e uscite indicando data, importo, conto,
descrizione, natura (ordinaria, giroconto o trasferimento tra spazi) e, per i
movimenti ordinari, facoltativamente categoria o sottocategoria e note
([DR-005](domain-rules.md#dr-005--movimenti)).
Origine: C; C per la distinzione tra spese, trasferimenti e rimborsi
(decisione del 2026-10-28).
Storie: [US-005](stories/US-005-manual-transactions.md), [US-006](stories/US-006-transfers.md).

#### FR-013 — Modifica ed eliminazione dei movimenti

Un utente può modificare ed eliminare i movimenti del proprio spazio, nel
rispetto dei vincoli sulle attribuzioni ([DR-010](domain-rules.md#dr-010--modifica-di-movimenti-attribuiti));
un movimento vincolato errato si corregge con la rettifica contabile
([DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo) punto 6),
che se viola la capienza è bloccata fino a una riconciliazione esplicita
delle attribuzioni.
Origine: C.
Storie: [US-005](stories/US-005-manual-transactions.md).

#### FR-014 — Giroconti

Un utente può registrare un giroconto tra due conti dello stesso spazio.
Il giroconto non è né entrata né uscita nei report ([DR-006](domain-rules.md#dr-006--giroconti)).
Uno spostamento tra il conto personale di un utente e un conto di un nucleo
di cui è membro si registra in ciascuno spazio come trasferimento tra
spazi, da chi ha accesso a quello spazio e senza accedere ai conti
dell'altro: modifica il saldo del conto, non ha categoria e non entra nei
totali né nei budget
([DR-007](domain-rules.md#dr-007--movimenti-tra-spazi-diversi)).
Origine: C (gestione dei trasferimenti tra conti; distinzione tra spese,
trasferimenti e rimborsi, decisione del 2026-10-28).
Storie: [US-006](stories/US-006-transfers.md), [US-016](stories/US-016-household-accounts-and-categories.md).

#### FR-015 — Ricerca e filtri dei movimenti

L'elenco dei movimenti è filtrabile per periodo, conto, tipo, natura,
categoria, sottocategoria, testo della descrizione e stato "Da
categorizzare".
Origine: P.
Storie: [US-005](stories/US-005-manual-transactions.md).

### Categorie

#### FR-016 — Tassonomia personalizzabile a due livelli

Ogni spazio ha una propria tassonomia di categorie e sottocategorie (es.
Ristorazione › Aperitivi, Pranzi, Cene; Trasporti › Carburante, Telepass),
che l'utente autorizzato può creare, rinominare, spostare e archiviare
([DR-008](domain-rules.md#dr-008--categorie)).
Origine: C.
Storie: [US-004](stories/US-004-categories.md), [US-016](stories/US-016-household-accounts-and-categories.md).

#### FR-017 — Tassonomia iniziale predefinita

Ogni nuovo spazio parte da una tassonomia predefinita, interamente
modificabile, che include almeno spese per casa, alimentari, ristorazione,
trasporti, salute, svago, abbonamenti ed entrate da lavoro.
Origine: P.
Storie: [US-004](stories/US-004-categories.md).

#### FR-018 — Eliminazione e unione di categorie

Una categoria o sottocategoria con movimenti, attribuzioni, budget o regole
associati può essere eliminata solo indicando una destinazione per
riassegnarli; in alternativa può essere archiviata.
Origine: P.
Storie: [US-004](stories/US-004-categories.md).

#### FR-019 — Regole di categorizzazione

Un utente può definire regole "se la descrizione contiene un testo, assegna
questa categoria o sottocategoria", applicate ai movimenti importati e, su
richiesta, a quelli esistenti da categorizzare.
Origine: P.
Storie: [US-011](stories/US-011-categorization-rules.md).

### Importazione

#### FR-020 — Importazione da file CSV ed Excel

Un utente può importare in un conto i movimenti contenuti in un file CSV o
Excel esportato dalla propria banca.
Origine: C.
Storie: [US-008](stories/US-008-file-import.md).

#### FR-021 — Mappatura e profili di importazione

L'utente indica quali colonne contengono data, descrizione e importo
(colonna unica con segno oppure colonne dare/avere), il formato delle date,
il separatore decimale e le righe da ignorare. La mappatura può essere
salvata come profilo riutilizzabile.
Origine: P.
Storie: [US-008](stories/US-008-file-import.md).

#### FR-022 — Anteprima e validazione dell'importazione

Prima della conferma l'utente vede un'anteprima con l'esito per riga
(valida, non valida con motivo, possibile duplicato). Nessun movimento viene
creato prima della conferma.
Origine: P.
Storie: [US-008](stories/US-008-file-import.md).

#### FR-023 — Rilevamento dei duplicati

Durante l'importazione il sistema segnala i possibili duplicati, sia nel
file sia rispetto ai movimenti già presenti nel conto, e l'utente decide se
includerli. Ogni movimento esistente è abbinato al più a una riga del file
([DR-016](domain-rules.md#dr-016--possibili-duplicati)).
Origine: C.
Storie: [US-009](stories/US-009-duplicate-detection.md).

#### FR-024 — Lotti di importazione

Ogni importazione confermata forma un lotto consultabile (file, conto, data,
numero di movimenti) che può essere annullato ([DR-017](domain-rules.md#dr-017--annullamento-di-un-lotto)).
Origine: P.
Storie: [US-010](stories/US-010-import-batches.md).

#### FR-025 — Abbinamento dei giroconti importati

Il sistema suggerisce di abbinare un'uscita e un'entrata di pari importo su
due conti dello stesso spazio, con date vicine, trasformandole in un
giroconto dopo conferma dell'utente.
Origine: P.
Storie: [US-012](stories/US-012-imported-transfer-matching.md).

### Condivisione e attribuzione

#### FR-026 — Condivisione in sola lettura

Il titolare può condividere in sola lettura un proprio conto con uno o più
nuclei di cui è membro e revocare la condivisione in qualsiasi momento. I
membri vedono saldo e movimenti, senza poterli modificare. I conti condivisi
non alimentano report e budget del nucleo ([DR-011](domain-rules.md#dr-011--perimetro-dei-report)).
Origine: C.
Storie: [US-017](stories/US-017-read-only-sharing.md).

#### FR-027 — Attribuzione dei movimenti a un nucleo

Il titolare può attribuire un movimento ordinario di un proprio conto, in
tutto o in parte, a uno o più nuclei di cui è membro, indicando per ciascuno
importo e categoria della tassonomia del nucleo. L'attribuzione non richiede
la condivisione del conto, non modifica il movimento originale ed è una
risorsa del nucleo collegata al movimento, con i diritti del titolare
definiti in [DR-009](domain-rules.md#dr-009--attribuzioni).
Origine: C; P per proprietà e accessi.
Storie: [US-018](stories/US-018-transaction-attribution.md).

#### FR-028 — Limite delle attribuzioni

La somma degli importi attribuiti a tutti i nuclei, comprese le attribuzioni
verso nuclei che il titolare ha lasciato, non può superare l'importo del
movimento, anche dopo uscite, rientri, modifiche, eliminazioni,
annullamenti di lotti e rettifiche contabili ([DR-009](domain-rules.md#dr-009--attribuzioni),
[DR-010](domain-rules.md#dr-010--modifica-di-movimenti-attribuiti),
[DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo)).
Origine: C.
Storie: [US-018](stories/US-018-transaction-attribution.md), [US-015](stories/US-015-household-roles-and-members.md), [US-010](stories/US-010-import-batches.md).

#### FR-029 — Riservatezza delle attribuzioni

Per un'attribuzione il nucleo vede solo data, importo attribuito, categoria
del nucleo, membro che ha attribuito e una descrizione scelta dal titolare.
Non vede il conto di origine, l'importo totale né la descrizione originale.
Origine: C (non esporre il conto); P (campi visibili, vedi [Q-003](open-questions-and-risks.md#q-003--campi-visibili-delle-attribuzioni)).
Storie: [US-018](stories/US-018-transaction-attribution.md).

### Report

#### FR-030 — Report mensile per categoria

Per uno spazio e un mese il report mostra totale entrate, totale uscite,
saldo netto e la ripartizione per categoria e sottocategoria, con accesso
ai movimenti che compongono ogni importo, e mostra fuori dai totali i
trasferimenti tra spazi in entrata e in uscita. I calcoli seguono
[DR-011](domain-rules.md#dr-011--perimetro-dei-report)–[DR-014](domain-rules.md#dr-014--rimborsi).
Origine: C.
Storie: [US-007](stories/US-007-monthly-report.md), [US-019](stories/US-019-household-reports-and-budgets.md).

#### FR-031 — Confronto con i mesi precedenti

Il report mensile mostra, per ogni categoria, la differenza rispetto al
mese precedente e alla media dei tre mesi precedenti.
Origine: P.
Storie: [US-007](stories/US-007-monthly-report.md).

#### FR-032 — Movimenti da categorizzare

I movimenti senza categoria compaiono nel report come voce "Da
categorizzare" e possono essere categorizzati direttamente da lì.
Origine: P.
Storie: [US-007](stories/US-007-monthly-report.md).

#### FR-033 — Perimetro dei report del nucleo

Report e budget del nucleo includono i movimenti ordinari dei conti del
nucleo, le quote attribuite al nucleo, comprese quelle di ex membri, e le
quote storiche del nucleo ([DR-024](domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo)).
Non includono mai i movimenti dei conti condivisi in sola lettura, i
trasferimenti tra spazi né le quote limitate durante un'opposizione
([DR-011](domain-rules.md#dr-011--perimetro-dei-report),
[DR-025](domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)).
Origine: C.
Storie: [US-019](stories/US-019-household-reports-and-budgets.md).

### Budget

#### FR-034 — Budget mensili

Per ogni spazio, personale o del nucleo, un utente autorizzato può definire
un importo previsto per mese e per categoria o sottocategoria di spesa.
Origine: C.
Storie: [US-013](stories/US-013-budgets.md), [US-019](stories/US-019-household-reports-and-budgets.md).

#### FR-035 — Confronto previsto e consuntivo

Per ogni voce di budget il sistema mostra previsto, consuntivo, scostamento
e percentuale di utilizzo; per il mese mostra totale previsto, consuntivo
coperto e spese non pianificate, senza sovrapposizioni tra voci di categoria
e di sottocategoria ([DR-019](domain-rules.md#dr-019--budget)).
Origine: C.
Storie: [US-013](stories/US-013-budgets.md).

#### FR-036 — Riutilizzo dei budget

Un utente può copiare il budget di un mese nel mese successivo e
modificarlo.
Origine: P.
Storie: [US-013](stories/US-013-budgets.md).

### Abbonamenti e investimenti

#### FR-037 — Abbonamenti

Un utente può registrare abbonamenti con nome, importo, frequenza (mensile,
trimestrale, semestrale, annuale), data del prossimo rinnovo, conto di
addebito, categoria e stato (attivo o cessato), nello spazio personale o del
nucleo ([DR-020](domain-rules.md#dr-020--abbonamenti)).
Origine: C.
Storie: [US-023](stories/US-023-subscriptions.md).

#### FR-038 — Costo e rinnovi degli abbonamenti

Il sistema mostra, per ciascun abbonamento attivo e in totale, il costo
annuale effettivo e l'equivalente mensile, distinti secondo
[DR-020](domain-rules.md#dr-020--abbonamenti), e i rinnovi previsti nei 30
giorni successivi.
Origine: P.
Storie: [US-023](stories/US-023-subscriptions.md).

#### FR-039 — Posizioni di investimento

In un conto investimento l'utente registra posizioni con nome, tipologia,
capitale investito e valore corrente aggiornato manualmente con data di
riferimento; il sistema mostra la differenza tra valore e capitale
([DR-021](domain-rules.md#dr-021--investimenti)).
Origine: C (gestione investimenti); P (valorizzazione manuale, vedi [Q-005](open-questions-and-risks.md#q-005--livello-di-dettaglio-degli-investimenti)).
Storie: [US-024](stories/US-024-investments-and-net-worth.md).

#### FR-040 — Patrimonio

Per ogni spazio il sistema mostra il patrimonio come somma dei saldi dei
conti attivi e del valore corrente delle posizioni d'investimento. I conti
condivisi in sola lettura non sono sommati al patrimonio del nucleo.
Origine: P.
Storie: [US-024](stories/US-024-investments-and-net-worth.md).

### Privacy e controllo dei dati

#### FR-041 — Esportazione dei dati

Un utente può esportare in un formato leggibile e riutilizzabile tutti i
dati del proprio spazio personale e le attribuzioni che ha effettuato,
comprese quelle verso nuclei lasciati, con il nome della categoria al
momento dell'uscita ([DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo)).
Origine: A (obblighi di portabilità, vedi [A-003](open-questions-and-risks.md#assunzioni)).
Storie: [US-020](stories/US-020-data-export.md).

#### FR-042 — Eliminazione dell'account

Un utente può eliminare il proprio account e i dati del proprio spazio
personale. Nei nuclei le sue quote attribuite restano come quote storiche
minimizzate, una per attribuzione e senza accorpamenti distruttivi, senza
riferimenti diretti all'autore, e i movimenti dei conti
del nucleo restano con i soli dati necessari alla correttezza contabile;
questi dati non sono anonimi e sono trattati come dati personali. L'utente
può opporsi alla conservazione ([FR-045](#fr-045--gestione-delle-opposizioni)); se l'opposizione è accolta, o se la
valutazione legale esclude la base giuridica proposta, le quote sono
eliminate e report e budget ricalcolati ([DR-024](domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo)).
Origine: A (diritto alla cancellazione); C (decisione provvisoria su
[Q-001](open-questions-and-risks.md#q-001--dati-conferiti-ai-nuclei-dopo-leliminazione-dellaccount),
subordinata a [Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione)
e al relativo gate di utilizzo).
Storie: [US-021](stories/US-021-account-deletion.md).

#### FR-043 — Registro attività

Ogni nucleo mostra ai membri attivi un **audit minimo**, indispensabile
nell'MVP, delle azioni che cambiano chi accede ai dati comuni o li
proteggono: ingressi, uscite e rimozioni, cambi di ruolo, condivisioni e
revoche di conti verso il nucleo, avvio, annullamento, scadenza e decadenza
dei preavvisi, compresi quelli di eliminazione del nucleo, esportazioni
dei dati del nucleo e riconciliazioni di quote di ex membri nelle
rettifiche contabili, quando autorizzate secondo
[Q-014](open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro)
([DR-026](domain-rules.md#dr-026--tutela-dei-dati-condivisi-del-nucleo),
[DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo)). Il **registro
completo**, rinviabile, aggiunge nel nucleo inviti, attribuzioni create,
modificate o rimosse e rinomina, e nello spazio personale le condivisioni e
revoche dei propri conti e le proprie attribuzioni.
Origine: C per la distinzione tra audit minimo, indispensabile nell'MVP, e
registro completo, rinviabile (decisione del product owner del
2026-10-28); P per il contenuto delle voci.
Storie: [US-022](stories/US-022-activity-log.md).

#### FR-044 — Informativa sullo storico del nucleo

Alla registrazione l'utente vede l'informativa sul trattamento dei dati
([NFR-010](#requisiti-non-funzionali)) e, quando i nuclei sono disponibili
(M4), la sezione sullo storico dei nuclei; chi si è registrato prima la vede
all'ingresso nel primo nucleo. La sezione, mostrata anche all'ingresso in
ciascun nucleo e alla prima attribuzione verso ciascun nucleo, spiega che
le quote attribuite
e i movimenti registrati nei conti del nucleo entrano nello storico del
nucleo; che all'uscita le attribuzioni restano al nucleo senza il nome
dell'autore e collegate in modo non visibile ai movimenti di origine, che
restano vincolati; che, se l'utente elimina l'account, vi restano in forma
minimizzata senza il suo nome. Indica base giuridica e diritto di
opposizione ([DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo),
[DR-024](domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo)).
Origine: P (necessaria alla base giuridica proposta; il contenuto della
sezione sullo storico dei nuclei è da validare con [Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione)).
Storie: [US-001](stories/US-001-registration-and-personal-space.md), [US-014](stories/US-014-household-creation-and-invitations.md), [US-018](stories/US-018-transaction-attribution.md), [US-021](stories/US-021-account-deletion.md).

#### FR-045 — Gestione delle opposizioni

Un utente che elimina l'account, o un ex membro per le proprie attribuzioni
in un nucleo lasciato, può opporsi alla loro conservazione nello storico del
nucleo indicando i motivi, per tutte o per alcune quote. L'opposizione è
valutata dal titolare del trattamento tramite un referente autorizzato, con
gli accessi limitati di NFR-013, con decisione motivata, registrata e
comunicata nei termini dell'art. 12 GDPR; durante la valutazione le quote
interessate sono limitate. Ogni opposizione, anche ripetuta, segue la stessa
procedura. La correzione di errori contabili dei movimenti vincolati non è
un'opposizione e segue la rettifica contabile di
[DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo). Gli
amministratori dei nuclei non decidono e non vedono le opposizioni ([DR-025](domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)).
Origine: C (decisione su [Q-013](open-questions-and-risks.md#q-013--gestione-dellopposizione));
P (limitazione e registro, da validare con [Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione)).
Storie: [US-015](stories/US-015-household-roles-and-members.md), [US-021](stories/US-021-account-deletion.md).

#### FR-046 — Esportazione dei dati del nucleo

Ogni membro attivo di un nucleo può esportare i dati del nucleo nella forma
in cui li vede, con le quote storiche aggregate senza provenienza e con
le esclusioni e le protezioni di
[DR-026](domain-rules.md#dr-026--tutela-dei-dati-condivisi-del-nucleo) e
le stesse garanzie di FR-041 su formato, verifica dell'identità, scadenza
del file e contenuti non interpretati come formule. L'esportazione è
disponibile in particolare durante i preavvisi di rimozione di un
amministratore e di eliminazione del nucleo.
Origine: C (decisione del 2026-10-28); P (contenuto). L'esportazione delle
quote di ex membri e delle quote storiche è soggetta al gate di [Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione).
Storie: [US-020](stories/US-020-data-export.md), [US-015](stories/US-015-household-roles-and-members.md).

## Requisiti non funzionali

Tutti i valori numerici sono proposte (P) da confermare.

| ID | Area | Requisito | Verifica |
|---|---|---|---|
| NFR-001 | Isolamento e autorizzazione | Ogni lettura e scrittura è consentita solo se l'utente ha diritto sullo spazio della risorsa ([DR-003](domain-rules.md#dr-003--isolamento-degli-spazi)) o, per le proprie attribuzioni, i diritti dell'autore ([DR-009](domain-rules.md#dr-009--attribuzioni)). L'accesso a una risorsa non autorizzata produce lo stesso esito di una risorsa inesistente. | Test negativi per ogni funzione: utente esterno, ex membro (incluso l'accesso alle sole proprie attribuzioni), membro di altro nucleo, riferimento diretto a identificativi altrui, operatore del servizio (NFR-013) |
| NFR-002 | Protezione dei dati | I dati sono cifrati in transito e a riposo, inclusi backup ed esportazioni temporanee. | Verifica di configurazione prima del rilascio |
| NFR-003 | Autenticazione e sessioni | Password robuste con protezione da tentativi ripetuti; sessioni che scadono dopo 30 minuti di inattività; autenticazione a due fattori disponibile come opzione dell'utente. | Test di accesso e scadenza sessione |
| NFR-004 | Esattezza degli importi | Importi gestiti esattamente al centesimo; nessun errore di arrotondamento in somme, attribuzioni parziali e confronti di budget; i valori derivati per divisione, come l'equivalente mensile degli abbonamenti, seguono [DR-020](domain-rules.md#dr-020--abbonamenti). | Test su dataset con importi frazionari e attribuzioni parziali |
| NFR-005 | Coerenza dei report | Report, budget, saldi e patrimonio rispettano le invarianti di [DR-012](domain-rules.md#dr-012--invariante-dei-totali), inclusi quadratura dei saldi e capienza delle attribuzioni, e riflettono immediatamente ogni modifica confermata; l'occultamento dell'identità all'uscita e all'eliminazione dell'account è immediato. | Test di invarianza su dataset di verifica, inclusi giroconti, trasferimenti tra spazi, rimborsi, attribuzioni, uscita e rientro di un membro |
| NFR-006 | Prestazioni | Con fino a 10.000 movimenti per spazio e anno: report mensile e budget visualizzati in ≤ 2 s; anteprima di un file da 1.000 righe in ≤ 10 s. | Misura su dataset di volume |
| NFR-007 | Usabilità e dispositivi | Interfaccia web utilizzabile da desktop e da smartphone (larghezza ≥ 360 px) sulle ultime due versioni dei principali browser. | Verifica manuale dei flussi principali |
| NFR-008 | Accessibilità | Conformità WCAG 2.1 livello AA per i flussi principali. | Audit di accessibilità |
| NFR-009 | Localizzazione | Interfaccia in italiano; date, numeri e valuta in formato italiano; valuta unica EUR ([A-001](open-questions-and-risks.md#assunzioni)). | Verifica manuale |
| NFR-010 | Privacy e minimizzazione | Nessuna cessione di dati a terzi, nessuna profilazione pubblicitaria; metriche d'uso solo aggregate e prive di importi e descrizioni; dopo l'eliminazione di un account restano solo i dati minimizzati previsti da [DR-024](domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo), trattati come dati personali; conformità GDPR ([A-003](open-questions-and-risks.md#assunzioni)). | Revisione privacy prima del rilascio |
| NFR-011 | File importati | Limite di 5 MB o 10.000 righe per file; il file originale non viene conservato dopo la conclusione dell'importazione; i contenuti del file sono trattati come dati e mai interpretati come formule o comandi, anche nelle esportazioni. | Test con file oltre i limiti, malformati e con contenuti malevoli |
| NFR-012 | Backup e ripristino | Perdita massima di dati di 24 ore (RPO) e ripristino entro 8 ore (RTO); procedura di ripristino provata almeno una volta prima del rilascio; backup conservati al massimo 35 giorni; al ripristino le eliminazioni di account successive al backup sono riapplicate prima che i dati tornino disponibili. | Prova di ripristino documentata |
| NFR-013 | Accesso del personale del servizio | Nessun operatore del servizio accede ai dati degli spazi tramite le funzioni del prodotto. Fa eccezione solo il referente autorizzato ([DR-025](domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)), che vede il registro delle opposizioni e le sole quote interessate, con autenticazione a due fattori obbligatoria; ogni suo accesso è registrato in un registro non modificabile e non visibile ai membri. Gli accessi tecnici di manutenzione e ripristino sono regolati dalle decisioni di architettura ([Q-011](open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico)). | Test negativi con un operatore senza ruolo e con un referente su quote non oggetto di opposizione; verifica del registro degli accessi |
