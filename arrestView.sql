CREATE VIEW VArrestDetails AS
SELECT
  f.year,
  f.month,
  f.day,
  
  c.name AS crime_name,
  
  d.name AS drug_name,
  
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
  l.lat,
  l.long
  
FROM FArrest f
JOIN DCrime c ON f.idCrime = c.id
JOIN DDrug d ON f.idDrug = d.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
