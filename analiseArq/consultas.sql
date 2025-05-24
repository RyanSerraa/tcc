-- Principais mortes por estado
SELECT
  DL.state,
  DDC.description AS cause_of_death,
  COUNT(*) AS total_deaths
FROM
  FShootings FS
  JOIN DLocal DL ON DL.id = FS.idLocal
  JOIN DDeathCause DDC ON FS.idCauseDeath = DDC.id
WHERE
  DDC.description != 'UNKNOWN' AND DL.state != 'UNKNOWN'
GROUP BY
  DL.state, DDC.description
ORDER BY
  DL.state,
  total_deaths DESC;


  SELECT
  DL.city,
  DDC.description,
  COUNT(DDC.description) AS qtd_kill
FROM
  FShootings AS FS
  JOIN DLocal DL ON DL.id = FS.idLocal
  JOIN DDeathCause DDC ON FS.idCauseDeath = DDC.id
WHERE
  DDC.description != 'UNKNOWN'
GROUP BY
  DDC.description,
  DL.city
ORDER BY
  qtd_kill DESC
LIMIT
  10;


SELECT
  DL.state,
  DDC.description,
  COUNT(DDC.description) AS qtd_kill
FROM
  FShootings AS FS
  JOIN DLocal DL ON DL.id = FS.idLocal
  JOIN DDeathCause DDC ON FS.idCauseDeath = DDC.id
WHERE
  DDC.description != 'UNKNOWN'
GROUP BY
  DDC.description,
  DL.state
ORDER BY
  qtd_kill DESC
LIMIT
  10;

SELECT
  DP.gender,
  DP.race,
  DP.idGroupAge,
  DL.state,
  DL.city,
  DC.name AS crime_name,
  COUNT(*) AS prisons_qtd
FROM
  FArrest
  JOIN DPerson DP ON DP.id = FArrest.idPerson
  AND DP.idGroupAge = FArrest.idGroupAge
  JOIN DWeapon DW ON FArrest.idWeapon = DW.id
  JOIN DLocal DL ON FArrest.idLocal = DL.id
  JOIN DCrime DC ON FArrest.idCrime = DC.id
GROUP BY
  DP.gender,
  DP.race,
  DP.idGroupAge,
  DL.state,
  DL.city,
  DC.name,
  DP.id
ORDER BY
  prisons_qtd DESC
LIMIT
  10;