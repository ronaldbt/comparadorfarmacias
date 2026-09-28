export default defineCachedEventHandler(async (event) => {
  const query = getQuery(event)
  const q = readConsulta(query.q)
  const tipo = readTipo(query.tipo)
  const coords = readCoords(query.lat, query.lng)

  if (!q) {
    throw createError({ statusCode: 400, statusMessage: 'Escribe al menos 2 letras del medicamento.' })
  }

  const avisos: string[] = []
  const [fonasa, simi] = await Promise.all([
    buscarFonasa(q, tipo, coords).catch(() => {
      avisos.push('El buscador de Fonasa no respondió. Intenta de nuevo en un momento.')
      return []
    }),
    buscarSimi(q).catch(() => {
      avisos.push('La búsqueda pública de Dr. Simi no respondió.')
      return []
    })
  ])

  return { consulta: q, tipo, fonasa, simi, avisos }
}, {
  maxAge: 60 * 10,
  getKey: (event) => {
    const query = getQuery(event)
    return `comparar:v2:${readConsulta(query.q)}:${readTipo(query.tipo)}:${readCoords(query.lat, query.lng).lat}:${readCoords(query.lat, query.lng).lng}`
  }
})
