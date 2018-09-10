-- Table: public.tbl_crawl

-- DROP TABLE public.tbl_crawl;

CREATE TABLE public.tbl_crawl
(
    crawlid integer NOT NULL DEFAULT nextval('tbl_crawl_crawlid_seq'::regclass),
    crawlbezeichnung character varying COLLATE pg_catalog."default",
    CONSTRAINT tbl_crawl_pkey PRIMARY KEY (crawlid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tbl_crawl
    OWNER to postgres;

GRANT ALL ON TABLE public.tbl_crawl TO postgres;