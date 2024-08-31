SELECT 
    a.name AS artist_name, 
    ri.date_month, 
    COUNT(r.id) AS release_count
FROM 
    artist a
JOIN 
    artist_credit ac ON a.id = ac.id
JOIN 
    release r ON ac.id = r.artist_credit
JOIN 
    release_info ri ON r.id = ri.release
WHERE 
    a.name LIKE 'Elvis%' 
    AND a.type = (SELECT id FROM artist_type WHERE name = 'Person')
    AND ri.date_month IS NOT NULL
GROUP BY 
    a.id, a.name, ri.date_month
ORDER BY 
    release_count DESC, 
    a.name ASC, 
    ri.date_month ASC;

