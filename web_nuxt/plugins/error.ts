export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.config.errorHandler = async (error) => {
    // handle error, e.g. report to a service
    if (error instanceof Error) {
      if (error.message === "Unauthorized") {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      } else {
        if (error.message === "Forbidden") {
          await nuxtApp.runWithContext(() => navigateTo("/"));
        } else {
          if (error.message === "Not Found") {
            await nuxtApp.runWithContext(() => navigateTo("/"));
          } else {
            if (error.message === "Bad Request") {
              await nuxtApp.runWithContext(() => navigateTo("/"));
            } else {
              if (error.message === "Internal Server Error") {
                await nuxtApp.runWithContext(() => navigateTo("/"));
              } else {
                if (error.message === "Network Error") {
                  await nuxtApp.runWithContext(() => navigateTo("/"));
                } else {
                  if (error.message === "Request failed with status code 401") {
                    await nuxtApp.runWithContext(() => navigateTo("/login"));
                  }
                }
              }
            }
          }
        }
      }
    }
  };
});
