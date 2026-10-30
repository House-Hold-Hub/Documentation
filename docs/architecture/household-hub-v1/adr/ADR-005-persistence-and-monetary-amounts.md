# ADR-005 — Convenzioni di persistenza, importi e invarianti

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Approvato nei principi** (2026-10-30): convenzioni di persistenza, importi e principio delle invarianti. I meccanismi di trigger e contatori del §3 **non sono approvati** e restano da verificare (VER-010 – VER-013) |
| Data | 2026-10-30 |
| Decisore | mdellapa (product owner) |
| Questione | [Q-011](../../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Requisiti | NFR-004, NFR-005, NFR-009, NFR-011; [DR-005](../../../prd/household-hub-v1/domain-rules.md#dr-005--movimenti), [DR-006](../../../prd/household-hub-v1/domain-rules.md#dr-006--giroconti), [DR-009](../../../prd/household-hub-v1/domain-rules.md#dr-009--attribuzioni), [DR-012](../../../prd/household-hub-v1/domain-rules.md#dr-012--invariante-dei-totali), [DR-013](../../../prd/household-hub-v1/domain-rules.md#dr-013--mese-di-competenza), [DR-020](../../../prd/household-hub-v1/domain-rules.md#dr-020--abbonamenti), [DR-022](../../../prd/household-hub-v1/domain-rules.md#dr-022--almeno-un-amministratore); RISK-002 |
| Correlati | [ADR-001](ADR-001-modular-monolith.md), [ADR-004](ADR-004-space-isolation-and-authorization.md), [ADR-006](ADR-006-testing-and-continuous-integration.md) |

## Contesto

Gli importi devono essere esatti al centesimo, senza errori di arrotondamento
in somme, attribuzioni parziali e budget (NFR-004). Alcune invarianti
riguardano più righe e devono valere anche con operazioni concorrenti:

- capienza delle attribuzioni;
- almeno un amministratore per nucleo;
- coerenza dei due lati di un giroconto.

In M0 non esistono ancora importi, ma le convenzioni di persistenza vanno
fissate prima delle prime tabelle, e il modello degli importi prima di M1.

## Decisione

### 1. Convenzioni di persistenza

| Tema | Convenzione |
|---|---|
| Schema | Un solo schema PostgreSQL. Tabelle con il nome predefinito di Django (`<modulo>_<modello>`); permessi assegnati per tabella dove servono (registri immutabili) |
| Identificativi | UUID generati dall'applicazione, non enumerabili; formato in VER-018 |
| Appartenenza | `space_id` obbligatorio su ogni risorsa di uno spazio ([ADR-004](ADR-004-space-isolation-and-authorization.md)) |
| Date contabili | Tipo `date`, senza orario né fuso (DR-005, DR-013) |
| Istanti tecnici | `timestamptz` in UTC; `USE_TZ` attivo; fuso di riferimento `Europe/Rome` per "oggi" e per i confini del mese |
| Orologio | Ora corrente ottenuta da un orologio di `core`, sostituibile nei test |
| Eliminazione | Eliminazione fisica dei dati di dominio, nessuna cancellazione logica diffusa; le eccezioni (lotti annullati con i soli conteggi, voci di audit) sono previste dalle regole di dominio |
| Vincoli | Le regole verificabili su una riga sono vincoli del database (`CHECK`, `UNIQUE`, chiavi esterne), dichiarati nei modelli |
| Transazioni | Confini espliciti nei servizi; nessuna transazione automatica per richiesta; isolamento `READ COMMITTED` predefinito di PostgreSQL |
| Migrazioni | Migrazioni di Django, riviste come codice, solo in avanti in produzione, eseguite con il ruolo proprietario ([ADR-004](ADR-004-space-isolation-and-authorization.md)) |
| Logica nel database | Ammessa solo per garantire invarianti (§3) e immutabilità; mai per regole di business |
| Doppio invio dei form | L'identificativo della risorsa da creare è generato quando il form viene mostrato e inviato con il form. Un secondo invio trova la risorsa già creata e la restituisce, se appartiene allo stesso spazio; altrimenti si comporta come una risorsa inesistente |

### 2. Importi monetari

**Rappresentazione**

- **Python**: tipo valore immutabile `Money` in `core`, che incapsula un
  `Decimal` con esattamente due decimali. La valuta EUR è implicita nel tipo
  (DR-015): un futuro multi-valuta tocca un solo punto.
- **Database**: `numeric(12,2)`, con valore massimo 9.999.999.999,99.
- **Mai `float`** in nessun passaggio: input, calcolo, persistenza, output.

**Costruzione e validazione.** `Money` si crea solo da:

- testo inserito dall'utente (parser italiano, sotto);
- `Decimal` già esatto;
- numero intero di centesimi;
- valore letto dal database.

Viene rifiutato con errore, mai corretto, ogni valore:

- di tipo `float`, o `Decimal` non finito (`NaN`, infinito);
- con più di due decimali significativi (es. `1,005`): **nessun
  arrotondamento implicito**;
- fuori dall'intervallo ammesso dalla colonna.

Il segno è validato per campo, non dal tipo:

| Campo | Regola |
|---|---|
| Importo del movimento | > 0, con la direzione separata (DR-005) |
| Importo dell'attribuzione | > 0 (DR-009) |
| Importo previsto di una voce di budget | ≥ 0 (DR-019) |
| Saldo iniziale | Con segno |

**Parser degli importi inseriti dall'utente (formato italiano)**

| Regola | Esempio accettato | Esempio rifiutato |
|---|---|---|
| Separatore decimale: la virgola, con 1 o 2 cifre dopo | `12,5` (= 12,50), `12,50` | `12,`, `12,505` |
| Punto solo come separatore delle migliaia, in gruppi di 3 cifre | `1.234,56`, `1234,56` | `12.50`, `1.23,4` |
| Spazi iniziali e finali ignorati | `␣12,50␣` | — |
| Notazione esponenziale, simboli e testo | — | `1e3`, `12,50abc` |
| Segno meno solo nei campi con segno | `-150,00` (saldo iniziale) | `-12,00` (importo di un movimento) |

Un input ambiguo come `12.50` è **rifiutato con un messaggio** ("usa la
virgola per i decimali"), mai interpretato. Simbolo `€` e tastiera degli
smartphone vanno verificati con VER-008.

**Importi da file importati.** Il parser è parametrizzato dal separatore
decimale scelto nella mappatura (AC-US-008-02), con la stessa rigidità. Le
celle numeriche dei file Excel sono numeri in virgola mobile: vanno convertite
dalla loro rappresentazione decimale più breve e accettate solo se hanno al
più due decimali; altrimenti la riga è non valida, con motivo (VER-009).
Le librerie che convertono le colonne in `float` (es. pandas) non si usano
per l'importazione.

**Aritmetica**

| Operazione | Regola |
|---|---|
| Ammessa | Somma e differenza tra `Money`, confronto, moltiplicazione per un intero |
| Vietata | Divisione e moltiplicazione per numeri non interi (l'operatore solleva un errore) |
| Calcoli che dividono | Solo tramite funzioni con nome. Unico caso nella V1: l'equivalente mensile di DR-020, ottenuto dal costo annuale effettivo (esatto perché 12 ÷ {1, 3, 6, 12} è intero) diviso per 12 e arrotondato **una sola volta**, metà per eccesso |
| Percentuali (utilizzo del budget) | Calcolate per la visualizzazione, mai salvate né usate per altri importi |

**Persistenza.** I campi importo dei modelli si valorizzano solo da `Money`.
L'arrotondamento eventualmente applicato da Django, dal driver o da
PostgreSQL a valori con più decimali non deve mai entrare in gioco: la
validazione avviene prima (VER-007). Le somme SQL su `numeric` sono esatte e
tornano `Money` con lo stesso controllo.

**Output.** Un solo filtro di template formatta gli importi in formato
italiano (es. `1.234,56 €`), senza conversioni intermedie.

**Controlli automatici**

- Tipi verificati in modo rigoroso sul modulo `Money`.
- Una regola di lint vieta `float` e `Decimal` creati da `float` nei moduli
  che trattano importi.
- Test property-based: `parse(format(x)) == x`, associatività delle somme,
  esempi di DR-020 del PRD
  ([ADR-006](ADR-006-testing-and-continuous-integration.md)).

### 3. Invarianti concorrenti

**Principio**

- Un'invariante che riguarda più righe si garantisce nel database facendo
  passare ogni scrittura rilevante da una **riga padre comune**, aggiornata
  nella stessa transazione e verificata con un vincolo su quella riga.
- La seconda transazione concorrente attende il lock della riga padre e vede
  lo stato aggiornato prima del controllo.
- I lock applicativi (`select_for_update`) servono a dare messaggi precisi
  all'utente (es. residuo attribuibile) e a coordinare operazioni composte,
  ma non sono l'unica garanzia.

**Esclusioni**

- Un trigger che verifica una somma o un conteggio a fine transazione,
  **senza** serializzazione su una riga padre, non garantisce l'invariante in
  `READ COMMITTED`: due transazioni concorrenti vedono ciascuna lo stato
  precedente e superano entrambe il controllo.
- L'aggiornamento di un contatore leggendo il valore, modificandolo e
  salvando l'oggetto perde aggiornamenti concorrenti. I contatori si
  aggiornano solo nel database, in modo relativo.

**Meccanismi candidati, tutti da verificare.** Nessuno è approvato: ciascuno
va provato con test di concorrenza prima della milestone che lo usa. L'esito
sarà registrato in un ADR dedicato.

| ID | Invariante | Meccanismo candidato | Entro |
|---|---|---|---|
| VER-012 | Giroconto: due lati, stesso spazio, stesso importo, direzioni opposte (DR-006) | Vincolo differito a fine transazione sul gruppo del giroconto; ogni modifica aggiorna sempre entrambi i lati, in ordine fisso | Prima di M1 (US-006) |
| VER-010 | Capienza: somma delle attribuzioni ≤ importo del movimento, comprese quelle verso nuclei lasciati (DR-009, DR-012 p.8) | Totale attribuito sulla riga del movimento, aggiornato da trigger a ogni inserimento, modifica o rimozione di attribuzione; `CHECK (totale attribuito ≤ importo)`; `UNIQUE (movimento, nucleo)` | Prima di M4 (US-018) |
| VER-011 | Nucleo con membri ha almeno un amministratore (DR-022) | Conteggi di membri attivi e amministratori sulla riga del nucleo, aggiornati da trigger; `CHECK (membri attivi = 0 OR amministratori ≥ 1)` | Prima di M4 (US-015) |
| VER-013 | Strumento per dichiarare, migrare e testare i trigger | Migrazioni SQL esplicite oppure una libreria per trigger dichiarati nei modelli | Con la prima delle verifiche sopra |

Restano come scelta applicativa in un solo punto di codice, con test di
concorrenza, le invarianti che non hanno una riga padre naturale: ordine e
rivalidazione dei preavvisi (lock sul nucleo) e assenza di duplicati tra
importazioni concorrenti nello stesso conto (lock sul conto). Saranno trattate
negli ADR di nuclei e importazione.

**Alternative se un meccanismo non regge**

1. Isolamento `SERIALIZABLE` limitato alle operazioni interessate, con
   ripetizione automatica in caso di conflitto.
2. Lock applicativo sulla riga padre, concentrato in un solo servizio e
   coperto da test di concorrenza: garanzia per disciplina, documentata come
   tale.

**Vincoli già certi** (verificati su una sola riga, nessuna dipendenza dalle
verifiche sopra): importi > 0 dove richiesto, unicità di un'attribuzione per
movimento e nucleo, unicità del lotto per sessione di importazione.

## Da verificare

| ID | Verifica | Entro |
|---|---|---|
| VER-007 | Comportamento di Django, psycopg e PostgreSQL con valori a più di due decimali su `numeric(12,2)` (errore o arrotondamento); test che lo documenta | Prima dei primi importi (M1) |
| VER-008 | Parser italiano: casi della tabella, simbolo `€`, tastiera degli smartphone (`inputmode="decimal"`), messaggi di errore | M1 |
| VER-009 | Conversione dei numeri delle celle Excel, sui file di esempio di Q-008 | M2 |
| VER-010 – VER-013 | Meccanismi delle invarianti concorrenti (tabella del §3) | Come indicato |
| VER-018 | Identificativi UUIDv7 (supportati dal modulo `uuid` di Python 3.14) o UUIDv4: ordinabilità e indici contro esposizione dell'istante di creazione | Durante M0, prima del primo modello |

## Rinviato

- Report calcolati in lettura e vista delle righe di report: ADR prima di M1.
- Colonna della valuta: dopo la V1, con il multi-valuta.

## Alternative considerate

| Alternativa | Motivo dello scarto |
|---|---|
| Centesimi interi (`bigint`) | Esatti, ma in Python la divisione tra interi produce un `float` senza errori; `Decimal` invece fallisce se mescolato a `float` |
| `float` o `double precision` | Non esatti (NFR-004) |
| Tipo `money` di PostgreSQL | Dipende dalle impostazioni locali del database, poco portabile |
| Invarianti solo nell'applicazione | Non reggono a percorsi di codice dimenticati, operazioni massive o concorrenza |
| Verifiche di aggregati in trigger senza riga padre | Non sicure sotto concorrenza (vedi §3) |

## Conseguenze

- Gli errori sugli importi si manifestano come rifiuti espliciti, mai come
  arrotondamenti silenziosi.
- Una piccola quantità di logica vive nel database, solo per le invarianti,
  e richiede test dedicati (RA-003).
- Fino all'esito delle verifiche, le invarianti di capienza e di
  amministrazione non hanno un meccanismo approvato: le storie interessate
  (US-006, US-015, US-018) non si implementano prima della relativa verifica.
