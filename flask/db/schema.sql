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
    gender TEXT NOT NULL,
    weight INT NOT NULL,
    bmi REAL NOT NULL,
    nicotine TEXT NOT NULL,
    deceased BOOL NOT NULL DEFAULT FALSE,
    adress TEXT NOT NULL,
    city TEXT NOT NULL,
    zipcode NUMERIC(5) NOT NULL
);

CREATE TABLE MedicalHistory (
    key_id CHAR(4) NOT NULL REFERENCES Patients (key_id),
    complication TEXT NOT NULL,
    PRIMARY KEY(key_id, complication)
);

CREATE TABLE Cases (
    caseId UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient CHAR(4) NOT NULL,
    complication TEXT NOT NULL,
    reviewedBy TEXT NOT NULL,
    reviewDate TIMESTAMP NOT NULL,
    closed BOOL NOT NULL,
    FOREIGN KEY (patient) REFERENCES Patients (key_id),
    UNIQUE (caseId,patient)
);

CREATE TABLE Treatments (
    treatmentId UUID DEFAULT gen_random_uuid(),
    caseId UUID NOT NULL,
    cytostatics TEXT NOT NULL,
    operationDate TIMESTAMP NOT NULL,
    doctor TEXT NOT NULL,
    assistent TEXT NOT NULL,
    medication TEXT NOT NULL,
    FOREIGN KEY (caseId) REFERENCES Cases (caseId),
    PRIMARY KEY (treatmentId,caseId)
);

INSERT INTO Patients (key_id,idnr,name,age,gender,weight,bmi,nicotine,adress,city,zipcode) VALUES
('0001','20000901-1234', 'Foo Bar', '69', 'Male' ,'420', '21.2', 'Nej', 'Hubbenvägen 1','Göteborg','41280'),
('0002','19940418-6234', 'Por Tals', '35','Female' ,'098', '21.59', 'Ja, lmao', 'Kemivägen 1','Göteborg','43331'),
('0003','19760123-8932', 'Rop Slat', '21', 'Male' , '98', '23.12', 'Nej', 'Föreningsgatan 12','Sävedalen','43370'),
('0004','19120313-3891', 'Zlatan Zlatansson', '110', 'Male', '123', '35.00', 'Ja', 'Bondgatan 123','Götebort','41170'),
('0005','20120124-1876', 'Anna Annasson', '11', 'Female', '24', '20.22', 'Ja', 'Bondgatan 321','Göteborg','41123');

INSERT INTO MedicalHistory (key_id,complication) VALUES
('0001', 'Diabetes'),
('0001', 'Neurologisk sjukdom'),
('0002', 'Hjärtsjukdom'),
('0003', 'Ämnesomsättningssjukdom'),
('0005', 'Leversjukdom');

INSERT INTO Cases (caseId,patient,complication,reviewedBy,reviewDate,closed) VALUES
('a789ea53-08b6-4108-a1d5-e992c2413654','0002', 'Cancer höger bröst','skrr','2022-09-23 12:30','FALSE'),
('27411ee6-c60b-11ec-9d64-0242ac120002','0001', 'Cancer vänster bröst', 'Kingen', '2022-04-19','TRUE'),
('db65bf73-d73a-4cd3-8848-c6618b893fc2','0005', 'Bröstcancer', 'Zlatan' ,'2022-01-01', 'FALSE'),
('f86cfbb0-45e1-4652-9e2d-e50bae59515b','0003','Cancer', 'Doktor' ,'2020-06-13', 'FALSE');

INSERT INTO Treatments (caseId,cytostatics,operationDate, doctor, assistent, medication) VALUES
('a789ea53-08b6-4108-a1d5-e992c2413654', 'Ja','2013-12-01', 'Gustavsson', 'Kingen', 'Adjuvant hormonterapi'),
('27411ee6-c60b-11ec-9d64-0242ac120002', 'Okänt','2014-11-19', 'Zlatan', 'Gästläkare', 'Adjuvant hormonterapi');


CREATE TABLE SearchHistory (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP(1),
    who TEXT NOT NULL,
    query TEXT NOT NULL,
    result JSON
);
