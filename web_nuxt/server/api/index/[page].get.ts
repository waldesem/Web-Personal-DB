export default defineEventHandler((event) => {
  const page = getRouterParam(event, 'page')
  const search = getQuery(event).search
  return { search: search, page: page }
})