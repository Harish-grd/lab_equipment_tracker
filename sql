-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 02, 2025 at 06:33 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lab_eq_tracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `bio_dissection_tools`
--

CREATE TABLE `bio_dissection_tools` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bio_microscopes`
--

CREATE TABLE `bio_microscopes` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bio_specimens_slides`
--

CREATE TABLE `bio_specimens_slides` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `chem_apparatus`
--

CREATE TABLE `chem_apparatus` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `chem_apparatus`
--

INSERT INTO `chem_apparatus` (`id`, `name`, `status`, `quantity`) VALUES
(1, 'Test tubes', 'Free', 120);

-- --------------------------------------------------------

--
-- Table structure for table `chem_chemicals`
--

CREATE TABLE `chem_chemicals` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `chem_chemicals`
--

INSERT INTO `chem_chemicals` (`id`, `name`, `status`, `quantity`) VALUES
(1, 'Test Tubes', 'Free', 20);

-- --------------------------------------------------------

--
-- Table structure for table `phys_acoustic_instruments`
--

CREATE TABLE `phys_acoustic_instruments` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `phys_electrical_instruments`
--

CREATE TABLE `phys_electrical_instruments` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `phys_measuring_instruments`
--

CREATE TABLE `phys_measuring_instruments` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `phys_measuring_instruments`
--

INSERT INTO `phys_measuring_instruments` (`id`, `name`, `status`, `quantity`) VALUES
(100, 'Vernier Caliper', 'Free', 0),
(101, 'Screw Gauge', 'Free', 0);

-- --------------------------------------------------------

--
-- Table structure for table `phys_optical_instruments`
--

CREATE TABLE `phys_optical_instruments` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `phys_thermal_instruments`
--

CREATE TABLE `phys_thermal_instruments` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `reservation_id` int(11) NOT NULL,
  `equipment_id` int(11) NOT NULL,
  `lab` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_id` varchar(10) NOT NULL,
  `reservation_date` date NOT NULL,
  `quantity_reserved` int(11) NOT NULL CHECK (`quantity_reserved` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`reservation_id`, `equipment_id`, `lab`, `category`, `user_name`, `user_id`, `reservation_date`, `quantity_reserved`) VALUES
(1, 1, 'Chemistry', 'Chemicals', 'Harish', 'Student', '2025-10-03', 10);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bio_dissection_tools`
--
ALTER TABLE `bio_dissection_tools`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bio_microscopes`
--
ALTER TABLE `bio_microscopes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bio_specimens_slides`
--
ALTER TABLE `bio_specimens_slides`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `chem_apparatus`
--
ALTER TABLE `chem_apparatus`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `chem_chemicals`
--
ALTER TABLE `chem_chemicals`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `phys_acoustic_instruments`
--
ALTER TABLE `phys_acoustic_instruments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `phys_electrical_instruments`
--
ALTER TABLE `phys_electrical_instruments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `phys_measuring_instruments`
--
ALTER TABLE `phys_measuring_instruments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `phys_optical_instruments`
--
ALTER TABLE `phys_optical_instruments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `phys_thermal_instruments`
--
ALTER TABLE `phys_thermal_instruments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`reservation_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bio_dissection_tools`
--
ALTER TABLE `bio_dissection_tools`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bio_microscopes`
--
ALTER TABLE `bio_microscopes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bio_specimens_slides`
--
ALTER TABLE `bio_specimens_slides`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `chem_apparatus`
--
ALTER TABLE `chem_apparatus`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `chem_chemicals`
--
ALTER TABLE `chem_chemicals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `phys_acoustic_instruments`
--
ALTER TABLE `phys_acoustic_instruments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `phys_electrical_instruments`
--
ALTER TABLE `phys_electrical_instruments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `phys_measuring_instruments`
--
ALTER TABLE `phys_measuring_instruments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- AUTO_INCREMENT for table `phys_optical_instruments`
--
ALTER TABLE `phys_optical_instruments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `phys_thermal_instruments`
--
ALTER TABLE `phys_thermal_instruments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `reservation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
