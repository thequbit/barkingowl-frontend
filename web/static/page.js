var tabs = ['home','dispatch-urls', /* 'manage-collections', */ 'configuration'];

$(document).ready(function() { 
    // bind 'myForm' and provide a simple callback function 
    $('#upload_form').ajaxForm(function( response ) { 

        $('#status_label').html( "Please wait ..." )

        var data = $.csv.toObjects( response );

        var json_data = JSON.stringify( data );

        $('#urls_json').val( json_data );

        $('#status_label').html( "" )                
        
    }); 
    
     $('#home').show();
});

function switch_tab(tab_name) {
    for(var i=0; i<tabs.length;i++) {
        $('#'+tabs[i]).hide();
    }
    $('#'+tab_name).show();
}

function upload_csv() {
    var filename = $("#file").val();
    $.ajax({
        type: "POST",
        url: "upload_csv",
        enctype: 'multipart/form-data',
        data: {
            file: filename
        },
        success: function( response ) {
            //alert("Data Uploaded: " + response);
            $('urls_json').val( response );
        }
    });
}

function submit_urls() {
    urls = encodeURIComponent( $('#urls_json').val() );
    $.getJSON('set_urls.json?urls=' + urls, function( data ) {
        // todo: report success/failure
    });
}

function shutdown_system() {
    $.getJSON('shutdown_system.json', function( data ) {
        // todo: report success/failure
    });
}