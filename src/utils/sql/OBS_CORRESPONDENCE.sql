SELECT * FROM observations_exploded AS
WITH main AS (
	-- alive_female_andata
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'F' AS sex,'AND' AS direction,'AD' AS state,alive_female_andata AS n
	FROM observations_observationdetail
	WHERE alive_female_andata IS NOT NULL
	UNION ALL
	-- alive_female_ritorno
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'F' AS sex,'RIT' AS direction,'AD' AS state,alive_female_ritorno AS n
	FROM observations_observationdetail
	WHERE alive_female_ritorno IS NOT NULL
	UNION ALL
	-- alive_female_indet
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'F' AS sex,'IND' AS direction,'AD' AS state,alive_female_indet AS n
	FROM observations_observationdetail
	WHERE alive_female_indet IS NOT NULL
	UNION ALL
	-- alive_male_ritorno
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'M' AS sex,'RIT' AS direction,'AD' AS state,alive_male_ritorno AS n
	FROM observations_observationdetail
	WHERE alive_male_ritorno IS NOT NULL
	UNION ALL
	-- alive_male_andata
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'M' AS sex,'AND' AS direction,'AD' AS state,alive_male_andata AS n
	FROM observations_observationdetail
	WHERE alive_male_andata IS NOT NULL
	UNION ALL
	-- alive_male_indet
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'M' AS sex,'IND' AS direction,'AD' AS state,alive_male_indet AS n
	FROM observations_observationdetail
	WHERE alive_male_indet IS NOT NULL
	UNION ALL
	-- alive_indet_andata
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'IND' AS sex,'AND' AS direction,'AD' AS state,alive_indet_andata AS n
	FROM observations_observationdetail
	WHERE alive_indet_andata IS NOT NULL
	UNION ALL
	-- alive_indet_ritorno
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'IND' AS sex,'RIT' AS direction,'AD' AS state,alive_indet_ritorno AS n
	FROM observations_observationdetail
	WHERE alive_indet_ritorno IS NOT NULL
	UNION ALL
	-- alive_indet_indet
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	TRUE AS life,'IND' AS sex,'IND' AS direction,'AD' AS state,alive_indet_indet AS n
	FROM observations_observationdetail
	WHERE alive_indet_indet IS NOT NULL
	UNION ALL
	-- dead_female
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	FALSE AS life,'F' AS sex,NULL AS direction,'AD' AS state,dead_female AS n
	FROM observations_observationdetail
	WHERE dead_female IS NOT NULL
	UNION ALL
	-- dead_male
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	FALSE AS life,'M' AS sex,NULL AS direction,'AD' AS state,dead_male AS n
	FROM observations_observationdetail
	WHERE dead_male IS NOT NULL
	UNION ALL
	-- dead_indet
	SELECT specie_id,session_id,created_by_id,created,modified,modified_by_id,
	FALSE AS life,'IND' AS sex,NULL AS direction,'AD' AS state,dead_indet AS n
	FROM observations_observationdetail
	WHERE dead_indet IS NOT NULL
)
SELECT * FROM main 
ORDER BY created,life,sex,direction,state,n