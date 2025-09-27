export async function refreshToken(refreshToken: string): Promise<string> {
  const { access_token } = (await $fetch("/routes/auth/refresh", {
    headers: {
      Authorization: "Bearer " + refreshToken,
    },
    method: "POST",
  })) as { access_token: string };
  return access_token;
}
