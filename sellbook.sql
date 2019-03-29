-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 29, 2019 at 03:17 PM
-- Server version: 5.7.24-0ubuntu0.18.04.1
-- PHP Version: 7.2.10-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sellbook`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `book_id` varchar(25) NOT NULL,
  `title` varchar(50) NOT NULL,
  `author` varchar(30) NOT NULL,
  `edition` int(3) DEFAULT NULL,
  `price` int(11) NOT NULL,
  `uploader` varchar(40) NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `branch` varchar(33) NOT NULL,
  `status` text NOT NULL,
  `img` longblob,
  `sem` int(11) NOT NULL,
  `desp` varchar(145) DEFAULT NULL,
  `photo` blob
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`book_id`, `title`, `author`, `edition`, `price`, `uploader`, `rating`, `branch`, `status`, `img`, `sem`, `desp`, `photo`) VALUES
('10602278', 'Database Managment', 'navathe', 20, 300, 'shrihariskulkarni8@gmail.com', 59, 'IS', 'available', NULL, 2, NULL, NULL),
('17331578', 'Software Engineering', 'Rajib Mall', NULL, 450, 'skshriharik@gmail.com', 44, 'IS', 'available', NULL, 5, NULL, NULL),
('18032932', 'Database Managment', 'navathe', NULL, 250, 'shrihariskulkarni8@gmail.com', 59, 'IS', 'available', NULL, 2, NULL, NULL),
('18849550', 'Database Managment', 'navathe', NULL, 213, 'shrihariskulkarni8@gmail.com', 59, 'IS', 'available', NULL, 2, NULL, NULL),
('20200532', 'Anim omnis exercitat', 'Dolorem culpa est ', NULL, 462, 'skshriharik@gmail.com', 56, 'IS', 'booked', NULL, 42, NULL, NULL),
('21043653', 'Recusandae Sit sit', 'Architecto facere ex', NULL, 174, 'shriharisk.is17@rvce.edu.in', 96, 'IS', 'available', NULL, 98, NULL, NULL),
('21086626', 'Database Managment', 'navathe', NULL, 250, 'shrihariskulkarni8@gmail.com', 59, 'IS', 'available', NULL, 2, NULL, NULL),
('23628556', 'Software Engineering', 'Rajib Mall', NULL, 200, 'skshriharik@gmail.com', 44, 'IS', 'available', NULL, 5, NULL, NULL),
('27427580', 'Software Engineering', 'Rajib Mall', NULL, 250, 'skshriharik@gmail.com', 44, 'IS', 'available', NULL, 5, NULL, NULL),
('35579443', 'Et culpa quisquam t', 'Fugiat laborum modi ', NULL, 441, 'skshriharik@gmail.com', 78, 'IS', 'available', NULL, 59, NULL, NULL),
('47870075', 'Software Engineering', 'Rajib Mall', NULL, 441, 'skshriharik@gmail.com', 78, 'IS', 'available', NULL, 59, NULL, NULL),
('71810805', 'Officiis accusamus u', 'Sunt rem est nemo o', NULL, 364, 'skshriharik@gmail.com', 45, 'TE', 'available', NULL, 5, NULL, NULL),
('85746230', 'Software Engineering', 'Rajib Mall', NULL, 450, 'skshriharik@gmail.com', 44, 'IS', 'available', NULL, 5, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_email` varchar(40) NOT NULL,
  `b_id` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_email`, `b_id`) VALUES
('shriharisk.is17@rvce.edu.in', '18032932'),
('shriharisk.is17@rvce.edu.in', '18849550'),
('shriharisk.is17@rvce.edu.in', '21086626');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `title` text,
  `author` text,
  `reviewby` varchar(45) DEFAULT NULL,
  `comments` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`title`, `author`, `reviewby`, `comments`) VALUES
(NULL, NULL, 'shrihariskulkarni8@gmail.com', '3 is the review'),
('title', 'author1', 'shrihariskulkarni8@gmail.com', 'this is 2nd review\r\n'),
('title', '2', 'shrihariskulkarni8@gmail.com', 'this is the best book i have ever used .. lovely explination');

-- --------------------------------------------------------

--
-- Table structure for table `sold`
--

CREATE TABLE `sold` (
  `book_id` varchar(25) NOT NULL,
  `buyer` varchar(40) NOT NULL,
  `seller` varchar(40) NOT NULL,
  `status` text NOT NULL,
  `date` date NOT NULL,
  `tran_id` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `email` varchar(30) NOT NULL,
  `user_id` varchar(20) DEFAULT NULL,
  `full_name` varchar(45) NOT NULL,
  `branch` varchar(30) NOT NULL,
  `reg_date` date DEFAULT NULL,
  `phone` bigint(13) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`email`, `user_id`, `full_name`, `branch`, `reg_date`, `phone`) VALUES
('shriharisk.is17@rvce.edu.in', '6', 'S S Kulkarni', 'IS', '2019-02-18', 8123654654),
('shrihariskulkarni8@gmail.com', '2', 'Shrihari Kulkarni', 'IS', NULL, 8123452478),
('skshriharik@gmail.com', '3', 'Nikhil K', 'IS', '2019-02-18', 8123654654),
('srevie11@sphinn.com', '38', 'Sydney Revie', 'IN', '2018-12-09', 7381837674),
('tschoffler1q@arstechnica.com', '63', 'Tommie Schoffler', 'IN', '2018-04-16', 9343443451),
('ttrunchionz@last.fm', '36', 'Toby Trunchion', 'IN', '2018-08-06', 1192159046),
('wcawkillw@drupal.org', '33', 'Willamina Cawkill', 'IN', '2019-03-11', 9299251900),
('ydurtnall2@google.pl', '3', 'Yves Durtnall', 'IN', '2018-12-12', 9919200743),
('zshuttee@1688.com', '15', 'Zsazsa Shutte', 'IN', '2019-02-19', 7872428147);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`book_id`),
  ADD KEY `uploader` (`uploader`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD KEY `cart_email` (`cart_email`);

--
-- Indexes for table `sold`
--
ALTER TABLE `sold`
  ADD PRIMARY KEY (`tran_id`),
  ADD KEY `buyer` (`buyer`),
  ADD KEY `seller` (`seller`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sold`
--
ALTER TABLE `sold`
  MODIFY `tran_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`uploader`) REFERENCES `users` (`email`);

--
-- Constraints for table `sold`
--
ALTER TABLE `sold`
  ADD CONSTRAINT `sold_ibfk_1` FOREIGN KEY (`buyer`) REFERENCES `users` (`email`),
  ADD CONSTRAINT `sold_ibfk_2` FOREIGN KEY (`seller`) REFERENCES `users` (`email`),
  ADD CONSTRAINT `sold_ibfk_3` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
