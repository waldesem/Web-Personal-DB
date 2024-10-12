export default defineEventHandler((event) => {
  const image = getQuery(event).image
  return { image: image }
})