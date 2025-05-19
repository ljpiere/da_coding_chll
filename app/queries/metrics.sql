-- app/queries/metrics.sql
/* Q1: Hires by dept & job, 2021 quarterly */
WITH base AS (
  SELECT d.department,
         j.job,
         EXTRACT(quarter FROM h.datetime) AS qtr
  FROM hired_employees h
  JOIN departments d ON d.id = h.department_id
  JOIN jobs j        ON j.id = h.job_id
  WHERE DATE_TRUNC('year', h.datetime) = DATE '2021-01-01'
)
SELECT department,
       job,
       COUNT(*) FILTER (WHERE qtr = 1) AS q1,
       COUNT(*) FILTER (WHERE qtr = 2) AS q2,
       COUNT(*) FILTER (WHERE qtr = 3) AS q3,
       COUNT(*) FILTER (WHERE qtr = 4) AS q4
FROM base
GROUP BY department, job
ORDER BY department, job;

/* Q2: Departments above average hires 2021 */
WITH hires AS (
  SELECT department_id, COUNT(*) AS hired
  FROM hired_employees
  WHERE DATE_TRUNC('year', datetime) = DATE '2021-01-01'
  GROUP BY department_id
),
avg_hires AS (SELECT AVG(hired)::NUMERIC AS avg FROM hires)
SELECT d.id,
       d.department,
       h.hired
FROM hires h
JOIN departments d ON d.id = h.department_id
CROSS JOIN avg_hires a
WHERE h.hired > a.avg
ORDER BY h.hired DESC;
