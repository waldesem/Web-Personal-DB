import { Buffer } from "buffer";
import type { User } from "@/types/interfaces";

export const useUserState = () => {
  if (userToken.value) {
    const payload = ref(userToken.value.split(" ")[1]);
    const user = useState(
      "user",
      () =>
        JSON.parse(
          Buffer.from(payload.value.split(".")[1], "base64").toString()
        ) as User
    );
    return user as Ref<User>;
  } else if (cookies.value) {
    const authFetch = useFetchAuth();
    const user = useState("user", async () => {
      const response = (await authFetch(`/api/auth`)) as User;
      return response;
    });
    return user as unknown as Ref<User>;
  } else {
    return {} as Ref<User>;
  }
};
