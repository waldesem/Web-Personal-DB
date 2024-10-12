export default defineEventHandler(async(event) => {
  const item = getRouterParam(event, 'item')
  const item_id = getRouterParam(event, 'item_id')
  return { item: item, item_id: item_id }
})