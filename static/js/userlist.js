$(function() {
    getUserlist('', '', '', '');
    $(".list_columnbox").find('li').map((index, data) => {
        $(this).removeClass("active");
        if ($(this).attr('class').indexof('user_list') > 0) {
            $(this).addClass('active');
        }
    })
    // $(".list_columnbox").find('.user_list').eq(0).addClass('active');
})