SELECT DL.state, DDC.description, (COUNT(DDC.description)*1.0/total_count) AS probability_police_killed FROM  FDeathPolice
    JOIN DLocal DL on FDeathPolice.idLocal = DL.id
    JOIN DDeathCause DDC on FDeathPolice.idDeathCause = DDC.id
    JOIN (
    SELECT COUNT(*) AS total_count
    FROM FDeathPolice
) AS total ON 1=1
GROUP BY DL.state, DDC.description, total.total_count
ORDER BY  probability_police_killed DESC,DL.state, description;
