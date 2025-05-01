<script setup lang="ts">
import type { Address } from "@/types";

await preloadComponents("DivsItemsAddressItem");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const address = ref({} as Address);
const addresses = ref<Address[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("addresses", async () => {
  addresses.value = (await useFetchAuth(
    "/route/items/addresses/" + candId.value
  )) as Address[];
});

async function submitAddress(form: Address) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
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
  const { message } = (await useFetchAuth(`/route/items/addresses/${id}`, {
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
    :variant="status == 'pending' || pending ? 'soft' : 'outline'"
    class="my-2 mx-1"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <div v-for="(item, idx) in addresses" :key="idx" class="p-1">
      <UCard :variant="status == 'pending' || pending ? 'soft' : 'outline'">
        <div class="flex">
          <div v-if="editable" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="address" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsAddressItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <div v-if="!addresses.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
    <template v-if="editable" #footer>
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
        :loading="status == 'pending' || pending"
        @click="
          address = {} as Address;
          modal = true;
        "
      />
      <ElementsDivMenu 
        v-if="addresses.length > 0 && (status != 'pending' || !pending)"
        @update="
          address = addresses[index];
          modal = true;
        "
        @delete="deleteAddress(addresses[index].id, index)"
      />
    </template>
  </UCard>
</template>
