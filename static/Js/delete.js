
$(document).ready(()=>{
    $('.delete_btn').click(function (e) {
        const csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()
        e.preventDefault()
        const id  = $(this).data("id")
        const name = $(this).data("model_name")
        const row_to_delete = $(`#ExpenseRow-${id}`)
        const messagesContainer = $('#MessagesContainer')
        Swal.fire({
                title: 'Are you sure?',
                text: 'do you wish to delete this item',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#343a40',
                cancelButtonColor: '#d9534f',
                confirmButtonText: 'Yes please!'
            }).then((result)=>{
                if (result.isConfirmed) {
                    $.ajax({
                        url : `/${name}/delete/`,
                        type: 'post',
                        data : {
                            'csrfmiddlewaretoken' : csrfmiddlewaretoken,
                            'ajax' : true,
                            'id' : id
                        },
                        success : (response)=> {
                            document.location.replace(`/${name}`)
                        },
                        error : (error) => {
                            console.log(error)
                        }
                    })
                }
            })
    })
})