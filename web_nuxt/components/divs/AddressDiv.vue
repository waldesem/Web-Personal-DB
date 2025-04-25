<script setup lang="ts">
import type { Address } from "@/types";

await preloadComponents("DivsItemsAddressItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

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
  <UCard class="m-2" :class="{ 'animate-pulse': status == 'pending' || pending }">
    <div v-for="(item, idx) in addresses" :key="idx" class="p-1">
       <UCard class="m-2">
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
      <ElementsDivMenu
        :items="addresses.length"
        @delete="deleteAddress(addresses[index].id, index)"
        @update="
          address = addresses[index];
          modal = true;
        "
        @create="
          address = {} as Address;
          modal = true;
        "
      />
    </template>
  </UCard>
</template>