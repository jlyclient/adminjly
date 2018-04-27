function get_cookie_by_name(name)
{
    var start = document.cookie.indexOf(name);
    if (start != -1) {
        var res = ""; 
        var end  = document.cookie.indexOf(";", start+1);
        if (end == -1) {
            res = document.cookie.substring(start+name.length+1);
        } else {
            res = document.cookie.substring(start+name.length+1, end);
        }   
        return res;
    }   
    return ""; 
}

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
    if (obj.user != '' && obj.password != '') {
      // 发送登陆请求
        $.ajax({
            url: '/',
            type: 'POST',
            data: D,
            success: function(para) {
                var jsondata = JSON.parse(para);
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
