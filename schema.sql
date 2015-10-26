create database if not exists dianping;

use dianping;

drop table if exists `dianping`;
create table `dianping` (
  `id` int(11) not null auto_increment,
  `md5id` varchar(255) not null unique,
  `shop_name` varchar(255) not null,
  `shop_address` varchar(255) not null,
  `shop_region` varchar(255) not null,
  `shop_city` varchar(255) not null,
  `shop_latitude` varchar(255) not null,
  `shop_longitude` varchar(255) not null,
  primary key (`id`)
) engine=innodb default charset=utf8;
