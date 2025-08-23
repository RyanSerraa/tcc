ALTER TYPE race_enum RENAME TO raca_enum;
ALTER TYPE type_enum RENAME TO tipo_de_pessoa_enum;
ALTER TYPE threat_enum RENAME TO ameaca_enum;
ALTER TYPE flee_enum RENAME TO fuga_enum;
ALTER TYPE gender_enum RENAME TO genero_enum;

-- Renomeando tabelas de Dimensão
ALTER TABLE DLocal RENAME TO DLocalidade;
ALTER TABLE DPerson RENAME TO DPessoa;
ALTER TABLE DCrime RENAME TO DCrime;
ALTER TABLE DDrug RENAME TO DDroga;
ALTER TABLE DDeathCause RENAME TO DCausaMorte;
ALTER TABLE DDept RENAME TO DDepartamento;
ALTER TABLE DWeapon RENAME TO DArma;

-- Renomeando tabelas de Fato
ALTER TABLE FDeathPolice RENAME TO FMortePolicial;
ALTER TABLE FShootings RENAME TO FTiros;
ALTER TABLE FFatalEncounters RENAME TO FConfrontosFatais;
ALTER TABLE FArrest RENAME TO FPrisao;
ALTER TABLE FCrime RENAME TO FCrime;

-- Renomeando colunas de DLocalidade
ALTER TABLE DLocalidade RENAME COLUMN avgBlack TO media_negros;
ALTER TABLE DLocalidade RENAME COLUMN avgWhite TO media_brancos;
ALTER TABLE DLocalidade RENAME COLUMN avgHispanic TO media_hispanicos;
ALTER TABLE DLocalidade RENAME COLUMN avgAsian TO media_asiaticos;
ALTER TABLE DLocalidade RENAME COLUMN standardDeviationBlack TO desvio_padrao_negros;
ALTER TABLE DLocalidade RENAME COLUMN standardDeviationWhite TO desvio_padrao_brancos;
ALTER TABLE DLocalidade RENAME COLUMN standardDeviationHispanic TO desvio_padrao_hispanicos;
ALTER TABLE DLocalidade RENAME COLUMN standardDeviationAsian TO desvio_padrao_asiaticos;

-- Renomeando colunas de DPessoa
ALTER TABLE DPessoa RENAME COLUMN idGroupAge TO id_faixa_etaria;
ALTER TABLE DPessoa RENAME COLUMN typePerson TO tipo_pessoa;
ALTER TABLE DPessoa RENAME COLUMN rangeInf TO faixa_inf;
ALTER TABLE DPessoa RENAME COLUMN rangeSup TO faixa_sup;

-- Renomeando colunas em FMortePolicial
ALTER TABLE FMortePolicial RENAME COLUMN idGroupAge TO id_faixa_etaria;
ALTER TABLE FMortePolicial RENAME COLUMN idDept TO id_departamento;
ALTER TABLE FMortePolicial RENAME COLUMN idDeathCause TO id_causa_morte;
ALTER TABLE FMortePolicial RENAME COLUMN idLocal TO id_localidade;

-- Renomeando colunas em FTiros
ALTER TABLE FTiros RENAME COLUMN idGroupAge TO id_faixa_etaria;
ALTER TABLE FTiros RENAME COLUMN idLocal TO id_localidade;
ALTER TABLE FTiros RENAME COLUMN idCauseDeath TO id_causa_morte;
ALTER TABLE FTiros RENAME COLUMN idWeapon TO id_arma;
ALTER TABLE FTiros RENAME COLUMN threatLevel TO status_de_ameaca;
ALTER TABLE FTiros RENAME COLUMN bodyCamera TO camera_corporal;

-- Renomeando colunas em FConfrontosFatais
ALTER TABLE FConfrontosFatais RENAME COLUMN idGroupAge TO id_faixa_etaria;
ALTER TABLE FConfrontosFatais RENAME COLUMN idDept TO id_departamento;
ALTER TABLE FConfrontosFatais RENAME COLUMN idLocal TO id_localidade;
ALTER TABLE FConfrontosFatais RENAME COLUMN idDeathCause TO id_causa_morte;
ALTER TABLE FConfrontosFatais RENAME COLUMN idWeapon TO id_arma;
ALTER TABLE FConfrontosFatais RENAME COLUMN threatLevel TO status_de_ameaca;
ALTER TABLE FConfrontosFatais RENAME COLUMN bodyCamera TO camera_corporal;

