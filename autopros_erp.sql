-- phpMyAdmin SQL Dump
-- version 5.2.2deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 15, 2025 at 02:20 PM
-- Server version: 11.4.5-MariaDB-1
-- PHP Version: 8.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `autopros_erp`
--

-- --------------------------------------------------------

--
-- Table structure for table `auditlog_logentry`
--

CREATE TABLE `auditlog_logentry` (
  `id` int(11) NOT NULL,
  `object_pk` varchar(255) NOT NULL,
  `object_id` bigint(20) DEFAULT NULL,
  `object_repr` longtext NOT NULL,
  `action` smallint(5) UNSIGNED NOT NULL CHECK (`action` >= 0),
  `changes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`changes`)),
  `timestamp` datetime(6) NOT NULL,
  `actor_id` bigint(20) DEFAULT NULL,
  `content_type_id` int(11) NOT NULL,
  `remote_addr` char(39) DEFAULT NULL,
  `additional_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`additional_data`)),
  `serialized_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`serialized_data`)),
  `cid` varchar(255) DEFAULT NULL,
  `changes_text` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add employee', 1, 'add_employee'),
(2, 'Can change employee', 1, 'change_employee'),
(3, 'Can delete employee', 1, 'delete_employee'),
(4, 'Can view employee', 1, 'view_employee'),
(5, 'Can delete employee records', 1, 'can_delete_employee'),
(6, 'Can add customer', 2, 'add_customer'),
(7, 'Can change customer', 2, 'change_customer'),
(8, 'Can delete customer', 2, 'delete_customer'),
(9, 'Can view customer', 2, 'view_customer'),
(10, 'Can add delivery', 3, 'add_delivery'),
(11, 'Can change delivery', 3, 'change_delivery'),
(12, 'Can delete delivery', 3, 'delete_delivery'),
(13, 'Can view delivery', 3, 'view_delivery'),
(14, 'Can add Department', 4, 'add_department'),
(15, 'Can change Department', 4, 'change_department'),
(16, 'Can delete Department', 4, 'delete_department'),
(17, 'Can view Department', 4, 'view_department'),
(18, 'Can add Estimate', 5, 'add_estimate'),
(19, 'Can change Estimate', 5, 'change_estimate'),
(20, 'Can delete Estimate', 5, 'delete_estimate'),
(21, 'Can view Estimate', 5, 'view_estimate'),
(22, 'Can add Region', 6, 'add_regionofoperation'),
(23, 'Can change Region', 6, 'change_regionofoperation'),
(24, 'Can delete Region', 6, 'delete_regionofoperation'),
(25, 'Can view Region', 6, 'view_regionofoperation'),
(26, 'Can add Spare Part', 7, 'add_sparepart'),
(27, 'Can change Spare Part', 7, 'change_sparepart'),
(28, 'Can delete Spare Part', 7, 'delete_sparepart'),
(29, 'Can view Spare Part', 7, 'view_sparepart'),
(30, 'Can add Role', 8, 'add_userrole'),
(31, 'Can change Role', 8, 'change_userrole'),
(32, 'Can delete Role', 8, 'delete_userrole'),
(33, 'Can view Role', 8, 'view_userrole'),
(34, 'Can add Verification', 9, 'add_verification'),
(35, 'Can change Verification', 9, 'change_verification'),
(36, 'Can delete Verification', 9, 'delete_verification'),
(37, 'Can view Verification', 9, 'view_verification'),
(38, 'Can add Stores Reconciliation', 10, 'add_storesreconciliation'),
(39, 'Can change Stores Reconciliation', 10, 'change_storesreconciliation'),
(40, 'Can delete Stores Reconciliation', 10, 'delete_storesreconciliation'),
(41, 'Can view Stores Reconciliation', 10, 'view_storesreconciliation'),
(42, 'Can add Notification', 11, 'add_notification'),
(43, 'Can change Notification', 11, 'change_notification'),
(44, 'Can delete Notification', 11, 'delete_notification'),
(45, 'Can view Notification', 11, 'view_notification'),
(46, 'Can add dispatch', 12, 'add_dispatch'),
(47, 'Can change dispatch', 12, 'change_dispatch'),
(48, 'Can delete dispatch', 12, 'delete_dispatch'),
(49, 'Can view dispatch', 12, 'view_dispatch'),
(50, 'Can add delivery item', 13, 'add_deliveryitem'),
(51, 'Can change delivery item', 13, 'change_deliveryitem'),
(52, 'Can delete delivery item', 13, 'delete_deliveryitem'),
(53, 'Can view delivery item', 13, 'view_deliveryitem'),
(54, 'Can add Estimate Item', 14, 'add_estimateitem'),
(55, 'Can change Estimate Item', 14, 'change_estimateitem'),
(56, 'Can delete Estimate Item', 14, 'delete_estimateitem'),
(57, 'Can view Estimate Item', 14, 'view_estimateitem'),
(58, 'Can add log entry', 15, 'add_logentry'),
(59, 'Can change log entry', 15, 'change_logentry'),
(60, 'Can delete log entry', 15, 'delete_logentry'),
(61, 'Can view log entry', 15, 'view_logentry'),
(62, 'Can add permission', 16, 'add_permission'),
(63, 'Can change permission', 16, 'change_permission'),
(64, 'Can delete permission', 16, 'delete_permission'),
(65, 'Can view permission', 16, 'view_permission'),
(66, 'Can add group', 17, 'add_group'),
(67, 'Can change group', 17, 'change_group'),
(68, 'Can delete group', 17, 'delete_group'),
(69, 'Can view group', 17, 'view_group'),
(70, 'Can add content type', 18, 'add_contenttype'),
(71, 'Can change content type', 18, 'change_contenttype'),
(72, 'Can delete content type', 18, 'delete_contenttype'),
(73, 'Can view content type', 18, 'view_contenttype'),
(74, 'Can add session', 19, 'add_session'),
(75, 'Can change session', 19, 'change_session'),
(76, 'Can delete session', 19, 'delete_session'),
(77, 'Can view session', 19, 'view_session'),
(78, 'Can add log entry', 20, 'add_logentry'),
(79, 'Can change log entry', 20, 'change_logentry'),
(80, 'Can delete log entry', 20, 'delete_logentry'),
(81, 'Can view log entry', 20, 'view_logentry');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-05-13 13:35:51.019422', '1', 'CRM', 1, '[{\"added\": {}}]', 4, 1),
(2, '2025-05-13 13:35:58.702194', '2', 'Sales', 1, '[{\"added\": {}}]', 4, 1),
(3, '2025-05-13 13:36:13.963225', '3', 'Outstanding', 1, '[{\"added\": {}}]', 4, 1),
(4, '2025-05-13 13:36:37.192452', '4', 'Stores', 1, '[{\"added\": {}}]', 4, 1),
(5, '2025-05-13 13:37:14.798201', '1', 'Estimates Officer', 1, '[{\"added\": {}}]', 8, 1),
(6, '2025-05-13 13:37:25.015989', '2', 'CRM Officer', 1, '[{\"added\": {}}]', 8, 1),
(7, '2025-05-13 13:37:55.734955', '3', 'Sales Officer', 1, '[{\"added\": {}}]', 8, 1),
(8, '2025-05-13 13:38:10.087005', '4', 'Credit Officer', 1, '[{\"added\": {}}]', 8, 1),
(9, '2025-05-13 13:38:24.062905', '5', 'Billing Officer', 1, '[{\"added\": {}}]', 8, 1),
(10, '2025-05-13 13:38:37.590921', '6', 'Delivery Officer', 1, '[{\"added\": {}}]', 8, 1),
(11, '2025-05-13 13:38:52.784282', '7', 'Dispatch Officer', 1, '[{\"added\": {}}]', 8, 1),
(12, '2025-05-13 13:39:39.021334', '1', 'Office', 1, '[{\"added\": {}}]', 6, 1),
(13, '2025-05-13 13:39:49.653108', '2', 'Eastern', 1, '[{\"added\": {}}]', 6, 1),
(14, '2025-05-13 13:39:57.000353', '3', 'Western', 1, '[{\"added\": {}}]', 6, 1),
(15, '2025-05-13 13:41:06.819802', '2', 'estimates', 1, '[{\"added\": {}}]', 1, 1),
(16, '2025-05-13 13:42:02.865709', '2', 'estimates', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Role\", \"Region of Operation\"]}}]', 1, 1),
(17, '2025-05-13 13:43:05.454116', '3', 'outstanding', 1, '[{\"added\": {}}]', 1, 1),
(18, '2025-05-13 13:43:57.325819', '3', 'outstanding', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Role\", \"Region of Operation\"]}}]', 1, 1),
(19, '2025-05-13 13:45:09.715509', '4', 'billing', 1, '[{\"added\": {}}]', 1, 1),
(20, '2025-05-13 13:45:30.428406', '4', 'billing', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Role\", \"Region of Operation\"]}}]', 1, 1),
(21, '2025-05-13 13:46:21.165608', '5', 'delivery', 1, '[{\"added\": {}}]', 1, 1),
(22, '2025-05-13 13:46:43.166397', '5', 'delivery', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Role\", \"Region of Operation\"]}}]', 1, 1),
(23, '2025-05-13 13:47:45.448007', '6', 'dispatch', 1, '[{\"added\": {}}]', 1, 1),
(24, '2025-05-13 13:48:28.162004', '6', 'dispatch', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Role\", \"Region of Operation\"]}}]', 1, 1),
(25, '2025-05-13 13:50:36.703651', '7', 'crm', 1, '[{\"added\": {}}]', 1, 1),
(26, '2025-05-13 13:50:57.675819', '7', 'crm', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Role\", \"Region of Operation\"]}}]', 1, 1),
(27, '2025-05-13 13:52:00.354582', '8', 'sales', 1, '[{\"added\": {}}]', 1, 1),
(28, '2025-05-13 13:52:43.719995', '4', 'Northern', 1, '[{\"added\": {}}]', 6, 1),
(29, '2025-05-13 13:52:45.488075', '8', 'sales', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Role\", \"Region of Operation\"]}}]', 1, 1),
(30, '2025-05-13 14:12:41.430396', '1', 'Delivery DEL---19309093 - None', 2, '[{\"changed\": {\"fields\": [\"Estimate number\", \"Delivery note number\"]}}]', 3, 1),
(31, '2025-05-14 09:12:33.297867', '8', 'davies', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 1, 1),
(32, '2025-05-14 10:33:51.274535', '2', 'Delivery DEL-122 - None', 2, '[{\"changed\": {\"fields\": [\"Estimate number\"]}}]', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(15, 'admin', 'logentry'),
(20, 'auditlog', 'logentry'),
(17, 'auth', 'group'),
(16, 'auth', 'permission'),
(18, 'contenttypes', 'contenttype'),
(2, 'erp', 'customer'),
(3, 'erp', 'delivery'),
(13, 'erp', 'deliveryitem'),
(4, 'erp', 'department'),
(12, 'erp', 'dispatch'),
(1, 'erp', 'employee'),
(5, 'erp', 'estimate'),
(14, 'erp', 'estimateitem'),
(11, 'erp', 'notification'),
(6, 'erp', 'regionofoperation'),
(7, 'erp', 'sparepart'),
(10, 'erp', 'storesreconciliation'),
(8, 'erp', 'userrole'),
(9, 'erp', 'verification'),
(19, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-05-13 13:30:40.568174'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-05-13 13:30:40.606671'),
(3, 'auth', '0001_initial', '2025-05-13 13:30:40.743706'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-05-13 13:30:40.770736'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-05-13 13:30:40.778311'),
(6, 'auth', '0004_alter_user_username_opts', '2025-05-13 13:30:40.787971'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-05-13 13:30:40.797856'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-05-13 13:30:40.800593'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-05-13 13:30:40.809310'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-05-13 13:30:40.818338'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-05-13 13:30:40.832214'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-05-13 13:30:40.848657'),
(13, 'auth', '0011_update_proxy_permissions', '2025-05-13 13:30:40.854583'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-05-13 13:30:40.860844'),
(15, 'erp', '0001_initial', '2025-05-13 13:30:41.774221'),
(16, 'admin', '0001_initial', '2025-05-13 13:30:41.854987'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-05-13 13:30:41.871839'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-13 13:30:41.887003'),
(19, 'auditlog', '0001_initial', '2025-05-13 13:30:41.971792'),
(20, 'auditlog', '0002_auto_support_long_primary_keys', '2025-05-13 13:30:42.058622'),
(21, 'auditlog', '0003_logentry_remote_addr', '2025-05-13 13:30:42.091794'),
(22, 'auditlog', '0004_logentry_detailed_object_repr', '2025-05-13 13:30:42.115945'),
(23, 'auditlog', '0005_logentry_additional_data_verbose_name', '2025-05-13 13:30:42.136162'),
(24, 'auditlog', '0006_object_pk_index', '2025-05-13 13:30:42.195398'),
(25, 'auditlog', '0007_object_pk_type', '2025-05-13 13:30:42.208938'),
(26, 'auditlog', '0008_action_index', '2025-05-13 13:30:42.236226'),
(27, 'auditlog', '0009_alter_logentry_additional_data', '2025-05-13 13:30:42.258187'),
(28, 'auditlog', '0010_alter_logentry_timestamp', '2025-05-13 13:30:42.286401'),
(29, 'auditlog', '0011_logentry_serialized_data', '2025-05-13 13:30:42.313339'),
(30, 'auditlog', '0012_add_logentry_action_access', '2025-05-13 13:30:42.327795'),
(31, 'auditlog', '0013_alter_logentry_timestamp', '2025-05-13 13:30:42.344253'),
(32, 'auditlog', '0014_logentry_cid', '2025-05-13 13:30:42.384987'),
(33, 'auditlog', '0015_alter_logentry_changes', '2025-05-13 13:30:42.508745'),
(34, 'sessions', '0001_initial', '2025-05-13 13:30:42.540844'),
(35, 'erp', '0002_remove_dispatch_authorized_by_and_more', '2025-05-13 15:15:24.589090'),
(36, 'erp', '0003_dispatch_dispatch_date', '2025-05-14 06:19:44.486204'),
(37, 'erp', '0004_alter_estimate_status', '2025-05-14 06:53:01.423765'),
(38, 'erp', '0005_delivery_dispatch_authorized_by_and_more', '2025-05-14 08:06:58.278526'),
(39, 'erp', '0006_delivery_dispatch_date', '2025-05-14 09:25:46.093534'),
(40, 'erp', '0007_remove_delivery_sales_person', '2025-05-14 10:25:34.429110'),
(41, 'erp', '0008_delivery_sales_person', '2025-05-14 10:45:27.754672'),
(42, 'erp', '0009_delivery_date_of_receipt', '2025-05-14 11:21:24.827014'),
(43, 'erp', '0010_dispatch_camera_number', '2025-05-15 13:39:15.822203');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('919mtrcf4rxmkuau6qol0m9od9wncixu', '.eJxVjDsOwjAQBe_iGlm7_oBDSc8ZovWujQPIluKkQtwdIqWA9s3Me6mR1qWMa0_zOIk6q6AOv1skfqS6AblTvTXNrS7zFPWm6J12fW2Snpfd_Tso1Mu3ZhjQugwODScEzEOAow8ZI3NiEe8pongwaGwmQUuYHWdmBhKPJ_X-AONWOGY:1uFYuf:n5AZ1CAJ-88fmjWPGPwwHUr29USHZ-MEhi_OyA6IInk', '2025-05-29 13:46:17.187469');

-- --------------------------------------------------------

--
-- Table structure for table `erp_customer`
--

CREATE TABLE `erp_customer` (
  `id` bigint(20) NOT NULL,
  `name_of_business` varchar(200) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `road_location` varchar(150) DEFAULT NULL,
  `town_division` varchar(100) DEFAULT NULL,
  `nearest_landmark` varchar(150) DEFAULT NULL,
  `tel_1` varchar(15) DEFAULT NULL,
  `tel_2` varchar(15) DEFAULT NULL,
  `owner_name` varchar(100) DEFAULT NULL,
  `owner_tel` varchar(15) DEFAULT NULL,
  `next_of_kin` varchar(100) DEFAULT NULL,
  `next_of_kin_tel` varchar(15) DEFAULT NULL,
  `approved_by` varchar(100) DEFAULT NULL,
  `prepared_by` varchar(100) DEFAULT NULL,
  `prepared_date` date DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `certificate_of_incorporation` varchar(100) DEFAULT NULL,
  `passport_photo` varchar(100) DEFAULT NULL,
  `trading_license` varchar(100) DEFAULT NULL,
  `national_id` varchar(100) DEFAULT NULL,
  `date_filled` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_customer`
