/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.5.25-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: SerialRecords
-- ------------------------------------------------------
-- Server version	10.5.25-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `serials_1500`
--

DROP TABLE IF EXISTS `serials_1500`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serials_1500` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serial_start` int(11) NOT NULL,
  `serial_end` int(11) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `batch_type` varchar(10) DEFAULT '1500',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serials_1500`
--

LOCK TABLES `serials_1500` WRITE;
/*!40000 ALTER TABLE `serials_1500` DISABLE KEYS */;
INSERT INTO `serials_1500` VALUES (1,762000,762100,NULL,'1500'),(2,570700,570800,'[570703 out]','1500'),(3,456100,456200,NULL,'1500'),(4,550600,550700,'[550686,550700 out]','1500'),(5,398801,398900,'[398888, 398858, 398857, 398886 out]','1500'),(9,628801,628900,'628812 out','1500');
/*!40000 ALTER TABLE `serials_1500` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serials_750`
--

DROP TABLE IF EXISTS `serials_750`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serials_750` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serial_start` int(11) NOT NULL,
  `serial_end` int(11) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `batch_type` varchar(10) DEFAULT '750',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serials_750`
--

LOCK TABLES `serials_750` WRITE;
/*!40000 ALTER TABLE `serials_750` DISABLE KEYS */;
/*!40000 ALTER TABLE `serials_750` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-10 21:41:35
