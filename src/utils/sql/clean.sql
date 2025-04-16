-- change species for old observation table
UPDATE observations_observation SET specie_id=(
SELECT id FROM observations_specie WHERE specie='Rana dalmatina')
FROM observations_session,observations_site,observations_specie
WHERE session_id=observations_session.id AND
observations_site.id=observations_session.site_id AND 
observations_observation.specie_id=observations_specie.id AND
specie='Rana temporaria' AND observations_site.name='Lago di Loppio';
-- change species for new observation table
UPDATE observations_observationdetail SET specie_id=(
SELECT id FROM observations_specie WHERE specie='Rana dalmatina')
FROM observations_session,observations_site,observations_specie
WHERE session_id=observations_session.id AND
observations_site.id=observations_session.site_id AND 
observations_observationdetail.specie_id=observations_specie.id AND
specie='Rana temporaria' AND observations_site.name='Lago di Loppio';
-- siti con particolare specie
SELECT DISTINCT observations_site.* FROM 
observations_session,observations_site,observations_specie
WHERE session_id=observations_session.id AND
observations_site.id=observations_session.site_id AND 
observations_observationdetail.specie_id=observations_specie.id AND
specie='Rana temporaria';