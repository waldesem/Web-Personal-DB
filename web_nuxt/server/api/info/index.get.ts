export default defineEventHandler((event) => {
  const region = getQuery(event).region
  const start = getQuery(event).start
  const end = getQuery(event).end
  return { region: region, start: start, end: end }
})