-- Renomeando colunas em FPrisao
ALTER TABLE FPrisao RENAME COLUMN idGroupAge TO id_faixa_etaria;
ALTER TABLE FPrisao RENAME COLUMN idLocal TO id_localidade;
ALTER TABLE FPrisao RENAME COLUMN idWeapon TO id_arma;
ALTER TABLE FPrisao RENAME COLUMN idDrug TO id_droga;

-- Renomeando colunas em FCrime
ALTER TABLE FCrime RENAME COLUMN idGroupAge TO id_faixa_etaria;
ALTER TABLE FCrime RENAME COLUMN idLocal TO id_localidade;
ALTER TABLE FCrime RENAME COLUMN idWeapon TO id_arma;


--- Renomeiando os values do enum 
-- ENUM raça
ALTER TYPE raca_enum RENAME VALUE 'WHITE' TO 'BRANCO';
ALTER TYPE raca_enum RENAME VALUE 'BLACK' TO 'NEGRO';
ALTER TYPE raca_enum RENAME VALUE 'ASIAN' TO 'ASIÁTICO';
ALTER TYPE raca_enum RENAME VALUE 'UNKNOWN' TO 'DESCONHECIDO';
ALTER TYPE raca_enum RENAME VALUE 'HISPANIC' TO 'HISPÂNICO';
ALTER TYPE raca_enum RENAME VALUE 'OTHERS' TO 'OUTROS';

-- ENUM tipo de pessoa
ALTER TYPE tipo_enum RENAME VALUE 'POLICE' TO 'POLICIAL';
ALTER TYPE tipo_enum RENAME VALUE 'VICTIM' TO 'VÍTIMA';
ALTER TYPE tipo_enum RENAME VALUE 'CRIMINAL' TO 'CRIMINOSO';

-- ENUM nível de ameaça
ALTER TYPE ameaca_enum RENAME VALUE 'ATTACK' TO 'ATAQUE';
ALTER TYPE ameaca_enum RENAME VALUE 'OTHER' TO 'OUTRO';
ALTER TYPE ameaca_enum RENAME VALUE 'UNKNOWN' TO 'DESCONHECIDO';

-- ENUM fuga
ALTER TYPE fuga_enum RENAME VALUE 'VECHILE' TO 'VEÍCULO'; 
ALTER TYPE fuga_enum RENAME VALUE 'FOOT' TO 'A PÉ';
ALTER TYPE fuga_enum RENAME VALUE 'UNKNOWN' TO 'DESCONHECIDO';
ALTER TYPE fuga_enum RENAME VALUE 'NOT FLEEING' TO 'NÃO FUGIU';

-- ENUM gênero
ALTER TYPE genero_enum RENAME VALUE 'MALE' TO 'MASCULINO';
ALTER TYPE genero_enum RENAME VALUE 'FEMALE' TO 'FEMININO';
ALTER TYPE genero_enum RENAME VALUE 'UNKNOWN' TO 'DESCONHECIDO';
ALTER TYPE genero_enum RENAME VALUE 'OTHERS' TO 'OUTROS';

