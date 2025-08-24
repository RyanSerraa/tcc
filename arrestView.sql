CREATE OR REPLACE VIEW VPrisao AS
SELECT
  MAKE_DATE(f.ano, f.mes, f.dia) AS data_crime,
  
  d.nome AS droga, -- possíveis valores: 'SUBSTÂNCIA CONTROLADA', 'CRACK', 'ECSTASY', 'GHB', 'HEROINA', 'HIDROCODONA', 'KETAMINA', 'MACONHA', 'METANFETAMINA', 'OXICODONA', 'PARAFERNÁLIA', 'COCAÍNA'
  COALESCE(c.nome_abreviado, 'DESCONHECIDO') AS nome_crime,
  COALESCE(a.nome_abreviado, 'DESCONHECIDA') AS arma_usada, -- arma usada no crime

  -- Dados da pessoa presa
  p.genero AS sexo_criminoso, -- possíveis valores: 'MASCULINO', 'FEMININO', 'DESCONHECIDO', 'OUTROS'
  p.raca AS raca_criminoso,   -- possíveis valores: 'BRANCO', 'NEGRO', 'ASIÁTICO', 'DESCONHECIDO', 'HISPÂNICO', 'OUTROS'
  p.tipo_pessoa AS tipo_criminoso, -- possíveis valores: 'CRIMINOSO'
  p.faixa_inf || ' - ' || p.faixa_sup AS faixa_etaria_criminoso,

  l.estado AS estado, -- estado dos EUA
  l.cidade AS cidade,  -- cidade dos EUA
  l.latitude AS latitude,
  l.longitude AS longitude

FROM fprisao f
JOIN DCrime c ON f.id_crime = c.id
JOIN DDroga d ON f.id_droga = d.id
JOIN DArma a ON f.id_arma = a.id
JOIN DPessoa p ON f.id_pessoa = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;
