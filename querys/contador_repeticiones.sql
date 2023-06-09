SELECT COUNT(*) AS cant_repeticiones, titulo FROM articulos
GROUP BY titulo
ORDER BY  cant_repeticiones DESC;