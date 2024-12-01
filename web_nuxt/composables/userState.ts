import { Buffer } from "buffer";
import type { Token } from "@/types";

export const useUserState = () => {
  if (accessToken.value) {
    const cridentials = accessToken.value.split(" ");
    if (cridentials.length > 1) {
      const payloads = cridentials[1].split(".");
      if (payloads.length > 1) {
        const token = useState(
          "user",
          () =>
            JSON.parse(Buffer.from(payloads[1], "base64").toString())
        );
        if (token.value) return token as Ref<Token>;
      }
    }
  }
  return {} as Ref<Token>;
};

export const useRefreshToken = () => {
  if (refreshToken.value) {
    const cridentials = refreshToken.value.split(" ");
    if (cridentials.length > 1) {
      const payloads = cridentials[1].split(".");
      if (payloads.length > 1) {
        const token = useState(
          "token",
          () =>
            JSON.parse(Buffer.from(payloads[1], "base64").toString())
        );
        if (token.value) return token as Ref<Token>;
      }
    }
  }
  return {} as Ref<Token>;
};