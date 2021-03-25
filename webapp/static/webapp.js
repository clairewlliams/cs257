// Claire Williams and Luisa Escosteguy

window.onload = initialize;

/**
 * Initializes all the data and runs when the window loads.
 */
function initialize() {
  [
    gamesTable,
    platformsTable,
    publishersTable,
    genresTable,
  ] = initializeDataTables();
  getGames(gamesTable);
  getPlatforms(platformsTable);
  getGenres(genresTable);
  getPublishers(publishersTable);
  setGamesFilters();
  openInsights();
}

/**
 * Opens the correct insights page based on the url. 
 */
function openInsights() {
  url = window.location.search;
  if (url.includes("platform")) {
    var platform = url.split("=")[1];
    platformInsights(platform);
  } else if (url.includes("genre")) {
    var genre = url.split("=")[1];
    genreInsights(genre);
  } else if (url.includes("publisher")) {
    var publisher = url.split("=")[1];
    publisherInsights(publisher);
  }
}

/**
 * Initializes the data tables. 
 * Returns a list of the data tables. 
 */
function initializeDataTables() {
  var gamesTable = $("#games").DataTable({
    order: [[1, "desc"]],
  });
  var platformsTable = $("#platforms").DataTable({
    info: false,
  });
  var publishersTable = $("#publishers").DataTable({
    info: false,
  });
  var genresTable = $("#genres").DataTable({
    info: false,
  });
  return [gamesTable, platformsTable, publishersTable, genresTable];
}

/**
 * Gets the API Base URL. 
 * Returns a string of the API Base URL.
 */
function getAPIBaseURL() {
  var baseURL =
    window.location.protocol +
    "//" +
    window.location.hostname +
    ":" +
    window.location.port +
    "/api";
  return baseURL;
}

/**
 * Adds data from gamesTable to the table on the home page. Catches errors and logs them.   
 * @param {*} gamesTable Games table that is initialized in initializeDataTables()
 */
function getGames(gamesTable) {
  var url = getAPIBaseURL() + "/games/";

  fetch(url, { method: "get" })
    .then((response) => response.json())

    .then(function (games) {
      for (var k = 0; k < games.length; k++) {
        var game = games[k];
        gamesTable.row
          .add([
            game["name"],
            game["sales"],
            "<a href='/publishers?publisher=" +
              game["publisher"] +
              "'>" +
              game["publisher"] +
              "</a>",
            "<a href='/platforms?platform=" +
              game["platform"] +
              "'>" +
              game["platform"] +
              "</a>",
            "<a href='/genres?genre=" +
              game["genre"] +
              "'>" +
              game["genre"] +
              "</a>",
            game["year"],
          ])
          .draw(false);
      }
    })

    .catch(function (error) {
      console.log(error);
    });
}

/**
 * Adds data from platformsTable to the list on the platforms page. 
 * Makes each name a link to that platform's insights. Catches errors and logs them.   
 * @param {*} platformsTable Platforms table that is initialized in initializeDataTables()
 */
function getPlatforms(platformsTable) {
  var url = getAPIBaseURL() + "/platforms/";

  fetch(url, { method: "get" })
    .then((response) => response.json())

    .then(function (platforms) {
      for (var k = 0; k < platforms.length; k++) {
        var platform = platforms[k];
        platformsTable.row
          .add([
            `<a href='#' onclick='platformInsights("${platform}")'>` +
              platform +
              "</a>",
          ])
          .draw(false);
      }
    })

    .catch(function (error) {
      console.log(error);
    });
}

/**
 * Adds data from genresTable to the list on the genres page. 
 * Makes each name a link to that genre's insights. Catches errors and logs them.   
 * @param {*} genresTable Genres table that is initialized in initializeDataTables()
 */
function getGenres(genresTable) {
  var url = getAPIBaseURL() + "/genres/";

  fetch(url, { method: "get" })
    .then((response) => response.json())

    .then(function (genres) {
      for (var k = 0; k < genres.length; k++) {
        var genre = genres[k];
        genresTable.row
          .add([
            `<a href='#' onclick='genreInsights("${genre}")'>` + genre + "</a>",
          ])
          .draw(false);
      }
    })

    .catch(function (error) {
      console.log(error);
    });
}

/**
 * Adds data from publishersTable to the list on the publishers page. 
 * Makes each name a link to that publisher's insights. Catches errors and logs them.   
 * @param {*} publishersTable Publishers table that is initialized in initializeDataTables()
 */
