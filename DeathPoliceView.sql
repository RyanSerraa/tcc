CREATE OR REPLACE VIEW VMortePolicial AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS data_morte,

  COALESCE(dc.shortname, 'DESCONHECIDA') AS causa_morte,
  d.name AS departamento_policia,

  p.tipo_pessoa AS tipo_policia, -- valor possível: 'POLICIAL'
  
  l.state AS estado, -- estado dos EUA
  l.city AS cidade,  -- cidade dos EUA
  l.lat AS latitude,
  l.long AS longitude

FROM FMortePolicial f
JOIN DCausaMorte dc ON f.id_causa_morte = dc.id
JOIN DDepartamento d ON f.id_departamento = d.id
JOIN DPessoa p ON f.idPerson = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;
