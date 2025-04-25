<script setup lang="ts">
import type { Address } from "@/types";

await preloadComponents("DivsItemsAddressItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const address = ref({} as Address);
const addresses = ref<Address[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("addresses", async () => {
  addresses.value = (await authFetch(
    "/route/items/addresses/" + candId.value
  )) as Address[];
});

async function submitAddress(form: Address) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/addresses/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  address.value = {} as Address;
  await refresh();
  emitMessage(message);
}

async function deleteAddress(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/addresses/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  index.value = 0;
  if (message == "success") {
    addresses.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <UCard
    class="m-2"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <USwitch
      v-if="editable"
      v-model="edit"
      :label="edit ? 'Отключить редактирование' : 'Включить редактирование'"
      size="xs"
      class="mb-2 me-2 justify-end"
    />
    <div v-for="(item, idx) in addresses" :key="idx" class="p-1">
      <UCard class="m-2">
        <div class="flex">
          <div v-if="edit" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="address" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsAddressItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <template v-if="edit" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Адреса"
        description="Данные профиля"
      >
        <template #content>
          <UCard class="m-2">
            <FormsAddressForm
              :address="address"
              @cancel="
                address = {} as Address;
                modal = false;
              "
              @update="submitAddress"
            />
          </UCard>
        </template>
      </UModal>
      <UButton
        icon="i-heroicons-document-plus"
        label="Добавить"
        variant="ghost"
        @click="
          address = {} as Address;
          modal = true;
        "
      />
      <ElementsDivMenu
        @update="
          address = addresses[index];
          modal = true;
        "
        @delete="deleteAddress(addresses[index].id, index)"
      />
    </template>
  </UCard>
</template>
