9| Qui a écrit le scénario du film Taxi sorti en 1998 ?
SELECT primaryName FROM name_basics WHERE primaryProfession LIKE '%writer%' AND nconst IN (SELECT writers FROM title_writers WHERE tconst IN (SELECT tconst FROM title_basics WHERE primaryTitle = 'Taxi' and startYear=1998));