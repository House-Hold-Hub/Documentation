# US-008 — Importazione CSV/Excel

| Campo | Valore |
|---|---|
| Milestone | [M2 — Importazione](../milestones/M2-import.md) |
| Requisiti | [FR-020](../requirements.md#fr-020--importazione-da-file-csv-ed-excel), [FR-021](../requirements.md#fr-021--mappatura-e-profili-di-importazione), [FR-022](../requirements.md#fr-022--anteprima-e-validazione-dellimportazione), NFR-006, NFR-011 |
| Regole | [DR-005](../domain-rules.md#dr-005--movimenti), [DR-013](../domain-rules.md#dr-013--mese-di-competenza), [DR-015](../domain-rules.md#dr-015--valuta) |
| Dipende da | [US-005](US-005-manual-transactions.md) |
| Questioni collegate | [Q-007](../open-questions-and-risks.md#q-007--carte-di-credito), [Q-008](../open-questions-and-risks.md#q-008--banche-prioritarie-e-file-di-esempio) (non bloccanti) |
| DoR | READY |

## Storia

Come utente, voglio importare l'estratto conto esportato dalla mia banca,
così da non dover inserire i movimenti a mano.

## Esito atteso

Un file CSV o Excel diventa un insieme di movimenti del conto scelto, dopo
una mappatura riutilizzabile e un'anteprima controllata dall'utente.

## Criteri di accettazione

- **AC-US-008-01** — Scelto un conto attivo, posso caricare un file CSV
  (separato da virgola, punto e virgola o tabulazione) o Excel (.xlsx,
  .xls); per un file Excel con più fogli scelgo il foglio.
- **AC-US-008-02** — Indico le colonne di data, descrizione e importo,
  oppure di data, descrizione, dare e avere; il formato della data; il
  separatore decimale; le righe iniziali e finali da ignorare; per i CSV la
  codifica dei caratteri. Con un file in formato "1.234,56" e colonne
  dare/avere, le righe in dare diventano uscite e quelle in avere entrate,
  con importi esatti al centesimo.
- **AC-US-008-03** — L'anteprima mostra per ogni riga l'esito (valida,
  non valida con motivo) e il riepilogo dei conteggi; nessun movimento
  viene creato prima della conferma e abbandonare l'anteprima non cambia
  nulla.
- **AC-US-008-04** — Le righe non valide (es. data non interpretabile,
  importo mancante) sono escluse; posso confermare le righe valide e al
  termine vedo quante righe sono state importate ed escluse.
- **AC-US-008-05** — Posso salvare la mappatura come profilo con un nome;
  alla successiva importazione nello stesso conto viene proposto l'ultimo
  profilo usato e l'anteprima si genera senza rifare la mappatura.
- **AC-US-008-06** — Un file vuoto, in formato non supportato o oltre
  5 MB o 10.000 righe è rifiutato con un messaggio che indica il motivo.
- **AC-US-008-07** — Il contenuto delle celle è trattato come testo o
  numero e mai eseguito: una descrizione che inizia con "=" o "@" è
  importata e mostrata letteralmente.
- **AC-US-008-08** — Il file caricato non è più disponibile nel sistema dopo
  la conferma o l'abbandono dell'importazione.
- **AC-US-008-09** — I movimenti importati sono ordinari e "Da categorizzare", salvo
  quanto previsto da [US-011](US-011-categorization-rules.md), e sono
  riconoscibili come importati.
- **AC-US-008-10** — L'anteprima di un file di 1.000 righe è disponibile
  entro 10 secondi.

## Verifica

Test di accettazione automatizzati con i file di esempio anonimizzati delle
banche prioritarie (Q-008) e con file costruiti per i casi limite (dare/avere,
separatori, codifiche, righe di riepilogo, celle che iniziano con "=");
verifica manuale del flusso di mappatura da desktop e smartphone.

## Task

- **TASK-024** — Caricamento e lettura di file CSV ed Excel con limiti e
  trattamento sicuro dei contenuti (AC-01, AC-06, AC-07, AC-08).
- **TASK-025** — Mappatura di colonne e formati (AC-02).
- **TASK-026** — Anteprima con validazione per riga e conferma (AC-03,
  AC-04, AC-09, AC-10).
- **TASK-027** — Profili di importazione salvati e riproposti (AC-05).

## Definition of Ready

READY. La verifica richiede i file di esempio di Q-008. Perimetro MVP: il
formato .xls di AC-01 è rinviabile; CSV e .xlsx sono indispensabili
([roadmap](../roadmap.md#perimetro-dellmvp)).
