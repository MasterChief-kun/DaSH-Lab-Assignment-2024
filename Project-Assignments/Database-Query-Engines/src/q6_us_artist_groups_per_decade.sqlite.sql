SELECT 
    CONCAT((begin_date_year / 10) * 10, 's') AS decade, 
    COUNT(*) AS group_count
FROM 
    artist a
JOIN 
    area ar ON a.area = ar.id
WHERE 
    ar.name = 'United States' 
    AND a.type = (SELECT id FROM artist_type WHERE name = 'Group')
    AND begin_date_year BETWEEN 1900 AND 2023
GROUP BY 
    (begin_date_year / 10) * 10
ORDER BY 
    (begin_date_year / 10) * 10 ASC;
