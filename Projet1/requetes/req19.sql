19| Quels sont les acteurs ayant joué le rôle de James Bond, et dans quels films ?
SELECT primaryName, primaryTitle FROM name_basics JOIN title_principals ON name_basics.nconst=title_principals.nconst JOIN title_basics ON title_principals.tconst=title_basics.tconst WHERE characters LIKE '%James Bond%';