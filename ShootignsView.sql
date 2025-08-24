CREATE OR REPLACE VIEW VTiroteio AS
SELECT
  MAKE_DATE(f.ano, f.mes, f.dia) AS data_crime,

  COALESCE(c.nome_abreviado, 'DESCONHECIDO') AS causa_morte,
  COALESCE(a.nome_abreviado, 'DESCONHECIDA') AS arma_usada, -- arma usada no crime

  f.status_de_ameaca AS status_ameaca, -- possíveis valores: 'ATAQUE', 'OUTROS', 'DESCONHECIDO'
  f.fuga AS status_fuga, -- possíveis valores: 'VEÍCULO', 'A PÉ', 'NÃO FUGIU', 'DESCONHECIDO'
  f.camera_corporal AS policial_com_camera,

  -- Dados da pessoa presa
  p.genero AS sexo_vitima, -- possíveis valores: 'MASCULINO', 'FEMININO', 'DESCONHECIDO', 'OUTROS'
  p.raca AS raca_vitima,   -- possíveis valores: 'BRANCO', 'NEGRO', 'ASIÁTICO', 'DESCONHECIDO', 'HISPÂNICO', 'OUTROS'
  p.tipo_pessoa AS tipo_vitima, -- possíveis valores: 'VITIMA'
  p.faixa_inf || ' - ' || p.faixa_sup AS faixa_etaria_criminoso,

  l.estado AS estado, -- estado dos EUA
  l.cidade AS cidade,  -- cidade dos EUA
  l.latitude AS latitude,
  l.longitude AS longitude

FROM FTiroteio f
JOIN DArma a ON f.id_arma = a.id
JOIN dcausamorte c ON f.id_causa_morte = c.id
JOIN DPessoa p ON f.id_pessoa = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;

