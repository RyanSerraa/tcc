CREATE OR REPLACE VIEW VCrime AS
SELECT
  MAKE_DATE(f.ano, f.mes, f.dia) AS data_crime,

  COALESCE(c.nome_abreviado, 'DESCONHECIDO') AS nome_crime,
  COALESCE(a.nome_abreviado, 'DESCONHECIDA') AS arma_usada, -- arma usada no crime

  -- Dados da pessoa criminosa
  p.genero AS sexo_criminoso, -- possíveis valores: 'MASCULINO', 'FEMININO', 'DESCONHECIDO', 'OUTROS'
  p.raca AS raca_criminoso,   -- possíveis valores: 'BRANCO', 'NEGRO', 'ASIÁTICO', 'DESCONHECIDO', 'HISPÂNICO', 'OUTROS'
  p.tipo_pessoa AS tipo_criminoso, -- possíveis valores: 'CRIMINOSO'
  p.faixa_inf || ' - ' || p.faixa_sup AS faixa_etaria_criminoso,

  l.estado AS estado, -- estado dos EUA
  l.cidade AS cidade,  -- cidade dos EUA
  l.latitude AS latitude,
  l.longitude AS longitude

FROM FCrime f
JOIN DCrime c ON f.id_crime = c.id
JOIN DArma a ON f.id_arma = a.id
JOIN DPessoa p ON f.id_pessoa = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;
