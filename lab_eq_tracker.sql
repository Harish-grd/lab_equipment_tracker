-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Sep 27, 2025 at 08:56 AM
-- Server version: 5.6.21
-- PHP Version: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `lab_eq_tracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `bio_dissection_tools`
--

CREATE TABLE IF NOT EXISTS `bio_dissection_tools` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `bio_microscopes`
--

CREATE TABLE IF NOT EXISTS `bio_microscopes` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `bio_specimens_slides`
--

CREATE TABLE IF NOT EXISTS `bio_specimens_slides` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `chem_apparatus`
--

CREATE TABLE IF NOT EXISTS `chem_apparatus` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `chem_apparatus`
--

INSERT INTO `chem_apparatus` (`id`, `name`, `status`, `quantity`) VALUES
(1, 'Test tubes', 'Free', 120);

-- --------------------------------------------------------

--
-- Table structure for table `chem_chemicals`
--

CREATE TABLE IF NOT EXISTS `chem_chemicals` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `phys_acoustic_instruments`
--

CREATE TABLE IF NOT EXISTS `phys_acoustic_instruments` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `phys_electrical_instruments`
--

CREATE TABLE IF NOT EXISTS `phys_electrical_instruments` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `phys_measuring_instruments`
--

CREATE TABLE IF NOT EXISTS `phys_measuring_instruments` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=latin1;

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

CREATE TABLE IF NOT EXISTS `phys_optical_instruments` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `phys_thermal_instruments`
--

CREATE TABLE IF NOT EXISTS `phys_thermal_instruments` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('In Use','Free','Damaged') NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE IF NOT EXISTS `reservations` (
`reservation_id` int(11) NOT NULL,
  `equipment_id` int(11) NOT NULL,
  `lab` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `reservation_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `chem_chemicals`
--
ALTER TABLE `chem_chemicals`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
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
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=102;
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
MODIFY `reservation_id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
