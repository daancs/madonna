--Clean everything
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;

--Table of Users
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), --random generated UUID
    username TEXT UNIQUE NOT NULL, --username
    password TEXT NOT NULL --password
);

--Creating an enum for the progress of specific studies
CREATE TYPE progress AS ENUM ('enkät ej utskickad', 'enkät utskickad', 'enkät delvis ifylld', 'enkät ifylld');

--Table of Patients
CREATE TABLE Patients (
    key_id CHAR(4) PRIMARY KEY, --identifying key_id
    idnr CHAR(13), --personal idnr
    name TEXT NOT NULL, --name
    age INT NOT NULL, --age
    gender TEXT NOT NULL, --gender
    weight INT NOT NULL, --weight
    bmi REAL NOT NULL, --body mass index
    nicotine TEXT NOT NULL, --If the patient uses nicotine and in that case what
    deceased BOOL NOT NULL DEFAULT FALSE, --if the patient is deceased or not
    adress TEXT NOT NULL, --adress
    city TEXT NOT NULL, --city
    zipcode NUMERIC(5) NOT NULL --zipcode
);

--Table of specific patients medical history and compliation
CREATE TABLE MedicalHistory (
    key_id CHAR(4) NOT NULL REFERENCES Patients (key_id),
    complication TEXT NOT NULL,
    PRIMARY KEY(key_id, complication)
);

--Table of cases assosiated with specific patients
CREATE TABLE Cases (
    caseId UUID PRIMARY KEY DEFAULT gen_random_uuid(), --random generated UUID
    patient CHAR(4) NOT NULL, --key_id references Patients.key_id
    complication TEXT NOT NULL, --complicatien
    reviewedBy TEXT NOT NULL, --the doctor reviewing the case
    reviewDate TIMESTAMP NOT NULL, --review date
    closed BOOL NOT NULL, --is the case open or closed
    FOREIGN KEY (patient) REFERENCES Patients (key_id),
    UNIQUE (caseId,patient) --combination of caseId and patient need to be unique
);

--Table of treatments for specific cases
CREATE TABLE Treatments (
    treatmentId UUID DEFAULT gen_random_uuid(), --random generated UUID
    caseId UUID NOT NULL, --caseID references Cases.caseId
    cytostatics TEXT NOT NULL, --if cytostatic treatment is used
    operationDate TIMESTAMP NOT NULL, -- operation date
    doctor TEXT NOT NULL, --doctor performing the treatment
    assistent TEXT NOT NULL, --assistant present
    medication TEXT NOT NULL, --medication after treatment
    FOREIGN KEY (caseId) REFERENCES Cases (caseId),
    PRIMARY KEY (treatmentId,caseId)
);

--Table of patient and studies they are included in
CREATE TABLE Studies(
    studyID INTEGER, --studyID
    patient CHAR(4) NOT NULL, --patien
    studyNumber INT NOT NULL,
    PRIMARY KEY(patient, studyID)
);

--Table of patients in study 1 and their answers
CREATE TABLE Study1 (
    studyID INTEGER,
    patient CHAR(4) REFERENCES Patients(key_id),
    progress progress DEFAULT 'enkät ej utskickad',
    do_you_smoke BOOL NOT NULL DEFAULT 'TRUE',
    is_your_house_red BOOL NOT NULL DEFAULT 'TRUE',
    is_your_dog_gay BOOL NOT NULL DEFAULT 'TRUE',
    FOREIGN  KEY (patient, studyID) REFERENCES Studies(patient, studyID),
    PRIMARY KEY (patient, studyID)
);

--Table of patients in study 2 and their answers
CREATE TABLE Study2 (
    studyID INTEGER,
    patient CHAR(4) REFERENCES Patients(key_id),
    progress progress DEFAULT 'enkät ej utskickad',
    how_tall_are_you TEXT DEFAULT 'Not answered',
    how_much_do_you_make TEXT DEFAULT 'Not answered',
    is_your_cat_gay BOOL NOT NULL DEFAULT 'TRUE',
    FOREIGN  KEY (patient, studyID) REFERENCES Studies(patient, studyID),
    PRIMARY KEY (patient, studyID)
);

