12| Quelle sont les 5 comédies romantiques les mieux notées ?
SELECT originalTitle FROM title_basics JOIN title_ratings ON title_basics.tconst=title_ratings.tconst WHERE title_basics.genres LIKE '%Comedy%' AND title_basics.genres LIKE '%Romance%' ORDER BY title_ratings.averageRating DESC LIMIT 5; 