--

INSERT INTO `erp_customer` (`id`, `name_of_business`, `district`, `road_location`, `town_division`, `nearest_landmark`, `tel_1`, `tel_2`, `owner_name`, `owner_tel`, `next_of_kin`, `next_of_kin_tel`, `approved_by`, `prepared_by`, `prepared_date`, `remarks`, `location`, `certificate_of_incorporation`, `passport_photo`, `trading_license`, `national_id`, `date_filled`) VALUES
(1, 'Muchuba Auto Spares Ltd', 'Gulu', 'nmri rd', 'gulu town', 'Stabex-RDw', '084840040443333', NULL, 'Opiyo Nicholas', '084980058', 'Ochaiya', '08495005800', NULL, NULL, '2025-05-15', '', 'North', 'documents/certificates/Logo.png', 'photos/passports/Logo.png', 'photos/license/Logo.png', 'photos/national_id/Logo.png', '2025-05-13 13:56:27.283295'),
(2, 'Kawempe Motor Spares', 'Kampala', 'Mbogo Rd', 'Kawempe Central', 'mbogo mosque', '074848847', '0748494987', 'Muhammed', '0849005880', 'Nasif', '08857007599', NULL, NULL, '2025-05-13', 'New customer', 'Kawempe Mbogo, Kawempe, Kampala, Central Region, Uganda', 'documents/certificates/IMG_5102_HbFTWGZ.jpg', 'photos/passports/IMG_5102_KtdmMm5.jpg', 'photos/license/Screenshot_From_2025-04-29_16-45-54_LJ10sl8.png', 'photos/national_id/ant_9.jpg', '2025-05-14 11:39:16.817984');

