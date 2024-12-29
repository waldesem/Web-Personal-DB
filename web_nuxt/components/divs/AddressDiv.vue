<script setup lang="ts">
import type { Address } from "@/types";

prefetchComponents("FormsAddressForm");

const emit = defineEmits(["message"]);

const authFetch = useFetchAuth();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const modal = ref(false);
const pending = ref(false);
const itemId = ref("");
const address = ref({} as Address);
const addresses = ref<Address[]>([]);

const { refresh, status } = await useLazyAsyncData("addresses", async () => {
  addresses.value = (await authFetch(
    "/route/items/addresses/" + props.candId
  )) as Address[];
});

async function submitAddress(form: Address) {
  closeAction();
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/addresses/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  await refresh();
  emit("message", message);
}

async function deleteAddress(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/addresses/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    addresses.value.splice(idx, 1);
  }
  emit("message", message);
}

function closeAction() {
  modal.value = false;
  itemId.value = "";
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :loading="status == 'pending' || pending"
    label="Добавить запись"
    variant="link"
    @click="modal = !modal"
  />
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsAddressForm
        :addrs="address"
        @cancel="closeAction"
        @update="submitAddress"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in addresses" :key="idx" class="py-3">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Тип'">{{
        item["view"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Адрес'">{{
        item["addresses"]
      }}</ElementsLabelSlot>
      <template v-if="props.editable" #footer>
        <ElementsNavSimpHoriz
          @delete="deleteAddress(item['id'], idx)"
          @update="
            address = item;
            itemId = item['id'];
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
