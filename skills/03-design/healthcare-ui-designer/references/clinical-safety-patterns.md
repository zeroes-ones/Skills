# Clinical Safety Patterns

In a clinical interface, a misread value is a patient-safety event, not a UX defect.

## The rules

| Concern | Requirement |
|---|---|
| Units | Always displayed; never assumed. mg vs mcg is a documented cause of harm |
| Decimals | Trailing zeros removed for dosing (per ISMP guidance); explicit leading zero before a decimal point |
| Look-alike/sound-alike | High-alert drugs and similar names visually differentiated |
| Alerts | Interrupt only for real risk; alert fatigue is itself a safety hazard |
| Confirmation | Destructive or irreversible actions require explicit confirmation showing what will change |
| Provenance | Every value shows who recorded it and when |

## Failure modes

- **Unit-less values.** The number is displayed and the unit is implied.
- **Alert overload.** So many warnings fire that all are dismissed, including the one that mattered.
- **Ambiguous abbreviations.** `U` read as `0` or `4`; `QD` read as `QID`.
- **Silent overwrite.** A new value replaces an old one with no audit trail.
- **Default-accept dialogs.** The safe action is not the default, and the user is trained to click through.
- **Colour-only severity.** A critical result signalled by red text alone.
