library(shiny)
library(data.table)
library(tidyverse)
library(plotly)

rating_by_beer = fread('data/Final_US_Beer_Ratings_By_Beer.txt',sep='\t')

rating_by_beer = rating_by_beer %>% 
  mutate(., hover_text_by_beer = paste(brewery_name,beer_name,paste0("ABV: ", abv,"%"), paste0("# Ratings: ", num_ratings),paste0("Rating: ", round(user_avg,2)),sep='\n'))


min_abv = min = min(rating_by_beer$abv)
max_abv = max((rating_by_beer$abv))

min_num_beer_ratings = min = min(rating_by_beer$num_ratings)
max_num_beer_ratings = max((rating_by_beer$num_ratings))

rating_by_brewery = rating_by_beer %>% 
                      group_by(., brewery_name, lat, lng) %>%
                      summarise(., total_num_ratings=sum(num_ratings), weighted_rating=sum(num_ratings*user_avg)/sum(num_ratings))

min_num_brewery_ratings = min(rating_by_brewery$total_num_ratings)
max_num_brewery_ratings = max(rating_by_brewery$total_num_ratings)


steps <- list(
  list(args = list("marker.color", "red"), 
       label = "Red", 
       method = "restyle", 
       value = "1"
  ),
  list(args = list("marker.color", "green"), 
       label = "Green", 
       method = "restyle", 
       value = "2"
  ),
  list(args = list("marker.color", "blue"), 
       label = "Blue", 
       method = "restyle", 
       value = "3"
  )
)