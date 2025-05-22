-- QUAIS FORAM AS PESSOAS que estão dentro das 10 maiores causa de morte e estão armadas
SELECT DP.name,DP.gender,DP.race,DP.idGroupAge, DW.name,DDC.description, count(DDC.description) as qtd_kill FROM FShootings AS FS
JOIN DPerson DP on FS.idPerson = DP.id and FS.idGroupAge = DP.idGroupAge
JOIN DWeapon DW on FS.idWeapon = DW.id
JOIN DDeathCause DDC on FS.idCauseDeath = DDC.id
WHERE DDC.description != 'UNKNOWN' AND DW.name != 'UNKNOWN WEAPON'
GROUP BY DP.name, DP.gender, DP.race, DP.idGroupAge, DW.name, DDC.description
ORDER BY qtd_kill DESC
LIMIT 10;

-- Quais são os locais com maior inumero de crimes e quais foram as armas utilizadas

SELECT DP.name,DP.race,DP.gender ,DW.name as weapon_name, DL.state, count(DL.state) as qtd_state FROM FCrime AS FC
join DPerson DP on DP.id = FC.idPerson and DP.idGroupAge = FC.idGroupAge
JOIN DLocal DL on DL.id = FC.idLocal
JOIN DWeapon DW on FC.idWeapon = DW.id
where DW.name != 'UNKNOWN' and dl.state != 'UNKNOWN'
GROUP BY DP.race, DP.gender, DW.name, DL.state, DP.name
ORDER BY  qtd_state DESC
LIMIT 10;


SELECT DP.gender, DP.race, DP.idGroupAge, DL.state, DL.city, DC.name as crime_name, COUNT(*) AS prisons_qtd   FROM FArrest
    JOIN DPerson DP on DP.id = FArrest.idPerson and DP.idGroupAge = FArrest.idGroupAge
    JOIN DWeapon DW on FArrest.idWeapon = DW.id
    JOIN DLocal DL on FArrest.idLocal = DL.id
    JOIN DCrime DC on FArrest.idCrime = DC.id
    GROUP BY DP.gender, DP.race, DP.idGroupAge,DL.state, DL.city, DC.name, DP.id
    ORDER BY prisons_qtd desc
    LIMIT 10;


SELECT DP.name,DP.race,DP.gender ,DW.name as weapon_name, DL.state, count(DP.id) as qtd_persons FROM FCrime AS FC
join DPerson DP on DP.id = FC.idPerson and DP.idGroupAge = FC.idGroupAge
JOIN DLocal DL on DL.id = FC.idLocal
JOIN DWeapon DW on FC.idWeapon = DW.id
where DW.name != 'UNKNOWN' and dl.state != 'UNKNOWN'
GROUP BY DP.race, DP.gender, DW.name, DL.state, DP.name
ORDER BY  qtd_persons DESC
LIMIT 10;