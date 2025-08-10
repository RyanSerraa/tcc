CREATE OR REPLACE VIEW VCrimeDetails AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS date_of_crime,

  COALESCE(c.shortname, 'UNKNOWN') AS crime_name,
  COALESCE(w.shortname, 'UNKNOWN') AS weapon_used, -- criminal weapon used

  -- Dados da pessoa criminal
  p.gender AS criminal_gender, -- possibles values: 'MALE', 'FEMALE', 'UNKNOWN', 'OTHERS'
  p.race AS criminal_race, -- possibles values: 'WHITE', 'BLACK', 'ASIAN', 'UNKNOWN', 'HISPANIC', 'OTHERS'
  p.typePerson AS criminal_type, -- possibles values: 'CRIMINAL'
  p.rangeInf || ' - ' || p.rangeSup AS criminal_age_range,

  l.state AS state, -- state of usa
  l.city AS city, -- city of usa
  l.lat AS latitude,
  l.long AS longitude

FROM FCrime f
JOIN DCrime c ON f.idCrime = c.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