--Some inserts of example data to the patient table
INSERT INTO Patients (key_id,idnr,name,age,gender,weight,bmi,nicotine,adress,city,zipcode) VALUES
('0001','20000901-1234', 'Foo Bar', '69', 'Male' ,'420', '21.2', 'Nej', 'Hubbenvägen 1','Göteborg','41280'),
('0002','19940418-6234', 'Por Tals', '35','Female' ,'098', '21.59', 'Ja, lmao', 'Kemivägen 1','Göteborg','43331'),
('0003','19760123-8932', 'Rop Slat', '21', 'Male' , '98', '23.12', 'Nej', 'Föreningsgatan 12','Sävedalen','43370'),
('0004','19120313-3891', 'Zlatan Zlatansson', '110', 'Male', '123', '35.00', 'Ja', 'Bondgatan 123','Götebort','41170'),
('0005','20120124-1876', 'Anna Annasson', '11', 'Female', '24', '20.22', 'Ja', 'Bondgatan 321','Göteborg','41123'),
('0006','13370101-1876', 'Carl Carlsson', '13', 'Male', '100', '45', 'Ja', 'Vasagatan 1','Göteborg','41236'),
('0007','20010603-1934', 'Zlatan Persson', '35', 'Male', '100', '19', 'Nej', 'Chalmersgatan 2','Götebort','43136'),
('0008','19951412-3895', 'Sven-Gunnar Lanngren', '10', 'Male', '79', '23', 'Nej', 'Vikenviken 16','Billdal','43652'),
('0009','17690815-1337', 'Napoleone Buonaparte', '51', 'Male', '77', '27.3', 'Ja', 'rue Saint-Charles 20000','Ajaccio','42411'),
('0010','19711010-0007', 'James Bond', '40', 'Male', '80', '22', 'Ja', 'Bondgatan 0','London','00700'),
('0011','19170702-3434', 'To Andersson', '50', 'Female', '45', '19', 'Nej', 'Daseborg','Götebort','41270'),
('0012','18950103-5454', 'Snobben Snobbsson', '111', 'Female', '40', '16', 'Nej', 'Verum 1','Göteborg','41236'),
('0013','19240503-6767', 'Asterix Gallsson', '74', 'Female', '90', '35.00', 'Ja', 'Winden 3','Götebort','42436'),
('0014','19781212-6789', 'Super Mario', '45', 'Male', '78', '21', 'Nej', 'Japangatan 1','Tokyo','42136'),
('0015','19831111-1234', 'Kalle Anka', '12', 'Female', '120', '33', 'Nej', 'Kalle ankas allé 1','Ankebort','41211');

--Some inserts of example data to the medical history table
INSERT INTO MedicalHistory (key_id,complication) VALUES
('0001', 'Diabetes'),
('0001', 'Neurologisk sjukdom'),
('0002', 'Hjärtsjukdom'),
('0003', 'Ämnesomsättningssjukdom'),
('0005', 'Leversjukdom');

--Some inserts of example data to the cases table
INSERT INTO Cases (caseId,patient,complication,reviewedBy,reviewDate,closed) VALUES
('a789ea53-08b6-4108-a1d5-e992c2413654','0002', 'Cancer höger bröst','skrr','2022-09-23 12:30','FALSE'),
('27411ee6-c60b-11ec-9d64-0242ac120002','0001', 'Cancer vänster bröst', 'Kingen', '2022-04-19','TRUE'),
('db65bf73-d73a-4cd3-8848-c6618b893fc2','0005', 'Bröstcancer', 'Zlatan' ,'2022-01-01', 'FALSE'),
('f86cfbb0-45e1-4652-9e2d-e50bae59515b','0003','Cancer', 'Doktor' ,'2020-06-13', 'FALSE');

