-- MIN oder MAX Kommentardatum einer Submission
SELECT 
		tbl_submission.id, tbl_submission.author,
		to_timestamp(timestamp_utc) at time zone 'UTC' as STIME,
        url,title,
        to_timestamp(timestamp) at time zone 'UTC' as CTIME,
        tbl_comment.author,body 
FROM 
	tbl_submission
INNER JOIN 
	tbl_comment 
    ON (tbl_comment.submissionid = tbl_submission.id)
WHERE 
-- 	tbl_submission.id = '97-42-t3_7lifir'
    tbl_submission.id like '97-10-t3_7lkfaf'
GROUP BY 
	tbl_submission.author,tbl_submission.timestamp_utc,url,title,tbl_comment.author,body,tbl_submission.id,CTIME
--ORDER BY CTIME ASC LIMIT 1;
ORDER BY CTIME DESC LIMIT 100;

-- Kommentare pro Submission
SELECT 
		tbl_submission.id, tbl_submission.url,
        to_timestamp(timestamp_utc) at time zone 'UTC' as STIME,
        tbl_submission.title, 
        COUNT(tbl_comment.cindex) as NoComments
FROM 
	tbl_submission
INNER JOIN 
	tbl_comment 
    ON (tbl_comment.submissionid = tbl_submission.id)
GROUP BY 
	tbl_submission.id, tbl_submission.id, tbl_submission.title, STIME
ORDER BY NoComments DESC LIMIT 100;


-- Kommentare pro Submission innerhalb der X Stunden
SELECT 
		tbl_submission.id, tbl_submission.url,
        to_timestamp(timestamp_utc) at time zone 'UTC' as STIME,
        tbl_submission.title, 
        COUNT(tbl_comment.cindex) as NoComments
FROM 
	tbl_submission
INNER JOIN 
	tbl_comment 
    ON (tbl_comment.submissionid = tbl_submission.id)
WHERE
	timestamp <= timestamp_utc+2*3600
GROUP BY 
	tbl_submission.id, tbl_submission.id, tbl_submission.title, STIME
ORDER BY NoComments DESC 
--LIMIT 100;


-- Alle Posts von Crawl 142
SELECT COUNT(*) FROM public.tbl_submission where crawlid=142;
    
-- Alle Post anzeigen, die zu Reddit Media verlinken	
SELECT COUNT(*)	AS Reddit_Media FROM public.tbl_submission
    WHERE is_reddit_media_domain = true and is_self = false and crawlid=142;;
-- Alle Post anzeigen, die auf extern verlinken	
SELECT COUNT(*)	AS Externe_Posts FROM public.tbl_submission
    WHERE is_reddit_media_domain = false and is_self = false and crawlid=142 and url not like '%reddit.com/r%';
SELECT COUNT(*)	AS Externe_Posts FROM public.tbl_submission
    WHERE is_reddit_media_domain = false and is_self = false and crawlid=142 and url like '%reddit.com/r%';

COPY (
SELECT url FROM public.tbl_submission
    WHERE is_reddit_media_domain = false and is_self = false and crawlid=142
    ) TO 'C:\temp\externeurls.csv' WITH CSV DELIMITER ';';
    
-- Alle Posts anzeigen, die reine Textbeiträge sind
SELECT COUNT(*)	AS Nur_Text FROM public.tbl_submission
    WHERE is_self = true and crawlid=142;

-- Alle Post anzeigen, die Stickie sind	
SELECT *	FROM public.tbl_submission
    WHERE stickied=true;
    
-- Alle Crawls anzeigen	
SELECT
	*
    FROM tbl_crawl;
   
--- Gesamtanzahl der Kommentare und Anzahl der Kommentare nach X Stunden Pro Submission und prozentuales Verhältnis zwischen beiden---
SELECT 
    *, 
    round((c.NoCommentsX::numeric/c.NoCommentsGesamt::numeric*100),2) as Prozent_in_X_Stunden
		FROM
			(SELECT 
                tbl_submission.id, tbl_submission.url,
                to_timestamp(timestamp_utc) at time zone 'UTC' as STIME,
                tbl_submission.title, 
                COUNT(tbl_comment.cindex) as NoCommentsGesamt,
                b.NoCommentsX
             --   ,SUM(tbl_comment.score) as CommentsScore,
             --   b.CommentsXScore
            FROM 
                tbl_submission 
                INNER JOIN (
                    -- Kommentare pro Submission innerhalb der x Stunden
                    SELECT 
                            tbl_submission.id,
                            COUNT(tbl_comment.cindex) as NoCommentsX,
                            SUM(tbl_comment.score) as CommentsXScore
                    FROM 
                        tbl_submission
                    INNER JOIN 
                        tbl_comment 
                        ON (tbl_comment.submissionid = tbl_submission.id)
                    WHERE
                        timestamp <= timestamp_utc+24*3600
                    GROUP BY 
                        tbl_submission.id
                ) as b ON (tbl_submission.id = b.id)
                INNER JOIN
                tbl_comment ON (tbl_comment.submissionid = b.id)
            WHERE
                tbl_submission.crawlid=142
            GROUP BY 
                tbl_submission.id, tbl_submission.id, tbl_submission.title, STIME, b.NoCommentsX,b.CommentsXScore
            -- Virale Posts analysisieren (Mehr als 100 Gesamtkommentare)
                HAVING COUNT(tbl_comment.cindex) > 10
            ORDER BY NoCommentsGesamt DESC) as c
