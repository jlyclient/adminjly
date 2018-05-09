$(function() {
    getUserlist(10, 10, 0, callbacklistFun);
    var option_id = null;
    $(".list_columnbox").find('li').map((index, data) => {
        $(data).removeClass("active");
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
    $(".sure_forbid_user").click(function() {
        var xsrf = get_cookie_by_name('_xsrf');
        var forbid_option = $('.forbid_user_select').find('option:selected').attr("value");
        var forbid_text = $('.forbid_user_text').val();
        // uid=xxx&option=xxx&msg=xxx
        if (forbid_option != '' || forbid_text != '') {
            $.ajax({
                url: '/forbid_user',
                type: 'POST',
                data: {
                    '_xsrf': xsrf,
                    option: forbid_option,
                    msg: forbid_text
                },
                success: function(data) {
                    var jsondata = JSON.parse(data);
                    if (jsondata.code == '0') {
                        closePopup(this, '.close_zhenghun');
                        getUserlist(10, 10, 0, callbacklistFun);
                    } else {
                        alert(jsondata.msg);
                    }
                },
                error: function(para) {
                    alert(para);
                }
            })
        } else {
            alert('请填写禁止用户的原因！');
        }
    })
    // 开通用户
    $('.table_tbody').on('click', '.allow_user', function() {
        option_id = $(this).attr('name');
        $('.openup_zhenghun').css({ display: 'block' });
    });
    $(".sureallow_user").click(function() {
        var xsrf = get_cookie_by_name('_xsrf');
        var forbid_option = $('.allow_user_select').find('option:selected').attr("value");
        var forbid_text = $('.allow_user_text').val();
        if (forbid_option != '' || forbid_text != '') {
            $.ajax({
                url: '/allow_user',
                type: 'POST',
                data: {
                    '_xsrf': xsrf,
                    option: forbid_option,
                    msg: forbid_text
                },
                success: function(data) {
                    var jsondata = JSON.parse(data);
                    if (jsondata.code == '0') {
                        closePopup(this, '.openup_zhenghun');
                        getUserlist(10, 10, 0, callbacklistFun);
                    } else {
                        alert(jsondata.msg);
                    }
                },
                error: function(para) {
                    alert(para);
                }
            })
        } else {
            alert('请填写开通用户的原因！');
        }
    });
    // 充值
    $('.table_tbody').on('click', '.chongzhi', function() {
        option_id = $(this).attr('name');
        $('.server_recharge').css({ display: 'block' });
    });
    $(".sure_user_chongzhi").click(function() {
        var xsrf = get_cookie_by_name('_xsrf');
        if ($(".recharge_input").val() != '' || $(".recharge_input").val() != 0) {
            $.ajax({
                url: '/chongzhi',
                type: 'POST',
                data: {
                    _xsrf: xsrf,
                    uid: option_id,
                    num: $(".recharge_input").val()
                },
                success: function(data) {
                    var jsondata = JSON.parse(data);
                    if (jsondata.code == '0') {
                        closePopup(this, '.server_recharge');
                        getUserlist(10, 10, 0, callbacklistFun);
                    } else {
                        alert(jsondata.msg);
                    }
                },
                error: function(para) {
                    alert(para);
                }
            })
        } else {
            alert('充值金额不能为空或者0');
        }
    })
    // $(".list_columnbox").find('.user_list').eq(0).addClass('active');
})
