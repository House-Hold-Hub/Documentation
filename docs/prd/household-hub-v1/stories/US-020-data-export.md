# US-020 — Esportazione dei dati

| Campo | Valore |
|---|---|
| Milestone | [M5 — Privacy e controllo dei dati](../milestones/M5-privacy-and-data-control.md) |
| Requisiti | [FR-041](../requirements.md#fr-041--esportazione-dei-dati), [FR-046](../requirements.md#fr-046--esportazione-dei-dati-del-nucleo), NFR-002, NFR-010, NFR-011 |
| Regole | [DR-003](../domain-rules.md#dr-003--isolamento-degli-spazi), [DR-009](../domain-rules.md#dr-009--attribuzioni), [DR-023](../domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo), [DR-026](../domain-rules.md#dr-026--tutela-dei-dati-condivisi-del-nucleo) |
| Dipende da | [US-015](US-015-household-roles-and-members.md), [US-016](US-016-household-accounts-and-categories.md), [US-018](US-018-transaction-attribution.md) |
| Questioni collegate | [Q-012](../open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione) (gate per le quote di ex membri e storiche in AC-06) |
| DoR | READY |

## Storia

Come utente, voglio scaricare tutti i miei dati in un formato riutilizzabile,
così da conservarli o portarli altrove; come membro di un nucleo, voglio
esportare i dati comuni, così da non perderli se il nucleo viene eliminato.

## Esito atteso

Un'esportazione completa dei dati dello spazio personale e delle proprie
attribuzioni, senza dati di altri utenti; un'esportazione dei dati del
nucleo per i membri attivi, nella forma in cui li vedono.

## Criteri di accettazione

- **AC-US-020-01** — L'esportazione contiene conti, movimenti, giroconti,
  categorie, regole, profili di importazione e budget del mio spazio
  personale e le attribuzioni che ho effettuato, comprese quelle verso
  nuclei che ho lasciato, con il nome del nucleo e il nome della categoria
  al momento dell'uscita.
  Dopo M6 include anche abbonamenti e posizioni d'investimento.
- **AC-US-020-02** — Il formato è leggibile da un normale foglio di calcolo
  e documentato; importi e date sono nel formato di NFR-009.
- **AC-US-020-03** — L'esportazione personale non contiene dati di altri utenti né
  dei nuclei, oltre ai nomi dei nuclei a cui ho attribuito quote.
- **AC-US-020-04** — Le descrizioni che iniziano con "=", "+", "-" o "@"
  sono esportate in modo che un foglio di calcolo non le interpreti come
  formule.
- **AC-US-020-05** — L'esportazione è disponibile solo all'utente che l'ha
  richiesta, dopo una nuova verifica dell'identità, e il file non resta
  disponibile oltre 24 ore.
- **AC-US-020-06** — Come membro attivo del nucleo A esporto i dati del
  nucleo: conti del nucleo con movimenti, giroconti e trasferimenti tra
  spazi, categorie, regole, budget, quote attribuite nella forma di FR-029,
  quote di ex membri e quote storiche nella forma della vista dei membri,
  senza identità né provenienza. Non sono inclusi conti
  condivisi in sola lettura, conti di origine, descrizioni originali,
  collegamenti tecnici né quote limitate durante un'opposizione. Valgono
  AC-02, AC-04 e AC-05.
- **AC-US-020-07** — Un ex membro o un non membro non può esportare i dati
  del nucleo, con lo stesso esito di una risorsa inesistente; ogni
  esportazione del nucleo è registrata nell'audit minimo del nucleo
  ([US-022](US-022-activity-log.md)).

## Verifica

Test di accettazione automatizzati; confronto tra conteggi dell'esportazione
e dati dello spazio; apertura manuale del file in un foglio di calcolo.

## Task

- **TASK-062** — Esportazione completa dello spazio personale e delle
  attribuzioni (AC-01 – AC-03).
- **TASK-063** — Protezione dei contenuti e dell'accesso al file esportato
  (AC-04, AC-05).
- **TASK-084** — Esportazione dei dati del nucleo per i membri attivi
  (AC-06, AC-07).

## Definition of Ready

READY. Le quote di ex membri e le quote storiche in AC-06 non si esportano
con dati reali prima del gate di Q-012; la registrazione in AC-07 richiede
l'audit minimo di US-022.
