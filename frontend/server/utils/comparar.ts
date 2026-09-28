export const SANTIAGO = { lat: -33.4489, lng: -70.6693 }

export type TipoBusqueda = 'nombre' | 'principio'

export function readCoords(latRaw: unknown, lngRaw: unknown) {
  const lat = Number(latRaw)
  const lng = Number(lngRaw)
  if (!Number.isFinite(lat) || !Number.isFinite(lng)) return SANTIAGO
  if (lat < -56 || lat > -17 || lng < -110 || lng > -66) return SANTIAGO
  return { lat, lng }
}

export function readTipo(value: unknown): TipoBusqueda {
  return value === 'principio' ? 'principio' : 'nombre'
}

export function readConsulta(value: unknown) {
  const q = String(value ?? '').replace(/\s+/g, ' ').trim()
  if (q.length < 2 || q.length > 80) return ''
  return q
}

export function toClpNumber(value: unknown) {
  const n = Number(String(value ?? '').replace(',', '.'))
  return Number.isFinite(n) ? Math.round(n) : null
}

type FonasaProducto = {
  id: number
  nombreMedicamento: string
  principioActivo1: string | null
  presentacion: string
  accionTerapeutica: string | null
  laboratorio: string | null
  equivalencia: string | null
  registroSanitario: string | null
  ofertaFonasa: string | null
}

type FonasaObtener = {
  codigo_salida?: number
  mensaje_salida?: string
  listado?: Array<{
    presentacionesExistentes?: Array<{
      productos?: FonasaProducto[]
    }>
  }>
}

export type MedicamentoFonasa = {
  clave: string
  nombre: string
  principio: string | null
  presentacion: string
  accion: string | null
  laboratorio: string | null
  equivalencia: string | null
  registro: string | null
  ofertaFonasa: number | null
}

const fonasaHeaders = {
  accept: 'application/json',
  origin: 'https://medicamentos.fonasa.cl',
  referer: 'https://medicamentos.fonasa.cl/'
}

export async function buscarFonasa(q: string, tipo: TipoBusqueda, coords: { lat: number, lng: number }) {
  const data = await $fetch<FonasaObtener>('https://api.fonasa.cl/medicamentos/obtener', {
    method: 'POST',
    headers: fonasaHeaders,
    timeout: 15000,
    body: {
      latitud: String(coords.lat),
      longitud: String(coords.lng),
      nombreMedicamento: tipo === 'nombre' ? q : null,
      principioActivo: tipo === 'principio' ? q : null
    }
  })

  const medicamentos: MedicamentoFonasa[] = []
  for (const grupo of data.listado ?? []) {
    for (const presentacion of grupo.presentacionesExistentes ?? []) {
      for (const producto of presentacion.productos ?? []) {
        const registro = producto.registroSanitario ?? ''
        const presentacionTexto = producto.presentacion ?? ''
        const laboratorio = producto.laboratorio ?? ''
        medicamentos.push({
          clave: `${registro}|${presentacionTexto}|${laboratorio}|${medicamentos.length}`,
          nombre: producto.nombreMedicamento,
          principio: producto.principioActivo1,
          presentacion: presentacionTexto,
          accion: producto.accionTerapeutica,
          laboratorio,
          equivalencia: producto.equivalencia,
          registro: producto.registroSanitario,
          ofertaFonasa: toClpNumber(producto.ofertaFonasa)
        })
      }
    }
  }

  medicamentos.sort((a, b) => (a.ofertaFonasa ?? Number.MAX_SAFE_INTEGER) - (b.ofertaFonasa ?? Number.MAX_SAFE_INTEGER))
  return medicamentos.slice(0, 24)
}

type SucursalFonasa = {
  nombreFarmacia?: string
  nombreSucursal?: string
  direccion?: string
  comuna?: string
  distancia?: number
  precioNormal?: string
  ofertaFonasa?: string
  ahorro?: string
  lunes?: string
  sabado?: string
  domingo?: string
  domungo?: string
}

