---
title: java 工程师面试过程中，比较经典的面试题有哪些？
description: 本文总结了 Java 工程师面试中的经典问题，涵盖了 Java 基础、集合框架、多线程、Spring Boot、Spring Cloud、MySQL 等多个方面。重点介绍了 Java 面向对象的三大特征、数据类型、String 类、集合类的区别与使用场景、HashMap 的底层实现、AOP 和 IOC 的概念、Spring Boot 的核心注解、MySQL 的事务特性及优化策略等。适合准备 Java 面试的开发者参考。
date: 2022-02-13 15:32:19
tags:
- 技术
categories:
- 编程与容器技术
---

## 说明  
本文的所有的 Springboot、SQL 资料均来源于网络以及 ChatGPT，本人只进行了些许整理。最初是为自己面试准备的，面试结束了分享给大家。如果您觉得没有帮助，请划走，如果您觉得有所帮助，可以帮忙点个关注，谢谢。

### Java 面向对象的三个特征  
封装：对象只需要选择性的对外公开一些属性和行为。继承：子对象可以继承父对象的属性和行为，并且可以在其之上进行修改以适合更特殊的场景需求。多态：允许不同类的对象对同一消息做出响应。

### Java 中基本的数据类型有哪些 以及他们的占用字节  
数据类型占用字节



| 数据类型 | 占用字节数 |
| --- | --- |
| byte | 1 |
| short | 2 |
| int | 4 |
| long | 8 |
| float | 4 |
| double | 8 |
| char | 2 |
| boolean | 4 |

### int 和 Integer 的区别  
int 是 Java 中的原始类型，Integer 是 Java 为 int 提供的封装类，他们有不同的特征和用法，包括大小、速度、默认值。

### String、StringBuilder、StringBuffer 的区别及使用场景  
String 一旦定义就不可改变，可空赋值。操作少量数据时使用。StringBuilder 可改变，线程不安全。操作单线程大量数据时使用。StringBuffer 可改变，线程安全。操作多线程大量数据时使用。

### ArrayList、Vector 和 LinkedList 的区别及使用场景  
ArrayList 和 Vector 都是使用数组方式存储数据，允许按序号索引元素，但是插入数据会涉及到元素移动等内存操作，所以索引快插入慢。

ArrayList 懒加载 默认大小### 每次扩容 1.5 倍 线程不安全 性能较高 Vector 实例化时初始化 默认大小### 每次扩容 2 倍 线程安全 性能较低 已弃用

额外回答加分项：多读少写建议使用 CopyOnWriteArrayList CopyOnWriteArrayList 原理是发生修改的时候复制一份 多写少读或读写比较均匀建议使用 Connections.synchronizedList

LinkedList 使用双向链表方式存储数据，插入只需要记录本项的前后项，索引需要向前或向后进行遍历，所以插入速度较快，线程不安全，频繁在任意位置插入和删除的情况可以使用，如果需要多线程访问，可以使用 Connections.synchronizedList() 或 ConcurrentLinkedQueue

### Collection 和 Collections 的区别  
Collection 是集合类上级接口，继承他的主要有 List 和 Set Collections 是集合类的帮助类，提供了对集合的搜索、排序、线程安全化等操作。

### List 和 Map 的区别  
List 是存储单列数据的集合，Map 是存储键值对双列数据的集合。List 存储的数据是有顺序且可重复的，Map 存储的数据是无顺序，键不可重复，值可重复的。

### HashMap 和 HashTable 的区别  
HashMap 是 Map 接口的实现，非线程安全，允许空键值。HashTable 是 Dictionary 的子类，线程安全，不允许空键值。几乎被淘汰，建议使用 ConcurrentHashMap 来替代它。HashMap 使用的是快速失败迭代器，在迭代器创建后，除非通过迭代器自身的 remove 或者 add 方法，其他任何方式的修改都会抛出异常。

