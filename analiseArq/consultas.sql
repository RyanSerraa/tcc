SELECT d.state, top."name", top.qtd
FROM dlocal d
JOIN LATERAL (
	SELECT d2."name" , count(*) AS qtd
	FROM fdeathpolice f
	LEFT JOIN ddept d2 ON f.iddept = d2.id
	WHERE f.idlocal = d.id
	GROUP BY d2."name"
	ORDER BY qtd DESC
	LIMIT 1
) AS top ON TRUE
ORDER BY top.qtd DESC, d.state;
--------------------------------------------------------------------------
SELECT *
FROM (
    SELECT fdeathpolice."year", fdeathpolice."month", COUNT(*) AS qtd
    FROM fdeathpolice
    GROUP BY fdeathpolice."year", fdeathpolice."month"
    UNION ALL
    SELECT fdeathpolice."year", NULL AS "month", COUNT(*) AS qtd
    FROM fdeathpolice
    GROUP BY fdeathpolice."year"
    UNION ALL
    SELECT NULL AS "year", NULL AS "month", COUNT(*) AS qtd
    FROM fdeathpolice
) AS response
WHERE response."year" <= 2025 AND response."year" >= 1890
ORDER BY response."year" desc NULLS LAST, response."month" NULLS LAST;

------------------------------------------------------------------------------------
SELECT *
FROM (
    SELECT
        CASE
            WHEN fdeathpolice."year" BETWEEN 2000 AND 2025 THEN '2000-2025'
            WHEN fdeathpolice."year" BETWEEN 1970 AND 1999 THEN '1970-1999'
            WHEN fdeathpolice."year" BETWEEN 1940 AND 1969 THEN '1940-1969'
            WHEN fdeathpolice."year" BETWEEN 1910 AND 1939 THEN '1910-1939'
            WHEN fdeathpolice."year" BETWEEN 1890 AND 1909 THEN '1890-1909'
            ELSE 'Outros'
        END AS periodo,
        fdeathpolice."month",
        COUNT(*) AS qtd
    FROM fdeathpolice
    WHERE fdeathpolice."year" <= 2025
    GROUP BY periodo, fdeathpolice."month"

    UNION ALL

    SELECT
        CASE
            WHEN fdeathpolice."year" BETWEEN 2000 AND 2025 THEN '2000-2025'
            WHEN fdeathpolice."year" BETWEEN 1970 AND 1999 THEN '1970-1999'
            WHEN fdeathpolice."year" BETWEEN 1940 AND 1969 THEN '1940-1969'
            WHEN fdeathpolice."year" BETWEEN 1910 AND 1939 THEN '1910-1939'
            WHEN fdeathpolice."year" BETWEEN 1890 AND 1909 THEN '1890-1909'
            ELSE 'Outros'
        END AS periodo,
        NULL AS "month",
        COUNT(*) AS qtd
    FROM fdeathpolice
    WHERE fdeathpolice."year" <= 2025
    GROUP BY periodo
) AS response
WHERE periodo IN ('2000-2025', '1970-1999', '1940-1969', '1890-1909')
ORDER BY
    CASE
        WHEN response.periodo = '2000-2025' THEN 1
        WHEN response.periodo = '1970-1999' THEN 2
        WHEN response.periodo = '1940-1969' THEN 3
        WHEN response.periodo = '1890-1909' THEN 4
        ELSE 5
    END,
    response."month" NULLS LAST;

  --------------------------------------------------------------------------------

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
  qtd_kill DESC;