--Some inserts of example data to the treatments table
INSERT INTO Treatments (caseId,cytostatics,operationDate, doctor, assistent, medication) VALUES
('a789ea53-08b6-4108-a1d5-e992c2413654', 'Ja','2013-12-01', 'Gustavsson', 'Kingen', 'Adjuvant hormonterapi'),
('27411ee6-c60b-11ec-9d64-0242ac120002', 'Okänt','2014-11-19', 'Zlatan', 'Gästläkare', 'Adjuvant hormonterapi');

--Table of a specific users search history
CREATE TABLE SearchHistory (
    search TEXT PRIMARY KEY
);

-- Table for changeLog to the patient data
CREATE TABLE changeLog (
    id SERIAL PRIMARY KEY,
    tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(1),
    operation TEXT NOT NULL,
    who TEXT DEFAULT current_user,
    new_val JSON,
    old_val JSON
);

-- Simple table for keeping track of currently logged in user.
CREATE TABLE currentFlaskUser (
    flaskUser TEXT PRIMARY KEY
);
INSERT INTO currentFlaskUser (flaskUser) VALUES ('not-logged-in');

-- Maybe a function for setting the current user in Flask
CREATE FUNCTION change_trigger() RETURNS trigger AS $$
BEGIN
    IF  TG_OP = 'INSERT'
        THEN
        INSERT INTO changeLog (operation, who, new_val)
        VALUES (TG_OP, (SELECT flaskUser FROM currentFlaskUser), row_to_json(NEW));
        RETURN NEW;
    ELSIF   TG_OP = 'UPDATE'
        THEN
        INSERT INTO changeLog (operation, who, new_val, old_val)
        VALUES (TG_OP, (SELECT flaskUser FROM currentFlaskUser), row_to_json(NEW), row_to_json(OLD));
        RETURN NEW;
    ELSIF   TG_OP = 'DELETE'
        THEN
        INSERT INTO changeLog (operation, who, old_val)
        VALUES (TG_OP, (SELECT flaskUser FROM currentFlaskUser), row_to_json(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;

CREATE TRIGGER changeLogTrigger INSERT OR UPDATE OR DELTE ON patients
    FOR EACH ROW EXCECUTE PROCEDURE change_trigger();

--Some inserts of example data to the studies table
INSERT INTO Studies(studyID, patient, studyNumber) VALUES
(1, '0001','1'),
(1, '0002','1'),
(2, '0003','2'),
(1, '0004','1'),
(2, '0005','2'),
(1, '0008','1'),
(2, '0009','2'),
(1, '0010','1'),
(2, '0012','2'),
(1, '0015','1');

--Some inserts of example data to the study1 table
INSERT INTO Study1(studyID, patient, progress, do_you_smoke, is_your_house_red, is_your_dog_gay) VALUES
(1, '0001', 'enkät utskickad', 'TRUE', 'FALSE', 'TRUE'),
(1, '0002', 'enkät delvis ifylld', 'TRUE', 'TRUE', 'TRUE'),
(1, '0004', 'enkät utskickad', 'TRUE', 'FALSE', 'TRUE'),
(1, '0008', 'enkät ifylld', 'TRUE', 'TRUE', 'TRUE');
INSERT INTO Study1(studyID, patient, progress, is_your_house_red, is_your_dog_gay) VALUES
(1, '0010', 'enkät ej utskickad', 'TRUE', 'TRUE'),
(1, '0015', 'enkät ej utskickad', 'FALSE', 'TRUE');

--Some inserts of example data to the study2 table
INSERT INTO Study2(studyID, patient, progress, how_tall_are_you, how_much_do_you_make, is_your_cat_gay) VALUES
(2, '0003','enkät ifylld','165','100000','TRUE');
INSERT INTO Study2(studyID, patient, progress, how_much_do_you_make, is_your_cat_gay) VALUES
(2, '0005','enkät ifylld','89561','TRUE'),
(2, '0009','enkät ej utskickad','3142','TRUE'),
(2, '0012','enkät delvis ifylld','9998612','TRUE');
