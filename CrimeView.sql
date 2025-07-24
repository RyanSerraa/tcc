CREATE OR REPLACE VIEW VCrimeDetails AS
SELECT
  f.year,
  f.month,
  f.day,

  COALESCE(c.shortname) AS crime_name,
  COALESCE(w.shortname) AS weapon_name,

  p.name AS person_name,
  p.sex,
  p.race,
  p.typePerson,
  p.rangeInf,
  p.rangeSup,
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

FROM FCrime f
JOIN DCrime c ON f.idCrime = c.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
