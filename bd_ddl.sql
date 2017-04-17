CREATE TABLE django_migrations
(
  id      SERIAL                   NOT NULL
    CONSTRAINT django_migrations_pkey
    PRIMARY KEY,
  app     VARCHAR(255)             NOT NULL,
  name    VARCHAR(255)             NOT NULL,
  applied TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE django_content_type
(
  id        SERIAL       NOT NULL
    CONSTRAINT django_content_type_pkey
    PRIMARY KEY,
  app_label VARCHAR(100) NOT NULL,
  model     VARCHAR(100) NOT NULL,
  CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq
  UNIQUE (app_label, model)
);

CREATE TABLE auth_permission
(
  id              SERIAL       NOT NULL
    CONSTRAINT auth_permission_pkey
    PRIMARY KEY,
  name            VARCHAR(255) NOT NULL,
  content_type_id INTEGER      NOT NULL
    CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co
    REFERENCES django_content_type
    DEFERRABLE INITIALLY DEFERRED,
  codename        VARCHAR(100) NOT NULL,
  CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq
  UNIQUE (content_type_id, codename)
);

CREATE INDEX auth_permission_content_type_id_2f476e4b
  ON auth_permission (content_type_id);

CREATE TABLE auth_group
(
  id   SERIAL      NOT NULL
    CONSTRAINT auth_group_pkey
    PRIMARY KEY,
  name VARCHAR(80) NOT NULL
    CONSTRAINT auth_group_name_key
    UNIQUE
);

CREATE INDEX auth_group_name_a6ea08ec_like
  ON auth_group (name);

CREATE TABLE auth_group_permissions
(
  id            SERIAL  NOT NULL
    CONSTRAINT auth_group_permissions_pkey
    PRIMARY KEY,
  group_id      INTEGER NOT NULL
    CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
    REFERENCES auth_group
    DEFERRABLE INITIALLY DEFERRED,
  permission_id INTEGER NOT NULL
    CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
    REFERENCES auth_permission
    DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq
  UNIQUE (group_id, permission_id)
);

CREATE INDEX auth_group_permissions_group_id_b120cbf9
  ON auth_group_permissions (group_id);

CREATE INDEX auth_group_permissions_permission_id_84c5c92e
  ON auth_group_permissions (permission_id);

CREATE TABLE auth_user
(
  id           SERIAL                   NOT NULL
    CONSTRAINT auth_user_pkey
    PRIMARY KEY,
  password     VARCHAR(128)             NOT NULL,
  last_login   TIMESTAMP WITH TIME ZONE,
  is_superuser BOOLEAN                  NOT NULL,
  username     VARCHAR(150)             NOT NULL
    CONSTRAINT auth_user_username_key
    UNIQUE,
  first_name   VARCHAR(30)              NOT NULL,
  last_name    VARCHAR(30)              NOT NULL,
  email        VARCHAR(254)             NOT NULL,
  is_staff     BOOLEAN                  NOT NULL,
  is_active    BOOLEAN                  NOT NULL,
  date_joined  TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX auth_user_username_6821ab7c_like
  ON auth_user (username);

CREATE TABLE auth_user_groups
(
  id       SERIAL  NOT NULL
    CONSTRAINT auth_user_groups_pkey
    PRIMARY KEY,
  user_id  INTEGER NOT NULL
    CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id
    REFERENCES auth_user
    DEFERRABLE INITIALLY DEFERRED,
  group_id INTEGER NOT NULL
    CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id
    REFERENCES auth_group
    DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq
  UNIQUE (user_id, group_id)
);

CREATE INDEX auth_user_groups_user_id_6a12ed8b
  ON auth_user_groups (user_id);

CREATE INDEX auth_user_groups_group_id_97559544
  ON auth_user_groups (group_id);

CREATE TABLE auth_user_user_permissions
(
  id            SERIAL  NOT NULL
    CONSTRAINT auth_user_user_permissions_pkey
    PRIMARY KEY,
  user_id       INTEGER NOT NULL
    CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id
    REFERENCES auth_user
    DEFERRABLE INITIALLY DEFERRED,
  permission_id INTEGER NOT NULL
    CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm
    REFERENCES auth_permission
    DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
  UNIQUE (user_id, permission_id)
);

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b
  ON auth_user_user_permissions (user_id);

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c
  ON auth_user_user_permissions (permission_id);

CREATE TABLE django_admin_log
(
  id              SERIAL                   NOT NULL
    CONSTRAINT django_admin_log_pkey
    PRIMARY KEY,
  action_time     TIMESTAMP WITH TIME ZONE NOT NULL,
  object_id       TEXT,
  object_repr     VARCHAR(200)             NOT NULL,
  action_flag     SMALLINT                 NOT NULL
    CONSTRAINT django_admin_log_action_flag_check
    CHECK (action_flag >= 0),
  change_message  TEXT                     NOT NULL,
  content_type_id INTEGER
    CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co
    REFERENCES django_content_type
    DEFERRABLE INITIALLY DEFERRED,
  user_id         INTEGER                  NOT NULL
    CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id
    REFERENCES auth_user
    DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX django_admin_log_content_type_id_c4bce8eb
  ON django_admin_log (content_type_id);

CREATE INDEX django_admin_log_user_id_c564eba6
  ON django_admin_log (user_id);

CREATE TABLE med_category
(
  id            SERIAL       NOT NULL
    CONSTRAINT med_category_pkey
    PRIMARY KEY,
  name          VARCHAR(128) NOT NULL,
  type_category VARCHAR(6)   NOT NULL
);

CREATE TABLE med_disease
(
  id          SERIAL         NOT NULL
    CONSTRAINT med_disease_pkey
    PRIMARY KEY,
  name        VARCHAR(128)   NOT NULL,
  avg_price   NUMERIC(12, 2) NOT NULL,
  category_id INTEGER        NOT NULL
    CONSTRAINT med_disease_category_id_404dd53a_fk_med_category_id
    REFERENCES med_category
    DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX med_disease_category_id_404dd53a
  ON med_disease (category_id);

CREATE TABLE med_diseaseanddoctor
(
  id         SERIAL         NOT NULL
    CONSTRAINT med_diseaseanddoctor_pkey
    PRIMARY KEY,
  price      NUMERIC(10, 2) NOT NULL,
  disease_id INTEGER        NOT NULL
    CONSTRAINT med_diseaseanddoctor_disease_id_ee501c44_fk_med_disease_id
    REFERENCES med_disease
    DEFERRABLE INITIALLY DEFERRED,
  doctor_id  INTEGER        NOT NULL
);

CREATE INDEX med_diseaseanddoctor_disease_id_ee501c44
  ON med_diseaseanddoctor (disease_id);

CREATE INDEX med_diseaseanddoctor_doctor_id_0c68648d
  ON med_diseaseanddoctor (doctor_id);

CREATE TABLE med_doctor
(
  id          SERIAL       NOT NULL
    CONSTRAINT med_doctor_pkey
    PRIMARY KEY,
  likes       INTEGER      NOT NULL,
  picture     VARCHAR(100) NOT NULL,
  category_id INTEGER      NOT NULL
    CONSTRAINT med_doctor_category_id_74ee9b56_fk_med_category_id
    REFERENCES med_category
    DEFERRABLE INITIALLY DEFERRED,
  hospital_id INTEGER      NOT NULL,
  user_id     INTEGER      NOT NULL
    CONSTRAINT med_doctor_user_id_key
    UNIQUE
    CONSTRAINT med_doctor_user_id_18b18627_fk_auth_user_id
    REFERENCES auth_user
    DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX med_doctor_category_id_74ee9b56
  ON med_doctor (category_id);

CREATE INDEX med_doctor_hospital_id_c6eb808a
  ON med_doctor (hospital_id);

ALTER TABLE med_diseaseanddoctor
  ADD CONSTRAINT med_diseaseanddoctor_doctor_id_0c68648d_fk_med_doctor_id
FOREIGN KEY (doctor_id) REFERENCES med_doctor
DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE med_hospital
(
  id           SERIAL       NOT NULL
    CONSTRAINT med_hospital_pkey
    PRIMARY KEY,
  name         VARCHAR(100) NOT NULL
    CONSTRAINT med_hospital_name_key
    UNIQUE,
  address      VARCHAR(100) NOT NULL
    CONSTRAINT med_hospital_address_key
    UNIQUE,
  phone_number VARCHAR(20)  NOT NULL,
  slug         VARCHAR(50)  NOT NULL
);

CREATE INDEX med_hospital_name_4ee64569_like
  ON med_hospital (name);

CREATE INDEX med_hospital_address_48e7e455_like
  ON med_hospital (address);

CREATE INDEX med_hospital_slug_537af03e
  ON med_hospital (slug);

CREATE INDEX med_hospital_slug_537af03e_like
  ON med_hospital (slug);

ALTER TABLE med_doctor
  ADD CONSTRAINT med_doctor_hospital_id_c6eb808a_fk_med_hospital_id
FOREIGN KEY (hospital_id) REFERENCES med_hospital
DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE registration_registrationprofile
(
  id             SERIAL      NOT NULL
    CONSTRAINT registration_registrationprofile_pkey
    PRIMARY KEY,
  activation_key VARCHAR(40) NOT NULL,
  user_id        INTEGER     NOT NULL
    CONSTRAINT registration_registrationprofile_user_id_key
    UNIQUE
    CONSTRAINT registration_registr_user_id_5fcbf725_fk_auth_user
    REFERENCES auth_user
    DEFERRABLE INITIALLY DEFERRED,
  activated      BOOLEAN     NOT NULL
);

CREATE TABLE registration_supervisedregistrationprofile
(
  registrationprofile_ptr_id INTEGER NOT NULL
    CONSTRAINT registration_supervisedregistrationprofile_pkey
    PRIMARY KEY
    CONSTRAINT registration_supervi_registrationprofile__0a59f3b2_fk_registrat
    REFERENCES registration_registrationprofile
    DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE django_session
(
  session_key  VARCHAR(40)              NOT NULL
    CONSTRAINT django_session_pkey
    PRIMARY KEY,
  session_data TEXT                     NOT NULL,
  expire_date  TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX django_session_session_key_c0390e0f_like
  ON django_session (session_key);

CREATE INDEX django_session_expire_date_a5c62663
  ON django_session (expire_date);

CREATE TABLE django_site
(
  id     SERIAL       NOT NULL
    CONSTRAINT django_site_pkey
    PRIMARY KEY,
  domain VARCHAR(100) NOT NULL
    CONSTRAINT django_site_domain_a2e37b91_uniq
    UNIQUE,
  name   VARCHAR(50)  NOT NULL
);

CREATE INDEX django_site_domain_a2e37b91_like
  ON django_site (domain);