UPDATE observations_session
SET effort=((COALESCE(array_length(string_to_array(volontari_unregistered, ','),1),0)+n)*EXTRACT(epoch from observations_session.end-observations_session.begin)/60)::integer
FROM 
(
SELECT observations_session.id AS session_id,COALESCE(n,0) AS n FROM observations_session
LEFT JOIN 
(
	
	SELECT session_id,COUNT(*) AS n FROM observations_session_volontari WHERE session_id IS NOT NULL
	GROUP BY session_id ORDER BY session_id ASC

) q ON q.session_id=id
) secondary
WHERE observations_session.id=secondary.session_id
AND ended_next_day IS false;
UPDATE observations_session
SET effort=((COALESCE(array_length(string_to_array(volontari_unregistered, ','),1),0)+n)*EXTRACT(epoch from (observations_session.end+date+interval '1' day-observations_session.begin)::time)/60)::integer
FROM 
(
SELECT observations_session.id AS session_id,COALESCE(n,0) AS n FROM observations_session
LEFT JOIN 
(
	
	SELECT session_id,COUNT(*) AS n FROM observations_session_volontari WHERE session_id IS NOT NULL
	GROUP BY session_id ORDER BY session_id ASC

) q ON q.session_id=id
) secondary
WHERE observations_session.id=secondary.session_id
AND ended_next_day IS true;