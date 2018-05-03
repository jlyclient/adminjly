$(function() {
    getUserlist('', '', '', '');
    $(".list_columnbox").find('li').map((index, data) => {
        $(data).removeClass("active");
        console.log($(data).attr('class'));
        if ($(data).attr('class') == 'list_column user_list') {
            $(data).addClass('active');
        }
    })
    // $(".list_columnbox").find('.user_list').eq(0).addClass('active');
})