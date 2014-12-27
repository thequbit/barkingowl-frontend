<html>
<head>

    <meta charset="utf-8" />

    <link rel="stylesheet" href="static/css/site.css" />

<!--    <link rel="stylesheet" href="static/foundation/css/foundation.css" /> -->
    
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>

</head>
<body>

    <script src="static/js/jquery-1.11.2.min.js"></script>
   
    <div class="site-wrapper">

        <div class="nav-wrapper">

        <div class="nav-info">

            <br/>
            Barking Owl<br/>
            Front End

        </div>

        <div class="nav-break"></div>

        <div class="nav-link" id="nav-container-home">
        <a href="/home" id="nav-link-home">Home</a>
        </div>

        <div class="nav-break"></div>

        <div class="nav-link" id="nav-container-target-urls">
        <a href="/target-urls" id="nav-link-target-urls">Target URLs</a>
        </div>

        <div class="nav-link" id="nav-container-scraper-jobs">
        <a href="/scraper-jobs" id="nav-link-scraper-jobs">Scraper Jobs</a>
        </div>

        <div class="nav-link" id="nav-container-link-scrapers">
        <a href="/scrapers" id="nav-link-scrapers">Scrapers</a>
        </div>

        <div class="nav-link" id="nav-container-scraper-runs">
        <a href="/scraper-runs" id="nav-link-scraper-runs">Scraper Runs</a>
        </div>

        <div class="nav-link" id="nav-container-documents">
        <a href="/documents" id="nav-link-documents">Documents</a>
        </div>

        <div class="nav-break"></div>

        <div class="nav-link" id="nav-container-settings">
        <a href="/settings" id="nav-link-settings">Settings</a>
        </div>

        <div class="nav-link" id="nav-container-logout">
        <a href="/logout" id="nav-link-logout">Logout</a>
        </div>

    </div>

   
        ${self.body()}

    </div>
    

    <script>

        var pages = [
            'home',
            'target-urls',
            'scraper-jobs',
            'scrapers',
            'scraper-runs',
            'documents',
            'settings',
            'logout',
        ]

        function declare_page(page_name) {

            console.log('declaring page: ' + page_name);

            $('#nav-container-' + page_name).addClass('nav-link-selected');

        }

    </script>

</body>
</html>
