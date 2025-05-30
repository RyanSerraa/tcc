CREATE TYPE race_enum AS ENUM ('WHITE', 'BLACK', 'ASIAN', 'UNKNOWN', 'HISPANIC', 'OTHERS');
CREATE TYPE type_enum AS ENUM ('POLICE', 'VICTIM', 'CRIMINAL');
CREATE TYPE threat_enum AS ENUM ('ATTACK', 'OTHER', 'UNKNOWN');
CREATE TYPE flee_enum AS ENUM ('VECHILE', 'FOOT', 'UNKNOWN', 'NOT FLEEING');
CREATE TYPE gender_enum AS ENUM('MALE', 'FEMALE', 'UNKNOWN', 'OTHERS');

CREATE TABLE DLocal (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  state VARCHAR(255) NOT NULL,
  city VARCHAR(255) NOT NULL,
  latitude DECIMAL(9,6) NOT NULL,
  longitude DECIMAL(9,6) NOT NULL,
  avgBlack REAL NOT NULL,
  avgWhite REAL NOT NULL,
  avgHispanic REAL NOT NULL,
  avgAsian REAL NOT NULL,
  standardDeviationBlack REAL NOT NULL,
  standardDeviationWhite REAL NOT NULL,
  standardDeviationHispanic REAL NOT NULL,
  standardDeviationAsian REAL NOT NULL
);

CREATE TABLE DPerson (
  id UUID NOT NULL,
  idGroupAge INTEGER NOT NULL,
  name VARCHAR(255) NOT NULL,
  gender gender_enum NOT NULL,
  race race_enum NOT NULL,
  typePerson type_enum NOT NULL,
  rangeInf INTEGER NOT NULL,
  rangeSup INTEGER NOT NULL,
  PRIMARY KEY (id, idGroupAge)
);

CREATE TABLE DCrime (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL
);

CREATE TABLE DDrug (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL
);

CREATE TABLE DDeathCause (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "desc" VARCHAR(255) NOT NULL
);

CREATE TABLE DDept (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL
);

CREATE TABLE DWeapon (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL
);

CREATE TABLE FDeathPolice (
  idPerson UUID NOT NULL,
  idGroupAge INTEGER NOT NULL,
  idDeathCause UUID NOT NULL,
  idDept UUID NOT NULL,
  idLocal UUID NOT NULL,
  day INTEGER NOT NULL,
  month INTEGER NOT NULL,
  year INTEGER NOT NULL,
  PRIMARY KEY (idPerson),
  FOREIGN KEY (idPerson, idGroupAge) REFERENCES DPerson (id, idGroupAge),
  FOREIGN KEY (idDept) REFERENCES DDept (id),
  FOREIGN KEY (idLocal) REFERENCES DLocal (id),
  FOREIGN KEY (idDeathCause) REFERENCES DDeathCause (id)
);

CREATE TABLE FShootings (
  idPerson UUID NOT NULL,
  idWeapon UUID NOT NULL,
  idGroupAge INTEGER NOT NULL,
  idLocal UUID NOT NULL,
  idCauseDeath UUID NOT NULL,
  threatLevel threat_enum NOT NULL,
  flee flee_enum NOT NULL,
  bodyCamera BOOLEAN,
  day INTEGER NOT NULL,
  month INTEGER NOT NULL,
  year INTEGER NOT NULL,
  PRIMARY KEY (idPerson),
  FOREIGN KEY (idPerson, idGroupAge) REFERENCES DPerson (id, idGroupAge),
  FOREIGN KEY (idLocal) REFERENCES DLocal (id),
  FOREIGN KEY (idCauseDeath) REFERENCES DDeathCause (id),
  FOREIGN KEY (idWeapon) REFERENCES DWeapon (id)
);

CREATE TABLE FFatalEncounters (
  idPerson UUID NOT NULL,
  idGroupAge INTEGER NOT NULL,
  idDeathCause UUID NOT NULL,
  idWeapon UUID NOT NULL,
  idDept UUID NOT NULL,
  idLocal UUID NOT NULL,
  threatLevel threat_enum NOT NULL,
  flee flee_enum NOT NULL,
  bodyCamera BOOLEAN,
  year INTEGER NOT NULL,
  month INTEGER NOT NULL,
  day INTEGER NOT NULL,
  PRIMARY KEY (idPerson),
  FOREIGN KEY (idPerson, idGroupAge) REFERENCES DPerson (id, idGroupAge),
  FOREIGN KEY (idDept) REFERENCES DDept (id),
  FOREIGN KEY (idLocal) REFERENCES DLocal (id),
  FOREIGN KEY (idDeathCause) REFERENCES DDeathCause (id),
  FOREIGN KEY (idWeapon) REFERENCES DWeapon (id)
);

CREATE TABLE FArrest (
  idCrime UUID NOT NULL,
  idLocal UUID NOT NULL,
  idPerson UUID NOT NULL,
  idGroupAge INTEGER NOT NULL,
  idWeapon UUID NOT NULL,
  idDrug UUID NOT NULL,
  year INTEGER NOT NULL,
  month INTEGER NOT NULL,
  day INTEGER NOT NULL,
  PRIMARY KEY (idCrime, idLocal, idPerson, idGroupAge, idWeapon, idDrug, day, month, year),
  FOREIGN KEY (idCrime) REFERENCES DCrime (id),
  FOREIGN KEY (idLocal) REFERENCES DLocal (id),
  FOREIGN KEY (idPerson, idGroupAge) REFERENCES DPerson (id, idGroupAge),
  FOREIGN KEY (idWeapon) REFERENCES DWeapon (id),
  FOREIGN KEY (idDrug) REFERENCES DDrug (id)
);


CREATE TABLE FCrime (
  idCrime UUID NOT NULL,
  idPerson UUID NOT NULL,
  idGroupAge INTEGER NOT NULL,
  idWeapon UUID NOT NULL,
  idLocal UUID NOT NULL,
  year INTEGER NOT NULL,
  month INTEGER NOT NULL,
  day INTEGER NOT NULL,
  PRIMARY KEY (idCrime, idPerson, idGroupAge, idWeapon, idLocal, day, month, year),
  FOREIGN KEY (idCrime) REFERENCES DCrime (id),
  FOREIGN KEY (idLocal) REFERENCES DLocal (id),
  FOREIGN KEY (idPerson, idGroupAge) REFERENCES DPerson (id, idGroupAge),
  FOREIGN KEY (idWeapon) REFERENCES DWeapon (id)
);
