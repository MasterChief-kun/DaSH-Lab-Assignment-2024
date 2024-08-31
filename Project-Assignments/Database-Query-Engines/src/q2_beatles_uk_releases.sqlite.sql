SELECT 
    distinct(r.name) AS album_name, 
    ri.date_year AS release_year 
FROM 
    release r
JOIN 
    artist_credit ac ON r.artist_credit = ac.id
JOIN 
    artist a ON ac.id = a.id
JOIN 
    medium m ON r.id = m.release
JOIN 
    medium_format mf ON m.format = mf.id
JOIN 
    release_info ri ON r.id = ri.release
JOIN 
    area ar ON ri.area = ar.id
WHERE 
    a.name = 'The Beatles'
    AND mf.name = '12" Vinyl'
    AND ar.name = 'United Kingdom'
    AND ri.date_year <= 1970
ORDER BY 
    ri.date_year ASC;
