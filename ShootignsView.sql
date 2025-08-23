CREATE OR REPLACE VIEW VTiroteio AS
SELECT
  TO_DATE(
    f.year || '-' || LPAD(f.month::text, 2, '0') || '-' || LPAD(f.day::text, 2, '0'),
    'YYYY-MM-DD'
  ) AS data_tiro,

  COALESCE(dc.shortname, 'DESCONHECIDA') AS causa_morte,
  COALESCE(w.shortname, 'DESCONHECIDA') AS arma_usada, -- arma usada pela vítima

  f.status_de_ameaca AS status_ameaca, -- possíveis valores: 'ATAQUE', 'OUTROS', 'DESCONHECIDO'
  f.fuga AS status_fuga, -- possíveis valores: 'VEÍCULO', 'A PÉ', 'NÃO FUGIU', 'DESCONHECIDO'
  f.camera_corporal AS policial_com_camera,

  -- Dados da vítima
  p.genero AS sexo_vitima, -- possíveis valores: 'MASCULINO', 'FEMININO', 'DESCONHECIDO', 'OUTROS'
  p.raca AS raca_vitima,   -- possíveis valores: 'BRANCO', 'NEGRO', 'ASIÁTICO', 'HISPÂNICO', 'DESCONHECIDO', 'OUTROS'
  p.tipo_pessoa AS tipo_vitima, -- valores possíveis: 'POLICIAL', 'VÍTIMA', 'CRIMINOSO'
  p.faixa_inf || ' - ' || p.faixa_sup AS faixa_etaria_vitima,

  l.state AS estado, -- estado dos EUA
  l.city AS cidade,  -- cidade dos EUA
  l.lat AS latitude,
  l.long AS longitude

FROM FTiroteio f
JOIN DCausaMorte dc ON f.id_causa_morte = dc.id
JOIN DArma w ON f.id_arma = w.id
JOIN DPessoa p ON f.idPerson = p.id AND f.id_faixa_etaria = p.id_faixa_etaria
JOIN DLocalidade l ON f.id_localidade = l.id;
