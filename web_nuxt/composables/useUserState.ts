import { Buffer } from "buffer";
import type { User } from "@/types/interfaces";

export const useUserState = () => {
  if (!userToken.value) {
    return {} as Ref<User>;
  }
  const payload = ref(userToken.value.split(" ")[1]);
  const user = useState(
    "user",
    () =>
      JSON.parse(
        Buffer.from(payload.value.split(".")[1], "base64").toString()
      ) as User
  );
  return user as Ref<User>;
};

// export const useUserState = () => {
//   if (!cookies.value) {
//     return {} as Ref<User>;
//   }
//   const user = useState(
//     "user",
//     () =>
//       cookies.value
//   );
//   return user as unknown as Ref<User>;
// };
