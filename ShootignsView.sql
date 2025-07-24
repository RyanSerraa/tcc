CREATE OR REPLACE VIEW VShootingDetails AS
SELECT
  f.year,
  f.month,
  f.day,

  COALESCE(dc.shortname) AS cause_death,
  COALESCE(w.shortname) AS weapon_name,

  f.threatLevel,
  f.flee,
  f.bodyCamera,

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

FROM FShootings f
JOIN DDeathCause dc ON f.idCauseDeath = dc.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
