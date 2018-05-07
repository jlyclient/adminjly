$(function() {
    getUserlist(10, 10, 0, callbacklistFun);
    var option_id = null;
    $(".list_columnbox").find('li').map((index, data) => {
        $(data).removeClass("active");
        console.log($(data).attr('class'));
        if ($(data).attr('class') == 'list_column user_list') {
            $(data).addClass('active');
        }
    })
    function callbacklistFun(value, next) {
        console.log(value, next);
        Page({
			num:value,				//页码数
			startnum:next+1,		//指定页码
			elem:$('#page1'),		//指定的元素
            callback:function(n){	//回调函数
                console.log(n);
				getUserlist(
                    10,
                    10,
                    n-1,
                    callbacklistFun
                );
			}
		});
    }
    $(".table_tbody").on('click', '.del_userlist', function() {
        option_id = $(this).attr('name');
        $(".del_user").css({ display: 'block' });
        console.log($(this).attr('name'));
    });
    $(".sure_del_root").click(function() {
        var xsrf = get_cookie_by_name('_xsrf');
        $.ajax({
            url: '',
            type: 'POST',
            data: {
                '_xsrf': xsrf
            },
            success: function(data) {
                var jsondata = JSON.parse(data);
                if(jsondata.code == 0) {
                    closePopup(this, '.del_user');
                    getUserlist(10, 10, 0, callbacklistFun);
                } else {
                    alert(jsondata.msg);
                }
            }
        })
    });
    // 禁止用户
    $('.table_tbody').on('click', '.forbid_user', function() {
        option_id = $(this).attr('name');
        $('.close_zhenghun').css({ display: 'block' });
    })
    // 开通用户
    $('.table_tbody').on('click', '.allow_user', function() {

    })
    // $(".list_columnbox").find('.user_list').eq(0).addClass('active');
})