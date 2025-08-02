CREATE OR REPLACE VIEW VFatalEncountersDetails AS
SELECT
  f.year,
  f.month,
  f.day,

  COALESCE(dc.shortname) AS death_cause,
  COALESCE(w.shortname) AS weapon_name,
  d.name AS police_department_name,

  f.threatLevel,
  f.flee,
  f.bodyCamera as is_police_wearing_camera,

  p.name AS person_name,
  p.gender as gender,
  p.race,
  p.typePerson,
  -- p.rangeInf, # não serve -- da para criar uma outra coluna com o concat 
  -- p.rangesup,
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

FROM FFatalEncounters f
JOIN DDeathCause dc ON f.idDeathCause = dc.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DDept d ON f.idDept = d.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
