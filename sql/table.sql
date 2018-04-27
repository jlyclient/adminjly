/*管理员基本表*/
create table if not exists jly_admin
(
    id int unsigned primary key auto_increment,
    name varchar(16),
    password  varchar(64),
    mobile    varchar(16),
    sex tinyint not null, /*1=male  2=female */
    role tinyint not null, /*0=root 1=admin*/
    regist_time timestamp not null,
    last_login  timestamp default CURRENT_TIMESTAMP not null,
    last_login_ip varchar(24) default '', /*login ip*/
    valid_state tinyint not null default 0, /*状态 0=合法 1=被禁止*/
    msg varchar(128) default '' /*被禁止的原因*/
) engine=InnoDB, charset=utf8;


