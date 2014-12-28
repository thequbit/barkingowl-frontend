<%inherit file="base.mak"/>

    <style>

    </style>

    <div class="page-wrapper">
       <div class="page-title">
           <h1>Documents</h1>
       </div>
       <div class="page-contents">
           <div id="documents-select"><select class="wide tall"><option>Loading ...</option></select></div>
           <div style="width: 450px;">
           <a class="button" id="refresh-documents">Refresh</a>
           </div>
       </div>
    </div>

    <script>

        $(document).ready( function() {
            
            declare_page('documents');

            populate_documents();

            $('#refresh-documents').on( 'click', function( e ) {

                populate_documents();

            });

        });

        function populate_documents() {

           //$('#scraper-urls-select').html('Please wait, loading data ...');

            var url = "get_documents.json";
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'GET',
                data: {
                    owner_id: 1,
                    scraper_job_id: 1,
                },
                success: function( response ) {

                    console.log( response );

                    var html = "";

                    html += '<select class="wide tall" multiple>';
                    for(var i=0; i<response.documents.length; i++) {
                        html += '<option value="' + i + '">' + response.documents[i].url + '</option>';
                    }
                    html += '</select>';

                    $('#documents-select').html(html);

                    scraper_jobs = response.scraper_jobs;

                },
                error: function( response ) {

                }
            });
 
        }

    </script>
    
