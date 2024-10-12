export default defineEventHandler((event) => {
  const item_id = getRouterParam(event, 'item_id')
  return { item_id: item_id }
})