CREATE OR REPLACE VIEW VCrime AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS data_crime,

  COALESCE(c.shortname, 'DESCONHECIDO') AS nome_crime,
  COALESCE(w.shortname, 'DESCONHECIDA') AS arma_usada, -- arma usada no crime

  -- Dados da pessoa criminosa
  p.genero AS sexo_criminoso, -- possíveis valores: 'MASCULINO', 'FEMININO', 'DESCONHECIDO', 'OUTROS'
  p.raca AS raca_criminoso,   -- possíveis valores: 'BRANCO', 'NEGRO', 'ASIÁTICO', 'DESCONHECIDO', 'HISPÂNICO', 'OUTROS'
  p.tipo_pessoa AS tipo_criminoso, -- possíveis valores: 'CRIMINOSO'
  p.faixa_inf || ' - ' || p.faixa_sup AS faixa_etaria_criminoso,

  l.state AS estado, -- estado dos EUA
  l.city AS cidade,  -- cidade dos EUA
  l.lat AS latitude,
  l.long AS longitude

FROM FCrime f
JOIN DCrime c ON f.idCrime = c.id
JOIN DArma w ON f.id_arma = w.id
JOIN DPessoa p ON f.idPerson = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;