function getPublishers(publishersTable) {
  var url = getAPIBaseURL() + "/publishers/";

  fetch(url, { method: "get" })
    .then((response) => response.json())

    .then(function (publishers) {
      for (var k = 0; k < publishers.length; k++) {
        var publisher = publishers[k];
        publishersTable.row
          .add([
            `<a href='#' onclick='publisherInsights("${publisher}")'>` +
              publisher +
              "</a>",
          ])
          .draw(false);
      }
    })

    .catch(function (error) {
      console.log(error);
    });
}

/**
 * Creates genre insights by making a call to the API and using the top results.
 * Creates html to display insights and adds it to the div.
 * Does this twice for sales and user score. Catches errors and logs them.   
 * @param {*} genre Genre to display insights for.
 */
function genreInsights(genre) {
  var colors = [" bg-danger", " bg-warning", "", " bg-info", " bg-success"];
  var genreDiv = document.getElementById("genre_insight");

  var url = getAPIBaseURL() + "/games?genre=" + genre;

  fetch(url, { method: "get" })
    .then((response) => response.json())

    .then(function (games) {
      top_genre_games_by_sales = [];
      for (var k = 0; k < 5; k++) {
        var game = games[k];
        top_genre_games_by_sales.push(game);
      }
      var topGamesByGenre = `<h4>Top 5 ${genre} games by sales</h4>`;
      for (var k = 0; k < 5; k++) {
        topGamesByGenre += `<h4 class="small font-weight-bold">${top_genre_games_by_sales[k]["name"]} (${top_genre_games_by_sales[k]["platform"]}) <span
        class="float-right">${top_genre_games_by_sales[k]["sales"]} million sales</span></h4>
        <div class="progress mb-4">
        <div class="progress-bar${colors[k]}" role="progressbar" style="width: ${top_genre_games_by_sales[k]["sales"]}%"
        aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
        </div>`;
      }
      topGamesByGenre += `<p>Note: the full bar represents 100 million sales</p>`;
      if (genreDiv) {
        genreDiv.innerHTML =
          "<h2>" + genre + " Insights</h2>" + topGamesByGenre + "<hr>";
      }
      url = url += "&order_by=user_score";
      return fetch(url, { method: "get" });
    })

    .then((response) => response.json())

    .then(function (games_user_score) {
      top_genre_games_by_user_score = [];
      if (games_user_score.length >= 5) {
        for (var k = 0; k < 5; k++) {
          var game = games_user_score[k];
          top_genre_games_by_user_score.push(game);
        }
        var topGamesByGenreUserScore = `<h4>Top 5 ${genre} games by user score</h4>`;
        for (var k = 0; k < 5; k++) {
          if(top_genre_games_by_user_score[k]["user_score"] == null){ 
            topGamesByGenreUserScore += `<p>Sorry, this genre does not have enough user score data, try another one!</p>`
            break;
          }
          topGamesByGenreUserScore += `<h4 class="small font-weight-bold">${
            top_genre_games_by_user_score[k]["name"]
          } <span
          class="float-right">${
            top_genre_games_by_user_score[k]["user_score"]
          }/10</span></h4>
          <div class="progress mb-4">
          <div class="progress-bar${
            colors[k]
          }" role="progressbar" style="width: 
          ${
            10 * top_genre_games_by_user_score[k]["user_score"]
          }%"aria-valuenow="8" aria-valuemin="0" aria-valuemax="100"></div></div>`;
        }
        if (genreDiv) {
          genreDiv.innerHTML += topGamesByGenreUserScore;
        }
      }
    })
    .catch(function (error) {
      console.log(error);
    });
}

/**
 * Creates platform insights by making a call to the API and using the top results.
 * Creates html to display insights and adds it to the div.
 * Does this twice for sales and user score. Catches errors and logs them.   
 * @param {*} platform Platform to display insights for.
 */
