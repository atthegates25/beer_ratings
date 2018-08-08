

# Get this figure: fig <- get_figure("kevindcannon", 4)
# Get this figure's data: data <- get_figure("kevindcannon", 4)$data
# Add data to this figure: p <- add_trace(p, x=c(4, 5), y=c(4, 5), kwargs=list(filename="American_Regular_IPAs", fileopt="extend"))

# Get figure documentation: https://plot.ly/r/get-requests/
# Add data documentation: https://plot.ly/r/file-options/

# You can reproduce this figure in R with the following code!

# Learn about API authentication here: https://plot.ly/r/getting-started
# Find your api_key here: https://plot.ly/settings/api

library(plotly)
trace1 <- list(
  hoverinfo = "text", 
  lat = rating_by_beer$lat,
  lon = rating_by_beer$lng,
    marker = list(
      autocolorscale = FALSE, 
      cauto = FALSE, 
      cmax = 5, 
      cmin = 2, 
      color = rating_by_beer$user_avg,
      colorbar = list(
        dtick = 5, 
        len = 0.75, 
        nticks = 5, 
        showexponent = "all", 
        tickfont = list(size = 12), 
        tickmode = "auto", 
        ticks = "outside", 
        title = "Rating", 
        titlefont = list(size = 16), 
        xanchor = "left"
      ), 
      colorscale = list(c(0, "rgb(190, 207, 182)"),list(0.35, "rgb(125, 178, 143)"),list(0.5, "rgb(40, 144, 126)"),list(0.6, "rgb(16, 125, 121)"),list(0.7, "rgb(24, 97, 108)"),list(1, "rgb(28, 71, 93)")), 
      line = list(
        color = "rgb(255, 255, 255)", 
        width = 0.5
      ), 
      showscale = TRUE, 
      size = rating_by_beer$num_ratings,
        sizemode = "area", 
        sizeref = 1.24125
    ), 
    mode = "markers", 
    name = "lng", 
    opacity = 1, 
    text = rating_by_beer$beer_name,
    type = "scattergeo"
)
data <- list(trace1)
layout <- list(
  autosize = TRUE, 
  font = list(size = 5), 
  geo = list(
    scope = "usa", 
    showcoastlines = TRUE, 
    showcountries = FALSE, 
    showlakes = FALSE, 
    showland = FALSE, 
    showrivers = FALSE, 
    subunitwidth = 0.5
  ), 
  hovermode = "closest", 
  paper_bgcolor = "rgb(255, 255, 255)", 
  showlegend = FALSE, 
  title = "Regular IPAs in America", 
  titlefont = list(size = 31)
)
p <- plot_ly()
p <- add_trace(p, hoverinfo=trace1$hoverinfo, lat=trace1$lat, latsrc=trace1$latsrc, lon=trace1$lon, lonsrc=trace1$lonsrc, marker=trace1$marker, mode=trace1$mode, name=trace1$name, opacity=trace1$opacity, text=trace1$text, textsrc=trace1$textsrc, type=trace1$type)
p <- layout(p, autosize=layout$autosize, font=layout$font, geo=layout$geo, hovermode=layout$hovermode, paper_bgcolor=layout$paper_bgcolor, showlegend=layout$showlegend, title=layout$title, titlefont=layout$titlefont)

p                              
                              