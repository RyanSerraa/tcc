CREATE VIEW VShootingDetails AS
SELECT
  f.year,
  f.month,
  f.day,
  dc."desc" AS cause_death,
  w.name AS weapon_name,
  f.threatLevel,
  f.flee,
  f.bodyCamera,
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
FROM FShootings f
JOIN DDeathCause dc ON f.idCauseDeath = dc.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
