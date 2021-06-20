// $(document).ready(function(){

//     $('form').on('submit', function(event){
//         console.log(event)
//         $.ajax({
//             data : {
//                 unsaved : $('#unsaveInput').val(),
//                 saved : $('#saveInput').val()
//                 },
//             type : 'POST',
//             url : '/save'
//         })
//         .done(function(data) {

//             if (data.unsaved) {
//                 $('#saveInput').show();
//                 $('#unsaveInput').hide();
//             }
//             else {
//                 $('#unsaveInput').show();
//                 $('#saveInput').hide();
//                 console.log(data)
//             }
//         });

//         event.preventDefault();


//     });

// });