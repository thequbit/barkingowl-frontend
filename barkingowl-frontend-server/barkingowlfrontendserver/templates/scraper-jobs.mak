<%inherit file="base.mak"/>

    <style>

    </style>

    <div class="page-wrapper">
       <div class="page-title">
           <h1>Scraper Jobs</h1>
       </div>
       <div class="page-contents">
           <div style="float: left;">
               <h2>New Scraper Job</h2>
               <div class="indent">
                   <label class="medium">Target URL:</label>
                   <div id="target-urls-container">
                       <select class="wide"><option>Loading ...</option></select>
                   </div>
                   <label class="medium">Name:</label><input class="wide" id="new-name"></input>
                   <label class="medium">Notes:</label><textarea class="wide very-short" id="new-notes"></textarea>
                   <label class="medium">Frequency</label>
                   <select class="wide">
                       <option value="24">Daily</option>
                       <option value="48">Every Other Day</option>
                       <option value="168">Once a Week</option>
                       <option value="336">Every Two Weeks</option>
                       <option value="1350">Once a Month</option>
                   </select>
                   <label class="medium">Document Type</label>
                   <div id="document-types-container">
                       <select class="wide"><option>Loading ...</option></select>
                   </div>
                   <div style="height: 22px;"></div>
                   <a class="button" href="#submit-scraper-job" id="submit-scraper-job">Submit New Scraper Job</a>
                   <label class="status" id="submit-status"></label>
               </div>
           </div>
           <h2>Existing Scraper Jobs</h2>
           <div style="float: left;">
               <div style="float: left;">
                   <div class="indent">
                       <div style="height: 26px"></div>
                       <div id="scraper-urls-select"></div>
                   </div>
               </div>
               <div style="float: left;" id="target-url-current" style="display: None;">
                   <div class="indent">
                       <div id="target-url-info"></div>
                   </div>
               </div>
           </div>
       </div>
    </div>

    <script>

        var target_urls = [];
        var document_types = [];
        var scraper_jobs = [];

        $(document).ready( function() {
            
            declare_page('scraper-urls');

            populate_target_urls();

            populate_document_types(); 

            populate_scraper_jobs();

            $('#scraper-urls-select').on( 'click', function( e ) {
                show_target_url( $(e.target).val() );    
            });

            $('#submit-scraper-job').on( 'click', function( e ) {
                submit_scraper_job( );
            });

        });

        function freq_decode( freq ) {
            var freq_text = '';
            switch( freq ) {
                case 24:
                    freq_text = "Daily";
                    break;
                case 48:
                    freq_text = "Every Other Day";
                    break;
                case 168:
                    freq_text = "Once a Week";
                    break;
                case 336:
                    freq_text = "Every two Weeks";
                    break;
                case 1350:
                    freq_text = "Once a Month";
                    break;
                default:
                    if ( freq == 1 ) {
                        freq_text += 'Every hour';
                    } else {
                       freq_text = "Every " + freq + " hours";
                    }
                    break;
            };
            return freq_text;
        }

        function update_status( status ) {

            if ( status == '' ) {
                $('#submit-status').html('');
                $('#submit-status').hide();
            } else {
                $('#submit-status').html( status );
                $('#submit-status').show();
            }

        }

        function populate_scraper_jobs() {
           
            $('#scraper-urls-select').html('Please wait, loading data ...');

            var url = "get_scraper_jobs.json"; 
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'GET',
                data: {
                    owner_id: 1,
                },
                success: function( response ) {

                    console.log( response );

                    var html = "";

                    html += '<select class="wide tall" multiple>';
                    for(var i=0; i<response.scraper_jobs.length; i++) {
                        html += '<option value="' + i + '">' + response.scraper_jobs[i].name + '</option>';
                    }
                    html += '</select>';

                    $('#scraper-urls-select').html(html);

                    scraper_jobs = response.scraper_jobs;

                },
                error: function( response ) {
                    
                }
            });
            
        }

        function populate_target_urls() {

            //$('#target-urls-select').html('Please wait, loading data ...');

            var url = "get_target_urls.json";
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'GET',
                data: {
                    owner_id: 1,
                },
                success: function( response ) {
                    var html = "";

                    html += '<select id="target-urls" class="wide">';
                    for(var i=0; i<response.target_urls.length; i++) {
                        html += '<option value="' + i + '">' + response.target_urls[i].title + '</option>';
                    }
                    html += '</select>';

                    $('#target-urls-container').html(html);

                    target_urls = response.target_urls;

                },
                error: function( response ) {

                }
            });

        }

        function populate_document_types() {

            //$('#document-types-select').html('Please wait, loading data ...');

            console.log('getting documents');

            var url = "get_document_types.json";
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'GET',
                data: {
                    owner_id: 1,
                },
                success: function( response ) {

                    console.log('docs:');
                    console.log( response );

                    var html = "";

                    html += '<select id="document-types" class="wide">';
                    for(var i=0; i<response.document_types.length; i++) {
                        html += '<option value="' + i + '">' + response.document_types[i].description + '</option>';
                    }
                    html += '</select>';

                    $('#document-types-container').html(html);

                    document_types = response.document_types;

                },
                error: function( response ) {

                }
            });

        }


        function show_target_url( index ) {

            $('#target-url-current').show();

            var html = "";
            
            html += '<label class="medium">Target URL:</label>';
            html += '<input class="wide" readonly value="' + scraper_jobs[index].target_url.url + '"></input>';

            html += '<label class="medium">Name:</label>';
            html += '<input class="wide" readonly value="' + scraper_jobs[index].name + '"></input>';

            html += '<label class="medium">Notes:</label>';
            html += '<textarea class="wide short" readonly value="' + scraper_jobs[index].notes + '"></textarea>';

            html += '<label class="medium">Frequency:</label>';
            html += '<input class="wide" readonly value="' + freq_decode(scraper_jobs[index].frequency) + '"></input>';

            html += '<label class="medium">Document Type:</label>';
            html += '<input class="wide" readonly value="' + scraper_jobs[index].document_type.name + '"></input>';

            $('#target-url-info').html(html);

        }

        function submit_scraper_job() {

            update_status('Please wait ...');
          
            var url = "create_scraper_job.json"; 
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'POST',
                data: {
                    owner_id: 1,
                    target_url_id: target_urls[parseInt($('#target-urls option:selected').val())].id,
                    name: $('#new-name').val(),
                    notes: $('#new-notes').val(),
                    link_level: -1,
                    document_type_id: document_types[parseInt($('#document-types option:selected').val())].id,
                    enabled: true,
                },
                success: function( response ) {
                    if ( response.success == true ) {
                        update_status('<b style="color: darkgreen">Scraper Job added successfully.</b>');

                        populate_scraper_jobs();
                    } else {
                        update_status('<b style="color: darkred">An error occured.  Scraper Job not created.</b>')
                    }
                },
                error: function( response ) {
                    update_status('<b style="color: darkred">An error occured.  Scraper Job not created.</b>');
                },
            })
 
        }

    </script>
    
