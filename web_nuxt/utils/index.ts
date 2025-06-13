import type { NitroFetchOptions } from "nitropack";
import type { ToastProps } from "@nuxt/ui";
import type { Method } from "@/types";

export const fetchAuth = async (
  url: string,
  options: NitroFetchOptions<ResponseType, Method> = {}
) => {
  options.headers = {
    ...options.headers,
    Authorization: `${accessToken.value}`,
  };
  try {
    return await $fetch(url, options);
  } catch (error) {
    console.error(error);
    await navigateTo("/login");
  }
};

export const makeToast = (
  color: ToastProps["color"] = "error",
  description = "Невозможно выполнить действие или операция завершилсь ошибкой"
) => {
  const icon = {
    error: "i-heroicons-exclamation-triangle",
    info: "i-heroicons-exclamation-circle",
    success: "i-heroicons-information-circle",
  };
  const title = {
    error: "Ошибка",
    info: "Внимание",
    success: "Успех",
  };
  const toast = useToast();
  toast.add({
    icon: icon[color as keyof typeof icon],
    title: title[color as keyof typeof title],
    description: description,
    color: color,
  });
};

export async function decompressGzip(compressedBuffer: Buffer) {
  const cs = new DecompressionStream("gzip");
  const writer = cs.writable.getWriter();
  writer.write(compressedBuffer);
  writer.close();

  const reader = cs.readable.getReader();
  let result = new Uint8Array();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const newResult = new Uint8Array(result.length + value.length);
    newResult.set(result, 0);
    newResult.set(value, result.length);
    result = newResult;
  }
  return result;
}

// const buffer = Buffer.from(data);
//   const compressedBuffer = new Uint8Array([buffer]);
//   decompressGzip(compressedBuffer)
//     .then(decompressedBuffer => {
//       candidates.value = JSON.parse(new TextDecoder().decode(decompressedBuffer));
//   })
//     .catch(error => {
//       console.error('Error:', error);
//   });
