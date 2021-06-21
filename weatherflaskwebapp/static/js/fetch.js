$(document).ready(function(){
    $("form").submit(function(e){
        // At this point you'll want to have some type of flag to indicate whether you
        // should allow the form submission to continue, or cancel the event. For example,
        // it could be whether not showMe is visible (I don't know what you're going for).

        e.preventDefault();
        console.log('You clicked me!');


        // Submit form after your code runs (or whenever you want)
//        $(this).submit();

        $.ajax({
            data : {
                city: $("#city").val(),
            },
            type : 'POST',
            url : '/fetch',
            success: function(data) {
//                alert('form was submitted');

                if (data.error) {
                    alert(data.error);
                }
                else {
                    console.log(data)
                    var template = $("#result_template").html()
                    var html = Mustache.to_html(template, data);
                    $("#result").html(html);
                    $('#flashMessage').hide();
                    console.log(data)
                }
            }

        });
    });
});



//$(document).ready(function(){
//    $("form").submit(function(e){
//        e.preventDefault();
//        errorAlert('You clicked me!');
//        console.log(event);
//
//        $.ajax({
//            data : {
//                form : $('#nameInput').val()
//                },
//            type : 'POST',
//            url : '/fetch'
//        })
//        .done(function(data) {
//
//            if (data.error) {
//                $('#errorAlert').text(data.error).show();
//                $('#successAlert').hide();
//            }
//            else {
//                $('#result').show();
//                $('#inputForm').hide();
//                console.log(data)
//            }
//        });

//
//});