SELECT 
    distinct(wt.name) AS WORK_TYPE,
    w.name AS WORK_NAME,
    LENGTH(w.comment) AS COMMENT_LENGTH,
    w.comment as 'COMMENT'
FROM 
    work w
JOIN 
    work_type wt ON w.type = wt.id
JOIN 
    (
        SELECT 
            type, 
            MAX(LENGTH(comment)) AS max_comment_length
        FROM 
            work
        WHERE 
            LENGTH(comment) > 0
        GROUP BY 
            type
    ) max_comments ON w.type = max_comments.type 
                  AND LENGTH(w.comment) = max_comments.max_comment_length
ORDER BY 
    wt.name ASC, 
    w.name ASC;
