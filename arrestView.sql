CREATE OR REPLACE VIEW VPrisao AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS data_prisao,

  c.name AS crime,  
  d.name AS droga, -- possíveis valores: 'SUBSTÂNCIA CONTROLADA', 'CRACK', 'ECSTASY', 'GHB', 'HEROINA', 'HIDROCODONA', 'KETAMINA', 'MACONHA', 'METANFETAMINA', 'OXICODONA', 'PARAFERNÁLIA', 'COCAÍNA'
  COALESCE(w.shortname, 'DESCONHECIDA') AS arma_usada, -- arma da prisão

  -- Dados da pessoa presa
  p.genero AS sexo_criminoso, -- possíveis valores: 'MASCULINO', 'FEMININO', 'DESCONHECIDO', 'OUTROS'
  p.raca AS raca_criminoso,   -- possíveis valores: 'BRANCO', 'NEGRO', 'ASIÁTICO', 'DESCONHECIDO', 'HISPÂNICO', 'OUTROS'
  p.tipo_pessoa AS tipo_criminoso, -- possíveis valores: 'CRIMINOSO'
  p.faixa_inf || ' - ' || p.faixa_sup AS faixa_etaria_criminoso,

  l.state AS estado, -- estado dos EUA
  l.city AS cidade,  -- cidade dos EUA
  l.lat AS latitude,
  l.long AS longitude

FROM FPrisao f
JOIN DCrime c ON f.idCrime = c.id
JOIN DDroga d ON f.id_droga = d.id
JOIN DArma w ON f.id_arma = w.id
JOIN DPessoa p ON f.idPerson = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;
