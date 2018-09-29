$(function(){
    //头像预览
    $("#avator").change(function(){
        
        //获取用户选中文件
        var file_obj = $(this)[0].files[0];

        //获取文件路径
        var reader = new FileReader();
        reader.readAsDataURL(file_obj);

        //修改img的src属性
        reader.onload = function(){

            $("#avator_img").attr("src",reader.result)
        
        }

    })

    //基于Ajax的提交
    $(".reg_btn").click(function(){

        var formdata = new FormData();
        var request_data = $("#form").serializeArray()

        $.each(request_data,function (index,data) {
            formdata.append(data.name,data.value)
        })

        formdata.append("avator",$("#avator")[0].files[0]);

        $.ajax({
            url:"",
            type:"post",
            contentType:false,
            processData:false,
            data:formdata,
            success:function(data){
                console.log(data)

                if(data.user){

                    location.href = '/login/'

                }
                else {
                    //清空错误信息
                    $("span.error").html("")

                    //展示此次错误信息
                    $.each(data.msg,function (field,error_list) {

                        if (field == "__all__"){
                            $("#id_re_pwd").next().html(error_list[0])
                        }

                        console.log(field,error_list)
                        $("#id_"+field).next().html(error_list[0]);
                        
                    })
                }
            }
        })


    })

})