-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: ege_project
-- ------------------------------------------------------
-- Server version	5.5.25

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
-- Table structure for table `exercises`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exercises` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text,
  `type` enum('test','written') NOT NULL,
  `instructions` text,
  `correct_answer` text,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `exercises_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercises`
--

LOCK TABLES `exercises` WRITE;
/*!40000 ALTER TABLE `exercises` DISABLE KEYS */;
INSERT INTO `exercises` VALUES (1,1,'Задача на производную','Найдите производную функции f(x)=3x^2-4x+1','test','Введите ваш ответ в поле ниже.','6x-4'),(2,1,'Интегрирование функций','Вычислите интеграл функции f(x)=2x','written','Подробно распишите решение и загрузите фото работы.',NULL),(3,2,'Тест на правописание корней','Выберите верный вариант написания слова: \"г..реть\"','test','Введите букву, которая пропущена.','о'),(4,2,'Сочинение-рассуждение','Напишите сочинение на тему: \"Важность чтения в жизни человека\".','written','Загрузите ваше сочинение файлом.',NULL),(5,3,'Перевод из двоичной системы','Переведите число 10101 из двоичной в десятичную систему.','test','Введите число в поле ответа.','21'),(6,3,'Задача на сортировку данных','Опишите алгоритм сортировки выбором.','written','Загрузите текстовый файл с описанием алгоритма.',NULL),(7,4,'Дата начала Великой Отечественной войны','Укажите дату начала Великой Отечественной войны.','test','Введите дату в формате ДД.ММ.ГГГГ','22.06.1941'),(8,4,'Эссе о реформах Петра I','Напишите эссе на тему \"Последствия реформ Петра I для России\".','written','Загрузите файл с вашим эссе.',NULL);
/*!40000 ALTER TABLE `exercises` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `results`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `exercise_id` int(11) NOT NULL,
  `score` int(11) DEFAULT NULL,
  `comment` text,
  `date_checked` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `exercise_id` (`exercise_id`),
  CONSTRAINT `results_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `results_ibfk_2` FOREIGN KEY (`exercise_id`) REFERENCES `exercises` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `results`
--

LOCK TABLES `results` WRITE;
/*!40000 ALTER TABLE `results` DISABLE KEYS */;
INSERT INTO `results` VALUES (1,4,1,0,'Ответ неверный. Правильный ответ: 6x-4','2025-03-31 05:39:23');
/*!40000 ALTER TABLE `results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `level` enum('basic','advanced') DEFAULT 'basic',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` VALUES (1,'Математика','Подготовка к профильному ЕГЭ по математике','advanced'),(2,'Русский язык','Подготовка к ЕГЭ по русскому языку','basic'),(3,'Информатика','Подготовка к ЕГЭ по информатике и ИКТ','advanced'),(4,'История','Подготовка к ЕГЭ по истории','basic');
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submissions`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `submissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `exercise_id` int(11) NOT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `answer_text` text,
  `date_submitted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pending','reviewed') DEFAULT 'pending',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `exercise_id` (`exercise_id`),
  CONSTRAINT `submissions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `submissions_ibfk_2` FOREIGN KEY (`exercise_id`) REFERENCES `exercises` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submissions`
--

LOCK TABLES `submissions` WRITE;
/*!40000 ALTER TABLE `submissions` DISABLE KEYS */;
INSERT INTO `submissions` VALUES (1,4,1,NULL,'2','2025-03-31 05:39:23','pending');
/*!40000 ALTER TABLE `submissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `theory`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `theory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `theory_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `theory`
--

LOCK TABLES `theory` WRITE;
/*!40000 ALTER TABLE `theory` DISABLE KEYS */;
INSERT INTO `theory` VALUES (1,1,'Производная функции','<h3>Производная функции</h3><p>Производная функции описывает скорость изменения функции в точке. Формула производной: <strong>f\'(x)=lim(h→0)(f(x+h)-f(x))/h</strong></p><p>Примеры: производная функции <em>f(x)=x²</em> равна <strong>2x</strong>.</p>'),(2,1,'Интегралы','<h3>Интегралы</h3><p>Интеграл — это операция, обратная дифференцированию. Определённый интеграл вычисляет площадь под кривой функции. Например: <strong>∫2xdx = x² + C</strong>.</p>'),(3,2,'Правописание корней с чередованием','<h3>Правописание корней с чередованием</h3><p>В русском языке корни с чередованием зависят от условий: ударения, последующего согласного и других факторов. Примеры: гореть – загар, мерить – замереть.</p>'),(4,2,'Слитное и раздельное написание НЕ с частями речи','<h3>Слитное и раздельное написание НЕ</h3><p>НЕ пишется слитно, если без НЕ слово не употребляется. Пример: ненавидеть. Раздельно пишется в случае противопоставления или наличия союзов: вовсе не интересно.</p>'),(5,3,'Двоичная система счисления','<h3>Двоичная система счисления</h3><p>Система счисления, в которой используются только цифры 0 и 1. Например, десятичное число 5 записывается в двоичной системе как 101.</p>'),(6,3,'Алгоритмы сортировки','<h3>Алгоритмы сортировки</h3><p>Алгоритмы сортировки упорядочивают элементы массива. Популярные алгоритмы: сортировка пузырьком, выбором, вставками.</p>'),(7,4,'Реформы Петра I','<h3>Реформы Петра I</h3><p>Реформы Петра I включали в себя военные, административные и культурные преобразования. Введение табели о рангах, создание флота.</p>'),(8,4,'Великая Отечественная война','<h3>Великая Отечественная война</h3><p>Ключевые события войны: начало войны (22 июня 1941 года), Сталинградская битва, битва на Курской дуге и взятие Берлина.</p>');
/*!40000 ALTER TABLE `theory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('student','admin') DEFAULT 'student',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Иван Иванов','ivan@example.com','password123','student'),(3,'Администратор','admin@example.com','adminpass','admin'),(4,'Илья Шихов','nefritful@gmail.com','123123','student');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ege_project'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-01  2:22:03
