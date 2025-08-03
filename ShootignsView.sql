CREATE OR REPLACE VIEW VShootingDetails AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS date_of_shooting,

  COALESCE(dc.shortname, 'UNKNOWN') AS cause_of_death,
  COALESCE(w.shortname, 'UNKNOWN') AS weapon_used,

  f.threatLevel AS threat_level,
  f.flee AS flee_status,
  f.bodyCamera AS is_police_wearing_camera,

  -- Dados da vítima (pessoa)
  p.name AS victim_name,
  p.gender AS victim_gender,
  p.race AS victim_race,
  p.typePerson AS victim_type,
  p.rangeInf || ' - ' || p.rangeSup AS victim_age_range,
  p.idGroupAge AS victim_age_group_id,

  l.state AS state,
  l.city AS city,
  l.lat AS latitude,
  l.long AS longitude

FROM FShootings f
JOIN DDeathCause dc ON f.idCauseDeath = dc.id
JOIN DWeapon w ON f.idWeapon = w.id
JOIN DPerson p ON f.idPerson = p.id AND f.idGroupAge = p.idGroupAge
JOIN DLocal l ON f.idLocal = l.id;
