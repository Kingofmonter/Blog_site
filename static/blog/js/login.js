$(function () {

    $("#view_code_img").click(function () {

        $(this)[0].src += "?"

    });

    $("#login-button").click(function () {


        $.ajax({
           url:"",
            type:"post",
            data:{
               user:$("#username").val(),
                pwd:$("#password").val(),
                view_code:$("#view_code ").val(),
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
            },
            success:function (data) {
            
                if(data.user){
                    location.href = '/index/'
                }
                else{

                    $(".error").text(data.msg)
                }


            }
        })
    })


});