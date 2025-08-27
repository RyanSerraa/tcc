CREATE OR REPLACE VIEW VMortePolicial AS
SELECT
  MAKE_DATE(f.ano, f.mes, f.dia) AS data_morte,

  COALESCE(c.nome_abreviado, 'DESCONHECIDO') AS causa_morte,

   p.tipo_pessoa AS tipo_policia, -- possíveis valores: 'POLICIAL'
   d.nome as departamento_policial,

  l.estado AS estado, -- estado dos EUA
  l.cidade AS cidade,  -- cidade dos EUA
  l.latitude AS latitude,
  l.longitude AS longitude

FROM fmortepolicial f
JOIN dcausamorte c ON f.id_causa_morte = c.id
JOIN ddepartamento d ON f.id_departamento = d.id
JOIN DPessoa p ON f.id_pessoa = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;
