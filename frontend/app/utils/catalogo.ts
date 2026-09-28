import catalogo from '~/data/catalogo.json'

export type OfertaCatalogo = {
  farmacia: string
  precio: number
  detalle?: string | null
  url: string | null
}

export type ProductoCatalogo = {
  id: string
  nombre: string
  marca: string | null
  consulta: string
  destacado: boolean
  ofertas: OfertaCatalogo[]
}

const RETAIL = new Set([
  'Ahumada', 'Dr. Simi', 'Salcobrand', 'Knop', 'La Botika', 'Farmex',
  'EcoFarmacias', 'EasyFarma', 'Novasalud', 'Farmazon',
])

export const productosCatalogo = catalogo.productos as ProductoCatalogo[]
export const catalogoActualizado = catalogo.actualizado as string | null

const clp = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 })

export function dinero(valor: number) {
  return clp.format(valor)
}

export function ahorroEntreFarmacias(ofertas: OfertaCatalogo[]) {
  const precios = ofertas.filter(oferta => RETAIL.has(oferta.farmacia)).map(oferta => oferta.precio)
  if (precios.length < 2) return null
  const mayor = Math.max(...precios)
  const menor = Math.min(...precios)
  if (mayor <= 0 || mayor === menor || mayor / menor > 2.5) return null
  return Math.round((1 - menor / mayor) * 100)
}

export function ofertasOrdenadas(ofertas: OfertaCatalogo[]) {
  return [...ofertas].sort((a, b) => a.precio - b.precio)
}

export function menorPrecio(ofertas: OfertaCatalogo[]) {
  return Math.min(...ofertas.map(oferta => oferta.precio))
}