### HashMap 底层实现原理和扩容机制  
JDK1.8 以前：数组 + 单链表的组合，以键值对的方式存储元素。JDK1.8 及以后：引入红黑树结构，添加元素时，若链表个数大于 8，链表会转换为红黑树，反之小于 6 时会修剪或还原成链表结构。选择 6 和 8 可以有效防止频繁的链表和红黑树转换。扩容条件：

存放新值的时候当前已有元素个数大于阈值。存放新值的时候当前存放数据发生 hash 碰撞（当前 key 计算的 hash 值换算出来的数组下标位置已经存在值）默认容量是 16，负载因子 0.75，所以扩容阈值是 12。每次扩容的容量是原有的 2 倍。

### HashMap 什么样的类适合作为键  
String 最为常见，因为 String 对象不可变，且重写了 equals 和 hashcode 方法。不可变性是必要的，如果 key 的 hashcode 存入和获取是不一致，就无法找到。获取对象时需要用到 equals 和 hashCode 方法，正确的重写这两个方法是非常重要的，因为两个不相等的对象返回不同的 hashCode 的话，碰撞的几率就会小些，就可以提高 HashMap 的性能。

### final、finally、finalize 的区别  
final 用于修饰属性、方法和类，分别表示属性不可变，方法不可覆盖，类不可继承。finally 是异常处理语句结构的一部分，表示总是执行。finalize 是 Object 类的一个方法，在 GC 执行时会调用被回收对象的此方法。

### sleep() 和 wait() 的区别  
sleep() 是 Thread 类的，wait() 是 Object 类的方法 sleep 不会释放锁，wait 会释放锁。sleep 可在任意地方使用，wait notify notifyAll 只能在 synchronized 块。sleep 必须捕获异常，而 wait 不需要。

### 抽象类和接口的区别、以及使用场景  
抽象类中可以有构造方法、静态方法、普通方法、普通成员变量。接口中不能有。抽象类中的抽象方法访问类型可以是 public、protected 和默认类型，接口中只能是 public。抽象类中的静态成员变量访问类型可以任意，接口中只能是 public 的。一个类只能继承一个类，但是可以实现多个接口。抽象类和子类为“是不是”的关系。主要用于为一些类提供公共实现代码。接口和实现为“有没有”的关系。主要用于代码的扩展性和可维护性。

### Overload（重载）和 Override（重写）的区别  
重载是一个类中多态性的一种表现，在一个类中定义了多个同名的方法，他们有不同的参数列表。重写是父类与子类之间多态的一种表现，子类中定义了与父类有相同名称和参数的方法时，子类对象使用该方法会调用子类中的定义。

### forward（转发）和 redirect（重定向）的区别  
forward 是服务器请求资源，服务器访问目标 URL，把响应内容发给用户，用户不知道数据是从哪来的。redirect 是服务器向客户端发送一个状态码，告知重新请求该 URL。

### 连接池的工作机制  
服务器启动时会建立一定数量的池连接，客户端需要连接时，池会返回一个未使用的连接并将其标记为忙，如果没有空闲连接，池会新建一定数量的连接，当连接使用完毕后，池会将其标记为空闲。

### 什么是序列化  
序列化就是一种用来处理对象流的机制，就是将对象的内容进行流化，可以对流化后的对象进行读写操作，也可以将流化后的对象传输于网络之间。可通过实现 java.io.Serializable 接口来实现序列化。

### 第三方框架部分  
### 什么是 AOP、Spring AOP 的底层原理是什么  
AOP 是面向切面编程，用于在不改变原有逻辑的基础上增加一些额外的功能，如事务管理、日志、缓存、权限控制等。Spring AOP 是基于代理的。如果目标对象实现了接口，则默认采用 JDK 动态代理。如果目标对象没有实现接口，则采用 CgLib 进行动态代理。如果目标对象实现了接口，且强制 CgLib 代理，则采用 CgLib 动态代理。

### 什么是 IOC、IOC 注入方式有哪些  
IOC 翻译为控制反转，他还有个别名为 DI（依赖注入）。IOC 就是由 IOC 容器来负责对象的生命周期和对象之间的关系。控制反转就是本来应该你做的事情，让系统去做，比如通常获取一个对象需要通过 new，而使用 IOC 则是 IOC 将对象创建后注入到被注入的对象中。注解注入（Spring）、构造器注入、setter 方法注入、接口方式注入（不推荐）

