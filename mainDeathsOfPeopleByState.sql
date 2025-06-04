-- main Deaths Of People By State

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