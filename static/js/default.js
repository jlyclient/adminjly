$(function() {
  // 退出登录
  $('.server_logout').click(function() {
    // 发送ajax请求
  });
});

// 关闭弹窗
function closePopup(e, cn) {
  $(cn).css({ display: 'none' });
}

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

//获取管理员列表
function getAdmin(limt, page, next, callback) {
  var xsrf = get_cookie_by_name('_xsrf');
  $.ajax({
    url: '/admin',
    type: 'POST',
    data: {
      limt: limt ? limt : '',
      page: page ? page : '',
      next: next ? next : '',
      '_xsrf': xsrf
    },
    success: function(json) {
      var jsondata = JSON.parse(json);
      console.log(jsondata);
      if (jsondata.code == 0) {
        callback(Math.ceil(jsondata.data.data.count / jsondata.data.data.page), next);
        var jsonhtml = json
        var tablehtml = '';
        $(".table_tbody").empty();
        for (var i = 0; i< jsondata.data.data.length; i++) {
          tablehtml += '<tr>'+
          '<th><input name='+ jsondata.data.data[i].id +' type="checkbox"></th>'+
          '<th>'+ jsondata.data.data[i].name +'</th>'+
          '<th>'+ jsondata.data.data[i].mobile +'</th>'+
          '<th>'+ jsondata.data.data[i].password +'</th>'+
          '<th>'+ jsondata.data.data[i].last_login +'</th>'+
          '<th>'+ jsondata.data.data[i].last_login_ip +'</th>'+
          '<th class="table_btn">'+
            '<span name='+ jsondata.data.data[i].name +' password='+ jsondata.data.data[i].password +' mobile='+ jsondata.data.data[i].mobile +' uid='+ jsondata.data.data[i].id +' class="cursor edit_root">编辑</span>'+
            '<span name='+ jsondata.data.data[i].id +' class="cursor del_root">删除</span>'+
          '</th>'+
        '</tr>';
        }
        $('.table_tbody').append(tablehtml);
      } else {
        alert(jsondata.msg);
      }
    },
    error: function(para) {
      alert(para);
    }
  })
}


// 获取用户列表
function getUserlist(limt, page, next, callback) {
  var xsrf = get_cookie_by_name('_xsrf');
  $.ajax({
    url: '/user_list',
    type: 'POST',
    data: {
      limt: limt ? limt : '',
      page: page ? page : '',
      next: next ? next : '',
      '_xsrf': xsrf
    },
    success: function(json) {
      var jsondata = JSON.parse(json);
      if (jsondata.code == 0) {
        callback(Math.ceil(jsondata.data.data.count / jsondata.data.data.page), next);
        var tablehtml = '';
        console.log(jsondata);
        $(".table_tbody").empty();
        var valid_state = ['待审核', '被禁止', '删除', '审核通过'];
        for (var i = 0; i < jsondata.data.data.length; i++) {
          tablehtml += '<tr>'+
          '<th><input name='+ jsondata.data.data[i].id +' type="checkbox"></th>'+
          '<th>'+ jsondata.data.data[i].id +'</th>'+
          '<th>'+ jsondata.data.data[i].nick_name +'</th>'+
          '<th>'+ valid_state[jsondata.data.data[i].valid_state] +'</th>'+
          '<th>'+ jsondata.data.data[i].msg +'</th>'+
          '<th>'+ jsondata.data.data[i].num +'</th>'+
          '<th>'+ jsondata.data.data[i].free +'</th>'+
          '<th>'+ jsondata.data.data[i].last_login +'</th>'+
          '<th>'+ jsondata.data.data[i].last_login_ip +'</th>'+
          '<th class="table_btn">'+
            '<span name='+ jsondata.data.data[i].id +' class="cursor">充值</span>'+
            '<span name='+ jsondata.data.data[i].id +' class="cursor">禁止</span>'+
            '<span name='+ jsondata.data.data[i].id +' class="cursor">开通</span>'+
            '<span name='+ jsondata.data.data[i].id +' class="cursor">删除</span>'+
          '</th>'+
        '</tr>';
        }
        // console.log(tablehtml);
        $('.table_tbody').append(tablehtml);
      } else {
        alert(jsondata.msg);
      }
    }
  })
}