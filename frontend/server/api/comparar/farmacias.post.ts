export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const coords = readCoords(body?.lat, body?.lng)
  const nombre = readConsulta(body?.nombre)
  const registro = String(body?.registro ?? '').trim().slice(0, 40)
  const presentacion = String(body?.presentacion ?? '').trim().slice(0, 80)
  const laboratorio = String(body?.laboratorio ?? '').trim().slice(0, 120)

  if (!nombre || !registro || !presentacion) {
    throw createError({ statusCode: 400, statusMessage: 'Falta el medicamento para buscar sucursales.' })
  }

  const farmacias = await farmaciasFonasa({
    lat: coords.lat,
    lng: coords.lng,
    nombre,
    registro,
    presentacion,
    laboratorio
  })

  return { farmacias }
})
