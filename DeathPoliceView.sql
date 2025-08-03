CREATE OR REPLACE VIEW VDeathPoliceDetails AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS date_of_death,

  COALESCE(dc.shortname, 'UNKNOWN') AS cause_of_death,
  d.name AS police_department,

  p.name AS police_name,
  p.gender AS police_gender,
  p.race AS police_race,
  p.typePerson AS police_type,
  p.rangeInf || ' - ' || p.rangeSup AS police_age_range,
  p.idGroupAge AS police_age_group_id,

  l.state AS state,
  l.city AS city,
  l.lat AS latitude,
  l.long AS longitude

FROM FDeathPolice f
JOIN DDeathCause dc ON f.idDeathCause = dc.id
JOIN DDept d ON f.idDept = d.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
