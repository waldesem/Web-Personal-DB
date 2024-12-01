import { Buffer } from "buffer";
import type { Token } from "@/types";

export function getPayload(token: string | null = accessToken.value) {
  if (token) {
    const cridentials = token.split(" ");
    if (cridentials.length > 1) {
      const payloads = cridentials[1].split(".");
      if (payloads.length > 1) {
        return JSON.parse(
          Buffer.from(payloads[1], "base64").toString()
        ) as Token;
      }
    }
  }
  return {} as Token;
}


