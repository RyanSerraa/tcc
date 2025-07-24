CREATE OR REPLACE VIEW VDeathPoliceDetails AS
SELECT
  f.year,
  f.month,
  f.day,

  COALESCE(dc.shortname) AS death_cause,
  d.name AS dept_name,

  p.name AS person_name,
  p.sex,
  p.race,
  p.typePerson,
  p.rangeInf,
  p.rangesup,
  p.idGroupAge,

  l.state,
  l.city,
  l.lat AS latitude,
  l.long AS longitude,
  l.avgBlack,
  l.avgWhite,
  l.avgHispanic,
  l.avgAsian,
  l.standardDeviationBlack,
  l.standardDeviationWhite,
  l.standardDeviationHispanic,
  l.standardDeviationAsian

FROM FDeathPolice f
JOIN DDeathCause dc ON f.idDeathCause = dc.id
JOIN DDept d ON f.idDept = d.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
