SELECT COUNT(*) AS repes, titulo, id
FROM articulos
GROUP BY id
ORDER BY repes DESC;