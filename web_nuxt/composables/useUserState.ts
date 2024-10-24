import { Buffer } from "buffer";
import type { User } from "@/types/interfaces";

export const useUserState = () => {
  if (userToken.value) {
    const cridentials = userToken.value.split(" ");
    if (cridentials.length > 1) {
      const payloads = cridentials[1].split(".");
      if (payloads.length > 1) {
        const user = useState(
          "user",
          () =>
            JSON.parse(Buffer.from(payloads[1], "base64").toString()) as User
        );
        if (user.value) return user as Ref<User>;
      }
    }
  }
  return {} as Ref<User>;
};
