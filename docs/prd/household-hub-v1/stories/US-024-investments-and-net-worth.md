# US-024 — Investimenti e patrimonio

| Campo | Valore |
|---|---|
| Milestone | [M6 — Abbonamenti e investimenti](../milestones/M6-subscriptions-and-investments.md) |
| Requisiti | [FR-039](../requirements.md#fr-039--posizioni-di-investimento), [FR-040](../requirements.md#fr-040--patrimonio), NFR-004 |
| Regole | [DR-021](../domain-rules.md#dr-021--investimenti), [DR-006](../domain-rules.md#dr-006--giroconti), [DR-011](../domain-rules.md#dr-011--perimetro-dei-report) |
| Dipende da | [US-003](US-003-personal-accounts.md), [US-006](US-006-transfers.md) |
| Questioni collegate | [Q-005](../open-questions-and-risks.md#q-005--livello-di-dettaglio-degli-investimenti) (non bloccante) |
| DoR | READY |

## Storia

Come utente, voglio registrare i miei investimenti e vedere il mio
patrimonio complessivo, così da avere un quadro completo oltre alle spese.

## Esito atteso

Posizioni d'investimento a valorizzazione manuale e un patrimonio per
spazio senza doppi conteggi tra versamenti e valore investito.

## Criteri di accettazione

- **AC-US-024-01** — In un conto investimento registro una posizione con
  nome, tipologia (es. ETF, azioni, obbligazioni, fondi, liquidità),
  capitale investito e valore corrente con data di riferimento; vedo la
  differenza tra valore e capitale in importo e percentuale.
- **AC-US-024-02** — Aggiornando il valore corrente con una nuova data,
  vedo il valore aggiornato e lo storico dei valori dichiarati.
- **AC-US-024-03** — Un versamento di 1.000,00 € dal conto corrente al
  conto investimento è un giroconto: non compare tra le uscite del report.
- **AC-US-024-04** — Dati un conto corrente con saldo 2.000,00 €, un conto
  deposito con 5.000,00 € e un conto investimento con versato netto
  1.000,00 € e posizioni dal valore totale di 1.100,00 €, il patrimonio è
  8.100,00 €.
- **AC-US-024-05** — Una posizione il cui valore non è aggiornato da più di
  90 giorni è segnalata.
- **AC-US-024-06** — Il patrimonio del nucleo comprende solo conti e
  posizioni del nucleo, non i conti condivisi in sola lettura (richiede M4).

## Verifica

Test di accettazione automatizzati con i dati di AC-04; verifica che il
report mensile non cambi per effetto di versamenti e aggiornamenti di
valore.

## Task

- **TASK-071** — Posizioni d'investimento e storico dei valori dichiarati
  (AC-01, AC-02, AC-05).
- **TASK-072** — Calcolo e vista del patrimonio per spazio (AC-03, AC-04, AC-06).

## Definition of Ready

READY. Il livello di dettaglio segue il default di Q-005; AC-06 è
verificabile solo dopo M4.