function platformInsights(platform) {
  var colors = [" bg-danger", " bg-warning", "", " bg-info", " bg-success"];
  var platformDiv = document.getElementById("platform_insight");

  var url = getAPIBaseURL() + "/games/?platform=" + platform;

  fetch(url, { method: "get" })
    .then((response) => response.json())

    .then(function (games) {
      top_platform_games_by_sales = [];
      if (games.length >= 5) {
        for (var k = 0; k < 5; k++) {
          var game = games[k];
          top_platform_games_by_sales.push(game);
        }
        var topGamesByPlatform = `<h4>Top 5 ${platform} games by sales</h4>`;
        for (var k = 0; k < 5; k++) {
          topGamesByPlatform += `<h4 class="small font-weight-bold">${top_platform_games_by_sales[k]["name"]} (${top_platform_games_by_sales[k]["platform"]}) <span
        class="float-right">${top_platform_games_by_sales[k]["sales"]} million sales</span></h4>
        <div class="progress mb-4">
        <div class="progress-bar${colors[k]}" role="progressbar" style="width: ${top_platform_games_by_sales[k]["sales"]}%"
        aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
        </div>`;
        }
        topGamesByPlatform += `<p>Note: the full bar represents 100 million sales</p>`;
        if (platformDiv) {
          platformDiv.innerHTML =
            "<h2>" + platform + " Insights</h2>" + topGamesByPlatform + "<hr>";
        }
      } else {
        if (platformDiv) {
          platformDiv.innerHTML =
            "<h2>" +
            platform +
            " Insights</h2>" +
            "<p>Sorry, this platform does not have enough games, try another one!<p/>";
        }
      }
      url = url += "&order_by=user_score";
      return fetch(url, { method: "get" });
    })

    .then((response) => response.json())

    .then(function (games_user_score) {
      top_platform_games_by_user_score = [];
      if (games_user_score.length >= 5) {
        for (var k = 0; k < 5; k++) {
          var game = games_user_score[k];
          top_platform_games_by_user_score.push(game);
        }
        var topGamesByPlatformUserScore = `<h4>Top 5 ${platform} games by user score</h4>`;
        for (var k = 0; k < 5; k++) {
          if(top_platform_games_by_user_score[k]['user_score'] == null){
            topGamesByPlatformUserScore += `<p>Sorry, this platform does not have enough user score data, try another one!</p>`
            break;
          }
          topGamesByPlatformUserScore += `<h4 class="small font-weight-bold">${
            top_platform_games_by_user_score[k]["name"]
          } <span
          class="float-right">${
            top_platform_games_by_user_score[k]["user_score"]
          }/10</span></h4>
          <div class="progress mb-4">
          <div class="progress-bar${
            colors[k]
          }" role="progressbar" style="width: ${
            10 * top_platform_games_by_user_score[k]["user_score"]
          }%"
          aria-valuenow="8" aria-valuemin="0" aria-valuemax="100"></div></div>`;
        }
        if (platformDiv) {
          platformDiv.innerHTML += topGamesByPlatformUserScore;
        }
      }
    })

    .catch(function (error) {
      console.log(error);
    });
}

/**
 * Creates publisher insights by making a call to the API and using the top results.
 * Creates html to display insights and adds it to the div.
 * Does this twice for sales and user score. Catches errors and logs them.   
 * @param {*} publisher Publisher to display insights for.
 */
function publisherInsights(publisher) {
  var colors = [" bg-danger", " bg-warning", "", " bg-info", " bg-success"];
  var publisherDiv = document.getElementById("publisher_insight");

  var url = getAPIBaseURL() + "/games/?publisher=" + publisher;

  fetch(url, { method: "get" })
    .then((response) => response.json())

    .then(function (games) {
      top_publisher_games_by_sales = [];
      if (games.length >= 5) {
        for (var k = 0; k < 5; k++) {
          var game = games[k];
          top_publisher_games_by_sales.push(game);
        }
        var topGamesByPublisher = `<h4>Top 5 games ${publisher} by sales</h4>`;
        for (var k = 0; k < 5; k++) {
          topGamesByPublisher += `<h4 class="small font-weight-bold">${top_publisher_games_by_sales[k]["name"]} (${top_publisher_games_by_sales[k]["platform"]}) <span
          class="float-right">${top_publisher_games_by_sales[k]["sales"]} million sales</span></h4>
          <div class="progress mb-4">
          <div class="progress-bar${colors[k]}" role="progressbar" style="width: ${top_publisher_games_by_sales[k]["sales"]}%"
          aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div></div>`;
        }
        topGamesByPublisher += `<p>Note: the full bar represents 100 million sales</p>`;

        if (publisherDiv) {
          publisherDiv.innerHTML =
            "<h2>" +
            publisher +
            " Insights</h2>" +
            topGamesByPublisher +
            "<hr>";
        }
      } else {
        if (publisherDiv) {
          publisherDiv.innerHTML =
            "<h2>" +
            publisher +
            " Insights</h2>" +
            "<p>Sorry, this publisher does not have enough games, try another one!<p/>";
        }
      }
      url = url += "&order_by=user_score";
      return fetch(url, { method: "get" });
    })

    .then((response) => response.json())

    .then(function (games_user_score) {
      top_publisher_games_by_user_score = [];
      if (games_user_score.length >= 5) {
        for (var k = 0; k < 5; k++) {
          var game = games_user_score[k];
          top_publisher_games_by_user_score.push(game);
        }
        var topGamesByPublisherUserScore = `<h4>Top 5 ${publisher} games by user score</h4>`;
        for (var k = 0; k < 5; k++) {
          if(top_publisher_games_by_user_score[k]["user_score"] == null){
            topGamesByPublisherUserScore += `<p>Sorry, this publisher does not have enough user score data, try another one!</p>`
            break;
          }
          topGamesByPublisherUserScore += `<h4 class="small font-weight-bold">${
            top_publisher_games_by_user_score[k]["name"]
          } <span
          class="float-right">${
            top_publisher_games_by_user_score[k]["user_score"]
          }/10</span></h4>
          <div class="progress mb-4">
          <div class="progress-bar${
            colors[k]
          }" role="progressbar" style="width: ${
            10 * top_publisher_games_by_user_score[k]["user_score"]
          }%"
          aria-valuenow="8" aria-valuemin="0" aria-valuemax="100"></div></div>`;
        }

        if (publisherDiv) {
          publisherDiv.innerHTML += topGamesByPublisherUserScore;
        }
      } else {
        if (publisherDiv) {
          publisherDiv.innerHTML =
            "<h2>" +
            publisher +
            " Insights</h2>" +
            "<p>Sorry, this publisher does not have enough games, try another one!<p/>";
        }
      }
    })

    .catch(function (error) {
      console.log(error);
    });
}

