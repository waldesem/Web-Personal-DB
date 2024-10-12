export default defineEventHandler((event) => {
  const person_id = getRouterParam(event, 'person_id')
  const region = getQuery(event).region
  return { region: region, person_id: person_id }
})