ORDER BY Prozent_in_X_Stunden
LIMIT 1000


-- Ausgabe in Textdatei

COPY (
    SELECT 
        *, 
        round((c.NoCommentsX::numeric/c.NoCommentsGesamt::numeric*100),2) as Prozent_in_X_Stunden
            FROM
                (SELECT 
                    tbl_submission.id,
                    to_timestamp(timestamp_utc) at time zone 'UTC' as STIME,
                    COUNT(tbl_comment.cindex) as NoCommentsGesamt,
                    b.NoCommentsX
                FROM 
                    tbl_submission 
                    INNER JOIN (
                        -- Kommentare pro Submission innerhalb der x Stunden
                        SELECT 
                                tbl_submission.id,
                                COUNT(tbl_comment.cindex) as NoCommentsX,
                                SUM(tbl_comment.score) as CommentsXScore
                        FROM 
                            tbl_submission
                        INNER JOIN 
                            tbl_comment 
                            ON (tbl_comment.submissionid = tbl_submission.id)
                        WHERE
                            timestamp <= timestamp_utc+1*3600
                        GROUP BY 
                            tbl_submission.id
                    ) as b ON (tbl_submission.id = b.id)
                    INNER JOIN
                    tbl_comment ON (tbl_comment.submissionid = b.id)
                WHERE
                    tbl_submission.crawlid=142
                GROUP BY 
                    tbl_submission.id, STIME, b.NoCommentsX,b.CommentsXScore
                -- Virale Posts analysisieren (Mehr als 100 Gesamtkommentare)
                --    HAVING COUNT(tbl_comment.cindex) > 10
                ORDER BY NoCommentsGesamt DESC) as c
    ORDER BY Prozent_in_X_Stunden
    --LIMIT 1000
) TO 'C:\temp\ausgabe1h.csv' WITH CSV DELIMITER ';';


--- Uhrzeit und Anzahl der Posts für Pivot Excel (Sekunden werden verworfen)
SELECT
	1 as default_value,
    date_trunc('minute',to_timestamp(timestamp_utc) at time zone 'UTC') as STIME
FROM
	tbl_submission
WHERE
	tbl_submission.crawlid=142
ORDER BY STIME DESC
    -- Zusammenfassung pro Minute
    SELECT
        COUNT(*) as Anzahl,
        date_trunc('minute',to_timestamp(timestamp_utc) at time zone 'UTC') as STIME
    FROM
        tbl_submission
    WHERE
        tbl_submission.crawlid=142
    GROUP BY STIME
    ORDER BY STIME DESC

    -- Zusammenfassung pro Stunde
    SELECT
        COUNT(*) as Anzahl,
        date_trunc('hour',to_timestamp(timestamp_utc) at time zone 'UTC') as STIME
    FROM
        tbl_submission
    WHERE
        tbl_submission.crawlid=142
    GROUP BY STIME
    ORDER BY STIME DESC
    


-- Auswertung Posts und Kommentare pro Wochentag / Kalenderwoche
-- The day of the week (0 - 6; Sunday is 0) 
-- Submissions pro Wochentag
    SELECT
        COUNT(*) as Anzahl,
        -- date_trunc('day',to_timestamp(timestamp_utc) at time zone 'UTC') as STIME
        EXTRACT (DOW FROM to_timestamp(timestamp_utc) at time zone 'UTC') as STIME
    FROM
        tbl_submission
    WHERE
        tbl_submission.crawlid=133
        --tbl_submission.crawlid=119
    GROUP BY STIME
    ORDER BY STIME DESC
-- Kommentare pro Wochentag    
    SELECT
        COUNT(*) as Anzahl,
        EXTRACT (DOW FROM to_timestamp(timestamp) at time zone 'UTC') as STIME
    FROM
        tbl_comment
    WHERE
        tbl_comment.crawlid=119
    GROUP BY STIME
    ORDER BY STIME DESC    
    
-- Submissions pro Kalenderwoche
    SELECT
        COUNT(*) as Anzahl,
        -- date_trunc('day',to_timestamp(timestamp_utc) at time zone 'UTC') as STIME
        EXTRACT (WEEK FROM to_timestamp(timestamp_utc) at time zone 'UTC') as STIME
    FROM
        tbl_submission
    WHERE
        tbl_submission.crawlid=133
    GROUP BY STIME
    ORDER BY STIME DESC
