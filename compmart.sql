-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: compmart
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_address`
--

DROP TABLE IF EXISTS `account_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `street` varchar(60) NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` varchar(2) NOT NULL,
  `zip_code` varchar(5) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_address_user_id_street_city_state_180bbc84_uniq` (`user_id`,`street`,`city`,`state`),
  CONSTRAINT `account_address_user_id_a1553eba_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_address`
--

LOCK TABLES `account_address` WRITE;
/*!40000 ALTER TABLE `account_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_creditcard`
--

DROP TABLE IF EXISTS `account_creditcard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_creditcard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` longblob NOT NULL,
  `card_type` varchar(20) NOT NULL,
  `holder_name` varchar(50) NOT NULL,
  `expiration_date` date NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_creditcard_user_id_fb5a802b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `account_creditcard_user_id_fb5a802b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_creditcard`
--

LOCK TABLES `account_creditcard` WRITE;
/*!40000 ALTER TABLE `account_creditcard` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_creditcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add permission',4,'add_permission'),(11,'Can change permission',4,'change_permission'),(12,'Can delete permission',4,'delete_permission'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add product',8,'add_product'),(23,'Can change product',8,'change_product'),(24,'Can delete product',8,'delete_product'),(25,'Can add review',9,'add_review'),(26,'Can change review',9,'change_review'),(27,'Can delete review',9,'delete_review'),(28,'Can add order item',10,'add_orderitem'),(29,'Can change order item',10,'change_orderitem'),(30,'Can delete order item',10,'delete_orderitem'),(31,'Can add order',11,'add_order'),(32,'Can change order',11,'change_order'),(33,'Can delete order',11,'delete_order'),(34,'Can add credit card',12,'add_creditcard'),(35,'Can change credit card',12,'change_creditcard'),(36,'Can delete credit card',12,'delete_creditcard'),(37,'Can add address',13,'add_address'),(38,'Can change address',13,'change_address'),(39,'Can delete address',13,'delete_address');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'argon2$argon2i$v=19$m=512,t=2,p=2$MVcxeFlaTDQ2MXJD$XW+ECcKWOfjj3UkVa6zECg','2017-09-26 03:41:11',1,'preston','Preston','West','prestonmontewest@gmail.com',1,1,'2017-09-26 03:41:02');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commerce_order`
--

DROP TABLE IF EXISTS `commerce_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commerce_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `street` varchar(60) NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` varchar(2) NOT NULL,
  `zip_code` varchar(5) NOT NULL,
  `purchase_date` datetime NOT NULL,
  `total` decimal(7,2) NOT NULL,
  `card_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `commerce_order_card_id_5c85892b_fk_account_creditcard_id` (`card_id`),
  KEY `commerce_order_user_id_3f7ff6c0_fk_auth_user_id` (`user_id`),
  CONSTRAINT `commerce_order_card_id_5c85892b_fk_account_creditcard_id` FOREIGN KEY (`card_id`) REFERENCES `account_creditcard` (`id`),
  CONSTRAINT `commerce_order_user_id_3f7ff6c0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commerce_order`
--

LOCK TABLES `commerce_order` WRITE;
/*!40000 ALTER TABLE `commerce_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `commerce_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commerce_orderitem`
--

DROP TABLE IF EXISTS `commerce_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commerce_orderitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `purchase_price` decimal(6,2) NOT NULL,
  `quantity` smallint(5) unsigned NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `commerce_orderitem_order_id_product_id_80761716_uniq` (`order_id`,`product_id`),
  KEY `commerce_orderitem_product_id_eeb6e678_fk_commerce_product_id` (`product_id`),
  CONSTRAINT `commerce_orderitem_order_id_c812b8bd_fk_commerce_order_id` FOREIGN KEY (`order_id`) REFERENCES `commerce_order` (`id`),
  CONSTRAINT `commerce_orderitem_product_id_eeb6e678_fk_commerce_product_id` FOREIGN KEY (`product_id`) REFERENCES `commerce_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commerce_orderitem`
--

LOCK TABLES `commerce_orderitem` WRITE;
/*!40000 ALTER TABLE `commerce_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `commerce_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commerce_product`
--

DROP TABLE IF EXISTS `commerce_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commerce_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `description` longtext NOT NULL,
  `discontinued` tinyint(1) NOT NULL,
  `stock` smallint(5) unsigned NOT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commerce_product`
--

LOCK TABLES `commerce_product` WRITE;
/*!40000 ALTER TABLE `commerce_product` DISABLE KEYS */;
INSERT INTO `commerce_product` VALUES (1,'Acer Aspire E 15 E5-575-33BM 15.6-Inch FHD Notebook (Intel Core i3-7100U 7th Generation , 4GB DDR4, 1TB 5400RPM HD, Intel HD Graphics 620, Windows 10 Home), Obsidian Black',349.99,'Acer Aspire E5-575-33BM comes with these high level specs: 7th Generation Intel Core i3-7100U Processor (2.4GHz, 3MB L3 cache), Windows 10 Home, 15.6\" Full HD Widescreen LED-backlit Display, Intel HD Graphics 620, 4GB DDR4 Memory, 1TB SATA Hard Drive (5400RPM), 8X DVD-Super Multi Double-Layer Drive (M-DISC enabled), Secure Digital (SD) card reader, High Definition Audio Support, 802.11ac Wi-Fi featuring MU-MIMO technology (Dual-Band 2.4GHz and 5GHz), Bluetooth 4.1, Gigabit Ethernet, Built-In HD Webcam (1280 x 720) supporting High Dynamic Range (HDR), 1 - USB 3.1 (Type C) port, 2 - USB 3.0 Ports (One with Power-off Charging), 1 - USB 2.0 Port, 1 - HDMI Port with HDCP support, 6-cell Li-ion Battery (2800 mAh), Up to 12-hours Battery Life, 5.27 lbs. | 2.39 kg (system unit only) (NX.GG5AA.005)',0,13,'images/products/51ReTYTeQyL._SL1000__ZpODh6V.jpg'),(2,'Acer Predator Helios 300 Gaming Laptop, Intel Core i7 CPU, GeForce GTX 1060 6GB, VR Ready, 15.6\" Full HD, 16GB DDR4, 256GB SSD, Red Backlit KB, Metal Chassis, G3-571-77QK',1049.99,'Acer Predator Helios 300 G3-571-77QK Gaming Notebook comes with these high level specs: 7th Generation Intel Core i7-7700HQ Processor 2.8GHz with Turbo Boost Technology up to 3.8GHz, 15.6\" Full HD (1920 x 1080) widescreen LED-backlit IPS display, NVIDIA GeForce GTX 1060 with 6 GB of dedicated GDDR5 VRAM, 16GB DDR4 2400MHz Memory, 256GB SSD, Acer TrueHarmony Technology Sound System, Two Built-in Stereo Speakers, Secure Digital (SD) card reader, 802.11ac WiFi featuring 2x2 MIMO technology (Dual-Band 2.4GHz and 5GHz), Bluetooth 4.0, 10/100/1000 Gigabit Ethernet LAN (RJ-45 port), HD Webcam (1280 x 720) supporting High Dynamic Range (HDR), 1 - USB 3.1 (Type C) port (Gen 1 up to 5 Gbps), 1 - USB 3.0 Port (featuring Power-off Charging), 2 - USB 2.0 Ports, 1 - HDMI 2.0 Port with HDCP Support, 4-cell Li-ion Battery (3220 mAh), Up to 7-hours Battery Life, 5.95 lbs. | 2.7 kg (system unit only) (NH.Q28AA.001)',0,8,'images/products/61l7du1g91L._SL1000__UGhdY3H.jpg'),(3,'Wireless Mouse, SzHahn 2.4G Slim Rechargeable Wireless Mouse with USB Receiver,3 Adjustable DPI Levels for Notebook, PC,MAC, Laptop, Computer, Macbook - Black',10.99,'Based on customer feedback research in last several months, we make some improvements to better our mouse: a powerful,reliable and accuracy connection,stay-put comfort,plug and play simply,portable recharging.You can work and play in any place where you would like.There\'s no limit to where you can get precise cursor control.',0,21,'images/products/61lpbP3wgqL._SL1500__wYER8nd.jpg'),(4,'Logitech 920-002478 K120 USB Keyboard',14.84,'With comfortable, quiet typing, a sleek yet sturdy design and a plug-and-play USB connection, the Logitech Keyboard K120 gives you a better typing experience that\'s built to last.',0,29,'images/products/61P0nVolUBL._SL1286__7yx0c6V.jpg'),(5,'CyberPower AVRG750U AVR UPS System, 750VA/450W, 12 Outlets, Compact',69.95,'Cyberpower AVR Series AVRG750U - UPS - AC 120 V - 450 watt - 750 VA 7 Ah - USB - output connectors: 12',0,17,'images/products/61pfjK4csnL._SL1000__BF1T3BK.jpg'),(6,'1536P Full HD Webcam, Besteker 1080P USB Web Camera with Microphone for Video Calling, Streaming and Recording, Wide Angle Skype Camera with Facial-enhancement Technology for Desktop, Laptop, PC, Mac',50.99,'',0,8,'images/products/61w-vHkyFL._SL1411__CuVtsTI.jpg'),(7,'CYBERPOWERPC Gamer Xtreme GXi10180A Desktop Gaming PC (Intel i7-7700 3.6GHz, NVIDIA GTX 1060 3GB, 8GB DDR4 RAM, 1TB 7200RPM HDD, Win 10 Home), Black',999.99,'Destroy the competition with the CYBERPOWERPC Gamer Xtreme series of gaming desktops. The Gamer Xtreme series features the latest generation of high performance Intel Core processors and ultra-quick DDR RAM to easily handle system-intensive tasks, such as high definition video playback and gaming. Coupled with powerful discreet video cards, the Gamer Xtreme series provides a smooth gaming and multimedia experience.',0,4,'images/products/71CM3Hz4wIL._SL1500__md9ADol.jpg'),(8,'Timetec Hynix IC 16GB Kit (2x8GB) DDR3 1600MHz PC3-12800 Non ECC Unbuffered 1.35V/1.5V CL11 2Rx8 Dual Rank 240 Pin UDIMM Desktop Memory Ram Module Upgrade (16GB Kit (2x8GB))',104.99,'Timetec® – Memory of a lifetime\r\n\r\nCompatible with (But not Limited to):\r\n*Please click image for more compatible systems model\r\n\r\nAcer - Aspire AT7 Series AT7-xxx/ ...\r\n\r\nAlienware - Aurora R4 Desktop/ x51 Desktop/...\r\n\r\nARBOR - MB-i77Q0 Motherboard/...\r\n\r\nASRock - Motherboard 970 Extreme3/...\r\n\r\nASUS/ASmobile - A55 Motherboard A55BM-A/...\r\n\r\nBCM - BC77Q Motherboard/ BC87Q/...\r\n\r\nBiostar - A55MD2/ A55MG+/ ...\r\n\r\nClevo - Notebook P150EM/...\r\n\r\nDell - Inspiron 3250/ 3647/ 3650/ 3847/...\r\n\r\nDFI - DL310-C226 Board/ DL631-C226/...\r\n\r\nEliteGroup (ECS) - (ECS) - A55F2-A2 Motherboard/...\r\n\r\nEVGA - - Classified X79/ X79 FTW/ SLI/ Z75/...\r\n\r\nFoxconn - A55A Motherboard/ A55M/ A55MP/...\r\n\r\nFujitsu - CELSIUS W420/ W520/ W530/...\r\n\r\nGateway - DX Desktop DX4375G-xxxx/ DX4885-UB3A/...\r\n\r\nGigabyte - G1.Assassin 2 Motherboard/ G1.Sniper 3/...\r\n\r\nHP/Compaq - 100 Desktop 100-405la/ 100-406la/...\r\n\r\nIntel - DB75EN Motherboard/ DB85FL/ DH77DF/...\r\n\r\nLenovo - Erazer X310/ X315/...\r\n\r\nMEDION - ERAZER X5308 F Gaming PC/ ...\r\n\r\nMSI - Motherboard 760GMA-P34/(FX)/ 760GM-P34/(FX)/...\r\n\r\nNEC - Express 5800 51Eb/...\r\n\r\nPortwell - CAR-3040 Rack-mount Server/ ...\r\n\r\nQNAP - NAS servers TVS-1271U/ ...\r\n\r\nSamsung - DB Desktop DB-Z400/...\r\n\r\nSapphire - PURE Black X79N (PB-CI7X79N)/ ...\r\n\r\nShuttle - SH81R4 Barebone/ ...\r\n\r\nSupermicro - A+ Server 1022TC-IBQF/...\r\n\r\nTyan Computers - Computers - S5535/...\r\n\r\nZOTAC - Motherboard H77-ITX WiFi A and B Series (DIMM)/...\r\n\r\nNeed to know if this part is compatible?\r\nContact us with manufacturer and model information of your motherboard',0,14,'images/products/71K15cYF8uL._SL1500__hmyeIDv.jpg'),(9,'Corsair Vengeance LPX 16GB (2x8GB) DDR4 DRAM 3000MHz C15 Desktop Memory Kit - Black (CMK16GX4M2B3000C15)',162.99,'Vengeance LPX memory is designed for high-performance overclocking. The heat spreader is made of pure aluminum for faster heat dissipation, and the eight-layer PCB helps manage heat and provides superior overclocking headroom. Each IC is individually screened for performance potential. The DDR4 form factor is optimized for the latest Intel 100 Series motherboards and offers higher frequencies, greater bandwidth, and lower power consumption than DDR3 modules. Vengeance LPX DDR4 modules are compatibility-tested across 100 Series motherboards for reliably fast performance. There\'s XMP 2.0 support for trouble-free automatic overclocking. And, they\'re available in multiple colors to match your motherboard, your components, or just your style. customer service/tech support: 1-888-222-4346 opt. 1',0,19,'images/products/71M8prTHgBL._SL1200__ncErIWt.jpg'),(10,'EVGA 500 W1, 80+ WHITE 500W, 3 Year Warranty, Power Supply 100-W1-0500-KR, Black',39.99,'When building on a budget, the EVGA 500W 80 PLUS is a great choice at a low cost. Supporting 40A on a single +12V rail provides more options without having to reduce your component requirements. Save space with the 500W\'s compact design, well-placed power switch and fully sleeved cables. The 500W offers the connections and protections needed for basic system builds. With a standard 3 year warranty and ultra quiet fan design the 500W will be a great asset for your next build on a budget.',1,2,'images/products/71nq2dgMs8L._SL1500__iAkAbts.jpg'),(11,'EVGA 600 B1, 80+ BRONZE 600W, 3 Year Warranty, Includes FREE Power On Self Tester, Power Supply 100-B1-0600-KR',58.96,'With price and performance in mind, the EVGA 600B is the best value power supply for your next build on a budget. With 80 Plus Bronze standard, over 80% efficiency under typical loads, the EVGA 600B is a great choice. Combining 600W of continuous power and Single +12V High AMP rail design, gain maximum power and efficiency while staying protected with a series of multiple safety protections all bundled into one!',0,64,'images/products/71QJGJY6egL._SL1500__evcf1lo.jpg'),(12,'Intel 7th Gen Intel Core Desktop Processor i7-7700K (BX80677I77700K)',299.00,'Intel 7th Gen Intel Core Desktop Processor i7-7700K (BX80677I77700K)',0,19,'images/products/410c2wJRXGL_FBPS3bN.jpg'),(13,'AMD FD6300WMHKBOX FX-6300 6-Core Processor Black Edition',89.12,'',0,0,'images/products/412qUhIDOUL_gp6XCzl.jpg'),(14,'EVGA GeForce GTX 1050 Ti SC GAMING, 4GB GDDR5, DX12 OSD Support (PXOC) Graphics Card 04G-P4-6253-KR',157.99,'The EVGA GeForce GTX 1050 Ti hits the perfect spot for that upgrade you know you need, but at the price you want! With the latest NVIDIA Pascal architecture, the 4GB GTX 1050 Ti displays stunning visuals and great performance at 1080p HD+. Installing a EVGA GeForce GTX 1050 Ti gives you the power to take on today\'s next-gen titles in full 1080p HD - with room to spare. These cards give you a choice of memory sizes, cooling options, factory overclocks, and power options to fit every need and every system. Of course, no GTX card would be complete without essential gaming technologies, such as NVIDIA GameStream, G-Sync, and GeForce Experience. If you\'ve been waiting for that card that gives you the performance to take back the competitive edge, but without taking out your wallet, then the GTX 1050 Ti is the card for you!',0,9,'images/products/8143RlelBcL._SL1500__aFQMTBJ.jpg'),(15,'Sennheiser GAME ZERO Gaming Headset- Black',168.98,'The new closed back G4ME ZERO headset is ideal for immersive gaming at the highest level of competition. Designed to be the most comfortable and best sounding closed headset on the market, the G4ME ZERO features XXL ear cups and a new ear pad design making it the perfect choice for immersive gaming. Drawing on Sennheiser\'s experience in creating professional headsets for aviation, layers of padding and memory foam are shaped to effectively shield the user from external sound and prevent gaming sound from disturbing others. This lets you hear every detail of the game, just as the game developers intended. G4ME ZERO is also perfect for the gamer on the move with a unique foldable design and supplied hard carry case.',0,12,'images/products/51hGrH11NVL.jpg'),(16,'Cooler Master Hyper 212 EVO RR-212E-20PK-R2 CPU Cooler with 120mm PWM Fan',29.99,'Cooler Master, an industry leading chassis, thermal solution, peripheral, and accessory manufacturer, signals the rebirth of a household name in computing, the Hyper 212 EVO CPU Cooler. It comes packed with an improved tower fin design, heat pipe layout, and upgraded fans and fan brackets that provide an even more extreme value for end-users of all types. Dents are created when the heat pipes are sealed.The cut and seal is not a damage, after the heatpipe is full, machine will crimp it.',0,45,'images/products/91UNx7QSvpL._SL1500_.jpg');
/*!40000 ALTER TABLE `commerce_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commerce_review`
--

DROP TABLE IF EXISTS `commerce_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commerce_review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `body` longtext NOT NULL,
  `rating` smallint(5) unsigned NOT NULL,
  `pub_date` datetime NOT NULL,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `commerce_review_product_id_user_id_838823bc_uniq` (`product_id`,`user_id`),
  KEY `commerce_review_user_id_4461d886_fk_auth_user_id` (`user_id`),
  CONSTRAINT `commerce_review_product_id_94c12bd0_fk_commerce_product_id` FOREIGN KEY (`product_id`) REFERENCES `commerce_product` (`id`),
  CONSTRAINT `commerce_review_user_id_4461d886_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commerce_review`
--

LOCK TABLES `commerce_review` WRITE;
/*!40000 ALTER TABLE `commerce_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `commerce_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2017-09-26 03:42:19','2','pmwest.pythonanywhere.com',2,'[{\"changed\": {\"fields\": [\"domain\", \"name\"]}}]',7,1),(2,'2017-09-27 15:58:13','1','preston',2,'[{\"changed\": {\"fields\": [\"first_name\", \"last_name\"]}}]',3,1),(3,'2017-09-27 16:03:34','1','Acer Aspire E 15 E5-575-33BM 15.6-Inch FHD Notebook (Intel Core i3-7100U 7th Generation , 4GB DDR4, 1TB 5400RPM HD, Intel HD Graphics 620, Windows 10 Home), Obsidian Black',1,'[{\"added\": {}}]',8,1),(4,'2017-09-27 16:04:51','2','Acer Predator Helios 300 Gaming Laptop, Intel Core i7 CPU, GeForce GTX 1060 6GB, VR Ready, 15.6\" Full HD, 16GB DDR4, 256GB SSD, Red Backlit KB, Metal Chassis, G3-571-77QK',1,'[{\"added\": {}}]',8,1),(5,'2017-09-27 16:07:27','3','Wireless Mouse, SzHahn 2.4G Slim Rechargeable Wireless Mouse with USB Receiver,3 Adjustable DPI Levels for Notebook, PC,MAC, Laptop, Computer, Macbook - Black',1,'[{\"added\": {}}]',8,1),(6,'2017-09-27 16:09:06','4','Logitech 920-002478 K120 USB Keyboard',1,'[{\"added\": {}}]',8,1),(7,'2017-09-27 16:14:41','5','CyberPower AVRG750U AVR UPS System, 750VA/450W, 12 Outlets, Compact',1,'[{\"added\": {}}]',8,1),(8,'2017-09-27 16:22:54','6','1536P Full HD Webcam, Besteker 1080P USB Web Camera with Microphone for Video Calling, Streaming and Recording, Wide Angle Skype Camera with Facial-enhancement Technology for Desktop, Laptop, PC, Mac',1,'[{\"added\": {}}]',8,1),(9,'2017-09-27 16:34:13','7','CYBERPOWERPC Gamer Xtreme GXi10180A Desktop Gaming PC (Intel i7-7700 3.6GHz, NVIDIA GTX 1060 3GB, 8GB DDR4 RAM, 1TB 7200RPM HDD, Win 10 Home), Black',1,'[{\"added\": {}}]',8,1),(10,'2017-09-27 18:28:56','8','Timetec Hynix IC 16GB Kit (2x8GB) DDR3 1600MHz PC3-12800 Non ECC Unbuffered 1.35V/1.5V CL11 2Rx8 Dual Rank 240 Pin UDIMM Desktop Memory Ram Module Upgrade (16GB Kit (2x8GB))',1,'[{\"added\": {}}]',8,1),(11,'2017-09-27 18:31:07','9','Corsair Vengeance LPX 16GB (2x8GB) DDR4 DRAM 3000MHz C15 Desktop Memory Kit - Black (CMK16GX4M2B3000C15)',1,'[{\"added\": {}}]',8,1),(12,'2017-09-27 18:32:22','10','EVGA 500 W1, 80+ WHITE 500W, 3 Year Warranty, Power Supply 100-W1-0500-KR, Black',1,'[{\"added\": {}}]',8,1),(13,'2017-09-27 18:33:58','11','EVGA 600 B1, 80+ BRONZE 600W, 3 Year Warranty, Includes FREE Power On Self Tester, Power Supply 100-B1-0600-KR',1,'[{\"added\": {}}]',8,1),(14,'2017-09-27 18:35:45','12','Intel 7th Gen Intel Core Desktop Processor i7-7700K (BX80677I77700K)',1,'[{\"added\": {}}]',8,1),(15,'2017-09-27 18:37:39','13','AMD FD6300WMHKBOX FX-6300 6-Core Processor Black Edition',1,'[{\"added\": {}}]',8,1),(16,'2017-09-27 18:38:49','14','EVGA GeForce GTX 1050 Ti SC GAMING, 4GB GDDR5, DX12 OSD Support (PXOC) Graphics Card 04G-P4-6253-KR',1,'[{\"added\": {}}]',8,1),(17,'2017-09-27 18:39:52','15','Sennheiser GAME ZERO Gaming Headset- Black',1,'[{\"added\": {}}]',8,1),(18,'2017-09-27 18:42:26','16','Cooler Master Hyper 212 EVO RR-212E-20PK-R2 CPU Cooler with 120mm PWM Fan',1,'[{\"added\": {}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (13,'account','address'),(12,'account','creditcard'),(1,'admin','logentry'),(2,'auth','group'),(4,'auth','permission'),(3,'auth','user'),(11,'commerce','order'),(10,'commerce','orderitem'),(8,'commerce','product'),(9,'commerce','review'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'sites','site');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-09-24 22:25:53'),(2,'auth','0001_initial','2017-09-24 22:26:11'),(3,'account','0001_initial','2017-09-24 22:26:19'),(4,'admin','0001_initial','2017-09-24 22:26:25'),(5,'admin','0002_logentry_remove_auto_add','2017-09-24 22:26:25'),(6,'contenttypes','0002_remove_content_type_name','2017-09-24 22:26:26'),(7,'auth','0002_alter_permission_name_max_length','2017-09-24 22:26:26'),(8,'auth','0003_alter_user_email_max_length','2017-09-24 22:26:27'),(9,'auth','0004_alter_user_username_opts','2017-09-24 22:26:27'),(10,'auth','0005_alter_user_last_login_null','2017-09-24 22:26:28'),(11,'auth','0006_require_contenttypes_0002','2017-09-24 22:26:28'),(12,'auth','0007_alter_validators_add_error_messages','2017-09-24 22:26:28'),(13,'auth','0008_alter_user_username_max_length','2017-09-24 22:26:29'),(14,'commerce','0001_initial','2017-09-24 22:26:47'),(15,'sessions','0001_initial','2017-09-24 22:26:50'),(16,'sites','0001_initial','2017-09-24 22:26:52'),(17,'sites','0002_alter_domain_unique','2017-09-24 22:26:52'),(18,'commerce','0002_auto_20170925_2200','2017-09-26 03:36:43'),(19,'commerce','0003_auto_20170925_2204','2017-09-26 03:36:43'),(20,'commerce','0004_auto_20170927_1118','2017-09-27 16:18:50');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('5c5xawgxdpawhbu3st9nd5ahxul5ib6r','ZjhiMmRjY2M5NWIyN2Q5NDYzN2FhODNhODY5MWZmMzkwM2YzNGZjMDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYzllNmMxZTViZDc4ZjdkMjdkNTQ3ZTVhYTRjZjA5ZTFiYTZmN2Y0NyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-10-11 18:43:33');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (2,'pmwest.pythonanywhere.com','CompMart');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-27 13:44:19
