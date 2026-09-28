export type CatalogTopic = 'alergia' | 'solar' | 'hidratacion'

export function useCatalog() {
  const query = useState('catalog-query', () => '')
  const topic = useState<CatalogTopic>('catalog-topic', () => 'alergia')

  return { query, topic }
}
