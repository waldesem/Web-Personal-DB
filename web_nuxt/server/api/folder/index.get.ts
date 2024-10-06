export default defineEventHandler((event) => {
  const folder = getQuery(event).folder
  return { folder: folder }
})