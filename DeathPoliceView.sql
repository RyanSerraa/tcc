CREATE OR REPLACE VIEW VDeathPoliceDetails AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS date_of_death,

  COALESCE(dc.shortname, 'UNKNOWN') AS cause_of_death,
  d.name AS police_department,

  p.typePerson AS police_type, -- possible value POLICE
  
  l.state AS state, -- state of usa
  l.city AS city, -- citys of usa
  l.lat AS latitude,
  l.long AS longitude

FROM FDeathPolice f
JOIN DDeathCause dc ON f.idDeathCause = dc.id
JOIN DDept d ON f.idDept = d.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
