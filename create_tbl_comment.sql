-- Table: public.tbl_comment

-- DROP TABLE public.tbl_comment;

CREATE TABLE public.tbl_comment
(
    cindex text COLLATE pg_catalog."default" NOT NULL,
    submissionid text COLLATE pg_catalog."default",
    score integer,
    author text COLLATE pg_catalog."default",
    body text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    "timestamp" bigint,
    parent_id text COLLATE pg_catalog."default",
    crawlid integer,
    CONSTRAINT tbl_kommentare_pkey PRIMARY KEY (cindex),
    CONSTRAINT tbl_kommentare_themenid_fkey FOREIGN KEY (submissionid)
        REFERENCES public.tbl_submission (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tbl_comment
    OWNER to postgres;

GRANT ALL ON TABLE public.tbl_comment TO postgres;

-- Index: submissionsid_idx

-- DROP INDEX public.submissionsid_idx;

CREATE INDEX submissionsid_idx
    ON public.tbl_comment USING btree
    (submissionid COLLATE pg_catalog."default")
    TABLESPACE pg_default;