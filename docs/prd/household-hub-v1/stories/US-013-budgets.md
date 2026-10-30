# US-013 — Budget mensili

| Campo | Valore |
|---|---|
| Milestone | [M3 — Budget](../milestones/M3-budgets.md) |
| Requisiti | [FR-034](../requirements.md#fr-034--budget-mensili), [FR-035](../requirements.md#fr-035--confronto-previsto-e-consuntivo), [FR-036](../requirements.md#fr-036--riutilizzo-dei-budget), NFR-004, NFR-005 |
| Regole | [DR-019](../domain-rules.md#dr-019--budget), [DR-012](../domain-rules.md#dr-012--invariante-dei-totali), [DR-014](../domain-rules.md#dr-014--rimborsi) |
| Dipende da | [US-007](US-007-monthly-report.md) |
| Questioni collegate | [Q-006](../open-questions-and-risks.md#q-006--trattamento-dei-rimborsi), [Q-009](../open-questions-and-risks.md#q-009--notifiche) (non bloccanti) |
| DoR | READY |

## Storia

Come utente, voglio stabilire quanto spendere ogni mese per categoria e
vedere come sto andando, così da pianificare invece di limitarmi a
constatare.

## Esito atteso

Un budget mensile per categoria o sottocategoria con consuntivo coerente
con il report e senza doppi conteggi tra livelli.

## Criteri di accettazione

Esempio: i movimenti del dataset di riferimento di
[US-007](US-007-monthly-report.md) riportati ad aprile.

- **AC-US-013-01** — Definisco per aprile Ristorazione 200,00 €,
  Ristorazione › Cene 120,00 € e Trasporti › Carburante 100,00 €: il totale
  previsto del mese è 300,00 €.
- **AC-US-013-02** — Il confronto mostra Ristorazione: previsto 200,00,
  consuntivo 105,00, scostamento 95,00, utilizzo 52,5%; Cene: 120,00,
  80,00, 40,00, 66,7%; Carburante: 100,00, 70,00, 30,00, 70,0%.
- **AC-US-013-03** — Le spese non pianificate sono 55,00 € (Telepass 25,00
  e Da categorizzare 30,00); consuntivo coperto da budget più spese non
  pianificate è uguale al totale uscite del mese (230,00 €).
- **AC-US-013-04** — Il consuntivo di ogni voce coincide con l'importo
  della stessa categoria nel report di aprile, anche dopo aver modificato,
  aggiunto o eliminato movimenti.
- **AC-US-013-05** — Se la somma delle voci delle sottocategorie supera la
  voce della categoria (es. Cene 120,00 e Aperitivi 100,00 con Ristorazione
  200,00), il sistema lo segnala e consente comunque il salvataggio.
- **AC-US-013-06** — Per una voce con previsto 0,00 l'utilizzo non è
  calcolato e il consuntivo è mostrato.
- **AC-US-013-07** — Le voci si definiscono solo su categorie di spesa, con
  importi maggiori o uguali a zero e al massimo due decimali.
- **AC-US-013-08** — Copio il budget di aprile su maggio: se maggio non ha
  voci sono copiate tutte; altrimenti il sistema chiede conferma prima di
  sostituirle.
- **AC-US-013-09** — Eliminando una categoria con voci di budget e
  scegliendo una destinazione, le voci passano alla destinazione; se la
  destinazione ha già una voce nello stesso mese gli importi si sommano.
- **AC-US-013-10** — Con le sole voci Ristorazione › Cene 120,00 € e
  Trasporti 150,00 € (nessuna voce su Ristorazione), il totale previsto è
  270,00 € e il consuntivo coperto 175,00 € (Cene 80,00, Trasporti 95,00);
  le spese non pianificate sono 55,00 € (Aperitivi 15,00, Ristorazione
  assegnata direttamente 10,00, Da categorizzare 30,00) e consuntivo
  coperto più spese non pianificate è uguale al totale uscite (230,00 €).

## Verifica

Test di accettazione automatizzati sul dataset di verifica di US-007 esteso
con voci di budget su categorie e sottocategorie.

## Task

- **TASK-038** — Definizione delle voci di budget mensili (AC-01, AC-05, AC-07).
- **TASK-039** — Confronto previsto/consuntivo e spese non pianificate
  senza sovrapposizioni (AC-02 – AC-04, AC-06, AC-10).
- **TASK-040** — Copia del budget dal mese precedente (AC-08).
- **TASK-041** — Riassegnazione delle voci all'eliminazione di categorie (AC-09).

## Definition of Ready

READY.
