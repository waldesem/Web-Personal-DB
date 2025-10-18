export async function refreshToken(refreshToken: string): Promise<string> {
  const { access_token } = (await $fetch("/routes/auth/refresh", {
    method: "POST",
    body: {
      refresh_token: `Bearer ${refreshToken}`,
    }
  })) as { access_token: string };
  return access_token;
}
