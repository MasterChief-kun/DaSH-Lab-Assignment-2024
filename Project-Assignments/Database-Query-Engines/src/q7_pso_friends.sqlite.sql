SELECT DISTINCT a.name
FROM artist_credit_name acn
JOIN artist a ON acn.artist = a.id
WHERE acn.artist_credit IN (
    -- Subquery to find all artist credits that involve Pittsburgh Symphony Orchestra
    SELECT ac.id
    FROM artist_credit ac
    JOIN artist_credit_name acn2 ON ac.id = acn2.artist_credit
    JOIN artist a2 ON acn2.artist = a2.id
    WHERE a2.name = 'Pittsburgh Symphony Orchestra'
)
AND a.name != 'Pittsburgh Symphony Orchestra'
ORDER BY a.name ASC;

