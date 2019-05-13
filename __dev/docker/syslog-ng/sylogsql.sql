DROP TABLE IF EXISTS `w_sys_logs`;
CREATE TABLE `w_sys_logs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `host` varchar(32) DEFAULT NULL,
  `facility` varchar(10) DEFAULT NULL,
  `priority` varchar(10) DEFAULT NULL,
  `level` varchar(10) DEFAULT NULL,
  `tag` varchar(10) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `program` varchar(15) DEFAULT NULL,
  `msg` text,
  PRIMARY KEY (`id`),
  KEY `host` (`host`),
  KEY `program` (`program`),
  KEY `datetime` (`datetime`),
  KEY `priority` (`priority`),
  KEY `facility` (`facility`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;