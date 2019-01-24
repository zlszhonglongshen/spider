CREATE TABLE `news` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `title` varchar(45) NOT NULL,
  `author` varchar(12) NOT NULL,
  `date` varchar(12) NOT NULL,
  `about` varchar(255) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_UNIQUE` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;