### Spring Boot 的核心注解是什么，它是由哪几个注解组成的  
核心注解：@SpringBootApplication 包含： @SpringBootConfiguration 实现配置文件功能 @EnableAutoConfiguration 打开自动配置功能 @CompoentScan 组件扫描功能

### SpringBoot 怎么读取配置文件  
属性上使用@Value 注解 类上使用@ConfigurationProperties 注解 读取指定文件注解可在类上使用@PropertySource（不支持 yml 文件读取）注入 Environment 对象获取到。

### SpringCloud 和 Dubbo 的区别  
SpringCloud 采用基于 HTTP 的 REST API，Dubbo 采用 RPC 方式。

### SpringCloud 的 Hystrix 断路器特性  
请求熔断：请求服务失败量超过一定比例（默认 50%）断路器会切换到开路状态，这时所有请求不会发送到后端服务，断路器在保持开路状态一段时间后（默认 5 秒），自动切换到半开路状态。这时如果下一次请求成功，断路器切回闭路状态，否则重新切换到开路状态。服务降级：对于查询操作，可以实现一个 fallback 方法。当请求服务出现异常时，可以使用 fallback 方法返回的值。依赖隔离：通过线程池来实现资源隔离，比如一个服务调用另外两个服务，如果这两个服务在同一线程池，那么如果一个服务卡住，后面的请求又来了，就会导致后面的请求都会卡住等待。请求缓存：缓存上次请求结果，返回给后续请求。请求合并：把多个请求合并成一个请求，提升效率。

### MySQL 数据库部分  
### 事物的四大特性和隔离级别  
原子性：不可分割的操作单元，要么全部成功，要么回滚。一致性：如果执行事物之前数据库是一致的，那么执行后还是一致的。隔离性：事物操作之间彼此独立和透明，互不影响。持久性：事物一旦提交，其结果就是永久的。未提交读：允许脏读，其他事物只要修改了数据，即使未提交，本事物也能看到修改后的数据值。提交读：只能读取到已提交的数据。可重复读（innoDB 默认）：无论其他事物是否修改并提交了数据，这个事物中的数据不受影响。串行读：完全串行化的读，每次读都要获得锁，读写相互都会阻塞。

### MySQL 优化相关  
使用更小的整数类型、尽可能的定义字段为 not null（否则会导致索引复杂）、只创建需要的索引、分库分表。使用 explain 检查复杂 SQL 语句、LIMIT 语句尽量要跟 order by 或 distinct、插入多条数据时使用单条 INSERT 语句。

### MySQL 存储引擎 InnoDB 和 MyISAM 的区别  
InnoDB 支持事物，MyISAM 不支持。InnoDB 支持外键，MyISAM 不支持。InnoDB 是聚集索引，MyISAM 是非聚集索引。索引和数据文件是分离的。InnoDB 必须要有主键（没有会自己找或创建），MyISAM 可以没有。InnoDB 不保存表的行数，MyISAM 用了一个变量保存表的行数。InnoDB 支持表、行级锁 默认行级锁，MyISAM 只支持表级锁。

### MySQL 在哪些情况下不使用索引  
like 查询使用%开头不能使用索引，但用%结尾的可以使用索引。where 语句中使用<>或!=。where 语句中使用 or，且没有把 or 中的所有字段加上索引。where 语句中对字段表达式操作。where 语句中使用 NOT IN。使用简单的 IN 会使用索引。

### MySQL 分库分表策略  
垂直切分：某个表字段过多，可以将不常用或字段长度较大的字段拆分出去到扩展表中。水平切分：分为库内分表和分库分表，是根据表内数据的逻辑关系，按照不同的条件分散到多个数据库或表中。

### MySQL 三个范式  
1. 满足原子性
2. 满足唯一性
3. 满足无传递依赖（每个字段依赖且仅依赖于主键

常用的 SQL 语句


