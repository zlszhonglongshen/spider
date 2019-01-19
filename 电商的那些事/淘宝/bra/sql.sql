CREATE TABLE `bra` (
`bra_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id' ,
`bra_color` varchar(25) NULL COMMENT '颜色' ,
`bra_size` varchar(25) NULL COMMENT '罩杯' ,
`resource` varchar(25) NULL COMMENT '数据来源' ,
`comment` varchar(500) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '评论' ,
`comment_time` datetime NULL COMMENT '评论时间' ,
PRIMARY KEY (`bra_id`)
) character set utf8
;
