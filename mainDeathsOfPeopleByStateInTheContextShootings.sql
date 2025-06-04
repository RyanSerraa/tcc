-- Top deaths Of People In the Context Shootings
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