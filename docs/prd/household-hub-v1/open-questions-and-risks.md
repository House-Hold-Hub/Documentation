# Questioni aperte, assunzioni e rischi — House-Hold-Hub V1

## Questioni aperte

Una questione **bloccante** impedisce di marcare READY le storie indicate.
Una questione con **gate di utilizzo** non impedisce di marcare READY né di
implementare e verificare con dati di prova: impedisce di usare con dati
reali i trattamenti indicati. Le altre hanno una proposta di default già
recepita nel PRD, valida finché il product owner non decide diversamente.

| ID | Questione | Bloccante | Storie |
|---|---|---|---|
| [Q-001](#q-001--dati-conferiti-ai-nuclei-dopo-leliminazione-dellaccount) | Dati conferiti ai nuclei dopo l'eliminazione dell'account | No — decisione provvisoria, subordinata a Q-012 | US-021 |
| [Q-002](#q-002--registrazione-aperta-o-su-invito) | Registrazione aperta o su invito | No | US-001 |
| [Q-003](#q-003--campi-visibili-delle-attribuzioni) | Campi visibili delle attribuzioni | No | US-018 |
| [Q-004](#q-004--attribuzioni-di-un-membro-uscito) | Attribuzioni di un membro uscito | No — decisa il 2026-10-28, subordinata alle regole privacy (Q-012) | US-015, US-018, US-019, US-022 |
| [Q-005](#q-005--livello-di-dettaglio-degli-investimenti) | Livello di dettaglio degli investimenti | No | US-024 |
| [Q-006](#q-006--trattamento-dei-rimborsi) | Trattamento dei rimborsi | No | US-007, US-013 |
| [Q-007](#q-007--carte-di-credito) | Carte di credito | No | US-003, US-008 |
| [Q-008](#q-008--banche-prioritarie-e-file-di-esempio) | Banche prioritarie e file di esempio | No (serve alla verifica) | US-008, US-009 |
| [Q-009](#q-009--notifiche) | Notifiche | No | US-013, US-023 |
| [Q-010](#q-010--criteri-dei-duplicati) | Criteri dei duplicati | No | US-009, US-012 |
| [Q-011](#q-011--architettura-e-stack-tecnologico) | Architettura e stack tecnologico | No — chiusa il 2026-10-30 con l'approvazione di ADR-001 – ADR-006 | Tutte |
| [Q-012](#q-012--valutazione-legale-del-trattamento-alleliminazione) | Valutazione legale del trattamento all'eliminazione | No per READY, implementazione e verifica con dati di prova; [gate di utilizzo](#gate-di-utilizzo) per l'uso con dati reali dei trattamenti interessati e quindi per autorizzare M4 e M5 | US-001, US-014, US-015, US-018, US-019, US-020, US-021 |
| [Q-013](#q-013--gestione-dellopposizione) | Gestione dell'opposizione | No — decisa il 2026-10-28 | US-015, US-021 |
| [Q-014](#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro) | Movimenti vincolati e ritiro delle quote dell'ex membro | No — default: blocco; rettifica contabile bloccata se viola la capienza, con riconciliazione esplicita; autorizzazioni nei nuclei lasciati da definire; nessun ritiro autonomo | US-005, US-010, US-015, US-018, US-022 |
| [Q-015](#q-015--comportamento-alleliminazione-in-attesa-di-q-012) | Comportamento all'eliminazione in attesa di Q-012 | No — default: policy provvisoria di Q-001 | US-021 |

### Q-001 — Dati conferiti ai nuclei dopo l'eliminazione dell'account

Quando un utente elimina l'account, cosa succede alle quote che ha
attribuito ai nuclei e ai movimenti che ha registrato nei conti del nucleo?

- **A.** Si eliminano: la privacy è massima, ma report e budget storici del
  nucleo cambiano retroattivamente.
- **B.** Restano anonimizzate ("ex membro"): lo storico del nucleo resta
  coerente, ma serve verificare che sia compatibile con il diritto alla
  cancellazione.
- **C.** L'utente sceglie al momento dell'eliminazione tra A e B.

**Decisione iniziale (2026-10-28):** opzione B, con conservazione solo di
dati aggregati o realmente anonimizzati e, in mancanza di anonimizzazione
garantita, eliminazione e ricalcolo. Applicata, portava a eliminare sempre
le quote, perché non sono anonimizzabili.

**Riesame (2026-10-28):** la mancanza di anonimato rende le quote dati
personali, ma non impone di per sé la loro cancellazione: questa dipende
dalla base giuridica e dal bilanciamento con i diritti degli altri membri
(vedi [implicazioni](#implicazioni-privacy-delleliminazione-dellaccount)).

**Decisione provvisoria in vigore (2026-10-28, product owner):** preservare,
ove possibile e lecito, la coerenza storica dei report del nucleo senza
conservare dati personali non necessari:

- le quote attribuite diventano quote storiche del nucleo minimizzate, senza
  riferimenti diretti all'autore e non definite anonime;
- i movimenti dei conti del nucleo conservano i dati necessari alla
  correttezza contabile, con riferimenti personali minimizzati;
- base giuridica proposta: legittimo interesse dei membri restanti, con
  bilanciamento da verificare e diritto di opposizione;
- ripiego: cancellazione delle quote e ricalcolo dei report.

La decisione è subordinata a
[Q-012](#q-012--valutazione-legale-del-trattamento-alleliminazione). Esito
sul dominio: [DR-024](domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo).

### Q-002 — Registrazione aperta o su invito

Il servizio è aperto a chiunque o solo a persone invitate? **Default:**
registrazione aperta con verifica dell'email ([FR-001](requirements.md#fr-001--registrazione-e-accesso)).

### Q-003 — Campi visibili delle attribuzioni

Il nucleo deve poter vedere la descrizione originale del movimento?
**Default:** no; il titolare scrive una descrizione facoltativa e, se vuota,
il nucleo vede il nome della categoria ([FR-029](requirements.md#fr-029--riservatezza-delle-attribuzioni)).

### Q-004 — Attribuzioni di un membro uscito

**Default iniziale (superato):** le attribuzioni restavano al nucleo con il
nome dell'autore.

**Decisione (2026-10-28, product owner):** all'uscita volontaria da un
nucleo gli accessi sono revocati e l'identità dell'ex membro è nascosta
nelle attribuzioni storiche visibili al nucleo. Quote e collegamenti
tecnici strettamente necessari sono preservati, subordinatamente alle regole
privacy applicabili. L'uscita non equivale alla cancellazione dell'account.

Esito sul dominio: [DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo). L'estensione della stessa regola alla
rimozione da parte di un amministratore è una proposta (P). La base
giuridica per conservare le quote degli ex membri è inclusa in
[Q-012](#q-012--valutazione-legale-del-trattamento-alleliminazione).

### Q-005 — Livello di dettaglio degli investimenti

**Default:** posizioni con capitale investito e valore corrente aggiornati a
mano ([FR-039](requirements.md#fr-039--posizioni-di-investimento)).
Alternative: quantità e prezzo, operazioni di acquisto e vendita, quotazioni
automatiche (in [roadmap](roadmap.md#evoluzione-successiva-post-v1)).

### Q-006 — Trattamento dei rimborsi

**Default:** un'entrata con categoria di spesa riduce quella categoria
([DR-014](domain-rules.md#dr-014--rimborsi)). Alternativa: i rimborsi sono
entrate ordinarie e la spesa resta lorda.

### Q-007 — Carte di credito

Le carte di credito con addebito mensile non sono in V1. Se gli estratti
conto della carta sono la fonte principale delle spese dell'utente, il valore
di M2 si riduce. **Default:** fuori V1; da rivalutare dopo la raccolta dei
file di esempio ([Q-008](#q-008--banche-prioritarie-e-file-di-esempio)).

### Q-008 — Banche prioritarie e file di esempio

Quali banche usano i primi utenti? Servono file di esempio anonimizzati
(CSV ed Excel) per verificare mappatura, anteprima e duplicati. Non blocca la
definizione delle storie ma serve prima della loro verifica.

### Q-009 — Notifiche

Avvisi su budget superato o rinnovi imminenti sono necessari in V1?
**Default:** no; le informazioni sono visibili nelle rispettive viste e le
notifiche sono in [roadmap](roadmap.md#evoluzione-successiva-post-v1).

### Q-010 — Criteri dei duplicati

La tolleranza di ±3 giorni e la normalizzazione della descrizione in
[DR-016](domain-rules.md#dr-016--possibili-duplicati) vanno validate sui file
reali di [Q-008](#q-008--banche-prioritarie-e-file-di-esempio).

### Q-011 — Architettura e stack tecnologico

Questo PRD non definisce tecnologie, architettura, modello dati o interfacce
tecniche. Prima di implementare M0 servono decisioni di architettura
documentate separatamente (es. ADR), coerenti con i NFR. Non è una questione
di prodotto ma è un prerequisito per tutte le storie.

**Stato: chiusa (2026-10-30, product owner).** Le decisioni sono nel
[documento di architettura](../../architecture/household-hub-v1/README.md),
che non modifica requisiti né regole di dominio di questo PRD.

**Decisioni approvate:**

- stack di riferimento della V1: Python con Django, PostgreSQL, HTMX;
- monolite modulare: una sola applicazione, un solo database, un solo deploy;
- pagine renderizzate dal server, senza SPA;
- nessuna API pubblica nella V1;
- gli ADR indispensabili prima di M0, approvati dopo la Decision Review:

| ADR | Tema | Stato |
|---|---|---|
| [ADR-001](../../architecture/household-hub-v1/adr/ADR-001-modular-monolith.md) | Monolite modulare con app Django | Approvato |
| [ADR-002](../../architecture/household-hub-v1/adr/ADR-002-stack-and-server-rendered-ui.md) | Stack, versioni e interfaccia renderizzata dal server | Approvato |
| [ADR-003](../../architecture/household-hub-v1/adr/ADR-003-authentication-and-sessions.md) | Autenticazione e sessioni | Approvato |
| [ADR-004](../../architecture/household-hub-v1/adr/ADR-004-space-isolation-and-authorization.md) | Isolamento degli spazi e autorizzazione applicativa, senza RLS | Approvato; il meccanismo di accesso filtrato si sceglie durante M0 (VER-016) |
| [ADR-005](../../architecture/household-hub-v1/adr/ADR-005-persistence-and-monetary-amounts.md) | Convenzioni di persistenza, importi e invarianti | Approvato nei principi; i meccanismi di trigger e contatori restano da verificare |
| [ADR-006](../../architecture/household-hub-v1/adr/ADR-006-testing-and-continuous-integration.md) | Test e integrazione continua | Approvato |

**Verifiche tecniche** ([elenco completo](../../architecture/household-hub-v1/README.md#9-dettagli-da-verificare)).
Nessuna condiziona le decisioni approvate:

- **Da completare durante M0**: fanno parte del criterio di completamento di
  [M0](milestones/M0-foundation.md). Le parti che dipendono dall'hosting
  (rilevamento dell'IP dietro proxy per i limiti di tentativi, ruoli del
  database presso il fornitore) seguono la scelta del fornitore, prima del
  livello 1.
- **Rinviabili**: si chiudono entro la milestone indicata. Tra queste, i
  meccanismi delle invarianti concorrenti: prima di M1 per i giroconti e
  prima di M4 per capienza delle attribuzioni e amministratori.

**Decisioni successive**: seguono il
[piano degli ADR](../../architecture/household-hub-v1/README.md#10-piano-degli-adr),
ciascuna prima della milestone che la richiede, senza riaprire Q-011. Tra
queste rientrano hosting, backup e ripristino, report, importazione, nuclei e
privacy. Gli accessi tecnici di manutenzione e ripristino richiamati da
[DR-002](domain-rules.md#dr-002--privacy-per-default) e
[NFR-013](requirements.md#requisiti-non-funzionali) sono regolati dall'ADR
di hosting, previsto prima del livello 1 di rilascio.

### Q-012 — Valutazione legale del trattamento all'eliminazione

Questione aperta. Nessuna delle interpretazioni normative di questo PRD è
considerata validata. Un consulente privacy deve confermare:

1. la base giuridica proposta (legittimo interesse dei membri restanti) per
   conservare quote storiche e movimenti dei conti del nucleo, con l'esito
   del [bilanciamento](#base-giuridica-proposta-e-bilanciamento-da-verificare)
   documentato;
2. contenuto e momenti della sezione sullo storico dei nuclei
   dell'informativa (registrazione quando i nuclei sono disponibili,
   ingresso nel nucleo, prima attribuzione:
   [FR-044](requirements.md#fr-044--informativa-sullo-storico-del-nucleo));
3. la gestione dell'opposizione ([DR-025](domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)), inclusa la conservazione
   temporanea del collegamento tra utente e quote, dell'indirizzo email e del
   nome dell'account, l'uso del riferimento di provenienza
   ([DR-024](domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo))
   e le richieste presentate dopo l'eliminazione;
4. la limitazione del trattamento durante un'opposizione (art. 18 GDPR): se
   applicarla a ogni opposizione o solo su richiesta, se escludere le quote
   da report e budget o mantenerle nei totali a tutela dei diritti degli
   altri membri (art. 18(2)), se mostrare ai membri l'avviso di importi
   sospesi, che nei nuclei piccoli può rivelare l'opposizione, se la
   riassegnazione di categoria e l'eliminazione del nucleo sono compatibili
   con la limitazione, e come informare l'interessato prima della revoca
   (art. 18(3));
5. la gestione dei termini di risposta (art. 12 GDPR): un mese dal
   ricevimento, proroga fino a due mesi ulteriori comunicata con i motivi
   entro il primo mese, indicazione di reclamo e ricorso, coordinamento con
   la conservazione dell'indirizzo email e con la scadenza dei backup;
6. la base giuridica per conservare, all'uscita dal nucleo, le quote
   dell'ex membro senza la sua identità, il collegamento tecnico tra ex
   membro, quote e movimento di origine, il conseguente blocco dei
   movimenti vincolati e la rettifica contabile delle quote degli ex membri
   ([DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo));
7. la durata di conservazione del registro delle opposizioni;
8. se, nel ripiego, i membri del nucleo vanno considerati destinatari a cui
   comunicare la cancellazione (art. 19 GDPR) e se e come mostrare l'avviso
   dei mesi ricalcolati;
9. se e per quanto tempo un registro tecnico di sicurezza, non visibile ai
   membri, possa conservare le azioni dell'utente eliminato;
10. i tempi di 30 giorni per l'eliminazione e 35 giorni per i backup;
11. se serve una valutazione d'impatto (art. 35 GDPR);
12. l'applicabilità del GDPR rispetto ad [A-003](#assunzioni) e
    [Q-002](#q-002--registrazione-aperta-o-su-invito);
13. se e a quali condizioni le opposizioni ripetute o prive di motivi nuovi
    possano essere trattate diversamente; fino ad allora ogni opposizione
    applica la limitazione ([DR-025](domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo) punto 8);
14. la base giuridica per l'esportazione, da parte dei membri attivi, delle
    quote di ex membri e delle quote storiche
    ([FR-046](requirements.md#fr-046--esportazione-dei-dati-del-nucleo)).

#### Gate di utilizzo

Finché Q-012 è aperta, i trattamenti seguenti possono essere progettati,
implementati e verificati solo con dati di prova e non possono essere usati
con dati di utenti reali:

| Trattamento | Regole | Punti di Q-012 |
|---|---|---|
| Conservazione delle attribuzioni degli ex membri, collegamento tecnico, blocco dei movimenti vincolati e rettifica contabile | DR-023 punti 3–7 | 6 |
| Quote storiche, riferimento di provenienza e movimenti dei conti del nucleo senza autore dopo l'eliminazione | DR-024 punti 2–3 | 1, 3 |
| Conservazione di collegamento, email e nome durante un'opposizione | DR-024 punto 6 | 3, 5 |
| Limitazione, avvisi ai membri, registro delle opposizioni | DR-025 | 3, 4, 5, 7, 13 |
| Ripiego e avviso dei mesi ricalcolati | DR-024 punto 7 | 8 |
| Sezione sullo storico dei nuclei dell'informativa | FR-044 | 2 |
| Esportazione delle quote di ex membri e delle quote storiche | FR-046 | 14 |

Uscite ed eliminazioni possono avvenire dal primo giorno d'uso dei nuclei:
per questo M4 e M5 sono autorizzate all'uso reale solo insieme e solo dopo
la chiusura di Q-012 ([livelli di rilascio](roadmap.md#livelli-di-rilascio)).
Le funzioni di M0–M3 non usano questi trattamenti: l'informativa generale
alla registrazione non dipende dal gate. Il gate si supera quando
ogni punto è risolto e i requisiti e i criteri interessati sono aggiornati.

Se la valutazione esclude la base proposta per l'eliminazione, il ripiego di
DR-024 si applica a tutte le eliminazioni e cambiano AC-US-021-06 –
AC-US-021-08. Per l'uscita dal nucleo il PRD non definisce un ripiego: se il
punto 6 esclude la base proposta, DR-023 va rivisto prima di superare il
gate. I punti 2–7, 10, 13 e 14 possono cambiare AC-US-001-09, AC-US-014-09,
AC-US-015-03, AC-US-015-04, AC-US-015-09 – AC-US-015-12, AC-US-015-14,
AC-US-018-11,
AC-US-020-06, AC-US-021-02 e AC-US-021-12 – AC-US-021-19.

### Q-013 — Gestione dell'opposizione

**Default iniziale (superato):** decisione del gestore del servizio entro
30 giorni.

**Decisione (2026-10-28, product owner):** le opposizioni sono valutate dal
soggetto individuato come titolare del trattamento, tramite un referente
autorizzato, con decisione motivata e tracciabile. Gli amministratori dei
nuclei non possono decidere. Esito sul dominio: [DR-025](domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo).

### Q-014 — Movimenti vincolati e ritiro delle quote dell'ex membro

Dopo l'uscita da un nucleo le attribuzioni restano collegate al movimento di
origine per preservarne la capienza ([DR-023](domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo)
punti 5–6): il movimento è vincolato.

**Default (P):** blocco delle operazioni che violerebbero la capienza.

**Decisione (2026-10-28, product owner):** la rettifica contabile di DR-023
punto 6 non riduce le attribuzioni per ordine cronologico né in altro modo
automatico. Se viola la capienza è bloccata e richiede una riconciliazione
esplicita delle attribuzioni. La riduzione automatica a partire dalla quota
più recente, presente in una bozza della versione 0.2.1, è respinta.

Da decidere:

1. **Autorizzazioni nei nuclei lasciati.** Chi può riconciliare, in una
   rettifica contabile, le attribuzioni verso un nucleo lasciato, e con
   quali garanzie per i membri di quel nucleo. Finché non è deciso, quelle
   attribuzioni non si riconciliano: la rettifica resta bloccata, il
   movimento resta vincolato e l'errore resta nel saldo e nei report
   personali ([RISK-015](#rischi)).
2. **Ritiro senza errore contabile**, oggi escluso: senza errore l'ex membro
   ottiene la rimozione delle quote solo con un'opposizione
   ([DR-025](domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)).
   Alternative non adottate:
   - **A.** Ritiro autonomo: l'ex membro rimuove le proprie quote da un
     nucleo lasciato, con l'avviso di ricalcolo ai membri; equivale al
     ritiro già possibile prima dell'uscita.
   - **B.** Finestra di ritiro solo per i membri rimossi da un
     amministratore, che non hanno avuto la possibilità di rivedere le
     attribuzioni prima dell'uscita.

Ogni soluzione deve preservare la capienza
([DR-009](domain-rules.md#dr-009--attribuzioni)) e passa per Q-012 (punto 6).

### Q-015 — Comportamento all'eliminazione in attesa di Q-012

Il PRD mantiene come comportamento previsto la policy provvisoria di
[Q-001](#q-001--dati-conferiti-ai-nuclei-dopo-leliminazione-dellaccount)
(quote storiche minimizzate) e il ripiego come alternativa. Resta da
decidere se, per ridurre il lavoro esposto all'esito di Q-012, l'MVP debba
implementare per primo il ripiego (cancellazione e ricalcolo), che serve
comunque, e aggiungere le quote storiche solo dopo il superamento del gate.

**Default:** nessun cambiamento; la decisione spetta al product owner prima
della pianificazione di TASK-066.

## Implicazioni privacy dell'eliminazione dell'account

Questa sezione descrive le conseguenze di
[DR-024](domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo).
Non costituisce un parere legale: le norme sono richiamate dal testo del GDPR
e la loro applicazione va confermata con
[Q-012](#q-012--valutazione-legale-del-trattamento-alleliminazione).

### Cosa resta e cosa viene eliminato

| Dato | Trattamento | Motivo |
|---|---|---|
| Risorse dello spazio personale | Eliminate | Dati personali senza altra finalità |
| Condivisioni in sola lettura e inviti in attesa | Revocati o annullati | Riguardano solo l'utente |
| Attribuzioni di un ex membro con account attivo | Conservate senza identità visibile, collegate in modo non visibile al movimento di origine, che resta vincolato; ridotte solo per riconciliazione autorizzata in una rettifica contabile (Q-014) o per opposizione accolta | Coerenza dello storico e capienza dei movimenti; base giuridica da verificare (Q-012 punto 6) |
| Quote attribuite ai nuclei, anche già lasciati | Trasformate in quote storiche minimizzate (nucleo, mese, categoria, tipo, importo, riferimento di provenienza), una per attribuzione; nel ripiego eliminate con ricalcolo | Coerenza dello storico del nucleo e rettificabilità; legittimo interesse da verificare |
| Movimenti dei conti del nucleo registrati o importati dall'utente | Conservati con i dati contabili necessari, senza autore; nel ripiego sostituite nei testi le occorrenze di nome, cognome ed email dell'account | Correttezza di saldi, giroconti e duplicati del conto del nucleo |
| Voci del registro attività con l'utente come autore o oggetto | Eliminate dai registri visibili | Identificano la persona e non servono allo storico |
| Quote oggetto di opposizione | Limitate fino all'esito: conservate singolarmente, non modificabili, non trasformate, escluse da report e budget | Limitazione durante la verifica (art. 18(1)(d)); da validare con Q-012 |
| Collegamento tra utente e quote durante un'opposizione | Conservato, non visibile ai membri, fino alla comunicazione dell'esito nei termini dell'art. 12 | Necessario per applicare l'esito |
| Indirizzo email dell'account durante un'opposizione | Conservato fino alla comunicazione dell'esito | Necessario per comunicare l'esito |
| Nome dell'account durante un'opposizione | Conservato fino all'esecuzione del ripiego, se l'opposizione è accolta | Necessario a sostituire le occorrenze nei testi dei movimenti del nucleo; da validare con Q-012 |
| Metriche d'uso aggregate su più utenti | Conservate | Prive di riferimenti alla persona |
| Copie esportate in precedenza dall'utente | Fuori dal controllo del servizio | Sono già in possesso dell'utente |

### Perché le quote storiche non sono anonime

Rimuovere autore, conto, movimento originale, descrizione e giorno lascia un
importo per nucleo, mese e categoria che deriva da una sola persona. I membri
restanti conoscono la composizione del nucleo e hanno già visto le
attribuzioni con il nome dell'autore: possono ricondurre l'importo
all'utente eliminato. Per il GDPR un dato è anonimo solo se nessuno può
identificare la persona con mezzi ragionevolmente utilizzabili, quindi le
quote storiche restano dati personali. Questo comporta che servano una base
giuridica, la minimizzazione e il rispetto dei diritti dell'interessato; non
comporta di per sé l'obbligo di cancellarle.

### Base giuridica proposta e bilanciamento da verificare

- **Durante l'appartenenza al nucleo:** le attribuzioni servono a fornire il
  servizio all'utente (esecuzione del contratto, art. 6(1)(b)).
- **Dopo l'eliminazione dell'account:** il contratto con l'utente cessa e la
  conservazione si fonderebbe sul legittimo interesse dei membri restanti
  (art. 6(1)(f)).
- **Non sul consenso:** la sua revoca imporrebbe la cancellazione
  (art. 17(1)(b)).
- **Dichiarata fin dall'inizio:** nell'informativa alla registrazione e alla
  prima attribuzione ([FR-044](requirements.md#fr-044--informativa-sullo-storico-del-nucleo)).

| Elemento del bilanciamento | Valutazione proposta, da verificare |
|---|---|
| Interesse | Storico coerente di report e budget del nucleo; correttezza dei conti del nucleo |
| Necessità | Senza le quote i totali passati cambiano; l'anonimizzazione non è possibile, quindi non esiste un'alternativa meno invasiva che preservi la coerenza |
| Minimizzazione | Solo nucleo, mese, categoria, tipo, importo e un riferimento di provenienza casuale; quote mostrate aggregate per mese, categoria e tipo senza distinguerne la provenienza, ma conservate singolarmente per consentire rettifiche e opposizioni; nessun dato sul conto personale |
| Aspettative ragionevoli | Quote condivise volontariamente con il nucleo, dopo un'informativa esplicita |
| Impatto sull'interessato | Basso: i membri non ricevono informazioni nuove |
| Garanzie | Quote immutabili, eliminate con il nucleo, opposizione, ripiego |

### Diritto di opposizione

- L'utente può opporsi al trattamento fondato sul legittimo interesse per
  motivi connessi alla sua situazione particolare; il titolare può
  proseguire solo dimostrando motivi legittimi cogenti prevalenti, e l'onere
  è suo (art. 21(1)). Se l'opposizione è accolta, i dati vanno cancellati
  (art. 17(1)(c)).
- Possono opporsi l'utente che elimina l'account, nel flusso o prima, e
  l'ex membro per le quote in un nucleo lasciato ([DR-025](domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo)).
- Decide il titolare del trattamento tramite un referente autorizzato, con
  decisione motivata e registrata; gli amministratori dei nuclei non hanno
  alcun ruolo ([Q-013](#q-013--gestione-dellopposizione)).
- Durante la valutazione le quote sono limitate (art. 18(1)(d)) e
  l'interessato è informato prima della revoca della limitazione
  (art. 18(3)).
- Termini: un mese dal ricevimento, prorogabile fino a due mesi ulteriori
  comunicando i motivi entro il primo mese; la risposta indica reclamo e
  ricorso (art. 12(3)–(4)).
- Ogni opposizione, anche ripetuta, segue la stessa procedura finché Q-012
  non decide diversamente (punto 13).
- Dopo l'eliminazione dell'account il collegamento tra utente e quote non
  esiste più: le quote storiche restano individuabili tramite il riferimento
  di provenienza, ma il suo uso per richieste successive e il modo di
  ricondurre la richiesta alle quote sono da confermare con Q-012 (punto 3).

### Ripiego: cancellazione e ricalcolo

Si applica se l'opposizione è accolta, o a tutte le eliminazioni se Q-012
esclude la base giuridica proposta:

- totali, ripartizioni per categoria e consuntivi di budget dei mesi
  interessati diminuiscono degli importi eliminati e restano coerenti
  ([DR-012](domain-rules.md#dr-012--invariante-dei-totali));
- i membri ricevono un avviso con i mesi ricalcolati, che non nomina la
  persona;
- i movimenti dei conti del nucleo non sono eliminati, perché ciò
  altererebbe saldi e giroconti: nei testi si sostituiscono solo le
  occorrenze di nome, cognome ed email dell'account.

### Vincoli normativi, interpretazioni e decisioni

| Affermazione | Classificazione |
|---|---|
| Un dato è anonimo solo se nessuno può identificare la persona con mezzi ragionevolmente utilizzabili (considerando 26) | Vincolo normativo |
| L'esenzione per uso domestico non copre chi fornisce la piattaforma (art. 2(2)(c), considerando 18) | Vincolo normativo |
| La cancellazione è dovuta solo se ricorre un motivo dell'art. 17(1); le eccezioni dell'art. 17(3) sono un'altra cosa | Vincolo normativo |
| Opposizione al legittimo interesse e onere dei motivi cogenti a carico del titolare (art. 21(1)) | Vincolo normativo |
| Risposta all'interessato entro un mese, prorogabile fino a due mesi ulteriori comunicando i motivi entro il primo mese; indicazione di reclamo e ricorso (art. 12(3)–(4)) | Vincolo normativo; applicazione da confermare (Q-012) |
| Diritto di ottenere la limitazione durante la verifica di un'opposizione e di essere informati prima della revoca (art. 18(1)(d), 18(3)) | Vincolo normativo |
| Le quote storiche sono dati personali per via della conoscenza dei membri | Interpretazione prudente adottata |
| Il legittimo interesse dei membri restanti giustifica la conservazione minimizzata | Interpretazione da validare (Q-012) |
| La base giuridica dello storico va dichiarata fin dall'inizio | Interpretazione da validare (Q-012) |
| I membri sono destinatari da informare nel ripiego (art. 19) | Da validare (Q-012) |
| Coerenza dello storico come obiettivo | Decisione di prodotto: una famiglia non ha obblighi di tenuta contabile, che il codice civile pone alle imprese (art. 2214 c.c.) |
| Tempi di 30 e 35 giorni, riapplicazione delle eliminazioni ai ripristini | Decisione di prodotto da validare |
| Limitazione applicata a ogni opposizione, con esclusione delle quote da report e budget | Decisione di prodotto da validare (Q-012): l'art. 18(2) potrebbe consentire di mantenerle nei totali a tutela dei diritti degli altri membri |
| Opposizioni decise dal titolare tramite referente autorizzato, mai dagli amministratori dei nuclei | Decisione di prodotto (Q-013) |
| All'uscita dal nucleo identità nascosta, quote e collegamento tecnico con il movimento conservati, movimenti vincolati | Decisione di prodotto (Q-004, decisione del 2026-10-28; blocco: Q-014); base giuridica da validare (Q-012) |
| Quote storiche non accorpate, con riferimento di provenienza | Decisione di prodotto (2026-10-28); base giuridica da validare (Q-012) |
| Rettifica contabile dei movimenti vincolati distinta dall'opposizione, bloccata se viola la capienza e senza riduzione automatica delle attribuzioni | Decisione di prodotto (2026-10-28); autorizzazioni nei nuclei lasciati aperte (Q-014); base giuridica inclusa nel gate (Q-012 punto 6) |
| Opposizioni ripetute trattate come ogni altra opposizione | Decisione prudente in attesa di Q-012 (punto 13); nessuna eccezione assunta |
| Nessun trattamento con dati reali prima del gate | Decisione di prodotto ([gate di utilizzo](#gate-di-utilizzo)) |
| Utenti nell'UE e registrazione aperta | Assunzioni (A-003, Q-002) |

### Eccezioni legali da valutare

Da confermare con
[Q-012](#q-012--valutazione-legale-del-trattamento-alleliminazione):

- **Accertamento, esercizio o difesa di un diritto in sede giudiziaria**:
  dati coinvolti in una contestazione in corso possono essere conservati,
  bloccati e non visibili, fino alla sua conclusione (art. 17(3)(e)).
- **Obblighi di conservazione per legge**: nessuno noto in V1, che non
  prevede pagamenti da parte degli utenti ([A-007](#assunzioni)).
- **Sicurezza**: un registro tecnico, separato e non visibile ai membri,
  potrebbe conservare per un periodo limitato le azioni dell'utente per
  indagare abusi.

### Rischi residui

- I membri ricordano ciò che hanno già visto e possono ricondurre le quote
  storiche alla persona: per questo sono trattate come dati personali.
- Descrizioni bancarie e note dei movimenti del nucleo possono citare la
  persona; fuori dal ripiego il servizio non le modifica.
- Backup e ripristini: coperti dai tempi e dalla riapplicazione delle
  eliminazioni di DR-024.
- Le voci del registro su uscite e rimozioni e l'autore dei movimenti dei
  conti del nucleo restano visibili: aiutano a ricondurre all'ex membro le
  quote "ex membro" (DR-023 punto 2).
- Gli avvisi di importi sospesi e di mesi ricalcolati possono rivelare
  un'opposizione e la persona nei nuclei piccoli (DR-025 punto 2); l'avviso
  di una riconciliazione in un nucleo lasciato, se Q-014 la autorizza,
  rivela che un ex membro ha corretto un proprio movimento (DR-023
  punto 6).
- Altri riferimenti indiretti alla persona nei testi dei movimenti del
  nucleo restano anche nel ripiego.

## Assunzioni

| ID | Assunzione | Impatto se falsa |
|---|---|---|
| A-001 | Valuta unica EUR | DR-015, NFR-009, report e budget |
| A-002 | Utenti in Italia; interfaccia in italiano | NFR-009, tassonomia predefinita FR-017 |
| A-003 | Utenti nell'UE: si applica il GDPR | FR-041, FR-042, FR-044, NFR-010 |
| A-004 | I file bancari sono tabelle con intestazione che contengono almeno data, descrizione e importo (unico o dare/avere) | FR-020, FR-021 |
| A-005 | Volumi: ≤ 10.000 movimenti per spazio e anno, ≤ 10 membri per nucleo, ≤ 10 nuclei per utente | NFR-006 |
| A-006 | In V1 i movimenti entrano solo manualmente o da file | Roadmap |
| A-007 | Il servizio non prevede pagamenti da parte degli utenti in V1 | Ambito |
| A-008 | Ogni membro del nucleo ha un proprio account; non esistono account condivisi | FR-001, DR-003 |

## Rischi

| ID | Rischio | Impatto | Mitigazione |
|---|---|---|---|
| RISK-001 | Esposizione di dati tra spazi o nuclei | Alto: perdita di fiducia, violazione di dati personali | DR-003, NFR-001 con test negativi in ogni storia, revisione di sicurezza alla fine di M4 |
| RISK-002 | Doppi conteggi o totali incoerenti per attribuzioni, condivisioni, giroconti, trasferimenti tra spazi, rimborsi, uscite e rientri di membri e budget su due livelli | Alto: l'analisi mensile perde valore | DR-007, DR-009, DR-011, DR-012 (quadratura dei saldi e capienza), DR-019; un unico dataset di verifica riusato da US-007, US-013, US-019 |
| RISK-003 | Eterogeneità dei file bancari (codifiche, separatori, date, dare/avere, righe di riepilogo) | Medio-alto: import inutilizzabile per alcune banche | Mappatura e profili, anteprima, file di esempio (Q-008) |
| RISK-004 | Falsi positivi o negativi nel controllo duplicati | Medio: movimenti mancanti o doppi | Decisione dell'utente riga per riga, nessuna cancellazione automatica, lotti annullabili |
| RISK-005 | Deduzione di informazioni private dalle attribuzioni | Medio | Campi minimi (FR-029), audit minimo (FR-043); registro completo rinviabile |
| RISK-006 | Perdita di dati per annullamento di lotti o eliminazioni | Medio | Conferme con conteggio degli elementi coinvolti, backup (NFR-012) |
| RISK-007 | Ampliamento dell'ambito (sincronizzazione, carte, investimenti avanzati) | Medio: ritardo dell'MVP | Confini MVP espliciti, voci in roadmap |
| RISK-008 | La futura sincronizzazione bancaria dipende da fornitori terzi e normativa | Basso in V1 | Lotti, duplicati e regole già indipendenti dalla fonte dei movimenti |
| RISK-009 | Riferimenti all'utente eliminato che restano in dati del nucleo, registri o backup | Alto: violazione del diritto alla cancellazione | DR-024, test di ricerca dei riferimenti residui, prova di ripristino con riapplicazione delle eliminazioni, valutazione legale Q-012 |
| RISK-010 | Ricalcolo dei report storici del nucleo, nel ripiego, percepito come perdita di dati | Medio | Ripiego limitato ai casi di DR-024 punto 7, avviso ai membri con i mesi ricalcolati |
| RISK-011 | La valutazione legale esclude la base giuridica proposta | Medio: tutte le eliminazioni passano al ripiego e lo storico cambia | Ripiego già specificato in DR-024 e nei criteri di US-021; Q-012 prima dell'implementazione definitiva |
| RISK-012 | Quote storiche e attribuzioni di ex membri sono riconducibili alla persona da parte dei membri | Medio | Trattate come dati personali; identità nascosta, minimizzazione, visualizzazione aggregata senza provenienza e senza distinguere tra ex membri; opposizione; gate di utilizzo di Q-012 |
| RISK-013 | Opposizioni gestite fuori dai termini dell'art. 12 o senza traccia della decisione | Alto: violazione dei diritti dell'interessato | Registro delle opposizioni con date di ricezione, proroga e comunicazione (DR-025); referente autorizzato; verifica in Q-012 |
| RISK-014 | Gli avvisi di importi sospesi o ricalcolati rivelano ai membri l'opposizione e la persona | Medio | Avviso senza nome; decisione su contenuto e opportunità in Q-012 (punti 4 e 8) |
| RISK-015 | I movimenti vincolati impediscono di correggere errori personali (es. duplicati importati) dopo l'uscita da un nucleo | Medio-alto: finché Q-014 non definisce le autorizzazioni nei nuclei lasciati, un duplicato o un importo errato con quote in un nucleo lasciato resta nel saldo e nei report personali; richieste di opposizione strumentali | Messaggio che indica le quote vincolanti; rettifica contabile con riconciliazione esplicita delle attribuzioni verso nuclei attivi (DR-023 punto 6); autorizzazioni nei nuclei lasciati e alternative in Q-014 |
| RISK-016 | Un utente registra come spesa un trasferimento tra spazi, o attribuisce al nucleo un rimborso ricevuto dal nucleo | Medio: doppio conteggio non rilevabile, perché i due lati non sono collegati | Regola e informazioni contestuali (DR-007, DR-009); trasferimenti mostrati fuori dai totali; quadratura dei saldi nel dataset di verifica |
| RISK-017 | Accessi del personale ai dati degli spazi | Alto: violazione della riservatezza | NFR-013 con test negativi e registro degli accessi |
| RISK-018 | Un Membro rimosso con effetto immediato perde l'accesso ai dati comuni prima di un'eliminazione del nucleo | Medio | Preavviso ed esportazione per i membri attivi (DR-026); alternativa B di Q-014 |
| RISK-019 | Rettifica contabile dichiarata senza un errore reale per ritirare quote da un nucleo lasciato | Medio, solo se Q-014 autorizza la riconciliazione nei nuclei lasciati: lo storico del nucleo cambia senza opposizione | Nessuna riduzione automatica; riconciliazione esplicita; con il default di Q-014 le quote nei nuclei lasciati non si riconciliano; nella decisione sulle autorizzazioni: motivo dichiarato, avviso ai membri, voce nell'audit minimo |
| RISK-020 | Un trasferimento tra spazi dichiarato per uno scambio che non rientra nella definizione (es. con un non membro) esclude dai totali una spesa reale | Medio | Definizione e informazione contestuale (DR-007); quadratura dei saldi; trasferimenti mostrati fuori dai totali |
