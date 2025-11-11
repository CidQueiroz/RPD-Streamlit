-- MySQL dump 10.13  Distrib 9.2.0, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: rpd_app_db
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `atividades`
--

DROP TABLE IF EXISTS `atividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `atividades` (
  `id_atividade` int NOT NULL AUTO_INCREMENT,
  `nome_atividade` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `periodo` enum('manha','tarde','noite') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'manha',
  `ativa` tinyint(1) NOT NULL DEFAULT '1',
  `usuario_fk` int NOT NULL,
  PRIMARY KEY (`id_atividade`),
  UNIQUE KEY `nome_atividade` (`nome_atividade`),
  KEY `fk_atividade_usuario` (`usuario_fk`),
  CONSTRAINT `fk_atividade_usuario` FOREIGN KEY (`usuario_fk`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=394 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atividades`
--

/*!40000 ALTER TABLE `atividades` DISABLE KEYS */;
INSERT INTO `atividades` VALUES (1,' Missão \'Explicador\': Dedicar 1 hora de suporte nos estudos/deveres das gêmeas.','tarde',1,1),(2,'Ativação: Beber 1 copo d\'água cheio ao acordar.','manha',1,1),(3,'Calibração: Fazer 5 minutos de respiração guiada ','manha',1,1),(4,'Curso DBT','manha',1,1),(5,'Logística Escolar: Buscar as gêmeas na escola.','tarde',1,1),(6,'Logística Terapêutica: Levar as gêmeas para suas terapias/atividades.','tarde',1,1),(7,'Marcar o \'x\' no seu \'D.Bordo\' para a AMV de estudo que você fez pela manhã.','noite',1,1),(8,'ORACLE NEXT EDUCATION','manha',1,1),(9,'Operações Domésticas: Executar 1 tarefa doméstica','tarde',1,1),(10,'Planejamento: Definir qual será a tarefa de estudo de amanhã','noite',1,1),(11,'Programação','manha',1,1),(12,'Projeto \'Caça-Preço\': Executar 1 bloco de 25 minutos de programação (Manhã)','manha',1,1),(13,'Projeto \'Caça-Preço\': Executar 1 bloco de 25 minutos de programação (Noite)','noite',1,1),(14,'Tarefa Doméstica','manha',0,1),(15,'Treinamento Principal: Executar 1 bloco de 25 minutos','manha',1,1),(16,'preencher 1 RPD com a \'Resposta Adaptativa\'. Se não houve, pule esta etapa.','noite',1,1);
/*!40000 ALTER TABLE `atividades` ENABLE KEYS */;

--
-- Table structure for table `diario_bordo`
--

