-- fNotes database structure.
-- version 1.0.0
-- http://code.google.com/p/fnotes/
-- gaotianpu@gmail.com


SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `fnotes`
--

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
CREATE TABLE IF NOT EXISTS `groups` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `userid` bigint(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `createdate` datetime NOT NULL,
  `lastmodifiedate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `notescount` int(11) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Table structure for table `notes`
--

CREATE TABLE IF NOT EXISTS `notes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `groupid` bigint(20) NOT NULL,
  `userid` bigint(20) NOT NULL,
  `notes` text NOT NULL,
  `summary` varchar(150) NOT NULL DEFAULT '',
  `createdate` datetime NOT NULL,
  `lastmodifieddate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` smallint(6) NOT NULL DEFAULT '1',
  `openorder` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `groupid` (`groupid`,`userid`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=30 ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `secretkey` varchar(50) NOT NULL DEFAULT '',
  `registerdate` datetime NOT NULL,
  `lastlogindate` datetime NOT NULL,
  `status` smallint(6) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;