-- Atualizando valores em DArma
UPDATE DArma SET nome = 'AR-CONDICIONADO' WHERE nome = 'AIR CONDITIONER';
UPDATE DArma SET nome = 'PISTOLA DE AR' WHERE nome = 'AIR PISTOL';
UPDATE DArma SET nome = 'ANIMAL' WHERE nome = 'ANIMAL';
UPDATE DArma SET nome = 'MACHADO' WHERE nome IN ('AX', 'AXE');
UPDATE DArma SET nome = 'BANQUETA' WHERE nome = 'BARSTOOL';
UPDATE DArma SET nome = 'BASTÃO DE BASEBOL' WHERE nome = 'BASEBALL BAT';
UPDATE DArma SET nome = 'BASTÃO' WHERE nome = 'BAT' OR nome = 'STICK';
UPDATE DArma SET nome = 'BAYONETA' WHERE nome = 'BAYONET';
UPDATE DArma SET nome = 'ESPANCAMENTO' WHERE nome = 'BEAT';
UPDATE DArma SET nome = 'CINTO' WHERE nome = 'BELT';
UPDATE DArma SET nome = 'CACETE' WHERE nome = 'BLACKJACK';
UPDATE DArma SET nome = 'LÂMINA' WHERE nome = 'BLADE';
UPDATE DArma SET nome = 'ARMA CONTUNDENTE' WHERE nome = 'BLUNT WEAPON';
UPDATE DArma SET nome = 'TÁBUA' WHERE nome = 'BOARD';
UPDATE DArma SET nome = 'GARRAFA' WHERE nome = 'BOTTLE';
UPDATE DArma SET nome = 'ESTILETE' WHERE nome = 'BOX CUTTER';
UPDATE DArma SET nome = 'SOCO-INGLÊS' WHERE nome = 'BRASS KNUCKLES';
UPDATE DArma SET nome = 'TIJOLO' WHERE nome = 'BRICK';
UPDATE DArma SET nome = 'CARRO' WHERE nome = 'CAR';
UPDATE DArma SET nome = 'CORRENTE' WHERE nome = 'CHAIN';
UPDATE DArma SET nome = 'MOTOSSERRA' WHERE nome = 'CHAINSAW';
UPDATE DArma SET nome = 'CADEIRA' WHERE nome = 'CHAIR';
UPDATE DArma SET nome = 'CUTELA' WHERE nome = 'CLEAVER';
UPDATE DArma SET nome = 'BESTA' WHERE nome = 'CROSSBOW';
UPDATE DArma SET nome = 'PÉ DE CABRA' WHERE nome = 'CROWBAR';
UPDATE DArma SET nome = 'ADAGA' WHERE nome = 'DAGGER';
UPDATE DArma SET nome = 'FURADEIRA' WHERE nome = 'DRILL';
UPDATE DArma SET nome = 'DROGAS' WHERE nome = 'DRUGS';
UPDATE DArma SET nome = 'EXPLOSIVO' WHERE nome = 'EXPLOSIVE';
UPDATE DArma SET nome = 'FOGO' WHERE nome = 'FIRE';
UPDATE DArma SET nome = 'FOGOS DE ARTIFÍCIO' WHERE nome = 'FIREWORKS';
UPDATE DArma SET nome = 'BANDEIRA' WHERE nome = 'FLAGPOLE';
UPDATE DArma SET nome = 'LANTERNA' WHERE nome = 'FLASHLIGHT';
UPDATE DArma SET nome = 'GARFO' WHERE nome = 'FORK';
UPDATE DArma SET nome = 'TESOURA DE JARDIM' WHERE nome = 'GARDEN SHEAR';
UPDATE DArma SET nome = 'FERRAMENTA DE JARDIM' WHERE nome = 'GARDEN TOOL';
UPDATE DArma SET nome = 'VIDRO' WHERE nome = 'GLASS';
UPDATE DArma SET nome = 'GRANADA' WHERE nome = 'GRENADE';
UPDATE DArma SET nome = 'ARMA DE FOGO' WHERE nome = 'GUN' or nome = 'HECKLER';
UPDATE DArma SET nome = 'MARTELO' WHERE nome = 'HAMMER';
UPDATE DArma SET nome = 'MACHADINHA' WHERE nome = 'HATCHET';
UPDATE DArma SET nome = 'TACO DE HÓQUEI' WHERE nome = 'HOCKEY STICK';
UPDATE DArma SET nome = 'PISTOLA DE COLA QUENTE' WHERE nome = 'HOT GLUE GUN';
UPDATE DArma SET nome = 'PICADOR DE GELO' WHERE nome = 'ICE PICK';
UPDATE DArma SET nome = 'DISPOSITIVO INCENDIÁRIO' WHERE nome = 'INCENDIARY DEVICE';
UPDATE DArma SET nome = 'FACA' WHERE nome = 'KNIFE';
UPDATE DArma SET nome = 'FACÃO' WHERE nome = 'MACHETE';
UPDATE DArma SET nome = 'ARTES MARCIAIS' WHERE nome = 'MARTIAL ARTS WEAPON';
UPDATE DArma SET nome = 'OBJETO METÁLICO' WHERE nome = 'METAL OBJECT';
UPDATE DArma SET nome = 'MÍSSIL' WHERE nome = 'MISSLE';
UPDATE DArma SET nome = 'MOTOCICLETA' WHERE nome = 'MOTORCYCLE';
UPDATE DArma SET nome = 'PISTOLA DE PREGOS' WHERE nome = 'NAIL GUN';
UPDATE DArma SET nome = 'REMO' WHERE nome = 'OAR';
UPDATE DArma SET nome = 'CANETA' WHERE nome = 'PEN';
UPDATE DArma SET nome = 'SPRAY DE PIMENTA' WHERE nome = 'PEPPER SPRAY';
UPDATE DArma SET nome = 'CANO' WHERE nome = 'PIPE';
UPDATE DArma SET nome = 'VENENO' WHERE nome = 'POISON';
UPDATE DArma SET nome = 'POSTE' WHERE nome = 'POLE';
UPDATE DArma SET nome = 'NAVALHA' WHERE nome = 'RAZOR';
UPDATE DArma SET nome = 'PEDRA' WHERE nome = 'ROCK';
UPDATE DArma SET nome = 'CORDA' WHERE nome = 'ROPE';
UPDATE DArma SET nome = 'ESPADA SAMURAI' WHERE nome = 'SAMURAI SWORD';
UPDATE DArma SET nome = 'LÍQUIDO ESCALDANTE' WHERE nome = 'SCALDING LIQUID';
UPDATE DArma SET nome = 'TESOURA' WHERE nome = 'SCISSORS';
UPDATE DArma SET nome = 'CHAVE DE FENDA' WHERE nome = 'SCREWDRIVER';
UPDATE DArma SET nome = 'OBJETO CORTANTE' WHERE nome = 'SHARP OBJECT';
UPDATE DArma SET nome = 'ESPINGARDA' WHERE nome = 'SHOTGUN';
UPDATE DArma SET nome = 'PÁ' WHERE nome = 'SHOVEL';
UPDATE DArma SET nome = 'LANÇA' WHERE nome = 'SPEAR';
UPDATE DArma SET nome = 'GRAMPEADOR' WHERE nome = 'STAPLER';
UPDATE DArma SET nome = 'ESTRANGULAMENTO' WHERE nome = 'STRANGULATION';
UPDATE DArma SET nome = 'ARMA DE CHOQUE' WHERE nome = 'STUN GUN';
UPDATE DArma SET nome = 'ESPADA' WHERE nome = 'SWORD';
UPDATE DArma SET nome = 'SERINGA' WHERE nome = 'SYRINGE';
UPDATE DArma SET nome = 'TASER' WHERE nome = 'TASER';
UPDATE DArma SET nome = 'CHAVE DE RODA' WHERE nome = 'TIRE IRON';
UPDATE DArma SET nome = 'BRINQUEDO' WHERE nome = 'TOY';
UPDATE DArma SET nome = 'DESARMADO' WHERE nome = 'UNARMED';
UPDATE DArma SET nome = 'VEÍCULO' WHERE nome = 'VEHICLE';
UPDATE DArma SET nome = 'BASTÃO DE CAMINHADA' WHERE nome = 'WALKING STICK';
UPDATE DArma SET nome = 'SPRAY DE VESPA' WHERE nome = 'WASP SPRAY';
UPDATE DArma SET nome = 'MADEIRA' WHERE nome = 'WOOD';
UPDATE DArma SET nome = 'CHAVE INGLESA' WHERE nome = 'WRENCH';



