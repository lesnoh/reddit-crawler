-- Table: public.tbl_submission

-- DROP TABLE public.tbl_submission;

CREATE TABLE public.tbl_submission
(
    id text COLLATE pg_catalog."default" NOT NULL,
    crawlid integer,
    index integer,
    title text COLLATE pg_catalog."default",
    ups integer,
    upvote_ratio double precision,
    author text COLLATE pg_catalog."default",
    timestamp_utc bigint,
    url text COLLATE pg_catalog."default",
    selftext text COLLATE pg_catalog."default",
    subreddit text COLLATE pg_catalog."default",
    is_reddit_media_domain boolean DEFAULT false,
    over_18 boolean DEFAULT false,
    is_self boolean DEFAULT false,
    stickied boolean DEFAULT false,
    CONSTRAINT tbl_themen_pkey PRIMARY KEY (id),
    CONSTRAINT tbl_themen_crawlid_fkey FOREIGN KEY (crawlid)
        REFERENCES public.tbl_crawl (crawlid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tbl_submission
    OWNER to postgres;

GRANT ALL ON TABLE public.tbl_submission TO postgres;

COMMENT ON COLUMN public.tbl_submission.over_18
    IS 'NSFW Posts';

COMMENT ON COLUMN public.tbl_submission.is_self
    IS 'Post mit Bezug auf eigenen Subreddit';

COMMENT ON COLUMN public.tbl_submission.stickied
    IS 'Post stickie im Subreddit (oberhalt anderer Submissions angeordnet)';

-- Index: id_idx

-- DROP INDEX public.id_idx;

CREATE INDEX id_idx
    ON public.tbl_submission USING btree
    (id COLLATE pg_catalog."default", crawlid)
    TABLESPACE pg_default;