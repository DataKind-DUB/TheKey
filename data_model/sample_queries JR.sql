SELECT
gp.stage_id
,sl.name
,gp.registered_date
,gp.group_id
--,gpt._id
,gpt.group_project_id
--,gpt.activity_ref
--,ar._id
,ar.name
--,gft.group_project_id		as UAT_group_proj_id
,gft.group_project_name	as UAT_group_proj_name
,gft.group_project_description	as UAT_group_proj_desc
,gft.registered_date		as UAT_group_proj_reg_date
FROM "group_project" gp
LEFT JOIN stage_lk sl ON sl._id = gp.stage_id
--LEFT 
INNER JOIN group_project_type gpt ON gpt._id = gp.group_id
LEFT JOIN activity_ref_lk ar ON ar._id = gpt.activity_ref
--LEFT 
INNER JOIN "group_project_free_text_anon" gft ON gft.group_project_id = gp.group_id
--LEFT JOIN groupprojecttext_temp gtt ON gtt.group_project_id = gf._id
WHERE gp.registered_date >= '2011-10-01'
--AND sl._id = '6'
--AND gft.group_project_description IS NOT NULL
--AND gft.group_project_description <> ""
--AND gft.group_project_name LIKE '%cinema%'
--AND gft.group_project_description LIKE '%sport%'

ORDER BY gp.registered_date DESC