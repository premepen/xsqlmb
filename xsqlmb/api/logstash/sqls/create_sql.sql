DROP TABLE IF EXISTS `waf_alert_log`;
CREATE TABLE `waf_alert_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `audit_logid` varchar(155) NOT NULL,
  `http_user_agent` longtext NOT NULL,
  `http_ver` varchar(155) NOT NULL,
  `src_ip` varchar(155) NOT NULL,
  `waf_serv` varchar(155) NOT NULL,
  `msg` varchar(155) NOT NULL,
  `category` varchar(155) NOT NULL,
  `audit_time` datetime(6) NOT NULL,
  `content_length` int(11) NOT NULL,
  `resp_code` int(11) NOT NULL,
  `uniq_id` varchar(255) NOT NULL,
  `request_url` varchar(255) NOT NULL,
  `request_method` varchar(16) NOT NULL,
  `content_type` varchar(155) NOT NULL,
  `server_port` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `modseclog_audit_logid_1af5d08d_uniq` (`audit_logid`)
) ENGINE=InnoDB AUTO_INCREMENT=10055 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `waf_access_log`;
CREATE TABLE `waf_access_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `request_id` varchar(255) NOT NULL,
  `remote_addr` varchar(55) NOT NULL,
  `server_addr` varchar(55) NOT NULL,
  `http_host` varchar(55) NOT NULL,
  `remote_user` varchar(255) NOT NULL DEFAULT '',
  `request_method` varchar(55) NOT NULL,
  `request_time` float(7,4) NOT NULL DEFAULT 0.0,
  `upstream_addr` varchar(55) NOT NULL,
  `upstream_response_time` float(7,4) NOT NULL DEFAULT 0.0,
  `upstream_status` varchar(55) NOT NULL,
  `status` int(11) NOT NULL,
  `request_url` varchar(255) NOT NULL,
  `time_local` datetime(6) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `request` longtext NOT NULL,
  `body_bytes_sent` int(11) NOT NULL,
  `http_user_agent` longtext NOT NULL,
  `http_referer` longtext NOT NULL,
  `user_agent` varchar(255) NOT NULL,
  `os` varchar(255) NOT NULL,
  `device` varchar(255) NOT NULL,
  `http_x_forwarded_for` varchar(255) NOT NULL,
  `server_port` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `request_id_1af5d08d_uniq` (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1111 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `alertlog_detail`;
CREATE TABLE `alertlog_detail` (
  `audit_logid` varchar(100) NOT NULL,
 `detaild`  json DEFAULT NULL,
  PRIMARY KEY (`audit_logid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

