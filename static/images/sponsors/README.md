# Sponsor logos

## MICIU / AEI

Official downloads (horizontal, colour; the required combination differs per
grant type):
https://www.aei.gob.es/ayudas-concedidas/comunicacion-publicidad-ayudas-concedidas

Governing rules: *Guía recopilatoria de obligaciones de comunicación y
publicidad de las ayudas a la I+D+i concedidas por la Agencia Estatal de
Investigación* (AEI, 2026-02-05, v09). Annex 1 lists which logo combination
applies to each grant type and call year.

| File | Use for | Status |
|---|---|---|
| `MICIU-AEI.jpg` | Grants funded from the national budget only | Not yet displayed |
| `MICIU-Cofinanciado-AEI.jpg` | Grants co-financed by ERDF / the European Union | Unused |

Originals are ~12000x3000 px and 2.7-3.4 MB. Both files here were scaled
proportionally to 600 px wide (q85, ~17 KB), which is enough for the 288 px
display width at 2x. Proportional scaling is permitted; cropping, recolouring
and rearranging the logos are not.

## Pending: adding PID2025 to the site

Project PID2025-173011NA-I00 (CSIC / Centro de Fisica de Materiales, 3 years,
0 predoctoral contracts). The provisional resolution of 2026-07-15 shows no
ERDF and no ESF+ co-financing, so `MICIU-AEI.jpg` is the correct file. The
project cannot start before 1 September 2026.

Once the final *resolucion de concesion* arrives:

1. Confirm the grant reference, and search the document for "FEDER" once more
   to verify there is still no co-financing.
2. Add `MICIU-AEI.jpg` to the `sponsor-logo-grid` in `layouts/index.html`.
3. Add the grant reference at the same time - the rules require the reference
   to always appear together with the MICIU and AEI logos:
   `Project PID2025-173011NA-I00 funded by MICIU/AEI/10.13039/501100011033`
   Do not translate the MICIU and AEI names or the text inside the logos, even
   on an English page.
4. The rules ask for this notice on every page of the site, visible on the
   home page without scrolling. A footer line is the practical way to cover
   every page; check with the CSIC research management office how strictly
   they interpret the home-page requirement.

Until step 2 and 3 are done together, do not display the logos on their own:
a logo without its grant reference is worse than no logo at all.
