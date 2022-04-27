--Clean everything
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;

CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE Patients (
    key_id CHAR(4) PRIMARY KEY,
    idnr CHAR(13),
    name TEXT NOT NULL,
    age INT NOT NULL,
    weight INT NOT NULL,
    bmi REAL NOT NULL,
    nicotine TEXT NOT NULL,
    deceased BOOL NOT NULL DEFAULT FALSE,
    adress TEXT NOT NULL,
    city TEXT NOT NULL,
    zipcode NUMERIC(5) NOT NULL
);

CREATE TABLE Cases (
    caseId UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient CHAR(4) NOT NULL,
    reviewedBy TEXT NOT NULL,
    reviewDate TIMESTAMP NOT NULL,
    closed BOOL NOT NULL,
    FOREIGN KEY (patient) REFERENCES Patients (key_id)
);

CREATE TABLE Treatments (
    treatmentId UUID DEFAULT gen_random_uuid(),
    caseId UUID NOT NULL,
    parameter1 TEXT NOT NULL,
    parameter2 TEXT NOT NULL,
    FOREIGN KEY (caseId) REFERENCES Cases (caseId),
    PRIMARY KEY (treatmentId,caseId)
);

INSERT INTO Patients (key_id,idnr,name,age,weight,bmi,nicotine,adress,city,zipcode) VALUES ('0001','20000901-1234', 'Foo Bar', '69', '420', '21.2', 'Nej', 'Hubbenvägen 1','Göteborg','41280');
INSERT INTO Patients (key_id,idnr,name,age,weight,bmi,nicotine,adress,city,zipcode) VALUES ('0002','19940418-6234', 'Por Tals', '35', '098', '21.59', 'Ja, lmao', 'Kemivägen 1','Göteborg','43331');

INSERT INTO Cases (patient,reviewedBy,reviewDate,closed) VALUES ('0001','Kingen','2022-04-19','TRUE');
INSERT INTO Cases (caseId,patient,reviewedBy,reviewDate,closed) VALUES ('a789ea53-08b6-4108-a1d5-e992c2413654','0002','skrr','2022-09-23 12:30','FALSE');

INSERT INTO Treatments (caseId,parameter1,parameter2) VALUES ('a789ea53-08b6-4108-a1d5-e992c2413654','TESTING','HELLO WORLD!');

