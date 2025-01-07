<script setup lang="ts">
import type { Address } from "@/types";
import { emitMessage } from "@/utils";

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const address = ref({} as Address);
const addresses = ref<Address[]>([]);

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
  if (message == "success") {
    addresses.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <div v-if="editable" class="my-3">
    <UButton
      :loading="status == 'pending' || pending"
      :label="
        status == 'pending' || pending
          ? 'Обновление данных...'
          : 'Добавить запись'
      "
      variant="link"
      @click="modal = !modal"
    />
  </div>
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsAddressForm
        :addrs="address"
        @cancel="
          address = {} as Address;
          modal = false;
        "
        @update="submitAddress"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in addresses" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Тип'">{{ item.view }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Адрес'">{{
        item.addresses
      }}</ElementsLabelSlot>
      <template v-if="editable" #footer>
        <ElementsDivMenu
          @delete="deleteAddress(item.id, idx)"
          @update="
            address = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
