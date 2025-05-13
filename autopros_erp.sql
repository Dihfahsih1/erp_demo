-- phpMyAdmin SQL Dump
-- version 5.2.2deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 12, 2025 at 03:00 PM
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


-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

 
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
(62, '2025-05-09 12:05:26.155855', '7', 'estimates', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 3, 1),
(63, '2025-05-12 08:17:18.009010', '8', 'scovia', 1, '[{\"added\": {}}]', 3, 1),
(64, '2025-05-12 08:17:58.193714', '7', 'Credit Officer', 2, '[{\"changed\": {\"fields\": [\"Role Name\"]}}]', 12, 1),
(65, '2025-05-12 08:18:08.585801', '8', 'scovia', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Role\", \"Region of Operation\"]}}]', 3, 1),
(66, '2025-05-12 08:18:38.349639', '4', 'delivery', 2, '[{\"changed\": {\"fields\": [\"Region of Operation\"]}}]', 3, 1),
(67, '2025-05-12 11:53:29.759222', '9', 'Maria', 1, '[{\"added\": {}}]', 3, 1),
(68, '2025-05-12 11:54:18.082149', '9', 'billing', 2, '[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Role\", \"Region of Operation\"]}}]', 3, 1),
(69, '2025-05-12 13:22:26.044732', '10', 'crm', 1, '[{\"added\": {}}]', 3, 1),
(70, '2025-05-12 13:23:10.567060', '10', 'crm', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Role\", \"Region of Operation\"]}}]', 3, 1),
(71, '2025-05-12 14:05:43.994105', '8', 'credit', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--
 
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
-- Dumping data for table `django_migrations`
--
 

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('5usr2o5swhsxi01f1hi5ye4u91dalq4k', '.eJxVjEEOwiAQRe_C2pBCizAu3fcMZJgZpGpoUtqV8e7apAvd_vfef6mI21ri1mSJE6uLGtTpd0tID6k74DvW26xprusyJb0r-qBNjzPL83q4fwcFW_nWPQs7yT4HwtAZAfaUDUDyAgDE1jLj0KUe0GUUw2cbRIxxFAIbn9T7AxrsOQ8:1uETny:sv7nAyk0tlzZ-Qys8Z7fOisBm2PZox3GVupYbF7m3-c', '2025-05-26 14:06:54.237878'),
('7im5qxhusc5nnfwc8gqban034ab6s9iy', '.eJxVjEEOwiAQRe_C2hAGGFpcuu8ZyABTqRqalHZlvLtt0oVu33v_v0WgbS1ha7yEKYurQHH5ZZHSk-sh8oPqfZZprusyRXkk8rRNDnPm1-1s_w4KtbKvLTjbQVZjMtp457OO1ClA349WKbAqgTYGyTvsITL6zBwNJpVoJ9aLzxetlDau:1uCw1C:-R1msot8sH68lK56XHFamcx5-64_vsvyBN1QQZC2SUk', '2025-05-22 07:50:10.313708'),
('cgze0wkrskl3rnjzrq74pkvptca0lanq', '.eJxVjEEOwiAQRe_C2hAGGFpcuu8ZyABTqRqalHZlvLtt0oVu33v_v0WgbS1ha7yEKYurQHH5ZZHSk-sh8oPqfZZprusyRXkk8rRNDnPm1-1s_w4KtbKvLTjbQVZjMtp457OO1ClA349WKbAqgTYGyTvsITL6zBwNJpVoJ9aLzxetlDau:1uCIZX:Pb5DCQ8jp6MsZ_xkKvSnJQrw0wMsoC7gMDA-xKOJtzE', '2025-05-20 13:42:59.339086');

-- --------------------------------------------------------

--
-- Table structure for table `erp_customer`
--

 
--
-- Dumping data for table `erp_customer`
--

INSERT INTO `erp_customer` (`id`, `certificate_of_incorporation`, `date_filled`, `approved_by`, `district`, `location`, `name_of_business`, `nearest_landmark`, `next_of_kin`, `next_of_kin_tel`, `owner_name`, `owner_tel`, `passport_photo`, `prepared_by`, `prepared_date`, `remarks`, `road_location`, `tel_1`, `tel_2`, `town_division`, `trading_license`, `national_id`) VALUES
(1, 'documents/certificates/Screenshot_From_2025-05-01_11-43-54.png', '2025-05-02 12:29:50.364071', 'Sales Person', 'Wakiso', 'Kawempe Mbogo, Kawempe, Kampala, Central Region, Uganda', 'New Spares Ltd', 'Nabweru Magistrrate', 'Mwesige', '049858085', 'Nankya Dorothy', '874989404', 'photos/passports/Screenshot_From_2025-04-29_16-45-54.png', 'James', '2025-05-09', 'Everything prepared', 'Central Markedt', '0398939030', '0389389940', 'Nansana', 'photos/license/Screenshot_From_2025-04-29_16-45-54.png', 'photos/national_id/Screenshot_From_2025-04-29_16-45-54.png'),
(2, 'documents/certificates/Email_Signature.png', '2025-05-09 14:19:27.638099', NULL, 'Wakiso', 'Kawempe Mbogo, Kawempe, Kampala, Central Region, Uganda', 'John Spares', 'Nan-12', 'Gideo', '07517673763', 'John Musingusi', '07517673763', 'photos/passports/Email_Signature.png', NULL, '2025-05-31', 'well noted', 'ESD Kayunga', '0756277827', '67889388', 'Nansana', 'photos/license/Email_Signature.png', 'photos/national_id/Email_Signature.png'),
(3, 'documents/certificates/Email_Signature_XibqKDd.png', '2025-05-12 13:33:58.216866', NULL, 'Kampala', 'Kawempe Mbogo, Kawempe, Kampala, Central Region, Uganda', 'Kawempe Auto Spares Garage', 'mosque rd', 'Musa', '+67468487474794', 'Lincoln Muchuba', '+26384874874784', 'photos/passports/Email_Signature_QJa7CVP.png', NULL, '2025-05-16', 'He is very dedicated to his work', 'kawempe ii', '+2567 674 947', '+256 788 888 83', 'Kawempe Division', 'photos/license/Email_Signature_YlsfSfg.png', 'photos/national_id/Email_Signature_T1O7yc2.png');

-- --------------------------------------------------------

--
-- Table structure for table `erp_deliverynote`
--
 
--
-- Dumping data for table `erp_deliverynote`
--

INSERT INTO `erp_deliverynote` (`id`, `estimate_number_id`, `date_goods_received`, `extracted_text`, `receiver_contact`, `receiver_name`, `remarks`, `image`, `created_at`, `updated_at`, `delivery_note_number`, `status`, `delivery_person`, `sale_agent_id`, `dispatch_authorized_by_id`, `packaging_verified_by_id`, `verified_by_id`) VALUES
(1, NULL, NULL, '', 'rrwr', 'wqrw', '', 'delivery_notes/Screenshot_From_2025-04-29_16-45-54_IFvtJ9B.png', NULL, NULL, 'f34', 'rejected', NULL, NULL, NULL, NULL, NULL),
(2, NULL, NULL, '', 'o0u9p', 'wqqee', '', 'delivery_notes/Logo_v2jdXgA.png', NULL, NULL, 'wwwr', 'received', NULL, NULL, NULL, NULL, NULL),
(3, NULL, NULL, '', 'eeee', 'eeee', '', 'delivery_notes/Screenshot_From_2025-04-29_16-45-54_nssJDq7.png', NULL, NULL, 'eeee', 'rejected', NULL, NULL, NULL, NULL, NULL),
(4, NULL, '2025-05-10', '', '0778793903', 'Francis', 'Delivered well', 'delivery_notes/Email_Signature_nWCpuic.png', '2025-05-03 09:55:29', '2025-05-03 09:55:29', 'DEL-23748', 'received', 'Person1', NULL, NULL, NULL, NULL),
(5, NULL, NULL, '', '2088399983', 'Frank', '', 'delivery_notes/Logo.png', NULL, NULL, 'DEL-1930484', 'rejected', NULL, NULL, NULL, NULL, NULL),
(6, NULL, NULL, '', 'Namuddu', 'Mariam', '', 'delivery_notes/Screenshot_From_2025-04-29_16-45-54_OJa6dAK.png', NULL, NULL, 'DEL-1236', 'received', NULL, NULL, NULL, NULL, NULL),
(7, NULL, '2025-05-09', '', '0784949494', 'Mzeee Freed', '', 'delivery_notes/IMG_5102_KtdmMm5_yRYsIRM.jpg', '2025-05-05 11:27:19', '2025-05-05 11:27:19', 'DEL-1234', 'received', 'Jesica', NULL, NULL, NULL, NULL),
(8, NULL, '2025-05-07', '', '07836537', 'Muzamiru', '', 'delivery_notes/Email_Signature.png', '2025-05-06 13:42:25', '2025-05-06 13:42:25', 'DEL-389487', 'rejected', 'Farouk', NULL, NULL, NULL, NULL),
(9, NULL, NULL, '', NULL, NULL, '', '', '2025-05-07 15:00:35', '2025-05-07 15:00:35', NULL, 'pending', 'hjduiiue', NULL, NULL, NULL, NULL),
(10, NULL, '2025-05-09', '', 'ilwou', 'kiuweiou', 'oofupfwe', 'delivery_notes/IMG_5102_KtdmMm5_yRYsIRM_tjentxr.jpg', '2025-05-07 15:01:19', '2025-05-07 15:01:19', 'wieiho', 'received', 'jhaukioefw', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `erp_deliverynoteitem`
--

 
-- --------------------------------------------------------

--
-- Table structure for table `erp_department`
- 
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

 
-- --------------------------------------------------------

--
-- Table structure for table `erp_employee`
--

 
--
-- Dumping data for table `erp_employee`
--

INSERT INTO `erp_employee` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `phone`, `department_id`, `is_verified`, `role_id`, `region_of_operation_id`) VALUES
(1, 'pbkdf2_sha256$390000$vgMmYBAV24hqSOTQyzePZ9$St6epRfXICeMCWYL58wjN0VWYxq1vQl2Dlu9g63+oC0=', '2025-05-12 13:59:44.216113', 1, 'admin', '', '', '', 1, 1, '2025-04-29 13:44:17.000000', '', NULL, 0, 4, NULL),
(2, 'sales2025?', NULL, 0, 'moses', 'Moses', 'Kasibante', 'moseskasiba@gmail.com', 0, 1, '2025-04-30 06:56:06.000000', '07835774676', 1, 0, 1, 2),
(3, 'sales', NULL, 0, 'rhoda', 'Rhodah', 'Nakimuli', 'sales@gmil.com', 0, 1, '2025-05-03 09:59:41.000000', '0848904', 1, 0, 1, 1),
(4, 'pbkdf2_sha256$390000$JlHjqHQRUZK47hYEgSxFiW$U7UISmxIu7SN7yOAVlyDvS3SeIQRI5DlhG4RiA8XhhU=', '2025-05-12 14:06:54.235371', 0, 'delivery', 'Ali', 'Moses', 'delivery@autozonpro.org', 0, 1, '2025-05-05 10:31:34.000000', '038484904', 6, 0, 5, 2),
(5, 'pbkdf2_sha256$390000$ZRpI8mp3hKDgfsbhDg8pIp$vgvbcjyguiZsVttTVOUipvTexrXOxrGIbm/Qe6uKIJ0=', '2025-05-12 09:31:35.783957', 0, 'davies', 'David', 'Kato', 'davies@gmail.com', 0, 1, '2025-05-05 11:29:33.000000', '0786373667', 1, 0, 1, 5),
(6, 'pbkdf2_sha256$390000$QRazrMiTmj3r4BsxhGFI4X$7/0PfaQSeYO+3I0aQ10meXT1mK7D7+z25r75dZuboYE=', '2025-05-06 13:41:18.904813', 0, 'yamal', 'Yamal', '', '', 0, 1, '2025-05-06 13:39:33.000000', '', 6, 0, 5, NULL),
(7, 'pbkdf2_sha256$390000$FjABzzZGM2kX1mxLV36KGE$d7/FdvsrciHejvCBVwvKCjtk7zGkFh5QJqTct4/CQvw=', '2025-05-12 13:35:15.599979', 0, 'estimates', 'Jolly', 'Naka', 'estimates@autozonepro.org', 0, 1, '2025-05-09 12:01:23.503714', '', 7, 0, 2, 2),
(8, 'pbkdf2_sha256$390000$mylh9y0LDXsd4cwbhd5rCO$JliNTCTeO3j4eGhZdip8L7L+xsp5th46mOxDKmRH4ks=', '2025-05-12 13:39:24.222735', 0, 'credit', 'Scovia', 'T', '', 0, 1, '2025-05-12 08:17:17.909852', '', 3, 0, 7, 2),
(9, 'pbkdf2_sha256$390000$2ZgGpsJjMVpbE3MlIcAWyM$UHFRESqAN4+5O0RfmHDRy5CMrqevWOZXgLUeVJRIDNU=', '2025-05-12 13:43:21.118815', 0, 'billing', 'Maria', 'The Biller', '', 0, 1, '2025-05-12 11:53:29.665444', '', 4, 0, 8, 2),
(10, 'pbkdf2_sha256$390000$TyGUqVVBBueejs3C5XEuQl$kOF36osKc8qEK9e5OBHbaI5qtzBLl/7gD0hMs3XWwGQ=', '2025-05-12 13:30:15.133721', 0, 'crm', 'Christine', 'Customer Relations', 'crm@autozonepro.org', 0, 1, '2025-05-12 13:22:25.948969', '', 2, 0, 9, 2);

-- --------------------------------------------------------

--
-- Table structure for table `erp_employee_groups`
--

 
-- --------------------------------------------------------

--
-- Table structure for table `erp_employee_user_permissions`
--

C 
-- --------------------------------------------------------

--
-- Table structure for table `erp_estimate`
--

 
--
-- Dumping data for table `erp_estimate`
--

INSERT INTO `erp_estimate` (`id`, `bk_estimate_id`, `status`, `created_at`, `updated_at`, `amount`, `created_date`, `customer_name_id`, `receiver_id`, `sales_person_id`, `date_billed`, `date_verified`, `invoice_amount`, `invoice_number`, `billing_officer_id`) VALUES
(10, 'EST-2025-0250', 'billed', '2025-05-12 07:26:40.866465', '2025-05-12 13:47:13.053389', 20000.00, '2025-05-16', 1, NULL, 3, '2025-05-12', '2025-05-12', 100000.00, 'INV-012099', 9),
(11, 'EST-2025-0251', 'cancelled', '2025-05-12 07:41:41.962259', '2025-05-12 08:44:09.589219', 3888.00, '2025-05-15', 2, NULL, 3, NULL, NULL, NULL, NULL, NULL),
(12, 'EST-2024-0252', 'billed', '2025-05-12 09:43:11.469222', '2025-05-12 12:32:22.115571', 20200.00, '2025-05-15', 2, NULL, 2, '2025-05-12', NULL, 200000.00, 'INV-12364', 1),
(13, 'EST-2025-0252', 'billed', '2025-05-12 13:35:51.102439', '2025-05-12 13:44:06.593842', 200000.00, '2025-05-10', 3, NULL, 3, '2025-05-12', '2025-05-12', 500000.00, 'INV-1209', 9);

-- --------------------------------------------------------

--
-- Table structure for table `erp_estimateitem`
--

 
-- --------------------------------------------------------

--
-- Table structure for table `erp_notification`
--

 
-- --------------------------------------------------------

--
-- Table structure for table `erp_userrole`
--

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
(7, 'Credit Officer', ''),
(8, 'Billing Officer', ''),
(9, 'CRM Officer', '');

-- --------------------------------------------------------

--
-- Table structure for table `erp_verification`
--

 
--
-- Indexes for dumped tables
--

--
-- Indexes for table `auditlog_logentry`
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
