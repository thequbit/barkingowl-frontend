<!doctype html>
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html>
<head>

    <link rel="icon" type="image/png" href="media/favicon.png">

    <title>BarkingOwl - Document Discovery Tool</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'> 
    
    <link rel="stylesheet" href="static/foundation/css/foundation.css" />
    <link rel="stylesheet" href="static/foundation/css/foundation-datepicker.css" />
    
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
    
    <style>
    
        body {
            font-family: 'Lato', sans-serif !important;
        }
        
        div.title-bar {
            margin-top: 100px;
            margin-bottom: 25px;
            background-color: #008CBA;
        }
        
        div.title-bar h1 {
            color: white;
            font-size: 400% !important;
        }
        
        div.title-bar h1 small {
            padding-left: 5px;
            color: lightblue;
        }
        
        div.input-bar {
            margin-bottom: 25px;
        }
        
        div.input-bar input {
            width: 50%;
            padding: 10px;
            font-size: 100%;
        }
        
        div.input-bar button {
            margin-left: 25px;
            margin-right: 25px;
        }
    
    </style>

</head>
<body>

    <div class="title-bar"> 
        <div class="row">
            <div class="large-12 columns">
                <h1>BarkingOwl<small>Document Discovery Tool</small></h1>
            </div>
        </div>
    </div>
    
    <script src="static/foundation/js/vendor/jquery.js"></script>
   
    <div class="input-bar">
        <div class="row">
             <div class="large-12 columns">
                <h4>URL to scrape:</h4>
                <input id="scrape-url"></input>
                <button onclick="getDocuments();">Get Documents</button>
                or
                <button onclick="startScraping();">Start Scraping</button>
            </div>
        </div>
    </div>
    
    <div class="row">
         <div class="large-12 columns">
            <h4>
                Documents
            </h4>
            <table id="doc-list">
                <tr>
                    <th width="95">Date</th>
                    <th width="150">Root URL</th>
                    <th width="150">Page Title</th>
                    <th width="150">Document Title</th>
                    <th>Document URL</th>
                </tr>
            </table>
        </div>
    </div>
    
    <script src="static/foundation/js/foundation/foundation.js"></script>
    
    <script src="static/foundation/js/foundation/foundation.dropdown.js"></script>

    <script src="static/foundation/js/vendor/modernizr.js"></script>

    <script src="static/foundation/js/foundation-datepicker.js"></script>

    <script>
        $(document).foundation({
            dropdown: {
                // specify the class used for active dropdowns
                active_class: 'open'
            }
        });
    </script>
    
    <script>
    
        var documentIds = [];
    
        function getDocuments() {
            
            var url = "get_documents.json?url=" + encodeURIComponent($('#scrape-url').val());
            $.getJSON(url, function(data) {
                
                var retHtml = $('#doc-list').html();
                
                for(int i=0; i<data.docs.length; i++) {
                    
                    if ( documentIds.indexOf(data.docs[i].id) == 0 ) {
                        
                        var rowString = "" +
                            "<tr>" +
                            "<td>__date__</td>" +
                            "<td>__root_url__</td>" +
                            "<td>__page_title__</td>" +
                            "<td>__doc_title__</td>" +
                            "<td><a src=\"__doc_url__\">__doc_url__</a></td>" +
                            "</tr>";
                            
                        rowString.replace('__date__', data.docs[i]['document']['found_datetime']);
                        rowString.replace('__root_url__', data.docs[i]['url_data']['target_url']);
                        rowString.replace('__page_title__', data.docs[i]['document']['url']['page_title']);
                        rowString.replace('__doc_title__', data.docs[i]['document']['url']['tag_text']);
                        rowString.replace('__doc_url__', data.docs[i]['document']['url']['url']);
                        
                        retHtml += rowString;
                        
                        documentIds.push(data.docs[i].id);
                        
                    }
                    
                }
                
                $('#doc-list').html(retHtml);
                
            });
            
        }
        
        function getDocuments() {
            
            var url = "start_scraping.json?url=" + encodeURIComponent($('#scrape-url').val());
            $.getJSON(url, function(data) {
                
                // things.
                
            });
            
        }
        
        //setInterval(populateDocuments, 5000);
    
    </script>
        
</body>
</html>
