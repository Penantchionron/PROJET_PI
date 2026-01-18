-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 18, 2026 at 11:41 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `math_pour_tous`
--

-- --------------------------------------------------------

--
-- Table structure for table `chats`
--

CREATE TABLE `chats` (
  `id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chats`
--

INSERT INTO `chats` (`id`, `title`, `user_id`, `created_at`) VALUES
(15, '**Deux côtés égaux**', 3, '2026-01-18 20:47:21'),
(16, 'Nouveau chat', 3, '2026-01-18 21:04:41');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `role` varchar(20) NOT NULL,
  `content` text NOT NULL,
  `chat_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `role`, `content`, `chat_id`, `user_id`, `created_at`) VALUES
(133, 'user', 'c\'est quoi un triangle isocèle ?', 15, 3, '2026-01-18 20:48:38'),
(134, 'assistant', '**EXPLICATION**\nUn triangle isocèle est un triangle qui a deux côtés de même longueur. \n- Le point commun aux deux côtés de même longueur est appelé le **sommet principal**.\n- Le côté opposé au sommet principal est appelé la **base**.\n- Un triangle isocèle possède deux angles égaux : ce sont les angles adjacents à la base.\n\n**EXEMPLE**\nSoit un triangle $ABC$ isocèle en $A$. \nSi $AB = 5 \\text{ cm}$, alors $AC = 5 \\text{ cm}$. \nLe point $A$ est le sommet principal et le segment $[BC]$ est la base. Les angles $\\widehat{ABC}$ et $\\widehat{ACB}$ ont la même mesure.\n\n**EXERCICE**\nOn considère un triangle $RST$ isocèle en $S$ tel que $RS = 7 \\text{ cm}$ et $RT = 4 \\text{ cm}$.\n1) Quelle est la longueur du segment $[ST]$ ? Justifie.\n2) Nomme la base de ce triangle.\n3) Si l\'angle $\\widehat{SRT}$ mesure $70^\\circ$, quelle est la mesure de l\'angle $\\widehat{STR}$ ?\n\n**CORRECTION**\n1) Le triangle $RST$ est isocèle en $S$, donc ses côtés issus du sommet principal $S$ sont de même longueur ($SR = ST$). Puisque $RS = 7 \\text{ cm}$, alors **$ST = 7 \\text{ cm}$**.\n2) Le sommet principal est $S$, donc la base est le côté opposé : **le segment $[RT]$**.\n3) Dans un triangle isocèle, les angles à la base sont égaux. La base étant $[RT]$, les angles $\\widehat{SRT}$ et $\\widehat{STR}$ sont égaux. Donc **$\\widehat{STR} = 70^\\circ$**.', 15, NULL, '2026-01-18 20:48:38');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `niveau` varchar(20) NOT NULL,
  `role` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nom`, `prenom`, `email`, `password`, `niveau`, `role`) VALUES
(1, 'camara', 'siaka', 'camara@gmail.com', '$2b$12$Mpprvgl.y3M6ADlfxEupMOsy9F7hGJB1e91PGd0UjgRu04bwckJFa', '4ème', 'student'),
(2, 'Kolo', 'Junior', 'kolo@gmail.com', '$2b$12$rDnqr9vqDMm11clkj4rVR..xo4dGFXkuVZT/DxCjLeV24gM59NX4a', '6ème', 'student'),
(3, 'aka', 'Josue', 'aka@gmail.com', '$2b$12$MzVC3NMn3hSPjPSYuIvbaeCy/5KbqyZkKTKWrODtMAUlQR.gMGeCG', '5ème', 'student');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chats`
--
ALTER TABLE `chats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `ix_chats_id` (`id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chat_id` (`chat_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `ix_messages_id` (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD KEY `ix_users_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chats`
--
ALTER TABLE `chats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=135;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chats`
--
ALTER TABLE `chats`
  ADD CONSTRAINT `chats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`chat_id`) REFERENCES `chats` (`id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
