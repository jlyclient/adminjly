

$(function () {
  $(".form_btn").click(function(){
    var obj = {
      user: '',
      password: ''
    };
    $(".love_form_center").find('input').map(function(index, data) {
      obj[$(data).attr('name')] = $(data).val();
    });
    var xsrf = get_cookie_by_name('_xsrf');
    D = {'name': obj.user, 'password': obj.password, '_xsrf': xsrf};
    console.log(D);
    if (obj.user != '' && obj.password != '') {
      // 发送登陆请求
        $.ajax({
            url: '/',
            type: 'POST',
            data: D,
            success: function(para) {
                var jsondata = JSON.parse(para);
                console.log(jsondata);
                if (jsondata.code == 0) {
                    location.href = '/';
                } else {
                    alert(jsondata.msg);
                }
            },
            error: function(para) {
            }
        });
    } else {
      $('.form_err').html('请输入完整的信息!');
    }
  });
  $('.love_form_center').find('input').focus(function() {
    $('.form_err').html('');
  })
})
