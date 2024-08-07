<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Contact } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const itemId = ref('');
const edit = ref(false);
const contact = ref(<Contact>{});

function cancelAction(){
  edit.value = false;
  itemId.value = "";
  const collapseContact = document.getElementById('contacter');
  collapseContact?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <ElementsDropDownHead :id="'contacter'" :header="'Контакты'"/>
  <div class="collapse card card-body mb-3" id="contacter">
    <FormsContactForm @cancel="cancelAction"/>
  </div>
  <div v-if="anketaState.anketa.value.contacts.length"> 
    <div 
      v-for="(item, idx) in anketaState.anketa.value.contacts" :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false" 
      class="card card-body mb-3"
    >
      <FormsContactForm
        v-if="edit && itemId == item['id'].toString()" 
        :contact="contact"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons 
            v-show="actions &&
              anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']"
            @delete="anketaState.deleteItem(item['id'].toString(), 'contacts')"
            @update="
              contact = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Вид'">{{ item['view'] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Контакт'">{{ item['contact'] }}</ElementsLabelSlot>
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