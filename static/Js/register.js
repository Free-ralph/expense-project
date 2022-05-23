$(document).ready(()=>{
    $('#username').keyup(()=>{
        username_field = $('#username')
        const value = username_field.val();
        $.ajax({
            url : "{% url 'auth:username_validator' %}",
            type : "get",
            data : {
                'username' : value
            },
            beforeSend: () => {
              $("#form").addClass('ajax-request')
              username_field.removeClass('is-invalid')
              username_field.removeClass('is-valid')
            },
            success : (response) => {
                if (response.username_valid){
                    username_field.addClass('is-valid')
                }
                if(response.username_error){
                    username_field.addClass('is-invalid')
                    $('#username_invalid').text(response.username_error).css('display', 'block')
                }else{
                    username_field.removeClass('is-invalid')
                    $('#username_invalid').css('display', 'none')
                }
            },
            complete: ()=>{
              $("#form").removeClass('ajax-request')
            },
            error : (error) => {
              
            } ,
            
        })
    })
})