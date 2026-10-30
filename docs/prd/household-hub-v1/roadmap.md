# Roadmap — House-Hold-Hub

Il dettaglio di ogni milestone è nelle [schede milestone](milestones/); i
requisiti sono in [requirements.md](requirements.md).

## MVP (M0–M5)

Obiettivo: un utente e la sua famiglia analizzano ogni mese le spese per
categoria, partendo dagli estratti conto, e pianificano con i budget,
mantenendo private le finanze personali.

| Milestone | Valore consegnato | Autorizzazione all'uso reale ([livelli](#livelli-di-rilascio)) |
|---|---|---|
| [M0](milestones/M0-foundation.md) | Accesso sicuro e spazio personale isolato | No (base tecnica) |
| [M1](milestones/M1-personal-monthly-analysis.md) | Analisi mensile personale con inserimento manuale | Sì, livello 1 (uso individuale interno) |
| [M2](milestones/M2-import.md) | Import degli estratti conto con duplicati e categorizzazione automatica | Sì, livello 1 |
| [M3](milestones/M3-budgets.md) | Budget personali con confronto previsto/consuntivo | Sì, livello 1 |
| [M4](milestones/M4-households.md) | Nuclei, conti comuni, condivisione, attribuzione, report e budget familiari | Solo livello 2, insieme a M5 e dopo il gate di Q-012 |
| [M5](milestones/M5-privacy-and-data-control.md) | Esportazione dei dati personali e del nucleo, eliminazione account, registro attività | Livello 2 insieme a M4, dopo il gate di Q-012; prerequisito per aprire il servizio a utenti esterni |

## Livelli di rilascio

