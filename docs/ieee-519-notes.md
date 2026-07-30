# Notes for an IEEE 519 Assessment

The active edition located during the audit is IEEE 519-2022, published on
August 5, 2022, and superseding IEEE 519-2014. Its official page describes
steady-state voltage and current distortion limits at the point of common
coupling (PCC):

- [IEEE Standards Association — IEEE 519-2022](https://standards.ieee.org/ieee/519/10677/)

## Difference between the prototype and a standards assessment

The prototype uses constant THD values and does not formally identify the PCC.
A traceable assessment should record at least:

1. exact standards edition and assessment date;
2. PCC location;
3. nominal voltage level;
4. measured voltage THD and individual voltage harmonics at the PCC;
5. current TDD and individual current harmonics;
6. maximum demand current `IL`;
7. short-circuit information and `Isc/IL` where applicable;
8. statistical window and observation period;
9. applicable limits selected from an authorized copy;
10. margin, compliance result, and measurement uncertainty.

## Repository design

The code does not embed numeric standards tables. `ieee519.py` receives a
measured value and a limit already selected by a professional with access to
the applicable edition. This avoids:

- presenting a context-dependent limit as universal;
- confusing current THD with TDD;
- copying protected standards content;
- claiming compliance without the required information.

Limit assessment and loss calculation remain separate. Being inside or
outside a distortion limit does not automatically determine lost kW.
