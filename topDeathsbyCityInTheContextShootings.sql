-- top 10 Deaths By City In The Context Shootings

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