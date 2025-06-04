  SELECT
  DP.gender,
  DP.race,
  DDC.description,
  (COUNT(DDC.description) * 100.0 / total.total_count) AS probability_gender_killed
FROM
  FFatalEncounters
  JOIN DPerson DP ON FFatalEncounters.idPerson = DP.id
  AND FFatalEncounters.idGroupAge = DP.idGroupAge
  JOIN DDeathCause DDC ON FFatalEncounters.idDeathCause = DDC.id
  JOIN (
    SELECT
      COUNT(*) AS total_count
    FROM
      FFatalEncounters
  ) AS total ON 1 = 1
GROUP BY
  DP.gender,
  DP.race,
  DDC.description,
  total.total_count
ORDER BY
  probability_gender_killed DESC;