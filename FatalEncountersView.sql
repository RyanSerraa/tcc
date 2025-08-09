CREATE OR REPLACE VIEW VFatalEncountersDetails AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS date_of_death,

  COALESCE(dc.shortname, 'UNKNOWN') AS cause_of_death,
  COALESCE(w.shortname, 'UNKNOWN') AS weapon_used, --victim weapon used
  d.name AS police_department,

  f.threatLevel AS threat_status, -- possibles values: 'ATTACK', 'OTHER', 'UNKNOWN'
  f.flee AS flee_status, -- possibles values 'VECHILE', 'FOOT', 'UNKNOWN', 'NOT FLEEING'
  f.bodyCamera AS is_police_wearing_camera,

  -- Dados da vítima (pessoa)
  p.gender AS victim_gender, -- possibles values: 'MALE', 'FEMALE', 'UNKNOWN', 'OTHERS'
  p.race AS victim_race, -- 'WHITE', 'BLACK', 'ASIAN', 'UNKNOWN', 'HISPANIC', 'OTHERS'
  p.typePerson AS victim_type, -- 'POLICE', 'VICTIM', 'CRIMINAL'
  p.rangeInf || ' - ' || p.rangeSup AS victim_age_range,

  l.state AS state, -- state of usa
  l.city AS city, -- citys of usa
  l.lat AS latitude, 
  l.long AS longitude

FROM FFatalEncounters f
JOIN DDeathCause dc ON f.idDeathCause = dc.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DDept d ON f.idDept = d.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
