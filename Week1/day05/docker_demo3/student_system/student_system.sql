/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80406
 Source Host           : localhost:3306
 Source Schema         : student_system

 Target Server Type    : MySQL
 Target Server Version : 80406
 File Encoding         : 65001

 Date: 29/12/2025 15:55:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '账号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头像',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '管理员信息' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 'admin', 'admin', '管理员', 'http://localhost:9090/files/download/1.png', '管理员');

-- ----------------------------
-- Table structure for clazz
-- ----------------------------
DROP TABLE IF EXISTS `clazz`;
CREATE TABLE `clazz`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `major_id` int NULL DEFAULT NULL COMMENT '专业ID',
  `teacher` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '班主任',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '班级信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of clazz
-- ----------------------------
INSERT INTO `clazz` VALUES (1, 'JK101', '计算机1班', 1, '李德全');
INSERT INTO `clazz` VALUES (2, 'JK102', '计算机2班', 1, '李武峰');
INSERT INTO `clazz` VALUES (3, 'DZ101', '电子1班', 2, '王凯华');
INSERT INTO `clazz` VALUES (4, 'DZ102', '电子2班', 2, '王凯慧');

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `teacher` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '老师',
  `score` int NULL DEFAULT NULL COMMENT '学分',
  `major_id` int NULL DEFAULT NULL COMMENT '所属专业',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '课程信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES (3, 'CS101', '计算机导论', '张伟', 2, 1);
INSERT INTO `course` VALUES (4, 'CS102', 'C语言程序设计', '李明', 3, 1);
INSERT INTO `course` VALUES (5, 'CS103', '数据结构', '王芳', 4, 1);
INSERT INTO `course` VALUES (6, 'CS104', '操作系统原理', '赵刚', 3, 1);
INSERT INTO `course` VALUES (7, 'CS105', '数据库系统', '刘洋', 3, 1);
INSERT INTO `course` VALUES (8, 'CS106', '计算机网络', '陈静', 3, 1);
INSERT INTO `course` VALUES (9, 'CS107', '软件工程', '孙磊', 3, 1);
INSERT INTO `course` VALUES (10, 'CS108', '人工智能基础', '周慧', 2, 1);
INSERT INTO `course` VALUES (11, 'CS109', 'Web前端开发', '吴昊', 3, 1);
INSERT INTO `course` VALUES (12, 'CS110', 'Python数据分析', '郑涛', 3, 1);
INSERT INTO `course` VALUES (13, 'CS201', 'Java高级编程', '钱勇', 4, 1);
INSERT INTO `course` VALUES (14, 'CS202', '算法设计与分析', '朱琳', 4, 1);
INSERT INTO `course` VALUES (15, 'CS203', '计算机组成原理', '何强', 3, 1);
INSERT INTO `course` VALUES (16, 'CS204', 'Linux系统管理', '马超', 2, 1);
INSERT INTO `course` VALUES (17, 'CS205', '移动应用开发', '宋佳', 3, 1);
INSERT INTO `course` VALUES (18, 'EE101', '电路分析基础', '黄建国', 3, 2);
INSERT INTO `course` VALUES (19, 'EE102', '模拟电子技术', '徐敏', 4, 2);
INSERT INTO `course` VALUES (20, 'EE103', '数字电子技术', '高伟', 3, 2);
INSERT INTO `course` VALUES (21, 'EE104', '信号与系统', '林芳', 4, 2);
INSERT INTO `course` VALUES (22, 'EE105', '电磁场理论', '谢军', 3, 2);
INSERT INTO `course` VALUES (23, 'EE106', '通信原理', '罗斌', 3, 2);
INSERT INTO `course` VALUES (24, 'EE107', '微机原理与接口', '唐娜', 3, 2);
INSERT INTO `course` VALUES (25, 'EE108', '数字信号处理', '董华', 3, 2);
INSERT INTO `course` VALUES (26, 'EE109', '电力电子技术', '韩梅', 3, 2);
INSERT INTO `course` VALUES (27, 'EE110', '嵌入式系统设计', '曹阳', 4, 2);
INSERT INTO `course` VALUES (28, 'EE201', '自动控制原理', '彭丽', 3, 2);
INSERT INTO `course` VALUES (29, 'EE202', '传感器技术', '方明', 2, 2);
INSERT INTO `course` VALUES (30, 'EE203', 'VLSI设计基础', '苏婷', 3, 2);
INSERT INTO `course` VALUES (31, 'EE204', '射频电路设计', '姜涛', 3, 2);
INSERT INTO `course` VALUES (32, 'EE205', '物联网技术', '程琳', 3, 2);

