<html>
<head>

    <meta charset="utf-8" />

    <link rel="stylesheet" href="static/foundation/css/foundation.css" />
    
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>

</head>
<body>

    <script src="static/foundation/js/vendor/jquery.js"></script>
   
    <div class="site-wrapper">
   
        <!--
        <div class="row">
             <div class="large-12 columns">
        -->
                ${self.body()}
        <!--
            </div>
        </div>
        -->

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

</body>
</html>