| Livello | Significato | Condizioni |
|---|---|---|
| Implementato | Funzioni realizzate e verificate solo con dati di prova | Criteri di accettazione soddisfatti e NFR verificati, al netto degli elementi rinviabili non realizzati |
| Livello 1 — Uso individuale interno (M0–M3) | Uso reale del solo spazio personale da parte di utenti non esterni, senza nuclei | M0–M3 implementate; requisiti di sicurezza verificati come per dati reali: isolamento, cifratura in transito e a riposo, inclusi backup ed esportazioni temporanee, autenticazione e sessioni ([NFR-001](requirements.md#requisiti-non-funzionali) – NFR-003), file importati (NFR-011), prova di ripristino (NFR-012) e nessun accesso degli operatori tramite le funzioni del prodotto (NFR-013, esclusa la parte sul referente); revisione privacy (NFR-010) delle funzioni rilasciate; informativa generale alla registrazione (AC-US-001-09); nessun trattamento del [gate di utilizzo](open-questions-and-risks.md#gate-di-utilizzo) |
| Livello 2 — MVP autorizzato all'uso reale (M0–M5) | Uso reale con nuclei e apertura a utenti esterni | MVP implementato; gate di utilizzo di Q-012 superato e criteri cambiati dalla valutazione riverificati; revisione privacy (NFR-010), prova di ripristino con riapplicazione delle eliminazioni (NFR-012) e accesso del personale, compreso il referente (NFR-013), completati |

Livelli e condizioni sono confermati dal product owner (C, 2026-10-28).

**MVP implementato**: gli elementi indispensabili e quelli dipendenti da
decisioni aperte di M0–M5 sono al livello "Implementato", in particolare
con NFR-001 (isolamento), NFR-005 (coerenza dei report) e NFR-013 (accesso
del personale) verificati. **MVP autorizzato all'utilizzo reale**: livello 2.
Un MVP implementato non è di per sé utilizzabile con dati reali di nuclei.

## Perimetro dell'MVP

Classificazione confermata dal product owner il 2026-10-28 (C). Gli elementi rinviabili non bloccano né l'MVP implementato né quello
autorizzato: se non realizzati passano dopo l'MVP, con gli stessi
identificativi, e sono esclusi dai criteri di completamento delle milestone
e dalla verifica dei NFR. Gli elementi
dipendenti da decisioni aperte si progettano e si verificano con dati di
prova, ma non si usano con utenti reali prima della decisione.

### Indispensabili

| Ambito | Storie e criteri | Motivo |
|---|---|---|
| Accesso e isolamento | US-001 (escluso AC-08), US-002 | Base di sicurezza (NFR-001, NFR-003) |
| Analisi mensile personale | US-003 – US-006, US-007 (escluso AC-05) | Obiettivo G-1 |
| Importazione | US-008 (CSV e .xlsx), US-009, US-010, US-011 | Obiettivo G-4, metriche SM-01 e SM-02 |
| Budget | US-013 | Obiettivo G-2 |
| Nuclei | US-014 – US-019, salvo i criteri dipendenti indicati sotto | Obiettivo G-3; condivisione e attribuzione confermate (C) |
| Controllo dei dati | US-020; US-021 per eliminazione di account e spazio personale e accessi del personale (AC-01, AC-03 – AC-05, AC-09 – AC-11, AC-16, AC-19); audit minimo di US-022 (AC-01, AC-04 – AC-06) | Diritti dell'interessato e protezione dei dati condivisi |

### Rinviabili

| Elemento | Origine | Effetto del rinvio |
|---|---|---|
| [US-012](stories/US-012-imported-transfer-matching.md) — Abbinamento dei giroconti importati | P | Resta l'unione manuale (AC-US-006-06) |
| Registro completo di [US-022](stories/US-022-activity-log.md) (AC-US-022-02, AC-US-022-03, AC-US-022-07) | P | Restano l'audit minimo e le viste correnti di attribuzioni e condivisioni; minore trasparenza verso i membri (RISK-005) |
| AC-US-007-05 — Confronto con i mesi precedenti (FR-031) | P | Il report mostra solo il mese selezionato |
| AC-US-001-08 — Verifica in due passaggi per gli utenti (NFR-003) | P | Resta obbligatoria per il referente (NFR-013) |
| Formato .xls in AC-US-008-01 | P | Restano CSV e .xlsx |

### Dipendenti da decisioni aperte

| Elemento | Decisione | Comportamento in attesa |
|---|---|---|
| Conservazione delle attribuzioni degli ex membri, collegamento tecnico e rettifica contabile (AC-US-015-03, AC-US-015-04, AC-US-015-09, AC-US-015-11, AC-US-015-12, AC-US-015-14) | Q-012 punto 6 | Implementabili e verificabili con dati di prova; nessun uso reale prima del gate |
| Blocco dei movimenti vincolati e riconciliazione nei nuclei lasciati (AC-US-010-08, AC-US-015-11, AC-US-015-14, AC-US-018-06; voce di AC-US-022-01 sulle riconciliazioni) | Q-014 | Default: blocco; rettifica contabile bloccata se viola la capienza, con riconciliazione esplicita delle sole attribuzioni verso nuclei attivi; nessun ritiro autonomo |
| Opposizioni, limitazione e registro (AC-US-015-10, AC-US-021-12 – AC-US-021-15, AC-US-021-17, AC-US-021-18) | Q-012 punti 3–5, 7, 13 | Procedura di DR-025 senza eccezioni, solo con dati di prova |
| Quote storiche e riepilogo prima dell'eliminazione (AC-US-021-02, AC-US-021-06 – AC-US-021-08) | Q-012 punto 1; Q-015 | Policy provvisoria di Q-001; ripiego già specificato |
| Sezione sullo storico dei nuclei dell'informativa (AC-US-001-09, AC-US-014-09, AC-US-018-11) | Q-012 punto 2 | Testo provvisorio, non usato con utenti reali; l'informativa generale non ne dipende |
| Esportazione delle quote di ex membri e storiche (AC-US-020-06) | Q-012 punto 14 | Solo con dati di prova |

## Completamento V1 (M6)

| Milestone | Valore consegnato |
|---|---|
| [M6](milestones/M6-subscriptions-and-investments.md) | Abbonamenti con rinnovi, costo annuale effettivo ed equivalente mensile; investimenti a valorizzazione manuale; patrimonio |

M6 dipende da M1 e, per abbonamenti e posizioni del nucleo, da M4; può
essere anticipata, anche in parallelo a M4, se la priorità cambia.

## Evoluzione successiva (post-V1)

Ordine indicativo; ogni voce richiederà un proprio PRD o un aggiornamento di
questo.

| Tema | Descrizione | Origine |
|---|---|---|
| Sincronizzazione bancaria automatica | Acquisizione automatica dei movimenti dalle banche, riusando lotti, duplicati e regole già definiti | C |
| Notifiche | Avvisi su budget in esaurimento o superato, rinnovi imminenti, inviti | P |
| Carte di credito | Conto carta con addebito differito sul conto corrente ([Q-007](open-questions-and-risks.md#q-007--carte-di-credito)) | P |
| Previsioni di cassa | Proiezione del saldo futuro da budget e abbonamenti | P |
| Collegamento abbonamenti–movimenti | Riconoscimento dei movimenti che corrispondono a un abbonamento | P |
| Investimenti avanzati | Operazioni di acquisto e vendita, quantità, quotazioni automatiche | P |
| Ripartizione spese tra membri | Calcolo di chi deve a chi all'interno del nucleo | P |
| Andamento pluriennale | Trend per categoria su 12+ mesi e confronti anno su anno | P |
| Obiettivi di risparmio | Traguardi con importo e scadenza per spazio | P |
| Ruoli aggiuntivi | Ruolo di sola lettura, membri minorenni | P |
| Multi-valuta | Conti e movimenti in valute diverse da EUR | P |
| Allegati | Scontrini e ricevute associati ai movimenti | P |
