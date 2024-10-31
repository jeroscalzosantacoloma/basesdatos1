SELECT s.id, s.name, c.title 
FROM students s 
INNER JOIN enrollments e ON s.id = e.student_id 
INNER JOIN courses c ON e.course_id = c.id;

SELECT s.id, s.name, c.title 
FROM students s 
LEFT JOIN enrollments e ON s.id = e.student_id 
LEFT JOIN courses c ON e.course_id = c.id;

SELECT c.id, c.title, s.name 
FROM courses c 
RIGHT JOIN enrollments e ON c.id = e.course_id 
RIGHT JOIN students s ON e.student_id = s.id;

SELECT MAX(age) AS max_age FROM students;
SELECT MIN(age) AS min_age FROM students;
SELECT AVG(age) AS avg_age FROM students;

SELECT c.title, AVG(e.grade) AS avg_grade 
FROM courses c 
INNER JOIN enrollments e ON c.id = e.course_id 
GROUP BY c.title;

SELECT c.title, MAX(e.grade) AS max_grade 
FROM courses c 
LEFT JOIN enrollments e ON c.id = e.course_id 
GROUP BY c.title;

SELECT c.title, MIN(e.grade) AS min_grade 
FROM courses c 
RIGHT JOIN enrollments e ON c.id = e.course_id 
GROUP BY c.title;

SELECT s.name, e.grade 
FROM students s 
INNER JOIN enrollments e ON s.id = e.student_id 
WHERE e.grade > 8;

SELECT s.name, COALESCE(c.title, 'Sin curso') AS course_title 
FROM students s 
LEFT JOIN enrollments e ON s.id = e.student_id 
LEFT JOIN courses c ON e.course_id = c.id;

SELECT c.title, COUNT(e.student_id) AS student_count 
FROM courses c 
LEFT JOIN enrollments e ON c.id = e.course_id 
GROUP BY c.title;

SELECT s.name, c.title, e.enrollment_date 
FROM students s 
INNER JOIN enrollments e ON s.id = e.student_id 
INNER JOIN courses c ON e.course_id = c.id;

SELECT c.title, COUNT(e.id) AS total_enrollments 
FROM courses c 
LEFT JOIN enrollments e ON c.id = e.course_id 
GROUP BY c.title;

SELECT c.title, AVG(e.grade) AS avg_grade, MAX(e.grade) AS max_grade 
FROM courses c 
INNER JOIN enrollments e ON c.id = e.course_id 
GROUP BY c.title;
