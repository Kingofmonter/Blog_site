$(function(){

    $("#view_code_img").click(function(){
        
        $(this)[0].src+="?"

        });


    $(".login_btn").click.function(){

        $.ajax({
            url:"",
            type:"",
            data:{
                user:$("username").val(),
                pwd:$("password").val(),
                view_code:$("#view_code").val(),
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
            },
            success:function(data){
                console.log(data)
            }

        })

    }
    


    });