DROP TABLE IF EXISTS `diario_bordo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diario_bordo` (
  `id_diario` int NOT NULL AUTO_INCREMENT,
  `data` datetime DEFAULT NULL,
  `usuario_fk` int DEFAULT NULL,
  `atividade_fk` int DEFAULT NULL,
  PRIMARY KEY (`id_diario`),
  KEY `usuario_fk` (`usuario_fk`),
  KEY `atividade_fk` (`atividade_fk`),
  CONSTRAINT `diario_bordo_ibfk_1` FOREIGN KEY (`usuario_fk`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `diario_bordo_ibfk_2` FOREIGN KEY (`atividade_fk`) REFERENCES `atividades` (`id_atividade`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diario_bordo`
--

/*!40000 ALTER TABLE `diario_bordo` DISABLE KEYS */;
INSERT INTO `diario_bordo` VALUES (17,'2025-08-11 00:00:00',1,4),(18,'2025-08-11 00:00:00',1,14),(19,'2025-08-12 00:00:00',1,11),(20,'2025-08-12 00:00:00',1,14),(21,'2025-08-15 00:00:00',1,11),(22,'2025-08-15 00:00:00',1,14),(23,'2025-08-17 00:00:00',1,4),(24,'2025-08-17 00:00:00',1,14),(25,'2025-08-20 00:00:00',1,11),(26,'2025-08-21 00:00:00',1,11),(27,'2025-08-21 00:00:00',1,8),(28,'2025-08-21 00:00:00',1,14),(29,'2025-08-22 00:00:00',1,8),(30,'2025-08-22 00:00:00',1,11),(31,'2025-08-23 00:00:00',1,4),(32,'2025-08-23 00:00:00',1,11);
/*!40000 ALTER TABLE `diario_bordo` ENABLE KEYS */;

--
-- Table structure for table `empresas`
--

DROP TABLE IF EXISTS `empresas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresas` (
  `id_empresa` int NOT NULL AUTO_INCREMENT,
  `nome_empresa` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_empresa`),
  UNIQUE KEY `nome_empresa` (`nome_empresa`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresas`
--

/*!40000 ALTER TABLE `empresas` DISABLE KEYS */;
INSERT INTO `empresas` VALUES (1,'CDK TECK');
/*!40000 ALTER TABLE `empresas` ENABLE KEYS */;

--
-- Table structure for table `estoque`
--

DROP TABLE IF EXISTS `estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoque` (
  `id_item` int NOT NULL AUTO_INCREMENT,
  `item` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `variacao` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quantidade` int NOT NULL,
  `preco` decimal(10,2) NOT NULL,
  `valor_total` decimal(10,2) GENERATED ALWAYS AS ((`quantidade` * `preco`)) STORED,
  `empresa_fk` int NOT NULL,
  PRIMARY KEY (`id_item`),
  KEY `fk_estoque_empresa` (`empresa_fk`),
  CONSTRAINT `fk_estoque_empresa` FOREIGN KEY (`empresa_fk`) REFERENCES `empresas` (`id_empresa`)
) ENGINE=InnoDB AUTO_INCREMENT=270 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque`
--

/*!40000 ALTER TABLE `estoque` DISABLE KEYS */;
INSERT INTO `estoque` (`id_item`, `item`, `variacao`, `quantidade`, `preco`, `empresa_fk`) VALUES (1,'Camisa','Flamengo',2,10.00,1),(2,'Cachorro','Laranja',4,5.00,1),(3,'Pulseira','Jade',2,10.00,1),(4,'Laço','pacotinho c/ 10',2,4.00,1),(5,'Camisa','Vasco',2,10.00,1),(6,'Camisa','Palmeiras',1,10.00,1),(7,'Cachorro','Rosa Transparente',3,5.00,1),(8,'Cachorro','Rosa Bolinha',1,5.00,1),(9,'Cachorro','Rosa Claro',2,5.00,1),(10,'Cachorro','Marfim',2,5.00,1),(11,'Cachorro','Perola',4,5.00,1),(12,'Cachorro','Verde',4,5.00,1),(13,'Camisa','Botafogo',3,10.00,1),(14,'Brincos','Azul (Alegria - Amor)',0,2.00,1),(15,'Brincos','Rosa (Benção)',1,2.00,1),(16,'Prendedor','Celular',1,10.00,1),(17,'Camisa','Flamengo - Rosa',1,10.00,1),(18,'Garrafa','Rosa',1,10.00,1),(19,'Garrafa','Azul',1,10.00,1),(20,'Cachorrão','Colorido',1,10.00,1),(21,'Cachorro','Marrom pequeno',2,5.00,1),(22,'Cachorro','Azul bolinha',1,5.00,1),(23,'Pulseira','Amarela-Marrom',1,5.00,1),(24,'Pulseira','Amarela',1,5.00,1),(25,'Brincos','Branco',1,5.00,1),(26,'Brincos','Verde',0,5.00,1),(27,'Pulseira','Branca',2,5.00,1),(28,'Pulseira','Azul',3,5.00,1),(29,'Colar','Capivara',1,10.00,1),(30,'Colar','Coração Colorido',1,10.00,1),(31,'Colar','Transparente',1,10.00,1),(32,'Brincos','Marrom-madeira',1,5.00,1),(33,'Pulseira','Branca-Rosa-Laranja',1,5.00,1),(34,'Pulseira','Vermelha-Prata',1,5.00,1),(35,'Pulseira','Colorido',1,5.00,1),(36,'Pulseira','Bolinha Colorida',2,5.00,1),(37,'Pulseira','Bolinha Azul',1,5.00,1),(38,'Conjunto','Verde',1,15.00,1),(39,'Camisa','Fluminense',1,10.00,1),(40,'Prendedor','Chiquinha  c/ nome',1,15.00,1),(41,'Prendedor','Chiquinha  s/ nome',1,10.00,1),(42,'Prendedor','Pingente',1,5.00,1),(43,'Pulseira','Lacinho',1,5.00,1),(44,'Pulseira','Borboleta-flor-mão',1,5.00,1),(45,'Pulseira','Golfinho coração',1,5.00,1),(46,'Cachorro','Vermelho',1,5.00,1),(47,'Prendedor','Xuxinha bolinha',3,0.50,1);
/*!40000 ALTER TABLE `estoque` ENABLE KEYS */;

--
-- Table structure for table `log_pod_diario`
--

DROP TABLE IF EXISTS `log_pod_diario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_pod_diario` (
  `id_log` int NOT NULL AUTO_INCREMENT,
  `data` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `usuario_fk` int DEFAULT NULL,
  `atividade_fk` int DEFAULT NULL,
  PRIMARY KEY (`id_log`),
  KEY `usuario_fk` (`usuario_fk`),
  KEY `tarefa_fk` (`atividade_fk`),
  CONSTRAINT `log_pod_diario_ibfk_1` FOREIGN KEY (`usuario_fk`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `log_pod_diario_ibfk_2` FOREIGN KEY (`atividade_fk`) REFERENCES `atividades` (`id_atividade`)
) ENGINE=InnoDB AUTO_INCREMENT=1185 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_pod_diario`
--

/*!40000 ALTER TABLE `log_pod_diario` DISABLE KEYS */;
INSERT INTO `log_pod_diario` VALUES (207,'2025-08-20 00:00:00',1,1,2),(209,'2025-08-20 00:00:00',1,1,15),(210,'2025-08-20 00:00:00',1,1,12),(211,'2025-08-20 00:00:00',1,1,5),(212,'2025-08-20 00:00:00',1,1,1),(213,'2025-08-20 00:00:00',1,1,9),(214,'2025-08-20 00:00:00',1,1,6),(215,'2025-08-20 00:00:00',1,1,13),(217,'2025-08-20 00:00:00',1,1,16),(219,'2025-08-21 00:00:00',1,1,2),(220,'2025-08-22 00:00:00',1,1,5),(221,'2025-08-21 00:00:00',1,1,15),(222,'2025-08-21 00:00:00',1,1,12),(223,'2025-08-21 00:00:00',1,1,5),(224,'2025-03-09 00:00:00',1,1,1),(225,'2025-08-21 00:00:00',1,1,9),(226,'2025-08-21 00:00:00',1,1,6),(227,'2025-08-21 00:00:00',1,1,13),(228,'2025-08-25 00:00:00',1,1,5),(229,'2025-08-21 00:00:00',1,1,16),(230,'2025-08-22 00:00:00',1,1,2),(231,'2025-08-22 00:00:00',1,1,15),(232,'2025-08-22 00:00:00',1,1,12),(233,'2025-08-22 00:00:00',1,1,5),(234,'2025-08-22 00:00:00',1,1,1),(236,'2025-08-22 00:00:00',1,1,6),(237,'2025-08-22 00:00:00',1,1,13),(241,'2025-08-23 00:00:00',1,1,2),(243,'2025-08-23 00:00:00',1,1,15),(245,'2025-01-09 00:00:00',1,1,1),(247,'2025-08-25 00:00:00',1,1,6),(248,'2025-08-23 00:00:00',1,1,13),(250,'2025-08-20 00:00:00',1,1,16),(252,'2025-08-26 00:00:00',1,1,5),(253,'2025-08-27 00:00:00',1,1,5),(254,'2025-08-28 00:00:00',1,1,5),(255,'2025-08-29 00:00:00',1,1,5),(256,'2025-02-09 00:00:00',1,1,5),(257,'2025-03-09 00:00:00',1,1,5),(258,'2025-08-27 00:00:00',1,1,6),(259,'2025-08-28 00:00:00',1,1,6),(260,'2025-08-29 00:00:00',1,1,6),(261,'2025-03-09 00:00:00',1,1,2),(262,'2025-04-09 00:00:00',1,1,2),(263,'2025-08-25 00:00:00',1,1,2),(264,'2025-08-28 00:00:00',1,1,2),(265,'2025-04-09 00:00:00',1,1,12),(266,'2025-08-23 00:00:00',1,1,12),(267,'2025-08-24 00:00:00',1,1,12),(268,'2025-08-25 00:00:00',1,1,12),(269,'2025-08-26 00:00:00',1,1,12),(270,'2025-08-27 00:00:00',1,1,12),(271,'2025-08-28 00:00:00',1,1,12),(272,'2025-08-29 00:00:00',1,1,12),(273,'2025-08-30 00:00:00',1,1,12),(274,'2025-08-31 00:00:00',1,1,12),(275,'2025-01-09 00:00:00',1,1,12),(276,'2025-02-09 00:00:00',1,1,12),(277,'2025-03-09 00:00:00',1,1,12),(278,'2025-08-24 00:00:00',1,1,15),(279,'2025-08-25 00:00:00',1,1,15),(280,'2025-08-26 00:00:00',1,1,15),(281,'2025-08-27 00:00:00',1,1,15),(282,'2025-08-28 00:00:00',1,1,15),(283,'2025-08-29 00:00:00',1,1,15),(284,'2025-08-30 00:00:00',1,1,15),(285,'2025-08-31 00:00:00',1,1,15),(286,'2025-01-09 00:00:00',1,1,15),(287,'2025-02-09 00:00:00',1,1,15),(288,'2025-03-09 00:00:00',1,1,15),(292,'2025-09-04 08:46:18',1,1,12),(313,'2025-09-04 08:50:00',1,1,2),(325,'2025-09-04 08:50:40',1,1,2),(327,'2025-09-04 08:50:40',1,1,15),(337,'2025-08-17 00:00:00',2,1,1),(345,'2025-08-17 00:00:00',2,1,1),(346,'2025-08-17 00:00:00',3,1,1),(347,'2025-08-17 00:00:00',15,1,1),(361,'2025-08-14 00:00:00',10,1,1),(362,'2025-08-14 00:00:00',10,1,1),(363,'2025-08-14 00:00:00',10,1,1),(381,'2025-08-15 00:00:00',10,1,1),(382,'2025-08-15 00:00:00',2,1,1),(383,'2025-08-15 00:00:00',3,1,1),(384,'2025-08-15 00:00:00',15,1,1),(398,'2025-08-16 00:00:00',2,1,1),(399,'2025-08-16 00:00:00',3,1,1),(400,'2025-08-16 00:00:00',15,1,1),(411,'2025-08-18 00:00:00',2,1,1),(413,'2025-08-18 00:00:00',15,1,1),(414,'2025-08-18 00:00:00',12,1,1),(415,'2025-08-18 00:00:00',5,1,1),(417,'2025-08-18 00:00:00',9,1,1),(418,'2025-08-18 00:00:00',6,1,1),(419,'2025-08-18 00:00:00',13,1,1),(421,'2025-08-19 00:00:00',3,1,1),(422,'2025-08-19 00:00:00',1,1,1),(423,'2025-08-20 00:00:00',2,1,1),(424,'2025-08-19 00:00:00',3,1,1),(425,'2025-08-20 00:00:00',15,1,1),(426,'2025-08-20 00:00:00',12,1,1),(427,'2025-08-20 00:00:00',5,1,1),(428,'2025-08-20 00:00:00',1,1,1),(429,'2025-08-20 00:00:00',9,1,1),(430,'2025-08-20 00:00:00',6,1,1),(431,'2025-08-20 00:00:00',13,1,1),(432,'2025-08-19 00:00:00',7,1,1),(433,'2025-08-20 00:00:00',16,1,1),(434,'2025-08-19 00:00:00',10,1,1),(435,'2025-08-21 00:00:00',2,1,1),(436,'2025-08-22 00:00:00',5,1,1),(437,'2025-08-21 00:00:00',15,1,1),(438,'2025-08-21 00:00:00',12,1,1),(439,'2025-08-21 00:00:00',5,1,1),(440,'2025-03-09 00:00:00',1,1,1),(441,'2025-08-21 00:00:00',9,1,1),(442,'2025-08-21 00:00:00',6,1,1),(443,'2025-08-21 00:00:00',13,1,1),(444,'2025-08-25 00:00:00',5,1,1),(445,'2025-08-21 00:00:00',16,1,1),(446,'2025-08-22 00:00:00',2,1,1),(447,'2025-08-22 00:00:00',15,1,1),(448,'2025-08-22 00:00:00',12,1,1),(449,'2025-08-22 00:00:00',5,1,1),(450,'2025-08-22 00:00:00',1,1,1),(654,'2025-09-07 18:31:09',1,1,2),(658,'2025-09-07 18:31:09',1,1,11),(660,'2025-09-07 18:31:09',1,1,14),(661,'2025-09-07 18:31:09',1,1,15),(669,'2025-09-07 18:31:10',1,1,13);
/*!40000 ALTER TABLE `log_pod_diario` ENABLE KEYS */;

--
-- Table structure for table `respostas`
--

DROP TABLE IF EXISTS `respostas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `respostas` (
  `id_resposta` int NOT NULL AUTO_INCREMENT,
  `data_hora` datetime DEFAULT NULL,
  `situacao` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pensamento` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `emocao` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `conclusao` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `resultado` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `usuario_fk` int DEFAULT NULL,
  PRIMARY KEY (`id_resposta`),
  KEY `usuario_fk` (`usuario_fk`),
  CONSTRAINT `respostas_ibfk_1` FOREIGN KEY (`usuario_fk`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respostas`
--

/*!40000 ALTER TABLE `respostas` DISABLE KEYS */;
INSERT INTO `respostas` VALUES (22,'2025-05-16 19:45:13','Minha mae me pediu ajuda para colocar algumas lampadas e eu perguntei \"agora\" entao ela disse \"deixa\".','Ela entendeu como má vontade minha.','Frustrado 50','ela estava certa 100','Eu devia ter ido fazer logo, pois fui meio preguiçoso',1),(23,'2025-05-17 08:41:10','Gemeas se alarmando pq o Mayque passou na frente de um carro (e por qualquer coisa)','frescura e drama delas','raiva, irritação 80','elas tem um problema de saude','Eu devia ser mais paciente com elas e entender melhor a condição delas',1),(24,'2025-05-18 10:05:25','minha mae me pede algo e não consigo ter tempo para as minhas as coisas','ela faz de proposito','irritação, preguiça 60','ela é energica, mas não tem a mesma saude q antes','preciso conversar com ela pra alinhar uns pontos',1),(25,'2025-05-26 07:47:07','uma menina sentou do meu lado no onibus','puxar assunto','timidez, vergonha 100','eu não sabia qual era a dela e so poderia saber conversando','eu podia ter falado qq coisa pra quebrar o gelo ou descobrir algo',1),(26,'2025-05-27 14:37:37','Fui na casa da minha mae e ela mal me respondeu e saiu com as meninas.','q eu tinha feito algo errado (90)','preocupação pra descobrir oq eu teria feito (50).','ela pode estar com pressa, pode estar zangada com as meninas.','alivio por ficar em casa sozinho (50)',1),(27,'2025-05-31 18:48:50','Hozanah perdeu o cartao de passagem e de identificação pois estava andando na rua de brincadeira. briguei muito com ela e com Cleópatra tbm.','elas sao inconsequentes e so fazem merda (50-50)','raiva 50 irritação 50','elas são crianças e é normal se comportarem assim e eventualmente aprontarem. 100','(50-50) Continuo achando q elas são assim, porém tentarei ser mais tolerante e brigar de forma menos efusiva.',1),(28,'2025-05-31 23:58:32','Liguei para minha filha as 14h e ela não atendeu. Depois tentei novamente às 20h.','Meu primeiro pensamento foi que a mãe dela desligou o celular para que eu não falasse com minha filha.','Fiquei chateado (60), enciumado (30), irritado (10).','De repente o telefone descarregou ou estava sem rede. (20)','Ela pode ou não ter feito de propósito, e eu tenho que dar o benefício da dívida e não sofrer por algo que não sei. 100',1),(29,'2025-06-02 14:13:07','me senti mal durante o final de semana (01/06), minha mae e as gemeas vieram passar o dia aqui','nao queria ninguem aqui perto, eu estava me sentindo mal e so queria ficar quietinho','tristeza por nao poder dizer nao pra elas, frustração (80)','elas estavam querendo me ajudar (100)','aceitar a ajuda delas',1),(30,'2025-06-02 23:59:33','Uma amiga muito próxima postou no story do WhatsApp que sente saudade do casamento e daria tudo pra voltar ao que era antes ','Senti empatia e queria o mesmo','Tristeza por ela e por mim, 90','Não podemos voltar ao passado, mas ainda podemos escrever o futuro. 50','Continuo com o mesmo pensamento, porém crendo que no futuro minha mente vai mudar',1),(31,'2025-06-05 03:36:59','Lembro de um fato de presenciar uma luta entre Brock Lesnar vs Frank Mir, onde o primeiro nocauteou o segundo com ferocidade ','Penso que não é na minha natureza agredir alguém ou que seria incapaz de acertar um soco na face de alguém. E isso me torna fraco perante as mulheres e incapaz de fornecer proteção que elas procuram','Frustração, impotência, Inferioridade, Preocupação, Vergonha, Tristeza, Medo ','Força física não está necessariamente ligada a proteção. Existe outras formas de proteger sem precisar agredir ninguém.','Preciso entender que comando por voz, presença, inteligência são e podem ser mais eficazes do que força bruta.',1),(32,'2025-06-05 03:39:32','As gêmeas não conseguem fazer absolutamente nada sem instrução','Se vira, porra','Tédio, irritação 80','Elas são constantemente polidas pela minha mãe que as impede de fazer muita coisa e ficam com medo de quem errado','Mais paciência. Ninguém nasce sabendo e elas vão aprender com o tempo. ',1),(33,'2025-06-06 14:00:13','eu sempre coloco roupa pra lavar na maquina aqui de casa. FDS minha mae veio e colocou roupa pra lavar. Durante a semana, eu fui colocar e percebi que o cano estava quebrado e vazou agua pela casa toda;','que minha mae quebrou e nao falou nada (uma evidencia é que tinha umna garrafa em cima do cano que parecia cumprir o papel de estancar o vazamento)','raiva 80','minha mae pode nao ter visto ou ter tentado consertar sem me preocupar.','Vou tentar consertar e conversar com ela para me avisar, de modo que eu nao seja pego desprevinido posteriormente',1),(34,'2025-06-07 10:35:15','A mãe da minha filha aceitou que a gente se visse o combinado era que eu fosse entrar na fila para poder pegar voucher para andarmos de balão acontece que estava muito cheio não conseguimos o voucher e o balão subia muito baixo','Meu primeiro pensamento foi de que ela fez de propósito para eu perder tempo nessa fila e ficar menos tempo com minha filha','Frustração, irritação, vergonha. Medo','O evento estar cheio não é culpa dela, o balão não subir tanto quanto eu imaginei também não é culpa dela','Ainda permaneceu a frustração e a irritação pelo tempo perdido porém eu sei que a culpa não é dela e não acredito que ela tenha feito de propósito tentar redirecionar esse essa frustração para outra oportunidade de encontro',1),(35,'2025-08-13 08:02:48','Minha mae mexendo no encanamento da piscina','que ela estava inventando historia e  trabalho era inutil','raiva e irritação (50)','Que eu deveria dar o espaço dela e deixar ela fazer do jeito que está acostumada','Retirado',1),(36,'2025-08-13 09:07:13','cleopatra passando o dia inteiro para arrumar o quarto, desde 10h ate meia noite','pois ela tem tempo e fica miando (chorando) e enrolando e acaba nao fazendo','extrema irritação','Que eu devo ser compreensivo e ajudá-la para que ela consiga concluir a tarefa ','Retirado',1),(37,'2025-08-15 10:42:02','minha mae saiu com meu cachorro, mayque, pra rua e ele quase foi atropelado. eu pedi pra q ela nao saisse mais com ele pela manhã sem mim e ela nao gostou. disse q nao cuidaria mais dele','que ela está sendo infantil. respondi com raiva e ignorando','irritação, raiva, grosseria','ter explicado com mais calma, ou pedido para que ela tomasse mais cuidado com ele na rua, aproveitando pra explicar o comportamento dele','Retirado',1),(38,'2025-08-18 12:44:26','minha mae reclamando do mayque, sendo que ela tá com ele ha 3 anos e agora ta com essa.','que ela está fazendo pra implicar e está com raiva querendo ter a razão','raiva e angustia','assumir a responsabilidade pelo cachorro e não discutir com ela.','Retirado',1),(39,'2025-08-20 23:59:22','Vi a moça hoje, tive a oportunidade de falar, mas congelei e não fiz nada.','\"Eu não consigo\", \"Foi vergonhoso\", \"Perdi a oportunidade\".','Vergonha, frustração, raiva de mim mesmo','O padrão de congelamento de décadas foi ativado. Isso era esperado. A missão não falhou; ela apenas revelou o nível de resistência do inimigo. A vitória de hoje não era falar com ela, mas sim analisar por que não falei. A próxima tentativa será mais informada.','Retirado',1),(40,'2025-08-24 14:19:26','Minha mãe foi pra igreja no domingo de manhã e combinou comigo que iríamos na outra casa resolver uns problemas que tem lá. Ela foi pra igreja e depois voltou pra casa sem me escutar e eu fui na outra casa sozinho','Ela muda de ideia o tempo todo e sem avisar conforme a vontade dele','Frustração, desconforto ','Conversar com tua e explicar a importância de ser avisado antes das mudanças de plano ou explicar a importância de seguir o combinado','Retirado',1),(41,'2025-08-31 14:02:50','Hoje eu vi três casais no mercado que tinha o mesmo perfil a menina era muito bonita e o homem era esquisito gordo ou feio ou estranho','Meu primeiro pensamento foi de porque eles conseguem e eu não consigo estou sozinho há um ano','Frustração tristeza desânimo baixa autoestima','Pensei que eu também consigo que um dia isso vai acontecer comigo','Retirado',1),(42,'2025-09-01 10:17:44','Hoje eu fui tirar uma xerox e na loja a atendente era muito simpática e estávamos conversando naturalmente eu tentando ser simpático também e quanto percebia eu comecei a falar que não entendia o fato de em 2025 ainda pedirem foto 3 por 4 entretanto nesse momento eu percebi que eu estava em uma loja que tirava foto 3 por 4 e fazia impressões, fiquei em silêncio imediatamente e ficou um clima meio estranho pelo que eu tinha acabado de falar','Eu pensei imediatamente que eu era burro e que não sabia me comunicar só falo merda','Vergonha','Eu deveria ter mudado de assunto e agir como se nada tivesse acontecido porque esse tipo de coisa acontece com qualquer um','Retirado',1),(44,'2025-09-08 19:40:59','dei match com uma menina do espirito santo','nao vao dar em nada','frustração','Não prevejo o futuro. de repente, é uma oportunidade de trabalhar minha comunicação.','Retirado',1),(59,'2025-09-09 09:14:07','acordei cansada','nao vou sair da cama','preguiça','preciso me movimentoar','Retirado',2),(60,'2025-09-09 09:20:47','acordei com cansada','nao quero sair da cama','preguiça','preciso ir pra escola','Retirado',3);
/*!40000 ALTER TABLE `respostas` ENABLE KEYS */;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `senha` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nome` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `acesso_dev_pessoal` tinyint(1) NOT NULL DEFAULT '0',
  `empresa_fk` int NOT NULL,
  `is_staff` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `fk_usuario_empresa` (`empresa_fk`),
  CONSTRAINT `fk_usuario_empresa` FOREIGN KEY (`empresa_fk`) REFERENCES `empresas` (`id_empresa`)
) ENGINE=InnoDB AUTO_INCREMENT=670 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'cid','$2b$12$IBdk6l8Nv6O/qTD1lVoFJOOUyQSMuWSrcutqz249UrzojRuXBnSUK','Cidirclay Queiroz',1,1,1),(2,'cleo','$2b$12$QVLfZYaT2xc5/Mptd8BD7OLvbLCK1XlHZOUg9c23HPO5xnHooiPpa','Cleópatra Santos',1,1,1),(3,'quiopa','$2b$12$sErqOiGkX6JFK2SK8uvnCuo6/evdsiN/8fDaKAPk4JXpVVRAE5na2','Cleópatra Lima',1,1,0),(4,'zanah','$2b$12$/gGb1XX/F4Pb8eakjpJnDeQkeROib1VTB23XkWsLZBjNBDHeg6mMC','Hozanah Lima',1,1,0),(46,'Mayque','$2b$12$sQwSEXO9wr5FDL7.ncSdQORf6XdkqyXTCQ6GoVLWnSL6zpveGLrbO','Mayquinho Malvadao',1,1,0);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;

--
-- Table structure for table `vendas`
--

DROP TABLE IF EXISTS `vendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendas` (
  `id_venda` int NOT NULL AUTO_INCREMENT,
  `data_hora` datetime NOT NULL,
  `quantidade` int NOT NULL,
  `preco_unitario` decimal(10,2) NOT NULL,
  `preco_total` decimal(10,2) GENERATED ALWAYS AS ((`quantidade` * `preco_unitario`)) STORED,
  `vendedor_fk` int DEFAULT NULL,
  `estoque_fk` int DEFAULT NULL,
  `empresa_fk` int NOT NULL,
  PRIMARY KEY (`id_venda`),
  KEY `vendedor_fk` (`vendedor_fk`),
  KEY `estoque_fk` (`estoque_fk`),
  KEY `fk_vendas_empresa` (`empresa_fk`),
  CONSTRAINT `fk_vendas_empresa` FOREIGN KEY (`empresa_fk`) REFERENCES `empresas` (`id_empresa`),
  CONSTRAINT `vendas_ibfk_1` FOREIGN KEY (`vendedor_fk`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `vendas_ibfk_2` FOREIGN KEY (`estoque_fk`) REFERENCES `estoque` (`id_item`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendas`
--

/*!40000 ALTER TABLE `vendas` DISABLE KEYS */;
INSERT INTO `vendas` (`id_venda`, `data_hora`, `quantidade`, `preco_unitario`, `vendedor_fk`, `estoque_fk`, `empresa_fk`) VALUES (7,'2025-07-16 18:53:09',1,10.00,2,1,1),(8,'2025-07-16 19:02:09',1,10.00,3,1,1),(9,'2025-07-16 19:04:47',2,4.00,4,4,1),(10,'2025-07-25 15:28:12',1,4.00,3,4,1),(11,'2025-07-25 15:28:32',2,10.00,3,1,1),(12,'2025-07-25 15:28:58',1,10.00,3,1,1),(26,'2025-09-09 13:17:15',1,2.00,4,14,1),(27,'2025-09-09 13:20:49',1,5.00,4,26,1);
/*!40000 ALTER TABLE `vendas` ENABLE KEYS */;

--
-- Dumping routines for database 'rpd_app_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 17:37:03
