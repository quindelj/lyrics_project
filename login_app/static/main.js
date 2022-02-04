$(document).ready(function(){
    //Shows snippits when over an image
    $( '.img_con' ).onmouseover(function() {
        $( '.snippit' ).show( 'slow' );
    });
    //Hides snippit when not over an image
    $( '.img_con' ).onmouseout(function() {
        $( '.snippit' ).hide( 'slow' );
    });

    //document.getElementById('#lyrics').addEventListener('select', makeSnip);
    
    /*function makeSnip (){
        alert('making snip');
    }*/
    document.getElementById('lyrics').onselect = function() {makeSnip()};

    function makeSnip(){
        document.getElementById('snippit').style.display = "block";
    };

    /*$('#lyrics').onselect(function () {
        $('.snippit').show();
    });*/

    $('#post'),submit(function (e) {
        e.preventDefault();

        console.log(e)
        console.log(this);

        $.ajax({
            url:'/comment',
            method: 'post',
            data: $(this).serialize(),
            success: function(serverResponse){

                console.log(serverResponse);
                $('.posts').prepend(serverResponse);
            }
        })
    })
})