-- ----------------------------
-- Table structure for grade
-- ----------------------------
DROP TABLE IF EXISTS `grade`;
CREATE TABLE `grade`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `student_id` int NULL DEFAULT NULL COMMENT '学生ID',
  `course_id` int NULL DEFAULT NULL COMMENT '课程ID',
  `score` int NULL DEFAULT NULL COMMENT '成绩',
  `ispass` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '是否及格',
  `time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '成绩信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of grade
-- ----------------------------
INSERT INTO `grade` VALUES (3, 7, 4, 60, '是', '2025-12-25 17:25:02');
INSERT INTO `grade` VALUES (4, 6, 3, 90, '是', '2025-12-25 17:25:31');
INSERT INTO `grade` VALUES (5, 6, 5, 80, '是', '2025-12-25 17:27:45');

-- ----------------------------
-- Table structure for major
-- ----------------------------
DROP TABLE IF EXISTS `major`;
CREATE TABLE `major`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '专业代码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `college` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '所属学院',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '专业信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of major
-- ----------------------------
INSERT INTO `major` VALUES (1, 'JS22001', '计算机科学与技术', '计算机学院');
INSERT INTO `major` VALUES (2, 'DZ10101', '电子信息工程', '电子工程学院');

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '标题',
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '内容',
  `time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '系统公告' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice
-- ----------------------------
INSERT INTO `notice` VALUES (1, '新学期选课通知', '各位同学请注意，本学年第二学期选课系统将于明天上午9:00正式开放。请同学们提前登录教务系统查看课程安排，合理安排选课时间。选课截止日期为后天下午17:00，逾期不予补选。如有疑问请联系各学院教务办公室。', '2025-12-29 15:41:52');
INSERT INTO `notice` VALUES (2, ' 关于国家助学金申请材料提交的提醒', '请已申请本学年国家助学金的同学，将完整的纸质版申请材料（包括申请表、家庭情况调查表及相关证明）交至学生处资助管理中心（行政楼201室）。材料不全或逾期未交者，将视为自动放弃申请资格。', '2025-12-29 15:42:02');
INSERT INTO `notice` VALUES (3, '沃林Ric带你做项目', '带你学习FastAPI + Vue的前后端分离项目', '2025-12-29 15:44:31');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '账号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头像',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色',
  `clazz_id` int NULL DEFAULT NULL COMMENT '班级',
  `score` int NULL DEFAULT NULL COMMENT '学分',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '学生信息' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (6, 'aaa', '123', '小张', 'http://127.0.0.1:9090/files/download/4.png', '学生', 2, 6);
INSERT INTO `student` VALUES (7, 'bbb', '123', '小王', 'http://127.0.0.1:9090/files/download/5.png', '学生', 2, 3);
INSERT INTO `student` VALUES (8, 'ccc', '123', '小陆', 'http://127.0.0.1:9090/files/download/3.jpeg', '学生', 2, 0);
INSERT INTO `student` VALUES (9, 'ddd', '123', '小慧', 'http://127.0.0.1:9090/files/download/2.png', '学生', 3, 0);
INSERT INTO `student` VALUES (11, 'ggg', '123', '小李', 'http://127.0.0.1:9090/files/download/酷.png', '学生', 1, 0);
INSERT INTO `student` VALUES (12, 'kkk', '123', '小华', 'http://127.0.0.1:9090/files/download/酷.png', '学生', 2, 0);
INSERT INTO `student` VALUES (13, 'mmm', '123', 'mmm', NULL, '学生', NULL, 0);

-- ----------------------------
-- Table structure for student_course
-- ----------------------------
DROP TABLE IF EXISTS `student_course`;
CREATE TABLE `student_course`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `student_id` int NULL DEFAULT NULL COMMENT '学生ID',
  `course_id` int NULL DEFAULT NULL COMMENT '课程ID',
  `year` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '学年',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '选课状态',
  `check_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '审核状态',
  `time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '选课时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '选课信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_course
-- ----------------------------
INSERT INTO `student_course` VALUES (2, 6, 3, '2025-2026', '已选', '通过', '2025-12-25 16:10:28');
INSERT INTO `student_course` VALUES (3, 7, 4, '2025-2026', '未选中', '拒绝', '2025-12-25 16:23:26');
INSERT INTO `student_course` VALUES (4, 7, 4, '2025-2026', '已选', '通过', '2025-12-25 16:24:36');
INSERT INTO `student_course` VALUES (5, 6, 5, '2025-2026', '已选', '通过', '2025-12-25 17:27:17');
INSERT INTO `student_course` VALUES (6, 6, 6, '2025-2026', '已选', '通过', '2025-12-25 17:39:36');
INSERT INTO `student_course` VALUES (7, 6, 7, '2025-2026', '申请中', '待审核', '2025-12-25 17:44:02');

SET FOREIGN_KEY_CHECKS = 1;
