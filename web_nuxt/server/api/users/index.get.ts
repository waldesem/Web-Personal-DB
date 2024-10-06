export default defineEventHandler((event) => {
  const search = getQuery(event).search
  return { search: search }
})