-- --------------------------------------------------------

--
-- Table structure for table `erp_delivery`
--

CREATE TABLE `erp_delivery` (
  `id` bigint(20) NOT NULL,
  `delivery_note_number` varchar(100) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `receiver_name` varchar(100) DEFAULT NULL,
  `receiver_contact` varchar(20) DEFAULT NULL,
  `date_goods_received` date DEFAULT NULL,
  `delivery_status` varchar(20) DEFAULT NULL,
  `delivery_person_id` bigint(20) DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `extracted_text` longtext DEFAULT NULL,
  `created_at` varchar(100) DEFAULT NULL,
  `updated_at` varchar(100) DEFAULT NULL,
  `estimate_number_id` bigint(20) DEFAULT NULL,
  `dispatch_authorized_by_id` bigint(20) DEFAULT NULL,
  `packaging_verified_by_id` bigint(20) DEFAULT NULL,
  `dispatch_date` date DEFAULT NULL,
  `sales_person_id` bigint(20) DEFAULT NULL,
  `date_of_receipt` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_delivery`
--

INSERT INTO `erp_delivery` (`id`, `delivery_note_number`, `delivery_date`, `receiver_name`, `receiver_contact`, `date_goods_received`, `delivery_status`, `delivery_person_id`, `remarks`, `image`, `extracted_text`, `created_at`, `updated_at`, `estimate_number_id`, `dispatch_authorized_by_id`, `packaging_verified_by_id`, `dispatch_date`, `sales_person_id`, `date_of_receipt`) VALUES
(1, 'DEL---19309093', NULL, 'Martin', '0785243728', NULL, 'pending', NULL, '', 'delivery_notes/IMG_5102_KtdmMm5_hdSThv9.jpg', '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(2, 'DEL-122', NULL, 'urwi9ore', '7y8oy8re', NULL, 'received', NULL, '', 'delivery_notes/IMG_5102_KtdmMm5_ipVw0Dc.jpg', '', NULL, NULL, 3, NULL, NULL, '2025-05-13', 8, NULL),
(3, 'DEL-123EF', NULL, 'Sachin', NULL, NULL, 'received', NULL, '', 'delivery_notes/IMG_5102_KtdmMm5_hdSThv9_JJ24o8q.jpg', '', NULL, NULL, 4, NULL, NULL, NULL, 8, '2025-05-15'),
(4, 'TODAY-DEL-NOTE', NULL, 'Nakimuli', 'Lydia', NULL, 'received', NULL, '', 'delivery_notes/IMG_5102_KtdmMm5_hdSThv9_JJ24o8q_zQoNqte.jpg', '', NULL, NULL, 5, NULL, NULL, NULL, 8, '2025-05-16'),
(5, 'DEL8739', NULL, NULL, NULL, NULL, 'pending', 6, '', '', '', NULL, NULL, NULL, 5, 4, '2025-05-15', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `erp_deliveryitem`
--

CREATE TABLE `erp_deliveryitem` (
  `id` bigint(20) NOT NULL,
  `item_code` varchar(100) DEFAULT NULL,
  `item_description` varchar(255) NOT NULL,
  `quantity` double NOT NULL,
  `delivery_note_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `erp_department`
--

CREATE TABLE `erp_department` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_department`
--

INSERT INTO `erp_department` (`id`, `name`, `description`) VALUES
(1, 'CRM', ''),
(2, 'Sales', ''),
(3, 'Outstanding', ''),
(4, 'Stores', '');

-- --------------------------------------------------------

--
-- Table structure for table `erp_dispatch`
--

CREATE TABLE `erp_dispatch` (
  `id` bigint(20) NOT NULL,
  `office_gate_pass` varchar(100) DEFAULT NULL,
  `store_gate_pass` varchar(100) DEFAULT NULL,
  `estimate_number_id` bigint(20) DEFAULT NULL,
  `dispatch_date` date DEFAULT NULL,
  `camera_number` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_dispatch`
--

INSERT INTO `erp_dispatch` (`id`, `office_gate_pass`, `store_gate_pass`, `estimate_number_id`, `dispatch_date`, `camera_number`) VALUES
(1, '5g54g', 'tgg4', 2, '2025-05-08', NULL),
(2, '893988973ee', 'dey037839', 4, '2025-05-14', NULL),
(3, 'TODAY-GATE-PASS-2', 'TODAY-GATE-PASS', 5, '2025-05-14', NULL),
(4, '83ye893e8', '87499uru', 6, '2025-05-13', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `erp_employee`
--

CREATE TABLE `erp_employee` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `department_id` bigint(20) DEFAULT NULL,
  `region_of_operation_id` bigint(20) DEFAULT NULL,
  `role_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_employee`
--

INSERT INTO `erp_employee` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `phone`, `is_verified`, `department_id`, `region_of_operation_id`, `role_id`) VALUES
(1, 'pbkdf2_sha256$390000$Cy3u530hpkn7cnDAKdQDff$xETmmHAwZp4G5U1HKGBY41mvj275Sq09U+CdnMDqTgg=', '2025-05-14 10:21:24.445655', 1, 'admin', '', '', '', 1, 1, '2025-05-13 13:34:03.152720', '', 0, NULL, NULL, NULL),
(2, 'pbkdf2_sha256$390000$vutHk9XebuTTuTnyrBxqJe$cde9HbGDxBd6/rhkKRRkj3Zd9axJMTH+tPPxZOnPuYQ=', '2025-05-15 06:11:17.513567', 0, 'estimates', 'Jolly', '', '', 0, 1, '2025-05-13 13:41:06.695663', '', 0, 1, 1, 1),
(3, 'pbkdf2_sha256$390000$0ge24fRi4iectOn4wz83Yc$GV+RG7TwrSVNw0VIEnCiDQeaY4G1Q86Ekfh5RS7mzjc=', '2025-05-14 13:40:48.701283', 0, 'outstanding', 'Scovia', '', '', 0, 1, '2025-05-13 13:43:05.329088', '', 0, 3, 1, 4),
(4, 'pbkdf2_sha256$390000$v5E1iv0FLz0yiL229jY5ks$RW3vlHOYiPGzCrc0EEOCrqtYiYmQJ6liF99JQssXhL0=', '2025-05-14 13:43:25.304681', 0, 'billing', 'Maria', '', '', 0, 1, '2025-05-13 13:45:09.586899', '', 0, 4, 1, 5),
(5, 'pbkdf2_sha256$390000$XOJfhfYqNXomz3DhY52aGc$3YHAMJ3YidMG+3DnoPtpJRusRJVCly+xj7eXwa0BCkY=', '2025-05-15 13:44:35.274838', 0, 'delivery', 'Ali', '', '', 0, 1, '2025-05-13 13:46:21.040539', '', 0, 4, 1, 6),
(6, 'pbkdf2_sha256$390000$NURtR93txiVLYJOe4ZEVAA$g4x4QSPRyLaIRV1sI+sErK9f0NEHge57xFzORzFrPxI=', '2025-05-14 13:44:31.138119', 0, 'dispatch', 'Yma', '', '', 0, 1, '2025-05-13 13:47:45.327171', '', 0, 4, 1, 7),
(7, 'pbkdf2_sha256$390000$T6dvNp8mWYTnnqKuRExibr$S1VKJPtrHuzgb28jfPd2rXHoRIJAxYJHz01iBH3yU5Q=', '2025-05-14 11:36:40.114920', 0, 'crm', 'Christine', '', '', 0, 1, '2025-05-13 13:50:36.576003', '', 0, 1, 1, 2),
(8, 'pbkdf2_sha256$390000$ithvEVrgEfUeNSx7GZJvji$T42WN68swkSmMxELeOmNTivOfawcTCuGuq94t29vmKc=', '2025-05-15 13:46:17.185717', 0, 'davies', 'Davies', '', '', 0, 1, '2025-05-13 13:52:00.229119', '', 0, 2, 4, 3);

-- --------------------------------------------------------

--
-- Table structure for table `erp_employee_groups`
--

CREATE TABLE `erp_employee_groups` (
  `id` bigint(20) NOT NULL,
  `employee_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `erp_employee_user_permissions`
--

CREATE TABLE `erp_employee_user_permissions` (
  `id` bigint(20) NOT NULL,
  `employee_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `erp_estimate`
--

CREATE TABLE `erp_estimate` (
  `id` bigint(20) NOT NULL,
  `created_date` date DEFAULT NULL,
  `bk_estimate_id` varchar(20) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `invoice_number` varchar(100) DEFAULT NULL,
  `invoice_amount` decimal(10,2) DEFAULT NULL,
  `date_verified` date DEFAULT NULL,
  `date_billed` date DEFAULT NULL,
  `billing_officer_id` bigint(20) DEFAULT NULL,
  `customer_name_id` bigint(20) DEFAULT NULL,
  `sales_person_id` bigint(20) DEFAULT NULL,
  `verified_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_estimate`
--

INSERT INTO `erp_estimate` (`id`, `created_date`, `bk_estimate_id`, `amount`, `status`, `created_at`, `updated_at`, `invoice_number`, `invoice_amount`, `date_verified`, `date_billed`, `billing_officer_id`, `customer_name_id`, `sales_person_id`, `verified_by_id`) VALUES
(1, '2025-05-14', 'EST-2025-0001', 200000.00, 'delivered', '2025-05-13 14:04:37.968834', '2025-05-13 14:07:36.956088', 'INV-1039', 2400000.00, '2025-05-13', '2025-05-13', 4, 1, 8, 3),
(2, '2025-05-14', 'EST-2025-0002', 300000.00, 'delivered', '2025-05-13 14:21:21.529016', '2025-05-14 08:19:23.733210', 'INV-208393', 2039489.00, '2025-05-13', '2025-05-13', 4, 1, 8, 3),
(3, '2025-05-15', 'EST-2025-0003', 30000000.00, 'delivered', '2025-05-14 06:08:49.894930', '2025-05-14 06:22:16.388512', 'INVO-123', 2000000.00, '2025-05-14', '2025-05-14', 4, 1, 8, 3),
(4, '2025-05-14', 'EST-2025-0004', 3000000.00, 'delivered', '2025-05-14 11:55:25.362106', '2025-05-14 13:58:05.879474', 'INV-1000', 2000000.00, '2025-05-14', '2025-05-14', 4, 2, 8, 3),
(5, '2025-05-15', 'EST-2025-0005', 1000000.00, 'delivered', '2025-05-14 12:26:47.974709', '2025-05-15 13:45:27.611058', 'TODAY INV', 200000.00, '2025-05-14', '2025-05-14', 4, 2, 8, 3),
(6, '2025-05-14', '5636287', 500000.00, 'dispatched', '2025-05-14 13:40:05.849331', '2025-05-14 13:52:57.072181', 'INV 038984', 400000.00, '2025-05-14', '2025-05-14', 4, 2, 8, 3);

-- --------------------------------------------------------

--
-- Table structure for table `erp_estimateitem`
--

CREATE TABLE `erp_estimateitem` (
  `id` bigint(20) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `negotiated_price` decimal(10,2) NOT NULL,
  `estimate_id` bigint(20) NOT NULL,
  `part_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `erp_notification`
--

CREATE TABLE `erp_notification` (
  `id` bigint(20) NOT NULL,
  `message` varchar(200) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `estimate_id` bigint(20) NOT NULL,
  `recipient_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `erp_regionofoperation`
--

CREATE TABLE `erp_regionofoperation` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_regionofoperation`
--

INSERT INTO `erp_regionofoperation` (`id`, `name`, `description`) VALUES
(1, 'Office', ''),
(2, 'Eastern', ''),
(3, 'Western', ''),
(4, 'Northern', '');

-- --------------------------------------------------------

--
-- Table structure for table `erp_sparepart`
--

CREATE TABLE `erp_sparepart` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `current_stock` int(10) UNSIGNED NOT NULL CHECK (`current_stock` >= 0),
  `unit_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `erp_storesreconciliation`
--

CREATE TABLE `erp_storesreconciliation` (
  `id` bigint(20) NOT NULL,
  `discrepancies` longtext NOT NULL,
  `reconciliation_date` datetime(6) NOT NULL,
  `estimate_id` bigint(20) NOT NULL,
  `reconciled_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `erp_userrole`
--

CREATE TABLE `erp_userrole` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_userrole`
--

INSERT INTO `erp_userrole` (`id`, `name`, `description`) VALUES
(1, 'Estimates Officer', ''),
(2, 'CRM Officer', ''),
(3, 'Sales Officer', ''),
(4, 'Credit Officer', ''),
(5, 'Billing Officer', ''),
(6, 'Delivery Officer', ''),
(7, 'Dispatch Officer', '');

-- --------------------------------------------------------

--
-- Table structure for table `erp_verification`
--

CREATE TABLE `erp_verification` (
  `id` bigint(20) NOT NULL,
  `notes` longtext NOT NULL,
  `verification_date` datetime(6) NOT NULL,
  `estimate_id` bigint(20) NOT NULL,
  `verified_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auditlog_logentry`
--
ALTER TABLE `auditlog_logentry`
  ADD PRIMARY KEY (`id`),
  ADD KEY `auditlog_logentry_actor_id_959271d2_fk_erp_employee_id` (`actor_id`),
  ADD KEY `auditlog_logentry_content_type_id_75830218_fk_django_co` (`content_type_id`),
  ADD KEY `auditlog_logentry_object_id_09c2eee8` (`object_id`),
  ADD KEY `auditlog_logentry_object_pk_6e3219c0` (`object_pk`),
  ADD KEY `auditlog_logentry_action_229afe39` (`action`),
  ADD KEY `auditlog_logentry_timestamp_37867bb0` (`timestamp`),
  ADD KEY `auditlog_logentry_cid_9f467263` (`cid`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_erp_employee_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `erp_customer`
--
ALTER TABLE `erp_customer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `erp_delivery`
--
ALTER TABLE `erp_delivery`
  ADD PRIMARY KEY (`id`),
  ADD KEY `erp_delivery_estimate_number_id_5617a4f0_fk_erp_estimate_id` (`estimate_number_id`),
  ADD KEY `erp_delivery_dispatch_authorized__7e9f0825_fk_erp_emplo` (`dispatch_authorized_by_id`),
  ADD KEY `erp_delivery_packaging_verified_b_10f9db7e_fk_erp_emplo` (`packaging_verified_by_id`),
  ADD KEY `erp_delivery_delivery_person_id_cd0341e7` (`delivery_person_id`),
  ADD KEY `erp_delivery_sales_person_id_a52a2dbc_fk_erp_employee_id` (`sales_person_id`);

--
-- Indexes for table `erp_deliveryitem`
--
ALTER TABLE `erp_deliveryitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `erp_deliveryitem_delivery_note_id_b989354e_fk_erp_delivery_id` (`delivery_note_id`);

--
-- Indexes for table `erp_department`
--
ALTER TABLE `erp_department`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `erp_dispatch`
--
ALTER TABLE `erp_dispatch`
  ADD PRIMARY KEY (`id`),
  ADD KEY `erp_dispatch_estimate_number_id_f26cd7f1_fk_erp_estimate_id` (`estimate_number_id`);

--
-- Indexes for table `erp_employee`
--
ALTER TABLE `erp_employee`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `erp_employee_department_id_9eca106d_fk_erp_department_id` (`department_id`),
  ADD KEY `erp_employee_region_of_operation__8206b6d5_fk_erp_regio` (`region_of_operation_id`),
  ADD KEY `erp_employee_role_id_0f6cc713_fk_erp_userrole_id` (`role_id`);

--
-- Indexes for table `erp_employee_groups`
--
ALTER TABLE `erp_employee_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `erp_employee_groups_employee_id_group_id_1f8d1473_uniq` (`employee_id`,`group_id`),
  ADD KEY `erp_employee_groups_group_id_bdb56b93_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `erp_employee_user_permissions`
--
ALTER TABLE `erp_employee_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `erp_employee_user_permis_employee_id_permission_i_cb8f6a63_uniq` (`employee_id`,`permission_id`),
  ADD KEY `erp_employee_user_pe_permission_id_4a870c3e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `erp_estimate`
--
ALTER TABLE `erp_estimate`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bk_estimate_id` (`bk_estimate_id`),
  ADD KEY `erp_estimate_billing_officer_id_547e31b8_fk_erp_employee_id` (`billing_officer_id`),
  ADD KEY `erp_estimate_customer_name_id_3207241c_fk_erp_customer_id` (`customer_name_id`),
  ADD KEY `erp_estimate_sales_person_id_8cdb94e9_fk_erp_employee_id` (`sales_person_id`),
  ADD KEY `erp_estimate_verified_by_id_6a5521a9_fk_erp_employee_id` (`verified_by_id`);

--
-- Indexes for table `erp_estimateitem`
--
ALTER TABLE `erp_estimateitem`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `erp_estimateitem_estimate_id_part_id_35af46f6_uniq` (`estimate_id`,`part_id`),
  ADD KEY `erp_estimateitem_part_id_c5a9681c_fk_erp_sparepart_id` (`part_id`);

--
-- Indexes for table `erp_notification`
--
ALTER TABLE `erp_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `erp_notification_estimate_id_8b71007c_fk_erp_estimate_id` (`estimate_id`),
  ADD KEY `erp_notification_recipient_id_6222b83a_fk_erp_employee_id` (`recipient_id`);

--
-- Indexes for table `erp_regionofoperation`
--
ALTER TABLE `erp_regionofoperation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `erp_sparepart`
--
ALTER TABLE `erp_sparepart`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sku` (`sku`);

--
-- Indexes for table `erp_storesreconciliation`
--
ALTER TABLE `erp_storesreconciliation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `estimate_id` (`estimate_id`),
  ADD KEY `erp_storesreconcilia_reconciled_by_id_384f4ca6_fk_erp_emplo` (`reconciled_by_id`);

--
-- Indexes for table `erp_userrole`
--
ALTER TABLE `erp_userrole`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `erp_verification`
--
ALTER TABLE `erp_verification`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `estimate_id` (`estimate_id`),
  ADD KEY `erp_verification_verified_by_id_b5516b77_fk_erp_employee_id` (`verified_by_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auditlog_logentry`
--
ALTER TABLE `auditlog_logentry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `erp_customer`
--
ALTER TABLE `erp_customer`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `erp_delivery`
--
ALTER TABLE `erp_delivery`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `erp_deliveryitem`
--
ALTER TABLE `erp_deliveryitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_department`
--
ALTER TABLE `erp_department`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `erp_dispatch`
--
ALTER TABLE `erp_dispatch`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `erp_employee`
--
ALTER TABLE `erp_employee`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `erp_employee_groups`
--
ALTER TABLE `erp_employee_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_employee_user_permissions`
--
ALTER TABLE `erp_employee_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_estimate`
--
ALTER TABLE `erp_estimate`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `erp_estimateitem`
--
ALTER TABLE `erp_estimateitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_notification`
--
ALTER TABLE `erp_notification`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_regionofoperation`
--
ALTER TABLE `erp_regionofoperation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `erp_sparepart`
--
ALTER TABLE `erp_sparepart`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_storesreconciliation`
--
ALTER TABLE `erp_storesreconciliation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_userrole`
--
ALTER TABLE `erp_userrole`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `erp_verification`
--
ALTER TABLE `erp_verification`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auditlog_logentry`
--
ALTER TABLE `auditlog_logentry`
  ADD CONSTRAINT `auditlog_logentry_actor_id_959271d2_fk_erp_employee_id` FOREIGN KEY (`actor_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `auditlog_logentry_content_type_id_75830218_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_erp_employee_id` FOREIGN KEY (`user_id`) REFERENCES `erp_employee` (`id`);

--
-- Constraints for table `erp_delivery`
--
ALTER TABLE `erp_delivery`
  ADD CONSTRAINT `erp_delivery_delivery_person_id_cd0341e7_fk_erp_employee_id` FOREIGN KEY (`delivery_person_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_delivery_dispatch_authorized__7e9f0825_fk_erp_emplo` FOREIGN KEY (`dispatch_authorized_by_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_delivery_estimate_number_id_5617a4f0_fk_erp_estimate_id` FOREIGN KEY (`estimate_number_id`) REFERENCES `erp_estimate` (`id`),
  ADD CONSTRAINT `erp_delivery_packaging_verified_b_10f9db7e_fk_erp_emplo` FOREIGN KEY (`packaging_verified_by_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_delivery_sales_person_id_a52a2dbc_fk_erp_employee_id` FOREIGN KEY (`sales_person_id`) REFERENCES `erp_employee` (`id`);

--
-- Constraints for table `erp_deliveryitem`
--
ALTER TABLE `erp_deliveryitem`
  ADD CONSTRAINT `erp_deliveryitem_delivery_note_id_b989354e_fk_erp_delivery_id` FOREIGN KEY (`delivery_note_id`) REFERENCES `erp_delivery` (`id`);

--
-- Constraints for table `erp_dispatch`
--
ALTER TABLE `erp_dispatch`
  ADD CONSTRAINT `erp_dispatch_estimate_number_id_f26cd7f1_fk_erp_estimate_id` FOREIGN KEY (`estimate_number_id`) REFERENCES `erp_estimate` (`id`);

--
-- Constraints for table `erp_employee`
--
ALTER TABLE `erp_employee`
  ADD CONSTRAINT `erp_employee_department_id_9eca106d_fk_erp_department_id` FOREIGN KEY (`department_id`) REFERENCES `erp_department` (`id`),
  ADD CONSTRAINT `erp_employee_region_of_operation__8206b6d5_fk_erp_regio` FOREIGN KEY (`region_of_operation_id`) REFERENCES `erp_regionofoperation` (`id`),
  ADD CONSTRAINT `erp_employee_role_id_0f6cc713_fk_erp_userrole_id` FOREIGN KEY (`role_id`) REFERENCES `erp_userrole` (`id`);

--
-- Constraints for table `erp_employee_groups`
--
ALTER TABLE `erp_employee_groups`
  ADD CONSTRAINT `erp_employee_groups_employee_id_92e4f461_fk_erp_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_employee_groups_group_id_bdb56b93_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `erp_employee_user_permissions`
--
ALTER TABLE `erp_employee_user_permissions`
  ADD CONSTRAINT `erp_employee_user_pe_employee_id_03f4f760_fk_erp_emplo` FOREIGN KEY (`employee_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_employee_user_pe_permission_id_4a870c3e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `erp_estimate`
--
ALTER TABLE `erp_estimate`
  ADD CONSTRAINT `erp_estimate_billing_officer_id_547e31b8_fk_erp_employee_id` FOREIGN KEY (`billing_officer_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_estimate_customer_name_id_3207241c_fk_erp_customer_id` FOREIGN KEY (`customer_name_id`) REFERENCES `erp_customer` (`id`),
  ADD CONSTRAINT `erp_estimate_sales_person_id_8cdb94e9_fk_erp_employee_id` FOREIGN KEY (`sales_person_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_estimate_verified_by_id_6a5521a9_fk_erp_employee_id` FOREIGN KEY (`verified_by_id`) REFERENCES `erp_employee` (`id`);

--
-- Constraints for table `erp_estimateitem`
--
ALTER TABLE `erp_estimateitem`
  ADD CONSTRAINT `erp_estimateitem_estimate_id_480b5e83_fk_erp_estimate_id` FOREIGN KEY (`estimate_id`) REFERENCES `erp_estimate` (`id`),
  ADD CONSTRAINT `erp_estimateitem_part_id_c5a9681c_fk_erp_sparepart_id` FOREIGN KEY (`part_id`) REFERENCES `erp_sparepart` (`id`);

--
-- Constraints for table `erp_notification`
--
ALTER TABLE `erp_notification`
  ADD CONSTRAINT `erp_notification_estimate_id_8b71007c_fk_erp_estimate_id` FOREIGN KEY (`estimate_id`) REFERENCES `erp_estimate` (`id`),
  ADD CONSTRAINT `erp_notification_recipient_id_6222b83a_fk_erp_employee_id` FOREIGN KEY (`recipient_id`) REFERENCES `erp_employee` (`id`);

--
-- Constraints for table `erp_storesreconciliation`
--
ALTER TABLE `erp_storesreconciliation`
  ADD CONSTRAINT `erp_storesreconcilia_reconciled_by_id_384f4ca6_fk_erp_emplo` FOREIGN KEY (`reconciled_by_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_storesreconciliation_estimate_id_9dbd4f39_fk_erp_estimate_id` FOREIGN KEY (`estimate_id`) REFERENCES `erp_estimate` (`id`);

--
-- Constraints for table `erp_verification`
--
ALTER TABLE `erp_verification`
  ADD CONSTRAINT `erp_verification_estimate_id_b8c99898_fk_erp_estimate_id` FOREIGN KEY (`estimate_id`) REFERENCES `erp_estimate` (`id`),
  ADD CONSTRAINT `erp_verification_verified_by_id_b5516b77_fk_erp_employee_id` FOREIGN KEY (`verified_by_id`) REFERENCES `erp_employee` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
