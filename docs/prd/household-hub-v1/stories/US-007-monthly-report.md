# US-007 — Report mensile per categoria

| Campo | Valore |
|---|---|
| Milestone | [M1 — Analisi mensile personale](../milestones/M1-personal-monthly-analysis.md) |
| Requisiti | [FR-030](../requirements.md#fr-030--report-mensile-per-categoria), [FR-031](../requirements.md#fr-031--confronto-con-i-mesi-precedenti), [FR-032](../requirements.md#fr-032--movimenti-da-categorizzare), NFR-004, NFR-005, NFR-006 |
| Regole | [DR-007](../domain-rules.md#dr-007--movimenti-tra-spazi-diversi), [DR-011](../domain-rules.md#dr-011--perimetro-dei-report), [DR-012](../domain-rules.md#dr-012--invariante-dei-totali), [DR-013](../domain-rules.md#dr-013--mese-di-competenza), [DR-014](../domain-rules.md#dr-014--rimborsi) |
| Dipende da | [US-005](US-005-manual-transactions.md), [US-006](US-006-transfers.md) |
| Questioni collegate | [Q-006](../open-questions-and-risks.md#q-006--trattamento-dei-rimborsi) (non bloccante) |
| DoR | READY |

## Storia

Come utente, voglio vedere ogni mese quanto ho speso per categoria e
sottocategoria, così da capire dove vanno i miei soldi.

## Esito atteso

Un report mensile affidabile, coerente con i movimenti e navigabile fino al
singolo movimento.

## Dataset di riferimento

Marzo, spazio personale:

| Movimento | Tipo | Importo | Categoria |
|---|---|---|---|
| Stipendio | Entrata | 2.000,00 | Lavoro |
| Cena | Uscita | 60,00 | Ristorazione › Cene |
| Cena | Uscita | 40,00 | Ristorazione › Cene |
| Aperitivo | Uscita | 15,00 | Ristorazione › Aperitivi |
| Bar | Uscita | 10,00 | Ristorazione |
| Rifornimento | Uscita | 70,00 | Trasporti › Carburante |
| Pedaggi | Uscita | 25,00 | Trasporti › Telepass |
| Pagamento POS | Uscita | 30,00 | — |
| Rimborso quota cena | Entrata | 20,00 | Ristorazione › Cene |
| Versamento su deposito | Giroconto | 500,00 | — |

## Criteri di accettazione

- **AC-US-007-01** — Con il dataset di riferimento il report di marzo
  mostra: entrate 2.000,00; uscite 230,00; saldo netto 1.770,00;
  Ristorazione 105,00 (Cene 80,00, Aperitivi 15,00, assegnati direttamente
  10,00); Trasporti 95,00 (Carburante 70,00, Telepass 25,00);
  Da categorizzare 30,00; il giroconto non è conteggiato.
- **AC-US-007-02** — Su ogni mese del dataset di verifica valgono tutte le
  invarianti di DR-012.
- **AC-US-007-03** — Selezionando una categoria o sottocategoria vedo
  esattamente i movimenti che ne compongono l'importo; la loro somma con
  segno coincide con l'importo mostrato.
- **AC-US-007-04** — Un mese senza movimenti mostra totali a zero, senza
  errori.
- **AC-US-007-05** — Per ogni categoria vedo la differenza rispetto al mese
  precedente e alla media dei tre mesi precedenti; la media considera solo
  i mesi dal primo mese con movimenti nello spazio e il confronto non è
  mostrato se non esiste alcun mese precedente con movimenti.
- **AC-US-007-06** — Categorizzando dal report un movimento "Da
  categorizzare", i totali si aggiornano subito e l'invariante resta
  valida.
- **AC-US-007-07** — I movimenti di un conto archiviato restano nei report
  dei mesi in cui sono avvenuti.
- **AC-US-007-08** — Con 10.000 movimenti annui nello spazio il report è
  visualizzato entro 2 secondi (NFR-006).
- **AC-US-007-09** — Su ogni mese del dataset di verifica la variazione del
  saldo di ogni conto è uguale alla somma con segno dei suoi movimenti,
  inclusi i giroconti e, da M4, i trasferimenti tra spazi (DR-012 punto 7).

## Verifica

Test di accettazione automatizzati sul dataset di riferimento e su un
dataset di verifica più ampio (giroconti, rimborsi, importi frazionari,
più mesi; trasferimenti tra spazi aggiunti in M4) riusato da [US-013](US-013-budgets.md) e
[US-019](US-019-household-reports-and-budgets.md); misura di prestazioni su
dataset di volume; verifica manuale della leggibilità su smartphone.

## Task

- **TASK-019** — Calcolo dei totali mensili per categoria e sottocategoria
  secondo DR-011 – DR-014 (AC-01, AC-02, AC-07 – AC-09).
- **TASK-020** — Vista del report con dettaglio dei movimenti (AC-03, AC-04).
- **TASK-021** — Confronto con il mese precedente e la media trimestrale (AC-05).
- **TASK-022** — Voce "Da categorizzare" con categorizzazione dal report (AC-06).
- **TASK-023** — Dataset di verifica dei report condiviso con le storie di
  budget e nucleo (AC-02).

## Definition of Ready

READY. Il trattamento dei rimborsi segue il default di Q-006; se cambiasse,
cambiano AC-01 e il dataset di verifica.
Perimetro MVP: AC-05 (confronto con i mesi precedenti, FR-031) è
rinviabile ([roadmap](../roadmap.md#perimetro-dellmvp)).