```
CREATE DATABASE <database_name> DEFAULT CHARACTER SET utf8;
ALTER DATABASE <database_name>;
DROP DATABASE [IF EXISTS] <database_name>;
SHOW DATABASES LIKE <module> WHERE <condition>;
USE <database_name>;
CREATE TABLE <table_name>;
DELETE TABLE <table_name>;
INSERT INTO <table_name> (column1,column2,...) VALUES (value1,value2,...);
UPDATE <table_name> SET column1=1,column2=2 WHERE id=61618;
DELETE FROM <table_name> WHERE <condition>;
SELECT * FROM <table_name> WHERE <condition>;
TRUNCATE TABLE <table_name>
MySQL存储引擎
SHOW ENGINES;
MySQL数据类型
```
1. 整型：TINYINT, SMALLINT, MEDIUMINT, INT, BIGINT
2. 浮点型：FLOAT, DOUBLE, DECIMAL(可变)
3. 字符串：CHAR(8), VARCHAR(255)
4. 文本：TEXT, BLOB
5. 时间：DATE, TIME, DATETIME, TIMESTAMP, YEAR

### MySQL 修改表操作  

```
ALTER TABLE <table_name> ADD <columnN> VARCHAR(50) NOT NULL;
-- 修改字段定义;
ALTER TABLE <table_name> MODIFY <columnN> VARCHAR(50);
-- 展示数据表;
DESC <table_name>;
ALTER TABLE <table_name> CHANGE COLUMN <old_column> <new_column>;
ALTER TABLE <table_name> DROP <column>;
ALTER TABLE <table_name> RENAME AS <new_table_name>;
RENAME TABLE <table_name> <new_table_name>;
DROP TABLE <table_name>;
CREATE TABLE <table_name> LIKE <back_table_name>;
MySQL运算符
```
1. + - \* /
2. = < > <= >= !=
3. is null, is not null, between and, in , not in, like, not like, regexp
4. AND OR XOR NOT

### MySQL 流程控制  
### IF  

```
IF <condition> THEN
...
ELSE IF <condition> THEN
...
ELSE 
...
END IF
```
### CASE  

```
CASE <var>
WHEN <val> THEN
...
WHEN <val> THEN
...
WHEN <val> THEN
...
END CASE
WHILE
WHILE <condition> THEN
...
END WHILE
```
### MySQL 多表联查  
### 内连接  
两个表存在相同的字段

### 外连接  

```
LEFT JOIN
RIGHT JOIN
```
这种查询建议选择写一段代码进行，提升可读性。

### MySQL 子查询  

```
IN, <compare>, EXISTS, ANY(挑一个), ALL(选全部)
-- 基本语法, 两个表可以相同也可以不同
SELECT <columns> FROM <table1_name> WHERE <key?> <subQuery> ( SELECT <columns> FROM <table2_name>)

-- 例如
SELECT <columns> FROM <table1_name> WHERE id IN( SELECT id FROM <table1_name> WHERE id BETWEEN 7 AND 10)
SELECT <columns> FROM <table1_name> WHERE id > ANY( SELECT id FROM <table1_name> WHERE id BETWEEN 7 AND 10)
```
### MySQL 索引  
主键是一种特殊的索引

### 存储过程与函数  
主要区别在于，存储过程一般用于增删改，而函数一般用于计算结果，不改动数据库本身。

### 存储过程  

```
CREATE PROCEDURE procedure_name (IN parameter INTEGER)
BEGIN
IF <condition> THEN
...
END IF

WHILE <condition> THEN
...
END WHILE

CASE <var>
WHEN 1 THEN
...
WHEN 2 THEN
...
END CASE

END
-- 调用
@parameter=7;
CALL procedure_name(@parameter);
-- 删除
DROP PROCEDURE procedure_name;
```
### 函数  

```
CREATE FUNCTION func_name (parameter INTEGER)
RETURNS VARCHAR(255)
BEGIN
RETURN (SELECT <column> FROM <table_name> WHERE id = parameter)
END
-- 调用
@parameter=5;
func_name(@parameter);
-- 删除
DROP FUNCTION func_name
```
