CREATE OR REPLACE VIEW VArrestDetails AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS date_of_arrest,

  c.name AS crime_name,
  d.name AS drug_name, -- possibles values: 'CONTROLLED SUBSTANCE', 'CRACK COCAINE', 'ECSTACY', 'GHB', 'HEROIN', 'HYDROCODONE', 'KETAMINE', 'MARIJUANA', 'METHAMPHETAMINE', 'OXYCODONE', 'PARAPHERNALIA', 'POWDER COCAINE'
  COALESCE(w.shortname, 'UNKNOWN') AS weapon_used, -- weapon of arrest

  -- Dados da pessoa criminal
  p.gender AS criminal_gender, -- possibles values: 'MALE', 'FEMALE', 'UNKNOWN', 'OTHERS'
  p.race AS criminal_race, -- possibles values: 'WHITE', 'BLACK', 'ASIAN', 'UNKNOWN', 'HISPANIC', 'OTHERS'
  p.typePerson AS criminal_type, -- possibles values: 'CRIMINAL'
  p.rangeInf || ' - ' || p.rangeSup AS criminal_age_range,

  l.state AS state, -- state of usa
  l.city AS city, -- city of usa
  l.lat AS latitude,
  l.long AS longitude

FROM FArrest f
JOIN DCrime c ON f.idCrime = c.id
JOIN DDrug d ON f.idDrug = d.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
