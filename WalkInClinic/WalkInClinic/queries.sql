insert into PATIENT(First_name,Last_name,Phone,Address) values ('Ishan','Pandya',9856547852,'Rosewood Drive')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('John','Right',7865456347,'St Anne Road')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('William','Tibbit',7659872649,'Hazel Street')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('Jesica','Lorenson',4345002595,'Hazel Street')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('Martina','Cook',8763653756,'Morgan Road')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('Jason','Roy',9836351979,'Churchil Road')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('Kane','Marsh',7647382746,'Doon South Valley')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('Justin','Cook',9876563726,'Niagara Road')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('Ross','Martini',9923443467,'Joel Steert')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('Rizwan','Khan',9823498732,'Churchil Road')
insert into PATIENT(First_name,Last_name,Phone,Address) values ('Amara','Watson',8785765745,'Morgan Road')

insert into DOCTOR(First_name,Last_name,Phone,Address,Specialization,Consultation_Fee) VALUES 
('Abhi','Patel',8569857412,'Wixon Street','MS Ortho',900)

insert into DOCTOR(First_name,Last_name,Phone,Address,Specialization,Consultation_Fee) VALUES 
('Kane','Williamson',7498564585,'Albert Street','MBBS',200)

insert into DOCTOR(First_name,Last_name,Phone,Address,Specialization,Consultation_Fee) VALUES 
('Jhye','Richardson',5197845689,'Lescter Street','Dentist',450)

insert into DOCTOR(First_name,Last_name,Phone,Address,Specialization,Consultation_Fee) VALUES 
('Steve','Smith',2268957845,'Queen Street','Psychologist',600)

insert into DOCTOR(First_name,Last_name,Phone,Address,Specialization,Consultation_Fee) VALUES 
('David','Shepherd',5197852356,'Dixon Street','MBBS',350)

insert into DOCTOR(First_name,Last_name,Phone,Address,Specialization,Consultation_Fee) VALUES 
('Marnus','Daniel',2268594578,'King Street','Psychologist',450)

insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (1,1,'2021-04-21 16:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (2,4,'2021-05-10 11:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (4,5,'2021-04-15 13:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (6,9,'2021-05-25 18:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (8,3,'2021-05-12 20:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (3,8,'2021-04-18 16:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (7,7,'2021-05-15 17:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (5,6,'2021-05-13 19:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (9,9,'2021-04-14 10:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (18,1,'2021-05-24 08:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (16,9,'2021-05-30 09:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (11,6,'2021-04-13 10:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (10,7,'2021-04-19 15:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (13,6,'2021-05-12 11:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (15,9,'2021-05-19 19:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (14,8,'2021-04-17 18:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (17,4,'2021-05-13 16:00')
insert into APPOINTMENT(Patient_ID,Doctor_ID,Apt_DateTime) values (12,6,'2021-05-19 13:00')

select * from APPOINTMENT where Patient_ID = 1
delete from APPOINTMENT