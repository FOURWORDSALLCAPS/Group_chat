CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    uuid              UUID      PRIMARY KEY       DEFAULT uuid_generate_v4() NOT NULL,
    username          VARCHAR(255) UNIQUE                                    NOT NULL,
    password          VARCHAR(255)                                           NOT NULL,
    first_name        VARCHAR(255)                                                   ,
    last_name         VARCHAR(255)                                                   ,
    middle_name       VARCHAR(255)                                                   ,
    birthday          DATE                                                           ,
    phone             VARCHAR(20)                                                    ,
    email             VARCHAR(255)                                                   ,
    active            BOOLEAN                     DEFAULT TRUE               NOT NULL,

    create_date       TIMESTAMP WITHOUT TIME ZONE DEFAULT now()                      ,
    update_date       TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

CREATE TABLE chats (
    uuid              UUID      PRIMARY KEY       DEFAULT uuid_generate_v4() NOT NULL,
    chat_name         VARCHAR(100)                                           NOT NULL,
    is_group_chat     BOOLEAN                     DEFAULT FALSE                      ,

    create_date       TIMESTAMP WITHOUT TIME ZONE DEFAULT now()                      ,
    update_date       TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

CREATE INDEX idx_chat_messages_names ON chat_messages (last_name, first_name, middle_name);

CREATE TABLE chat_users (
    uuid              UUID      PRIMARY KEY       DEFAULT uuid_generate_v4() NOT NULL,
    chat_uuid         UUID REFERENCES chats(uuid) ON DELETE CASCADE                  ,
    user_uuid         UUID REFERENCES users(uuid) ON DELETE CASCADE                  ,
    join_date         TIMESTAMP WITHOUT TIME ZONE DEFAULT now()                      ,

    create_date       TIMESTAMP WITHOUT TIME ZONE DEFAULT now()                      ,
    update_date       TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

CREATE TABLE chat_messages (
    uuid              UUID      PRIMARY KEY       DEFAULT uuid_generate_v4() NOT NULL,
    chat_uuid         UUID REFERENCES chats(uuid) ON DELETE CASCADE          NOT NULL,
    user_uuid         UUID REFERENCES users(uuid) ON DELETE                  SET NULL,
    text              TEXT                                                   NOT NULL,
    dispatch_date     TIMESTAMP WITHOUT TIME ZONE DEFAULT now()                      ,
    is_read           BOOLEAN                     DEFAULT FALSE                      ,

    create_date       TIMESTAMP WITHOUT TIME ZONE DEFAULT now()                      ,
    update_date       TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
