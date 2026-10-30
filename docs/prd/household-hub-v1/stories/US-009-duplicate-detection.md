# US-009 — Rilevamento duplicati

| Campo | Valore |
|---|---|
| Milestone | [M2 — Importazione](../milestones/M2-import.md) |
| Requisiti | [FR-023](../requirements.md#fr-023--rilevamento-dei-duplicati) |
| Regole | [DR-016](../domain-rules.md#dr-016--possibili-duplicati) |
| Dipende da | [US-008](US-008-file-import.md) |
| Questioni collegate | [Q-010](../open-questions-and-risks.md#q-010--criteri-dei-duplicati) (non bloccante), [Q-008](../open-questions-and-risks.md#q-008--banche-prioritarie-e-file-di-esempio) (file di esempio per la verifica) |
| DoR | READY |

## Storia

Come utente, voglio che l'importazione mi segnali i movimenti già presenti,
così da poter importare estratti conto con periodi sovrapposti senza
contare due volte le stesse spese.

## Esito atteso

I possibili duplicati sono evidenziati in anteprima con un esito
predefinito prudente; la decisione finale resta all'utente.

## Criteri di accettazione

- **AC-US-009-01** — Reimportando lo stesso file nello stesso conto, tutte
  le righe risultano "Duplicato probabile" ed escluse per default;
  confermando senza cambiare gli esiti non viene creato alcun movimento.
- **AC-US-009-02** — Importando un file dal 15 febbraio al 15 marzo e poi
  uno dal 1° al 31 marzo, nel secondo risultano escluse solo le righe dal
  1° al 15 marzo già importate.
- **AC-US-009-03** — Una riga con stesso tipo e importo di un movimento
  inserito a mano, data entro ±3 giorni e descrizione diversa risulta
  "Possibile corrispondenza", inclusa ed evidenziata, con il riferimento al
  movimento esistente.
- **AC-US-009-04** — Due righe identiche nello stesso file (es. due pedaggi
  uguali nello stesso giorno) sono incluse ed evidenziate come ripetizione.
- **AC-US-009-05** — Le descrizioni "PAGAMENTO  POS Bar Roma." e "pagamento
  pos bar roma" sono considerate uguali.
- **AC-US-009-06** — Posso cambiare l'esito di ogni riga e includere o
  escludere in blocco tutti i duplicati probabili.
- **AC-US-009-07** — Il controllo considera solo il conto di destinazione:
  un movimento identico su un altro conto non è un duplicato.
- **AC-US-009-08** — Il controllo non modifica né elimina mai movimenti
  esistenti.
- **AC-US-009-09** — Se il conto contiene un solo movimento "Pedaggio A1"
  da 2,50 € del 3 marzo e il file contiene due righe identiche con quei
  dati, una sola riga risulta "Duplicato probabile" ed esclusa; l'altra è
  valida, inclusa ed evidenziata come ripetizione nel file. Ogni movimento
  esistente è abbinato al più a una riga (DR-016).

## Verifica

Test di accettazione automatizzati con file costruiti per ciascun caso e
con i file di esempio di Q-008, misurando falsi positivi e falsi negativi
per validare i criteri (Q-010).

## Task

- **TASK-028** — Riconoscimento di duplicati probabili e possibili
  corrispondenze rispetto ai movimenti del conto, con abbinamento uno a uno
  (AC-01 – AC-03, AC-05, AC-07 – AC-09).
- **TASK-029** — Riconoscimento delle ripetizioni nel file (AC-04).
- **TASK-030** — Decisione per riga e in blocco nell'anteprima (AC-06).

## Definition of Ready

READY. I criteri seguono il default di Q-010, da validare sui file reali.
