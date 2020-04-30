/*
 Navicat Premium Data Transfer

 Source Server         : spider
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost:3306
 Source Schema         : monitor

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : 65001

 Date: 29/04/2020 21:49:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bar
-- ----------------------------
DROP TABLE IF EXISTS `bar`;
CREATE TABLE `bar` (
  `平台` varchar(255) DEFAULT NULL,
  `项目` varchar(255) DEFAULT NULL,
  `数量` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of bar
-- ----------------------------
BEGIN;
INSERT INTO `bar` VALUES ('资讯', '新闻手机端', 182033);
INSERT INTO `bar` VALUES ('资讯', '新闻网页端', 128488);
INSERT INTO `bar` VALUES ('资讯', '微信', 95000);
INSERT INTO `bar` VALUES ('资讯', '微博', 84888);
INSERT INTO `bar` VALUES ('资讯', '纸媒', 61777);
INSERT INTO `bar` VALUES ('口碑', '微博', 18200);
INSERT INTO `bar` VALUES ('口碑', '美团', 15844);
INSERT INTO `bar` VALUES ('口碑', '贴吧', 9544);
INSERT INTO `bar` VALUES ('口碑', '股吧', 6477);
INSERT INTO `bar` VALUES ('口碑', '论坛', 5111);
INSERT INTO `bar` VALUES ('资讯', '钉钉', 73773);
INSERT INTO `bar` VALUES ('口碑', 'B站', 7366);
COMMIT;

-- ----------------------------
-- Table structure for pie
-- ----------------------------
DROP TABLE IF EXISTS `pie`;
CREATE TABLE `pie` (
  `来源` varchar(255) DEFAULT NULL,
  `正面` int(16) DEFAULT NULL,
  `负面` int(16) DEFAULT NULL,
  `中性` int(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of pie
-- ----------------------------
BEGIN;
INSERT INTO `pie` VALUES ('微信', 300, 200, 500);
INSERT INTO `pie` VALUES ('微博', 247, 341, 429);
INSERT INTO `pie` VALUES ('美团', 332, 486, 231);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
