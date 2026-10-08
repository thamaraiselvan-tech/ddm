-- ============================================================
-- EVENTIFY DBMS PROJECT - COMPLETE MYSQL DATABASE SCRIPT
-- Database Name: eventify_db
-- ============================================================

CREATE DATABASE IF NOT EXISTS `eventify_db`;
USE `eventify_db`;

-- ------------------------------------------------------------
-- 1. TABLE: events
-- Stores all event details hosted on the platform.
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `registrations`;
DROP TABLE IF EXISTS `events`;
DROP TABLE IF EXISTS `participants`;

CREATE TABLE `events` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(200) NOT NULL,
    `description` TEXT NOT NULL,
    `event_date` DATETIME NOT NULL,
    `venue` VARCHAR(250) NOT NULL,
    `max_seats` INT NOT NULL,
    `category` VARCHAR(50) NOT NULL DEFAULT 'workshop',
    `image_url` VARCHAR(500) NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 2. TABLE: participants
-- Stores participant contact details.
-- ------------------------------------------------------------
CREATE TABLE `participants` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(254) NOT NULL UNIQUE,
    `phone` VARCHAR(20) DEFAULT '',
    `college` VARCHAR(200) DEFAULT '',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 3. TABLE: registrations
-- Junction table connecting participants to events (Many-to-Many).
-- Includes UNIQUE constraint to prevent duplicate registrations.
-- ------------------------------------------------------------
CREATE TABLE `registrations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `event_id` INT NOT NULL,
    `participant_id` INT NOT NULL,
    `registered_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_reg_event` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_reg_participant` FOREIGN KEY (`participant_id`) REFERENCES `participants` (`id`) ON DELETE CASCADE,
    CONSTRAINT `unique_event_participant` UNIQUE (`event_id`, `participant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- SAMPLE DATA INSERTIONS
-- ============================================================

-- Insert Events
INSERT INTO `events` (`id`, `name`, `description`, `event_date`, `venue`, `max_seats`, `category`, `image_url`) VALUES
(1, 'HackFusion 2024', 'A 24-hour national level hackathon bringing together coders, designers, and innovators to build AI solutions.', '2026-10-25 09:00:00', 'Main Auditorium, Block A', 50, 'hackathon', 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800'),
(2, 'Full-Stack Web Dev Workshop', 'Hands-on practical session covering HTML5, CSS Grid, React, Django REST Framework, and MySQL integration.', '2026-10-28 14:00:00', 'Computer Lab 3, IT Building', 40, 'workshop', 'https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800'),
(3, 'AI & Future Tech Seminar', 'Expert talk by industry leaders from Google DeepMind and Microsoft on Generative AI and LLMs.', '2026-11-02 10:30:00', 'Mini Seminar Hall 2', 100, 'seminar', 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800'),
(4, 'Cloud Architecture Webinar', 'Online session explaining Microservices, Docker, Kubernetes, and AWS deployment pipelines.', '2026-11-05 18:00:00', 'Zoom / Google Meet Online', 200, 'webinar', 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800'),
(5, 'UI/UX Design Masterclass', 'Master Figma, design systems, modern typography, glassmorphism aesthetics, and accessibility.', '2026-11-10 11:00:00', 'Design Studio, 4th Floor', 30, 'workshop', 'https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?w=800'),
(6, 'CyberSecurity Capture The Flag (CTF)', 'Ethical hacking competition testing skills in cryptography, web security, and reverse engineering.', '2026-11-15 09:30:00', 'Cybersecurity Lab, 2nd Floor', 25, 'competition', 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800'),
(7, 'DevOps & CI/CD Summit', 'Conference on modern software delivery, pipeline automation, continuous testing, and monitoring.', '2026-11-20 09:00:00', 'Grand Convention Center', 150, 'conference', 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800'),
(8, 'Open Source Developers Meetup', 'Community gathering for open-source contributors, GitHub maintainers, and tech enthusiasts.', '2026-11-25 16:00:00', 'Innovation Hub, Central Library', 60, 'meetup', 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800');

-- Insert Participants
INSERT INTO `participants` (`id`, `name`, `email`, `phone`, `college`) VALUES
(1, 'Aarav Sharma', 'aarav.sharma@example.com', '9876543210', 'IIT Madras'),
(2, 'Ananya Sen', 'ananya.sen@example.com', '9876543211', 'NIT Trichy'),
(3, 'Rohan Verma', 'rohan.verma@example.com', '9876543212', 'Anna University'),
(4, 'Priya Patel', 'priya.patel@example.com', '9876543213', 'BITS Pilani'),
(5, 'Vikram Singh', 'vikram.singh@example.com', '9876543214', 'SRM Institute'),
(6, 'Sneha Reddy', 'sneha.reddy@example.com', '9876543215', 'VIT Vellore'),
(7, 'Karthik Raja', 'karthik.raja@example.com', '9876543216', 'PSG College of Tech'),
(8, 'Diya Mukherji', 'diya.m@example.com', '9876543217', 'Jadavpur University');

-- Insert Registrations
INSERT INTO `registrations` (`event_id`, `participant_id`, `registered_at`) VALUES
(1, 1, '2026-10-06 10:00:00'),
(1, 2, '2026-10-06 10:15:00'),
(1, 3, '2026-10-06 10:30:00'),
(1, 4, '2026-10-06 10:45:00'),
(1, 5, '2026-10-06 11:00:00'),
(2, 2, '2026-10-06 11:15:00'),
(2, 6, '2026-10-06 11:30:00'),
(2, 7, '2026-10-06 11:45:00'),
(3, 1, '2026-10-06 12:00:00'),
(3, 3, '2026-10-06 12:15:00'),
(3, 8, '2026-10-06 12:30:00'),
(4, 4, '2026-10-06 12:45:00'),
(4, 5, '2026-10-06 13:00:00'),
(5, 6, '2026-10-06 13:15:00'),
(5, 8, '2026-10-06 13:30:00'),
(6, 1, '2026-10-06 13:45:00'),
(6, 7, '2026-10-06 14:00:00'),
(7, 2, '2026-10-06 14:15:00'),
(7, 3, '2026-10-06 14:30:00'),
(7, 4, '2026-10-06 14:45:00'),
(8, 5, '2026-10-06 15:00:00'),
(8, 6, '2026-10-06 15:15:00');
