CREATE OR REPLACE VIEW VCrimeDetails AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS date_of_crime,

  COALESCE(c.shortname, 'UNKNOWN') AS crime_name,
  COALESCE(w.shortname, 'UNKNOWN') AS weapon_used,

  -- Dados da pessoa criminal
  p.name AS criminal_name,
  p.gender AS criminal_gender,
  p.race AS criminal_race,
  p.typePerson AS criminal_type,
  p.rangeInf || ' - ' || p.rangeSup AS criminal_age_range,
  p.idGroupAge AS criminal_age_group_id,

  l.state AS state,
  l.city AS city,
  l.lat AS latitude,
  l.long AS longitude

FROM FCrime f
JOIN DCrime c ON f.idCrime = c.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
