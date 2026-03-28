export const useEditStore = defineStore("editable", () => {
  const personStore = usePersonStore();

  const userStore = useUserStore();

  const editable = computed(() => {
    return (
      personStore.person.editable &&
      userStore.user?.role === "user" &&
      userStore.user?.id === personStore.person.user_id &&
      !personStore.person.locked
    );
  });

  return { editable };
});
