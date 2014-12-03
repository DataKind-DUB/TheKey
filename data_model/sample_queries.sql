--
-- Retrieves project details and sample text content for a project where text is non null
--
select g._id, o.name "Org",
       g.name "Group", 
       gp.stage,
       gp.registered,
       -- these text fields correspond to idea/project description; see more in group_project_free_text table.
       gt.group_project_description, 
       gt.panel_how_group_developed_idea, 
       gt.how_group_formed,
       gt.whats_done_previously,
       gt.other_factors
from "organisation" o,
     "group" g,
     "group_project" gp,
     "group_project_free_text" gt
where g.organisation_id=o._id
and gp.group_id = g._id
and gt.group_project_id = gp._id
and gt.group_project_description is not null and gt.group_project_description <> ""
order by gp.registered desc

--
-- What project types get the most/least assignments?
--
select count(gpt.name) "Assignments", (count(gpt.name)+0.0)/tot.total "Ratio", name "Type"
from 
  group_project_type gpt,
  (select count(*) as "total" from group_project_type) tot
group by gpt.name
order by count(gpt.name) desc

--
-- there can be more than 1 assignment per project, so how does the category-project assignment looks like?
--
select assigned_categories, count(*) "projects"
from
  (select count(name) "assigned_categories"
   from group_project_type
   group by group_project_id)
group by assigned_categories
order by assigned_categories
