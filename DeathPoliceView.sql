CREATE OR REPLACE VIEW VMortePolicial AS
SELECT
  MAKE_DATE(f.ano, f.mes, f.dia) AS data_crime,

  COALESCE(c.nome_abreviado, 'DESCONHECIDO') AS causa_morte,

   p.tipo_pessoa AS tipo_policia, -- possíveis valores: 'POLICIAL'
  p.faixa_inf || ' - ' || p.faixa_sup AS faixa_etaria_criminoso,

  l.estado AS estado, -- estado dos EUA
  l.cidade AS cidade,  -- cidade dos EUA
  l.latitude AS latitude,
  l.longitude AS longitude

FROM fmortepolicial f
JOIN dcausamorte c ON f.id_causa_morte = c.id
JOIN ddepartamento d ON f.id_departamento = d.id
JOIN DPessoa p ON f.id_pessoa = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;
