<%inherit file="base.mak"/>

    <style>

    </style>

    <div class="page-wrapper">
       <div class="page-title">
           <h1>Target URLs</h1>
       </div>
       <div class="page-contents">
           <div style="float: left;">
               <h2>New Target URL</h2>
               <div class="indent">
                   <label class="medium">URL:</label><input class="wide" id="new-url"></input>
                   <label class="medium">Title:</label><input class="wide" id="new-title"></input>
                   <label class="medium">Description:</label><textarea class="wide tall" id="new-description"></textarea>
                   <div style="height: 22px;"></div>
                       <a class="button" href="#submit-target-url" id="submit-target-url">Submit New Target URL</a>
                       <label class="status" id="submit-status"></label>
               </div>
           </div>
           <div class="second-column">
               <h2>Existing Target URLs</h2>
               <div class="indent">
                   <div style="height: 26px"></div>
                   <div id="target-urls-select"></div>
                   <!--
                   <select class="wide tall" multiple>
                       <option>TimDuffy.Me</option>
                       <option>Village of Scottsville, NY</option>
                   </select>
                   -->
               </div>
           </div>
           <div class="third-column" id="target-url-current" style="display: None;">
               <!--<h2>Selected Target URL</h2>-->
               <div style="height: 65px;"></div>
               <div class="indent">
                   <div id="target-url-info"></div>
               </div>
           </div>
       </div>
    </div>

    <script>

        var target_urls = [];

        $(document).ready( function() {
            
            declare_page('target-urls');

            populate_target_urls();

            $('#target-urls-select').on( 'click', function( e ) {
                show_target_url( $(e.target).val() );    
            });

            $('#submit-target-url').on( 'click', function( e ) {
                submit_target_url( );
            });

        });

        function update_status( status ) {

            if ( status == '' ) {
                $('#submit-status').html('');
                $('#submit-status').hide();
            } else {
                $('#submit-status').html( status );
                $('#submit-status').show();
            }

        }

        function populate_target_urls() {
           
            $('#target-urls-select').html('Please wait, loading data ...');

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

                    html += '<select class="wide tall" multiple>';
                    for(var i=0; i<response.target_urls.length; i++) {
                        html += '<option value="' + i + '">' + response.target_urls[i].title + '</option>';
                    }
                    html += '</select>';

                    $('#target-urls-select').html(html);

                    target_urls = response.target_urls;

                },
                error: function( response ) {
                    
                }
            });
            
        }

        function show_target_url( index ) {

            $('#target-url-current').show();

            var html = "";
            
            html += '<label class="medium">URL:</label>';
            html += '<input class="wide" readonly value="' + target_urls[index].url + '"></input>';

            html += '<label class="medium">Title:</label>';
            html += '<input class="wide" readonly value="' + target_urls[index].title + '"></input>';

            html += '<label class="medium">Description:</label>';
            html += '<textarea class="wide short" readonly value="' + target_urls[index].description + '"></textarea>';

            html += '<label class="medium">Created:</label>';
            html += '<input class="wide" readonly value="' + target_urls[index].created + '"></input>';

            $('#target-url-info').html(html);

        }

        function submit_target_url() {

            update_status('Please wait ...');
          
            var url = "add_target_url.json"; 
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'POST',
                data: {
                    owner_id: 1,
                    url: $('#new-url').val(),
                    title: $('#new-title').val(),
                    description: $('#new-description').val(),
                },
                success: function( response ) {
                    if ( response.success == true ) {
                        update_status('<b style="color: darkgreen">Target URL added successfully.</b>'); 

                        populate_target_urls();
                    } else {
                        update_status('<b style="color: darkred">An error occured.  Target URL not created.</b>')
                    }
                },
                error: function( response ) {
                    update_status('<b style="color: darkred">An error occured.  Target URL not created.</b>');
                },
            })
 
        }

    </script>
    
