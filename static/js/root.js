$(function() {
    getAdmin(10, 10, 0, callbacklistFun);
    var del_uid = null;
    var type_sure = false;
    var uid = null;
    function callbacklistFun(value, next) {
        console.log(value, next);
        Page({
			num:value,				//页码数
			startnum:next+1,		//指定页码
			elem:$('#page1'),		//指定的元素
            callback:function(n){	//回调函数
                console.log(n);
				getAdmin(
                    10,
                    10,
                    n-1,
                    callbacklistFun
                );
			}
		});
    }
    $('.creat_root').click(function() {
        $(".add_root").css({ display: 'block' });
        $(".addroot_form").find('input').map((index, data) => {
            $(data).val('');
        });
        type_sure = false;
    });

    $(".sure_creat_root").click(function() {
        var obj = {name: '', mobile: '', password: ''};
        $(".addroot_form").find('input').map((index, data) => {
            obj[$(data).attr('name')] = $(data).val();
        });
        if (obj.name != '' && obj.mobile != '' && obj.password != '') {
            var xsrf = get_cookie_by_name('_xsrf');
            $.ajax({
                url: type_sure == false ? '/create_admin' : '/edit_admin',
                type: 'POST',
                data: type_sure == false ? {
                    name: obj.name,
                    mobile: obj.mobile,
                    password: obj.password,
                    '_xsrf': xsrf
                } : {
                    uid: uid,
                    name: obj.name,
                    mobile: obj.mobile,
                    password: obj.password,
                    '_xsrf': xsrf
                } ,
                success: function(data) {
                    var jsondata = JSON.parse(data);
                    console.log(jsondata);
                    if (jsondata.code == 0) {
                        closePopup(this, '.add_root');
                        getAdmin(10, 10, 0, callbacklistFun);
                    } else {
                        alert(jsondata.msg);
                    }
                },
                error: function(para) {
                    alert(para);
                }
            })
        } else {
            alert('请输入完整的信息！')
        }
    })
    $(".table_tbody").on('click', '.del_root', function() {
        del_uid = $(this).attr('name');
        $(".del_user").css({ display: 'block' });
    });
    $('.table_tbody').on('click', '.edit_root', function() {
        $(".add_root").css({ display: 'block' });
        type_sure = true;
        var This = this;
        uid = $(this).attr('uid');
        $(".addroot_form").find('input').map((index, data) => {
            $(data).val($(This).attr($(data).attr('name')));
        });
    });
    $(".sure_del_root").click(function() {
        var xsrf = get_cookie_by_name('_xsrf');
        $.ajax({
            url: '/del_admin',
            type: 'POST',
            data: {
                '_xsrf': xsrf,
                uid: del_uid,
            },
            success: function(data) {
                var jsondata = JSON.parse(data);
                if (jsondata.code == 0) {
                    closePopup(this, '.del_user');
                    getAdmin(10, 10, 0, callbacklistFun);
                } else {
                    alert(jsondata.msg);
                }
            },
            error: function(para) {
                alert(para);
            }
        })
    })
})