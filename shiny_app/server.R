
function(input, output, session) {

  
  
  ratings_by_beer_data = reactive({
    rating_by_beer %>%
      filter(., between(abv, input$beer_abv_slider[1], input$beer_abv_slider[2]),
             between(num_ratings, input$beer_num_ratings_slider[1], input$beer_num_ratings_slider[2]),
             between(user_avg, input$beer_rating_slider[1], input$beer_rating_slider[2]))
  })
  
  ratings_by_brewery_data = reactive({
    rating_by_beer %>%
      filter(., between(abv, input$brewery_abv_slider[1], input$brewery_abv_slider[2]),
             between(num_ratings, input$brewery_beer_num_ratings_slider[1], input$brewery_beer_num_ratings_slider[2]),
             between(user_avg, input$beer_rating_slider[1], input$beer_rating_slider[2])) %>%
      group_by(., brewery_name, lat, lng) %>%
      summarise(., total_num_ratings=sum(num_ratings), weighted_rating=sum(num_ratings*user_avg)/sum(num_ratings)) %>%
      mutate(., hover_text_by_brewery=paste(brewery_name, paste0("# Ratings: ", total_num_ratings),paste0("Weighted Rating: ", round(weighted_rating,2)),sep='\n')) %>%
      filter(., between(total_num_ratings, input$brewery_num_ratings_slider[1], input$brewery_num_ratings_slider[2]))
    
  })
  

  # plot for ratings by beer
  output$ratings_by_beer = renderPlotly({
    
                      data_df = ratings_by_beer_data()
    
                      trace1 <- list(
                        hoverinfo = "text", 
                        lat = data_df$lat,
                        lon = data_df$lng,
                        marker = list(
                          autocolorscale = FALSE, 
                          cauto = FALSE, 
                          cmax = 5, 
                          cmin = 2, 
                          color = data_df$user_avg,
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
                          size = data_df$num_ratings,
                          sizemode = "area", 
                          sizeref = 1.24125
                        ), 
                        mode = "markers", 
                        name = "lng", 
                        opacity = 1, 
                        text = data_df$hover_text_by_beer,
                        type = "scattergeo"
                      )
                      data <- list(trace1)
                      layout1 <- list(
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
                        showlegend = FALSE
                      )
                      plot_ly(hoverinfo=trace1$hoverinfo, lat=trace1$lat, lon=trace1$lon, marker=trace1$marker, mode=trace1$mode, name=trace1$name, opacity=trace1$opacity, text=trace1$text, type=trace1$type) %>%
                        layout(autosize=layout1$autosize, font=layout1$font, geo=layout1$geo, hovermode=layout1$hovermode, paper_bgcolor=layout1$paper_bgcolor, showlegend=layout1$showlegend, title=layout1$title, titlefont=layout1$titlefont)
                      
                      })

  # plot for ratings by brewery
  output$ratings_by_brewery = renderPlotly({
    
    data_df = ratings_by_brewery_data()
    
    trace1 <- list(
      hoverinfo = "text", 
      lat = data_df$lat,
      lon = data_df$lng,
      marker = list(
        autocolorscale = FALSE, 
        cauto = FALSE, 
        cmax = 5, 
        cmin = 2, 
        color = data_df$weighted_rating,
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
        size = data_df$total_num_ratings,
        sizemode = "area", 
        sizeref = 1.24125
      ), 
      mode = "markers", 
      name = "lng", 
      opacity = 1, 
      text = data_df$hover_text_by_brewery,
      type = "scattergeo"
    )
    data <- list(trace1)
    layout1 <- list(
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
      showlegend = FALSE
    )
    plot_ly(hoverinfo=trace1$hoverinfo, lat=trace1$lat, lon=trace1$lon, marker=trace1$marker, mode=trace1$mode, name=trace1$name, opacity=trace1$opacity, text=trace1$text, type=trace1$type) %>%
      layout(autosize=layout1$autosize, font=layout1$font, geo=layout1$geo, hovermode=layout1$hovermode, paper_bgcolor=layout1$paper_bgcolor, showlegend=layout1$showlegend, title=layout1$title, titlefont=layout1$titlefont)
    
  })

  # ratings scatter plot
  output$ratings_scatter = renderPlotly({
    
    data_df = rating_by_beer
    
    trace1 <- list(
      x = rating_by_beer$user_std,
      y = rating_by_beer$user_avg,
      marker = list(
        autocolorscale = FALSE, 
        cauto = TRUE, 
        cmax = 10.1, 
        cmin = 2.7, 
        color = rating_by_beer$abv,
        colorbar = list(title = "ABV"), 
        colorscale = list(c(0, "rgb(178, 10, 28)"),list(0.3, "rgb(230, 145, 90)"),list(0.4, "rgb(220, 170, 132)"),list(0.5, "rgb(190, 190, 190)"),list(0.65, "rgb(106, 137, 247)"),list(1, "rgb(5, 10, 172)")),
        line = list(width = 1), 
        opacity = 0.7, 
        reversescale = FALSE, 
        showscale = TRUE, 
        size = rating_by_beer$num_ratings,
        sizemode = "area", 
        sizeref = 1.24125, 
        symbol = "circle"
      ), 
      mode = "markers", 
      name = "user_avg", 
      text = rating_by_beer$hover_text_by_beer,
      type = "scatter"
    )
    data <- list(trace1)
    layout <- list(
      hovermode = "closest", 
      xaxis = list(
        autorange = TRUE, 
        range = c(0.202121141985, 0.736968859406), 
        title = "Rating StDev", 
        type = "linear"
      ), 
      yaxis = list(
        autorange = TRUE, 
        range = c(2.54846372206, 4.95052455089), 
        title = "Average Rating", 
        type = "linear"
      )
    )
    plot_ly(x=trace1$x, y=trace1$y, marker=trace1$marker, mode=trace1$mode, name=trace1$name, text=trace1$text, type=trace1$type, xsrc=trace1$xsrc, ysrc=trace1$ysrc) %>%
      layout(hovermode=layout$hovermode, xaxis=layout$xaxis, yaxis=layout$yaxis)

  })
  
    
}
