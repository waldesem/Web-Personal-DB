<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa, stateUser, stateClassify } from "@/state";
import { Address } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const AddressForm = defineAsyncComponent(
  () => import("@components/content/forms/AddressForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const actions = ref(false);
const edit = ref(false);
const itemId = ref('');
const address = ref(<Address>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapseAddress = document.getElementById("addresser");
  collapseAddress?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <DropDownHead :id="'addresser'" :header="'Адреса'" />
  <div class="collapse card card-body mb-3" id="addresser">
    <AddressForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.addresses.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.addresses"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <AddressForm 
        v-if="edit && itemId == item['id'].toString()" 
        :addrs="address" 
        @cancel="cancelAction" 
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="
                actions &&
                stateAnketa.anketa.persons['user_id'] == stateUser.userId &&
                stateAnketa.anketa.persons['standing']
              "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'addresses')"
            @update="
              address = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Тип'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Адрес'">{{ item["addresses"] }}</LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>
