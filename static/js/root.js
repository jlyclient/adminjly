$(function() {
    getAdmin('', '', '', '');
    $('.creat_root').click(function() {
        $(".add_root").css({ display: 'block' });
    });
    var del_uid = null;
    $(".sure_creat_root").click(function() {
        var obj = {name: '', mobile: '', password: ''};
        $(".addroot_form").find('input').map((index, data) => {
            obj[$(data).attr('name')] = $(data).val();
        });
        if (obj.name != '' && obj.mobile != '' && obj.password != '') {
            var xsrf = get_cookie_by_name('_xsrf');
            $.ajax({
                url: '/create_admin',
                type: 'POST',
                data: {
                    name: obj.name,
                    mobile: obj.mobile,
                    password: obj.password,
                    '_xsrf': xsrf
                },
                success: function(data) {
                    var jsondata = JSON.parse(data);
                    console.log(jsondata);
                    if (jsondata.code == 0) {
                        closePopup(this, '.add_root');
                        getAdmin('', '', '', '');
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
        console.log($(this).attr('name'));
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
                    getAdmin('', '', '', '');
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