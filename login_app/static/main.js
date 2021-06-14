$(document).ready(function(){

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