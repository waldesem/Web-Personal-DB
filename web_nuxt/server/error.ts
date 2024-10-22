export default defineNitroErrorHandler((error, event) => {
  setResponseHeader(event, 'Content-Type', 'text/plain')
  return send(event, error.stack)
});
