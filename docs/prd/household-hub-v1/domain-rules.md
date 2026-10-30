# Glossario e regole di dominio — House-Hold-Hub V1

Fonte canonica della terminologia, delle regole di calcolo e di visibilità.
I requisiti in [requirements.md](requirements.md) rimandano a queste regole.
Origine: **C** confermato, **P** proposta, **A** assunzione.

## Glossario

| Termine | Definizione |
|---|---|
| Utente | Persona registrata. Un account appartiene a una sola persona. |
| Spazio | Perimetro di proprietà dei dati: lo spazio personale di un utente oppure un nucleo. |
| Spazio personale | Spazio privato creato per ogni utente alla registrazione. |
| Nucleo (familiare) | Spazio condiviso da un gruppo di utenti, con risorse proprie. |
| Membro | Utente che appartiene a un nucleo, con ruolo Amministratore o Membro. |
| Risorsa | Oggetto che appartiene a uno spazio: conto, movimento, categoria, budget, abbonamento, posizione d'investimento, regola di categorizzazione, profilo di importazione; nel nucleo anche attribuzione e quota storica ([DR-001](#dr-001--appartenenza-delle-risorse)). |
| Conto | Contenitore di movimenti: conto corrente, conto deposito, conto investimento, contanti. |
| Conto del nucleo | Conto che appartiene a un nucleo (es. conto cointestato). |
| Movimento | Entrata o uscita registrata su un conto, di natura ordinaria, giroconto o trasferimento tra spazi ([DR-005](#dr-005--movimenti)). |
| Giroconto | Spostamento di denaro tra due conti dello stesso spazio; neutro nei report. |
| Trasferimento tra spazi | Spostamento di denaro tra il conto personale di un utente e un conto di un nucleo di cui è membro; ogni spazio ne registra il proprio lato, neutro nei report, senza accedere ai conti dell'altro ([DR-007](#dr-007--movimenti-tra-spazi-diversi)). |
| Rimborso | Entrata ordinaria con categoria di spesa, che riduce quella spesa ([DR-014](#dr-014--rimborsi)). |
| Tassonomia | Insieme di categorie e sottocategorie di uno spazio. |
| Categoria / Sottocategoria | Classificazione di primo e secondo livello (es. Ristorazione › Cene). |
| Condivisione in sola lettura | Permesso, concesso dal titolare, di vedere un suo conto personale ai membri di un nucleo. |
| Attribuzione | Quota di un movimento personale assegnata a un nucleo, con importo e categoria del nucleo. È una risorsa del nucleo collegata al movimento di origine; il collegamento è visibile solo al titolare ([DR-009](#dr-009--attribuzioni)). |
| Residuo attribuibile | Importo di un movimento meno la somma di tutte le sue attribuzioni, comprese quelle verso nuclei lasciati ([DR-009](#dr-009--attribuzioni)). |
| Movimento vincolato | Movimento personale con attribuzioni verso nuclei lasciati dal titolare; non può essere eliminato né ridotto sotto la somma delle attribuzioni, salvo rettifica contabile ([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)). |
| Rettifica contabile | Correzione di un movimento vincolato errato. Non riduce mai le attribuzioni in automatico: se viola la capienza è bloccata finché le attribuzioni non sono riconciliate esplicitamente. Non è un'opposizione ([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)). |
| Audit minimo | Parte indispensabile del registro attività del nucleo, limitata alle azioni che cambiano chi accede ai dati comuni o li proteggono ([FR-043](requirements.md#fr-043--registro-attività)). |
| Quota storica del nucleo | Quota derivata da una singola attribuzione di un utente che ha eliminato l'account, conservata in forma minimizzata senza riferimenti diretti all'autore ([DR-024](#dr-024--eliminazione-dellaccount-e-storico-del-nucleo)). Non è un dato anonimo. |
| Riferimento di provenienza | Identificativo casuale comune alle quote storiche dello stesso utente eliminato, non visibile ai membri e non collegato all'identità ([DR-024](#dr-024--eliminazione-dellaccount-e-storico-del-nucleo)). |
| Ex membro | Utente che ha lasciato un nucleo o ne è stato rimosso; le sue attribuzioni restano al nucleo senza la sua identità e collegate ai movimenti di origine in modo non visibile al nucleo ([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)). |
| Referente autorizzato | Persona incaricata dal titolare del trattamento di valutare le opposizioni ([DR-025](#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)), con gli accessi limitati di [NFR-013](requirements.md#requisiti-non-funzionali). |
| Lotto di importazione | Insieme dei movimenti creati da una singola importazione confermata. |
| Profilo di importazione | Mappatura salvata delle colonne e dei formati di un file bancario. |
| Possibile duplicato | Riga importata che potrebbe corrispondere a un movimento già presente o ad altra riga dello stesso file. |
| Regola di categorizzazione | Associazione tra un testo contenuto nella descrizione e una categoria. |
| Voce di budget | Importo previsto per uno spazio, un mese e una categoria o sottocategoria di spesa. |
| Voci di riferimento | Voci di budget che compongono il totale previsto e il consuntivo coperto senza sovrapposizioni ([DR-019](#dr-019--budget)). |
| Consuntivo | Importo effettivamente speso, calcolato con le stesse regole del report. |
| Abbonamento | Spesa ricorrente prevista, con frequenza e data di rinnovo. |
| Costo annuale effettivo | Somma degli addebiti di un abbonamento in un anno; valore esatto di riferimento ([DR-020](#dr-020--abbonamenti)). |
| Equivalente mensile | Costo annuale effettivo diviso per 12 e arrotondato al centesimo; valore indicativo, non corrisponde a un addebito ([DR-020](#dr-020--abbonamenti)). |
| Posizione d'investimento | Strumento detenuto in un conto investimento, con capitale investito e valore dichiarato. |
| Patrimonio | Somma dei saldi dei conti e del valore delle posizioni di uno spazio. |

## Regole di dominio

### DR-001 — Appartenenza delle risorse

Ogni risorsa appartiene a esattamente uno spazio. La proprietà di una risorsa
non cambia per effetto di condivisioni o attribuzioni. Un'attribuzione e una
quota storica appartengono al nucleo destinatario; l'autore di
un'attribuzione ha sui propri dati solo i diritti indicati in
[DR-009](#dr-009--attribuzioni) e [DR-023](#dr-023--uscita-e-rimozione-dal-nucleo),
senza altri accessi al nucleo. Origine: C/P.

### DR-002 — Privacy per default

Una risorsa dello spazio personale non è visibile ad altri utenti finché il
titolare non la condivide ([DR-004](#dr-004--condivisione-in-sola-lettura))
o non ne attribuisce una quota a un nucleo ([DR-009](#dr-009--attribuzioni)).
Non esistono eccezioni per amministratori di nucleo. Gli operatori del
servizio non accedono ai dati degli spazi tramite le funzioni del prodotto,
salvo il referente autorizzato; i limiti del referente e degli accessi
tecnici di manutenzione e ripristino sono quelli di
[NFR-013](requirements.md#requisiti-non-funzionali) e [Q-011](open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico).
Origine: C; P per gli operatori del servizio.

### DR-003 — Isolamento degli spazi

Un utente accede a uno spazio solo se ne è titolare (spazio personale) o
membro attivo (nucleo). Per chi non ha diritto, una risorsa non accessibile
è indistinguibile da una inesistente. I dati di un nucleo non sono mai
visibili ai membri di un altro nucleo, anche se gli utenti coincidono in
parte. Origine: C.

### DR-004 — Condivisione in sola lettura

Il titolare può condividere un proprio conto personale con uno o più nuclei
di cui è membro attivo. I membri del nucleo vedono nome, tipologia, saldo e
movimenti del conto, con le categorie personali del titolare, ma non possono
modificarli, attribuirli né importarvi file. La revoca ha effetto immediato.
La condivisione non trasferisce la proprietà e non alimenta report, budget
o patrimonio del nucleo ([DR-011](#dr-011--perimetro-dei-report)).
Origine: C.

### DR-005 — Movimenti

Un movimento ha tipo (entrata o uscita), importo positivo espresso in EUR al
centesimo, data di calendario senza orario, conto, descrizione non vuota e,
facoltativamente, categoria o sottocategoria e note. Un movimento può essere
registrato solo su un conto attivo.

Ogni movimento ha una natura: **ordinaria** (spesa, entrata o rimborso,
[DR-014](#dr-014--rimborsi)), **giroconto** ([DR-006](#dr-006--giroconti))
o **trasferimento tra spazi** ([DR-007](#dr-007--movimenti-tra-spazi-diversi)).
Solo i movimenti ordinari hanno categoria ed entrano nei totali di entrate
e uscite; tutte le nature modificano il saldo del conto
([DR-018](#dr-018--saldo-del-conto)). Origine: P; C per la distinzione tra
spese, trasferimenti e rimborsi (decisione del product owner del
2026-10-28).

### DR-006 — Giroconti

Un giroconto collega un'uscita su un conto e un'entrata di pari importo su
un altro conto dello stesso spazio. Ciascun lato ha la propria data, di
norma uguale; può differire quando i lati provengono da importazioni di
banche diverse ([FR-025](requirements.md#fr-025--abbinamento-dei-giroconti-importati)).
Non ha categoria, non è
conteggiato tra entrate e uscite e modifica solo i saldi dei due conti.
Modificare o eliminare un giroconto agisce su entrambi i lati. Versamenti su
conto deposito o investimento dello stesso spazio sono giroconti.
Origine: C (corretta gestione dei trasferimenti); P (regola).

### DR-007 — Movimenti tra spazi diversi

Un **trasferimento tra spazi** è uno spostamento di denaro tra il conto
personale di un utente e un conto di un nucleo di cui quell'utente è membro
alla data del movimento. Esempi: versamento di un membro sul conto
cointestato; prelievo dal conto cointestato verso il conto personale di un
membro; rimborso a un membro, dal conto del nucleo, di una spesa che il
membro ha attribuito al nucleo. Non è un giroconto: ogni spazio ne registra
il proprio lato.

- Ogni lato è registrato da chi ha accesso a quello spazio: nel nucleo
  qualsiasi membro, anche quando il denaro va o viene dal conto personale di
  un altro membro; nello spazio personale il titolare. Nessuno accede ai
  conti dell'altro spazio: la natura è dichiarata da chi registra.
- Il movimento non registra conto né spazio di controparte. I due lati non
  sono collegati: ciascuno è registrato, modificato o eliminato nel proprio
  spazio ([DR-001](#dr-001--appartenenza-delle-risorse)).
- È un'uscita o un'entrata senza categoria: modifica il saldo del proprio
  conto ([DR-018](#dr-018--saldo-del-conto)) ma non è conteggiato tra entrate
  e uscite, nei budget né tra i movimenti "Da categorizzare".
- Non può essere attribuito ([DR-009](#dr-009--attribuzioni)).
- Sono movimenti ordinari (spesa, entrata o rimborso) gli scambi che non
  rientrano nella definizione: con il conto personale di un altro utente
  visto dallo spazio personale, con un nucleo di cui l'utente non è membro,
  tra due nuclei.

**Nessun doppio conteggio nel nucleo.** Una spesa familiare entra nel
nucleo una sola volta: come uscita di un conto del nucleo oppure come quota
attribuita. Se il nucleo rimborsa a un membro una spesa che il membro ha
attribuito, il rimborso dal conto del nucleo è un trasferimento tra spazi;
registrarlo come spesa del nucleo conteggerebbe due volte la stessa spesa.
Nel proprio spazio il membro registra l'entrata come trasferimento tra spazi
oppure come rimborso ([DR-014](#dr-014--rimborsi)); in nessun caso attribuisce
quell'entrata al nucleo.

Origine: C (distinzione tra spese, trasferimenti e rimborsi, decisione del
product owner del 2026-10-28); P (regola).

### DR-008 — Categorie

- La tassonomia ha al massimo due livelli: categoria e sottocategoria.
- Ogni categoria è di tipo spesa o entrata; le sottocategorie ne ereditano
  il tipo. I nomi sono unici tra le categorie di primo livello e tra le
  sottocategorie della stessa categoria.
- Un movimento ordinario può avere una categoria, una sottocategoria (che
  implica la categoria padre) o nessuna; in quest'ultimo caso è "Da
  categorizzare". Giroconti e trasferimenti tra spazi non hanno categoria
  e non sono mai "Da categorizzare".
- Un'uscita può avere solo categorie di spesa. Un'entrata può avere
  categorie di entrata o di spesa (rimborso, [DR-014](#dr-014--rimborsi)).
- Una categoria archiviata resta nei dati storici ma non è proposta per
  nuove assegnazioni.

Origine: C (due livelli personalizzabili); P (dettagli).

### DR-009 — Attribuzioni

- Si può attribuire solo un movimento ordinario (entrata o uscita) di un
  conto personale, non un giroconto, un trasferimento tra spazi né un
  movimento di un conto del nucleo.
- Il titolare attribuisce solo a nuclei di cui è membro attivo, al massimo
  una attribuzione per nucleo e per movimento. Il limite conta anche le
  attribuzioni allo stesso nucleo create durante una precedente
  appartenenza ([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)).
- Ogni attribuzione ha importo maggiore di zero e una categoria della
  tassonomia del nucleo, compatibile secondo [DR-008](#dr-008--categorie).
- **Capienza.** La somma di tutte le attribuzioni di un movimento, comprese
  quelle verso nuclei lasciati dal titolare, non supera il suo importo. Il
  residuo attribuibile è l'importo meno questa somma. Il vincolo vale dopo
  ogni uscita, rientro, modifica, eliminazione o annullamento di lotto
  ([DR-010](#dr-010--modifica-di-movimenti-attribuiti),
  [DR-017](#dr-017--annullamento-di-un-lotto)).
- La quota attribuita assume data e tipo del movimento originale.
- Il movimento originale resta invariato: importo pieno e categoria
  personale nel report personale.
- **Proprietà e accessi.** L'attribuzione è una risorsa del nucleo
  destinatario ([DR-001](#dr-001--appartenenza-delle-risorse)), collegata al
  movimento di origine; il collegamento è visibile solo al titolare. Il
  titolare crea, modifica e rimuove le proprie attribuzioni finché è membro
  attivo del nucleo; le vede e le esporta anche dopo l'uscita
  ([FR-041](requirements.md#fr-041--esportazione-dei-dati)), senza altri
  accessi al nucleo. I membri le vedono secondo
  [FR-029](requirements.md#fr-029--riservatezza-delle-attribuzioni); nessun
  altro utente le modifica. Dopo l'uscita dal nucleo valgono le regole di
  [DR-023](#dr-023--uscita-e-rimozione-dal-nucleo).
- L'attribuzione è indipendente dalla condivisione del conto.
- Un rimborso si attribuisce solo se ricevuto da terzi: il denaro ricevuto da
  un conto del nucleo è un trasferimento tra spazi
  ([DR-007](#dr-007--movimenti-tra-spazi-diversi)).

Origine: C; C per la capienza dopo l'uscita (decisione del product owner del
2026-10-28); P per proprietà e accessi.

### DR-010 — Modifica di movimenti attribuiti

- L'importo di un movimento attribuito non può scendere sotto la somma di
  tutte le sue attribuzioni, comprese quelle verso nuclei lasciati: occorre
  prima ridurre quelle verso nuclei di cui il titolare è membro attivo.
- Il cambio di data aggiorna la data delle attribuzioni verso nuclei di cui
  il titolare è membro attivo; le attribuzioni verso nuclei lasciati
  mantengono la propria data, così che lo storico di quei nuclei non cambi.
- Il cambio di tipo, la trasformazione in giroconto o in trasferimento tra
  spazi e l'eliminazione richiedono una conferma che indica i nuclei
  coinvolti e rimuovono le attribuzioni verso nuclei di cui il titolare è
  membro attivo.
- Le stesse operazioni, e la riduzione sotto le attribuzioni verso nuclei
  lasciati, non sono consentite su un movimento vincolato
  ([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)), perché lascerebbero nei
  nuclei lasciati quote senza movimento o superiori al suo importo; un
  movimento vincolato errato si corregge con la rettifica contabile di
  DR-023 punto 6.

Origine: C (limite e capienza); P (comportamento; alternative al blocco in
[Q-014](open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro)).

### DR-011 — Perimetro dei report

| Spazio | Incluso | Escluso |
|---|---|---|
| Personale | Movimenti ordinari dei conti personali, per importo pieno e con categorie personali, indipendentemente da attribuzioni e condivisioni | Giroconti; trasferimenti tra spazi; conti e attribuzioni di altri utenti |
| Nucleo | Movimenti ordinari dei conti del nucleo; quote attribuite a quel nucleo, comprese quelle di ex membri, con categorie del nucleo; quote storiche del nucleo ([DR-024](#dr-024--eliminazione-dellaccount-e-storico-del-nucleo)) | Giroconti; trasferimenti tra spazi; movimenti dei conti condivisi in sola lettura; quote attribuite ad altri nuclei; quote limitate durante un'opposizione ([DR-025](#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)) |

Report di spazi diversi sono prospettive distinte e non si sommano: V1 non
offre viste che aggregano più spazi. Nella vista di un nucleo ogni euro è
conteggiato al massimo una volta, anche quando un conto è sia condiviso sia
oggetto di attribuzioni e anche quando un membro rientra nel nucleo. Una
spesa pagata da un membro e rimborsata dal conto del nucleo è conteggiata
tramite la quota attribuita; il rimborso è un trasferimento tra spazi
([DR-007](#dr-007--movimenti-tra-spazi-diversi)). Il report mostra, fuori dai
totali, i trasferimenti tra spazi in entrata e in uscita del mese.
Origine: C; P per trasferimenti e rimborsi.

### DR-012 — Invariante dei totali

Per ogni spazio e mese:

1. Totale uscite = somma delle uscite ordinarie meno i rimborsi
   ([DR-014](#dr-014--rimborsi)); totale entrate = somma delle entrate
   ordinarie che non sono rimborsi. Nel nucleo quote attribuite e quote
   storiche contano secondo il proprio tipo e la propria categoria.
2. Saldo netto = totale entrate − totale uscite.
3. La somma delle categorie di spesa, inclusa la voce "Da categorizzare",
   è uguale al totale uscite; analogamente per le entrate.
4. Il totale di una categoria è la somma delle sue sottocategorie più gli
   importi assegnati direttamente alla categoria.
5. I giroconti e i trasferimenti tra spazi contribuiscono zero a ogni
   totale.
6. Il consuntivo di una voce di budget è uguale al totale della stessa
   categoria o sottocategoria nel report dello stesso spazio e mese.
7. **Quadratura dei saldi.** Per ogni conto dello spazio, la variazione del
   saldo nel mese è uguale alla somma con segno dei suoi movimenti del mese:
   entrate e rimborsi in aumento, uscite in diminuzione, lati dei giroconti e
   trasferimenti tra spazi secondo la direzione
   ([DR-018](#dr-018--saldo-del-conto)). Quote attribuite e quote storiche
   entrano nei totali del nucleo ma non modificano alcun saldo.
8. **Capienza.** Per ogni movimento la somma delle sue attribuzioni,
   comprese quelle verso nuclei lasciati, non supera il suo importo
   ([DR-009](#dr-009--attribuzioni)).

Origine: C (correttezza dei report aggregati e assenza di doppi conteggi);
P (formulazione).

### DR-013 — Mese di competenza

Un movimento, e ogni sua quota attribuita, appartiene al mese della propria
data. Per i movimenti importati la data è quella della colonna scelta nella
mappatura (data operazione o data valuta). Origine: P.

### DR-014 — Rimborsi

Un'entrata ordinaria con categoria di spesa è un rimborso: riduce il totale
di quella categoria e il totale uscite, senza contare tra le entrate. Il
totale di una categoria di spesa può risultare negativo se i rimborsi
superano le spese. Un trasferimento tra spazi non è un rimborso, anche
quando restituisce una spesa ([DR-007](#dr-007--movimenti-tra-spazi-diversi)).
Origine: P (vedi [Q-006](open-questions-and-risks.md#q-006--trattamento-dei-rimborsi));
C per la distinzione tra rimborsi e trasferimenti (decisione del
2026-10-28).

### DR-015 — Valuta

V1 gestisce solo EUR. Movimenti in valuta estera sono registrati con
l'importo in EUR addebitato o accreditato dalla banca. Origine: A.

### DR-016 — Possibili duplicati

Durante un'importazione nello stesso conto:

| Livello | Condizione | Esito predefinito |
|---|---|---|
| Duplicato probabile | Stesso tipo, importo e data e descrizione uguale dopo normalizzazione (maiuscole, spazi, punteggiatura), rispetto a un movimento esistente | Esclusa |
| Possibile corrispondenza | Stesso tipo e importo, data entro ±3 giorni, descrizione diversa, rispetto a un movimento esistente non importato (es. inserito a mano) | Inclusa ed evidenziata |
| Ripetizione nel file | Due o più righe identiche nello stesso file | Incluse ed evidenziate |

**Abbinamento uno a uno.** Ogni movimento esistente giustifica l'esito
"Duplicato probabile" o "Possibile corrispondenza" di una sola riga del
file e ogni riga è abbinata al più a un movimento esistente, privilegiando
i duplicati probabili e, a parità, la data più vicina. Se il file contiene
più righe uguali a movimenti esistenti indistinguibili, le righe segnalate
come duplicato probabile sono al massimo quanti sono quei movimenti; le
altre sono valide e, se uguali tra loro, evidenziate come ripetizione nel
file.

L'utente può cambiare l'esito di ogni riga prima della conferma. Il sistema
non elimina né modifica mai movimenti esistenti per effetto del controllo
duplicati. Origine: C (gestione dei duplicati); C per l'abbinamento uno a
uno (decisione del 2026-10-28); P (criteri, vedi
[Q-010](open-questions-and-risks.md#q-010--criteri-dei-duplicati)).

### DR-017 — Annullamento di un lotto

Annullare un lotto elimina tutti i movimenti del lotto ancora presenti,
esclusi i movimenti vincolati ([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)),
che restano nel conto. Se alcuni movimenti sono stati modificati,
categorizzati, attribuiti, abbinati in un giroconto o sono vincolati, il
sistema ne mostra il numero per ciascun caso e chiede conferma. Le
attribuzioni dei movimenti eliminati, che riguardano solo nuclei di cui il
titolare è membro attivo, sono rimosse; un giroconto con un lato nel lotto
viene sciolto e l'altro lato torna movimento ordinario del tipo originale.
Il lotto annullato indica quanti movimenti sono rimasti perché vincolati;
ciascuno può essere corretto con la rettifica contabile
([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo) punto 6).
Origine: P; C per la capienza (decisione del 2026-10-28).

### DR-018 — Saldo del conto

Il saldo iniziale è il saldo noto a fine giornata della data di
riferimento. Il saldo a una data successiva si ottiene aggiungendo entrate,
giroconti e trasferimenti tra spazi in entrata e sottraendo uscite,
giroconti e trasferimenti tra spazi in uscita intercorsi; a una data
precedente sottraendo l'effetto dei movimenti intercorsi. Attribuzioni e
quote storiche non modificano alcun saldo. Origine: P.

### DR-019 — Budget

- Una voce di budget si riferisce a uno spazio, un mese, una categoria o
  sottocategoria di spesa e ha importo previsto maggiore o uguale a zero.
- Il consuntivo è calcolato secondo [DR-011](#dr-011--perimetro-dei-report)–[DR-014](#dr-014--rimborsi);
  il consuntivo di una categoria include le sue sottocategorie.
- Scostamento = previsto − consuntivo; utilizzo = consuntivo ÷ previsto
  (non calcolato se il previsto è zero).
- **Voci di riferimento.** Sono le voci di categoria e le voci di
  sottocategoria la cui categoria padre non ha una voce propria. Il totale
  previsto del mese è la somma dei loro importi previsti e il consuntivo
  coperto la somma dei loro consuntivi: nessun importo è contato due volte.
- Se la somma delle voci delle sottocategorie supera la voce della
  categoria il sistema lo segnala senza bloccare.
- **Spese non pianificate** = totale uscite del mese
  ([DR-012](#dr-012--invariante-dei-totali)) − consuntivo coperto.
  Comprendono le spese di categorie e sottocategorie non coperte da una voce
  di riferimento, gli importi assegnati direttamente a una categoria che ha
  voci solo su alcune sottocategorie e la voce "Da categorizzare". Consuntivo
  coperto + spese non pianificate = totale uscite.

Origine: C (budget e confronto); C per il calcolo senza sovrapposizioni
(decisione del 2026-10-28); P (regole).

### DR-020 — Abbonamenti

Un abbonamento è una previsione: non genera movimenti e non entra nei
consuntivi. Per ciascun abbonamento:

- il **costo annuale effettivo** è la somma degli addebiti in un anno,
  cioè importo × 12 ÷ mesi del periodo (1, 3, 6, 12): è sempre esatto al
  centesimo ed è il valore di riferimento;
- l'**equivalente mensile** è il costo annuale effettivo ÷ 12, arrotondato
  al centesimo (metà per eccesso): è un valore indicativo, che serve a
  confrontare abbonamenti con frequenze diverse, non corrisponde a un
  addebito e non si usa per ricavare altri importi.

Il totale annuale effettivo è la somma esatta dei costi annuali effettivi.
Il totale degli equivalenti mensili è la somma dei valori mostrati nelle
righe e può differire di alcuni centesimi dal totale annuale effettivo
diviso per 12 (es. trimestrale da 10,00 €: 40,00 € l'anno, equivalente
mensile 3,33 €; tre abbonamenti uguali: 120,00 € l'anno ed equivalenti
mensili per 9,99 €, mentre 120,00 € ÷ 12 = 10,00 €). Superata la data di
rinnovo, la successiva è calcolata secondo la frequenza. Gli abbonamenti
cessati sono esclusi dai totali. Origine: C (abbonamenti); P (regole).

### DR-021 — Investimenti

I versamenti e i prelievi su un conto investimento sono giroconti o
trasferimenti tra spazi ([DR-006](#dr-006--giroconti), [DR-007](#dr-007--movimenti-tra-spazi-diversi)).
Per un conto investimento il saldo da movimenti rappresenta il versato
netto; al patrimonio contribuisce invece la somma dei valori correnti
dichiarati delle posizioni, inclusa l'eventuale liquidità registrata come
posizione. Un valore non aggiornato da più di 90 giorni è segnalato.
Origine: C (investimenti); P (regole).

### DR-022 — Almeno un amministratore

Un nucleo con almeno un altro membro ha sempre almeno un amministratore:
l'ultimo amministratore non può lasciare il nucleo né rinunciare al ruolo
senza prima nominarne un altro. Se l'unico membro lascia il nucleo, il
nucleo e i suoi dati sono eliminati dopo conferma esplicita. La rimozione
o il declassamento di un altro amministratore e l'eliminazione di un
nucleo con altri membri seguono
[DR-026](#dr-026--tutela-dei-dati-condivisi-del-nucleo). Origine: P.

### DR-023 — Uscita e rimozione dal nucleo

Origine: C per l'uscita volontaria (decisione su
[Q-004](open-questions-and-risks.md#q-004--attribuzioni-di-un-membro-uscito)
del 2026-10-28) e per il mantenimento del collegamento tecnico con il
movimento di origine (decisione del product owner del 2026-10-28),
subordinate alle regole privacy applicabili e alla valutazione di
[Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione),
con il relativo gate di utilizzo; P per l'estensione alla rimozione da parte
di un amministratore e per il blocco dei movimenti vincolati.

Quando un membro lascia il nucleo o ne è rimosso:

1. **Accessi.** Perde subito l'accesso ai dati del nucleo; le sue
   condivisioni in sola lettura verso quel nucleo sono revocate. La
   rimozione di un amministratore ha effetto dopo il preavviso di
   [DR-026](#dr-026--tutela-dei-dati-condivisi-del-nucleo).
2. **Identità nascosta.** Nelle sue attribuzioni storiche, e nelle voci del
   registro attività che riguardano quelle attribuzioni, i membri non vedono
   più il suo nome né la descrizione che aveva scritto: vedono data,
   importo, categoria del nucleo e l'indicazione "ex membro", senza
   distinguere tra ex membri diversi. Restano
   visibili, perché sono dati del nucleo e non delle attribuzioni, l'autore
   dei movimenti dei conti del nucleo e le voci del registro su inviti,
   ingressi, uscite, rimozioni e cambi di ruolo.
3. **Quote preservate.** Le attribuzioni restano al nucleo con importi,
   date e categorie: report e budget del nucleo non cambiano.
4. **Attribuzioni non modificabili.** Nessuno può più modificarle o
   rimuoverle, salvo l'esito di un'opposizione accolta
   ([DR-025](#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo))
   o una riconciliazione esplicita autorizzata in una rettifica contabile
   (punto 6);
   seguono la riassegnazione quando la loro categoria viene eliminata o
   unita ([FR-018](requirements.md#fr-018--eliminazione-e-unione-di-categorie))
   e sono eliminate insieme al nucleo.
5. **Collegamento tecnico con il movimento.** Il collegamento tra
   attribuzione, movimento di origine ed ex membro è mantenuto e non è
   visibile al nucleo. Serve solo a:
   - preservare la capienza del movimento: le attribuzioni restano nel
     residuo attribuibile e nel limite di riduzione dell'importo
     ([DR-009](#dr-009--attribuzioni), [DR-010](#dr-010--modifica-di-movimenti-attribuiti));
   - mostrare all'ex membro, sul movimento e nell'elenco delle proprie
     attribuzioni, nucleo, data, importo e nome della categoria al momento
     dell'uscita, ed esportarli ([FR-041](requirements.md#fr-041--esportazione-dei-dati));
     l'ex membro non vede modifiche successive del nucleo, comprese rinomine
     e unioni di categorie;
   - gestire una sua opposizione (DR-025) e applicare
     [DR-024](#dr-024--eliminazione-dellaccount-e-storico-del-nucleo) se
     elimina l'account.
6. **Movimento vincolato.** Un movimento con attribuzioni verso nuclei
   lasciati è vincolato. Il titolare può cambiarne descrizione, note,
   categoria personale e data, e aumentarne l'importo; il cambio di data non
   modifica le quote dei nuclei lasciati. Non può ridurne l'importo sotto la
   somma delle attribuzioni, eliminarlo, cambiarne il tipo, trasformarlo in
   giroconto o in trasferimento tra spazi, né eliminarlo annullando il lotto
   ([DR-017](#dr-017--annullamento-di-un-lotto)). Il vincolo cessa quando
   quelle attribuzioni sono eliminate per opposizione accolta, con il nucleo
   o con l'eliminazione dell'account.

   **Rettifica contabile.** Se il movimento vincolato è errato (importo
   sbagliato, duplicato, movimento inesistente o di tipo sbagliato), il
   titolare può chiederne la correzione dichiarandone il motivo. La
   rettifica non riduce né elimina mai le attribuzioni in automatico. Se la
   correzione viola la capienza, cioè lascerebbe attribuzioni superiori al
   nuovo importo o su un movimento eliminato o non attribuibile, è bloccata
   e il movimento resta invariato finché le attribuzioni non sono
   riconciliate esplicitamente, indicando il nuovo importo di ciascuna
   attribuzione da ridurre o rimuovere. Correzione e riconciliazione si
   applicano insieme, in un'unica operazione, solo se il risultato rispetta
   la capienza ([DR-009](#dr-009--attribuzioni)).

   - Le attribuzioni verso nuclei di cui è membro attivo le riconcilia il
     titolare, con i diritti dell'autore.
   - Chi può autorizzare la riconciliazione delle attribuzioni verso nuclei
     lasciati è da definire in
     [Q-014](open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro).
     Finché non è definito, quelle attribuzioni non si riconciliano: la
     rettifica che lo richiede resta bloccata e il movimento resta
     vincolato.

   Quando una riconciliazione autorizzata riduce quote in un nucleo
   lasciato, i membri di quel nucleo vedono un avviso senza nome con i mesi
   ricalcolati e l'audit minimo la registra
   ([FR-043](requirements.md#fr-043--registro-attività)). La rettifica
   corregge un errore contabile e non è un'opposizione: non passa dal
   referente, non comporta limitazione e non richiede motivi legati alla
   situazione particolare ([DR-025](#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)).
   Il ritiro di quote non errate resta escluso; le alternative sono in
   Q-014. Origine: C per il blocco e la riconciliazione esplicita, senza
   riduzione automatica (decisione del product owner del 2026-10-28).
7. **Rientro nel nucleo.** Se l'ex membro rientra nello stesso nucleo, le
   attribuzioni della precedente appartenenza restano con l'indicazione "ex
   membro", non modificabili e collegate al movimento: contano nel residuo e
   nel limite di una attribuzione per nucleo e per movimento (DR-009), quindi
   lo stesso movimento non può essere attribuito di nuovo a quel nucleo. Le
   nuove attribuzioni seguono le regole ordinarie.
8. **Non è una cancellazione.** Account, spazio personale e movimenti
   originali dell'ex membro restano invariati. Per ottenere la rimozione
   delle quote dal nucleo l'ex membro può opporsi secondo DR-025.

Prima di uscire il membro può ancora modificare o rimuovere le proprie
attribuzioni (DR-009); in quel caso report e budget del nucleo cambiano come
per ogni altra modifica. L'indicazione "ex membro" non impedisce ai membri di
intuire l'identità quando gli ex membri sono pochi, anche grazie alle voci del
registro su uscite e rimozioni: è un rischio residuo documentato.

### DR-024 — Eliminazione dell'account e storico del nucleo

**Stato:** decisione di prodotto provvisoria del 2026-10-28 (Origine: C),
subordinata alla valutazione legale di
[Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione)
e al relativo gate di utilizzo; l'assenza di accorpamenti distruttivi è
una decisione del product owner del 2026-10-28 (C); procedura e tempi sono
proposte (P).

**Principio.** Preservare, ove possibile e lecito, la coerenza storica dei
report del nucleo senza conservare dati personali non necessari. I dati
conservati sono minimizzati e privi di riferimenti diretti alla persona, ma
**non sono anonimi**: i membri del nucleo possono ricondurli a lei. Restano
dati personali e sono trattati come tali.

Quando un utente elimina l'account:

1. **Spazio personale.** Tutte le risorse sono eliminate. Le condivisioni
   in sola lettura sono revocate e gli inviti in attesa inviati dall'utente
   o a lui destinati sono annullati.
2. **Quote attribuite.** In ogni nucleo ancora esistente, compresi quelli
   che l'utente aveva già lasciato, ciascuna sua attribuzione diventa una
   *quota storica del nucleo*: si conservano solo nucleo, mese di
   competenza, categoria del nucleo, tipo, importo e riferimento di
   provenienza. Si eliminano autore, conto di origine, collegamento al
   movimento originale, descrizione scritta dal titolare e giorno.
   - **Nessun accorpamento distruttivo.** Ogni quota storica deriva da una
     sola attribuzione, resta registrata e individuabile singolarmente e
     non è mai unita nella registrazione a quote di altri utenti.
   - **Nessuna correlazione visibile.** Nella vista e nell'esportazione del
     nucleo le quote storiche sono mostrate come una sola riga per mese,
     categoria e tipo, con il totale di tutte le quote storiche, senza
     distinguerne la provenienza.
   - **Riferimento di provenienza.** Identificativo casuale, comune alle
     quote storiche dello stesso utente nello stesso nucleo e diverso per
     ogni utente e per ogni nucleo, non
     visibile ai membri e non collegato all'identità, salvo durante
     un'opposizione (punto 6). Serve solo a rettifiche, come la
     riassegnazione di categoria, e a eseguire l'esito di un'opposizione
     sulle sole quote interessate. Il suo uso per richieste presentate dopo
     l'eliminazione è da validare con Q-012.
   - Nessuno può modificare o eliminare le quote storiche; seguono la
     riassegnazione quando la loro categoria viene eliminata o unita
     ([FR-018](requirements.md#fr-018--eliminazione-e-unione-di-categorie))
     e sono eliminate insieme al nucleo. Report e budget del nucleo non
     cambiano.
   - Le attribuzioni oggetto di un'opposizione in corso non sono trasformate
     finché l'esito non è comunicato
     ([DR-025](#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)).
3. **Movimenti dei conti del nucleo** registrati o importati dall'utente.
   Non sono quote ma movimenti originali di un conto del nucleo: restano i
   dati necessari alla correttezza contabile del conto (data, importo, tipo,
   conto, categoria, descrizione, appartenenza a giroconti e lotti), così
   che saldi, giroconti e controllo duplicati restino corretti. Si elimina
   ogni riferimento all'utente come autore dei movimenti e dei lotti di
   importazione. Descrizioni bancarie e note non sono modificate in
   automatico: possono citare la persona e sono un rischio residuo
   documentato.
4. **Registro attività.** Le voci di cui l'utente è autore o oggetto sono
   eliminate dai registri visibili ai membri.
5. **Base giuridica proposta.** Finché l'utente è membro, le attribuzioni
   servono a fornirgli il servizio (esecuzione del contratto). Dopo
   l'eliminazione, la conservazione delle quote storiche e dei movimenti dei
   conti del nucleo si fonda sul legittimo interesse dei membri restanti a
   uno storico coerente e a conti corretti. La base è dichiarata fin
   dall'inizio nell'informativa ([FR-044](requirements.md#fr-044--informativa-sullo-storico-del-nucleo)),
   non si fonda sul consenso ed è soggetta al bilanciamento descritto in
   [Base giuridica e bilanciamento](open-questions-and-risks.md#base-giuridica-proposta-e-bilanciamento-da-verificare).
6. **Opposizione.** Nel flusso di eliminazione, e in qualsiasi momento
   prima, l'utente può opporsi secondo [DR-025](#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo),
   per tutte o per alcune quote. Anche con l'opposizione account e spazio
   personale diventano subito inaccessibili e sono eliminati nei tempi del
   punto 8; il collegamento tra utente e quote interessate,
   l'indirizzo email e il nome dell'account sono conservati, non visibili ai
   membri, solo fino alla comunicazione dell'esito e, se l'opposizione è
   accolta, fino all'esecuzione del ripiego (punto 7). La conservazione del
   nome è da validare con Q-012.
7. **Ripiego: cancellazione e ricalcolo.** Si applica se l'opposizione è
   accolta ([DR-025](#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)), o a tutte le eliminazioni se la valutazione di Q-012 esclude la
   base giuridica proposta:
   - le quote dell'utente, o solo quelle oggetto dell'opposizione accolta,
     sono eliminate; report e consuntivi di budget dei mesi interessati sono
     ricalcolati e rispettano [DR-012](#dr-012--invariante-dei-totali);
   - i membri vedono un avviso con i mesi ricalcolati, senza indicazione
     della persona; nei nuclei con pochi membri l'avviso può consentire di
     dedurla (rischio residuo; contenuto e opportunità dell'avviso da
     validare con Q-012);
   - i movimenti dei conti del nucleo non sono eliminati, perché ciò
     altererebbe saldi e giroconti: nelle loro descrizioni e note le
     occorrenze di nome, cognome e indirizzo email dell'account, come
     registrati, sono sostituite da "ex membro", mantenendo importi, date,
     tipi, conti e categorie; altri riferimenti indiretti restano un rischio
     residuo documentato.
8. **Tempi.** Alla conferma della richiesta account e spazio personale
   diventano inaccessibili a chiunque e, nello stesso momento, i membri non vedono più in alcun
   nucleo il nome dell'utente né le descrizioni che aveva scritto, come in
   [DR-023](#dr-023--uscita-e-rimozione-dal-nucleo) punto 2. Eliminazioni e
   trasformazioni terminano entro un mese dalla conferma della richiesta
   (art. 12(3) GDPR, da confermare con Q-012; obiettivo di prodotto:
   30 giorni). Per le quote oggetto di opposizione
   valgono i termini di DR-025. I backup
   che contengono i dati scadono entro 35 giorni e, se un backup viene
   ripristinato, le eliminazioni sono riapplicate prima che i dati tornino
   disponibili.
9. **Dati aggregati della piattaforma.** Le metriche d'uso aggregate su più
   utenti ([NFR-010](requirements.md#requisiti-non-funzionali)) restano.

Implicazioni privacy, vincoli normativi ed eccezioni legali sono descritti
in [Implicazioni privacy dell'eliminazione dell'account](open-questions-and-risks.md#implicazioni-privacy-delleliminazione-dellaccount).

### DR-025 — Opposizione alla conservazione nello storico del nucleo

Origine: C per chi decide (decisione su
[Q-013](open-questions-and-risks.md#q-013--gestione-dellopposizione) del
2026-10-28); P per limitazione e procedura, da validare con [Q-012](open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione)
e soggette al relativo gate di utilizzo.

1. **Chi può opporsi.** L'utente che elimina l'account, nel flusso di
   eliminazione o prima, e l'ex membro per le proprie attribuzioni in un
   nucleo lasciato, indicando i motivi legati alla sua situazione
   particolare ([FR-045](requirements.md#fr-045--gestione-delle-opposizioni)).
   L'opposizione può riguardare tutte o solo alcune quote; ogni quota
   interessata è individuata singolarmente. La correzione di un errore
   contabile del movimento di origine non è un'opposizione e segue la
   rettifica contabile di [DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)
   punto 6.
2. **Chi decide.** Il soggetto individuato come titolare del trattamento,
   tramite un referente autorizzato, con decisione motivata; gli accessi del
   referente seguono [NFR-013](requirements.md#requisiti-non-funzionali).
   Amministratori e membri dei nuclei non decidono, non vedono l'opposizione
   né il registro e non ne sono informati. Gli avvisi dei punti 4 e 6 possono
   però consentire di dedurre l'esistenza di un'opposizione e la persona,
   soprattutto nei nuclei con pochi membri o pochi ex membri: è un rischio
   residuo, e contenuto e opportunità degli avvisi sono da validare con
   Q-012.
3. **Tracciabilità.** Ogni opposizione è registrata con data di ricezione,
   nuclei e quote interessati, motivi, eventuale proroga e relativi motivi,
   decisione, motivazione, referente e data di comunicazione; vi sono
   annotate anche le operazioni tecniche sulle quote limitate (punto 4). Il
   registro non è modificabile ed è accessibile solo ai referenti
   autorizzati; la sua durata di conservazione è da validare con Q-012.
4. **Limitazione durante la valutazione.** Le quote interessate sono
   conservate singolarmente ma non modificabili, escluse da report e budget
   del nucleo e non oggetto di altri trattamenti (art. 18(1)(d) GDPR, da
   validare con Q-012); non sono trasformate in quote storiche né mostrate in
   forma aggregata fino all'esito. I membri vedono un avviso, senza nome, che
   alcuni importi dei mesi indicati sono sospesi. Se durante la limitazione
   la categoria di una quota viene eliminata o unita, la quota segue la
   destinazione come operazione tecnica di integrità; se il nucleo viene
   eliminato, le quote sono eliminate con il nucleo e l'esito è comunicato
   all'interessato. La compatibilità di queste due operazioni con la
   limitazione è da validare con Q-012.
5. **Termini.** L'esito è comunicato entro un mese dal ricevimento. Se
   necessario, tenuto conto della complessità e del numero di richieste, il
   termine è prorogato fino a due mesi ulteriori, comunicando la proroga e i
   motivi entro il primo mese. La comunicazione dell'esito indica la
   possibilità di proporre reclamo all'autorità di controllo e ricorso
   giurisdizionale (art. 12(3)–(4) GDPR; applicazione da confermare con
   Q-012).
6. **Esito accolto.** Le quote interessate sono eliminate dal nucleo e si
   applica il ripiego di [DR-024](#dr-024--eliminazione-dellaccount-e-storico-del-nucleo),
   punto 7. Per un ex membro con account attivo i movimenti originali non
   cambiano e, se non hanno altre attribuzioni verso nuclei lasciati, non
   sono più vincolati ([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)).
7. **Esito respinto.** L'interessato è informato prima che la limitazione
   venga revocata (art. 18(3) GDPR); poi le quote tornano nei report nella
   forma prevista da DR-023 o da DR-024, nella categoria eventualmente
   riassegnata durante la limitazione.
8. **Opposizioni ripetute.** Ogni opposizione, anche se riguarda quote già
   oggetto di una decisione, è registrata, valutata e applica la
   limitazione del punto 4. Un trattamento diverso delle opposizioni
   ripetute o prive di motivi nuovi non è adottato finché Q-012 non ne
   conferma i presupposti.

### DR-026 — Tutela dei dati condivisi del nucleo

Origine: C (protezione di rimozione degli amministratori, eliminazione del
nucleo ed esportazione dei dati condivisi, decisione del product owner del
2026-10-28); P (preavviso di 7 giorni e procedura).

1. **Rimozione e declassamento di un amministratore.** Un amministratore
   può rimuovere un altro amministratore o riportarlo a Membro solo con un
   preavviso di 7 giorni, comunicato all'interessato e visibile a tutti i
   membri. Durante il preavviso l'interessato mantiene ruolo e accessi e può
   esportare i dati del nucleo (punto 3); l'amministratore che ha avviato il
   preavviso può annullarlo. La rinuncia al proprio ruolo
   ([DR-022](#dr-022--almeno-un-amministratore)) e la rimozione di un Membro
   hanno effetto immediato.
2. **Eliminazione del nucleo.** Se il nucleo ha altri membri,
   l'eliminazione avviata da un amministratore ha effetto dopo un preavviso
   di 7 giorni, comunicato a tutti i membri. Durante il preavviso il nucleo
   resta consultabile, ogni membro attivo può esportarne i dati e qualsiasi
   amministratore può annullare l'eliminazione. Se chi elimina è l'unico
   membro si applica DR-022.
3. **Esportazione dei dati condivisi.** Ogni membro attivo può esportare i
   dati del nucleo nella forma in cui li vede
   ([FR-046](requirements.md#fr-046--esportazione-dei-dati-del-nucleo)):
   conti del nucleo con movimenti, giroconti e trasferimenti tra spazi,
   categorie, regole, budget, quote attribuite secondo
   [FR-029](requirements.md#fr-029--riservatezza-delle-attribuzioni), quote
   di ex membri e quote storiche nella forma della vista dei membri, senza
   identità né provenienza ([DR-023](#dr-023--uscita-e-rimozione-dal-nucleo)
   punto 2, [DR-024](#dr-024--eliminazione-dellaccount-e-storico-del-nucleo)
   punto 2). Non sono esportati conti
   condivisi in sola lettura, conti di origine, descrizioni originali,
   collegamenti tecnici né quote limitate.
4. **Audit minimo.** Avvio, annullamento, scadenza e decadenza dei
   preavvisi, compresi quelli di eliminazione del nucleo, ed esportazioni
   dei dati del nucleo
   compaiono nell'audit minimo del nucleo
   ([FR-043](requirements.md#fr-043--registro-attività)).
5. **Rivalidazione alla scadenza.** Alla scadenza di un preavviso
   l'operazione è applicata in un'unica operazione indivisibile solo se, in
   quel momento: chi l'ha avviata è ancora amministratore attivo;
   l'interessato è ancora membro e, per un declassamento, ancora
   amministratore; dopo l'applicazione il nucleo, se ha altri membri, ha
   almeno un amministratore ([DR-022](#dr-022--almeno-un-amministratore)).
   Altrimenti il preavviso decade senza effetti e i membri ne sono informati.
   I preavvisi dello stesso nucleo che scadono insieme sono applicati uno
   alla volta, in ordine di avvio, ciascuno rivalidato sullo stato prodotto
   dal precedente. L'eliminazione del nucleo fa decadere i preavvisi ancora
   in corso.

## Matrice dei permessi del nucleo

Origine: P; C per le protezioni di [DR-026](#dr-026--tutela-dei-dati-condivisi-del-nucleo).
Il titolare di uno spazio personale ha tutti i permessi sul proprio spazio e
nessun altro utente ne ha.

| Azione nel nucleo | Amministratore | Membro |
|---|---|---|
| Vedere conti, movimenti, report, budget, abbonamenti, investimenti del nucleo | Sì | Sì |
| Vedere conti condivisi in sola lettura e attribuzioni ricevute | Sì | Sì |
| Esportare i dati del nucleo ([DR-026](#dr-026--tutela-dei-dati-condivisi-del-nucleo)) | Sì | Sì |
| Registrare, modificare, eliminare e importare movimenti nei conti del nucleo | Sì | Sì |
| Gestire abbonamenti e posizioni d'investimento del nucleo | Sì | Sì |
| Attribuire al nucleo movimenti dei propri conti personali | Sì | Sì |
| Vedere ed esportare le proprie attribuzioni, anche dopo l'uscita ([DR-009](#dr-009--attribuzioni)) | Sì, solo le proprie | Sì, solo le proprie |
| Creare, archiviare ed eliminare conti del nucleo | Sì | No |
| Gestire categorie, regole e budget del nucleo | Sì | No |
| Invitare membri, promuovere e rimuovere Membri | Sì | No |
| Rimuovere o declassare un altro amministratore | Sì, con preavviso e rivalidazione alla scadenza ([DR-026](#dr-026--tutela-dei-dati-condivisi-del-nucleo)) | No |
| Rinominare il nucleo | Sì | No |
| Eliminare il nucleo | Sì, con preavviso e rivalidazione se ha altri membri ([DR-026](#dr-026--tutela-dei-dati-condivisi-del-nucleo)) | No |
| Modificare attribuzioni o condivisioni di altri membri | No | No |
| Vedere l'identità di un ex membro nelle sue attribuzioni storiche o il loro collegamento con i movimenti di origine | No | No |
| Vedere o decidere le opposizioni alla conservazione nello storico | No (solo il referente autorizzato del titolare del trattamento, [DR-025](#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)) | No |
| Lasciare il nucleo | Sì, nel rispetto di [DR-022](#dr-022--almeno-un-amministratore) | Sì |
