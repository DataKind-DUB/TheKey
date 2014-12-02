-- Created by Vertabelo (http://vertabelo.com)
-- Script type: create
-- Scope: [tables, references, sequences, views, procedures]
-- Generated at Mon Dec 01 21:57:09 UTC 2014




-- tables
-- Table: activity_ref_lk
CREATE TABLE activity_ref_lk (
    id integer    NOT NULL ,
    name integer    NOT NULL ,
    CONSTRAINT activity_ref_lk_pk PRIMARY KEY (id)
);

-- Table: contact_lk
CREATE TABLE contact_lk (
    id integer    NOT NULL ,
    name integer    NOT NULL ,
    CONSTRAINT contact_lk_pk PRIMARY KEY (id)
);

-- Table: disability_ref_lk
CREATE TABLE disability_ref_lk (
    id integer    NOT NULL ,
    name integer    NOT NULL ,
    CONSTRAINT disability_ref_lk_pk PRIMARY KEY (id)
);

-- Table: ethnicity_ref_lk
CREATE TABLE ethnicity_ref_lk (
    id integer    NOT NULL ,
    name integer    NOT NULL ,
    CONSTRAINT ethnicity_ref_lk_pk PRIMARY KEY (id)
);

-- Table: `group`
CREATE TABLE `group` (
    id integer    NOT NULL ,
    organisation_id integer    NOT NULL ,
    name varchar(255)    NOT NULL ,
    CONSTRAINT group_pk PRIMARY KEY (id)
);

-- Table: group_member
CREATE TABLE group_member (
    id integer    NOT NULL ,
    is_male integer    NOT NULL ,
    postcode varchar(255)    NOT NULL ,
    ethnicity_ref integer    NOT NULL ,
    disability_ref integer    NOT NULL ,
    CONSTRAINT group_member_pk PRIMARY KEY (id)
);

-- Table: group_project
CREATE TABLE group_project (
    id integer    NOT NULL ,
    group_id integer    NOT NULL ,
    contact_id integer    NOT NULL ,
    licence_holder_id integer    NOT NULL ,
    stage_id integer    NOT NULL ,
    key_fund_stage_id integer    NOT NULL ,
    registered_date datetime    NOT NULL ,
    CONSTRAINT group_project_pk PRIMARY KEY (id)
);

-- Table: group_project_free_text
CREATE TABLE group_project_free_text (
    id integer    NOT NULL ,
    group_project_id integer    NOT NULL ,
    group_project_name varchar(255)    NOT NULL ,
    group_project_description varchar(255)    NOT NULL ,
    how_group_formed varchar(255)    NOT NULL ,
    how_often_group_meets varchar(255)    NOT NULL ,
    whats_done_previously varchar(255)    NOT NULL ,
    other_factors varchar(255)    NOT NULL ,
    other_comments varchar(255)    NOT NULL ,
    participant_explanation varchar(255)    NOT NULL ,
    conflict_explanation varchar(255)    NOT NULL ,
    issue_tackled varchar(255)    NOT NULL ,
    panel_description varchar(255)    NOT NULL ,
    panel_how_group_developed_idea varchar(255)    NOT NULL ,
    panel_skills_development varchar(255)    NOT NULL ,
    panel_how_young_people_change varchar(255)    NOT NULL ,
    panel_new_experiences varchar(255)    NOT NULL ,
    panel_how_benefitted varchar(255)    NOT NULL ,
    facilitator_eval_summary varchar(255)    NOT NULL ,
    facilitator_skill_support varchar(255)    NOT NULL ,
    facilitator_how_group_benefitted varchar(255)    NOT NULL ,
    facilitator_hints_tips varchar(255)    NOT NULL ,
    registered_date datetime    NOT NULL ,
    CONSTRAINT group_project_free_text_pk PRIMARY KEY (id)
);

-- Table: group_project_member
CREATE TABLE group_project_member (
    id integer    NOT NULL ,
    group_member_id integer    NOT NULL ,
    group_project_id integer    NOT NULL ,
    CONSTRAINT group_project_member_pk PRIMARY KEY (id)
);

-- Table: group_project_member_skill
CREATE TABLE group_project_member_skill (
    id integer    NOT NULL ,
    group_project_member_id integer    NOT NULL ,
    is_before integer    NOT NULL ,
    is_after integer    NOT NULL ,
    timestamp timestamp    NOT NULL ,
    CONSTRAINT group_project_member_skill_pk PRIMARY KEY (id)
);

-- Table: group_project_member_skill_wheel_item
CREATE TABLE group_project_member_skill_wheel_item (
    id integer    NOT NULL ,
    group_project_member_skill_wheel_id integer    NOT NULL ,
    reference_id integer    NOT NULL ,
    value integer    NOT NULL ,
    CONSTRAINT group_project_member_skill_wheel_item_pk PRIMARY KEY (id)
);

-- Table: group_project_type
CREATE TABLE group_project_type (
    _id integer    NOT NULL ,
    group_project_id integer    NOT NULL ,
    activity_ref integer    NOT NULL ,
    CONSTRAINT group_project_type_pk PRIMARY KEY (id)
);

-- Table: key_fund_stage_lk
CREATE TABLE key_fund_stage_lk (
    id integer    NOT NULL ,
    name integer    NOT NULL ,
    CONSTRAINT key_fund_stage_lk_pk PRIMARY KEY (id)
);

-- Table: licence_holder_lk
CREATE TABLE licence_holder_lk (
    _id integer    NOT NULL ,
    name integer    NOT NULL ,
    CONSTRAINT licence_holder_lk_pk PRIMARY KEY (id)
);

-- Table: organisation_lk
CREATE TABLE organisation_lk (
    id integer    NOT NULL ,
    name integer    NOT NULL ,
    postcode integer    NOT NULL ,
    CONSTRAINT organisation_lk_pk PRIMARY KEY (id)
);

-- Table: skill_ref_lk
CREATE TABLE skill_ref_lk (
    id integer    NOT NULL ,
    name integer    NOT NULL ,
    CONSTRAINT skill_ref_lk_pk PRIMARY KEY (id)
);

-- Table: stage_lk
CREATE TABLE stage_lk (
    id integer    NOT NULL ,
    name integer    NOT NULL ,
    CONSTRAINT stage_lk_pk PRIMARY KEY (id)
);





-- foreign keys
-- Reference:  group_group_project (table: group_project)


ALTER TABLE group_project ADD CONSTRAINT group_group_project FOREIGN KEY group_group_project (group_id)
    REFERENCES `group` (id);
-- Reference:  group_member_disability_ref_lk (table: group_member)


ALTER TABLE group_member ADD CONSTRAINT group_member_disability_ref_lk FOREIGN KEY group_member_disability_ref_lk (disability_ref)
    REFERENCES disability_ref_lk (id);
-- Reference:  group_member_ethnicity_ref_lk (table: group_member)


ALTER TABLE group_member ADD CONSTRAINT group_member_ethnicity_ref_lk FOREIGN KEY group_member_ethnicity_ref_lk (ethnicity_ref)
    REFERENCES ethnicity_ref_lk (id);
-- Reference:  group_organisation (table: `group`)


ALTER TABLE `group` ADD CONSTRAINT group_organisation FOREIGN KEY group_organisation (organisation_id)
    REFERENCES organisation_lk (id);
-- Reference:  group_project_contact_lk (table: group_project)


ALTER TABLE group_project ADD CONSTRAINT group_project_contact_lk FOREIGN KEY group_project_contact_lk (contact_id)
    REFERENCES contact_lk (id);
-- Reference:  group_project_free_text_group_project (table: group_project_free_text)


ALTER TABLE group_project_free_text ADD CONSTRAINT group_project_free_text_group_project FOREIGN KEY group_project_free_text_group_project (group_project_id)
    REFERENCES group_project (id);
-- Reference:  group_project_key_fund_stage_lk (table: group_project)


ALTER TABLE group_project ADD CONSTRAINT group_project_key_fund_stage_lk FOREIGN KEY group_project_key_fund_stage_lk (key_fund_stage_id)
    REFERENCES key_fund_stage_lk (id);
-- Reference:  group_project_licence_holder (table: group_project)


ALTER TABLE group_project ADD CONSTRAINT group_project_licence_holder FOREIGN KEY group_project_licence_holder (licence_holder_id)
    REFERENCES licence_holder_lk (id);
-- Reference:  group_project_member_group_member (table: group_project_member)


ALTER TABLE group_project_member ADD CONSTRAINT group_project_member_group_member FOREIGN KEY group_project_member_group_member (group_member_id)
    REFERENCES group_member (id);
-- Reference:  group_project_member_group_project (table: group_project_member)


ALTER TABLE group_project_member ADD CONSTRAINT group_project_member_group_project FOREIGN KEY group_project_member_group_project (group_project_id)
    REFERENCES group_project (id);
-- Reference:  group_project_member_skill_wheel_group_project_member (table: group_project_member_skill)


ALTER TABLE group_project_member_skill ADD CONSTRAINT group_project_member_skill_wheel_group_project_member FOREIGN KEY group_project_member_skill_wheel_group_project_member (group_project_member_id)
    REFERENCES group_project_member (id);
-- Reference:  group_project_member_skill_wheel_item_group_project_member_skill_wheel (table: group_project_member_skill_wheel_item)


ALTER TABLE group_project_member_skill_wheel_item ADD CONSTRAINT group_project_member_skill_wheel_item_group_project_member_skill_wheel FOREIGN KEY group_project_member_skill_wheel_item_group_project_member_skill_wheel (group_project_member_skill_wheel_id)
    REFERENCES group_project_member_skill (id);
-- Reference:  group_project_member_skill_wheel_item_skill_ref_lk (table: group_project_member_skill_wheel_item)


ALTER TABLE group_project_member_skill_wheel_item ADD CONSTRAINT group_project_member_skill_wheel_item_skill_ref_lk FOREIGN KEY group_project_member_skill_wheel_item_skill_ref_lk (reference_id)
    REFERENCES skill_ref_lk (id);
-- Reference:  group_project_stage_lk (table: group_project)


ALTER TABLE group_project ADD CONSTRAINT group_project_stage_lk FOREIGN KEY group_project_stage_lk (stage_id)
    REFERENCES stage_lk (id);
-- Reference:  group_project_type_activity_ref_lk (table: group_project_type)


ALTER TABLE group_project_type ADD CONSTRAINT group_project_type_activity_ref_lk FOREIGN KEY group_project_type_activity_ref_lk (activity_ref)
    REFERENCES activity_ref_lk (id);
-- Reference:  group_project_type_group_project (table: group_project_type)


ALTER TABLE group_project_type ADD CONSTRAINT group_project_type_group_project FOREIGN KEY group_project_type_group_project (group_project_id)
    REFERENCES group_project (id);



-- End of file.

