CREATE VIEW VDeathPoliceDetails AS
SELECT
  f.year,
  f.month,
  f.day,
  dc."desc" AS death_cause,
  d.name AS dept_name,
  p.name AS person_name,
  p.sex,
  p.race,
  p.typePerson,
  p.rangeInf,
  p.rangeSup,
  l.state,
  l.city,
  l.lat,
  l.long
FROM FDeathPolice f
JOIN DDeathCause dc ON f.idDeathCause = dc.id
JOIN DDept d ON f.idDept = d.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
