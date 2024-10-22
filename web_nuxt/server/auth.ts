export default defineEventHandler((event) => {
  const headers = getRequestHeaders(event);
  const payload = ref(headers.split(" ")[1]);
  const user = JSON.parse(
    Buffer.from(payload.split(".")[1], "base64").toString()
  ) as user;
  const requestURL = getRequestURL(event).pathname as string;
  if (requestURL.startsWith('/index')) {
    console.log(event.context.user)
  }
})

