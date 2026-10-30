# US-023 — Abbonamenti

| Campo | Valore |
|---|---|
| Milestone | [M6 — Abbonamenti e investimenti](../milestones/M6-subscriptions-and-investments.md) |
| Requisiti | [FR-037](../requirements.md#fr-037--abbonamenti), [FR-038](../requirements.md#fr-038--costo-e-rinnovi-degli-abbonamenti) |
| Regole | [DR-020](../domain-rules.md#dr-020--abbonamenti), [Matrice dei permessi](../domain-rules.md#matrice-dei-permessi-del-nucleo) |
| Dipende da | [US-003](US-003-personal-accounts.md), [US-004](US-004-categories.md) |
| Questioni collegate | [Q-009](../open-questions-and-risks.md#q-009--notifiche) (non bloccante) |
| DoR | READY |

## Storia

Come utente, voglio tenere sotto controllo i miei abbonamenti e quanto mi
costano in un anno, così da decidere quali mantenere.

## Esito atteso

Elenco degli abbonamenti con costo annuale effettivo, equivalente mensile
e rinnovi imminenti, senza effetti sui consuntivi.

## Criteri di accettazione

- **AC-US-023-01** — Registro un abbonamento con nome, importo, frequenza
  (mensile, trimestrale, semestrale, annuale), data del prossimo rinnovo,
  conto di addebito e categoria; compare nell'elenco degli attivi.
- **AC-US-023-02** — Con un abbonamento mensile da 12,99 € e uno annuale da
  60,00 €, il totale annuale effettivo è 215,88 € e il totale degli
  equivalenti mensili 17,99 €.
- **AC-US-023-03** — Vedo gli abbonamenti attivi con rinnovo nei 30 giorni
  successivi, ordinati per data.
- **AC-US-023-04** — Superata la data di rinnovo, la successiva è
  calcolata secondo la frequenza (es. trimestrale dal 15 gennaio al
  15 aprile).
- **AC-US-023-05** — Un abbonamento cessato non rientra nei totali né nei
  rinnovi e resta consultabile.
- **AC-US-023-06** — Registrare o modificare abbonamenti non cambia
  movimenti, report né consuntivi di budget.
- **AC-US-023-07** — Nel nucleo gli abbonamenti usano conti e categorie del
  nucleo e sono gestiti secondo la matrice dei permessi (richiede M4).
- **AC-US-023-08** — Un abbonamento trimestrale da 10,00 € ha costo
  annuale effettivo 40,00 € ed equivalente mensile 3,33 €. Con tre
  abbonamenti uguali il totale annuale effettivo è 120,00 €, somma esatta
  dei costi annuali, e il totale degli equivalenti mensili è 9,99 €, somma
  delle righe mostrate, presentato come valore indicativo. Il costo annuale
  non è mai ricavato dall'equivalente mensile (3,33 € × 12 = 39,96 €) né
  il totale mensile dal totale annuale (DR-020).

## Verifica

Test di accettazione automatizzati, inclusi i calcoli di AC-02 e AC-04 e il
confronto dei report prima e dopo AC-06.

## Task

- **TASK-069** — Gestione degli abbonamenti nello spazio personale e del
  nucleo (AC-01, AC-05 – AC-07).
- **TASK-070** — Costo annuale effettivo, equivalente mensile, rinnovi imminenti e avanzamento della
  data di rinnovo (AC-02 – AC-04, AC-08).

## Definition of Ready

READY. AC-07 è verificabile solo dopo M4.