--  Kommentare pro Kalenderwoche

SELECT
    COUNT(*) as Anzahl,
        EXTRACT (WEEK FROM to_timestamp(timestamp) at time zone 'UTC') as STIME
    FROM
        tbl_comment
    WHERE
        tbl_comment.crawlid=119
    GROUP BY STIME
    ORDER BY STIME DESC    

-- Kommentare über den Zeitverlauf
    SELECT
        COUNT(*) as Anzahl,
        date_trunc('day',to_timestamp(timestamp) at time zone 'UTC') as STIME
    FROM
        tbl_comment
    WHERE
        tbl_comment.crawlid=142
    GROUP BY STIME
    ORDER BY STIME DESC

-- --- Durchschnitts Kontroversität pro Subreddit
-- SELECT * 
-- 	FROM
--         (SELECT
--             subreddit,
--             crawlid,
--             AVG(upvote_ratio) as avg_score,
--             MIN(upvote_ratio),
--             MAX(upvote_ratio),
--             COUNT(id) as Anzahl_Submissions
--         FROM
--             tbl_submission
--         GROUP BY crawlid,subreddit
--         ORDER BY avg_score DESC) as b
--     WHERE b.Anzahl_Submissions >100

-- MIT HAVING
SELECT COUNT(*) FROM
	        (SELECT
                subreddit,
                crawlid,
                CAST(AVG(upvote_ratio) AS DECIMAL(10,3)) as avg_score,
                MIN(upvote_ratio),
                MAX(upvote_ratio),
                COUNT(id) as Anzahl_Submissions
            FROM
                tbl_submission
            WHERE crawlid = 142
            GROUP BY crawlid,subreddit
            HAVING COUNT(id) > 30
            ORDER BY avg_score DESC) as b
WHERE b.avg_score = 1

--- TOP Subreddits eines Crawls
SELECT
    subreddit,
    COUNT(id) as Anzahl_Submissions
FROM
    tbl_submission
WHERE
	crawlid = 142
GROUP BY subreddit
ORDER BY Anzahl_Submissions DESC
LIMIT 10

--- TOP Kommentare pro Subreddits eines Crawls
SELECT
    subreddit,
    COUNT(cindex) as Anzahl_Kommentare
FROM
    tbl_comment 
    INNER JOIN tbl_submission ON (tbl_comment.submissionid = tbl_submission.id)
WHERE
	tbl_comment.crawlid = 142
GROUP BY subreddit
ORDER BY Anzahl_Kommentare DESC
LIMIT 10

-- --- BRAINFUCK ohne title ---
-- SELECT 
--     tbl_submission.id, tbl_submission.url,
--     to_timestamp(timestamp_utc) at time zone 'UTC' as STIME,
--     COUNT(tbl_comment.cindex) as NoCommentsGesamt,
--     b.NoCommentsX
--     --,ROUND((b.NoCommentsX/NoCommentsGesamt), 2)
-- FROM 
-- 	tbl_submission 
--     INNER JOIN (
--        	-- Kommentare pro Submission innerhalb der x Stunden
--         SELECT 
--                 tbl_submission.id,
--                 COUNT(tbl_comment.cindex) as NoCommentsX
--         FROM 
--             tbl_submission
--         INNER JOIN 
--             tbl_comment 
--             ON (tbl_comment.submissionid = tbl_submission.id)
--         WHERE
--             timestamp <= timestamp_utc+1*3600
--         GROUP BY 
--             tbl_submission.id
--     ) as b ON (tbl_submission.id = b.id)
--     INNER JOIN
--     tbl_comment ON (tbl_comment.submissionid = b.id)
-- WHERE
-- --            timestamp <= timestamp_utc+72*3600
-- 	tbl_submission.crawlid=101 
-- GROUP BY 
-- 	tbl_submission.id, tbl_submission.id, STIME, b.NoCommentsX
-- ORDER BY NoCommentsGesamt DESC

-- Anzahl Submission IDs:
SELECT 
		COUNT (DISTINCT tbl_submission.id)
        --DISTINCT tbl_submission.id, to_timestamp(timestamp_utc) at time zone 'UTC' as STIME
FROM 
	tbl_submission
WHERE
    tbl_submission.crawlid=142

-- Anzahl Kommentare IDs:
SELECT 
		COUNT (DISTINCT tbl_comment.cindex)
        --DISTINCT tbl_comment.cindex
FROM 
	tbl_comment
WHERE
    tbl_comment.crawlid=142 
LIMIT 10



-- Alles löschen!
--delete from tbl_comment;
--delete from tbl_submission;
--delete from tbl_crawl;
