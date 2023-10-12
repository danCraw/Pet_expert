CREATE TABLE clients (
        id SERIAL NOT NULL,
        name VARCHAR(65) NOT NULL,
        surname VARCHAR(65) NOT NULL,
        patronomic VARCHAR(65) NOT NULL,
        photo VARCHAR(65) NOT NULL,
        phone VARCHAR(65) NOT NULL,
        email VARCHAR(65) NOT NULL,
        password_hash VARCHAR(65) NOT NULL,
        PRIMARY KEY (id)
);


CREATE TABLE doctors (
        id SERIAL NOT NULL,
        name VARCHAR(65) NOT NULL,
        surname VARCHAR(65) NOT NULL,
        patronomic VARCHAR(65) NOT NULL,
        photo VARCHAR(65) NOT NULL,
        email VARCHAR(65) NOT NULL,
        password_hash VARCHAR(65) NOT NULL,
        rating FLOAT NOT NULL,
        education VARCHAR(150) NOT NULL,
        treatment_profile VARCHAR(1000) NOT NULL,
        work_experience INTEGER NOT NULL,
        PRIMARY KEY (id)
);

CREATE TABLE visits (
    id SERIAL,
    client_id INTEGER NOT NULL,
    diagnosis VARCHAR(65) NOT NULL,
    photos VARCHAR(65)[] NOT NULL,
    date_of_receipt DATE NOT NULL,
    pet_name VARCHAR(65) NOT NULL,
    pet_age INTEGER NOT NULL,
    pet_breed VARCHAR(65) NOT NULL,
    pet_type VARCHAR(65) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE

);

CREATE TABLE hospitals (
    id SERIAL NOT NULL,
    name VARCHAR(65) NOT NULL,
    description VARCHAR(150) NOT NULL,
    photos VARCHAR(65)[] NOT NULL,
    phone VARCHAR(65),
    email VARCHAR(65) NOT NULL,
    password_hash VARCHAR(65) NOT null,
    PRIMARY KEY (id)
);

CREATE TABLE reviews (
    id SERIAL NOT NULL,
    visit_id INTEGER NOT NULL,
    hospital_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    liked VARCHAR (2000) NOT NULL,
    did_not_liked VARCHAR (2000) NOT NULL,
    comment VARCHAR (2000) NOT NULL,
    review_time TIMESTAMP NOT NULL,
    confirmed BOOLEAN NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals (id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE CASCADE,
    FOREIGN KEY (visit_id) REFERENCES visits (id) ON DELETE CASCADE
);

CREATE TABLE reply (
    review_id INTEGER NOT NULL,
    reply_review_id INTEGER NOT NULL,
    FOREIGN KEY (review_id) REFERENCES reviews (id) ON DELETE CASCADE,
    FOREIGN KEY (reply_review_id) REFERENCES reviews (id) ON DELETE CASCADE
);

CREATE TABLE filial (
    hospital_id INTEGER NOT NULL,
    filial_id INTEGER NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES hospitals (id) ON DELETE CASCADE,
    FOREIGN KEY (filial_id) REFERENCES hospitals (id) ON DELETE CASCADE
);

CREATE TABLE addresses (
    id SERIAL NOT NULL,
    hospital_id INTEGER NOT NULL,
    city VARCHAR(65) NOT NULL,
    street VARCHAR(65) NOT NULL,
    number INTEGER NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES hospitals (id) ON DELETE CASCADE
);

CREATE TABLE day_of_week (
    id SERIAL NOT NULL,
    name VARCHAR(65) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE services (
    id SERIAL NOT NULL,
    name VARCHAR(65) NOT NULL,
    description VARCHAR(150) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE work_day (
    id SERIAL NOT NULL,
    service_id INTEGER,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    time_range INTERVAL NOT null,
    PRIMARY KEY (id),
    FOREIGN KEY (service_id) REFERENCES services (id) ON DELETE SET NULL
);

CREATE TABLE doctor_service (
    doctor_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
    PRIMARY KEY (doctor_id, service_id),
    FOREIGN KEY (service_id) REFERENCES services (id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE CASCADE
);

CREATE TABLE doctor_hospital (
    doctor_id INTEGER NOT NULL,
    hospital_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    PRIMARY KEY (doctor_id, hospital_id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals (id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE CASCADE
);

CREATE TABLE favorite_doctors (
    client_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    PRIMARY KEY (client_id, doctor_id),
    FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE CASCADE
);

CREATE TABLE favorite_hospitals (
    client_id INTEGER NOT NULL,
    hospital_id INTEGER NOT NULL,
    PRIMARY KEY (client_id, hospital_id),
    FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE,
    FOREIGN KEY (hospital_id) REFERENCES hospitals (id) ON DELETE CASCADE
);

CREATE TABLE course (
    id SERIAL NOT NULL,
    name VARCHAR(65) NOT NULL,
    description VARCHAR(150) NOT NULL,
    photos VARCHAR(150)[] NOT NULL,
    doctor_id INTEGER NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE CASCADE
);

CREATE TABLE schedule (
    id SERIAL NOT NULL,
    doctor_id INTEGER NOT NULL,
    day_of_week_id INTEGER NOT NULL,
    work_day_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE cascade,
    FOREIGN KEY (day_of_week_id) REFERENCES day_of_week (id) ON DELETE cascade,
    FOREIGN KEY (work_day_id) REFERENCES work_day (id) ON DELETE cascade
);