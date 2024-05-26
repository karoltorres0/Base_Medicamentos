CREATE TABLE Medicamento (
    expediente varchar (500) PRIMARY KEY,
    producto VARCHAR(500),
    descripcioncomercial varchar (500),
    atc VARCHAR(500),
    formafarmaceutica varchar (500),
    IUM varchar (500) 
);

CREATE TABLE Control_Unico_Medicamentos (
    consecutivocum INTEGER PRIMARY KEY,
    expediente varchar (500) REFERENCES MEDICAMENTO(expediente),
    expedientecum varchar (500),
    cantidadcum INTEGER,
    estadocum VARCHAR(500),
    fechaactivo DATE,
    fechainactivo DATE,
    muestramedica BOOLEAN
);

CREATE TABLE Principio_Activo (
    principioactivo VARCHAR(500) PRIMARY KEY,
    unidadmedida VARCHAR(12),
    unidadreferencia VARCHAR(500)
);

CREATE TABLE Composicion_Medicamento (
    expediente varchar (500) REFERENCES MEDICAMENTO(expediente),
    principioactivo VARCHAR(500) REFERENCES PRINCIPIO_ACTIVO(principioactivo),
    concentracion varchar (500),
    cantidad numeric (50,0),
    PRIMARY KEY (expediente, principioactivo)
);

CREATE TABLE Registro_Sanitario (
    registrosanitario varchar (500) PRIMARY KEY,
    expediente varchar (500) REFERENCES MEDICAMENTO(expediente),
    titular VARCHAR(500),
    fechaexpedicion DATE,
    fechavencimiento DATE,
    estadoregistro VARCHAR(500)
);

CREATE TABLE Rol_Medicamento (
    nombrerol VARCHAR(500) PRIMARY KEY,
    registrosanitario VARCHAR (500) REFERENCES REGISTRO_SANITARIO(registrosanitario),
    tiporol VARCHAR(500),
    descripcionatc VARCHAR(250),
    modalidad VARCHAR(500)
);


COPY Medicamento (expediente, producto, descripcioncomercial, atc, formafarmaceutica, IUM)
FROM 'C:\Users\Public\Medicamento.csv' DELIMITER AS ',' CSV HEADER;

COPY Control_Unico_Medicamentos (consecutivocum, expediente, expedientecum, cantidadcum, estadocum, fechaactivo, fechainactivo, muestramedica)
FROM 'C:\Users\Public\Control_Unico_Medicamentos.csv' DELIMITER AS ',' CSV HEADER;

COPY Principio_Activo (principioactivo, unidadmedida, unidadreferencia)
FROM 'C:\Users\Public\Principio_Activo.csv' DELIMITER AS ',' CSV HEADER;

COPY Composicion_Medicamento (expediente, principioactivo, concentracion, cantidad)
FROM 'C:\Users\Public\Composicion_Medicamento.csv' DELIMITER AS ',' CSV HEADER;

COPY Registro_Sanitario (registrosanitario, expediente, titular, fechaexpedicion, fechavencimiento, estadoregistro)
FROM 'C:\Users\Public\Registro_Sanitario.csv' DELIMITER AS ',' CSV HEADER;

COPY Rol_Medicamento (nombrerol, registrosanitario, tiporol, descripcionatc, modalidad)
FROM 'C:\Users\Public\Rol_Medicamento.csv' DELIMITER AS ',' CSV HEADER;

