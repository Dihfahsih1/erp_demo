-- phpMyAdmin SQL Dump
-- version 5.2.2deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 10, 2025 at 12:53 PM
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
(1, 'Can add customer', 1, 'add_customer'),
(2, 'Can change customer', 1, 'change_customer'),
(3, 'Can delete customer', 1, 'delete_customer'),
(4, 'Can view customer', 1, 'view_customer'),
(5, 'Can add Department', 2, 'add_department'),
(6, 'Can change Department', 2, 'change_department'),
(7, 'Can delete Department', 2, 'delete_department'),
(8, 'Can view Department', 2, 'view_department'),
(9, 'Can add Employee', 3, 'add_employee'),
(10, 'Can change Employee', 3, 'change_employee'),
(11, 'Can delete Employee', 3, 'delete_employee'),
(12, 'Can view Employee', 3, 'view_employee'),
(13, 'Can add Estimate', 4, 'add_estimate'),
(14, 'Can change Estimate', 4, 'change_estimate'),
(15, 'Can delete Estimate', 4, 'delete_estimate'),
(16, 'Can view Estimate', 4, 'view_estimate'),
(17, 'Can modify estimate status', 4, 'change_estimate_status'),
(18, 'Can view all estimates', 4, 'view_all_estimates'),
(19, 'Can add Spare Part', 5, 'add_sparepart'),
(20, 'Can change Spare Part', 5, 'change_sparepart'),
(21, 'Can delete Spare Part', 5, 'delete_sparepart'),
(22, 'Can view Spare Part', 5, 'view_sparepart'),
(23, 'Can add Verification', 6, 'add_verification'),
(24, 'Can change Verification', 6, 'change_verification'),
(25, 'Can delete Verification', 6, 'delete_verification'),
(26, 'Can view Verification', 6, 'view_verification'),
(27, 'Can add Stores Reconciliation', 7, 'add_storesreconciliation'),
(28, 'Can change Stores Reconciliation', 7, 'change_storesreconciliation'),
(29, 'Can delete Stores Reconciliation', 7, 'delete_storesreconciliation'),
(30, 'Can view Stores Reconciliation', 7, 'view_storesreconciliation'),
(31, 'Can add Notification', 8, 'add_notification'),
(32, 'Can change Notification', 8, 'change_notification'),
(33, 'Can delete Notification', 8, 'delete_notification'),
(34, 'Can view Notification', 8, 'view_notification'),
(35, 'Can add Dispatch', 9, 'add_dispatch'),
(36, 'Can change Dispatch', 9, 'change_dispatch'),
(37, 'Can delete Dispatch', 9, 'delete_dispatch'),
(38, 'Can view Dispatch', 9, 'view_dispatch'),
(39, 'Can add Estimate Item', 10, 'add_estimateitem'),
(40, 'Can change Estimate Item', 10, 'change_estimateitem'),
(41, 'Can delete Estimate Item', 10, 'delete_estimateitem'),
(42, 'Can view Estimate Item', 10, 'view_estimateitem'),
(43, 'Can add delivery note', 11, 'add_deliverynote'),
(44, 'Can change delivery note', 11, 'change_deliverynote'),
(45, 'Can delete delivery note', 11, 'delete_deliverynote'),
(46, 'Can view delivery note', 11, 'view_deliverynote'),
(47, 'Can add Role', 12, 'add_userrole'),
(48, 'Can change Role', 12, 'change_userrole'),
(49, 'Can delete Role', 12, 'delete_userrole'),
(50, 'Can view Role', 12, 'view_userrole'),
(51, 'Can add delivery note item', 13, 'add_deliverynoteitem'),
(52, 'Can change delivery note item', 13, 'change_deliverynoteitem'),
(53, 'Can delete delivery note item', 13, 'delete_deliverynoteitem'),
(54, 'Can view delivery note item', 13, 'view_deliverynoteitem'),
(55, 'Can add log entry', 14, 'add_logentry'),
(56, 'Can change log entry', 14, 'change_logentry'),
(57, 'Can delete log entry', 14, 'delete_logentry'),
(58, 'Can view log entry', 14, 'view_logentry'),
(59, 'Can add permission', 15, 'add_permission'),
(60, 'Can change permission', 15, 'change_permission'),
(61, 'Can delete permission', 15, 'delete_permission'),
(62, 'Can view permission', 15, 'view_permission'),
(63, 'Can add group', 16, 'add_group'),
(64, 'Can change group', 16, 'change_group'),
(65, 'Can delete group', 16, 'delete_group'),
(66, 'Can view group', 16, 'view_group'),
(67, 'Can add content type', 17, 'add_contenttype'),
(68, 'Can change content type', 17, 'change_contenttype'),
(69, 'Can delete content type', 17, 'delete_contenttype'),
(70, 'Can view content type', 17, 'view_contenttype'),
(71, 'Can add session', 18, 'add_session'),
(72, 'Can change session', 18, 'change_session'),
(73, 'Can delete session', 18, 'delete_session'),
(74, 'Can view session', 18, 'view_session'),
(75, 'Can add log entry', 19, 'add_logentry'),
(76, 'Can change log entry', 19, 'change_logentry'),
(77, 'Can delete log entry', 19, 'delete_logentry'),
(78, 'Can view log entry', 19, 'view_logentry'),
(79, 'Can add testing model', 20, 'add_testingmodel'),
(80, 'Can change testing model', 20, 'change_testingmodel'),
(81, 'Can delete testing model', 20, 'delete_testingmodel'),
(82, 'Can view testing model', 20, 'view_testingmodel'),
(83, 'Can add Region', 21, 'add_regionofoperation'),
(84, 'Can change Region', 21, 'change_regionofoperation'),
(85, 'Can delete Region', 21, 'delete_regionofoperation'),
(86, 'Can view Region', 21, 'view_regionofoperation'),
(87, 'Can delete employee records', 3, 'can_delete_employee');

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
(1, '2025-04-30 06:53:05.155872', '1', 'Sales', 1, '[{\"added\": {}}]', 2, 1),
(2, '2025-04-30 06:53:30.697790', '2', 'CRM', 1, '[{\"added\": {}}]', 2, 1),
(3, '2025-04-30 06:54:07.318827', '3', 'Credit Control', 1, '[{\"added\": {}}]', 2, 1),
(4, '2025-04-30 06:54:37.443028', '4', 'Billing', 1, '[{\"added\": {}}]', 2, 1),
(5, '2025-04-30 06:55:18.177700', '5', 'Stores', 1, '[{\"added\": {}}]', 2, 1),
(6, '2025-04-30 06:55:54.883585', '6', 'Dispatch', 1, '[{\"added\": {}}]', 2, 1),
(7, '2025-04-30 06:57:21.769639', '2', 'sales', 1, '[{\"added\": {}}]', 3, 1),
(8, '2025-04-30 07:02:20.698265', '1', 'Sales Executive', 1, '[{\"added\": {}}]', 12, 1),
(9, '2025-04-30 07:03:26.783819', '2', 'Estimates in charge', 1, '[{\"added\": {}}]', 12, 1),
(10, '2025-04-30 07:03:54.122810', '3', 'Head of Sales', 1, '[{\"added\": {}}]', 12, 1),
(11, '2025-04-30 07:04:13.741303', '2', 'sales', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 3, 1),
(12, '2025-04-30 07:22:57.507089', '4', 'Admin', 1, '[{\"added\": {}}]', 12, 1),
(13, '2025-04-30 07:22:59.956350', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Role\"]}}]', 3, 1),
(14, '2025-05-03 09:48:07.442636', '2', 'Delivery iuwehoj - wqqee', 2, '[{\"changed\": {\"fields\": [\"Delivery no\", \"Customer name\", \"Receiver contact\", \"Invoice no\", \"Transaction value\", \"Estimate number\", \"Customer name address\", \"Delivery person\", \"Remarks\"]}}]', 11, 1),
(15, '2025-05-03 10:00:49.300359', '3', 'rhoda', 1, '[{\"added\": {}}]', 3, 1),
(16, '2025-05-03 10:01:09.522639', '2', 'moses', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 3, 1),
(17, '2025-05-03 10:20:43.689930', '1', 'Delivery None - Admin-1', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(18, '2025-05-03 10:20:56.524343', '4', 'Delivery None - None', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(19, '2025-05-03 10:21:22.215198', '3', 'Delivery None - None', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(20, '2025-05-03 10:21:33.925301', '3', 'Delivery None - None', 2, '[]', 11, 1),
(21, '2025-05-03 10:21:44.493890', '1', 'Delivery None - Admin-1', 2, '[]', 11, 1),
(22, '2025-05-03 10:22:02.025489', '2', 'Delivery iuwehoj - wqqee', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(23, '2025-05-05 10:31:34.263279', '4', 'delivery', 1, '[{\"added\": {}}]', 3, 1),
(24, '2025-05-05 10:32:34.862425', '5', 'Delivery Officer', 1, '[{\"added\": {}}]', 12, 1),
(25, '2025-05-05 10:32:58.432711', '4', 'delivery', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Phone Number\", \"Role\"]}}]', 3, 1),
(26, '2025-05-05 11:29:33.647888', '5', 'davies', 1, '[{\"added\": {}}]', 3, 1),
(27, '2025-05-05 11:30:17.899621', '5', 'davies', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Phone Number\", \"Role\"]}}]', 3, 1),
(28, '2025-05-05 11:32:17.829433', '6', 'Delivery None - None', 2, '[{\"changed\": {\"fields\": [\"Date of billing\", \"Sales person\"]}}]', 11, 1),
(29, '2025-05-06 12:49:55.035185', '7', 'Delivery None - None', 2, '[{\"changed\": {\"fields\": [\"Date of billing\", \"Sales person\"]}}]', 11, 1),
(30, '2025-05-06 12:50:49.980703', '6', 'Delivery DEL-123DF - Mariam', 2, '[{\"changed\": {\"fields\": [\"Delivery no\", \"Sales person\"]}}]', 11, 1),
(31, '2025-05-06 12:51:10.403158', '6', 'Delivery DEL-123DF - Mariam', 2, '[]', 11, 1),
(32, '2025-05-06 12:51:21.032863', '1', 'Delivery None - wqrw', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(33, '2025-05-06 12:51:42.932733', '2', 'Delivery iuwehoj - wqqee', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(34, '2025-05-06 12:51:51.692739', '3', 'Delivery None - eeee', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(35, '2025-05-06 12:52:01.336449', '5', 'Delivery None - None', 2, '[{\"changed\": {\"fields\": [\"Date of billing\", \"Sales person\"]}}]', 11, 1),
(36, '2025-05-06 12:52:08.625374', '6', 'Delivery DEL-123DF - Mariam', 2, '[]', 11, 1),
(37, '2025-05-06 13:39:33.955531', '6', 'yamal', 1, '[{\"added\": {}}]', 3, 1),
(38, '2025-05-06 13:39:58.211235', '6', 'yamal', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Role\"]}}]', 3, 1),
(39, '2025-05-06 13:40:17.807824', '6', 'yamal', 2, '[]', 3, 1),
(40, '2025-05-08 08:21:39.734514', '1', 'Sales Officer', 2, '[{\"changed\": {\"fields\": [\"Role Name\"]}}]', 12, 1),
(41, '2025-05-08 09:15:15.660960', '1', 'Central', 1, '[{\"added\": {}}]', 21, 1),
(42, '2025-05-08 09:15:44.832816', '2', 'Office', 1, '[{\"added\": {}}]', 21, 1),
(43, '2025-05-08 09:16:46.863205', '3', 'Eastern', 1, '[{\"added\": {}}]', 21, 1),
(44, '2025-05-08 09:17:15.897443', '4', 'Western', 1, '[{\"added\": {}}]', 21, 1),
(45, '2025-05-08 09:17:43.572932', '5', 'North', 1, '[{\"added\": {}}]', 21, 1),
(46, '2025-05-08 09:17:53.997316', '5', 'davies', 2, '[{\"changed\": {\"fields\": [\"Region of Operation\"]}}]', 3, 1),
(47, '2025-05-08 09:19:24.450843', '2', 'moses', 2, '[{\"changed\": {\"fields\": [\"Region of Operation\"]}}]', 3, 1),
(48, '2025-05-08 09:19:37.766021', '3', 'rhoda', 2, '[{\"changed\": {\"fields\": [\"Region of Operation\"]}}]', 3, 1),
(49, '2025-05-08 11:53:59.196438', '2', 'Estimates Officer', 2, '[{\"changed\": {\"fields\": [\"Role Name\"]}}]', 12, 1),
(50, '2025-05-08 11:55:22.864519', '6', 'Dispatch Officer', 1, '[{\"added\": {}}]', 12, 1),
(51, '2025-05-08 11:56:21.926047', '7', 'Outstanding Officer', 1, '[{\"added\": {}}]', 12, 1),
(52, '2025-05-08 11:56:36.619397', '8', 'Billing Officer', 1, '[{\"added\": {}}]', 12, 1),
(53, '2025-05-08 11:57:24.738298', '9', 'CRM Officer', 1, '[{\"added\": {}}]', 12, 1),
(54, '2025-05-09 11:17:03.840606', '5', 'Delivery DEL-1930484 - Frank', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(55, '2025-05-09 11:17:19.086468', '2', 'Delivery wwwr - wqqee', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(56, '2025-05-09 11:19:21.998990', '1', 'Delivery f34 - wqrw', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 1),
(57, '2025-05-09 11:20:12.383597', '4', 'Delivery None - None', 2, '[{\"changed\": {\"fields\": [\"Sales person\"]}}]', 11, 1),
(58, '2025-05-09 11:20:32.500620', '9', 'Delivery None - None', 2, '[{\"changed\": {\"fields\": [\"Date of billing\", \"Sales person\"]}}]', 11, 1),
(59, '2025-05-09 11:55:04.383815', '7', 'Estimates', 1, '[{\"added\": {}}]', 2, 1),
(60, '2025-05-09 12:01:23.629110', '7', 'crm', 1, '[{\"added\": {}}]', 3, 1),
(61, '2025-05-09 12:03:40.722515', '7', 'crm', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Role\", \"Region of Operation\"]}}]', 3, 1),
(62, '2025-05-09 12:05:26.155855', '7', 'estimates', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 3, 1);

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
(14, 'admin', 'logentry'),
(19, 'auditlog', 'logentry'),
(16, 'auth', 'group'),
(15, 'auth', 'permission'),
(17, 'contenttypes', 'contenttype'),
(1, 'erp', 'customer'),
(11, 'erp', 'deliverynote'),
(13, 'erp', 'deliverynoteitem'),
(2, 'erp', 'department'),
(9, 'erp', 'dispatch'),
(3, 'erp', 'employee'),
(4, 'erp', 'estimate'),
(10, 'erp', 'estimateitem'),
(8, 'erp', 'notification'),
(21, 'erp', 'regionofoperation'),
(5, 'erp', 'sparepart'),
(7, 'erp', 'storesreconciliation'),
(20, 'erp', 'testingmodel'),
(12, 'erp', 'userrole'),
(6, 'erp', 'verification'),
(18, 'sessions', 'session');

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
(1, 'contenttypes', '0001_initial', '2025-04-29 13:41:54.185539'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-04-29 13:41:54.224263'),
(3, 'auth', '0001_initial', '2025-04-29 13:41:54.349095'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-04-29 13:41:54.372893'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-04-29 13:41:54.377805'),
(6, 'auth', '0004_alter_user_username_opts', '2025-04-29 13:41:54.382887'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-04-29 13:41:54.389262'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-04-29 13:41:54.391244'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-04-29 13:41:54.396322'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-04-29 13:41:54.401666'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-04-29 13:41:54.407541'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-04-29 13:41:54.422509'),
(13, 'auth', '0011_update_proxy_permissions', '2025-04-29 13:41:54.427659'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-04-29 13:41:54.433077'),
(15, 'erp', '0001_initial', '2025-04-29 13:41:55.022132'),
(16, 'admin', '0001_initial', '2025-04-29 13:41:55.081949'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-04-29 13:41:55.090921'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-29 13:41:55.103050'),
(19, 'auditlog', '0001_initial', '2025-04-29 13:41:55.184656'),
(20, 'auditlog', '0002_auto_support_long_primary_keys', '2025-04-29 13:41:55.265727'),
(21, 'auditlog', '0003_logentry_remote_addr', '2025-04-29 13:41:55.287348'),
(22, 'auditlog', '0004_logentry_detailed_object_repr', '2025-04-29 13:41:55.310708'),
(23, 'auditlog', '0005_logentry_additional_data_verbose_name', '2025-04-29 13:41:55.325662'),
(24, 'auditlog', '0006_object_pk_index', '2025-04-29 13:41:55.386177'),
(25, 'auditlog', '0007_object_pk_type', '2025-04-29 13:41:55.394842'),
(26, 'auditlog', '0008_action_index', '2025-04-29 13:41:55.421346'),
(27, 'auditlog', '0009_alter_logentry_additional_data', '2025-04-29 13:41:55.431671'),
(28, 'auditlog', '0010_alter_logentry_timestamp', '2025-04-29 13:41:55.459565'),
(29, 'auditlog', '0011_logentry_serialized_data', '2025-04-29 13:41:55.486915'),
(30, 'auditlog', '0012_add_logentry_action_access', '2025-04-29 13:41:55.502032'),
(31, 'auditlog', '0013_alter_logentry_timestamp', '2025-04-29 13:41:55.515553'),
(32, 'auditlog', '0014_logentry_cid', '2025-04-29 13:41:55.551548'),
(33, 'auditlog', '0015_alter_logentry_changes', '2025-04-29 13:41:55.664696'),
(34, 'erp', '0002_alter_deliveryconfirmation_options_and_more', '2025-04-29 13:41:55.949343'),
(35, 'erp', '0003_alter_dispatch_estimate', '2025-04-29 13:41:56.030659'),
(36, 'erp', '0004_remove_dispatch_is_delivered_and_more', '2025-04-29 13:41:56.099502'),
(37, 'erp', '0005_deliverynote_delete_deliveryconfirmation', '2025-04-29 13:41:56.116409'),
(38, 'erp', '0006_alter_estimate_customer_alter_estimate_sales_agent', '2025-04-29 13:41:56.298258'),
(39, 'erp', '0007_alter_customer_options_remove_customer_address_and_more', '2025-04-29 13:41:56.637587'),
(40, 'erp', '0008_userrole_remove_customer_business_billboard_and_more', '2025-04-29 13:41:56.740925'),
(41, 'erp', '0009_alter_deliverynote_options_and_more', '2025-04-29 13:41:57.109269'),
(42, 'erp', '0010_remove_deliverynote_created_at', '2025-04-29 13:41:57.126593'),
(43, 'erp', '0011_remove_deliverynoteitem_s_no_deliverynote_created_at_and_more', '2025-04-29 13:41:57.252201'),
(44, 'erp', '0012_deliverynote_delivery_note_number', '2025-04-29 13:41:57.268213'),
(45, 'erp', '0013_deliverynote_status', '2025-04-29 13:41:57.294831'),
(46, 'erp', '0014_rename_uploaded_image_deliverynote_image', '2025-04-29 13:41:57.312279'),
(47, 'sessions', '0001_initial', '2025-04-29 13:41:57.341289'),
(48, 'erp', '0015_alter_employee_department', '2025-04-29 13:44:03.554007'),
(49, 'erp', '0016_customer_national_id', '2025-05-02 12:11:47.603351'),
(50, 'erp', '0017_rename_designation_customer_approved_by_and_more', '2025-05-02 13:07:01.374068'),
(51, 'erp', '0018_rename_date_of_delivery_deliverynote_date_of_billing_and_more', '2025-05-02 14:28:34.043165'),
(52, 'erp', '0019_rename_cutomer_name_deliverynote_customer_name', '2025-05-02 14:31:19.638742'),
(53, 'erp', '0002_testingmodel', '2025-05-03 11:04:45.841858'),
(54, 'erp', '0003_delete_testingmodel_and_more', '2025-05-03 11:11:43.322375'),
(55, 'erp', '0015_rename_designation_customer_approved_by_and_more', '2025-05-03 11:43:22.934057'),
(56, 'erp', '0016_deliverynote_designation', '2025-05-03 11:44:21.591957'),
(57, 'erp', '0018_deliverynote_test_tqc', '2025-05-03 11:49:28.320583'),
(58, 'erp', '0019_remove_deliverynote_test_tqc', '2025-05-03 11:49:50.481566'),
(59, 'erp', '0020_alter_deliverynote_estimate_number', '2025-05-03 12:47:28.617714'),
(60, 'erp', '0021_remove_deliverynote_delivery_no_and_more', '2025-05-06 13:30:15.856969'),
(61, 'erp', '0022_regionofoperation_employee_region_of_operation', '2025-05-08 09:07:03.884532'),
(62, 'erp', '0023_alter_employee_region_of_operation', '2025-05-08 09:19:04.018693'),
(63, 'erp', '0024_alter_dispatch_options_and_more', '2025-05-08 13:11:50.002757'),
(64, 'erp', '0025_alter_employee_region_of_operation', '2025-05-09 12:00:40.031557'),
(65, 'erp', '0026_remove_estimate_customer_remove_estimate_sales_agent_and_more', '2025-05-09 12:53:31.570929'),
(66, 'erp', '0027_remove_estimate_received_date', '2025-05-09 13:30:54.869743'),
(67, 'erp', '0028_alter_employee_options_alter_estimate_sales_person', '2025-05-10 12:45:44.237783');

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
('7im5qxhusc5nnfwc8gqban034ab6s9iy', '.eJxVjEEOwiAQRe_C2hAGGFpcuu8ZyABTqRqalHZlvLtt0oVu33v_v0WgbS1ha7yEKYurQHH5ZZHSk-sh8oPqfZZprusyRXkk8rRNDnPm1-1s_w4KtbKvLTjbQVZjMtp457OO1ClA349WKbAqgTYGyTvsITL6zBwNJpVoJ9aLzxetlDau:1uCw1C:-R1msot8sH68lK56XHFamcx5-64_vsvyBN1QQZC2SUk', '2025-05-22 07:50:10.313708'),
('bk6r0dd9mz0xxi81wuxmjdrn0lq1wh4v', '.eJxVjDEOwyAQBP9CHSFjc3CkTO83II6D4CTCkrGrKH-PLblImi12ZvctfNjW4reWFj-xuAorLr8dhfhM9QD8CPU-yzjXdZlIHoo8aZPjzOl1O92_gxJa2deJexuHgAqSRibbmQwMJmaHjpQD0lp32ANjAu1UzJaiJdxDA5rBiM8X5z03nw:1uDeZb:whtP-D6z0hiVRJeahCd0WW8Kc3JUbx0QBv5r-q27fSg', '2025-05-24 07:24:39.425452'),
('cgze0wkrskl3rnjzrq74pkvptca0lanq', '.eJxVjEEOwiAQRe_C2hAGGFpcuu8ZyABTqRqalHZlvLtt0oVu33v_v0WgbS1ha7yEKYurQHH5ZZHSk-sh8oPqfZZprusyRXkk8rRNDnPm1-1s_w4KtbKvLTjbQVZjMtp457OO1ClA349WKbAqgTYGyTvsITL6zBwNJpVoJ9aLzxetlDau:1uCIZX:Pb5DCQ8jp6MsZ_xkKvSnJQrw0wMsoC7gMDA-xKOJtzE', '2025-05-20 13:42:59.339086');

-- --------------------------------------------------------

--
-- Table structure for table `erp_customer`
--

CREATE TABLE `erp_customer` (
  `id` bigint(20) NOT NULL,
  `certificate_of_incorporation` varchar(100) DEFAULT NULL,
  `date_filled` datetime(6) DEFAULT NULL,
  `approved_by` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `name_of_business` varchar(200) DEFAULT NULL,
  `nearest_landmark` varchar(150) DEFAULT NULL,
  `next_of_kin` varchar(100) DEFAULT NULL,
  `next_of_kin_tel` varchar(15) DEFAULT NULL,
  `owner_name` varchar(100) DEFAULT NULL,
  `owner_tel` varchar(15) DEFAULT NULL,
  `passport_photo` varchar(100) DEFAULT NULL,
  `prepared_by` varchar(100) DEFAULT NULL,
  `prepared_date` date DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `road_location` varchar(150) DEFAULT NULL,
  `tel_1` varchar(15) DEFAULT NULL,
  `tel_2` varchar(15) DEFAULT NULL,
  `town_division` varchar(100) DEFAULT NULL,
  `trading_license` varchar(100) DEFAULT NULL,
  `national_id` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_customer`
--

INSERT INTO `erp_customer` (`id`, `certificate_of_incorporation`, `date_filled`, `approved_by`, `district`, `location`, `name_of_business`, `nearest_landmark`, `next_of_kin`, `next_of_kin_tel`, `owner_name`, `owner_tel`, `passport_photo`, `prepared_by`, `prepared_date`, `remarks`, `road_location`, `tel_1`, `tel_2`, `town_division`, `trading_license`, `national_id`) VALUES
(1, 'documents/certificates/Screenshot_From_2025-05-01_11-43-54.png', '2025-05-02 12:29:50.364071', 'Sales Person', 'Wakiso', 'Kawempe Mbogo, Kawempe, Kampala, Central Region, Uganda', 'New Spares Ltd', 'Nabweru Magistrrate', 'Mwesige', '049858085', 'Nankya Dorothy', '874989404', 'photos/passports/Screenshot_From_2025-04-29_16-45-54.png', 'James', '2025-05-09', 'Everything prepared', 'Central Markedt', '0398939030', '0389389940', 'Nansana', 'photos/license/Screenshot_From_2025-04-29_16-45-54.png', 'photos/national_id/Screenshot_From_2025-04-29_16-45-54.png'),
(2, 'documents/certificates/Email_Signature.png', '2025-05-09 14:19:27.638099', NULL, 'Wakiso', 'Kawempe Mbogo, Kawempe, Kampala, Central Region, Uganda', 'John Spares', 'Nan-12', 'Gideo', '07517673763', 'John Musingusi', '07517673763', 'photos/passports/Email_Signature.png', NULL, '2025-05-31', 'well noted', 'ESD Kayunga', '0756277827', '67889388', 'Nansana', 'photos/license/Email_Signature.png', 'photos/national_id/Email_Signature.png');

-- --------------------------------------------------------

--
-- Table structure for table `erp_deliverynote`
--

CREATE TABLE `erp_deliverynote` (
  `id` bigint(20) NOT NULL,
  `estimate_number` varchar(200) DEFAULT NULL,
  `customer_name_address` longtext DEFAULT NULL,
  `date_goods_received` date DEFAULT NULL,
  `extracted_text` longtext DEFAULT NULL,
  `receiver_contact` varchar(20) DEFAULT NULL,
  `receiver_name` varchar(100) DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `sales_person_id` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `created_at` varchar(100) DEFAULT NULL,
  `updated_at` varchar(100) DEFAULT NULL,
  `delivery_note_number` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `delivery_person` varchar(200) DEFAULT NULL,
  `invoice_no` varchar(100) DEFAULT NULL,
  `transaction_value` varchar(100) DEFAULT NULL,
  `date_of_billing` varchar(100) DEFAULT NULL,
  `sale_agent_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_deliverynote`
--

INSERT INTO `erp_deliverynote` (`id`, `estimate_number`, `customer_name_address`, `date_goods_received`, `extracted_text`, `receiver_contact`, `receiver_name`, `remarks`, `sales_person_id`, `image`, `created_at`, `updated_at`, `delivery_note_number`, `status`, `customer_name`, `delivery_person`, `invoice_no`, `transaction_value`, `date_of_billing`, `sale_agent_id`) VALUES
(1, NULL, '', NULL, '', 'rrwr', 'wqrw', '', '5', 'delivery_notes/Screenshot_From_2025-04-29_16-45-54_IFvtJ9B.png', NULL, NULL, 'f34', 'rejected', NULL, NULL, NULL, NULL, NULL, NULL),
(2, NULL, '', NULL, '', 'o0u9p', 'wqqee', '', '5', 'delivery_notes/Logo_v2jdXgA.png', NULL, NULL, 'wwwr', 'received', NULL, NULL, NULL, NULL, NULL, NULL),
(3, NULL, '', NULL, '', 'eeee', 'eeee', '', '5', 'delivery_notes/Screenshot_From_2025-04-29_16-45-54_nssJDq7.png', NULL, NULL, 'eeee', 'rejected', NULL, NULL, NULL, NULL, NULL, NULL),
(4, 'EST-2039', '', '2025-05-10', '', '0778793903', 'Francis', 'Delivered well', '5', 'delivery_notes/Email_Signature_nWCpuic.png', '2025-05-03 09:55:29', '2025-05-03 09:55:29', 'DEL-23748', 'received', 'Customer-1', 'Person1', 'Invoice-1', '20000', NULL, NULL),
(5, NULL, '', NULL, '', '2088399983', 'Frank', '', '5', 'delivery_notes/Logo.png', NULL, NULL, 'DEL-1930484', 'rejected', NULL, NULL, NULL, NULL, NULL, NULL),
(6, NULL, '', NULL, '', 'Namuddu', 'Mariam', '', '5', 'delivery_notes/Screenshot_From_2025-04-29_16-45-54_OJa6dAK.png', NULL, NULL, 'DEL-1236', 'received', NULL, NULL, NULL, NULL, NULL, NULL),
(7, 'EST-1903', '', '2025-05-09', '', '0784949494', 'Mzeee Freed', '', '5', 'delivery_notes/IMG_5102_KtdmMm5_yRYsIRM.jpg', '2025-05-05 11:27:19', '2025-05-05 11:27:19', 'DEL-1234', 'received', 'Joshua', 'Jesica', 'INV-2000', '2000', '2025-05-06', NULL),
(8, 'EST-1904', '', '2025-05-07', '', '07836537', 'Muzamiru', '', '5', 'delivery_notes/Email_Signature.png', '2025-05-06 13:42:25', '2025-05-06 13:42:25', 'DEL-389487', 'rejected', 'Joshua Kemmy', 'Farouk', 'INV-2001', '2400', '2025-05-07', NULL),
(9, '93904949', '', NULL, '', NULL, NULL, '', '5', '', '2025-05-07 15:00:35', '2025-05-07 15:00:35', NULL, 'pending', 'ywyueuyeueu', 'hjduiiue', 'INV983988948', '200888', '2025-05-10', NULL),
(10, 'oief0[u90w', '', '2025-05-09', '', 'ilwou', 'kiuweiou', 'oofupfwe', '5', 'delivery_notes/IMG_5102_KtdmMm5_yRYsIRM_tjentxr.jpg', '2025-05-07 15:01:19', '2025-05-07 15:01:19', 'wieiho', 'received', 'ioqiffihowe', 'jhaukioefw', 'uifqouife', '9843980', '2025-05-16', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `erp_deliverynoteitem`
--

CREATE TABLE `erp_deliverynoteitem` (
  `id` bigint(20) NOT NULL,
  `item_description` varchar(255) NOT NULL,
  `quantity` double NOT NULL,
  `delivery_note_id` bigint(20) NOT NULL,
  `item_code` varchar(100) DEFAULT NULL
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
(1, 'Sales', ''),
(2, 'CRM', 'Customer relations Management department'),
(3, 'Credit Control', 'Verification of the customer\'s credit'),
(4, 'Billing', 'Determine the cost of the items in the estimates'),
(5, 'Stores', 'Inventory management of the items'),
(6, 'Dispatch', 'Handle the item packing and delivering of the items through the courier'),
(7, 'Estimates', 'Receive Customer Estimates');

-- --------------------------------------------------------

--
-- Table structure for table `erp_dispatch`
--

CREATE TABLE `erp_dispatch` (
  `id` bigint(20) NOT NULL,
  `billing_date` date DEFAULT NULL,
  `customer_name` varchar(200) DEFAULT NULL,
  `invoice_amount` varchar(100) DEFAULT NULL,
  `invoice_no` varchar(100) DEFAULT NULL,
  `office_gate_pass` varchar(100) DEFAULT NULL,
  `store_gate_pass` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

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
  `department_id` bigint(20) DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  `region_of_operation_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_employee`
--

INSERT INTO `erp_employee` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `phone`, `department_id`, `is_verified`, `role_id`, `region_of_operation_id`) VALUES
(1, 'pbkdf2_sha256$390000$vgMmYBAV24hqSOTQyzePZ9$St6epRfXICeMCWYL58wjN0VWYxq1vQl2Dlu9g63+oC0=', '2025-05-09 12:04:54.405036', 1, 'admin', '', '', '', 1, 1, '2025-04-29 13:44:17.000000', '', NULL, 0, 4, NULL),
(2, 'sales2025?', NULL, 0, 'moses', 'Moses', 'Kasibante', 'moseskasiba@gmail.com', 0, 1, '2025-04-30 06:56:06.000000', '07835774676', 1, 0, 1, 2),
(3, 'sales', NULL, 0, 'rhoda', 'Rhodah', 'Nakimuli', 'sales@gmil.com', 0, 1, '2025-05-03 09:59:41.000000', '0848904', 1, 0, 1, 1),
(4, 'pbkdf2_sha256$390000$JlHjqHQRUZK47hYEgSxFiW$U7UISmxIu7SN7yOAVlyDvS3SeIQRI5DlhG4RiA8XhhU=', '2025-05-10 07:23:57.809555', 0, 'delivery', 'Ali', 'Moses', 'delivery@autozonpro.org', 0, 1, '2025-05-05 10:31:34.000000', '038484904', 6, 0, 5, NULL),
(5, 'pbkdf2_sha256$390000$ZRpI8mp3hKDgfsbhDg8pIp$vgvbcjyguiZsVttTVOUipvTexrXOxrGIbm/Qe6uKIJ0=', '2025-05-10 07:22:54.079267', 0, 'davies', 'David', 'Kato', 'davies@gmail.com', 0, 1, '2025-05-05 11:29:33.000000', '0786373667', 1, 0, 1, 5),
(6, 'pbkdf2_sha256$390000$QRazrMiTmj3r4BsxhGFI4X$7/0PfaQSeYO+3I0aQ10meXT1mK7D7+z25r75dZuboYE=', '2025-05-06 13:41:18.904813', 0, 'yamal', 'Yamal', '', '', 0, 1, '2025-05-06 13:39:33.000000', '', 6, 0, 5, NULL),
(7, 'pbkdf2_sha256$390000$FjABzzZGM2kX1mxLV36KGE$d7/FdvsrciHejvCBVwvKCjtk7zGkFh5QJqTct4/CQvw=', '2025-05-10 07:24:39.422801', 0, 'estimates', 'Jolly', 'Naka', 'estimates@autozonepro.org', 0, 1, '2025-05-09 12:01:23.503714', '', 7, 0, 2, 2);

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
  `bk_estimate_id` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `created_date` date DEFAULT NULL,
  `customer_name_id` bigint(20) DEFAULT NULL,
  `receiver_id` bigint(20) DEFAULT NULL,
  `sales_person_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_estimate`
--

INSERT INTO `erp_estimate` (`id`, `bk_estimate_id`, `status`, `created_at`, `updated_at`, `amount`, `created_date`, `customer_name_id`, `receiver_id`, `sales_person_id`) VALUES
(1, 'EST-2025-0001', 'draft', '2025-05-09 14:31:06.027473', '2025-05-09 14:31:06.027516', 0.00, NULL, NULL, NULL, NULL),
(2, '7986896', 'draft', '2025-05-10 12:11:41.847434', '2025-05-10 12:11:41.847480', 2000.00, '2025-05-31', NULL, NULL, NULL),
(3, 'EST-2025-00023', 'draft', '2025-05-10 12:52:34.786433', '2025-05-10 12:52:34.786488', 346.00, '2025-05-08', NULL, NULL, 2);

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
-- Table structure for table `erp_region`
--

CREATE TABLE `erp_region` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `erp_region`
--

INSERT INTO `erp_region` (`id`, `name`, `description`) VALUES
(1, 'Central', '');

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
(1, 'Central', 'Kampala Business Area'),
(2, 'Office', 'Working at the office'),
(3, 'Eastern', 'Mbale, Sironko, Kapichorwa\r\nManafwa'),
(4, 'Western', 'Mbarara, Rukungiri, Kabaale'),
(5, 'North', 'Gulu, Arua');

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
(1, 'Sales Officer', 'Handling the marketing'),
(2, 'Estimates Officer', 'Handling estimates'),
(3, 'Head of Sales', ''),
(4, 'Admin', ''),
(5, 'Delivery Officer', 'Work on delivery'),
(6, 'Dispatch Officer', 'Handle dispatching item details'),
(7, 'Outstanding Officer', ''),
(8, 'Billing Officer', ''),
(9, 'CRM Officer', '');

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
-- Indexes for table `erp_deliverynote`
--
ALTER TABLE `erp_deliverynote`
  ADD PRIMARY KEY (`id`),
  ADD KEY `erp_deliverynote_sale_agent_id_8a3ff71e_fk_erp_employee_id` (`sale_agent_id`);

--
-- Indexes for table `erp_deliverynoteitem`
--
ALTER TABLE `erp_deliverynoteitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `erp_deliverynoteitem_delivery_note_id_5aa0e851_fk_erp_deliv` (`delivery_note_id`);

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
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `erp_employee`
--
ALTER TABLE `erp_employee`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `erp_employee_role_id_0f6cc713_fk_erp_userrole_id` (`role_id`),
  ADD KEY `erp_employee_department_id_9eca106d_fk_erp_department_id` (`department_id`),
  ADD KEY `erp_employee_region_of_operation__8206b6d5_fk_erp_regio` (`region_of_operation_id`);

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
  ADD KEY `erp_estimate_customer_name_id_3207241c_fk_erp_customer_id` (`customer_name_id`),
  ADD KEY `erp_estimate_receiver_id_e156689e_fk_erp_employee_id` (`receiver_id`),
  ADD KEY `erp_estimate_sales_person_id_8cdb94e9_fk_erp_employee_id` (`sales_person_id`);

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
-- Indexes for table `erp_region`
--
ALTER TABLE `erp_region`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=88;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT for table `erp_customer`
--
ALTER TABLE `erp_customer`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `erp_deliverynote`
--
ALTER TABLE `erp_deliverynote`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `erp_deliverynoteitem`
--
ALTER TABLE `erp_deliverynoteitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_department`
--
ALTER TABLE `erp_department`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `erp_dispatch`
--
ALTER TABLE `erp_dispatch`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `erp_employee`
--
ALTER TABLE `erp_employee`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
-- AUTO_INCREMENT for table `erp_region`
--
ALTER TABLE `erp_region`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `erp_regionofoperation`
--
ALTER TABLE `erp_regionofoperation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

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
-- Constraints for table `erp_deliverynote`
--
ALTER TABLE `erp_deliverynote`
  ADD CONSTRAINT `erp_deliverynote_sale_agent_id_8a3ff71e_fk_erp_employee_id` FOREIGN KEY (`sale_agent_id`) REFERENCES `erp_employee` (`id`);

--
-- Constraints for table `erp_deliverynoteitem`
--
ALTER TABLE `erp_deliverynoteitem`
  ADD CONSTRAINT `erp_deliverynoteitem_delivery_note_id_5aa0e851_fk_erp_deliv` FOREIGN KEY (`delivery_note_id`) REFERENCES `erp_deliverynote` (`id`);

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
  ADD CONSTRAINT `erp_estimate_customer_name_id_3207241c_fk_erp_customer_id` FOREIGN KEY (`customer_name_id`) REFERENCES `erp_customer` (`id`),
  ADD CONSTRAINT `erp_estimate_receiver_id_e156689e_fk_erp_employee_id` FOREIGN KEY (`receiver_id`) REFERENCES `erp_employee` (`id`),
  ADD CONSTRAINT `erp_estimate_sales_person_id_8cdb94e9_fk_erp_employee_id` FOREIGN KEY (`sales_person_id`) REFERENCES `erp_employee` (`id`);

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