type FonasaDetalle = {
  Farmacias?: Array<{ nombre?: string, data?: SucursalFonasa[] }>
}

export type Sucursal = {
  farmacia: string
  sucursal: string
  direccion: string
  comuna: string
  distancia: number | null
  precioNormal: number | null
  ofertaFonasa: number | null
  ahorro: number | null
  ahorroAnual: number | null
  horario: string
}

export async function farmaciasFonasa(input: {
  lat: number
  lng: number
  nombre: string
  registro: string
  presentacion: string
  laboratorio: string
}) {
  const data = await $fetch<FonasaDetalle>('https://api.fonasa.cl/medicamentos/detalle', {
    method: 'POST',
    headers: fonasaHeaders,
    timeout: 15000,
    body: {
      latitud: String(input.lat),
      longitud: String(input.lng),
      nombreMedicamento: input.nombre,
      registroSanitario: input.registro,
      presentacion: input.presentacion,
      laboratorio: input.laboratorio
    }
  })

  const sucursales: Sucursal[] = []
  for (const grupo of data.Farmacias ?? []) {
    for (const local of grupo.data ?? []) {
      const ahorro = toClpNumber(local.ahorro)
      const domingo = local.domingo || local.domungo
      sucursales.push({
        farmacia: local.nombreFarmacia || grupo.nombre || 'Farmacia',
        sucursal: local.nombreSucursal || '',
        direccion: local.direccion || '',
        comuna: local.comuna || '',
        distancia: typeof local.distancia === 'number' ? local.distancia : null,
        precioNormal: toClpNumber(local.precioNormal),
        ofertaFonasa: toClpNumber(local.ofertaFonasa),
        ahorro,
        ahorroAnual: ahorro == null ? null : ahorro * 12,
        horario: [local.lunes && `Lun–vie ${local.lunes}`, local.sabado && `Sáb ${local.sabado}`, domingo && `Dom ${domingo}`]
          .filter(Boolean)
          .join(' · ')
      })
    }
  }

  sucursales.sort((a, b) => (a.distancia ?? Number.MAX_SAFE_INTEGER) - (b.distancia ?? Number.MAX_SAFE_INTEGER))
  return sucursales.slice(0, 8)
}

type SimiOffer = {
  Price?: number
  ListPrice?: number
  IsAvailable?: boolean
}

type SimiProduct = {
  productName?: string
  brand?: string
  link?: string
  Bioequivalente?: string[]
  'Principio Activo'?: string[]
  'Registro Sanitario'?: string[]
  items?: Array<{ sellers?: Array<{ commertialOffer?: SimiOffer }> }>
}

export type PrecioSimi = {
  nombre: string
  marca: string | null
  principio: string | null
  bioequivalente: boolean
  precio: number | null
  precioLista: number | null
  disponible: boolean
  registro: string | null
  url: string | null
}

export async function buscarSimi(q: string) {
  const data = await $fetch<SimiProduct[]>(
    `https://www.drsimi.cl/api/catalog_system/pub/products/search/${encodeURIComponent(q)}`,
    {
      query: { _from: 0, _to: 7 },
      headers: { accept: 'application/json' },
      timeout: 12000
    }
  )

  return (Array.isArray(data) ? data : []).map((producto) => {
    const offer = producto.items?.[0]?.sellers?.[0]?.commertialOffer
    return {
      nombre: producto.productName || 'Medicamento',
      marca: producto.brand || null,
      principio: producto['Principio Activo']?.[0] || null,
      bioequivalente: producto.Bioequivalente?.[0] === 'SI',
      precio: toClpNumber(offer?.Price),
      precioLista: toClpNumber(offer?.ListPrice),
      disponible: Boolean(offer?.IsAvailable),
      registro: producto['Registro Sanitario']?.[0] || null,
      url: producto.link || null
    } satisfies PrecioSimi
  })
}
