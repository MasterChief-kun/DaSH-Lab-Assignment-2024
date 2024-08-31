SELECT 
    r.name AS release_name, 
    ac.name AS artist_name, 
    ri.date_year AS release_year
FROM 
    release r
JOIN 
    artist_credit ac ON r.artist_credit = ac.id
JOIN 
    release_info ri ON r.id = ri.release
JOIN 
    medium me ON r.id = me.release
JOIN
    medium_format mf ON me.format = mf.id
WHERE
    mf.name LIKE 'Cassette'
ORDER BY 
    ri.date_year DESC, 
    ri.date_month DESC, 
    ri.date_day DESC, 
    r.name ASC, 
    ac.name ASC
LIMIT 10;
