

fluidPage(
  navbarPage(
    'American IPAs',
    tabPanel(
      'Breweries',
      sidebarLayout(
        sidebarPanel(
          width=2,
          
          sliderInput("brewery_num_ratings_slider", label = h3("# Brewery Ratings"), min = min_num_brewery_ratings, 
                      max = max_num_brewery_ratings, value = c(min_num_brewery_ratings, max_num_brewery_ratings)),
          sliderInput("brewery_abv_slider", label = h4("Abv"), min = min_abv, max = max_abv,
                      value = c(min_abv, max_abv)),
          sliderInput("brewery_beer_num_ratings_slider", label = h4("# Beer Ratings"), min = min_num_beer_ratings, max = max_num_beer_ratings,
                      value = c(min_num_beer_ratings, max_num_beer_ratings))
        ),
        mainPanel(
          titlePanel(h2("American IPA Breweries", align='center')),
          plotlyOutput("ratings_by_brewery", height="800px")
        )
      )
    ),
    tabPanel(
      'IPAs By Location',
      sidebarLayout(
        sidebarPanel(
          width=2,

          sliderInput("beer_abv_slider", label = h3("Abv"), min = min_abv, max = max_abv,
                      value = c(min_abv, 5.5)),
          sliderInput("beer_num_ratings_slider", label = h3("# Ratings"), min = min_num_beer_ratings, max = max_num_beer_ratings,
                      value = c(min_num_beer_ratings, max_num_beer_ratings)),
          sliderInput("beer_rating_slider", label = h3("Rating"), min = 2, max = 5, step=0.05,
                      value = c(2, 5))
          
        ),
        mainPanel(
          titlePanel(h2("American IPAs", align='center')),
          plotlyOutput("ratings_by_beer", height="800px")
        )
      )
    ),
    tabPanel(
      'IPAs Ratings',
      sidebarLayout(
        sidebarPanel(
          width=2
        ),
        mainPanel(
          titlePanel(h2("IPA Ratings", align='center')),
          plotlyOutput("ratings_scatter", height="800px")
        )
      )
    )
  )
)