-- renomeando os valores do ENUM
ALTER TYPE ddroga_enum RENAME VALUE 'CONTROLLED SUBSTANCE' TO 'SUBSTÂNCIA CONTROLADA';
ALTER TYPE ddroga_enum RENAME VALUE 'CRACK COCAINE' TO 'CRACK';
ALTER TYPE ddroga_enum RENAME VALUE 'ECSTACY' TO 'ECSTASY';  
ALTER TYPE ddroga_enum RENAME VALUE 'GHB' TO 'GHB';
ALTER TYPE ddroga_enum RENAME VALUE 'HEROIN' TO 'HEROINA';
ALTER TYPE ddroga_enum RENAME VALUE 'HYDROCODONE' TO 'HIDROCODONA';
ALTER TYPE ddroga_enum RENAME VALUE 'KETAMINE' TO 'KETAMINA';
ALTER TYPE ddroga_enum RENAME VALUE 'MARIJUANA' TO 'MACONHA';
ALTER TYPE ddroga_enum RENAME VALUE 'METHAMPHETAMINE' TO 'METANFETAMINA';
ALTER TYPE ddroga_enum RENAME VALUE 'OXYCODONE' TO 'OXICODONA';
ALTER TYPE ddroga_enum RENAME VALUE 'PARAPHERNALIA' TO 'PARAFERNÁLIA';
ALTER TYPE ddroga_enum RENAME VALUE 'POWDER COCAINE' TO 'COCAÍNA';


