export default defineEventHandler(async(event) => {
  const item = getRouterParam(event, 'item')
  const item_id = getRouterParam(event, 'item_id')
  const file = await readBody(event)
  return { item: item, item_id: item_id, file: file }
})