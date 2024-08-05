<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/utils/state";
import type { Address } from "@/utils/interfaces";

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
  <ElementsDropDownHead :id="'addresser'" :header="'Адреса'" />
  <div class="collapse card card-body mb-3" id="addresser">
    <FormsAddressForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.addresses.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.addresses"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <FormsAddressForm 
        v-if="edit && itemId == item['id'].toString()" 
        :addrs="address" 
        @cancel="cancelAction" 
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
                actions &&
                stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
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
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Тип'">{{ item["view"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Адрес'">{{ item["addresses"] }}</ElementsLabelSlot>
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