-- Atualizando valores da coluna descricao em DCausaMorte
UPDATE DCausaMorte SET descricao = 'ACIDENTE' WHERE descricao = 'ACCIDENT';
UPDATE DCausaMorte SET descricao = 'ANIMAL' WHERE descricao = 'ANIMAL';
UPDATE DCausaMorte SET descricao = 'ASFIXIA' WHERE descricao = 'ASPHYXIA';
UPDATE DCausaMorte SET descricao = 'AGRESSÃO' WHERE descricao = 'ASSAULT';
UPDATE DCausaMorte SET descricao = 'ESPANCAMENTO' WHERE descricao = 'BEATEN';
UPDATE DCausaMorte SET descricao = 'BOMBA' WHERE descricao = 'BOMB';
UPDATE DCausaMorte SET descricao = 'QUÍMICO' WHERE descricao = 'CHEMICAL';
UPDATE DCausaMorte SET descricao = 'AFOGAMENTO' WHERE descricao = 'DROWNED';
UPDATE DCausaMorte SET descricao = 'ELETROCUTADO' WHERE descricao = 'ELECTROCUTED';
UPDATE DCausaMorte SET descricao = 'EXPLOSÃO' WHERE descricao = 'EXPLOSION';
UPDATE DCausaMorte SET descricao = 'EXPOSIÇÃO A TOXINAS' WHERE descricao = 'EXPOSURE TO TOXINS';
UPDATE DCausaMorte SET descricao = 'QUEDA' WHERE descricao = 'FALL';
UPDATE DCausaMorte SET descricao = 'INCÊNDIO' WHERE descricao = 'FIRE';
UPDATE DCausaMorte SET descricao = 'DISPARO DE ARMA DE FOGO' WHERE descricao = 'GUNFIRE';
UPDATE DCausaMorte SET descricao = 'ATAQUE CARDÍACO' WHERE descricao = 'HEART ATTACK';
UPDATE DCausaMorte SET descricao = 'EXAUSTÃO PELO CALOR' WHERE descricao = 'HEAT EXHAUSTION';
UPDATE DCausaMorte SET descricao = 'DOENÇA' WHERE descricao = 'ILLNESS';
UPDATE DCausaMorte SET descricao = 'EMERGÊNCIA MÉDICA' WHERE descricao = 'MEDICAL EMERGENCY';
UPDATE DCausaMorte SET descricao = 'DESASTRE NATURAL' WHERE descricao = 'NATURAL DISASTER';
UPDATE DCausaMorte SET descricao = 'OVERDOSE' WHERE descricao = 'OVERDOSE'; 
UPDATE DCausaMorte SET descricao = 'CONTENÇÃO FÍSICA' WHERE descricao = 'PHYSICAL RESTRAINT';
UPDATE DCausaMorte SET descricao = 'ENVENENAMENTO' WHERE descricao = 'POISONED';
UPDATE DCausaMorte SET descricao = 'ESFAQUEADO' WHERE descricao = 'STABBED';
UPDATE DCausaMorte SET descricao = 'COLAPSO DE ESTRUTURA' WHERE descricao = 'STRUCTURE COLLAPSE';
UPDATE DCausaMorte SET descricao = 'TASER' WHERE descricao = 'TASER';
UPDATE DCausaMorte SET descricao = 'ATAQUE TERRORISTA' WHERE descricao = 'TERRORIST ATTACK';
UPDATE DCausaMorte SET descricao = 'VEÍCULO' WHERE descricao = 'VEHICLE';

