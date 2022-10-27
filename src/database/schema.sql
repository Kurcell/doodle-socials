-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    uid integer NOT NULL DEFAULT nextval('users_uid_seq'::regclass),
    username character varying(200) COLLATE pg_catalog."default" NOT NULL,
    screenname character varying(200) COLLATE pg_catalog."default" NOT NULL,
    password character varying(200) COLLATE pg_catalog."default" NOT NULL,
    email character varying(200) COLLATE pg_catalog."default" NOT NULL,
    createdat timestamp with time zone,
    CONSTRAINT users_pkey PRIMARY KEY (uid),
    CONSTRAINT users_username_key UNIQUE (username)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to gxsfadrohqpnss;


-- Table: public.post

-- DROP TABLE IF EXISTS public.post;

CREATE TABLE IF NOT EXISTS public.post
(
    pid integer NOT NULL DEFAULT nextval('post_pid_seq'::regclass),
    content character varying(500) COLLATE pg_catalog."default" NOT NULL,
    user_id integer,
    CONSTRAINT post_pkey PRIMARY KEY (pid),
    CONSTRAINT post_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.post
    OWNER to gxsfadrohqpnss;


-- Table: public.canvas

-- DROP TABLE IF EXISTS public.canvas;

CREATE TABLE IF NOT EXISTS public.canvas
(
    cid integer NOT NULL DEFAULT nextval('canvas_cid_seq'::regclass),
    instructions character varying(500) COLLATE pg_catalog."default" NOT NULL,
    post_id integer,
    CONSTRAINT canvas_pkey PRIMARY KEY (cid),
    CONSTRAINT canvas_post_id_fkey FOREIGN KEY (post_id)
        REFERENCES public.post (pid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.canvas
    OWNER to gxsfadrohqpnss;


-- Table: public.following

-- DROP TABLE IF EXISTS public.following;

CREATE TABLE IF NOT EXISTS public.following
(
    following_id integer NOT NULL DEFAULT nextval('following_following_id_seq'::regclass),
    followee_uid integer NOT NULL,
    followed_uid integer NOT NULL,
    CONSTRAINT following_pkey PRIMARY KEY (following_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.following
    OWNER to gxsfadrohqpnss;


-- Table: public.blocking

-- DROP TABLE IF EXISTS public.blocking;

CREATE TABLE IF NOT EXISTS public.blocking
(
    blocking_id integer NOT NULL DEFAULT nextval('blocking_blocking_id_seq'::regclass),
    blockee_uid integer NOT NULL,
    blocked_uid integer NOT NULL,
    CONSTRAINT blocking_pkey PRIMARY KEY (blocking_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.blocking
    OWNER to gxsfadrohqpnss;

