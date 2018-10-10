$(function () {


    $(".social-main .like").click(function () {

        var is_up = $(this).hasClass("like-up");


        $.ajax({
            url: "/digg/",
            type: "post",
            data: {
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
                "is_up": is_up,
                "article_id": "{{article_obj.pk}}"

            },
            success: function (data) {


                console.log(data);

            }
        })


    })

})