/**
 * Adds filters to the homepage based on the top values in each catagory. Catches errors and logs them.    
 */
function setGamesFilters() {
  var url = getAPIBaseURL() + "/categories/";

  fetch(url, { method: "get" })
    .then((response) => response.json())

    .then(function (categories) {
      var content = `<h3 class="small font-weight-bold">Platforms</h3>`;
      var platforms = categories["platforms"];
      for (var k = 0; k < platforms.length; k++) {
        content += `<div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="platform-${platforms[k]}" value="${platforms[k]}">
        <label class="form-check-label" for="${platforms[k]}">${platforms[k]}</label>
      </div>`;
      }
      var platformsChecks = document.getElementById("platforms_checks");
      if (platformsChecks) {
        platformsChecks.innerHTML = content;
      }

      var content = `<h3 class="small font-weight-bold">Genres</h3>`;
      var genres = categories["genres"];
      for (var k = 0; k < genres.length; k++) {
        content += `<div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="genre-${genres[k]}" value="${genres[k]}">
        <label class="form-check-label" for="${genres[k]}">${genres[k]}</label>
      </div>`;
      }
      var genresChecks = document.getElementById("genres_checks");
      if (genresChecks) {
        genresChecks.innerHTML = content;
      }

      var content = `<h3 class="small font-weight-bold">Publishers</h3>`;
      var publishers = categories["publishers"];
      for (var k = 0; k < publishers.length; k++) {
        content += `<div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="publisher-${publishers[k]}" value="${publishers[k]}">
        <label class="form-check-label" for="${publishers[k]}">${publishers[k]}</label>
      </div>`;
      }
      var publishersChecks = document.getElementById("publishers_checks");
      if (publishersChecks) {
        publishersChecks.innerHTML = content;
      }
    })

    .catch(function (error) {
      console.log(error);
    });
}

/**
 * Filters results based on user specification and updates the data table on the home page.
 * Reverts to full table when nothing is selected.    
 */
function filterGames() {
  var tableHeader = document.getElementById("table_header");
  var gamesFilterTable = $("#games").DataTable();

  gamesFilterTable.search("").columns().search("").draw();

  (platforms = []), (publishers = []), (genres = []);
  $("input[type=checkbox]:checked").each(function () {
    var value = $(this).attr("id");
    if (value.includes("publisher")) {
      publishers.push(value.split("-")[1]);
    } else if (value.includes("platform")) {
      platforms.push(value.split("-")[1]);
    } else {
      genres.push(value.split("-")[1]);
    }
  });

  if (
    tableHeader &&
    (platforms.length > 0 || publishers.length > 0 || genres.length > 0)
  ) {
    tableHeader.innerHTML = "Filter results";
    if (publishers.length > 0)
      gamesFilterTable
        .column(2)
        .search(publishers.join("|"), true, false)
        .draw();
    if (platforms.length > 0)
      gamesFilterTable
        .column(3)
        .search(platforms.join("|"), true, false)
        .draw();
    if (genres.length > 0)
      gamesFilterTable.column(4).search(genres.join("|"), true, false).draw();
  } else if (tableHeader) {
    tableHeader.innerHTML = "Top 500 games by global sales ranking";
  }
}
